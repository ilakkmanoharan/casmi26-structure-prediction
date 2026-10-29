# Analysis — 2026-10-29 cycle03

## Quota (re-checked at 2026-10-29T12:04Z)

Competition day for this Cloud prompt starts **01:00 America/Chicago** (06:00 UTC CDT). Kaggle’s enforced reset is midnight UTC (`scripts/casmi_loop/slots.py`). This run is the **07:00 CDT / 12:04 UTC** slot (last suggested Cloud cadence).

Cloud runner has **no** `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN`, so `write_kaggle_credentials()` returned False, `~/.kaggle/kaggle.json` was **not** written, and `kaggle competitions submissions` could not be refreshed here. Counts below come from Actions runs **40805625766** / **40850896999** + `origin/main` `agent/state.json` after the 09:53Z push (`2f9d4bc`).

| Clock | Used | Remaining | Notes |
|-------|------|-----------|-------|
| UTC calendar 2026-10-29 | **2 / 5** | 3 | 57756058 (~02:33Z), 57767052 (~09:53Z) |
| Chicago 01:00 (since 06:00 UTC) | **1 / 5** | 4 | 57756058 landed *before* 01:00 CDT (21:33 CDT Oct 28); 57767052 is on this Chicago day |
| Quota exhausted? | **No** | — | Do not exit; implement + hand off |

No `casmi-loop` run is in progress. Last success: **40850896999** at 09:35Z. Later hourly crons (10:00 / 11:00 / 12:00 UTC) have not appeared yet (GitHub schedule delay on this public repo).

## Recent Kaggle submissions (newest first, from Actions log + state.json)

- id=**57767052** score=None status=COMPLETE desc=`2026-10-29_cycle02 H-peak-mz` kernel **v168** (Actions 40850896999, ~09:53Z)
- id=**57756058** score=None status=COMPLETE desc=`2026-10-29_cycle01 H-top-peaks` kernel **v167** (Actions 40805625766, ~02:33Z)
- id=57750957 score=None status=COMPLETE desc=`2026-10-28_cycle04 H-peaks`
- id=57745595 score=None status=COMPLETE desc=`2026-10-28_cycle03 H-peak-mz`
- id=57735008 score=None status=COMPLETE desc=`2026-10-28_cycle02 H-peak-mz`
- id=57724850 score=None status=COMPLETE desc=`2026-10-28_cycle01 H-top-peaks`
- id=57716036 score=None status=COMPLETE desc=`2026-10-27_cycle05 H-domain`
- id=57712244 score=None status=COMPLETE desc=`2026-10-27_cycle04 H-peaks`
- id=57704012 score=None status=COMPLETE desc=`2026-10-27_cycle03 H-peak-mz`
- id=57693774 score=None status=COMPLETE desc=`2026-10-27_cycle02 H-peak-mz`

All recent public scores are **null**. Best scored public remains **0.143** (v0.1).

## Leaderboard context (CLIST fetched 2026-10-29T12:04Z; page “updated 13 hours ago”)

Public top: **Oleksandr Parfionov 0.52**, **Savko 0.51**, **pikachu / Shehab Alshehabi / CHU1PC 0.50**, then a long 0.48–0.49 band. Community analog notebooks still ~0.43–0.46; copied-notebook pile ~0.464. Gap vs our 0.143 is not a missing `TOP_PEAKS` or `PEAK_MZ_TOL` constant — those are already live.

## Why the score is low

1. **Poisoned exact duplicates (v0.1 failure).** Exact test↔train spectrum copies exist in `enveda-180` whose train InChIKey14 ≠ competition GT. Exact-dup exclusion is on; that prevents the 0.143 “perfect library match” trap from repeating, but it also removes the easy rank-1 hits.

2. **Weak library hits pad the top-25.** `retrieve.py` keeps every hybrid score `>= cfg.min_similarity` before truncating to `TOP_K_SPECTRA_PER_QUERY=120`. Live `MIN_SIMILARITY=0.05` is far below GNPS library-search (0.5) / MASST (0.7) admission defaults and far below Li/Fiehn’s 0.75 *call* threshold. Decoys occupy rank-list slots that MRR@25 then treats as plausible.

3. **Slot rotation has been a no-op for weeks, and it just happened again.** Live main after Actions 10-29 cycle02: `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, mass-wide 35/80, `TOP_K=120`, `PEAK_MZ_TOL=0.02`, **`MIN_SIMILARITY=0.05`**. Replaying H-peak-mz (slot-3 fallback, identical to slot-2) does not change the spectrum object. Cloud PRs #41 (H-min-sim), #42 (H-peaks), and #43 (H-min-sim at 10:30Z) stayed draft; Actions 40850896999 therefore spent UTC ticket 2 on already-live `PEAK_MZ_TOL=0.02`.

## Concrete improvement for this slot

Implement **one** major ablation: `MIN_SIMILARITY` **0.05 → 0.12**.

Retarget Actions **slot-3** (next unused hourly) from already-live H-peak-mz to **H-min-sim**. Retarget **slot-4** to `TOP_PEAKS=160` only so it does not reset `MIN_SIMILARITY` back to 0.05.

If this PR is **not** merged before that slot, Actions will spend UTC ticket 3 on `PEAK_MZ_TOL=0.02` — a third no-op today.

Do **not** `workflow_dispatch` casmi-loop from this runner: an unmerged dispatch would replay H-peak-mz on main.

## Cloud submit attempt (this runner)

`write_kaggle_credentials()` returned **False**. `KAGGLE_USERNAME`, `KAGGLE_KEY`, and `KAGGLE_API_TOKEN` are unset; `~/.kaggle/kaggle.json` was not written. Kaggle CLI 2.2.5 is installed but cannot authenticate. No `kernels push` / `competition_submit_code` from Cloud. Handoff is the substantial cycle03 docs + `config_patch: {"MIN_SIMILARITY": 0.12}` so casmi-loop slot 3 can reuse them after merge.
