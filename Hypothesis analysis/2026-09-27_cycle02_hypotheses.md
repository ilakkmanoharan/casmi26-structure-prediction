# Hypotheses — 2026-09-27 cycle02

## H1 — Higher neighbor similarity floor (THIS SLOT)

**Statement.** Raising `MIN_SIMILARITY` from 0.05 → **0.12** will drop weak hybrid ties that currently occupy the top-25 after the exact-dup IK ban, moving true structures up the MRR@25 list without changing the mass window, peak ladder, or entropy/modcos mix.

**Why.** Li et al., *Nat. Methods* (2021) report FDR < 10% at entropy similarity **0.75** on natural-product MS/MS. Our kernel already uses `ENTROPY_WEIGHT=0.75`, but still *accepts* neighbors at 0.05 — more than an order of magnitude below that identity operating point. Scheubert et al. (2017) show that unthresholded spectral matching inflates false annotations. 0.12 is the unused P1 reserved in 2026-09-26 cycle02 H3 (range 0.12–0.15); it is conservative enough that analogues scoring 0.2–0.6 still enter the list. Backfill (`MASS_TOL_PPM_BACKFILL=80`) and the ethanol placeholder keep submissions valid if a sparse query goes empty.

**Expected MRR direction.** Up vs 0.143 if decoys above the true hit are mostly sub-0.12 hybrid scores. Neutral if public scoring is still delayed. Down if many true structures only match CE-shifted library spectra at 0.05–0.11.

**Failure mode.** Sparse 2–3 peak queries lose all neighbors and fall through to backfill (0.1× score) or the CCO placeholder (MRR 0 for that molecule). Mitigant: keep 0.12 not 0.20; keep backfill + placeholder.

## H2 — Domain-prior NP boost (already used)

Boost `enveda-np-examples` / `enveda-180` / `gnps` priors. Actions ran this as 2026-09-26 cycle05. Soft re-rank only; does not change who enters the candidate pool.

## H3 — Repeat entropy / mass / peaks (do not run)

`ENTROPY_WEIGHT=0.75`, mass-wide 35/80, and `TOP_PEAKS=128` are already on main. Slot-2 fallback `H-entropy` would be a no-op.

## H4 — Flash Entropy / MS2Query (not this kernel)

Needs extra wheels or embeddings. Out of scope for a one-constant ablation. Retrieval still cannot claim Class-3 de novo is solved.

## Ablation this slot

**Run H1 only.** `config_patch = {"MIN_SIMILARITY": 0.12}`.
