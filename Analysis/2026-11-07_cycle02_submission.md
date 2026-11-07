# Analysis — 2026-11-07 cycle02

## Quota (re-checked at 2026-11-07T09:04Z)

Competition day for this Cloud prompt starts **01:00 America/Chicago** (07:00 UTC in CST). Kaggle’s enforced reset is midnight UTC (`scripts/casmi_loop/slots.py`).

Cloud runner has **no** `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN` (confirmed empty via `printenv`; `~/.kaggle/` exists, mode 0700, but has **no** `kaggle.json`). `write_kaggle_credentials()` returns **False**. The CLI list could not be refreshed here. Counts below come from Actions run **42330089426** + `origin/main` `agent/state.json` after the 02:53Z push (`dc15868`) plus the failed 2026-11-06 slot-4 run **42307757034** (submit succeeded, GitHub push 500) and open Cloud drafts #82 / #83.

| Clock | Used | Remaining | Notes |
|-------|------|-----------|-------|
| UTC calendar 2026-11-07 | **1 / 5** | 4 | 58076904 (02:53Z, kernel v202, H-top-peaks) |
| Chicago 01:00 (since 07:00 UTC) | **0 / 5** | 5 | The UTC ticket landed *before* 01:00 CST. No casmi-loop run after 02:36Z. |
| Quota exhausted? | **No** | — | Do not exit; implement + hand off |

Do not CSV-submit. Direct `kernels push` / `competition_submit_code` is impossible from this runner until Cursor Cloud actually injects the Kaggle secrets.

Hourly `casmi-loop` last **success** was Actions **42330089426** at 02:36Z. No 07:00 / 08:00 / 09:00 UTC hourly jobs appear in `gh run list`. Ticket 2 is still unused.

## Recent Kaggle submissions (newest first, from Actions logs + state.json)

- id=**58076904** score=None status=COMPLETE desc=`2026-11-07_cycle01 H-top-peaks` kernel **v202** (Actions 42330089426, 02:53Z). Config patch `{TOP_PEAKS: 128}` — already live; no-op vs main.
- id=**58071327** score=None status=COMPLETE desc=`2026-11-06_cycle04 H-peaks` kernel **v201** (Actions 42307757034, ~23:09Z). Applied `{TOP_PEAKS: 160, MIN_SIMILARITY: 0.05}` but **GitHub push failed**, so origin/main never got 160. Cycle01 today reset the kernel to 128.
- id=**58065731** score=None status=COMPLETE desc=`2026-11-06_cycle03 H-peak-mz` kernel **v200**
- id=**58055178** score=None status=COMPLETE desc=`2026-11-06_cycle02 H-peak-mz` kernel **v199**
- id=**58042294** score=None status=COMPLETE desc=`2026-11-06_cycle01 H-top-peaks` kernel **v198**
- id=**58035989** score=None status=COMPLETE desc=`2026-11-05_cycle03 H-peak-mz` kernel **v197**
- id=**58026170** score=None status=COMPLETE desc=`2026-11-05_cycle02 H-peak-mz` kernel **v196**
- id=**58012064** score=None status=COMPLETE desc=`2026-11-05_cycle01 H-top-peaks` kernel **v195**

All recent public scores are **null**. Best scored public remains **0.143** (v0.1).

## Leaderboard context (CLIST, updated ~5 hours before this cycle)

Public top: **Shehab Alshehabi 0.54**, **Savko 0.53**, **Oleksandr Parfionov 0.52**, **democat 0.51**, **pikachu / Paweł Biernat / pain in the mass / CHU1PC 0.50**. Native Kaggle leaderboard page 429’d this runner. Gap vs our 0.143 is not a missing `TOP_PEAKS` or `PEAK_MZ_TOL` constant — those are already live.

## Why the score is low

1. **Poisoned exact duplicates (v0.1 failure).** Exact test↔train spectrum copies exist in `enveda-180` whose train InChIKey14 ≠ competition GT. Exact-dup exclusion is on; that prevents the 0.143 “perfect library match” trap from repeating, but it also removes the easy rank-1 hits.

2. **Identity search still mixes analogue-oriented cosine.** `hybrid_similarity` returns `0.75·entropy + 0.25·modified_cosine`. Li 2021 showed entropy already beats cosine (and 41 other metrics) for identity library search; Flash Entropy identity search scores with entropy only. The 0.25 cosine term can promote CE-shifted / intense-ion decoys into the top-25 after exact-dup exclusion, crowding true near-matches. `ENTROPY_WEIGHT=0.75` is a mix weight, **not** the Li/Fiehn FDR threshold of 0.75.

3. **Slot rotation has been a no-op for weeks.** Live main after Actions 11-07 cycle01: `TOP_PEAKS=128`, `PEAK_MZ_TOL=0.02`, **`ENTROPY_WEIGHT=0.75`**, `INTENSITY_FLOOR=0.01`, `MASS_TOL_PPM=35`, `MIN_SIMILARITY=0.05`. Replaying H-peak-mz (slot-2/slot-3 fallbacks) does not change the similarity object.

4. **Unmerged Cloud drafts do not spend Kaggle tickets.** PR **#82** (H-sim-gate, 06:04Z) and PR **#83** (H-mass-tight, 07:34Z) stay draft. Actions will not see their `config_patch` until merge. This cycle therefore implements a *third* unused lever (`ENTROPY_WEIGHT=1.0`) and retargets slot-2 so the next hourly cannot no-op.

## Concrete improvement for this slot

Implement **one** major ablation: `ENTROPY_WEIGHT` **0.75 → 1.0**. Hold `PEAK_MZ_TOL=0.02`, `TOP_PEAKS=128`, `MIN_SIMILARITY=0.05`, mass 35/80.

Retarget Actions **slot-2** (next unused hourly on UTC 2026-11-07) to this patch, **slot-3** to H-sim-gate (`MIN_SIMILARITY=0.12`), **slot-4** to H-mass-tight (`MASS_TOL_PPM=15.0`) so remaining tickets are real ablations.

If this PR is **not** merged before the next unused hourly, Actions will spend UTC ticket 2 on `PEAK_MZ_TOL=0.02` — a second no-op today.

## Cloud submit attempt (this runner)

`KAGGLE_USERNAME`, `KAGGLE_KEY`, and `KAGGLE_API_TOKEN` are unset; `~/.kaggle/kaggle.json` was not written. No `kernels push` / `competition_submit_code` from Cloud. Handoff is the substantial cycle02 docs + parseable `config_patch: {"ENTROPY_WEIGHT": 1.0}` so casmi-loop slot 2 can reuse them after merge.
