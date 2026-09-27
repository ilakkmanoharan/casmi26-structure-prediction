# Spec — 2026-09-27 cycle02

## Goal

One-factor ablation vs current main (`c20465a` / 2026-09-27_cycle01): raise the retrieval neighbor floor so weak hybrid ties no longer fill the top-25.

## config_patch

```json
{"MIN_SIMILARITY": 0.12}
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
| `ENTROPY_WEIGHT` | 0.75 |
| `EXCLUDE_EXACT_DUPLICATES` | true |
| `MAX_CANDIDATES` | 25 |

## Implementation

1. Set `MIN_SIMILARITY = 0.12` in `casmi26/config.py`.
2. Retarget `FALLBACK_ABLATIONS[1]` (Actions UTC slot 2) from no-op `H-entropy` to this same patch so `casmi-loop` does not waste the next hourly run.
3. Rebuild `kaggle_kernel/` (`enable_internet: false`; RDKit wheels `ilakkmanoharan/rdkit-cp312-wheels-casmi26`).
4. `kaggle kernels push -p kaggle_kernel`
5. Poll until `COMPLETE`.
6. `competition_submit_code` with message `2026-09-27_cycle02 H-min-sim` on kernel `ilakkmanoharan/casmi26-retrieval-symbolic-v01`. Never CSV submit.

## Loop handoff

If Cloud cannot authenticate to Kaggle, leave these docs on the branch. `write_cycle_docs` will reuse them when they are substantial on the runner checkout. Actions fallback slot 2 is pointed at this same patch so an OpenAI-429 path does not redo `ENTROPY_WEIGHT=0.75`.

## Success criteria

- Kernel embeds `MIN_SIMILARITY = 0.12`.
- Public MRR@25, when scored, is recorded in `agent/state.json`.
- No claim that Class-3 de novo is solved.
