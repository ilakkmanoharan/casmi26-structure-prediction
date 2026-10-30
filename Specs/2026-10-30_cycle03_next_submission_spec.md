# Spec — 2026-10-30 cycle03

One major ablation vs live main after Actions cycle02.

## config_patch

```json
{"MIN_SIMILARITY": 0.12}
```

config_patch: {"MIN_SIMILARITY": 0.12}

## Hold (do not change)

| Constant | Live value |
|----------|------------|
| `TOP_PEAKS` | 128 |
| `PEAK_MZ_TOL` | 0.02 |
| `ENTROPY_WEIGHT` | 0.75 |
| `INTENSITY_FLOOR` | 0.01 |
| `MASS_TOL_PPM` / `_BACKFILL` | 35 / 80 |
| `TOP_K_SPECTRA_PER_QUERY` | 120 |
| `EXCLUDE_EXACT_DUPLICATES` | True |
| `MAX_CANDIDATES` | 25 |

## Implementation

1. Set `MIN_SIMILARITY = 0.12` in `casmi26/config.py`.
2. In `scripts/casmi_loop/chatgpt_spec.py`:
   - slot-2 fallback = `{MIN_SIMILARITY: 0.12}` (H-min-sim; protects future UTC days after today’s wasted H-peak-mz)
   - slot-3 fallback = `{MIN_SIMILARITY: 0.12}` (H-min-sim; **today’s next unused Actions slot is 3**, 10:00 UTC)
   - slot-4 fallback = `{TOP_PEAKS: 160}` only (H-peaks; do **not** reset `MIN_SIMILARITY` to 0.05)
3. Rebuild `kaggle_kernel/` (`enable_internet: false`; RDKit wheels `ilakkmanoharan/rdkit-cp312-wheels-casmi26`).
4. `kaggle kernels push -p kaggle_kernel` → poll `COMPLETE` → `competition_submit_code` for `ilakkmanoharan/casmi26-retrieval-symbolic-v01`. Never CSV submit.
5. If Cloud has no Kaggle secrets: skip push/submit; keep substantial cycle03 docs so casmi-loop slot 3 reuses them after merge. Do not dispatch unmerged casmi-loop (would replay `PEAK_MZ_TOL=0.02`).

## Kernel message

`2026-10-30_cycle03 H-min-sim MIN_SIMILARITY 0.05→0.12`

## Acceptance

- `MIN_SIMILARITY == 0.12` in package and embedded notebook.
- Slot-2 and slot-3 fallbacks are H-min-sim, not H-peak-mz.
- Slot-4 fallback is `TOP_PEAKS=160` without resetting `MIN_SIMILARITY`.
- Kernel metadata `enable_internet: false`.
