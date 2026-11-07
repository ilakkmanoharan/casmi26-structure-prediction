# Analysis — 2026-11-07 cycle03

## Quota (re-checked at 2026-11-07T10:32Z)

Competition day for this Cloud prompt starts **01:00 America/Chicago** (07:00 UTC on CST). Kaggle’s enforced reset is midnight UTC (`scripts/casmi_loop/slots.py`).

Cloud runner has **no** `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN` (confirmed empty before any CLI call). `~/.kaggle/kaggle.json` was **not** written. Counts below come from Actions run **42361044458** logs + `origin/main` `agent/state.json` after the 10:02Z push (`f1b0638`).

| Clock | Used | Remaining | Notes |
|-------|------|-----------|-------|
| UTC calendar 2026-11-07 | **2 / 5** | 3 | 58076904 (02:53Z), 58088101 (10:02Z) |
| Chicago 01:00 (since 07:00 UTC) | **1 / 5** | 4 | cycle01 landed *before* 01:00 CST; cycle02 after |
| Quota exhausted? | **No** | — | Do not exit; implement + hand off |

## Recent Kaggle submissions (newest first, from Actions 42361044458 log + state)

- id=**58088101** score=None status=PENDING (at submit) desc=`2026-11-07_cycle02 H-peak-mz` kernel **v203** (Actions 42361044458, 10:02Z)
- id=**58076904** score=None status=COMPLETE desc=`2026-11-07_cycle01 H-top-peaks` kernel **v202** (Actions 42330089426, 02:53Z)
- id=58071327 score=None status=COMPLETE desc=`2026-11-06_cycle04 H-peaks`
- id=58065731 score=None status=COMPLETE desc=`2026-11-06_cycle03 H-peak-mz`
- id=58055178 score=None status=COMPLETE desc=`2026-11-06_cycle02 H-peak-mz`
- id=58042294 score=None status=COMPLETE desc=`2026-11-06_cycle01 H-top-peaks`
- id=58035989 score=None status=COMPLETE desc=`2026-11-05_cycle03 H-peak-mz`
- id=58026170 score=None status=COMPLETE desc=`2026-11-05_cycle02 H-peak-mz`
- id=58012064 score=None status=COMPLETE desc=`2026-11-05_cycle01 H-top-peaks`
- id=58001652 score=None status=COMPLETE desc=`2026-11-04_cycle04 H-peaks`

All recent public scores are **null**. Best scored public remains **0.143** (v0.1).

## Leaderboard context (CLIST ~2026-11-07T10:32Z, ~9h stale)

Public top: **Shehab Alshehabi 0.54**, **Savko 0.53**, **Oleksandr Parfionov 0.52**, democat 0.51, pikachu / Paweł Biernat / CHU1PC 0.50. Community analog notebooks still ~0.43–0.48. Gap vs our 0.143 is not a missing `TOP_PEAKS=128` or `PEAK_MZ_TOL=0.02` constant — those are already live and were just re-submitted as UTC tickets 1–2.

## Why the score is low

1. **Poisoned exact duplicates (v0.1 failure).** Exact test↔train spectrum copies exist in `enveda-180` whose train InChIKey14 ≠ competition GT. Exact-dup exclusion is on; that prevents the 0.143 “perfect library match” trap from repeating, but it also removes the easy rank-1 hits.

2. **Peak ladder is still clipped at 128.** `clean_spectrum(..., top_peaks=cfg.top_peaks)` runs in `casmi26/index.py` and `retrieve.py`. Flash Entropy / ms_entropy default `max_peak_num=0` (no cap) after the 1% noise floor (`INTENSITY_FLOOR=0.01`, already live). NP spectra from GNPS / RIKEN / Enveda routinely keep more than 128 centroided ions after that floor. Entropy similarity is robust to extra noise ions (Li 2021); clipping mid-intensity diagnostic fragments loses identity-search signal.

3. **Slot rotation has been a no-op for weeks.** Live main after Actions 11-07 cycle02: `TOP_PEAKS=128`, `PEAK_MZ_TOL=0.02`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, mass-wide 35/80, `TOP_K=120`, `MIN_SIMILARITY=0.05`. Replaying H-peak-mz (slot-3 fallback) does not change the spectrum object.

4. **Retrieval-only ceiling.** Public 0.50–0.54 entries use analog / formula-pool / model channels. This kernel remains library retrieval. Do not claim Class-3 de novo.

## Concrete improvement for this slot

Implement **one** major ablation: `TOP_PEAKS` **128 → 256**.

Retarget Actions **slot-3** (next unused hourly; historically ~11:00 UTC after today’s 09:45 run) from already-live H-peak-mz to **H-top-peaks-256**. Retarget **slot-4** from `TOP_PEAKS=160` (would *reduce* the ladder once 256 is live) to **H-sim-gate** (`MIN_SIMILARITY=0.12`).

If this PR is **not** merged before that slot, Actions will spend UTC ticket 3 on `PEAK_MZ_TOL=0.02` — a third no-op today.

Distinct from unmerged drafts #82 (H-sim-gate), #83 (H-mass-tight 15 ppm), #84 (H-entropy-pure).

## Cloud submit attempt (this runner)

`write_kaggle_credentials()` returned **False**. `KAGGLE_USERNAME`, `KAGGLE_KEY`, and `KAGGLE_API_TOKEN` are unset; `~/.kaggle/kaggle.json` was not written. No `kernels push` / `competition_submit_code` from Cloud. Handoff is the substantial cycle03 docs + `config_patch: {"TOP_PEAKS": 256}` so casmi-loop slot 3 can reuse them after merge.
