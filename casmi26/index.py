"""Mass-pruned spectral retrieval index."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Sequence, Tuple

import numpy as np
import pandas as pd
import pyarrow.parquet as pq
from tqdm import tqdm

from .adducts import ADDUCT_RULES, DIMER_ADDUCTS, infer_neutral_mass
from .config import ARTIFACT_DIR, DOMAIN_PRIOR, RunConfig
from .spectrum import clean_spectrum


@dataclass
class SpectrumIndex:
    neutral_mass: np.ndarray
    precursor_mz: np.ndarray
    order: np.ndarray
    inchikey14: np.ndarray
    smiles: np.ndarray
    library: np.ndarray
    adduct: np.ndarray
    ionization_mode: np.ndarray
    quality: np.ndarray
    exact_mass: np.ndarray
    domain_prior: np.ndarray
    peak_mz: np.ndarray
    peak_intensity: np.ndarray
    collision_energy: np.ndarray

    def save(self, path: Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(
            path,
            neutral_mass=self.neutral_mass,
            precursor_mz=self.precursor_mz,
            order=self.order,
            inchikey14=self.inchikey14,
            smiles=self.smiles,
            library=self.library,
            adduct=self.adduct,
            ionization_mode=self.ionization_mode,
            quality=self.quality,
            exact_mass=self.exact_mass,
            domain_prior=self.domain_prior,
            peak_mz=self.peak_mz,
            peak_intensity=self.peak_intensity,
            collision_energy=self.collision_energy,
        )

    @classmethod
    def load(cls, path: Path) -> "SpectrumIndex":
        data = np.load(path, allow_pickle=True)
        return cls(**{k: data[k] for k in data.files})

    def mass_window(self, mass: float, tol_ppm: float) -> Tuple[int, int]:
        if not np.isfinite(mass) or mass <= 0:
            return 0, 0
        delta = mass * tol_ppm * 1e-6
        lo = int(np.searchsorted(self.neutral_mass, mass - delta, side="left"))
        hi = int(np.searchsorted(self.neutral_mass, mass + delta, side="right"))
        return lo, hi


def _mean_ce(val) -> float:
    if val is None:
        return float("nan")
    arr = np.asarray(val, dtype=np.float64)
    if arr.size == 0:
        return float("nan")
    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        return float("nan")
    return float(arr.mean())


def _quality_score(precursor_error_ppm, num_peaks) -> float:
    err = abs(float(precursor_error_ppm)) if precursor_error_ppm == precursor_error_ppm else 1e6
    q_err = 1.0 / (1.0 + err / 5.0)
    peaks = float(num_peaks) if num_peaks == num_peaks else 0.0
    q_peaks = min(1.0, peaks / 64.0)
    return 0.7 * q_err + 0.3 * q_peaks


def _vector_neutral_mass(precursor_mz: np.ndarray, adducts: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Fast adduct → neutral mass for arrays. Returns (neutral_mass, supported_mask)."""
    n = len(precursor_mz)
    out = np.full(n, np.nan, dtype=np.float64)
    supported = np.zeros(n, dtype=bool)
    # group by adduct string
    adducts = np.asarray(adducts, dtype=object)
    for adduct, rule in ADDUCT_RULES.items():
        mask = adducts == adduct
        if not np.any(mask):
            continue
        p = precursor_mz[mask].astype(np.float64)
        if adduct in DIMER_ADDUCTS:
            nm = (p - rule.delta) / 2.0
        else:
            nm = p * abs(rule.charge) - rule.delta
        out[mask] = nm
        supported[mask] = True
    return out, supported


def build_index_from_train(
    train_path: Path,
    cfg: RunConfig,
    cache_path: Optional[Path] = None,
    max_rows: Optional[int] = None,
    libraries: Optional[Sequence[str]] = None,
) -> SpectrumIndex:
    cache_path = Path(cache_path) if cache_path else ARTIFACT_DIR / "spectrum_index.npz"
    meta_path = cache_path.with_suffix(".meta.json")
    if cache_path.exists():
        print(f"[index] loading cache {cache_path}")
        return SpectrumIndex.load(cache_path)

    t0 = time.time()
    pf = pq.ParquetFile(train_path)
    cols = [
        "ingest_lib",
        "normalized_smiles",
        "inchikey14",
        "ionization_mode",
        "adduct",
        "precursor_mz",
        "precursor_error_ppm",
        "ms2_mzs",
        "ms2_normalized_intensities",
        "num_peaks",
        "collision_energy_ev",
    ]

    chunks = []
    n_unsupported = 0
    n_bad_peaks = 0
    n_kept = 0
    lib_filter = set(libraries) if libraries else None

    for rg_idx in tqdm(range(pf.num_row_groups), desc="index row_groups"):
        if max_rows is not None and n_kept >= max_rows:
            break
        df = pf.read_row_group(rg_idx, columns=cols).to_pandas()
        if lib_filter is not None:
            df = df[df["ingest_lib"].isin(lib_filter)]
        if df.empty:
            continue
        if max_rows is not None:
            remain = max_rows - n_kept
            if len(df) > remain:
                df = df.iloc[:remain]

        precursor = df["precursor_mz"].to_numpy(dtype=np.float64)
        neutral, ok = _vector_neutral_mass(precursor, df["adduct"].to_numpy())
        n_unsupported += int((~ok).sum())
        df = df.loc[ok].copy()
        neutral = neutral[ok]
        precursor = precursor[ok]
        if df.empty:
            continue

        peak_mz = []
        peak_int = []
        keep_mask = []
        mzs_col = df["ms2_mzs"].to_numpy()
        ints_col = df["ms2_normalized_intensities"].to_numpy()
        for i in range(len(df)):
            mz, inten = clean_spectrum(
                mzs_col[i],
                ints_col[i],
                precursor_mz=float(precursor[i]),
                intensity_floor=cfg.intensity_floor,
                top_peaks=cfg.top_peaks,
            )
            if len(mz) < 3:
                keep_mask.append(False)
                peak_mz.append(None)
                peak_int.append(None)
            else:
                keep_mask.append(True)
                peak_mz.append(mz)
                peak_int.append(inten)
        keep_mask = np.asarray(keep_mask, dtype=bool)
        n_bad_peaks += int((~keep_mask).sum())
        if not keep_mask.any():
            continue

        df = df.loc[keep_mask]
        neutral = neutral[keep_mask]
        precursor = precursor[keep_mask]
        peak_mz = [peak_mz[i] for i, k in enumerate(keep_mask) if k]
        peak_int = [peak_int[i] for i, k in enumerate(keep_mask) if k]

        libs = df["ingest_lib"].fillna("unknown").astype(str)
        err = df["precursor_error_ppm"].to_numpy()
        npeaks = df["num_peaks"].to_numpy()
        quality = np.array([_quality_score(e, p) for e, p in zip(err, npeaks)], dtype=np.float32)
        prior = libs.map(lambda x: float(DOMAIN_PRIOR.get(x, 0.3))).to_numpy(dtype=np.float32)
        ce = np.array([_mean_ce(v) for v in df["collision_energy_ev"].to_numpy()], dtype=np.float32)

        chunk = {
            "neutral_mass": neutral.astype(np.float64),
            "precursor_mz": precursor.astype(np.float64),
            "inchikey14": df["inchikey14"].to_numpy(dtype=object),
            "smiles": df["normalized_smiles"].to_numpy(dtype=object),
            "library": libs.to_numpy(dtype=object),
            "adduct": df["adduct"].to_numpy(dtype=object),
            "ionization_mode": df["ionization_mode"].to_numpy(dtype=object),
            "quality": quality,
            "exact_mass": neutral.astype(np.float64),
            "domain_prior": prior,
            "peak_mz": np.asarray(peak_mz, dtype=object),
            "peak_intensity": np.asarray(peak_int, dtype=object),
            "collision_energy": ce,
        }
        chunks.append(chunk)
        n_kept += len(df)

    if not chunks:
        raise RuntimeError("No spectra retained while building index")

    def cat(key, dtype=None):
        arrs = [c[key] for c in chunks]
        if dtype is object or arrs[0].dtype == object:
            return np.concatenate(arrs)
        return np.concatenate(arrs).astype(dtype) if dtype else np.concatenate(arrs)

    neutral_mass = cat("neutral_mass", np.float64)
    order = np.argsort(neutral_mass)
    index = SpectrumIndex(
        neutral_mass=neutral_mass[order],
        precursor_mz=cat("precursor_mz", np.float64)[order],
        order=order,
        inchikey14=cat("inchikey14")[order],
        smiles=cat("smiles")[order],
        library=cat("library")[order],
        adduct=cat("adduct")[order],
        ionization_mode=cat("ionization_mode")[order],
        quality=cat("quality", np.float32)[order],
        exact_mass=cat("exact_mass", np.float64)[order],
        domain_prior=cat("domain_prior", np.float32)[order],
        peak_mz=cat("peak_mz")[order],
        peak_intensity=cat("peak_intensity")[order],
        collision_energy=cat("collision_energy", np.float32)[order],
    )
    index.save(cache_path)
    meta = {
        "n_kept": int(n_kept),
        "n_unsupported": int(n_unsupported),
        "n_bad_peaks": int(n_bad_peaks),
        "elapsed_sec": time.time() - t0,
        "config": cfg.to_dict(),
    }
    meta_path.write_text(json.dumps(meta, indent=2))
    print(
        f"[index] kept={n_kept} unsupported={n_unsupported} bad_peaks={n_bad_peaks} "
        f"elapsed={meta['elapsed_sec']:.1f}s -> {cache_path}"
    )
    return index
