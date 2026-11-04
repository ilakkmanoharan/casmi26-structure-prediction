# Analysis — 2026-11-04 cycle02

## Quota (re-checked at 2026-11-04T07:36Z)

Competition day for this Cloud prompt starts **01:00 America/Chicago**. At trigger time **2026-11-04T07:35Z / 01:35 CST** Chicago day **2026-11-04 is open** (started 01:00 CST Nov 4 = 07:00 UTC). Kaggle’s enforced reset is midnight UTC (`scripts/casmi_loop/slots.py`). This run tags **2026-11-04_cycle02** so `casmi-loop` will reuse these substantial docs on the next unused UTC slot after merge.

Cloud runner has **no** `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN`, so the CLI list could not be refreshed here. Counts below come from `origin/main` `agent/state.json` after the 01:59Z Actions push (`b16656d`) plus `gh run list`.

| Clock | Used | Remaining | Notes |
|-------|------|-----------|-------|
| UTC calendar 2026-11-04 | **1 / 5** | 4 | 57967804 (02:19Z, Actions 41757745330) |
| Chicago 01:00 (2026-11-04 day, now open) | **0 / 5** | 5 | No code submits since 07:00 UTC. |
| Chicago 01:00 (2026-11-03 day, now closed) | **4 / 5** | — | 57939381 (08:00Z Nov 3), 57953771 (16:16Z), 57961369 (21:58Z), 57967804 (02:19Z Nov 4). |
| Quota exhausted? | **No** | — | Do not exit; implement + hand off |

02:00–07:00 UTC `casmi-loop` hours did **not** fire. Next unused hourly is **08:00 UTC**.

## Recent Kaggle submissions (newest first, from state.json)

- id=**57967804** score=None status=COMPLETE desc=`2026-11-04_cycle01 H-top-peaks` (`TOP_PEAKS=128`, kernel **v191**, Actions 41757745330, 01:59Z)
- id=**57961369** score=None status=COMPLETE desc=`2026-11-03_cycle04 H-peaks` (`TOP_PEAKS=160`, kernel **v190**, Actions 41723888498, 21:40Z)
- id=**57953771** score=None status=COMPLETE desc=`2026-11-03_cycle03 H-peak-mz` (`PEAK_MZ_TOL=0.02`, kernel **v189**, Actions 41669236923, 15:57Z)
- id=**57939381** score=None status=COMPLETE desc=`2026-11-03_cycle02 H-peak-mz` (`PEAK_MZ_TOL=0.02`, kernel **v188**, Actions 41598050009, 07:42Z)
- id=**57927482** score=None status=COMPLETE desc=`2026-11-03_cycle01 H-top-peaks` (`TOP_PEAKS=128`, kernel **v187**, Actions 41555977510, 00:52Z)
- id=57917568 score=None status=COMPLETE desc=`2026-11-02_cycle03 H-peak-mz`
- id=57900287 score=None status=COMPLETE desc=`2026-11-02_cycle02 H-peak-mz`
- id=57889756 score=None status=COMPLETE desc=`2026-11-02_cycle01 H-top-peaks`

All recent public scores are **null**. Best scored public remains **0.143** (v0.1).

## Leaderboard context (CLIST ~2026-11-04T07:36Z, page ~21h stale)

Public top: **Shehab 0.53**, **Savko 0.52**, **Parfionov 0.52**, **democat 0.51**, **pikachu / CHU1PC 0.50**. Community analog notebooks still badge **0.479–0.481**. Gap vs our 0.143 is not a missing `TOP_PEAKS` or `PEAK_MZ_TOL` constant — those are already live (128 / 0.02).

## Why the score is low

1. **Poisoned exact duplicates (v0.1 failure).** Exact test↔train spectrum copies exist in `enveda-180` whose train InChIKey14 ≠ competition GT. Exact-dup exclusion is on; that prevents the 0.143 “perfect library match” trap from repeating, but it also removes the easy rank-1 hits.

2. **Admission floor is still 0.05.** `retrieve_for_spectrum` keeps every library hit with `sim >= cfg.min_similarity` (`casmi26/retrieve.py`). Literature identification bands sit at entropy ≥0.55–0.75 (Li/Fiehn, de Jonge JASMS), GNPS cosine ≥0.5, MS2Query discard-below-0.6. A 0.05 hybrid floor packs `TOP_K_SPECTRA=120` and then the top-25 with weak decoys.

3. **Slot rotation is a no-op or a revert.** Live main after Actions 11-04 cycle01: `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, mass-wide 35/80, `MIN_SIMILARITY=0.05`, **`PEAK_MZ_TOL=0.02`**. Slot-2 fallback still applies `PEAK_MZ_TOL=0.02` (next unused UTC slot). Slot-4 `H-peaks` currently sets `MIN_SIMILARITY=0.05`, which would undo a merged floor raise. Cycle04’s `TOP_PEAKS=160` was a real ablation, then cycle01 immediately restored 128.

Cloud PRs **#38–#67** already wrote H-min-sim but stayed draft. #67 (06:00Z) asked for a merge before 07:00 UTC; that hourly did not fire, so the ticket was not wasted — yet. The next unused hourly is 08:00 UTC.

## Concrete improvement for this slot

**`MIN_SIMILARITY` 0.05 → 0.12** (library-hit admission floor).

Retarget Actions **slot-2 and slot-3** fallbacks to **H-min-sim**, and **slot-4** to `TOP_PEAKS=160` **without** resetting the floor. Slot-2 is the next unused UTC ticket (~08:00 UTC).

If this PR is **not** merged before that hour, Actions will spend UTC ticket 2 on `PEAK_MZ_TOL=0.02` — another no-op.

## Cloud submit attempt (this runner)

`write_kaggle_credentials()` returned **False**. `KAGGLE_USERNAME`, `KAGGLE_KEY`, and `KAGGLE_API_TOKEN` are unset; `~/.kaggle/kaggle.json` was not written. No `kernels push` / `competition_submit_code` from Cloud. Handoff is the substantial cycle02 docs + `config_patch: {"MIN_SIMILARITY": 0.12}` so casmi-loop slot 2 can reuse them after merge.
