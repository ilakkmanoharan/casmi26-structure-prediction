# Spec — next submission (cycle02)

## Objective

Raise public MRR@25 by making the entropy/modcos hybrid **entropy-dominant**, while keeping exact test↔train duplicate exclusion enabled. Notebook-only Kaggle code submit.

## Major ablation (one)

Raise entropy weight from 0.55 → **0.70**.

config_patch: {"ENTROPY_WEIGHT": 0.70}

## Constants to leave unchanged this slot

| Constant | Keep |
|----------|------|
| `EXCLUDE_EXACT_DUPLICATES` | `True` |
| `MASS_TOL_PPM` | `25.0` |
| `MASS_TOL_PPM_BACKFILL` | `60.0` |
| `PEAK_MZ_TOL` | `0.05` |
| `TOP_PEAKS` | `128` |
| `INTENSITY_FLOOR` | `0.001` |
| `TOP_K_SPECTRA_PER_QUERY` | `80` |
| `TOP_CANDIDATES_PER_SPECTRUM` | `50` |
| `MIN_SIMILARITY` | `0.08` |
| `MAX_CANDIDATES` | `25` |

## Implementation notes (Actions / implement.py)

1. Apply only the `config_patch` above to `casmi26/config.py`.
2. Rebuild index / run pipeline in internet-off kernel.
3. Confirm evidence: rank-1 not uniformly sim=1.0 from exact dups.
4. Submit via notebook competition code path — never CSV-only submit.

## Acceptance

- Unit tests pass
- No placeholders; ≤25 unique inchikey14 per molecule
- Kernel &lt; 9 h offline
- New public score visible on Kaggle

## Message string

`2026-09-15_cycle02 ENTROPY_WEIGHT=0.70 entropy-dominant hybrid`
