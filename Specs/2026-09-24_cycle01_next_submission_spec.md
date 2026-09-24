# Spec — 2026-09-24 cycle01

## One major ablation

Restore the fragment ladder that cycle05 destroyed.

```json
{
  "TOP_PEAKS": 128
}
```

config_patch: {"TOP_PEAKS": 128}

Do **not** change `MASS_TOL_PPM`, `MASS_TOL_PPM_BACKFILL`, `PEAK_MZ_TOL`, `INTENSITY_FLOOR`, `TOP_K_SPECTRA_PER_QUERY`, `TOP_CANDIDATES_PER_SPECTRUM`, `MIN_SIMILARITY`, `ENTROPY_WEIGHT`, `EXCLUDE_EXACT_DUPLICATES`, or `MAX_CANDIDATES`.

## Implementation

1. Set `TOP_PEAKS = 128` in `casmi26/config.py`.
2. Rebuild `kaggle_kernel/` via `scripts/casmi_loop/build_kernel.py`.
3. Confirm `kaggle_kernel/kernel-metadata.json` has `enable_internet: false` and dataset `ilakkmanoharan/rdkit-cp312-wheels-casmi26`.
4. Keep exact-dup InChIKey14 ban (`EXCLUDE_EXACT_DUPLICATES=True`).
5. Engineering (same PR, not a second score factor):  
   - `_openai_json` returns `None` on HTTP 429 / network errors so Actions uses `FALLBACK_ABLATIONS`.  
   - Slot-1 fallback `config_patch` is `{"TOP_PEAKS": 128}`.  
   - `write_kaggle_credentials()` writes `~/.kaggle/kaggle.json` (0600) and `access_token` from env when present.

## Submit path

- Kernel: `ilakkmanoharan/casmi26-retrieval-symbolic-v01`
- `kaggle kernels push -p kaggle_kernel`
- Poll until `COMPLETE`
- `competition_submit_code` only (never CSV `competitions submit`)
- Competition: `enveda-CASMI26-molecule-id-mass-spectra`
- Message: `2026-09-24_cycle01 restore TOP_PEAKS 5→128`

If Cloud secrets are missing, record `skipped_reason=missing_kaggle_secrets` and still push docs/code so Actions can submit after merge.

## Success criteria

- Unit tests pass, including peak-count and 429-fallback tests.
- Embedded kernel source contains `TOP_PEAKS = 128`.
- Internet remains disabled in kernel metadata.
- A Kaggle **code** submission is created **or** Analysis + `agent/state.json` explicitly record why not.
