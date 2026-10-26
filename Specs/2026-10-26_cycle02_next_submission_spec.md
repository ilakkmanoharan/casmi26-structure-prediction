# Spec — 2026-10-26 cycle02

## Major ablation (one factor)

Raise the library-hit admission floor so junk hybrid scores do not fill `top_k_spectra`.

config_patch: {"MIN_SIMILARITY": 0.12}

Live baseline after Actions 2026-10-26 cycle01 (kernel v154):

| Constant | Live | This slot |
|----------|------|-----------|
| `MIN_SIMILARITY` | 0.05 | **0.12** |
| `TOP_PEAKS` | 128 | 128 (unchanged) |
| `PEAK_MZ_TOL` | 0.02 | 0.02 (unchanged) |
| `INTENSITY_FLOOR` | 0.01 | 0.01 (unchanged) |
| `ENTROPY_WEIGHT` | 0.75 | 0.75 (unchanged) |
| `MASS_TOL_PPM` / backfill | 35 / 80 | unchanged |
| `EXCLUDE_EXACT_DUPLICATES` | True | unchanged |

## Implementation steps

1. Set `MIN_SIMILARITY = 0.12` in `casmi26/config.py` (`RunConfig.min_similarity` already reads the constant).
2. Rebuild `kaggle_kernel/` via `scripts/casmi_loop/build_kernel.py` so the embedded notebook matches.
3. Keep `kaggle_kernel/kernel-metadata.json` at `enable_internet: false` and RDKit wheels `ilakkmanoharan/rdkit-cp312-wheels-casmi26`.
4. Retarget `FALLBACK_ABLATIONS` so the next unused Actions hours do not replay live `PEAK_MZ_TOL=0.02`:
   - slot-2 (index 1) → H-min-sim `{"MIN_SIMILARITY": 0.12}` (this patch)
   - slot-3 (index 2) → H-peaks `{"TOP_PEAKS": 160}` (do not reset `MIN_SIMILARITY`)
5. Update `tests/test_spectrum_and_loop.py` assertions for the new live constant and the two fallbacks.
6. Submit with **code** API only (`competition_submit_code`), kernel `ilakkmanoharan/casmi26-retrieval-symbolic-v01`. Never CSV-submit.

## Handoff if Cloud cannot push the kernel

Merge this PR before the next unused `casmi-loop` hourly (`0 * * * *`, next window ~07:00 UTC). `write_cycle_docs` will reuse these substantial cycle02 files and apply the same `config_patch`. If unmerged, Actions slot 2 wastes UTC ticket 2 on already-live `PEAK_MZ_TOL=0.02`.
