# Hypotheses 2026-10-01_cycle01

From Research + Analysis. One major ablation this slot.

## H1 (run now) — 1% intensity floor

**Statement.** Raising `INTENSITY_FLOOR` from `0.001` to `0.01` (msentropy / Li–Fiehn / matchms FlashSimilarity default) removes sub-1% base-peak noise before hybrid entropy/modcos, which reduces false high-similarity library hits and **raises public MRR@25** versus the current 0.143 / null-score carousel.

**Why this slot.** It is the only unused P0 config constant. `TOP_PEAKS`, `ENTROPY_WEIGHT`, mass windows, and the H-domain prior dict are already live. Cloud PRs #13/#14 specified this patch and never merged, so Kaggle has never scored it.

**Expected MRR direction.** Up, or at worst flat. Cleaning is monotonic: we drop ions the literature already treats as noise. Rank of a true hit should not fall unless the true ladder *is* a set of &lt;1% peaks (rare for IDable MS/MS).

**Failure mode.** Sparse/low-S spectra lose the last informative ions and fall back to mass-only / placeholder candidates → MRR flat or slightly down. `EXCLUDE_EXACT_DUPLICATES` stays on, so we will not “win” by matching poisoned exact dups.

## H2 (next unused) — raise min similarity

`MIN_SIMILARITY` 0.05 → 0.12. Drops junk neighbors that currently occupy top-25 slots. Cloud PRs #11/#12. Do **not** stack with H1 today.

## H3 (later) — 20 mDa fragment tolerance

`PEAK_MZ_TOL` 0.01 → 0.02 to match Flash entropy’s default window. One-factor, later slot.

## H4 (not this kernel) — analog / de novo channel

Top public notebooks are analog/multi-evidence rankers (~0.32–0.34). Adding a *second* analog-propagation channel or a de novo model is a code change, not a config constant. Retrieval still does **not** solve Class-3 de novo.

## This slot

Run **H1 only**. Submission message: `2026-10-01_cycle01 H-intensity`.
