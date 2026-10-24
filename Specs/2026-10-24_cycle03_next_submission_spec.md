# Spec — 2026-10-24 cycle03

One major ablation vs live main after Actions 10-24 cycle02 (kernel v145 / Kaggle 57584149).

```json
{"PEAK_MZ_TOL": 0.02}
```

config_patch: {"PEAK_MZ_TOL": 0.02}

## Hold constant (do not confound H1)

| Constant | Live value |
|----------|------------|
| `TOP_PEAKS` | 128 |
| `ENTROPY_WEIGHT` | 0.75 |
| `INTENSITY_FLOOR` | 0.01 |
| `MASS_TOL_PPM` | 35.0 |
| `MASS_TOL_PPM_BACKFILL` | 80.0 |
| `TOP_K_SPECTRA_PER_QUERY` | 120 |
| `MIN_SIMILARITY` | 0.05 |
| `EXCLUDE_EXACT_DUPLICATES` | True |

## Implementation

1. Set `PEAK_MZ_TOL = 0.02` in `casmi26/config.py`.
2. In `scripts/casmi_loop/chatgpt_spec.py`: slot-2 fallback = `{PEAK_MZ_TOL: 0.02}` (H-peak-mz); slot-3 fallback = `{PEAK_MZ_TOL: 0.02}` (H-peak-mz). Today’s next unused Actions slot is **3**; slot 2 already submitted H-entropy at 05:48Z.
3. Rebuild `kaggle_kernel/` with internet **off**; RDKit wheels dataset `ilakkmanoharan/rdkit-cp312-wheels-casmi26`.
4. `kaggle kernels push -p kaggle_kernel` → poll COMPLETE → `competition_submit_code` on `ilakkmanoharan/casmi26-retrieval-symbolic-v01`. **Never CSV submit.**
5. If Cloud secrets are absent, leave `submitted=false` / `skipped_reason=cloud_missing_kaggle_secrets` and rely on casmi-loop reusing these substantial docs (`config_patch` parsed from this spec).

## Submit message

`2026-10-24_cycle03 H-peak-mz PEAK_MZ_TOL 0.01→0.02 (Flash Entropy 20 mDa)`

## Acceptance

- `PEAK_MZ_TOL == 0.02` in package and embedded notebook.
- Slot-2 and slot-3 fallbacks are H-peak-mz, not H-entropy / H-intensity.
- Kernel metadata `enable_internet: false`.
- Pytest green.
