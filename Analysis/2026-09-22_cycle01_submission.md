# Analysis 2026-09-22_cycle01 — submissions, quota, why score is low

## Competition-day clock

- Trigger: Cloud Automation cron `0 6 * * *` at **2026-09-22T06:02:07Z**.
- Chicago local: **2026-09-22 01:02 CDT** — day start (01:00 America/Chicago). This is **cycle 01**.
- Daily limit: 5 code submits. Day key for this prompt: Chicago 01:00.

## Quota (0 / 5) — not exhausted

Cloud Agent env has **no** `KAGGLE_USERNAME`, `KAGGLE_KEY`, or `KAGGLE_API_TOKEN` (confirmed `printenv`; `~/.kaggle/` empty). Direct `kaggle competitions submissions` could not be run from this runner.

Proxy from GitHub Actions **35685129013** (`casmi-loop`, 2026-09-22T03:58:51Z), which *does* have Kaggle secrets:

```
submissions used today (2026-09-22): local=0 kaggle=0
kaggle submissions [
  (56298621, None, 'Implementing broader candidate libraries...'),
  (56290985, None, 'Optimizing mass tolerance parameters...'),
  (56290242, None, 'Refining mass tolerance parameters...'),
  (56289785, None, '2026-09-16 v10 rdkit-install fix + all-libs entropy/modcos'),
  (56289779, None, 'probe v3')
]
```

Those five refs are the **same** set as 2026-09-17 / 09-21. No submit has landed since kernel v13 / 56298621. Actions then died on **OpenAI HTTP 429** in `_openai_json` before implement/submit — same failure as 35311548455, 35421305696, 35492737629, 35561902203.

**Conclusion:** Chicago-day 2026-09-22 quota is **0/5**. Do not exit for quota. The blocker is (1) Cloud missing Kaggle secrets, (2) main `casmi-loop` crashing on OpenAI 429 so Actions cannot spend the quota either.

This Cloud run called `write_kaggle_credentials()` → **False** (no `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN`). `kaggle competitions submissions` and `kernels push` both stopped at kaggle 2.2 “Authentication required”. **No** `competition_submit_code` was issued. After this branch merges, hourly Actions (which has the secrets) can reuse these docs and submit.

## Public leaderboard (2026-09-22)

Fetched https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra/leaderboard

| Rank | Team | Public MRR@25 |
| --- | --- | --- |
| 1 | Ozymandias31415 | **0.415** |
| 2 | Randy | 0.388 |
| 3 | Udam Liyanage | 0.387 |
| 4 | DDM | 0.381 |
| 5 | Yousef Masad | 0.380 |

Yesterday’s memory still had GUAM **0.332** on top. The public field moved ~0.08 in a day. Open notebooks in the 0.33–0.34 band (Analog Ranker 0.337, Quad-Channel 0.339, Strong Retrieval 0.335) show the method cluster: analog / multi-channel ranking on full fragment ladders.

Our **best scored public** is still **0.143** (v0.1 exact-dup leak). Later code submits (56290242, 56290985, 56298621) still show `publicScore=None` in the Actions briefing.

## Why our score is low

1. **Poisoned exact duplicates (v0.1).** Test↔train spectrum copies in `enveda-180` carry train InChIKeys that are **not** competition GT. Perfect library match → ~0.143 public. `EXCLUDE_EXACT_DUPLICATES=True` is already on.
2. **Cycle05 `TOP_PEAKS=5` (live on main).** Last successful Actions submit (35194073264 → 56298621) applied this. `clean_spectrum()` then discards the fragment ladder that entropy / modified cosine / analog search need. Cloud cycles 09-18…09-21 all specified restore-to-128; those PRs (#4–#7) are still **DRAFT / unmerged**, so main and the kernel still run 5 peaks.
3. **No new scored submit in five days.** Actions hourly cron has failed every run since 2026-09-18 05:37Z on OpenAI 429. Cloud cron cannot `kernels push` without Kaggle secrets.

## Concrete improvements this slot

1. **Major ablation:** `TOP_PEAKS` 5 → **128** (only scoring-facing change).
2. **Unblock Actions:** `_openai_json` must return `None` on HTTP 429/5xx / URLError so `write_cycle_docs` uses deterministic fallback or, after this PR, the substantial pre-written docs.
3. **Cloud kaggle 2.2 helper:** write `~/.kaggle/kaggle.json` (0600) and `access_token` when env secrets exist (they do not on this runner).
4. After merge, hourly `casmi-loop` can reuse these docs, skip OpenAI, and `competition_submit_code` on kernel `ilakkmanoharan/casmi26-retrieval-symbolic-v01`.
