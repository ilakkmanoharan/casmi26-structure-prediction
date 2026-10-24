# Hypotheses — 2026-10-24 cycle03

## H1 — H-peak-mz (run this slot)

**Claim.** Raising `PEAK_MZ_TOL` from **0.01 Da (10 mDa)** to **0.02 Da (20 mDa)** aligns fragment pairing with Flash Entropy / ms_entropy / matchms defaults and recovers CE / instrument shifts that currently miss `_greedy_match`, improving public MRR@25 versus the 0.143 plateau.

**Mechanism.** `hybrid_similarity` passes `tol=cfg.peak_mz_tol` into both entropy and modified-cosine matchers. At 10 mDa, a 12–18 mDa centroid disagreement (common on mid-intensity GNPS / MassBank / MONA / Enveda ions) drops the pair, so the true structure’s entropy/modcos score falls below `MIN_SIMILARITY=0.05` and never enters the rank list. Doubling the window to the literature default keeps those pairs without changing mass-window coverage, peak cleaning, or the 0.75 entropy mix.

**Expected MRR direction.** Small-to-moderate positive if recall of true-structure near-matches is the bottleneck; near-zero if the top-25 is already filled with closer decoys. Failure mode: a wider window also pairs more decoy fragments, inflating false similarities and pushing GT down the list (MRR down). That is acceptable to measure — it is a real ablation, unlike replaying `ENTROPY_WEIGHT=0.75` or `INTENSITY_FLOOR=0.01`.

## H2 — MIN_SIMILARITY 0.05 → 0.12 (next unused)

**Claim.** Li/Fiehn FDR work implies very low hybrid scores are mostly decoys. Raising the floor may stop packing the top-25 with noise.

**Why not now.** Confounds H1: a tighter score floor plus a wider pair window moves two knobs. Measure the window first.

## H3 — TOP_PEAKS 128 → 160 (slot-4 fallback)

**Claim.** A longer ladder after the 1% intensity floor can keep diagnostic mid-intensity ions.

**Why not now.** Slot-4 fallback already tries 160 + `MIN_SIMILARITY=0.05`. Do not stack it on H1.

## H4 — Analog / MS2Deepscore (out of scope)

Needs extra wheels or embeddings. Out of scope for a one-constant ablation. Do not claim Class-3 de novo is solved by retrieval.

## One major ablation this slot

Run **H1 only**. `config_patch: {"PEAK_MZ_TOL": 0.02}`.
