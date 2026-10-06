# Spec 2026-10-06_cycle02

## Major factor (one change)

Widen the hybrid entropy/modcos fragment match window to the Flash Entropy Search default.

```json
{"PEAK_MZ_TOL": 0.02}
```

config_patch: {"PEAK_MZ_TOL": 0.02}

| Constant | Live main | This slot |
|----------|-----------|-----------|
| `PEAK_MZ_TOL` | 0.01 | **0.02** |
| `INTENSITY_FLOOR` | 0.001 | unchanged |
| `TOP_PEAKS` | 128 | unchanged |
| `ENTROPY_WEIGHT` | 0.75 | unchanged |
| `MASS_TOL_PPM` / backfill | 35 / 80 | unchanged |
| `MIN_SIMILARITY` | 0.05 | unchanged |
| `EXCLUDE_EXACT_DUPLICATES` | true | unchanged |

## Implementation

1. Set `PEAK_MZ_TOL = 0.02` in `casmi26/config.py`.
2. Retarget `FALLBACK_ABLATIONS[1]` in `scripts/casmi_loop/chatgpt_spec.py` to H-peak-mz (`PEAK_MZ_TOL=0.02`) so Actions slot 2 is not a no-op.
3. Rebuild `kaggle_kernel/` (`enable_internet: false`; wheels `ilakkmanoharan/rdkit-cp312-wheels-casmi26`).
4. `kaggle kernels push -p kaggle_kernel` then `competition_submit_code` for `ilakkmanoharan/casmi26-retrieval-symbolic-v01`. Never CSV submit.

## Message

`2026-10-06_cycle02 H-peak-mz`

## Notes

Cloud Automation cannot push/submit without Kaggle secrets. If this spec is on main before the next `casmi-loop` hour, Actions should reuse these docs (`_substantial`) and apply the same patch.
