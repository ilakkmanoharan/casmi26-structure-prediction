# Spec — 2026-09-29 cycle02

## One major change vs previous submit (56659366 / kernel v32)

Previous: `TOP_PEAKS=128` (already live).  
This slot: **noise floor only.**

```json
{"INTENSITY_FLOOR": 0.01}
```

config_patch: {"INTENSITY_FLOOR": 0.01}

## Hold constant

| Constant | Value |
|----------|-------|
| `MASS_TOL_PPM` | 35.0 |
| `MASS_TOL_PPM_BACKFILL` | 80.0 |
| `PEAK_MZ_TOL` | 0.01 |
| `TOP_PEAKS` | 128 |
| `TOP_K_SPECTRA_PER_QUERY` | 120 |
| `TOP_CANDIDATES_PER_SPECTRUM` | 25 |
| `MIN_SIMILARITY` | 0.05 |
| `ENTROPY_WEIGHT` | 0.75 |
| `EXCLUDE_EXACT_DUPLICATES` | true |
| `MAX_CANDIDATES` | 25 |

## Implementation

1. Set `INTENSITY_FLOOR = 0.01` in `casmi26/config.py`.
2. Rebuild `kaggle_kernel/` (`enable_internet: false`; RDKit wheels `ilakkmanoharan/rdkit-cp312-wheels-casmi26`).
3. Retarget Actions `FALLBACK_ABLATIONS[1]` (UTC slot 2) to H-intensity so the next `casmi-loop` applies this patch if OpenAI is missing and these docs are on main (`_substantial` reuse also reads this spec).
4. `kaggle kernels push -p kaggle_kernel`
5. Poll until COMPLETE.
6. `competition_submit_code` for `enveda-CASMI26-molecule-id-mass-spectra`, kernel `ilakkmanoharan/casmi26-retrieval-symbolic-v01`. Never CSV submit.

## Message

`2026-09-29_cycle02 H-intensity`

## Success checks

- Kernel metadata `enable_internet` is false.
- Embedded notebook config shows `intensity_floor: 0.01`.
- Pytest: floor constant, slot-2 fallback, and 1% cleaning behavior.
