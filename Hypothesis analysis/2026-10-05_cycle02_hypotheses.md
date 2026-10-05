# Hypotheses — 2026-10-05 cycle02

## H1 (this slot) — 1% intensity floor

**Claim.** Raising `INTENSITY_FLOOR` from `0.001` to `0.01` removes sub-1% noise ions that currently survive cleaning, occupy greedy peak matches, and inflate hybrid entropy/modcos toward poisoned or analog-wrong inchikey14s. Aligns `clean_spectrum` with Flash / msentropy `noise_threshold=0.01`.

**Expected MRR direction.** Up vs 0.143 if noise ions are currently promoting decoys into the top-25; flat if test spectra are already sparse after the 128-peak restore.

**Failure mode.** Sparse 2–4 peak queries drop below `MIN_SIMILARITY` and fall back to placeholders. Mitigant: keep `MIN_SIMILARITY=0.05` and mass-window backfill 80 ppm.

## H2 — Entropy weight 0.75 (already live; do not resubmit)

`ENTROPY_WEIGHT=0.75` is on main. Re-pushing H-entropy is a no-op ticket.

## H3 — Flash fragment window 0.02 Da (next unused)

`PEAK_MZ_TOL` 0.01 → 0.02 matches Flash `ms2_tolerance_in_da=0.02`. Hold until H1 is scored.

## H4 — Raise min similarity to 0.12 (later)

Drops weak cosine ties. Cloud PRs #11/#12 never merged. Risk of empty lists on sparse queries.

## Ablation this slot

**One major factor:** H1. `config_patch = {"INTENSITY_FLOOR": 0.01}`. Also retarget Actions slot-2 fallback so the next `casmi-loop` applies H-intensity instead of H-entropy.
