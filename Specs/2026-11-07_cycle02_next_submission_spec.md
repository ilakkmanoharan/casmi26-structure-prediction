# Spec — 2026-11-07 cycle02

One major ablation vs live main after Actions 11-07 cycle01 (kernel v202 / Kaggle 58076904).

```json
{"MASS_TOL_PPM": 15.0}
```

config_patch: {"MASS_TOL_PPM": 15.0}

## Hold constant (do not confound H1)

| Constant | Live value |
|----------|------------|
| `MASS_TOL_PPM_BACKFILL` | 80.0 |
| `TOP_PEAKS` | 128 |
| `PEAK_MZ_TOL` | 0.02 |
| `ENTROPY_WEIGHT` | 0.75 |
| `INTENSITY_FLOOR` | 0.01 |
| `TOP_K_SPECTRA_PER_QUERY` | 120 |
| `MIN_SIMILARITY` | 0.05 |
| `EXCLUDE_EXACT_DUPLICATES` | True |

## Implementation

1. Set `MASS_TOL_PPM = 15.0` in `casmi26/config.py`.
2. In `scripts/casmi_loop/chatgpt_spec.py`: slot-2 fallback = `{MASS_TOL_PPM: 15.0}` (H-mass-tight); slot-3 fallback = `{MASS_TOL_PPM: 15.0}` (H-mass-tight). Today’s next unused Actions slot is **2**; slot 1 already submitted H-top-peaks at 02:53Z.
3. Rebuild `kaggle_kernel/` with internet **off**; RDKit wheels dataset `ilakkmanoharan/rdkit-cp312-wheels-casmi26`.
4. `kaggle kernels push -p kaggle_kernel` → poll COMPLETE → `competition_submit_code` on `ilakkmanoharan/casmi26-retrieval-symbolic-v01`. **Never CSV submit.**
5. If Cloud secrets are absent, leave `submitted=false` / `skipped_reason=cloud_missing_kaggle_secrets` and rely on casmi-loop reusing these substantial docs (`config_patch` parsed from this spec).

## Submit message

`2026-11-07_cycle02 H-mass-tight MASS_TOL_PPM 35→15 (ibnmarzuk/timsTOF 15 ppm; backfill 80)`

## Acceptance

- `MASS_TOL_PPM == 15.0` in package and embedded notebook.
- `MASS_TOL_PPM_BACKFILL` remains 80.0.
- Slot-2 and slot-3 fallbacks are H-mass-tight, not H-peak-mz.
- Kernel metadata `enable_internet: false`.
- Pytest green.
