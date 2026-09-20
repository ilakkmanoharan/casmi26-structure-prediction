# Spec 2026-09-20_cycle01 — restore TOP_PEAKS 5→128

## Goal

One major factor vs last submitted kernel (v13 / Kaggle 56298621):
put the fragment ladder back into entropy + modified-cosine retrieval.

## config_patch

```json
{"TOP_PEAKS": 128}
```

Do **not** change in this kernel:

- `MASS_TOL_PPM` (10)
- `MASS_TOL_PPM_BACKFILL` (15)
- `PEAK_MZ_TOL` (0.01)
- `INTENSITY_FLOOR` (0.001)
- `TOP_K_SPECTRA_PER_QUERY` (80)
- `TOP_CANDIDATES_PER_SPECTRUM` (25)
- `MIN_SIMILARITY` (0.08)
- `ENTROPY_WEIGHT` (0.6)
- `EXCLUDE_EXACT_DUPLICATES` (true)
- `MAX_CANDIDATES` (25)
- domain priors / preferred libraries

## Implementation

1. Set `TOP_PEAKS = 128` in `casmi26/config.py` with a comment pointing at
   Li/Fiehn + Flash Entropy `max_peak_num`.
2. Rebuild `kaggle_kernel/` via `scripts/casmi_loop/build_kernel.py`.
   Keep `enable_internet: false` and RDKit wheels
   `ilakkmanoharan/rdkit-cp312-wheels-casmi26`.
3. Runner hardening (not part of the MRR ablation, required for Actions
   to submit after merge):
   - `_openai_json` catches `HTTPError` / `URLError` and returns `None`.
   - `write_kaggle_credentials()` writes `~/.kaggle/kaggle.json` (mode 0600)
     and `access_token` from env (kaggle CLI 2.2).
4. Tests: spectrum keeps >5 peaks at `TOP_PEAKS=128`; 429 fallback;
   credential helper no-ops without env and writes 0600 with dummy env.

## Submit path

- `kaggle kernels push -p kaggle_kernel`
- Poll until `COMPLETE` (treat `ERROR` as terminal).
- `competition_submit_code` on `ilakkmanoharan/casmi26-retrieval-symbolic-v01`
  with the **pushed version**. Never CSV submit.
- Message: `2026-09-20_cycle01 restore TOP_PEAKS 5→128 fragment ladder`

## If Cloud secrets are missing

Write this spec + code + docs, record `submitted=false` /
`skipped_reason=missing_kaggle_secrets` in `agent/state.json`, push a PR.
After merge, hourly `casmi-loop` should reuse these substantial docs and
submit H1 without calling OpenAI.
