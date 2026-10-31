# Spec 2026-10-31_cycle03

## Goal

Submit one unused real ablation vs live main after Actions 10-31 cycle02: raise the library-hit admission floor.

## config_patch

```json
{"MIN_SIMILARITY": 0.12}
```

Hold all other knobs: `TOP_PEAKS=128`, `PEAK_MZ_TOL=0.02`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, `MASS_TOL_PPM=35`, `MASS_TOL_PPM_BACKFILL=80`, `EXCLUDE_EXACT_DUPLICATES=True`.

## Actions fallback retarget (so the next unused hourly does not no-op)

| Slot | Current fallback | New fallback |
|------|------------------|--------------|
| 1 | H-top-peaks `TOP_PEAKS=128` | unchanged |
| 2 | H-peak-mz `PEAK_MZ_TOL=0.02` (live) | **H-min-sim `MIN_SIMILARITY=0.12`** |
| 3 | H-peak-mz `PEAK_MZ_TOL=0.02` (live) | **H-min-sim `MIN_SIMILARITY=0.12`** |
| 4 | H-peaks `TOP_PEAKS=160, MIN_SIMILARITY=0.05` | **H-peaks `TOP_PEAKS=160` only** |
| 5 | H-domain | unchanged |

## Kernel

Rebuild `kaggle_kernel/` from `casmi26/`. `enable_internet: false`. RDKit wheels: `ilakkmanoharan/rdkit-cp312-wheels-casmi26`. Kernel id: `ilakkmanoharan/casmi26-retrieval-symbolic-v01`.

## Submit

`kaggle kernels push -p kaggle_kernel` → poll COMPLETE → `competition_submit_code` only. Never CSV submit.

If Cloud secrets are missing: commit docs + code + `agent/state.json`, open PR, **do not** dispatch casmi-loop until merged (dispatch on current main would replay `PEAK_MZ_TOL=0.02`). Next unused hourly as of 10:34Z is **11:00 UTC**.

## Tests

- `MIN_SIMILARITY == 0.12`
- slot-2 and slot-3 fallbacks are H-min-sim
- slot-4 is `TOP_PEAKS=160` without `MIN_SIMILARITY` in the patch
