# Spec — 2026-11-07 cycle02

## Ablation (one major factor)

Set `ENTROPY_WEIGHT` from **0.75 → 1.0** so `hybrid_similarity` is pure Li/Fiehn entropy similarity. Do not change mass windows, peak cleaning, or the 0.05 admission floor in this kernel.

```json
config_patch: {"ENTROPY_WEIGHT": 1.0}
```

## Hold constant

| Constant | Live value | Why |
|----------|------------|-----|
| `MASS_TOL_PPM` | 35.0 | H3 / PR #83; do not confound |
| `MASS_TOL_PPM_BACKFILL` | 80.0 | Empty-list fill |
| `PEAK_MZ_TOL` | 0.02 | Flash Entropy default; already live |
| `TOP_PEAKS` | 128 | Already live; slot-1 today was this no-op |
| `INTENSITY_FLOOR` | 0.01 | Flash Entropy 1% noise cut |
| `TOP_K_SPECTRA_PER_QUERY` | 120 | Coverage |
| `TOP_CANDIDATES_PER_SPECTRUM` | 25 | MRR@25 list length |
| `MIN_SIMILARITY` | 0.05 | H2 / PR #82; do not confound |
| `EXCLUDE_EXACT_DUPLICATES` | True | Poisoned-label guard |
| `MAX_CANDIDATES` | 25 | Competition cap |

## Implementation steps

1. Set `ENTROPY_WEIGHT = 1.0` in `casmi26/config.py`.
2. Retarget `FALLBACK_ABLATIONS` so OpenAI-missing hourly runs cannot replay live `PEAK_MZ_TOL=0.02`:
   - slot 2 → `{"ENTROPY_WEIGHT": 1.0}` (this patch)
   - slot 3 → `{"MIN_SIMILARITY": 0.12}` (H-sim-gate)
   - slot 4 → `{"MASS_TOL_PPM": 15.0}` (H-mass-tight)
3. Update `tests/test_spectrum_and_loop.py` assertions for the live constant and the new fallbacks.
4. Rebuild `kaggle_kernel/` (`enable_internet: false`; RDKit wheels `ilakkmanoharan/rdkit-cp312-wheels-casmi26`).
5. `kaggle kernels push -p kaggle_kernel` then `competition_submit_code` for `ilakkmanoharan/casmi26-retrieval-symbolic-v01`. Never CSV submit.

## Actions handoff

If Cloud cannot authenticate to Kaggle, leave these docs on the branch. `write_cycle_docs` reuses substantial pre-written cycle02 files when they are on the runner checkout, parsing the `config_patch` JSON above. Also point Actions fallback slot 2 at this same patch so an OpenAI-429 path does not redo `H-peak-mz`.

## Kernel checks

- Kernel embeds `ENTROPY_WEIGHT = 1.0`.
- `enable_internet` remains false.
- No claim that retrieval solves Class-3 de novo.

## Submit message

`2026-11-07_cycle02 H-entropy-pure ENTROPY_WEIGHT=1.0`
