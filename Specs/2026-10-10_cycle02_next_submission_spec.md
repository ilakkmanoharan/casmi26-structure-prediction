# Spec 2026-10-10_cycle02

One major ablation vs live `main` (post Actions 2026-10-10_cycle01 / kernel v78).

## config_patch

```json
{"PEAK_MZ_TOL": 0.02}
```

## Live constants (do not change this slot)

| Constant | Live value |
| --- | --- |
| `MASS_TOL_PPM` | 35.0 |
| `MASS_TOL_PPM_BACKFILL` | 80.0 |
| `TOP_PEAKS` | 128 |
| `INTENSITY_FLOOR` | 0.001 |
| `TOP_K_SPECTRA_PER_QUERY` | 120 |
| `TOP_CANDIDATES_PER_SPECTRUM` | 25 |
| `MIN_SIMILARITY` | 0.05 |
| `ENTROPY_WEIGHT` | 0.75 |
| `EXCLUDE_EXACT_DUPLICATES` | true |
| `MAX_CANDIDATES` | 25 |

## Implementation

1. Set `PEAK_MZ_TOL = 0.02` in `casmi26/config.py`. `retrieve.py` already passes `tol=cfg.peak_mz_tol` into `hybrid_similarity`.
2. Retarget `FALLBACK_ABLATIONS[1]` in `scripts/casmi_loop/chatgpt_spec.py` from `H-entropy` / `ENTROPY_WEIGHT=0.75` to `H-peak-mz` / `PEAK_MZ_TOL=0.02`.
3. Rebuild `kaggle_kernel/` (`enable_internet: false`; RDKit wheels `ilakkmanoharan/rdkit-cp312-wheels-casmi26`).
4. `kaggle kernels push -p kaggle_kernel` then `competition_submit_code` for `ilakkmanoharan/casmi26-retrieval-symbolic-v01`. **Never CSV submit.**
5. If Cloud secrets are missing, commit this spec + code and merge before the next hourly `casmi-loop` so UTC slot 2 submits H-peak-mz instead of the live no-op.

## Success / fail

- Success: public MRR@25 &gt; 0.143 or a scored kernel that is not `None`.
- Fail: score stays 0.143 / `None` — revert slot-2 fallback and try `INTENSITY_FLOOR=0.01` next.
