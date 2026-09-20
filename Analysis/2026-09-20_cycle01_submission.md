# Analysis 2026-09-20_cycle01 — quota, scores, why 0.143

## Competition-day clock

- Trigger: Cursor Automation cron `0 6 * * *` (2026-09-20T06:02:54Z).
- Local: **Sun Sep 20 01:03 CDT** → Chicago day **2026-09-20** opened (~3 min after 01:00).
- Cycle tag: `2026-09-20_cycle01` (first unused slot for this day).

## Quota (not exhausted)

This Cloud Agent does **not** have `KAGGLE_USERNAME` / `KAGGLE_KEY` /
`KAGGLE_API_TOKEN` in the environment, so `~/.kaggle/kaggle.json` could not be
written (kaggle CLI 2.2.4 present). Quota is taken from the last Actions run
that **did** authenticate:

**GitHub Actions `casmi-loop` 35492737629** (2026-09-20 05:51Z, ~12 min
before this cron):

```
submissions used today (2026-09-20): local=0 kaggle=0
=== casmi-loop 2026-09-20 slot 1 ===
```

Recent Kaggle rows from that log (newest first; **all publicScore=None**):

| id | publicScore | description |
| --- | --- | --- |
| 56298621 | None | cycle05 — broader libs + entropy/modcos + `TOP_PEAKS=5` |
| 56290985 | None | cycle04 — mass-tol optimization |
| 56290242 | None | cycle03 — mass-tol refinement |
| 56289785 | None | 2026-09-16 v10 rdkit-install + all-libs |
| 56289779 | None | probe v3 |

Last **scored** public MRR@25 remains **0.143** (v0.1 exact-dup failure).
No new scored submit since 2026-09-17. **0/5 used today — do not skip for quota.**

Actions then died on `urllib.error.HTTPError: HTTP Error 429` inside
`chatgpt_spec._openai_json` **before** implement/push/submit. Same failure
mode as every hourly run since 35311548455 (2026-09-18 05:37Z).

Unmerged draft PRs #4 (2026-09-18) and #5 (2026-09-19) already restore
`TOP_PEAKS=128` + 429 fallback but never landed on `main`, so the runner
still crashes and the last kernel still has `TOP_PEAKS=5`.

## Leaderboard context (public web, 2026-09-20)

From [Kaggle LB](https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra/leaderboard)
and [CLIST standings](https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/):

- Public LB ~33% of test; ~668 teams / ~3k submissions.
- Top: **GUAM 0.332**, Minal kharat123 0.324, Preechanon Chatthai 0.319.
- Gap: 0.143 → 0.332 is more than 2×. Retrieval is not exhausted; our last
  scored run matched poisoned `enveda-180` exact dups.

## Why the score is low

1. **Poisoned exact duplicates (v0.1).** Test spectra that are identical to
   `enveda-180` train rows carry train InChIKeys that are **not** competition
   GT. Perfect library match → wrong structure → MRR ~0.143.
2. **`TOP_PEAKS=5` (cycle05, last submitted kernel v13).** Entropy and
   modified cosine lose the fragment ladder. `spectra_identical` also
   coarsens, so the poison ban both over- and under-fires.
3. **No scored iterate since 2026-09-17.** Cloud Automation still lacks
   Kaggle secrets; Actions has secrets but dies on OpenAI 429 before submit.

## Concrete improvements this slot

1. **Major ablation:** `TOP_PEAKS` 5 → **128** (only competition-facing
   change vs 56298621).
2. **Runner fix (not an MRR ablation):** `_openai_json` must return `None`
   on HTTP 429/5xx so `casmi-loop` uses `FALLBACK_ABLATIONS` and still
   submits. Without this, even after docs land, the next hourly run on an
   unfixed `main` dies again if it calls OpenAI.
3. **Cloud submit:** cannot `kernels push` / `competition_submit_code`
   from this agent until Automation secrets include `KAGGLE_USERNAME` and
   `KAGGLE_KEY` (and `KAGGLE_API_TOKEN` for CLI 2.2). After merge, hourly
   Actions can reuse these substantial docs (`_substantial` ≥400 chars)
   and skip OpenAI entirely.

## Quota skip?

**No.** `submissions_today = 0` (Kaggle count from Actions 35492737629).
Submit is blocked only by missing Cloud secrets, not by the 5-slot cap.
