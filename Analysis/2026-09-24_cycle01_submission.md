# Analysis — 2026-09-24 cycle01

## Quota check (Chicago competition day 2026-09-24)

Day start: **01:00 America/Chicago (CDT)** = 06:00 UTC. Daily limit 5 code submits.

**Cloud Agent cannot call the Kaggle API.** `KAGGLE_USERNAME`, `KAGGLE_KEY`, and `KAGGLE_API_TOKEN` are unset in this environment. `~/.kaggle/` exists but is empty. Kaggle CLI 2.2.4 prints “Authentication required” and will not list submissions. This is the same Cloud secret gap recorded every day since 2026-09-16.

**Proxy used instead of a live `kaggle competitions submissions` call:** GitHub Actions run [35953065654](https://github.com/ilakkmanoharan/casmi26-structure-prediction/actions/runs/35953065654) (2026-09-24T03:49:42Z) authenticated with repo Kaggle secrets and printed:

```
submissions used today (2026-09-24): local=0 kaggle=0
kaggle submissions [
  (56298621, None, 'Implementing broader candidate libraries...'),
  (56290985, None, 'Optimizing mass tolerance parameters...'),
  (56290242, None, 'Refining mass tolerance parameters...'),
  (56289785, None, '2026-09-16 v10 rdkit-install fix + all-libs entropy/modcos'),
  (56289779, None, 'probe v3')
]
```

Newest ids are still the 2026-09-17 cycle03–05 code submits. No later `casmi-loop` run had completed by ~06:10 UTC (next listed failure is still 03:49Z).

**Conclusion: `submissions_today = 0` &lt; 5. Quota is not exhausted. Do not exit.** A Cloud `kernels push` / `competition_submit_code` still cannot run until Cursor injects Kaggle secrets.

## Recent public scores

| Ref | When (approx) | Message | Public MRR@25 |
|-----|----------------|---------|----------------|
| 56298621 | 2026-09-17 cycle05 | broader libs + mass filters + entropy/modcos | **null** (never posted) |
| 56290985 | 2026-09-17 cycle04 | mass-tol optimization | **null** |
| 56290242 | 2026-09-17 cycle03 | mass-tol refinement | **null** |
| v0.1 (state) | first scored kernel | exact-dup library match | **0.143** |

Best committed public score remains **0.143**. Public LB top **GUAM 0.332** (Kaggle, 2026-09-24). Gap ≈ 0.19.

## Why the score is low

1. **Poisoned exact duplicates (v0.1).** Identical test↔train spectra in `enveda-180` carry train SMILES that are **not** competition GT. A perfect match still scored ~0.143. Cycle05 already sets `EXCLUDE_EXACT_DUPLICATES=True`. Keep that.

2. **`TOP_PEAKS=5` on `main` (cycle05 config_patch).** `clean_spectrum` keeps only the five strongest ions for **both** the query and the library index. Entropy similarity (Li 2021) and modified cosine then compare 5-peak stubs. That is the most destructive live setting. Cloud PRs 4–9 (09-18…09-23) restore 128 but are still unmerged drafts; Actions never applied them because it dies first.

3. **Actions cannot submit.** Every hourly `casmi-loop` since 2026-09-18 05:37Z fails in `chatgpt_spec._openai_json` with `HTTP Error 429: Too Many Requests` **after** it has already counted `kaggle=0`. Last successful submit: run 35194073264 → Kaggle **56298621**. Until 429 is caught, the 5-slot quota is wasted as no-ops.

4. **Unscored 09-17 kernels.** cycle03–05 public scores are still null. We cannot treat mass-tol 5/10/15 ppm as validated.

5. **Retrieval ceiling.** Even a healthy library search cannot solve Class-3 de novo. Leaders near 0.33 are still well below 1.0.

## Concrete improvements for this slot

1. **Major ablation:** `TOP_PEAKS` 5 → **128** (restore fragment ladder; one factor).
2. **Unblock Actions:** `_openai_json` returns `None` on HTTP 429/5xx so `write_cycle_docs` uses `FALLBACK_ABLATIONS`. Slot-1 fallback must itself be `TOP_PEAKS=128`.
3. **Credentials helper:** write `~/.kaggle/kaggle.json` (mode 0600) + `access_token` when env vars exist (needed for kaggle 2.2). Cloud still has no values today.
4. **Do not** change `MASS_TOL_PPM`, `ENTROPY_WEIGHT`, or library priors in the same slot.

## What we will not claim

Restoring 128 peaks does not solve Class-3 structures that are absent from every attached library. It only gives the hybrid scorer the ions the literature methods assume.
