# Analysis 2026-09-21_cycle01

Chicago competition day **2026-09-21** opened at 01:00 CDT (06:00 UTC). This is **cycle 1 / 5**.

## Preflight: Kaggle credentials

Cloud Agent env has **no** `KAGGLE_USERNAME`, `KAGGLE_KEY`, or `KAGGLE_API_TOKEN` (same as 2026-09-18/19/20 cloud cycles). `~/.kaggle/` exists but is empty. Could not write `kaggle.json` mode 0600 from secrets, so this run cannot call the Kaggle CLI/API.

GitHub Actions **does** inject those secrets (run [35561902203](https://github.com/ilakkmanoharan/casmi26-structure-prediction/actions/runs/35561902203) env shows `KAGGLE_USERNAME`/`KAGGLE_KEY`/`KAGGLE_API_TOKEN` set).

## Quota for this competition day

**Not exhausted. Count = 0/5. Do not skip for quota.**

Evidence:

- Actions 35561902203 (2026-09-21 04:40Z, `TZ=America/Chicago`) printed  
  `submissions used today (2026-09-21): local=0 kaggle=0`  
  then listed the five newest Kaggle rows (public scores still null):

  | id | publicScore | description |
  | --- | --- | --- |
  | 56298621 | None | cycle05: broader libs / entropy-modcos / TOP_PEAKS=5 |
  | 56290985 | None | cycle04: mass-tol optimization |
  | 56290242 | None | cycle03: mass-tol refinement |
  | 56289785 | None | 2026-09-16 v10 rdkit-install + all-libs |
  | 56289779 | None | probe v3 |

- No Kaggle id newer than **56298621** (2026-09-17). Hourly `casmi-loop` has failed every run since 2026-09-18 05:37Z on OpenAI **HTTP 429** in `_openai_json` (including 35492737629, 35421305696, 35561902203). Those failures abort **before** `kernels push`.

Note: Actions `competition_day()` is the **UTC calendar date** (`scripts/casmi_loop/slots.py`), not Chicago 01:00. 04:40Z is still 23:40 CDT on 2026-09-20, so that `kaggle=0` count is UTC-day 2026-09-21. CLOUD_CYCLE_PROMPT still uses Chicago 01:00. Either clock, today’s used submits are **0**.

## Why public MRR@25 is still ~0.143

1. **Last scored public is 0.143 (v0.1).** Later code submits have not published a publicScore in the Actions briefing.
2. **v0.1 failure mode still live:** exact test↔train spectrum duplicates in `enveda-180` with train labels ≠ competition GT. Exact-library hit on a poisoned InChIKey14 ranks the wrong structure at #1.
3. **v13 made similarity worse:** `TOP_PEAKS=5` throws away the fragment ladder entropy/modcos need. That is the last *submitted* config (`agent/state.json` cycle 2026-09-17_cycle05).
4. **Leaderboard gap:** public top is **GUAM 0.332** ([Kaggle LB](https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra/leaderboard), fetched 2026-09-21). Field is ~0.26–0.33 for the top 20; we are stuck at 0.143 until a post-v0.1 kernel actually scores.

## Why Actions cannot submit even with quota remaining

`write_cycle_docs` calls OpenAI whenever Research/Analysis/Hypothesis files are missing on **main**. Main still has no 2026-09-18/19/20/21 docs (those live only on unmerged draft PRs #4/#5/#6). `_openai_json` raises on HTTP 429 instead of falling back, so the job never reaches implement/submit.

Draft PRs #4–#6 already restore `TOP_PEAKS=128` and add the 429 fallback, but they are **unmerged**, so hourly runs keep crashing on the same main HEAD (`c9def7f`).

## Concrete improvements for this slot

1. **Major ablation vs last submit:** `TOP_PEAKS` 5 → **128**.
2. **Unblock Actions:** catch OpenAI HTTP 429/5xx and URL errors; use `FALLBACK_ABLATIONS` (or reuse these substantial docs after merge).
3. **Cloud kaggle 2.2:** write `~/.kaggle/kaggle.json` **and** `access_token` when env secrets exist (CLI 2.2 ignores json-only).
4. After merge, next hourly `casmi-loop` can reuse these docs (`_substantial`) and `competition_submit_code` without OpenAI.

This Cloud Agent will **not** `kernels push` / `competition_submit_code` because Kaggle secrets are not injected here. Skip reason is **missing_kaggle_secrets**, not quota.

## This-run outcome

- `write_kaggle_credentials()` returned False (env empty). No `kaggle.json` written.
- `kaggle kernels push -p kaggle_kernel` failed: Kaggle CLI **2.2.4** wants `KAGGLE_API_TOKEN` or `~/.kaggle/access_token`.
- Kernel rebuilt with `TOP_PEAKS=128`, `enable_internet=false`.
- Pytest: **20 passed**.
