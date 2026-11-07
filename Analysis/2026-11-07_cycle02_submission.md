# Analysis — 2026-11-07 cycle02

## Quota (re-checked at 2026-11-07T07:35Z)

Competition day for this Cloud prompt starts **01:00 America/Chicago** (07:00 UTC in CST). Kaggle’s enforced reset is midnight UTC (`scripts/casmi_loop/slots.py`).

Cloud runner has **no** `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN` (confirmed empty; `~/.kaggle/` exists but has no `kaggle.json`). The CLI list could not be refreshed here. Counts below come from Actions run **42330089426** logs + `origin/main` `agent/state.json` after the 02:53Z push (`dc15868`) plus the failed 2026-11-06 slot-4 run **42307757034** (submit succeeded, GitHub push 500).

| Clock | Used | Remaining | Notes |
|-------|------|-----------|-------|
| UTC calendar 2026-11-07 | **1 / 5** | 4 | 58076904 (02:53Z, kernel v202, H-top-peaks) |
| Chicago 01:00 (since 07:00 UTC) | **0 / 5** | 5 | The UTC ticket landed *before* 01:00 CST |
| Quota exhausted? | **No** | — | Do not exit; implement + hand off |

`write_kaggle_credentials()` would return **False** here. Do not CSV-submit. Direct `kernels push` / `competition_submit_code` is impossible from this runner.

## Recent Kaggle submissions (newest first, from Actions logs)

- id=**58076904** score=None status=PENDING→submitted desc=`2026-11-07_cycle01 H-top-peaks` kernel **v202** (Actions 42330089426, 02:53Z). Config patch `{TOP_PEAKS: 128}` — already live; no-op vs main.
- id=**58071327** score=None status=PENDING desc=`2026-11-06_cycle04 H-peaks` kernel **v201** (Actions 42307757034, ~23:09Z). Applied `{TOP_PEAKS: 160, MIN_SIMILARITY: 0.05}` but **GitHub push failed** (`remote: Internal Server Error`), so origin/main never got 160. Cycle01 today reset the kernel to 128.
- id=**58065731** score=None status=COMPLETE desc=`2026-11-06_cycle03 H-peak-mz` kernel **v200**
- id=**58055178** score=None status=COMPLETE desc=`2026-11-06_cycle02 H-peak-mz` kernel **v199**
- id=**58042294** score=None status=COMPLETE desc=`2026-11-06_cycle01 H-top-peaks` kernel **v198**

All recent public scores are **null**. Best scored public remains **0.143** (v0.1).

## Leaderboard context (CLIST, updated ~5 hours before this cycle)

Public top: **Shehab Alshehabi 0.54**, **Savko 0.53**, **Oleksandr Parfionov 0.52**, **democat 0.51**, **pikachu / Paweł Biernat / CHU1PC 0.50**. Gap vs our 0.143 is not a missing `TOP_PEAKS` or `PEAK_MZ_TOL` constant — those are already live.

## Why the score is low

1. **Poisoned exact duplicates (v0.1 failure).** Exact test↔train spectrum copies exist in `enveda-180` whose train InChIKey14 ≠ competition GT. Exact-dup exclusion is on; that prevents the 0.143 “perfect library match” trap from repeating, but it also removes the easy rank-1 hits.

2. **Primary mass window is still 35 ppm.** `retrieve_for_spectrum` uses `index.mass_window(neutral_mass, cfg.mass_tol_ppm)`. Live `MASS_TOL_PPM=35` is more than 2× the ibnmarzuk 15 ppm precursor gate and ~4× shiferaxa’s 8.5 ppm structure pool. Off-formula library neighbors consume `TOP_K_SPECTRA_PER_QUERY=120` and crowd the top-25 after aggregation. Backfill at 80 ppm is the right *fallback*, not the primary gate.

3. **Slot rotation has been a no-op for weeks.** Live main after Actions 11-07 cycle01: `TOP_PEAKS=128`, `PEAK_MZ_TOL=0.02`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, **`MASS_TOL_PPM=35`**. Replaying H-peak-mz (slot-2/slot-3 fallbacks) does not change the candidate pool.

## Concrete improvement for this slot

Implement **one** major ablation: `MASS_TOL_PPM` **35 → 15**. Hold `MASS_TOL_PPM_BACKFILL=80` so empty lists still fill.

Retarget Actions **slot-2** (next unused hourly on UTC 2026-11-07) and **slot-3** from already-live H-peak-mz to **H-mass-tight**.

If this PR is **not** merged before that slot, Actions will spend UTC ticket 2 on `PEAK_MZ_TOL=0.02` — a second no-op today.

## Cloud submit attempt (this runner)

`KAGGLE_USERNAME`, `KAGGLE_KEY`, and `KAGGLE_API_TOKEN` are unset; `~/.kaggle/kaggle.json` was not written. No `kernels push` / `competition_submit_code` from Cloud. Handoff is the substantial cycle02 docs + `config_patch: {"MASS_TOL_PPM": 15.0}` so casmi-loop slot 2 can reuse them after merge.
