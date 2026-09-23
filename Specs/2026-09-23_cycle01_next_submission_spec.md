# Spec — 2026-09-23 cycle01

## Objective

Restore fragment-ion coverage for the entropy/modcos hybrid so the next code submit is identifiable against kernel v13 / Kaggle 56298621 (`TOP_PEAKS=5`). Notebook-only `competition_submit_code`. Never CSV `competitions submit`.

## Major ablation (one)

Restore `TOP_PEAKS` from 5 → **128**.

config_patch: {"TOP_PEAKS": 128}

```json
{"TOP_PEAKS": 128}
```

## Constants to leave unchanged this slot

| Constant | Keep (current main / v13) |
|----------|---------------------------|
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

## Implementation notes

1. Apply only the `config_patch` above to `casmi26/config.py`.
2. Rebuild `kaggle_kernel/` with `enable_internet: false` and RDKit wheels dataset `ilakkmanoharan/rdkit-cp312-wheels-casmi26`.
3. Also (infra, not a scoring ablation): `_openai_json` must return `None` on HTTP 429 / URL errors so `casmi-loop` uses fallback docs instead of dying with quota remaining. Write `~/.kaggle/kaggle.json` + `access_token` when env secrets exist (kaggle CLI 2.2).
4. Submit via `kaggle kernels push` → poll COMPLETE → `competition_submit_code` on `ilakkmanoharan/casmi26-retrieval-symbolic-v01`. Never CSV submit.

## Acceptance

- Unit tests pass, including `TOP_PEAKS == 128` and `clean_spectrum` keeping >5 ions
- Kernel metadata `enable_internet: false`
- No placeholders required for a valid 25-SMILES row
- New public score visible on Kaggle after Actions (or Cloud) submit

## Message string

`2026-09-23_cycle01 restore TOP_PEAKS=128 fragment ladder`
