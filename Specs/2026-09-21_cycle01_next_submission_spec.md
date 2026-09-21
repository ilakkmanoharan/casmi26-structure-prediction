# Spec 2026-09-21_cycle01

## Goal

One major ablation vs last **submitted** kernel (v13 / Kaggle 56298621): restore fragment-ion budget so entropy/modcos can use a real ladder.

## config_patch

```json
{
  "TOP_PEAKS": 128
}
```

Unchanged (do not restack):

| constant | value |
| --- | --- |
| `MASS_TOL_PPM` | 10 |
| `MASS_TOL_PPM_BACKFILL` | 15 |
| `PEAK_MZ_TOL` | 0.01 |
| `INTENSITY_FLOOR` | 0.001 |
| `TOP_K_SPECTRA_PER_QUERY` | 80 |
| `TOP_CANDIDATES_PER_SPECTRUM` | 25 |
| `MIN_SIMILARITY` | 0.08 |
| `ENTROPY_WEIGHT` | 0.6 |
| `EXCLUDE_EXACT_DUPLICATES` | true |
| `MAX_CANDIDATES` | 25 |

## Kernel

- Rebuild `kaggle_kernel/` from current `casmi26/` (`scripts/casmi_loop/build_kernel.py`).
- `enable_internet`: **false**
- Dataset: `ilakkmanoharan/rdkit-cp312-wheels-casmi26`
- Kernel id: `ilakkmanoharan/casmi26-retrieval-symbolic-v01`
- Submit with **`competition_submit_code` only** (never CSV).

## Infrastructure (same commit, not a second ablation)

1. `scripts/casmi_loop/chatgpt_spec.py`: on OpenAI HTTP 429/5xx or URLError, return `None` so `FALLBACK_ABLATIONS` / pre-written docs run. Stops Actions 35561902203-class crashes.
2. `scripts/casmi_loop/submit.py`: `write_kaggle_credentials()` writes `~/.kaggle/kaggle.json` (0600) and `access_token` when `KAGGLE_USERNAME` + `KAGGLE_KEY`/`KAGGLE_API_TOKEN` exist (kaggle CLI 2.2).

## Submit message

`2026-09-21_cycle01 restore TOP_PEAKS 5→128 (Flash Entropy fragment ladder)`

## Tests

- `TOP_PEAKS == 128`; `clean_spectrum(..., top_peaks=TOP_PEAKS)` keeps >5 ions.
- `_openai_json` returns `None` on HTTP 429 and URLError.
- `write_kaggle_credentials` no-op without env; mode 0600 with env.

## Cloud submit gate

If Cloud Agent still lacks Kaggle secrets: implement + commit, **do not** invent a CSV submit. Record `skipped_reason=missing_kaggle_secrets`. After this PR merges, hourly `casmi-loop` should reuse these substantial docs and submit.
