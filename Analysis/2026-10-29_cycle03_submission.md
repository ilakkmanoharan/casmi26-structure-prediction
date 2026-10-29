# Analysis — 2026-10-29 cycle03

## Quota (re-checked at 2026-10-29T09:10Z)

Competition day for this Cloud prompt starts **01:00 America/Chicago** (06:00 UTC today). Kaggle’s enforced reset is midnight UTC (`scripts/casmi_loop/slots.py`). Suggested local slots: 01:00, 02:30, **04:00**, 05:30, 07:00 CDT. This run is the **04:00 CDT / 09:00 UTC** slot.

Cloud runner has **no** `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN`, so `write_kaggle_credentials()` cannot write `~/.kaggle/kaggle.json`. Counts below come from Actions run **40805625766** logs + `origin/main` `agent/state.json` after the 02:33Z push (`dfd5902`) + `gh run list` (no casmi-loop run after 02:19Z).

| Clock | Used | Remaining | Notes |
|-------|------|-----------|-------|
| UTC calendar 2026-10-29 | **1 / 5** | 4 | 57756058 (~02:33Z) |
| Chicago 01:00 (since 06:00 UTC) | **0 / 5** | 5 | UTC ticket 1 landed at 21:33 CDT Oct 28, *before* 01:00 CDT |
| Quota exhausted? | **No** | — | Do not exit; implement + hand off |

No additional Kaggle code submits landed between 06:00Z Cloud cycle02 and this 09:00Z slot. casmi-loop cron is `0 * * * *` but GitHub has not scheduled another successful run since 02:19Z (same sparse cadence as 10-28: ~4 runs/day, not true hourly).

## Recent Kaggle submissions (newest first, from Actions log + state)

- id=**57756058** score=None status=PENDING (at submit) desc=`2026-10-29_cycle01 H-top-peaks` kernel **v167** (Actions 40805625766, ~02:33Z)
- id=**57750957** score=None status=COMPLETE desc=`2026-10-28_cycle04 H-peaks` kernel **v166**
- id=57745595 score=None status=COMPLETE desc=`2026-10-28_cycle03 H-peak-mz`
- id=57735008 score=None status=COMPLETE desc=`2026-10-28_cycle02 H-peak-mz`
- id=57724850 score=None status=COMPLETE desc=`2026-10-28_cycle01 H-top-peaks`
- id=57716036 score=None status=COMPLETE desc=`2026-10-27_cycle05 H-domain`
- id=57712244 score=None status=COMPLETE desc=`2026-10-27_cycle04 H-peaks`
- id=57704012 score=None status=COMPLETE desc=`2026-10-27_cycle03 H-peak-mz`
- id=57693774 score=None status=COMPLETE desc=`2026-10-27_cycle02 H-peak-mz`
- id=57685058 score=None status=COMPLETE desc=`2026-10-27_cycle01 H-top-peaks`

All recent public scores are **null**. Best scored public remains **0.143** (v0.1).

## Leaderboard context (CLIST page, updated ~10h before 09:10Z)

Public top: **Oleksandr Parfionov 0.52**, **Savko 0.51**, **pikachu / Shehab Alshehabi / CHU1PC 0.50**. Crowd at 0.48–0.49. Community analog notebooks still ~0.43–0.46 (e.g. public forks labeled 0.472 / 0.477). Gap vs our 0.143 is not a missing `PEAK_MZ_TOL` constant — that is already live at 0.02.

## Why the score is low

1. **Poisoned exact duplicates (v0.1 failure).** Exact test↔train spectrum copies exist in `enveda-180` whose train InChIKey14 ≠ competition GT. Exact-dup exclusion is on; that prevents the 0.143 “perfect library match” trap from repeating, but it also removes the easy rank-1 hits.

2. **Hard peak cap after the 1% floor.** `clean_spectrum` already drops sub-1% noise (`INTENSITY_FLOOR=0.01`). `TOP_PEAKS=128` then discards remaining mid-intensity ions that Flash Entropy / ms_entropy would keep (`max_peak_num=None`). Entropy similarity is designed to *use* those ions, not drop them.

3. **Admission floor is still 0.05 on live main.** Cycle02 PR #41 (`MIN_SIMILARITY` 0.05 → 0.12) is still **draft / unmerged**. This cycle does **not** apply that constant (one factor). Slot-2 fallback is retargeted so the next unused Actions hour can take the floor without replaying `PEAK_MZ_TOL=0.02`.

4. **Slot rotation has been a no-op for weeks.** Live main after Actions 10-29 cycle01: `TOP_PEAKS=128`, `PEAK_MZ_TOL=0.02`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, mass-wide 35/80, `TOP_K=120`, `MIN_SIMILARITY=0.05`. Replaying H-peak-mz does not change which fragments enter entropy/modcos.

## Concrete improvement for this slot

Implement **one** major ablation: `TOP_PEAKS` **128 → 160**.

Retarget Actions **slot-2** (next unused UTC ticket) to **H-min-sim**, and **slot-3 / slot-4** to **H-peaks** (`TOP_PEAKS=160` only — do not reset `MIN_SIMILARITY` back to 0.05).

If this PR is **not** merged before the next casmi-loop hour, Actions will spend UTC ticket 2 on `PEAK_MZ_TOL=0.02` — a second no-op today — unless PR #41 merges first.

## Cloud submit attempt (this runner)

`write_kaggle_credentials()` returned **False**. `KAGGLE_USERNAME`, `KAGGLE_KEY`, and `KAGGLE_API_TOKEN` are unset; `~/.kaggle/kaggle.json` was not written. No `kernels push` / `competition_submit_code` from Cloud. Handoff is the substantial cycle03 docs + `config_patch: {"TOP_PEAKS": 160}` so casmi-loop slot 3 can reuse them after merge. Slot-2 still needs the H-min-sim fallback retarget (cycle02 docs live only on unmerged PR #41).
