# Hypotheses — 2026-10-29 cycle02

## H1 — H-min-sim (run this slot)

**Claim.** Raising `MIN_SIMILARITY` from **0.05** to **0.12** drops low-confidence hybrid entropy/modcos library hits that currently pad `top_k` and the top-25, improving public MRR@25 versus the 0.143 plateau.

**Mechanism.** `search_mass_window` appends a library spectrum only when `sim >= cfg.min_similarity` (`casmi26/retrieve.py`). At 0.05, near-random matches survive the 35/80 ppm mass window and crowd out mid-quality true-structure near-matches before aggregation. 0.12 is a conservative first step: well above noise, well below the Li/Fiehn 0.75 identification cutoff, so sparse-but-real hits should still enter the list.

**Expected MRR direction.** Small-to-moderate positive if decoy padding is the bottleneck; near-zero if the top-25 is already filled with closer decoys that also clear 0.12. Failure mode: true-structure near-matches in the 0.05–0.12 band disappear and lists go empty on sparse queries (MRR down; fallback/placeholder counts rise). That is acceptable to measure — it is a real ablation, unlike replaying `PEAK_MZ_TOL=0.02` or `TOP_PEAKS=128`.

## H2 — TOP_PEAKS 128 → 160 (next unused / slot-3 fallback)

**Claim.** A longer ladder after the 1% intensity floor can keep diagnostic mid-intensity ions.

**Why not now.** Confounds H1: more peaks plus a tighter score floor moves two knobs. Measure the floor first. Slot-3/4 fallbacks try 160 **without** resetting `MIN_SIMILARITY`.

## H3 — Jump MIN_SIMILARITY to 0.75 (not this slot)

**Claim.** Li/Fiehn FDR < 10% at entropy similarity 0.75.

**Why not now.** That is an identification cutoff, not an MRR@25 recall floor. It would empty too many queries on this hybrid + multi-library setup. 0.12 is the first unused step.

## H4 — Analog / MS2Deepscore (out of scope)

Needs extra wheels or embeddings. Out of scope for a one-constant ablation. Do not claim Class-3 de novo is solved by retrieval.

## One major ablation this slot

Run **H1 only**. `config_patch: {"MIN_SIMILARITY": 0.12}`.
