# Spec — 2026-11-05 cycle02

One major ablation vs live main after Actions 11-05 cycle01 (kernel v195 / Kaggle 58012064).

```json
{"ENTROPY_WEIGHT": 1.0}
```

config_patch: {"ENTROPY_WEIGHT": 1.0}

## Hold constant (do not confound H1)

| Constant | Live value |
|----------|------------|
| `TOP_PEAKS` | 128 |
| `PEAK_MZ_TOL` | 0.02 |
| `INTENSITY_FLOOR` | 0.01 |
| `MASS_TOL_PPM` | 35.0 |
| `MASS_TOL_PPM_BACKFILL` | 80.0 |
| `TOP_K_SPECTRA_PER_QUERY` | 120 |
| `MIN_SIMILARITY` | 0.05 |
| `EXCLUDE_EXACT_DUPLICATES` | True |

## Implementation

1. Set `ENTROPY_WEIGHT = 1.0` in `casmi26/config.py`.
2. In `scripts/casmi_loop/chatgpt_spec.py`: slot-2 fallback = `{ENTROPY_WEIGHT: 1.0}` (H-entropy-pure); slot-3 fallback = `{MIN_SIMILARITY: 0.12}` (H-min-sim). Today’s next unused Actions slot is **2**; slot 1 already submitted H-top-peaks at 06:06Z. Slot-4 fallback = `{TOP_PEAKS: 160}` only (do not roll `MIN_SIMILARITY` back to 0.05).
3. Rebuild `kaggle_kernel/` with internet **off**; RDKit wheels dataset `ilakkmanoharan/rdkit-cp312-wheels-casmi26`.
4. `kaggle kernels push -p kaggle_kernel` → poll COMPLETE → `competition_submit_code` on `ilakkmanoharan/casmi26-retrieval-symbolic-v01`. **Never CSV submit.**
5. If Cloud secrets are absent, leave `submitted=false` / `skipped_reason=cloud_missing_kaggle_secrets` and rely on casmi-loop reusing these substantial docs (`config_patch` parsed from this spec).

## Submit message

`2026-11-05_cycle02 H-entropy-pure ENTROPY_WEIGHT 0.75→1.0 (drop modified cosine)`

## Acceptance

- `ENTROPY_WEIGHT == 1.0` in package and embedded notebook.
- Slot-2 fallback is H-entropy-pure, not H-peak-mz.
- Slot-3 fallback is H-min-sim (`MIN_SIMILARITY=0.12`), not a second H-peak-mz.
- Kernel metadata `enable_internet: false`.
- Pytest green.
