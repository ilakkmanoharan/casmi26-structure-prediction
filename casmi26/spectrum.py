"""Deterministic spectrum cleaning and similarity."""

from __future__ import annotations

from typing import Optional, Tuple

import numpy as np


def clean_spectrum(
    mzs,
    intensities,
    precursor_mz: Optional[float] = None,
    intensity_floor: float = 0.001,
    top_peaks: int = 64,
    merge_tol: float = 0.005,
    remove_above_precursor_da: float = 2.0,
    sqrt_intensity: bool = True,
) -> Tuple[np.ndarray, np.ndarray]:
    """Return cleaned (mz, intensity) float32 arrays sorted by mz."""
    if mzs is None or intensities is None:
        return np.zeros(0, dtype=np.float32), np.zeros(0, dtype=np.float32)

    mz = np.asarray(mzs, dtype=np.float64)
    inten = np.asarray(intensities, dtype=np.float64)
    if mz.size == 0 or inten.size == 0 or mz.size != inten.size:
        return np.zeros(0, dtype=np.float32), np.zeros(0, dtype=np.float32)

    mask = np.isfinite(mz) & np.isfinite(inten) & (mz > 0) & (inten >= 0)
    if precursor_mz is not None and np.isfinite(precursor_mz):
        mask &= mz <= (float(precursor_mz) + remove_above_precursor_da)
    mz = mz[mask]
    inten = inten[mask]
    if mz.size == 0:
        return np.zeros(0, dtype=np.float32), np.zeros(0, dtype=np.float32)

    order = np.argsort(mz)
    mz = mz[order]
    inten = inten[order]

    # merge nearby peaks (intensity-weighted mz)
    merged_mz = []
    merged_int = []
    cur_mz = mz[0]
    cur_int = inten[0]
    for i in range(1, len(mz)):
        if mz[i] - cur_mz <= merge_tol:
            total = cur_int + inten[i]
            if total > 0:
                cur_mz = (cur_mz * cur_int + mz[i] * inten[i]) / total
            cur_int = total
        else:
            merged_mz.append(cur_mz)
            merged_int.append(cur_int)
            cur_mz = mz[i]
            cur_int = inten[i]
    merged_mz.append(cur_mz)
    merged_int.append(cur_int)
    mz = np.asarray(merged_mz, dtype=np.float64)
    inten = np.asarray(merged_int, dtype=np.float64)

    max_i = inten.max()
    if max_i <= 0:
        return np.zeros(0, dtype=np.float32), np.zeros(0, dtype=np.float32)
    inten = inten / max_i
    keep = inten >= intensity_floor
    mz = mz[keep]
    inten = inten[keep]
    if mz.size == 0:
        return np.zeros(0, dtype=np.float32), np.zeros(0, dtype=np.float32)

    if mz.size > top_peaks:
        top_idx = np.argpartition(inten, -top_peaks)[-top_peaks:]
        top_idx.sort()
        mz = mz[top_idx]
        inten = inten[top_idx]
        # re-sort by mz
        order = np.argsort(mz)
        mz = mz[order]
        inten = inten[order]

    if sqrt_intensity:
        inten = np.sqrt(inten)

    # L2 normalize for cosine-like scoring
    norm = np.linalg.norm(inten)
    if norm > 0:
        inten = inten / norm

    return mz.astype(np.float32), inten.astype(np.float32)


def _greedy_match(
    mz_a: np.ndarray,
    mz_b: np.ndarray,
    tol: float,
    shift: float = 0.0,
) -> Tuple[np.ndarray, np.ndarray]:
    """Greedy 1-1 matching of peaks within tol after applying shift to b."""
    i = j = 0
    pairs_a = []
    pairs_b = []
    used_b = np.zeros(len(mz_b), dtype=bool)
    # two-pointer with local search for closest unused b
    for i, ma in enumerate(mz_a):
        target = ma - shift
        # advance j near target
        while j < len(mz_b) and mz_b[j] < target - tol:
            j += 1
        best_j = -1
        best_diff = tol + 1
        k = j
        while k < len(mz_b) and mz_b[k] <= target + tol:
            if not used_b[k]:
                diff = abs(mz_b[k] - target)
                if diff < best_diff:
                    best_diff = diff
                    best_j = k
            k += 1
        if best_j >= 0:
            used_b[best_j] = True
            pairs_a.append(i)
            pairs_b.append(best_j)
    return np.asarray(pairs_a, dtype=np.int64), np.asarray(pairs_b, dtype=np.int64)


def modified_cosine(
    mz_a: np.ndarray,
    int_a: np.ndarray,
    mz_b: np.ndarray,
    int_b: np.ndarray,
    precursor_a: float,
    precursor_b: float,
    tol: float = 0.05,
    use_neutral_loss: bool = True,
) -> float:
    """Modified cosine with optional precursor-shift (neutral-loss) matching."""
    if len(mz_a) == 0 or len(mz_b) == 0:
        return 0.0

    ia, ib = _greedy_match(mz_a, mz_b, tol, shift=0.0)
    matched = set(zip(ia.tolist(), ib.tolist())) if len(ia) else set()

    if use_neutral_loss and np.isfinite(precursor_a) and np.isfinite(precursor_b):
        shift = float(precursor_a) - float(precursor_b)
        if abs(shift) > 1e-6:
            # rematch unused peaks under shift
            used_a = {p[0] for p in matched}
            used_b = {p[1] for p in matched}
            mz_a2 = mz_a
            mz_b2 = mz_b
            ia2, ib2 = _greedy_match(mz_a2, mz_b2, tol, shift=shift)
            for a_idx, b_idx in zip(ia2.tolist(), ib2.tolist()):
                if a_idx in used_a or b_idx in used_b:
                    continue
                matched.add((a_idx, b_idx))
                used_a.add(a_idx)
                used_b.add(b_idx)

    if not matched:
        return 0.0

    score = 0.0
    for a_idx, b_idx in matched:
        score += float(int_a[a_idx]) * float(int_b[b_idx])
    # already L2-normalized => score in [0, 1]
    return float(max(0.0, min(1.0, score)))


def _spectral_entropy(intensities: np.ndarray) -> float:
    s = float(np.sum(intensities))
    if s <= 0:
        return 0.0
    p = intensities / s
    p = p[p > 0]
    return float(-np.sum(p * np.log(p)))


def _entropy_weights(intensities: np.ndarray) -> np.ndarray:
    """Li & Fiehn intensity reweighting based on spectral entropy."""
    ent = _spectral_entropy(intensities)
    w = 0.25 + 0.25 * ent  # in [0.25, ~1+]
    weighted = np.power(np.maximum(intensities, 0.0), w)
    total = float(np.sum(weighted))
    if total <= 0:
        return intensities
    return weighted / total


def entropy_similarity(
    mz_a: np.ndarray,
    int_a: np.ndarray,
    mz_b: np.ndarray,
    int_b: np.ndarray,
    tol: float = 0.05,
) -> float:
    """Entropy similarity in [0, 1] after un-doing L2 norm assumption.

    Inputs may be L2-normalized cleaned peaks; we convert to positive weights,
    apply entropy weighting, merge matched peaks, and score:
    1 - (2*S_ab - S_a - S_b) / ln(4).
    """
    if len(mz_a) == 0 or len(mz_b) == 0:
        return 0.0
    # Recover relative intensities (already non-negative)
    wa = _entropy_weights(np.asarray(int_a, dtype=np.float64) ** 2)  # undo sqrt+L2 approx
    wb = _entropy_weights(np.asarray(int_b, dtype=np.float64) ** 2)
    # If ints were not sqrt-scaled L2, fallback to abs values
    if not np.isfinite(wa).all() or float(np.sum(wa)) <= 0:
        wa = _entropy_weights(np.abs(np.asarray(int_a, dtype=np.float64)))
    if not np.isfinite(wb).all() or float(np.sum(wb)) <= 0:
        wb = _entropy_weights(np.abs(np.asarray(int_b, dtype=np.float64)))

    ia, ib = _greedy_match(mz_a, mz_b, tol, shift=0.0)
    merged = []
    used_a = set(ia.tolist()) if len(ia) else set()
    used_b = set(ib.tolist()) if len(ib) else set()
    for a_idx, b_idx in zip(ia.tolist(), ib.tolist()) if len(ia) else []:
        merged.append(wa[a_idx] + wb[b_idx])
    for i, v in enumerate(wa):
        if i not in used_a:
            merged.append(v)
    for j, v in enumerate(wb):
        if j not in used_b:
            merged.append(v)
    merged = np.asarray(merged, dtype=np.float64)
    s_a = _spectral_entropy(wa)
    s_b = _spectral_entropy(wb)
    s_ab = _spectral_entropy(merged)
    denom = np.log(4.0)
    sim = 1.0 - (2.0 * s_ab - s_a - s_b) / denom
    return float(max(0.0, min(1.0, sim)))


def hybrid_similarity(
    mz_a: np.ndarray,
    int_a: np.ndarray,
    mz_b: np.ndarray,
    int_b: np.ndarray,
    precursor_a: float,
    precursor_b: float,
    tol: float = 0.05,
    use_neutral_loss: bool = True,
    entropy_weight: float = 0.55,
) -> float:
    cos = modified_cosine(
        mz_a, int_a, mz_b, int_b, precursor_a, precursor_b, tol, use_neutral_loss
    )
    ent = entropy_similarity(mz_a, int_a, mz_b, int_b, tol=tol)
    w = float(entropy_weight)
    return float(w * ent + (1.0 - w) * cos)


def spectra_identical(
    mz_a: np.ndarray,
    int_a: np.ndarray,
    mz_b: np.ndarray,
    int_b: np.ndarray,
    precursor_a: float,
    precursor_b: float,
    prec_atol: float = 1e-4,
) -> bool:
    """True if cleaned spectra + precursor match (poisoned-label guard)."""
    if abs(float(precursor_a) - float(precursor_b)) > prec_atol:
        return False
    if len(mz_a) != len(mz_b) or len(mz_a) == 0:
        return False
    return bool(np.array_equal(mz_a, mz_b) and np.array_equal(int_a, int_b))
