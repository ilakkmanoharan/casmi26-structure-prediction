# Spec — 2026-10-07 cycle02

## Goal

One-factor ablation vs current main (`6cfaf90` / 2026-10-07_cycle01):
raise the relative intensity denoiser from 0.1% to **1%**.

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
| `ENTROPY_WEIGHT` | 0.75 |
| `TOP_K_SPECTRA_PER_QUERY` | 120 |
| `TOP_CANDIDATES_PER_SPECTRUM` | 25 |
| `MIN_SIMILARITY` | 0.05 |
| `EXCLUDE_EXACT_DUPLICATES` | true |
| `MAX_CANDIDATES` | 25 |

## Implementation

1. Set `INTENSITY_FLOOR = 0.01` in `casmi26/config.py`.
2. Point `FALLBACK_ABLATIONS[1]` (Actions slot 2) at H-intensity so an
   OpenAI-missing / 429 path cannot redo live `ENTROPY_WEIGHT=0.75`.
3. Rebuild `kaggle_kernel/` (`enable_internet: false`; RDKit wheels
   `ilakkmanoharan/rdkit-cp312-wheels-casmi26`).
4. `kaggle kernels push -p kaggle_kernel`
5. Poll until `COMPLETE` (or `ERROR`).
6. `competition_submit_code` with message `2026-10-07_cycle02 H-intensity`
   on kernel `ilakkmanoharan/casmi26-retrieval-symbolic-v01`. Never CSV submit.

## Loop handoff

Docs in this folder are substantial. `write_cycle_docs` will reuse them and
parse `config_patch` when they are on the runner checkout. Merge before the
next hourly `casmi-loop` or UTC slot 2 wastes a ticket.

## Success criteria

- Kernel embeds `INTENSITY_FLOOR = 0.01`.
- Slot-2 fallback hypothesis is `H-intensity`.
- Public MRR@25, when scored, is recorded in `agent/state.json`.
- No claim that Class-3 de novo is solved.
