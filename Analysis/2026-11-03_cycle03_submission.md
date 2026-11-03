# Analysis — 2026-11-03 cycle03

Competition day for this Cloud prompt starts **01:00 America/Chicago**. At trigger time **2026-11-03T09:02Z / 03:02 CST** Chicago day **2026-11-03 is open** (started 01:00 CST = 07:00 UTC). Kaggle’s enforced reset is midnight UTC (`scripts/casmi_loop/slots.py`). This run tags **2026-11-03_cycle03** so `casmi-loop` will reuse these substantial docs on the next unused UTC slot after merge.

## Quota (re-checked 09:04 UTC)

Cloud secrets `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN` are **absent**, so `write_kaggle_credentials()` returned **False** and `~/.kaggle/kaggle.json` was not written. `kaggle competitions submissions` is not callable. Count is from `agent/state.json` + GitHub Actions `casmi-loop` + public CLIST / prior Cloud notes.

| Clock | Used | Remaining | Rows counted |
|-------|------|-----------|--------------|
| UTC calendar 2026-11-03 | **2/5** | 3 | Actions 41555977510 → Kaggle **57927482** H-top-peaks kernel v187 ~01:06Z (`TOP_PEAKS=128`, already live). Actions 41598050009 → Kaggle **57939381** H-peak-mz kernel v188 ~08:00Z (`PEAK_MZ_TOL=0.02`, already live). |
| Chicago 01:00 2026-11-02 (closed 07:00 UTC) | **3/5** | — | 57900287 (07:45Z H-peak-mz); 57917568 (18:17Z H-peak-mz); 57927482 (01:06Z H-top-peaks). 57889756 at 00:50Z Nov 2 landed *before* 01:00 CST. |
| Chicago 01:00 2026-11-03 (open) | **1/5** | 4 | 57939381 at ~08:00Z / 02:00 CST. 57927482 at 01:06Z is *before* 07:00 UTC so it belongs to Chicago 2026-11-02. |
| Quota exhausted? | **No** | — | Do not exit; implement + hand off. |

Quota is **not** exhausted (5/5 not used on either clock). Next unused cycle on `main` for UTC 2026-11-03 is **cycle03**. Cloud PRs **#38–#63** already wrote H-min-sim but stayed draft. #63 missed the 08:00 UTC merge window, so Actions spent UTC ticket 2 on already-live `PEAK_MZ_TOL=0.02`. 01:00 / 02:00 / 03:00 / 04:00 / 05:00 / **09:00** UTC `casmi-loop` hours did not fire. Next unused casmi-loop hourly is **10:00 UTC**.

## Recent submissions (from committed Analysis + state)

- id=**57939381** score=None status=COMPLETE desc=`2026-11-03_cycle02 H-peak-mz` (`PEAK_MZ_TOL=0.02`, already live; kernel v188)
- id=**57927482** score=None status=COMPLETE desc=`2026-11-03_cycle01 H-top-peaks` (`TOP_PEAKS=128`, already live; kernel v187)
- id=**57917568** score=None status=COMPLETE desc=`2026-11-02_cycle03 H-peak-mz` (`PEAK_MZ_TOL=0.02`, already live; kernel v186)
- id=**57900287** score=None status=COMPLETE desc=`2026-11-02_cycle02 H-peak-mz` (`PEAK_MZ_TOL=0.02`, already live; kernel v185)
- id=**57889756** score=None status=COMPLETE desc=`2026-11-02_cycle01 H-top-peaks` (`TOP_PEAKS=128`, already live; kernel v184)
- id=**57884052** score=None status=COMPLETE desc=`2026-11-01_cycle04 H-peaks` (`TOP_PEAKS=160`, kernel v183)
- id=**57878253** score=None status=COMPLETE desc=`2026-11-01_cycle03 H-peak-mz` (`PEAK_MZ_TOL=0.02`, already live; kernel v182)
- id=**57867206** score=None status=COMPLETE desc=`2026-11-01_cycle02 H-peak-mz` (`PEAK_MZ_TOL=0.02`, already live; kernel v181)
- id=**57857604** score=None status=COMPLETE desc=`2026-11-01_cycle01 H-top-peaks` (`TOP_PEAKS=128`, already live; kernel v180)
- id=57852239 score=None status=COMPLETE desc=`2026-10-31_cycle05 H-domain`

No publicScore on any of our rows. Best scored public remains **0.143** (v0.1).

## Leaderboard (CLIST, re-fetched 09:04Z)

Savko **0.52**, Parfionov **0.52**, democat **0.51**, pikachu / Shehab / CHU1PC **0.50**. Community analog notebooks still badge **0.479**. Gap vs our 0.143 is analog + fingerprint + in-silico rerank, but the immediate no-op is that Actions will replay `PEAK_MZ_TOL=0.02` at 10:00 UTC unless fallbacks are retargeted and this spec is on `main`.

Kaggle’s native leaderboard page rate-limited (`Too many requests`); CLIST is the live public snapshot used here.

## Why score is low

1. **Exact test↔train spectrum duplicates** in `enveda-180` with train labels ≠ competition GT. `EXCLUDE_EXACT_DUPLICATES=True` already bans those inchikey14s. Remaining score is from non-identical evidence.

2. **Admission floor is 0.05.** `retrieve_for_spectrum` (`casmi26/retrieve.py`) keeps every hybrid entropy/modcos hit ≥ `cfg.min_similarity`. At 0.05, weak cross-library decoys fill `TOP_K_SPECTRA=120` and crowd the top-25. Literature identification floors are 0.55–0.75 (entropy), ~0.6 (MS2Query discard band), ~0.5 (GNPS cosine). 0.12 is the first unused one-knob step.

3. **Slot rotation is a no-op.** Live main after Actions 11-03 cycle02: `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, mass-wide 35/80, `MIN_SIMILARITY=0.05`, **`PEAK_MZ_TOL=0.02`**. Slot-3 fallback still applies `PEAK_MZ_TOL=0.02` (next unused UTC slot). Slot-4 `H-peaks` currently sets `MIN_SIMILARITY=0.05`, which would undo a merged floor raise.

## Concrete improvement for this slot

**`MIN_SIMILARITY` 0.05 → 0.12** (library-hit admission floor).

Retarget Actions **slot-2 and slot-3** fallbacks to **H-min-sim**, and **slot-4** to `TOP_PEAKS=160` **without** resetting the floor. Slot-2 already fired today as H-peak-mz; slot-3 is the next unused UTC ticket.

If this PR is **not** merged before **10:00 UTC**, the next unused `casmi-loop` hour will spend UTC ticket 3 on `PEAK_MZ_TOL=0.02` — another no-op.

`write_kaggle_credentials()` returned **False**. No `kernels push` / `competition_submit_code` from Cloud. Do **not** dispatch casmi-loop until merged.
