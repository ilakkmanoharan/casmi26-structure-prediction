# Spec — 2026-10-04 cycle02

## Major ablation

Apply the Li/Fiehn 1% noise floor. One constant vs live main.

```json
{"INTENSITY_FLOOR": 0.01}
```

## Live constants to keep

| Constant | Value | Why |
|----------|-------|-----|
| `TOP_PEAKS` | 128 | Cycle01 restore; do not revert to 5 |
| `ENTROPY_WEIGHT` | 0.75 | Li 2021 FDR<10% operating point; already live |
| `MASS_TOL_PPM` | 35.0 | Mass-wide |
| `MASS_TOL_PPM_BACKFILL` | 80.0 | Sparse-query recovery |
| `TOP_K_SPECTRA_PER_QUERY` | 120 | Mass-wide companion |
| `MIN_SIMILARITY` | 0.05 | Do not tighten in the same slot |
| `PEAK_MZ_TOL` | 0.01 | Next unused after this lands |
| `EXCLUDE_EXACT_DUPLICATES` | true | Poisoned exact-dup ban |

## Implementation

1. Set `INTENSITY_FLOOR = 0.01` in `casmi26/config.py`.
2. Match `clean_spectrum(..., intensity_floor=0.01)` default so unit calls agree with `RunConfig`.
3. Retarget `FALLBACK_ABLATIONS[1]` in `scripts/casmi_loop/chatgpt_spec.py` from `H-entropy` / `ENTROPY_WEIGHT=0.75` to `H-intensity` / `INTENSITY_FLOOR=0.01`.
4. Rebuild `kaggle_kernel/` with `enable_internet: false` and RDKit wheels dataset `ilakkmanoharan/rdkit-cp312-wheels-casmi26`.
5. `kaggle kernels push -p kaggle_kernel` → poll COMPLETE → `competition_submit_code` kernel `ilakkmanoharan/casmi26-retrieval-symbolic-v01`. Never CSV submit.

## Tests

- Assert `INTENSITY_FLOOR == 0.01`.
- `clean_spectrum` drops a 0.5% peak and keeps 2% / base-peak ions.
- Slot-2 fallback hypothesis is `H-intensity` with `{"INTENSITY_FLOOR": 0.01}`.

## Notes

If Cloud cannot authenticate to Kaggle, still land the code + fallback retarget so the next hourly `casmi-loop` submits this ablation instead of wasting UTC slot 2 on `ENTROPY_WEIGHT=0.75`.
