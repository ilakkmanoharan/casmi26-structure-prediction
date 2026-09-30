# Spec — 2026-09-30 cycle02

## Goal

One major ablation vs Actions 36648798697 / Kaggle 56692019 (`H-top-peaks`, kernel v36): align spectrum cleaning with the Li/Fiehn + msentropy 1% noise floor.

## config_patch

```json
{"INTENSITY_FLOOR": 0.01}
```

config_patch: {"INTENSITY_FLOOR": 0.01}

## Unchanged (already live on main)

| Constant | Value |
|----------|-------|
| `TOP_PEAKS` | 128 |
| `ENTROPY_WEIGHT` | 0.75 |
| `MASS_TOL_PPM` | 35.0 |
| `MASS_TOL_PPM_BACKFILL` | 80.0 |
| `TOP_K_SPECTRA_PER_QUERY` | 120 |
| `MIN_SIMILARITY` | 0.05 |
| `EXCLUDE_EXACT_DUPLICATES` | true |
| `MAX_CANDIDATES` | 25 |

## Implementation

1. Set `INTENSITY_FLOOR = 0.01` in `casmi26/config.py`.
2. Rebuild `kaggle_kernel/` (`enable_internet: false`; RDKit wheels `ilakkmanoharan/rdkit-cp312-wheels-casmi26`).
3. Retarget `FALLBACK_ABLATIONS[1]` from `H-entropy` (already live, no-op) to `H-intensity` so the next hourly `casmi-loop` slot 2 applies this patch if Grok docs are not yet on main.
4. `kaggle kernels push -p kaggle_kernel` → poll COMPLETE → `competition_submit_code` for `ilakkmanoharan/casmi26-retrieval-symbolic-v01`. Never CSV submit.
5. Record in `agent/state.json`.

## Kernel / submit constraints

- Notebook-only competition.
- Internet off.
- If Cloud secrets are missing, still land the code + docs on a PR so Actions can submit after merge. Do not invent a CSV path.
