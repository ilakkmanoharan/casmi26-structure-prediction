# Hypotheses — 2026-10-29 cycle03

## H1 — H-min-sim (run this slot)

**Claim.** Raising `MIN_SIMILARITY` from **0.05** to **0.12** drops low-confidence hybrid library hits that currently pad the top-25, improving public MRR@25 versus the 0.143 plateau.

**Mechanism.** `retrieve.py` gates library spectra with `if sim >= cfg.min_similarity` before `top_k` truncation and structure aggregation. At 0.05, near-noise entropy/modcos scores (well below GNPS 0.5 / MASST 0.7 / Li–Fiehn 0.75) occupy rank-list slots. 0.12 is still an *admission* floor, not a 0.75 *call* threshold, so sparse-but-real hits remain eligible. Pairing window (`PEAK_MZ_TOL=0.02`), entropy mix (0.75), intensity floor (0.01), and peak ladder (128) stay fixed.

**Expected MRR direction.** Small-to-moderate positive if decoy padding is the bottleneck; near-zero if the true structure already sits in the top-25 with a score ≥ 0.12. Failure mode: sparse queries whose best true-structure hit is in (0.05, 0.12) fall out of the list (MRR 0 on those queries). That is acceptable to measure — it is a real ablation, unlike replaying `PEAK_MZ_TOL=0.02`.

## H2 — TOP_PEAKS 128 → 160 (next unused / slot-4 fallback)

**Claim.** A longer ladder after the 1% intensity floor can keep diagnostic mid-intensity ions.

**Why not now.** Confounds H1: more peaks plus a tighter score floor moves two knobs. Measure the floor first. Slot-4 fallback after this PR is `TOP_PEAKS=160` only (do not reset `MIN_SIMILARITY`).

## H3 — Replay PEAK_MZ_TOL=0.02 (reject)

Already live on main (Actions 10-24 Cloud merge + today’s cycle02 kernel v168). Slot-3 fallback currently *is* this no-op. Do not run it.

## H4 — Analog / MS2Deepscore (out of scope)

Needs extra wheels or embeddings. Out of scope for a one-constant ablation. Do not claim Class-3 de novo is solved by retrieval.

## One major ablation this slot

Run **H1 only**. `config_patch: {"MIN_SIMILARITY": 0.12}`.
