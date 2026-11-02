# Analysis — 2026-11-02 cycle03

Competition day for this Cloud prompt starts **01:00 America/Chicago**. At trigger time **2026-11-02T07:32Z / 01:32 CST** Chicago day **2026-11-02** is open (01:00 CST = 07:00 UTC). Kaggle’s enforced reset is midnight UTC (`scripts/casmi_loop/slots.py`). This run tags **2026-11-02_cycle03** so it does not collide with Actions in-flight cycle02, and so `casmi-loop` will reuse these substantial docs on the next unused UTC slot after merge.

## Quota (re-checked 07:33 UTC)

Cloud secrets `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN` are **absent**, so `write_kaggle_credentials()` returned **False** and `~/.kaggle/kaggle.json` was not written. `kaggle competitions submissions` is not callable. Count is from `agent/state.json` + GitHub Actions `casmi-loop` + public CLIST.

| Clock | Used | Remaining | Rows counted |
|-------|------|-----------|--------------|
| UTC calendar 2026-11-02 | **1/5 complete, 1 in flight** | ≤3 | Complete: Actions → Kaggle **57889756** H-top-peaks kernel v184 ~00:50Z (`TOP_PEAKS=128`, already live). In flight: `casmi-loop` **41406414674** started 07:27Z on `3b6c562` (slot-2 fallback H-peak-mz, already live). |
| Chicago 01:00 2026-11-01 | **4/5** | closed | 57867206, 57878253, 57884052, 57889756. Day ended 07:00 UTC. |
| Chicago 01:00 2026-11-02 | **0 complete, 1 in flight** | ≤4 | Day opened 07:00 UTC. The 07:27Z Actions job is the first Chicago-day submit. |

Quota is **not** exhausted (5/5 not used on either clock). Do not exit; implement + hand off. Next unused cycle on `main` after the in-flight job records cycle02 is **cycle03**. Cloud PRs **#38–#59** already wrote H-min-sim but stayed draft. Next unused casmi-loop hourly after 41406414674 is **08:00 UTC**.

## Recent submissions (from committed Analysis + state)

- id=**57889756** score=None status=COMPLETE desc=`2026-11-02_cycle01 H-top-peaks` (`TOP_PEAKS=128`, already live; kernel v184)
- id=**57884052** score=None status=COMPLETE desc=`2026-11-01_cycle04 H-peaks` (`TOP_PEAKS=160`, kernel v183)
- id=**57878253** score=None status=COMPLETE desc=`2026-11-01_cycle03 H-peak-mz` (`PEAK_MZ_TOL=0.02`, already live; kernel v182)
- id=**57867206** score=None status=COMPLETE desc=`2026-11-01_cycle02 H-peak-mz` (`PEAK_MZ_TOL=0.02`, already live; kernel v181)
- id=**57857604** score=None status=COMPLETE desc=`2026-11-01_cycle01 H-top-peaks` (`TOP_PEAKS=128`, already live; kernel v180)
- id=57852239 score=None status=COMPLETE desc=`2026-10-31_cycle05 H-domain`
- id=57847630 score=None status=COMPLETE desc=`2026-10-31_cycle04 H-peaks`
- id=57840318 score=None status=COMPLETE desc=`2026-10-31_cycle03 H-peak-mz`
- id=57830376 score=None status=COMPLETE desc=`2026-10-31_cycle02 H-peak-mz`
- id=57821778 score=None status=COMPLETE desc=`2026-10-31_cycle01 H-top-peaks`

No scored public row above **0.143**. Kernel versions keep incrementing; public MRR does not.

## Leaderboard context (CLIST, re-fetched 07:35Z)

Savko **0.52**, Parfionov **0.52**, democat **0.51**, pikachu / Shehab / CHU1PC **0.50**. Community analog notebooks still badge **0.479**. Gap vs our 0.143 is analog + fingerprint + in-silico rerank, but the immediate no-op is that Actions is replaying `PEAK_MZ_TOL=0.02` right now and will replay it again at 08:00 UTC unless fallbacks are retargeted and this spec is on `main`.

Kaggle’s native leaderboard page rate-limited (`Too many requests`); CLIST is the live public snapshot used here.

## Why score is low

1. **Exact test↔train spectrum duplicates** in `enveda-180` with train labels ≠ competition GT. `EXCLUDE_EXACT_DUPLICATES=True` already bans those inchikey14s. Remaining score is from non-identical evidence.

2. **Admission floor is 0.05.** `retrieve_for_spectrum` (`casmi26/retrieve.py`) keeps every hybrid entropy/modcos hit ≥ `cfg.min_similarity`. At 0.05, weak cross-library decoys fill `TOP_K_SPECTRA=120` and crowd the top-25. Literature identification floors are 0.55–0.75 (entropy), ~0.6 (MS2Query discard band), ~0.5 (GNPS cosine). 0.12 is the first unused one-knob step.

3. **Slot rotation is a no-op.** Live main after Actions 11-02 cycle01: `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, mass-wide 35/80, `MIN_SIMILARITY=0.05`, **`PEAK_MZ_TOL=0.02`**. Slot-2 and slot-3 fallbacks still apply `PEAK_MZ_TOL=0.02`. The 07:27Z Actions job is spending UTC ticket 2 on that already-live knob. Slot-4 `H-peaks` currently sets `MIN_SIMILARITY=0.05`, which would undo a merged floor raise.

## Concrete improvement for this slot

**`MIN_SIMILARITY` 0.05 → 0.12** (library-hit admission floor).

Retarget Actions **slot-2 and slot-3** fallbacks to **H-min-sim**, and **slot-4** to `TOP_PEAKS=160` **without** resetting the floor.

If this PR is **not** merged before **08:00 UTC**, the next unused `casmi-loop` hour will spend UTC ticket 3 on `PEAK_MZ_TOL=0.02` — another no-op.

`write_kaggle_credentials()` returned **False**. No `kernels push` / `competition_submit_code` from Cloud. Do **not** dispatch casmi-loop until merged (and not while 41406414674 is running).
