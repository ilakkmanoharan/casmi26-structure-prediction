# Hypotheses — 2026-09-29 cycle02

## H1 (this slot) — 1% intensity floor

**Claim.** Raising `INTENSITY_FLOOR` from 0.001 to 0.01 (msentropy / Li–Fiehn default) removes noise ions that currently (a) steal `TOP_PEAKS=128` slots and (b) inflate the 0.25 modified-cosine term, so the true InChIKey14 (when present in a non-poisoned library row) moves up in the MRR@25 list.

**Why now.** Live main already has entropy 0.75, 128 peaks, and the wide mass window. Floor is the unused cleaning knob. Prior Cloud cycles retargeted `MIN_SIMILARITY` and never merged.

**Expected MRR direction.** Up vs 0.143 if a non-trivial fraction of public molecules have a correct library hit that is currently outranked by noisy decoys. Neutral if the remaining error is almost all poisoned-label / out-of-library (Class-3). Down if true fragments sit between 0.1% and 1% of base peak and are required to distinguish analogs.

**Failure mode.** Sparse MS/MS (few fragments above 1%) collapse to <2 peaks after cleaning → those query spectra skip retrieval (`len(mz) < 2`). Backfill should still fill the 25-list. Watch `placeholder_molecules` and `fallback_molecules` in kernel `run_summary.json`.

## H2 — MIN_SIMILARITY 0.05 → 0.12 (deferred)

Drops junk from the 25-list. Cloud PRs #11 and #12 already specified this; they never reached main. Run only after H1 is scored or rejected.

## H3 — Real domain_prior boost (deferred)

`H-domain` fallback currently writes the same 1.0 / 1.0 / 0.85 values already on main (no-op). A real change would raise `gnps`/`riken` relative to `enveda-180` so synthetic poisoned neighbors lose aggregation weight. Separate factor.

## H4 — Analog / candidate-DB ranker (out of kernel scope this slot)

Public notebooks ~0.33 show the LB gap is analog + extra DBs, not another ppm tweak. Requires attached datasets and a second ranker. Not Class-3 de novo.

## Ablation this slot

**H1 only.** `config_patch: {"INTENSITY_FLOOR": 0.01}`
