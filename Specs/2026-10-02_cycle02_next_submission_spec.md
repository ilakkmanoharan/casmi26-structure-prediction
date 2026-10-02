# Spec — 2026-10-02 cycle02

## Goal

One-factor ablation vs current main (`6656535` / 2026-10-02_cycle01): match Flash Entropy / `ms-entropy` **1% noise floor**.

## config_patch

```json
{"INTENSITY_FLOOR": 0.01}
```

## Held constant (do not retouch)

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

1. Set `INTENSITY_FLOOR = 0.01` in `casmi26/config.py` (and the `clean_spectrum` default so standalone calls match).
2. Retarget Actions `FALLBACK_ABLATIONS[1]` from no-op `H-entropy` (`ENTROPY_WEIGHT=0.75`, already live) to `H-intensity` with this same patch, so the next hourly `casmi-loop` slot 2 cannot waste UTC ticket 2.
3. Rebuild `kaggle_kernel/` (`enable_internet: false`; RDKit wheels `ilakkmanoharan/rdkit-cp312-wheels-casmi26`).
4. `kaggle kernels push -p kaggle_kernel`
5. Poll until `COMPLETE` (do not busy-wait a 9h training window).
6. `competition_submit_code` with message `2026-10-02_cycle02 H-intensity` on kernel `ilakkmanoharan/casmi26-retrieval-symbolic-v01`. Never CSV submit.

## Loop handoff

If Cloud cannot authenticate to Kaggle, leave these docs + the code patch on the branch. `write_cycle_docs` will reuse substantial Research/Analysis/Hypothesis when present. Merge before the next hourly cron or slot 2 still submits the old entropy no-op.

## Success criteria

- Kernel embeds `INTENSITY_FLOOR = 0.01`.
- Slot-2 fallback hypothesis is `H-intensity`.
- Public MRR@25, when scored, is recorded in `agent/state.json`.
- No claim that Class-3 de novo is solved.
