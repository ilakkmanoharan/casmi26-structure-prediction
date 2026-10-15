# Spec — 2026-10-15 cycle02

## Major ablation (one factor)

Raise the relative intensity floor to the Flash Entropy / matchms 1% cut.

config_patch: {"INTENSITY_FLOOR": 0.01}

## Keep unchanged

- `EXCLUDE_EXACT_DUPLICATES=True`
- `ENTROPY_WEIGHT=0.75`
- `TOP_PEAKS=128`
- `MASS_TOL_PPM=35.0`, `MASS_TOL_PPM_BACKFILL=80.0`, `TOP_K_SPECTRA_PER_QUERY=120`
- `PEAK_MZ_TOL=0.01` (H2 next)
- `MIN_SIMILARITY=0.05` (H3 later)
- Kernel `ilakkmanoharan/casmi26-retrieval-symbolic-v01`, `enable_internet: false`, RDKit wheels `ilakkmanoharan/rdkit-cp312-wheels-casmi26`

## Implementation

1. Set `INTENSITY_FLOOR = 0.01` in `casmi26/config.py` (and the `clean_spectrum` default so unconfigured calls match).
2. Retarget `FALLBACK_ABLATIONS[1]` from `H-entropy` / `ENTROPY_WEIGHT=0.75` to `H-intensity` / `INTENSITY_FLOOR=0.01`.
3. `python3 -m scripts.casmi_loop.build_kernel` — rebuild `kaggle_kernel/`.
4. `kaggle kernels push -p kaggle_kernel` → poll COMPLETE → `competition_submit_code` (never CSV).
5. If Cloud secrets are missing, commit this spec so Actions slot 2 reuses these docs (`_substantial` + parseable `config_patch`).

## Success / rollback

- Success: public MRR@25 > 0.143 or any newly scored submit beats the last scored sibling.
- Rollback: `INTENSITY_FLOOR=0.001` if Hit@25 collapses on sparse queries.
