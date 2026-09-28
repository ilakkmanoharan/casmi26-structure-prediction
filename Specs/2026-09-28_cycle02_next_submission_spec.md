# Spec — 2026-09-28 cycle02

One major ablation: raise the hybrid similarity floor so weak decoys no longer fill MRR@25 after the exact-dup ban.

## config_patch

```json
{"MIN_SIMILARITY": 0.12}
```

Hold (do not change this slot):

| constant | keep |
|----------|------|
| `TOP_PEAKS` | 128 |
| `ENTROPY_WEIGHT` | 0.75 |
| `MASS_TOL_PPM` | 35.0 |
| `MASS_TOL_PPM_BACKFILL` | 80.0 |
| `TOP_K_SPECTRA_PER_QUERY` | 120 |
| `EXCLUDE_EXACT_DUPLICATES` | true |
| `PEAK_MZ_TOL` | 0.01 |
| `INTENSITY_FLOOR` | 0.001 |

## Implement

1. Set `MIN_SIMILARITY = 0.12` in `casmi26/config.py`.
2. Retarget Actions slot-2 fallback from H-entropy (already applied) to H-min-sim so a later hourly cron does not no-op.
3. Rebuild `kaggle_kernel/` (`enable_internet: false`; RDKit wheels `ilakkmanoharan/rdkit-cp312-wheels-casmi26`).
4. `kaggle kernels push -p kaggle_kernel` then `competition_submit_code` for `ilakkmanoharan/casmi26-retrieval-symbolic-v01`. **Never CSV submit.**

## Message

`2026-09-28_cycle02 H-min-sim`

## Hypothesis

`H-min-sim`

## Notes

Cloud Agent lacks Kaggle secrets; if this spec is on `main` before the next `casmi-loop` hour, Actions must perform push+submit. Do not claim Class-3 de novo is solved by retrieval.
