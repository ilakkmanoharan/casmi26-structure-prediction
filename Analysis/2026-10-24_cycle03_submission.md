# Analysis — 2026-10-24 cycle03

## Quota (re-checked at 2026-10-24T06:05Z)

Competition day for this Cloud prompt starts **01:00 America/Chicago** (06:00 UTC). Kaggle’s enforced reset is midnight UTC (`scripts/casmi_loop/slots.py`).

Cloud runner has **no** `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN`, so the CLI list could not be refreshed here. Counts below come from Actions run **40066560089** logs + `origin/main` `agent/state.json` after the 05:48Z push (`b0a60f1`).

| Clock | Used | Remaining | Notes |
|-------|------|-----------|-------|
| UTC calendar 2026-10-24 | **2 / 5** | 3 | 57576969 (00:39Z), 57584149 (05:48Z) |
| Chicago 01:00 (since 06:00 UTC) | **0 / 5** | 5 | Both UTC tickets landed *before* 01:00 CDT |
| Quota exhausted? | **No** | — | Do not exit; implement + hand off |

## Recent Kaggle submissions (newest first, from Actions log)

- id=**57584149** score=None status=PENDING (at submit) desc=`2026-10-24_cycle02 H-entropy` kernel **v145** (Actions 40066560089, 05:48Z)
- id=**57576969** score=None status=COMPLETE desc=`2026-10-24_cycle01 H-top-peaks` kernel **v144** (Actions 40044740000, 00:39Z)
- id=57573321 score=None status=COMPLETE desc=`2026-10-23_cycle05 H-domain`
- id=57570294 score=None status=COMPLETE desc=`2026-10-23_cycle04 H-peaks`
- id=57564638 score=None status=COMPLETE desc=`2026-10-23_cycle03 H-intensity`
- id=57556346 score=None status=COMPLETE desc=`2026-10-23_cycle02 H-entropy`
- id=57548841 score=None status=COMPLETE desc=`2026-10-23_cycle01 H-top-peaks`

All recent public scores are **null**. Best scored public remains **0.143** (v0.1).

## Leaderboard context (CLIST ~2026-10-24T06:10Z, ~hours stale)

Public top: **Oleksandr Parfionov 0.50**, **pikachu 0.50**, **CHU1PC 0.50**, Savko 0.49, JJ 0.49, MarvinTMB / Oliver Ford / Dunyuan Zha / Parth Talsania 0.48. Community analog notebooks still ~0.43–0.46. Gap vs our 0.143 is not a missing `TOP_PEAKS` or `ENTROPY_WEIGHT` constant — those are already live.

## Why the score is low

1. **Poisoned exact duplicates (v0.1 failure).** Exact test↔train spectrum copies exist in `enveda-180` whose train InChIKey14 ≠ competition GT. Exact-dup exclusion is on; that prevents the 0.143 “perfect library match” trap from repeating, but it also removes the easy rank-1 hits.

2. **Fragment pairing is still 10 mDa.** `hybrid_similarity` / `_greedy_match` use `tol=cfg.peak_mz_tol` (`casmi26/retrieve.py`). Live `PEAK_MZ_TOL=0.01` is half the Flash Entropy / ms_entropy / matchms default (0.02 Da). Cross-library CE and centroid error routinely exceed 10 mDa on mid-intensity ions, so true-structure near-matches fall below `MIN_SIMILARITY=0.05` and never enter the top-25.

3. **Slot rotation has been a no-op for weeks.** Live main after Actions 10-24 cycle02: `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, mass-wide 35/80, `TOP_K=120`, `MIN_SIMILARITY=0.05`, **`PEAK_MZ_TOL=0.01`**. Replaying H-intensity (slot-3 fallback) does not change the spectrum object.

## Concrete improvement for this slot

Implement **one** major ablation: `PEAK_MZ_TOL` **0.01 → 0.02**.

Retarget Actions **slot-2** (already burned today; protects future UTC days) and **slot-3** (next unused hourly, historically ~07:00 UTC after today’s 05:31 run) from already-live H-entropy / H-intensity to **H-peak-mz**.

If this PR is **not** merged before that slot, Actions will spend UTC ticket 3 on `INTENSITY_FLOOR=0.01` — a third no-op today.

## Cloud submit attempt (this runner)

`write_kaggle_credentials()` returned **False**. `KAGGLE_USERNAME`, `KAGGLE_KEY`, and `KAGGLE_API_TOKEN` are unset; `~/.kaggle/kaggle.json` was not written. No `kernels push` / `competition_submit_code` from Cloud. Handoff is the substantial cycle03 docs + `config_patch: {"PEAK_MZ_TOL": 0.02}` so casmi-loop slot 3 can reuse them after merge.
