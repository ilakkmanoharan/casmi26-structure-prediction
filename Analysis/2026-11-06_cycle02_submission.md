# Analysis — 2026-11-06 cycle02

## Quota (re-checked at 2026-11-06T07:32Z)

Competition day for this Cloud prompt starts **01:00 America/Chicago**. This run fired at **01:31 CST / 07:31 UTC** — Chicago day **2026-11-06 is open**. Kaggle’s enforced reset is **midnight UTC** (`scripts/casmi_loop/slots.py` `competition_day()`).

Cloud runner has **no** `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN` (confirmed empty env; `~/.kaggle/` exists but has no `kaggle.json`). `write_kaggle_credentials()` is **False**. Counts below come from Actions run **42147867834** + `origin/main` `agent/state.json` after the 02:22Z push (`b0377dc`) + `gh run list` at 07:32Z.

| Clock | Used | Remaining | Notes |
|-------|------|-----------|-------|
| UTC calendar 2026-11-06 | **1 / 5** | 4 | Kaggle **58042294** (02:22Z, kernel v198, `2026-11-06_cycle01 H-top-peaks`). Last casmi-loop success: 42147867834 at 02:03Z. **03:00–07:00 UTC hourly did not fire.** |
| Chicago 01:00 (since 07:00 UTC) | **0 / 5** | 5 | 58042294 landed at 02:22Z, still on Chicago day **2026-11-05**. No Kaggle submit observed after 07:00 UTC. |
| Quota exhausted? | **No** | — | Do not exit; implement + hand off. Binding constraint is UTC 1/5. |

Could not call `kaggle competitions submissions` from this pod. Not treating that as quota-full.

## Recent Kaggle submissions (newest first, from Actions log 42147867834 + state.json)

- id=**58042294** score=None status=COMPLETE (recorded) desc=`2026-11-06_cycle01 H-top-peaks` kernel **v198** (Actions 42147867834, 02:22Z)
- id=**58035989** score=None status=COMPLETE desc=`2026-11-05_cycle03 H-peak-mz`
- id=**58026170** score=None status=COMPLETE desc=`2026-11-05_cycle02 H-peak-mz`
- id=**58012064** score=None status=COMPLETE desc=`2026-11-05_cycle01 H-top-peaks`
- id=**58001652** score=None status=COMPLETE desc=`2026-11-04_cycle04 H-peaks`
- id=57992996 score=None status=COMPLETE desc=`2026-11-04_cycle03 H-peak-mz`
- id=57979390 score=None status=COMPLETE desc=`2026-11-04_cycle02 H-peak-mz`
- id=57967804 score=None status=COMPLETE desc=`2026-11-04_cycle01 H-top-peaks`
- id=57961369 score=None status=COMPLETE desc=`2026-11-03_cycle04 H-peaks`
- id=57953771 score=None status=COMPLETE desc=`2026-11-03_cycle03 H-peak-mz`

All recent public scores are **null**. Best scored public remains **0.143** (v0.1).

## Leaderboard context (CLIST, page said updated ~4 hours before this run)

Public top: **Shehab Alshehabi 0.54**, **Savko 0.53**, **Oleksandr Parfionov 0.52**, democat 0.51, pikachu / Paweł Biernat / CHU1PC / pain-in-the-mass 0.50. Community analog notebooks historically ~0.43–0.46. Gap vs our 0.143 is not a missing `TOP_PEAKS` or `PEAK_MZ_TOL` constant — those are already live.

## Why the score is low

1. **Poisoned exact duplicates (v0.1 failure).** Exact test↔train spectrum copies exist in `enveda-180` whose train InChIKey14 ≠ competition GT. Exact-dup exclusion is on; that prevents the 0.143 “perfect library match” trap from repeating, but it also removes the easy rank-1 hits.

2. **Admission gate is still 0.05.** `retrieve_for_spectrum` keeps every hybrid score `>= cfg.min_similarity` (`casmi26/retrieve.py`). Live `MIN_SIMILARITY=0.05` is far below Li/Fiehn’s FDR<10% entropy operating point (0.75) and below Scheubert/GNPS-style identification cutoffs (~0.7). After `PEAK_MZ_TOL=0.02` went live, *more* weak fragment pairs survive, so the top-25 is even more likely to be packed with mass-isobar decoys. MRR@25 only scores the first correct InChIKey14.

3. **Slot rotation has been a no-op for weeks.** Live main after Actions 11-06 cycle01: `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, mass-wide 35/80, `TOP_K=120`, **`MIN_SIMILARITY=0.05`**, `PEAK_MZ_TOL=0.02`. Replaying H-peak-mz (slot-2 fallback) does not change the spectrum object. Cloud H-min-sim / H-sim-gate PRs **#67–#77** specified 0.05→0.12 and stayed draft; Actions then spent the next UTC ticket on the fallback no-op.

## Concrete improvement for this slot

Implement **one** major ablation: `MIN_SIMILARITY` **0.05 → 0.12**.

Retarget Actions **slot-2** (next unused hourly; likely **08:00 UTC** if the 07:00 cron already missed) and **slot-3** (backup if this PR is late) from already-live H-peak-mz to **H-sim-gate**.

If this PR is **not** merged before that slot, Actions will spend UTC ticket 2 on `PEAK_MZ_TOL=0.02` — a second no-op today.

## Cloud submit attempt (this runner)

`write_kaggle_credentials()` returned **False**. `KAGGLE_USERNAME`, `KAGGLE_KEY`, and `KAGGLE_API_TOKEN` are unset; `~/.kaggle/kaggle.json` was not written. No `kernels push` / `competition_submit_code` from Cloud. Handoff is the substantial cycle02 docs + `config_patch: {"MIN_SIMILARITY": 0.12}` so casmi-loop slot 2 can reuse them after merge.
