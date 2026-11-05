# Analysis — 2026-11-05 cycle02

## Quota (re-checked at 2026-11-05T06:10Z)

Competition day for this Cloud prompt starts **01:00 America/Chicago**. At trigger time Chicago was **00:03 CST** (still 2026-11-04 until 07:00 UTC). Kaggle’s enforced reset is midnight UTC (`scripts/casmi_loop/slots.py`).

Cloud runner has **no** `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN`, so `~/.kaggle/kaggle.json` was **not** written and the CLI list could not be refreshed here. Counts below come from `origin/main` after Actions run **41976074079** (`8c9adc0`, finished 06:06Z).

| Clock | Used | Remaining | Notes |
|-------|------|-----------|-------|
| UTC calendar 2026-11-05 | **1 / 5** | 4 | Hourly `casmi-loop` **41976074079** submitted **58012064** (`2026-11-05_cycle01 H-top-peaks`, kernel **v195**) |
| Chicago 01:00 (since 07:00 UTC Nov 4 / until 07:00 UTC Nov 5) | **5 / 5** | 0 on the stale Chicago day | 57967804–58001652 plus 58012064 (UTC cycle01 landed at 06:06Z, still before 01:00 CST) |
| Chicago day 2026-11-05 (starts 07:00 UTC) | **0 / 5** | 5 | Next hourly ~07:00Z is UTC slot 2 / first Chicago-Nov-5 ticket |
| Quota exhausted? | **No** (UTC) | — | Do not exit; implement + hand off cycle02 so the next hourly does not replay PEAK_MZ_TOL=0.02 |

## Recent Kaggle submissions (newest first, from Actions log + committed state)

- id=**58012064** score=None status=PENDING (at submit) desc=`2026-11-05_cycle01 H-top-peaks` kernel **v195** (Actions 41976074079, 06:06Z)
- id=**58001652** score=None status=COMPLETE desc=`2026-11-04_cycle04 H-peaks` kernel **v194** (Actions, 23:36Z)
- id=**57992996** score=None status=COMPLETE desc=`2026-11-04_cycle03 H-peak-mz` kernel **v193**
- id=**57979390** score=None status=COMPLETE desc=`2026-11-04_cycle02 H-peak-mz` kernel **v192**
- id=**57967804** score=None status=COMPLETE desc=`2026-11-04_cycle01 H-top-peaks` kernel **v191**
- id=57961369 score=None status=COMPLETE desc=`2026-11-03_cycle04 H-peaks`
- id=57953771 score=None status=COMPLETE desc=`2026-11-03_cycle03 H-peak-mz`
- id=57939381 score=None status=COMPLETE desc=`2026-11-03_cycle02 H-peak-mz`
- id=57927482 score=None status=COMPLETE desc=`2026-11-03_cycle01 H-top-peaks`

All recent public scores are **null**. Best scored public remains **0.143** (v0.1).

## Leaderboard context (CLIST ~17 h stale at 2026-11-05T06:10Z)

Public top: **Shehab Alshehabi 0.54**, **Savko 0.52**, **Oleksandr Parfionov 0.52**, democat 0.51, pikachu / CHU1PC 0.50. Many mid-board scores cluster at 0.48–0.49. Gap vs our 0.143 is not a missing `TOP_PEAKS` or `PEAK_MZ_TOL` constant — those are already live.

## Why the score is low

1. **Poisoned exact duplicates (v0.1 failure).** Exact test↔train spectrum copies exist in `enveda-180` whose train InChIKey14 ≠ competition GT. Exact-dup exclusion is on; that prevents the 0.143 “perfect library match” trap from repeating, but it also removes the easy rank-1 hits.

2. **Admission floor is still 0.05.** `retrieve_for_spectrum` keeps every hybrid entropy/modcos hit with `sim >= MIN_SIMILARITY`. After Flash Entropy pairing (20 mDa) and a 160-peak ladder, lots of weak decoys clear 0.05 and occupy the per-spectrum 25 and then the molecule 25. Li/Fiehn FDR < 10% needs entropy ≥ 0.75; 0.05 is noise.

3. **Slot rotation has been a no-op for weeks.** Live main after Actions 11-05 cycle01: `TOP_PEAKS=128`, `PEAK_MZ_TOL=0.02`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, mass-wide 35/80, `TOP_K=120`, **`MIN_SIMILARITY=0.05`**. Replaying H-peak-mz (slot-2/3 fallback) does not change who enters the list. Cycle01 only rolled `TOP_PEAKS` 160→128; the admission floor is unchanged.

## Concrete improvement for this slot

Implement **one** major ablation: `MIN_SIMILARITY` **0.05 → 0.12**.

Retarget Actions **slot-2** and **slot-3** fallbacks from already-live H-peak-mz to **H-min-sim**. The in-progress hourly is UTC slot 1 (H-top-peaks). The next unused hourly is **slot 2**.

If this PR is **not** merged before that slot, Actions will spend UTC ticket 2 on `PEAK_MZ_TOL=0.02` — another no-op today.

## Cloud submit attempt (this runner)

`write_kaggle_credentials()` returned **False**. `KAGGLE_USERNAME`, `KAGGLE_KEY`, and `KAGGLE_API_TOKEN` are unset; `~/.kaggle/kaggle.json` was not written. No `kernels push` / `competition_submit_code` from Cloud. Handoff is the substantial cycle02 docs + `config_patch: {"MIN_SIMILARITY": 0.12}` so casmi-loop slot 2 can reuse them after merge.
