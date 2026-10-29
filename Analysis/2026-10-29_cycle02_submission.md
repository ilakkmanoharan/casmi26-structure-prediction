# Analysis — 2026-10-29 cycle02

## Quota (re-checked at 2026-10-29T06:10Z)

Competition day for this Cloud prompt starts **01:00 America/Chicago** (06:00 UTC). Kaggle’s enforced reset is midnight UTC (`scripts/casmi_loop/slots.py`).

Cloud runner has **no** `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN`, so `write_kaggle_credentials()` cannot write `~/.kaggle/kaggle.json`. Counts below come from Actions run **40805625766** logs + `origin/main` `agent/state.json` after the 02:33Z push (`dfd5902`).

| Clock | Used | Remaining | Notes |
|-------|------|-----------|-------|
| UTC calendar 2026-10-29 | **1 / 5** | 4 | 57756058 (~02:33Z) |
| Chicago 01:00 (since 06:00 UTC) | **0 / 5** | 5 | UTC ticket 1 landed at 21:33 CDT Oct 28, *before* 01:00 CDT |
| Quota exhausted? | **No** | — | Do not exit; implement + hand off |

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

## Leaderboard context (CLIST ~2026-10-29T02:00Z, ~4h stale)

Public top: **Oleksandr Parfionov 0.52**, **Savko 0.51**, **pikachu / Shehab Alshehabi / CHU1PC 0.50**. Community analog notebooks still ~0.43–0.46. Gap vs our 0.143 is not a missing `TOP_PEAKS` or `PEAK_MZ_TOL` constant — those are already live.

## Why the score is low

1. **Poisoned exact duplicates (v0.1 failure).** Exact test↔train spectrum copies exist in `enveda-180` whose train InChIKey14 ≠ competition GT. Exact-dup exclusion is on; that prevents the 0.143 “perfect library match” trap from repeating, but it also removes the easy rank-1 hits.

2. **Admission floor is still 0.05.** `search_mass_window` keeps a library spectrum iff `sim >= cfg.min_similarity` (`casmi26/retrieve.py`). Live `MIN_SIMILARITY=0.05` lets near-random entropy/modcos scores occupy `top_k=120` and then the top-25. Li/Fiehn treat scores well below 0.75 as non-identifications; 0.05 is an order of magnitude below that band.

3. **Slot rotation has been a no-op for weeks.** Live main after Actions 10-29 cycle01: `TOP_PEAKS=128`, `PEAK_MZ_TOL=0.02`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, mass-wide 35/80, `TOP_K=120`, **`MIN_SIMILARITY=0.05`**. Replaying H-peak-mz (slot-2 fallback) does not change which hits enter the rank list.

## Concrete improvement for this slot

Implement **one** major ablation: `MIN_SIMILARITY` **0.05 → 0.12**.

Retarget Actions **slot-2** (next unused hourly, historically ~07:00 UTC) to **H-min-sim**, and **slot-3 / slot-4** to **H-peaks** (`TOP_PEAKS=160` only — do not reset `MIN_SIMILARITY` back to 0.05).

If this PR is **not** merged before that slot, Actions will spend UTC ticket 2 on `PEAK_MZ_TOL=0.02` — a second no-op today.

## Cloud submit attempt (this runner)

`write_kaggle_credentials()` returned **False**. `KAGGLE_USERNAME`, `KAGGLE_KEY`, and `KAGGLE_API_TOKEN` are unset; `~/.kaggle/kaggle.json` was not written. No `kernels push` / `competition_submit_code` from Cloud. Handoff is the substantial cycle02 docs + `config_patch: {"MIN_SIMILARITY": 0.12}` so casmi-loop slot 2 can reuse them after merge.
