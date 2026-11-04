# Analysis — 2026-11-04 cycle03

## Quota (re-checked at 2026-11-04T10:33Z)

Competition day for this Cloud prompt starts **01:00 America/Chicago** (07:00 UTC after DST fallback). Kaggle’s enforced reset is midnight UTC (`scripts/casmi_loop/slots.py`).

Cloud runner has **no** `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN`, so the CLI list could not be refreshed here. Counts below come from `gh run list` + `origin/main` `agent/state.json` after the 09:16Z push (`80a9dcb`).

| Clock | Used | Remaining | Notes |
|-------|------|-----------|-------|
| UTC calendar 2026-11-04 | **2 / 5** | 3 | 57967804 (~02:19Z), 57979390 (~09:16Z) |
| Chicago 01:00 (since 07:00 UTC) | **1 / 5** | 4 | 57967804 landed *before* 01:00 CST; 57979390 is on Chicago day |
| Quota exhausted? | **No** | — | Do not exit; implement + hand off |

02:00–08:00 UTC and **10:00 UTC** casmi-loop hours did **not** fire. 09:00 UTC spent UTC ticket 2 on already-live `PEAK_MZ_TOL=0.02`.

## Recent Kaggle submissions (newest first, from Actions log / state.json)

- id=**57979390** score=None status=COMPLETE desc=`2026-11-04_cycle02 H-peak-mz` kernel **v192** (Actions 41803698801, ~09:16Z)
- id=**57967804** score=None status=COMPLETE desc=`2026-11-04_cycle01 H-top-peaks` kernel **v191** (Actions 41757745330, ~02:19Z)
- id=57961369 score=None status=COMPLETE desc=`2026-11-03_cycle04 H-peaks` (`TOP_PEAKS=160`; later undone)
- id=57953771 score=None status=COMPLETE desc=`2026-11-03_cycle03 H-peak-mz`
- id=57939381 score=None status=COMPLETE desc=`2026-11-03_cycle02 H-peak-mz`
- id=57927482 score=None status=COMPLETE desc=`2026-11-03_cycle01 H-top-peaks`

All recent public scores are **null**. Best scored public remains **0.143** (v0.1).

## Leaderboard context (CLIST ~2026-11-04T10:34Z, page ~2h stale)

Public top: **Shehab 0.54**, Savko **0.52**, Parfionov **0.52**, democat **0.51**, pikachu / CHU1PC **0.50**. Community analog notebooks still badge **0.479–0.481**. Gap vs our 0.143 is not a missing `TOP_PEAKS` or `PEAK_MZ_TOL` constant — those are already live.

## Why the score is low

1. **Poisoned exact duplicates (v0.1 failure).** Exact test↔train spectrum copies exist in `enveda-180` whose train InChIKey14 ≠ competition GT. Exact-dup exclusion is on; that prevents the 0.143 “perfect library match” trap from repeating, but it also removes the easy rank-1 hits.

2. **Admission floor is still 0.05.** `retrieve_for_spectrum` keeps any hybrid entropy/modcos score ≥ `cfg.min_similarity` (`casmi26/retrieve.py`). Live `MIN_SIMILARITY=0.05` is far below Li/Fiehn identification (~0.75), JASMS entropy (~0.55), GNPS cosine (0.5 / 0.7), and MS2Query’s “discard below 0.6” band. Weak decoys fill `TOP_K_SPECTRA=120` and then the top-25.

3. **Slot rotation has been a no-op for weeks.** Live main after Actions 11-04 cycle02: `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, mass-wide 35/80, `PEAK_MZ_TOL=0.02`, **`MIN_SIMILARITY=0.05`**. Replaying H-peak-mz (slot-3 fallback) does not change the spectrum object.

## Concrete improvement for this slot

Implement **one** major ablation: `MIN_SIMILARITY` **0.05 → 0.12**.

Retarget Actions **slot-2 and slot-3** fallbacks to **H-min-sim**. Retarget **slot-4** to H-peaks with `{TOP_PEAKS: 160}` only (do not reset the floor).

If this PR is **not** merged before the next unused hourly (**11:00 UTC**), Actions will spend UTC ticket 3 on `PEAK_MZ_TOL=0.02` — a third no-op today.

## Cloud submit attempt (this runner)

`write_kaggle_credentials()` returned **False**. `KAGGLE_USERNAME`, `KAGGLE_KEY`, and `KAGGLE_API_TOKEN` are unset; `~/.kaggle/kaggle.json` was not written. No `kernels push` / `competition_submit_code` from Cloud. Did **not** dispatch casmi-loop (would waste UTC ticket 3 on already-live `PEAK_MZ_TOL=0.02`). Handoff is the substantial cycle03 docs + `config_patch: {"MIN_SIMILARITY": 0.12}` so casmi-loop slot 3 can reuse them after merge.
