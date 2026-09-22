# Spec 2026-09-22_cycle01 — next submission

## Goal

One major ablation vs last submitted kernel v13 / Kaggle **56298621**: restore the fragment ladder so entropy + modified cosine can use more than five peaks.

## Config patch (existing `casmi26/config.py` constants only)

```json
{
  "TOP_PEAKS": 128
}
```

Unchanged from 56298621 (do not retune this slot):

| Constant | Value |
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

## Implementation

1. Set `TOP_PEAKS = 128` in `casmi26/config.py` with a short comment (Li/Fiehn + Flash Entropy; cycle05 5-peak cap).
2. Rebuild `kaggle_kernel/` via `scripts/casmi_loop/build_kernel.py`. `enable_internet: false`. Wheels: `ilakkmanoharan/rdkit-cp312-wheels-casmi26`.
3. Guardrails (not scoring ablations):
   - `scripts/casmi_loop/chatgpt_spec.py`: HTTP 429 / 5xx / URLError → `None` so Actions does not die before Kaggle.
   - `scripts/casmi_loop/submit.py`: `write_kaggle_credentials()` writes `~/.kaggle/kaggle.json` (0600) and `access_token` when env is present.
4. Tests: spectrum keep-more-than-five; OpenAI 429 fallback; credential helper (example values only).
5. Submit path (if secrets exist): `kaggle kernels push -p kaggle_kernel` → poll COMPLETE → `competition_submit_code` on `ilakkmanoharan/casmi26-retrieval-symbolic-v01`. **Never** CSV `competitions submit`.

## Success criteria

- `TOP_PEAKS == 128` in config and embedded notebook.
- Kernel metadata `enable_internet` is false.
- Pytest green.
- If Cloud secrets missing: record `submitted=false` and leave substantial docs so merged `casmi-loop` can submit this patch without calling OpenAI.

## Out of scope

Mass-window, entropy-weight, domain-prior, analog-search, and ranker-weight changes.
