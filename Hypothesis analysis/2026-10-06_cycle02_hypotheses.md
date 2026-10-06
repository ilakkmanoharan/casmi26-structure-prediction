# Hypotheses 2026-10-06_cycle02

## H1 (this slot) — H-peak-mz

**Claim:** Raising `PEAK_MZ_TOL` from 0.01 to **0.02** increases the number of true fragment pairs in `hybrid_similarity` (entropy + modified cosine share `cfg.peak_mz_tol` in `casmi26/retrieve.py`). Flash Entropy Search and Li/Fiehn treat 20 mDa as the default match window because 10 mDa under-covers low-abundance and cross-library mass error. More true matches should lift the correct inchikey14’s score and MRR@25.

**Expected MRR direction:** up from 0.143 if we are missing in-tolerance fragment pairs; flat if 10 mDa already captures almost all true matches on this test set.

**Failure mode:** wider window also matches decoy fragments, inflating near-isobaric wrong structures. `EXCLUDE_EXACT_DUPLICATES` and structure-level mass filters stay on to limit that.

## H2 — H-intensity (deferred)

`INTENSITY_FLOOR` 0.001 → 0.01 (msentropy 1% noise floor). Scientifically sound; Cloud PRs #13–#19 already implement it and remain unmerged. Not this slot’s major factor.

## H3 — H-min-sim (deferred)

`MIN_SIMILARITY` 0.05 → 0.12. Cloud PRs #11–#12 never merged. Risk: sparse queries lose all neighbors.

## H4 — H-entropy (reject this slot)

`ENTROPY_WEIGHT=0.75` is already live. Actions slot-2 fallback must not repeat it.

## Chosen ablation

**H1 / H-peak-mz only.** One constant. Retarget Actions slot 2 fallback to the same patch so GitHub Actions can submit if this PR lands before the next hourly cron.
