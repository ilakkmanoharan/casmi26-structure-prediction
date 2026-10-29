# Spec — 2026-10-29 cycle03

One major ablation vs live main after Actions 10-29 cycle02 (kernel v168 / Kaggle 57767052).

```json
{"MIN_SIMILARITY": 0.12}
```

config_patch: {"MIN_SIMILARITY": 0.12}

## Hold constant (do not confound H1)

| Constant | Live value |
|----------|------------|
| `TOP_PEAKS` | 128 |
| `ENTROPY_WEIGHT` | 0.75 |
| `INTENSITY_FLOOR` | 0.01 |
| `PEAK_MZ_TOL` | 0.02 |
| `MASS_TOL_PPM` | 35.0 |
| `MASS_TOL_PPM_BACKFILL` | 80.0 |
| `TOP_K_SPECTRA_PER_QUERY` | 120 |
| `EXCLUDE_EXACT_DUPLICATES` | True |

## Implementation

1. Set `MIN_SIMILARITY = 0.12` in `casmi26/config.py`.
2. In `scripts/casmi_loop/chatgpt_spec.py`: slot-3 fallback = `{MIN_SIMILARITY: 0.12}` (H-min-sim); slot-4 fallback = `{TOP_PEAKS: 160}` only (H-peaks; do **not** reset `MIN_SIMILARITY` to 0.05). Today’s next unused Actions slot is **3**; slot 2 already submitted H-peak-mz at ~09:53Z.
3. Rebuild `kaggle_kernel/` with internet **off**; RDKit wheels dataset `ilakkmanoharan/rdkit-cp312-wheels-casmi26`.
4. `kaggle kernels push -p kaggle_kernel` → poll COMPLETE → `competition_submit_code` on `ilakkmanoharan/casmi26-retrieval-symbolic-v01`. **Never CSV submit.**
5. If Cloud secrets are absent, leave `submitted=false` / `skipped_reason=cloud_missing_kaggle_secrets` and rely on casmi-loop reusing these substantial docs (`config_patch` parsed from this spec). Do not `workflow_dispatch` until this PR is on main — an unmerged dispatch replays `PEAK_MZ_TOL=0.02`.

## Submit message

`2026-10-29_cycle03 H-min-sim MIN_SIMILARITY 0.05→0.12`

## Acceptance

- `MIN_SIMILARITY == 0.12` in package and embedded notebook.
- Slot-3 fallback is H-min-sim, not a second H-peak-mz.
- Slot-4 fallback is `TOP_PEAKS=160` without resetting `MIN_SIMILARITY`.
- Kernel metadata `enable_internet: false`.
- Pytest green.
