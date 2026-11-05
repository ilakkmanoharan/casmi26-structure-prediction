# Spec — 2026-11-05 cycle02

## Goal

One-factor ablation vs current main (`8c9adc0` / 2026-11-05_cycle01): raise the hybrid admission floor so weak cosine/entropy ties stop filling the top-25.

## config_patch

```json
{"MIN_SIMILARITY": 0.12}
```

## Held constant (do not retouch)

| Constant | Value |
|----------|-------|
| `MASS_TOL_PPM` | 35.0 |
| `MASS_TOL_PPM_BACKFILL` | 80.0 |
| `PEAK_MZ_TOL` | 0.02 |
| `TOP_PEAKS` | 128 |
| `INTENSITY_FLOOR` | 0.01 |
| `TOP_K_SPECTRA_PER_QUERY` | 120 |
| `TOP_CANDIDATES_PER_SPECTRUM` | 25 |
| `ENTROPY_WEIGHT` | 0.75 |
| `EXCLUDE_EXACT_DUPLICATES` | true |
| `MAX_CANDIDATES` | 25 |

## Implementation

1. Set `MIN_SIMILARITY = 0.12` in `casmi26/config.py`.
2. In `scripts/casmi_loop/chatgpt_spec.py`: retarget slot-2 and slot-3 fallbacks to `{"MIN_SIMILARITY": 0.12}` (`H-min-sim`). Keep slot-4 extra-peaks but pin `MIN_SIMILARITY=0.12` so it does not undo the floor.
3. Rebuild `kaggle_kernel/` (`enable_internet: false`; RDKit wheels `ilakkmanoharan/rdkit-cp312-wheels-casmi26`).
4. `kaggle kernels push -p kaggle_kernel`
5. Poll until `COMPLETE`.
6. `competition_submit_code` with message `2026-11-05_cycle02 H-min-sim` on kernel `ilakkmanoharan/casmi26-retrieval-symbolic-v01`. Never CSV submit.

## Loop handoff

If Cloud cannot authenticate to Kaggle, leave these docs on the branch. `write_cycle_docs` reuses them when they are substantial on the runner checkout. Actions next unused UTC slot is **2** (`used=1` from 58012064). Merge before the next unused hourly (~13:00 UTC) or ticket 2 is another `PEAK_MZ_TOL=0.02` no-op.

After a successful submit of H-min-sim, the next unused real ablation is `MASS_TOL_PPM` 35→10 or `ENTROPY_WEIGHT` 0.75→1.0 — not another min-sim draft.

## Success criteria

- Package and embedded notebook both have `MIN_SIMILARITY = 0.12`.
- Kernel metadata keeps `enable_internet: false`.
- Public MRR@25, when scored, is recorded in `agent/state.json`.
- No claim that Class-3 de novo is solved.
