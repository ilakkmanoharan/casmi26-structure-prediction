# Spec — 2026-10-03 cycle02

## One major ablation

Apply Li / Fiehn / Flash Entropy **1% noise floor**. Leave every other live constant unchanged.

```json
{"INTENSITY_FLOOR": 0.01}
```

## Live constants (do not revert)

| Constant | Keep |
|----------|------|
| `TOP_PEAKS` | 128 |
| `ENTROPY_WEIGHT` | 0.75 |
| `MASS_TOL_PPM` | 35.0 |
| `MASS_TOL_PPM_BACKFILL` | 80.0 |
| `TOP_K_SPECTRA_PER_QUERY` | 120 |
| `MIN_SIMILARITY` | 0.05 |
| `PEAK_MZ_TOL` | 0.01 |
| `EXCLUDE_EXACT_DUPLICATES` | true |
| `MAX_CANDIDATES` | 25 |

## Actions handoff

Retarget `FALLBACK_ABLATIONS[1]` (slot 2) from `H-entropy` / `ENTROPY_WEIGHT=0.75` to `H-intensity` / `INTENSITY_FLOOR=0.01` so hourly `casmi-loop` submits this factor if Cloud cannot `kernels push`.

## Kernel

- Rebuild `kaggle_kernel/` from `casmi26/` (`enable_internet: false`).
- RDKit wheels: `ilakkmanoharan/rdkit-cp312-wheels-casmi26`.
- Submit **code only**: kernel `ilakkmanoharan/casmi26-retrieval-symbolic-v01`. Never CSV.

## Success / rollback

- Success: public MRR@25 > 0.143 or a scored movement vs the silent COMPLETE streak.
- Rollback: restore `INTENSITY_FLOOR=0.001` and slot-2 H-entropy if MRR drops or fallback_molecules spike.
