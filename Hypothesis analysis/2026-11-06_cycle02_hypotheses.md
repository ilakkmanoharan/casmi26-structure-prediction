# Hypotheses — 2026-11-06 cycle02

## H1 — H-sim-gate (run this slot)

**Claim.** Raising `MIN_SIMILARITY` from **0.05** to **0.12** drops weak hybrid scores that currently fill the top-25 with mass-isobar decoys, improving public MRR@25 versus the 0.143 plateau, with fragment pairing, peak ladder, and entropy mix held at their already-live Flash Entropy defaults.

**Mechanism.** `retrieve_for_spectrum` appends a library hit only when `sim >= cfg.min_similarity`. At 0.05, CE-shifted GNPS/MassBank/MONA/Enveda near-isobars with a handful of 20 mDa fragment coincidences enter aggregation, consume `TOP_CANDIDATES_PER_SPECTRUM=25` slots, and can outrank a true structure that lost its exact-dup evidence (poisoned `enveda-180` rows are banned). 0.12 is a conservative step toward Li/Fiehn / Scheubert identification regimes (0.7–0.75) without jumping to 0.75, which would empty many true CE-mismatched hits. One constant; no change to `PEAK_MZ_TOL`, `TOP_PEAKS`, or `ENTROPY_WEIGHT`.

**Expected MRR direction.** Small-to-moderate positive if decoy packing is the bottleneck after 0.02 Da pairing; near-zero if true structures already sit at rank 1 with scores ≫ 0.12. Failure mode: true-structure library hits that only score 0.05–0.11 (sparse peaks, large CE gap) drop out and the molecule falls back to a placeholder (MRR down). That is acceptable to measure — it is a real ablation, unlike replaying `PEAK_MZ_TOL=0.02` or `TOP_PEAKS=128`.

## H2 — TOP_PEAKS 128 → 160 (next unused)

**Claim.** A longer ladder after the 1% intensity floor can keep diagnostic mid-intensity ions.

**Why not now.** Slot-4 fallback already tries 160 + `MIN_SIMILARITY=0.05`. Do not stack it on H1.

## H3 — MASS_TOL_PPM 35 → 10–15 (later)

**Claim.** Tighter structure-level exact-mass filter reduces extra formulas that survive the 35 ppm window.

**Why not now.** Confounds H1: a tighter mass window plus a tighter score floor moves two knobs. Measure the gate first.

## H4 — Analog / MS2Deepscore (out of scope)

Needs extra wheels or embeddings. Out of scope for a one-constant ablation. Do not claim Class-3 de novo is solved by retrieval.

## One major ablation this slot

Run **H1 only**. `config_patch: {"MIN_SIMILARITY": 0.12}`.
