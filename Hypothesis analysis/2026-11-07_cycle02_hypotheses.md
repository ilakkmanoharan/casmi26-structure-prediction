# Hypotheses — 2026-11-07 cycle02

## H1 (this slot) — H-mass-tight

**Statement:** Tightening the primary structure-level mass window from 35 ppm to 15 ppm, while keeping the 80 ppm backfill, reduces off-formula decoys in the scored top-k and raises public MRR@25.

**Rationale:** ibnmarzuk’s public CASMI baseline gates at ±15 ppm; shiferaxa’s public pipeline uses 8.5 ppm. Live `MASS_TOL_PPM=35` admits a much larger isomer/formula neighborhood into `retrieve_for_spectrum` before hybrid entropy/modcos scoring. Fragment knobs (`PEAK_MZ_TOL=0.02`, `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`) are already at literature defaults, so the unused lever is the *pool*, not the similarity object.

**Expected MRR direction:** Up vs 0.143 if a non-trivial fraction of public test structures are in the library at the correct mass; flat if the remaining errors are poisoned labels / Class-3 absence (then analog/de novo is required).

**Failure mode:** True hits whose adduct-inferred neutral mass is >15 ppm off (wrong adduct, dimer, or isotope) drop out of the primary window. Mitigant: `MASS_TOL_PPM_BACKFILL=80` still fills empty lists at 0.1× score, so they occupy ranks  after real hits rather than replacing them.

## H2 — Longer peak ladder (`TOP_PEAKS` 128 → 160)

Tried as 2026-11-06 cycle04 (Kaggle 58071327, kernel v201) but never landed on main (GitHub 500). Do not confound with H1 this slot.

## H3 — Higher similarity floor (`MIN_SIMILARITY` 0.05 → 0.12)

Li/Fiehn FDR work implies very low hybrid scores are decoys. Could stop packing the top-25 with noise *after* the mass gate is tight. Next unused slot if H1 is not too tight.

## H4 — Analog Tanimoto / MS2Query-style channel

Public 0.50–0.54 pipelines use analog evidence when exact library match is poisoned. Out of scope this cycle (fingerprints + extra ranker; internet-off kernel budget).

## Ablation this slot

**One major change:** H1. `config_patch: {"MASS_TOL_PPM": 15.0}`
