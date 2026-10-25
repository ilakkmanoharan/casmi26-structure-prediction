# Spec — 2026-10-25 cycle02

One major ablation vs live main after Actions 10-25 cycle01 (kernel v149 / Kaggle 57612600).

```json
{"TOP_PEAKS": 160}
```

config_patch: {"TOP_PEAKS": 160}

## Hold constant (do not confound H1)

| Constant | Live value |
|----------|------------|
| `PEAK_MZ_TOL` | 0.02 |
| `ENTROPY_WEIGHT` | 0.75 |
| `INTENSITY_FLOOR` | 0.01 |
| `MASS_TOL_PPM` | 35.0 |
| `MASS_TOL_PPM_BACKFILL` | 80.0 |
| `TOP_K_SPECTRA_PER_QUERY` | 120 |
| `MIN_SIMILARITY` | 0.05 |
| `EXCLUDE_EXACT_DUPLICATES` | True |

## Implementation

1. Set `TOP_PEAKS = 160` in `casmi26/config.py`.
2. In `scripts/casmi_loop/chatgpt_spec.py`: slot-2 fallback = `{TOP_PEAKS: 160, MIN_SIMILARITY: 0.05}` (H-peaks); slot-3 fallback = `{MIN_SIMILARITY: 0.12}` (H-min-sim). Today’s next unused Actions slot is **2** (hourly `0 * * * *`).
3. Rebuild `kaggle_kernel/` with internet **off**; RDKit wheels dataset `ilakkmanoharan/rdkit-cp312-wheels-casmi26`.
4. `kaggle kernels push -p kaggle_kernel` → poll COMPLETE → `competition_submit_code` on `ilakkmanoharan/casmi26-retrieval-symbolic-v01`. **Never CSV submit.**
5. If Cloud secrets are absent, leave `submitted=false` / `skipped_reason=cloud_missing_kaggle_secrets` and rely on casmi-loop reusing these substantial docs (`config_patch` parsed from this spec).

## Submit message

`2026-10-25_cycle02 H-peaks TOP_PEAKS 128→160 (Flash Entropy keep more ions)`

## Acceptance

- `TOP_PEAKS == 160` in package and embedded notebook.
- Slot-2 fallback is H-peaks; slot-3 fallback is H-min-sim, not H-peak-mz.
- Kernel metadata `enable_internet: false`.
- Pytest green.
