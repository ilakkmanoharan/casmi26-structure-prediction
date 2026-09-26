# Spec — 2026-09-26 cycle02

## Goal

One-factor ablation vs current main (`c62e0a8` / 2026-09-26_cycle01): make hybrid similarity **entropy-dominant**.

## config_patch

```json
{"ENTROPY_WEIGHT": 0.75}
```

## Held constant (do not retouch)

| Constant | Value |
|----------|-------|
| `MASS_TOL_PPM` | 35.0 |
| `MASS_TOL_PPM_BACKFILL` | 80.0 |
| `PEAK_MZ_TOL` | 0.01 |
| `TOP_PEAKS` | 128 |
| `INTENSITY_FLOOR` | 0.001 |
| `TOP_K_SPECTRA_PER_QUERY` | 120 |
| `TOP_CANDIDATES_PER_SPECTRUM` | 25 |
| `MIN_SIMILARITY` | 0.05 |
| `EXCLUDE_EXACT_DUPLICATES` | true |
| `MAX_CANDIDATES` | 25 |

## Implementation

1. Set `ENTROPY_WEIGHT = 0.75` in `casmi26/config.py`.
2. Rebuild `kaggle_kernel/` (`enable_internet: false`; RDKit wheels `ilakkmanoharan/rdkit-cp312-wheels-casmi26`).
3. `kaggle kernels push -p kaggle_kernel`
4. Poll until `COMPLETE`.
5. `competition_submit_code` with message `2026-09-26_cycle02 H-entropy` on kernel `ilakkmanoharan/casmi26-retrieval-symbolic-v01`. Never CSV submit.

## Loop handoff

If Cloud cannot authenticate to Kaggle, leave these docs on the branch. `write_cycle_docs` will reuse them when they are substantial on the runner checkout. Also point Actions fallback slot 2 at this same patch so an OpenAI-429 path does not redo `H-mass-tight`.

## Success criteria

- Kernel embeds `ENTROPY_WEIGHT = 0.75`.
- Public MRR@25, when scored, is recorded in `agent/state.json`.
- No claim that Class-3 de novo is solved.
