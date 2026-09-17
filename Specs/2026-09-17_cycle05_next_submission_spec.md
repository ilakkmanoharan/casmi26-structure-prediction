# Spec — 2026-09-17 cycle05

## Goal

One major ablation vs current main (`ENTROPY_WEIGHT=0.55`, mass 10/15 ppm, exact-dup ban on): push the hybrid toward entropy similarity.

## config_patch

```json
{"ENTROPY_WEIGHT": 0.70}
```

## Unchanged (do not touch this slot)

| Constant | Value |
|----------|-------|
| `MASS_TOL_PPM` | 10 |
| `MASS_TOL_PPM_BACKFILL` | 15 |
| `PEAK_MZ_TOL` | 0.05 |
| `TOP_PEAKS` | 128 |
| `INTENSITY_FLOOR` | 0.001 |
| `TOP_K_SPECTRA_PER_QUERY` | 80 |
| `TOP_CANDIDATES_PER_SPECTRUM` | 50 |
| `MIN_SIMILARITY` | 0.08 |
| `EXCLUDE_EXACT_DUPLICATES` | true |
| `MAX_CANDIDATES` | 25 |

Hybrid becomes `0.70 * entropy_similarity + 0.30 * modified_cosine`.

## Implementation

1. Set `ENTROPY_WEIGHT = 0.70` in `casmi26/config.py`.
2. Rebuild `kaggle_kernel/` (`enable_internet: false`; RDKit wheels `ilakkmanoharan/rdkit-cp312-wheels-casmi26`).
3. `kaggle kernels push -p kaggle_kernel`
4. Poll until COMPLETE (do not busy-wait a 9h training window).
5. `competition_submit_code` for `enveda-CASMI26-molecule-id-mass-spectra`, kernel `ilakkmanoharan/casmi26-retrieval-symbolic-v01`, **with `kernel_version`**. Never CSV `competitions submit`.

## Submission message

`2026-09-17_cycle05 ENTROPY_WEIGHT=0.70 entropy-dominant hybrid`

## Hypothesis

H1 (entropy-dominant hybrid). Cycle02 planned this; kernel v4 ERROR; still untested.

## Success criteria

- Kernel COMPLETE (not ERROR).
- Code submission created.
- Public MRR@25 > 0.143 would support H1; ~0.143 with COMPLETE kernel suggests ranking still poisoned or coverage-limited (try H3 next).
