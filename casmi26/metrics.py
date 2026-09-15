"""Grouped validation metrics (MRR@25, Hit@k)."""

from __future__ import annotations

from typing import Dict, Iterable, List, Sequence

import numpy as np


def reciprocal_rank(pred_ik14: Sequence[str], true_ik14: str, k: int = 25) -> float:
    if not true_ik14:
        return 0.0
    for i, ik in enumerate(pred_ik14[:k]):
        if ik == true_ik14:
            return 1.0 / (i + 1)
    return 0.0


def hit_at_k(pred_ik14: Sequence[str], true_ik14: str, k: int) -> float:
    return 1.0 if true_ik14 in list(pred_ik14)[:k] else 0.0


def summarize_metrics(
    predictions: Dict[str, Sequence[str]],
    truths: Dict[str, str],
) -> Dict[str, float]:
    """predictions: molecule_id -> ranked inchikey14 list; truths: molecule_id -> ik14."""
    ids = sorted(set(predictions) & set(truths))
    if not ids:
        return {"n": 0}
    mrr = []
    hits = {k: [] for k in (1, 5, 10, 25)}
    for mid in ids:
        pred = list(predictions[mid])
        true = truths[mid]
        mrr.append(reciprocal_rank(pred, true, 25))
        for k in hits:
            hits[k].append(hit_at_k(pred, true, k))
    out = {
        "n": float(len(ids)),
        "mrr@25": float(np.mean(mrr)),
        "hit@1": float(np.mean(hits[1])),
        "hit@5": float(np.mean(hits[5])),
        "hit@10": float(np.mean(hits[10])),
        "hit@25": float(np.mean(hits[25])),
    }
    return out
