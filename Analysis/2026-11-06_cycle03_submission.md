# Analysis — 2026-11-06 cycle03

## Quota (re-checked at 2026-11-06T12:01Z)

Competition day for this Cloud prompt starts **01:00 America/Chicago** (07:00 UTC on CST). Kaggle’s enforced reset is midnight UTC (`scripts/casmi_loop/slots.py`).

Cloud runner has **no** `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN`, so the CLI list could not be refreshed here. Counts below come from Actions run **42203446292** logs + `origin/main` `agent/state.json` after the 10:50Z push (`6d8a83b`). `write_kaggle_credentials()` returned **False**; `~/.kaggle/` is empty.

| Clock | Used | Remaining | Notes |
|-------|------|-----------|-------|
| UTC calendar 2026-11-06 | **2 / 5** | 3 | 58042294 (02:22Z), 58055178 (10:50Z) |
| Chicago 01:00 (since 07:00 UTC) | **1 / 5** | 4 | Cycle01 landed *before* 01:00 CST (02:22Z = 20:22 CST Nov 5) |
| Quota exhausted? | **No** | — | Do not exit; implement + hand off |

## Recent Kaggle submissions (newest first, from Actions log)

- id=**58055178** score=None status=PENDING (at submit) desc=`2026-11-06_cycle02 H-peak-mz` kernel **v199** (Actions 42203446292, 10:50Z)
- id=**58042294** score=None status=COMPLETE desc=`2026-11-06_cycle01 H-top-peaks` kernel **v198** (Actions 42147867834, 02:22Z)
- id=58035989 score=None status=COMPLETE desc=`2026-11-05_cycle03 H-peak-mz`
- id=58026170 score=None status=COMPLETE desc=`2026-11-05_cycle02 H-peak-mz`
- id=58012064 score=None status=COMPLETE desc=`2026-11-05_cycle01 H-top-peaks`
- id=58001652 score=None status=COMPLETE desc=`2026-11-04_cycle04 H-peaks`
- id=57992996 score=None status=COMPLETE desc=`2026-11-04_cycle03 H-peak-mz`
- id=57979390 score=None status=COMPLETE desc=`2026-11-04_cycle02 H-peak-mz`
- id=57967804 score=None status=COMPLETE desc=`2026-11-04_cycle01 H-top-peaks`
- id=57961369 score=None status=COMPLETE desc=`2026-11-03_cycle04 H-peaks`

All recent public scores are **null**. Best scored public remains **0.143** (v0.1).

## Leaderboard context (CLIST ~2026-11-06T12:05Z, ~8 h stale)

Public top: **Shehab Alshehabi 0.54**, **Savko 0.53**, **Oleksandr Parfionov 0.52**, **democat 0.51**, then pikachu / Paweł Biernat / pain in the mass / CHU1PC at **0.50**. Community analog notebooks still ~0.43–0.46. Gap vs our 0.143 is not a missing `TOP_PEAKS` or `PEAK_MZ_TOL` constant — those just replayed live values today.

## Why the score is low

1. **Poisoned exact duplicates (v0.1 failure).** Exact test↔train spectrum copies exist in `enveda-180` whose train InChIKey14 ≠ competition GT. Exact-dup exclusion is on; that prevents the 0.143 “perfect library match” trap from repeating, but it also removes the easy rank-1 hits.

2. **The hybrid admission floor is still 0.05.** After Flash Entropy 20 mDa pairing, 1% noise cut, and 0.75 entropy mix are live, `retrieve_for_spectrum` still keeps every mass-window hit with `sim >= 0.05`. Random isobars with two shared ions fill `TOP_K_SPECTRA=120` and then the MRR@25 list. Li/Fiehn treat scores this low as decoys (FDR < 10% only near 0.75).

3. **Slot rotation has been a no-op for weeks.** Live main after Actions 11-06 cycle02: `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, mass-wide 35/80, `TOP_K=120`, `PEAK_MZ_TOL=0.02`, **`MIN_SIMILARITY=0.05`**. Replaying H-peak-mz (slot-3 fallback) does not change the spectrum object.

## Concrete improvement for this slot

Implement **one** major ablation: `MIN_SIMILARITY` **0.05 → 0.12**.

Retarget Actions **slot-2** (already burned today; protects future UTC days) and **slot-3** (next unused hourly) from already-live H-peak-mz to **H-sim-gate**.

If this PR is **not** merged before that slot, Actions will spend UTC ticket 3 on `PEAK_MZ_TOL=0.02` — a third no-op today. Hourly casmi-loop 11:00 UTC did not fire; next likely unused hourly is **~13:00 UTC** (historical cadence after 10:32Z is sparse).

## Cloud submit attempt (this runner)

`write_kaggle_credentials()` returned **False**. `KAGGLE_USERNAME`, `KAGGLE_KEY`, and `KAGGLE_API_TOKEN` are unset; `~/.kaggle/kaggle.json` was not written. No `kernels push` / `competition_submit_code` from Cloud. Handoff is the substantial cycle03 docs + `config_patch: {"MIN_SIMILARITY": 0.12}` so casmi-loop slot 3 can reuse them after merge.
