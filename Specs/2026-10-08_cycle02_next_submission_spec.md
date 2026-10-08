# Spec 2026-10-08_cycle02

One major factor vs live `main` (kernel v70 / Actions 56927100 H-top-peaks).

## config_patch

```json
{"PEAK_MZ_TOL": 0.02}
```

| Constant | Live `main` | This slot |
| --- | --- | --- |
| `PEAK_MZ_TOL` | 0.01 | **0.02** |
| `TOP_PEAKS` | 128 | unchanged |
| `ENTROPY_WEIGHT` | 0.75 | unchanged |
| `MASS_TOL_PPM` / backfill | 35 / 80 | unchanged |
| `INTENSITY_FLOOR` | 0.001 | unchanged (next unused) |
| `MIN_SIMILARITY` | 0.05 | unchanged |
| `EXCLUDE_EXACT_DUPLICATES` | true | unchanged |

## Implementation

1. Set `PEAK_MZ_TOL = 0.02` in `casmi26/config.py`.
2. Retarget `FALLBACK_ABLATIONS[1]` from H-entropy to **H-peak-mz** so Actions slot 2 is not a no-op.
3. Rebuild `kaggle_kernel/` (`enable_internet: false`; RDKit wheels `ilakkmanoharan/rdkit-cp312-wheels-casmi26`).
4. `kaggle kernels push -p kaggle_kernel` then `competition_submit_code` on `ilakkmanoharan/casmi26-retrieval-symbolic-v01`. **Never** CSV `competitions submit`.
5. If Cloud lacks Kaggle secrets: leave the patch on a PR and merge before the next hourly `casmi-loop`.

## Success / stop

- Kernel COMPLETE + code submission created, or explicit skip `cloud_missing_kaggle_secrets`.
- Do not claim Class-3 de novo is solved.
