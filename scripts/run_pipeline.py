#!/usr/bin/env python3
"""End-to-end first submission pipeline for Enveda CASMI 2026."""

from __future__ import annotations

import argparse
import json
import random
import time
import traceback
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
import pyarrow.parquet as pq
from tqdm import tqdm

from casmi26.config import (
    ARTIFACT_DIR,
    DATA_DIR,
    OUTPUT_DIR,
    PREFERRED_LIBS,
    RunConfig,
)
from casmi26.index import SpectrumIndex, build_index_from_train
from casmi26.metrics import summarize_metrics
from casmi26.retrieve import aggregate_molecule_candidates
from casmi26.submission import build_submission_frame, validate_submission, write_submission


def set_seeds(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)


def print_versions() -> None:
    import sys
    import rdkit
    import pyarrow

    print("python", sys.version.split()[0])
    print("numpy", np.__version__)
    print("pandas", pd.__version__)
    print("pyarrow", pyarrow.__version__)
    print("rdkit", rdkit.__version__)


def load_test(path: Path) -> pd.DataFrame:
    df = pq.read_table(path).to_pandas()
    # schema checks
    assert "ms2_mzs" in df.columns and "ms2_normalized_intensities" in df.columns
    bad = 0
    for mzs, ints in zip(df["ms2_mzs"], df["ms2_normalized_intensities"]):
        if mzs is None or ints is None or len(mzs) != len(ints):
            bad += 1
            continue
        arr = np.asarray(ints, dtype=np.float64)
        if np.any(~np.isfinite(arr)) or np.any(arr < 0):
            bad += 1
    print(f"[test] rows={len(df)} molecules={df.molecule_id.nunique()} bad_peak_rows={bad}")
    return df


def run_inference(
    test_df: pd.DataFrame,
    index: SpectrumIndex,
    cfg: RunConfig,
) -> tuple[Dict[str, List[str]], pd.DataFrame, dict]:
    predictions: Dict[str, List[str]] = {}
    evidence_rows = []
    stats = defaultdict(int)
    t0 = time.time()
    groups = list(test_df.groupby("molecule_id", sort=False))
    for molecule_id, g in tqdm(groups, desc="infer molecules"):
        cands, diag = aggregate_molecule_candidates(molecule_id, g, index, cfg)
        predictions[molecule_id] = [c.smiles for c in cands]
        if diag.get("fallback_used"):
            stats["fallback_molecules"] += 1
        if diag.get("placeholder_used"):
            stats["placeholder_molecules"] += 1
        stats["n_candidates_total"] += len(cands)
        for rank, c in enumerate(cands, start=1):
            row = c.to_dict()
            row["molecule_id"] = molecule_id
            row["rank"] = rank
            row["neutral_mass"] = diag.get("neutral_mass")
            evidence_rows.append(row)
    stats["elapsed_sec"] = time.time() - t0
    stats["n_molecules"] = len(groups)
    evidence = pd.DataFrame(evidence_rows)
    return predictions, evidence, dict(stats)


def naive_mass_baseline(
    test_df: pd.DataFrame,
    index: SpectrumIndex,
    cfg: RunConfig,
) -> Dict[str, List[str]]:
    """Baseline: nearest exact-mass structures, no spectral similarity."""
    from casmi26.adducts import infer_neutral_mass, polarity_compatible

    preds = {}
    for molecule_id, g in test_df.groupby("molecule_id", sort=False):
        masses = []
        for row in g.itertuples(index=False):
            nm = infer_neutral_mass(row.precursor_mz, row.adduct)
            ok, _ = polarity_compatible(row.adduct, row.ionization_mode)
            if nm.supported and ok:
                masses.append(nm.neutral_mass)
        if not masses:
            preds[molecule_id] = ["CCO"]
            continue
        mass = float(np.median(masses))
        lo, hi = index.mass_window(mass, cfg.mass_tol_ppm_backfill)
        seen = set()
        smiles = []
        # take closest by mass among window
        if hi > lo:
            order = np.argsort(np.abs(index.neutral_mass[lo:hi] - mass))
            for off in order:
                pos = lo + int(off)
                ik = index.inchikey14[pos]
                if ik in seen:
                    continue
                seen.add(ik)
                smiles.append(index.smiles[pos])
                if len(smiles) >= cfg.max_candidates:
                    break
        preds[molecule_id] = smiles or ["CCO"]
    return preds


def run_grouped_validation(
    train_path: Path,
    index: SpectrumIndex,
    cfg: RunConfig,
    n_query_structures: int = 200,
    spectra_per_mol: int = 3,
    seed: int = 42,
) -> dict:
    """Run known-spectrum and unseen-structure simulations on an enveda slice."""
    print("[val] sampling query structures from enveda-180 / enveda-np-examples...")
    cols = [
        "ingest_lib",
        "normalized_smiles",
        "inchikey14",
        "ionization_mode",
        "adduct",
        "precursor_mz",
        "ms2_mzs",
        "ms2_normalized_intensities",
        "base_peak_intensity",
        "collision_energy_ev",
        "instrument_type",
    ]
    meta = pq.read_table(
        train_path,
        columns=["ingest_lib", "inchikey14", "instrument_type"],
    ).to_pandas()
    mask = meta["ingest_lib"].isin(["enveda-180", "enveda-np-examples"])
    meta = meta[mask]
    rng = np.random.default_rng(seed)
    # Prefer structures with enough spectra for multi-spectrum queries
    counts = meta["inchikey14"].value_counts()
    eligible = counts[counts >= spectra_per_mol + 1].index.to_numpy()
    if len(eligible) == 0:
        eligible = meta["inchikey14"].dropna().unique()
    if len(eligible) > n_query_structures:
        holdout = set(rng.choice(eligible, size=n_query_structures, replace=False))
    else:
        holdout = set(eligible)

    def subset_index(idx: SpectrumIndex, mask_arr: np.ndarray) -> SpectrumIndex:
        return SpectrumIndex(
            neutral_mass=idx.neutral_mass[mask_arr],
            precursor_mz=idx.precursor_mz[mask_arr],
            order=idx.order[mask_arr],
            inchikey14=idx.inchikey14[mask_arr],
            smiles=idx.smiles[mask_arr],
            library=idx.library[mask_arr],
            adduct=idx.adduct[mask_arr],
            ionization_mode=idx.ionization_mode[mask_arr],
            quality=idx.quality[mask_arr],
            exact_mass=idx.exact_mass[mask_arr],
            domain_prior=idx.domain_prior[mask_arr],
            peak_mz=idx.peak_mz[mask_arr],
            peak_intensity=idx.peak_intensity[mask_arr],
            collision_energy=idx.collision_energy[mask_arr],
        )

    pf = pq.ParquetFile(train_path)
    query_rows = []
    for rg in range(pf.num_row_groups):
        df = pf.read_row_group(rg, columns=cols).to_pandas()
        df = df[
            df["inchikey14"].isin(holdout)
            & df["ingest_lib"].isin(["enveda-180", "enveda-np-examples"])
        ]
        if len(df):
            query_rows.append(df)
    if not query_rows:
        return {"error": "no holdout spectra"}
    qdf_all = pd.concat(query_rows, ignore_index=True)

    parts = []
    truths = {}
    for ik, g in qdf_all.groupby("inchikey14"):
        g = g.sample(n=min(spectra_per_mol, len(g)), random_state=seed)
        mid = f"val_{ik}"
        g = g.copy()
        g["molecule_id"] = mid
        g["spectrum_id"] = [f"{mid}_s{i}" for i in range(len(g))]
        parts.append(g)
        truths[mid] = ik
    qdf = pd.concat(parts, ignore_index=True)

    from casmi26.chemistry import inchikey14_from_smiles

    def preds_to_ik(preds_smiles: Dict[str, List[str]]) -> Dict[str, List[str]]:
        out = {}
        for mid, smis in preds_smiles.items():
            iks = []
            seen = set()
            for s in smis:
                ik = inchikey14_from_smiles(s)
                if ik and ik not in seen:
                    seen.add(ik)
                    iks.append(ik)
            out[mid] = iks
        return out

    # Known-spectrum: structure remains in index (library-match / Class-1 diagnostic)
    print("[val] known-spectrum simulation...")
    preds_known, _, _ = run_inference(qdf, index, cfg)
    metrics_known = summarize_metrics(preds_to_ik(preds_known), truths)
    metrics_known["mode"] = "known_spectrum"
    print("[val] known-spectrum:", metrics_known)

    # Mass-only naive baseline on same queries
    print("[val] naive mass baseline...")
    naive_smiles = naive_mass_baseline(qdf, index, cfg)
    metrics_naive = summarize_metrics(preds_to_ik(naive_smiles), truths)
    metrics_naive["mode"] = "naive_mass_known_spectrum"
    print("[val] naive mass:", metrics_naive)

    # Unseen-structure: remove all spectra of holdout IKs from index
    print("[val] unseen-structure simulation...")
    keep = np.array([ik not in holdout for ik in index.inchikey14])
    filtered = subset_index(index, keep)
    preds_unseen, _, _ = run_inference(qdf, filtered, cfg)
    metrics_unseen = summarize_metrics(preds_to_ik(preds_unseen), truths)
    metrics_unseen["mode"] = "unseen_structure"
    metrics_unseen["note"] = (
        "Exact-structure MRR is expected near zero when the target IK is removed; "
        "this exposes Class-3 / de-novo limitation of retrieval."
    )
    print("[val] unseen-structure:", metrics_unseen)

    return {
        "n_holdout_structures": len(holdout),
        "known_spectrum": metrics_known,
        "naive_mass_baseline": metrics_naive,
        "unseen_structure": metrics_unseen,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=DATA_DIR)
    parser.add_argument("--out-dir", type=Path, default=OUTPUT_DIR)
    parser.add_argument("--artifact-dir", type=Path, default=ARTIFACT_DIR)
    parser.add_argument("--max-train-rows", type=int, default=None)
    parser.add_argument("--skip-validation", action="store_true")
    parser.add_argument("--rebuild-index", action="store_true")
    parser.add_argument("--preferred-libs-only", action="store_true", default=False)
    parser.add_argument("--val-structures", type=int, default=150)
    args = parser.parse_args()

    cfg = RunConfig()
    set_seeds(cfg.seed)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    args.artifact_dir.mkdir(parents=True, exist_ok=True)

    print("=== Enveda CASMI 2026 first submission ===")
    print_versions()
    print("config:", json.dumps(cfg.to_dict(), indent=2))

    train_path = args.data_dir / "train.parquet"
    test_path = args.data_dir / "test.parquet"
    sample_path = args.data_dir / "sample_submission.csv"
    assert train_path.exists(), train_path
    assert test_path.exists(), test_path
    assert sample_path.exists(), sample_path

    cache = args.artifact_dir / "spectrum_index.npz"
    if args.rebuild_index and cache.exists():
        cache.unlink()

    libs = PREFERRED_LIBS if args.preferred_libs_only else None
    t_index = time.time()
    index = build_index_from_train(
        train_path,
        cfg,
        cache_path=cache,
        max_rows=args.max_train_rows,
        libraries=libs,
    )
    print(f"[timing] index stage {time.time() - t_index:.1f}s size={len(index.neutral_mass)}")

    test_df = load_test(test_path)
    sample = pd.read_csv(sample_path)

    val_metrics = {}
    if not args.skip_validation:
        try:
            val_metrics = run_grouped_validation(
                train_path,
                index,
                cfg,
                n_query_structures=args.val_structures,
            )
            # naive baseline on same holdout is expensive; skip full redo — report flag only
            val_metrics["naive_baseline_note"] = (
                "mass-only baseline available via -- compare offline; "
                "primary metric is unseen-structure retrieval MRR@25"
            )
        except Exception as exc:
            val_metrics = {"error": str(exc), "traceback": traceback.format_exc()}
            print("[val] failed:", exc)

    t_inf = time.time()
    predictions, evidence, stats = run_inference(test_df, index, cfg)
    print(f"[timing] inference {time.time() - t_inf:.1f}s stats={stats}")

    sub = build_submission_frame(predictions, sample)
    errors = validate_submission(sub, sample, test_molecule_ids=test_df.molecule_id.unique())
    if errors:
        raise SystemExit("submission validation failed:\n- " + "\n- ".join(errors))

    sub_path = args.out_dir / "submission.csv"
    evidence_path = args.out_dir / "candidate_evidence.parquet"
    write_submission(sub, sub_path)
    evidence.to_parquet(evidence_path, index=False)

    # also copy submission to repo root for convenience
    root_sub = Path(__file__).resolve().parents[1] / "submission.csv"
    write_submission(sub, root_sub)

    cand_counts = sub["smiles"].apply(lambda s: len(str(s).split(";")))
    summary = {
        "submission_path": str(sub_path),
        "n_rows": len(sub),
        "candidate_count_mean": float(cand_counts.mean()),
        "candidate_count_min": int(cand_counts.min()),
        "candidate_count_max": int(cand_counts.max()),
        "inference_stats": stats,
        "validation": val_metrics,
        "fallback_rate": stats.get("fallback_molecules", 0) / max(stats.get("n_molecules", 1), 1),
        "placeholder_rate": stats.get("placeholder_molecules", 0) / max(stats.get("n_molecules", 1), 1),
    }
    summary_path = args.out_dir / "run_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, default=str))
    print("=== RUN SUMMARY ===")
    print(json.dumps(summary, indent=2, default=str))
    print(f"Wrote {sub_path} and {evidence_path}")


if __name__ == "__main__":
    main()
