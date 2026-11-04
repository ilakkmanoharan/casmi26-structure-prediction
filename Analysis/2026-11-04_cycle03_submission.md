# Analysis — 2026-11-04 cycle03

## Quota (re-checked at 2026-11-04T09:19Z)

Competition day for this Cloud prompt starts **01:00 America/Chicago**. At trigger time **2026-11-04T09:04Z / 03:04 CST** Chicago day **2026-11-04 is open** (started 01:00 CST Nov 4 = 07:00 UTC). Kaggle’s enforced reset is midnight UTC (`scripts/casmi_loop/slots.py`). This run tags **2026-11-04_cycle03** so `casmi-loop` will reuse these substantial docs on the next unused UTC slot after merge.

Cloud runner has **no** `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN`, so the CLI list could not be refreshed here. Counts below come from `origin/main` `agent/state.json` after the 09:16Z Actions push (`80a9dcb`, Kaggle **57979390**) plus `gh run list`.

| Clock | Used | Remaining | Notes |
|-------|------|-----------|-------|
| UTC calendar 2026-11-04 | **2 / 5** | 3 | 57967804 (02:19Z, Actions 41757745330); 57979390 (09:16Z, Actions 41803698801) |
| Chicago 01:00 (2026-11-04 day, now open) | **1 / 5** | 4 | 57979390 is the first code submit after 07:00 UTC. 57967804 landed at 02:19Z (Chicago 11-03). |
| Quota exhausted? | **No** | — | Do not exit; implement + hand off |

02:00–08:00 UTC `casmi-loop` hours did **not** fire. 09:00 UTC **did** fire and spent UTC ticket 2 on already-live `PEAK_MZ_TOL=0.02`. Next unused hourly is **10:00 UTC**.

## Recent Kaggle submissions (newest first, from state.json)

- id=**57979390** score=None status=COMPLETE desc=`2026-11-04_cycle02 H-peak-mz` (`PEAK_MZ_TOL=0.02`, kernel **v192**, Actions 41803698801, 08:59Z)
- id=**57967804** score=None status=COMPLETE desc=`2026-11-04_cycle01 H-top-peaks` (`TOP_PEAKS=128`, kernel **v191**, Actions 41757745330, 01:59Z)
- id=**57961369** score=None status=COMPLETE desc=`2026-11-03_cycle04 H-peaks` (`TOP_PEAKS=160`, kernel **v190**, Actions 41723888498, 21:40Z)
- id=**57953771** score=None status=COMPLETE desc=`2026-11-03_cycle03 H-peak-mz` (`PEAK_MZ_TOL=0.02`, kernel **v189**, Actions 41669236923, 15:57Z)
- id=**57939381** score=None status=COMPLETE desc=`2026-11-03_cycle02 H-peak-mz` (`PEAK_MZ_TOL=0.02`, kernel **v188**, Actions 41598050009, 07:42Z)
- id=**57927482** score=None status=COMPLETE desc=`2026-11-03_cycle01 H-top-peaks` (`TOP_PEAKS=128`, kernel **v187**, Actions 41555977510, 00:52Z)
- id=57917568 score=None status=COMPLETE desc=`2026-11-02_cycle03 H-peak-mz`
- id=57900287 score=None status=COMPLETE desc=`2026-11-02_cycle02 H-peak-mz`
- id=57889756 score=None status=COMPLETE desc=`2026-11-02_cycle01 H-top-peaks`

All recent public scores are **null**. Best scored public remains **0.143** (v0.1).

## Leaderboard context (CLIST ~2026-11-04T09:08Z, page updated ~1h earlier)

Public top: **Shehab 0.54**, **Savko 0.52**, **Parfionov 0.52**, **democat 0.51**, **pikachu / CHU1PC 0.50**. Community analog notebooks still badge **0.479–0.481**. Gap vs our 0.143 is not a missing `TOP_PEAKS` or `PEAK_MZ_TOL` constant — those are already live (128 / 0.02). Shehab moved 0.53→0.54 since the 07:35Z Cloud cycle.

## Why the score is low

1. **Poisoned exact duplicates (v0.1 failure).** Exact test↔train spectrum copies exist in `enveda-180` whose train InChIKey14 ≠ competition GT. Exact-dup exclusion is on; that prevents the 0.143 “perfect library match” trap from repeating, but it also removes the easy rank-1 hits.

2. **Admission floor is still 0.05.** `retrieve_for_spectrum` keeps every library hit with `sim >= cfg.min_similarity` (`casmi26/retrieve.py`). Literature identification bands sit at entropy ≥0.55–0.75 (Li/Fiehn, de Jonge JASMS), GNPS cosine ≥0.5, MS2Query discard-below-0.6. A 0.05 hybrid floor packs `TOP_K_SPECTRA=120` and then the top-25 with weak decoys.

3. **Slot rotation is a no-op or a revert.** Live main after Actions 11-04 cycle02: `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, mass-wide 35/80, `MIN_SIMILARITY=0.05`, **`PEAK_MZ_TOL=0.02`**. Slot-3 fallback still applies `PEAK_MZ_TOL=0.02` (next unused UTC slot). Slot-4 `H-peaks` currently sets `MIN_SIMILARITY=0.05`, which would undo a merged floor raise. Cycle04’s `TOP_PEAKS=160` was a real ablation, then cycle01 immediately restored 128. Cycle02 replayed the already-live 0.02 Da window.

Cloud PRs **#38–#68** already wrote H-min-sim but stayed draft. #68 (07:35Z) asked for a merge before 08:00 UTC; that hourly did not fire, so 09:00 UTC spent ticket 2 on `PEAK_MZ_TOL=0.02`. The next unused hourly is 10:00 UTC.

## Concrete improvement for this slot

**`MIN_SIMILARITY` 0.05 → 0.12** (library-hit admission floor).

Retarget Actions **slot-2 and slot-3** fallbacks to **H-min-sim**, and **slot-4** to `TOP_PEAKS=160` **without** resetting the floor. Slot-3 is the next unused UTC ticket (~10:00 UTC).

If this PR is **not** merged before that hour, Actions will spend UTC ticket 3 on `PEAK_MZ_TOL=0.02` — another no-op.

## Cloud submit attempt (this runner)

`write_kaggle_credentials()` returned **False**. `KAGGLE_USERNAME`, `KAGGLE_KEY`, and `KAGGLE_API_TOKEN` are unset; `~/.kaggle/kaggle.json` was not written. No `kernels push` / `competition_submit_code` from Cloud. Handoff is the substantial cycle03 docs + `config_patch: {"MIN_SIMILARITY": 0.12}` so casmi-loop slot 3 can reuse them after merge.
