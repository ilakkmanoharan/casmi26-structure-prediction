# Analysis — 2026-10-25 cycle02

## Quota (re-checked at 2026-10-25T06:05Z)

Competition day for this Cloud prompt starts **01:00 America/Chicago** (06:00 UTC). Kaggle’s enforced reset is midnight UTC (`scripts/casmi_loop/slots.py`).

Cloud runner has **no** `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN`, so the CLI list could not be refreshed here (`write_kaggle_credentials()` → False; `~/.kaggle/` empty). Counts below come from Actions run **40148909273** + `origin/main` `agent/state.json` after the 01:16Z push (`c1f236c`).

| Clock | Used | Remaining | Notes |
|-------|------|-----------|-------|
| UTC calendar 2026-10-25 | **1 / 5** | 4 | 57612600 (~01:16Z) |
| Chicago 01:00 (since 06:00 UTC) | **0 / 5** | 5 | The UTC ticket landed *before* 01:00 CDT |
| Quota exhausted? | **No** | — | Do not exit; implement + hand off |

## Recent Kaggle submissions (newest first, from Actions / state)

- id=**57612600** score=None status=COMPLETE desc=`2026-10-25_cycle01 H-top-peaks` kernel **v149** (Actions 40148909273, ~01:16Z)
- id=57603123 score=None status=COMPLETE desc=`2026-10-24_cycle05 H-domain` kernel v148
- id=57597566 score=None status=COMPLETE desc=`2026-10-24_cycle04 H-peaks` kernel v147
- id=57591809 score=None status=COMPLETE desc=`2026-10-24_cycle03 grok-docs` kernel v146 (`PEAK_MZ_TOL=0.02`)
- id=57584149 score=None status=COMPLETE desc=`2026-10-24_cycle02 H-entropy` kernel v145
- id=57576969 score=None status=COMPLETE desc=`2026-10-24_cycle01 H-top-peaks` kernel v144

All recent public scores are **null**. Best scored public remains **0.143** (v0.1).

## Leaderboard context (CLIST ~2026-10-25T06:10Z)

Public top: **Oleksandr Parfionov 0.50**, **pikachu 0.50**, **Savko 0.50**, **CHU1PC 0.50**, JJ 0.49, MarvinTMB / Oliver Ford / Dunyuan Zha / democatXamer / Parth Talsania 0.48. Community analog notebooks still ~0.43–0.46. Gap vs our 0.143 is not a missing `PEAK_MZ_TOL` or `ENTROPY_WEIGHT` constant — those are already live.

## Why the score is low

1. **Poisoned exact duplicates (v0.1 failure).** Exact test↔train spectrum copies exist in `enveda-180` whose train InChIKey14 ≠ competition GT. Exact-dup exclusion is on; that prevents the 0.143 “perfect library match” trap from repeating, but it also removes the easy rank-1 hits.

2. **Cleaned ladder is still truncated at 128.** `clean_spectrum` applies the 1% floor then `TOP_PEAKS`. Flash Entropy / ms_entropy default `max_peak_num=None`. After the 10-24 merge, fragment pairing is the literature 20 mDa window, so extra mid-intensity ions can now match. Keeping only 128 of them still drops diagnostic fragments the 2024 JASMS weighting paper treats as structurally informative.

3. **Slot-2 fallback is a no-op.** Live main after Actions 10-25 cycle01: `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, mass-wide 35/80, `TOP_K=120`, `MIN_SIMILARITY=0.05`, **`PEAK_MZ_TOL=0.02`**. Replaying H-peak-mz (slot-2 fallback) does not change the spectrum object.

## Concrete improvement for this slot

Implement **one** major ablation: `TOP_PEAKS` **128 → 160**.

Retarget Actions **slot-2** (next unused hourly, `0 * * * *`) from already-live H-peak-mz to **H-peaks**, and **slot-3** from H-peak-mz to **H-min-sim** (`MIN_SIMILARITY=0.12`) so a later unused hour cannot replay 0.02 again.

If this PR is **not** merged before the next unused casmi-loop hour, Actions will spend UTC ticket 2 on `PEAK_MZ_TOL=0.02` — a second no-op today.

## Cloud submit attempt (this runner)

`write_kaggle_credentials()` returned **False**. `KAGGLE_USERNAME`, `KAGGLE_KEY`, and `KAGGLE_API_TOKEN` are unset; `~/.kaggle/kaggle.json` was not written. No `kernels push` / `competition_submit_code` from Cloud. Handoff is the substantial cycle02 docs + `config_patch: {"TOP_PEAKS": 160}` so casmi-loop slot 2 can reuse them after merge.
