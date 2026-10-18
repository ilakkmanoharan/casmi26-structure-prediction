# Spec — 2026-10-18 cycle03

## One major ablation

Raise the relative intensity floor to Flash Entropy / ms_entropy default (1% of base peak).

```json
{"INTENSITY_FLOOR": 0.01}
```

config_patch: {"INTENSITY_FLOOR": 0.01}

## Live constants after this slot (unchanged except floor)

| Constant | Value |
|----------|-------|
| `MASS_TOL_PPM` | 35.0 |
| `MASS_TOL_PPM_BACKFILL` | 80.0 |
| `PEAK_MZ_TOL` | 0.01 |
| `TOP_PEAKS` | 128 |
| `INTENSITY_FLOOR` | **0.01** (was 0.001) |
| `TOP_K_SPECTRA_PER_QUERY` | 120 |
| `TOP_CANDIDATES_PER_SPECTRUM` | 25 |
| `MIN_SIMILARITY` | 0.05 |
| `ENTROPY_WEIGHT` | 0.75 |
| `EXCLUDE_EXACT_DUPLICATES` | true |
| `MAX_CANDIDATES` | 25 |

## Implementation steps

1. Set `INTENSITY_FLOOR = 0.01` in `casmi26/config.py`.
2. Retarget Actions **slot-3** fallback (`FALLBACK_ABLATIONS[2]`) from H-mass-wide to H-intensity so a 429/no-key hourly run does not replay 35/80 ppm.
3. Rebuild `kaggle_kernel/` with internet **off**; RDKit wheels dataset `ilakkmanoharan/rdkit-cp312-wheels-casmi26`.
4. `kaggle kernels push -p kaggle_kernel` → poll COMPLETE → `competition_submit_code` on `ilakkmanoharan/casmi26-retrieval-symbolic-v01`. **Never CSV submit.**
5. If Cloud lacks Kaggle secrets: record skip, open PR, and rely on casmi-loop reuse of these docs (`_substantial` ≥ 400 chars).

## Kernel / submit constraints

- Notebook-only competition.
- `enable_internet: false`.
- Message: `2026-10-18_cycle03 H-intensity`.
- Do not claim Class-3 de novo is solved by retrieval.

## Success / rollback

- Success: public MRR@25 > 0.143 or a scored movement vs 57341340.
- Rollback: restore `INTENSITY_FLOOR = 0.001` if scored MRR drops.
