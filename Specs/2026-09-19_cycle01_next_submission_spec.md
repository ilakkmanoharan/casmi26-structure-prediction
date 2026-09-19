# Spec — next submission (2026-09-19 cycle01)

## Objective

Raise public MRR@25 by restoring the MS/MS fragment ladder after cycle05 truncated every spectrum to five peaks. Notebook-only Kaggle **code** submit (`competition_submit_code`). Internet **off**.

## Major ablation (one)

Restore `TOP_PEAKS` from 5 → **128**.

```json
{"TOP_PEAKS": 128}
```

config_patch: {"TOP_PEAKS": 128}

## Constants to leave unchanged this slot

| Constant | Keep |
|----------|------|
| `EXCLUDE_EXACT_DUPLICATES` | `True` |
| `MASS_TOL_PPM` | `10` |
| `MASS_TOL_PPM_BACKFILL` | `15` |
| `PEAK_MZ_TOL` | `0.01` |
| `INTENSITY_FLOOR` | `0.001` |
| `TOP_K_SPECTRA_PER_QUERY` | `80` |
| `TOP_CANDIDATES_PER_SPECTRUM` | `25` |
| `MIN_SIMILARITY` | `0.08` |
| `ENTROPY_WEIGHT` | `0.6` |
| `MAX_CANDIDATES` | `25` |

## Supporting (not a scoring ablation)

1. `scripts/casmi_loop/chatgpt_spec.py`: on OpenAI HTTP 429/5xx or URL error, return `None` so the existing deterministic fallback writes docs and the slot still implements + submits (Actions 35311548455 / 35421305696 crashed before push).
2. `scripts/casmi_loop/submit.py`: materialize `~/.kaggle/kaggle.json` (mode 0600) and `access_token` from env when present (kaggle 2.2).
3. Rebuild `kaggle_kernel/` with `enable_internet: false` and RDKit wheels dataset `ilakkmanoharan/rdkit-cp312-wheels-casmi26`.

## Implementation notes

1. Apply only the `config_patch` above to `casmi26/config.py`.
2. Rebuild the kernel via `scripts/casmi_loop/build_kernel.py`.
3. `kaggle kernels push -p kaggle_kernel` then poll to COMPLETE.
4. `competition_submit_code` on kernel `ilakkmanoharan/casmi26-retrieval-symbolic-v01` — never CSV `competitions submit`.
5. If Cloud secrets are missing, still land the code so casmi-loop can reuse these substantial docs.

## Acceptance

- Unit tests pass
- Kernel metadata `enable_internet: false`
- ≤25 unique inchikey14 per molecule
- New public score visible on Kaggle after Actions/Cloud submit

## Message string

`2026-09-19_cycle01 TOP_PEAKS=128 restore fragment ladder`
