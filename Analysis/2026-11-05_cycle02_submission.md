# Analysis — 2026-11-05 cycle02

## Quota (re-checked at 2026-11-05T07:35Z)

Competition day for this Cloud prompt starts **01:00 America/Chicago** (07:00 UTC on 2026-11-05, CST). Kaggle’s enforced reset is midnight UTC (`scripts/casmi_loop/slots.py`).

Cloud runner has **no** `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN`, so `~/.kaggle/kaggle.json` was **not** written and the CLI list could not be refreshed here. Counts below come from Actions run **41976074079** logs + `origin/main` `agent/state.json` after the 06:06Z push (`8c9adc0`).

| Clock | Used | Remaining | Notes |
|-------|------|-----------|-------|
| UTC calendar 2026-11-05 | **1 / 5** | 4 | 58012064 (kernel v195, ~06:06Z) |
| Chicago 01:00 (since 07:00 UTC) | **0 / 5** | 5 | UTC ticket 1 landed *before* 01:00 CST |
| Quota exhausted? | **No** | — | Do not exit; implement + hand off |

## Recent Kaggle submissions (newest first, from Actions log)

- id=**58012064** score=None status=PENDING (at submit) desc=`2026-11-05_cycle01 H-top-peaks` kernel **v195** (Actions 41976074079, 06:06Z)
- id=**58001652** score=None status=COMPLETE desc=`2026-11-04_cycle04 H-peaks` kernel **v194**
- id=**57992996** score=None status=COMPLETE desc=`2026-11-04_cycle03 H-peak-mz` kernel **v193**
- id=**57979390** score=None status=COMPLETE desc=`2026-11-04_cycle02 H-peak-mz` kernel **v192**
- id=**57967804** score=None status=COMPLETE desc=`2026-11-04_cycle01 H-top-peaks` kernel **v191**
- id=57961369 score=None status=COMPLETE desc=`2026-11-03_cycle04 H-peaks`
- id=57953771 score=None status=COMPLETE desc=`2026-11-03_cycle03 H-peak-mz`
- id=57939381 score=None status=COMPLETE desc=`2026-11-03_cycle02 H-peak-mz`
- id=57927482 score=None status=COMPLETE desc=`2026-11-03_cycle01 H-top-peaks`
- id=57917568 score=None status=COMPLETE desc=`2026-11-02_cycle03 H-peak-mz`

All recent public scores are **null**. Best scored public remains **0.143** (v0.1). OpenAI on Actions returned **HTTP 429**, so slot 1 used the deterministic fallback (`TOP_PEAKS=128`) rather than a new ablation.

## Leaderboard context (CLIST, updated ~17h before this run)

Public top: **Shehab Alshehabi 0.54**, **Savko 0.52**, **Oleksandr Parfionov 0.52**, democat 0.51, pikachu / CHU1PC 0.50. A large public-notebook cluster still sits near **0.464**. Gap vs our 0.143 is not a missing `TOP_PEAKS` or `PEAK_MZ_TOL` constant — those are already live.

## Why the score is low

1. **Poisoned exact duplicates (v0.1 failure).** Exact test↔train spectrum copies exist in `enveda-180` whose train InChIKey14 ≠ competition GT. Exact-dup exclusion is on; that prevents the 0.143 “perfect library match” trap from repeating, but it also removes the easy rank-1 hits.

2. **Score function still mixes 25% modified cosine.** `hybrid_similarity` returns `0.75·entropy + 0.25·modcos` (`casmi26/spectrum.py`). Li & Fiehn 2021 showed entropy **alone** beats cosine; cosine collapses on a single intense noise ion and saturates on shared fragments. The live 0.75 mix copies the paper’s FDR *cutoff* as a blend weight — so every rank decision still listens to the weaker scorer.

3. **Slot rotation has been a no-op for weeks.** Live main after Actions 11-05 cycle01: `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, mass-wide 35/80, `TOP_K=120`, `MIN_SIMILARITY=0.05`, `PEAK_MZ_TOL=0.02`. Replaying H-peak-mz (slot-2 fallback) does not change the spectrum object. Cloud PR **#72** (draft) already specified `MIN_SIMILARITY=0.12` for this cycle02 tag and was not merged before this run.

## Concrete improvement for this slot

Implement **one** major ablation: `ENTROPY_WEIGHT` **0.75 → 1.0** (pure entropy similarity).

Retarget Actions **slot-2** (next unused hourly, historically ~08:00 UTC after today’s 05:46 run) from already-live H-peak-mz to **H-entropy-pure**. Retarget **slot-3** from the second H-peak-mz copy to **H-min-sim** (`MIN_SIMILARITY=0.12`) so ticket 3 is not a no-op if this PR merges. Slot-4 keeps `TOP_PEAKS=160` only so it cannot roll `MIN_SIMILARITY` back to 0.05.

If this PR is **not** merged before that slot, Actions will spend UTC ticket 2 on `PEAK_MZ_TOL=0.02` — a second no-op today.

## Cloud submit attempt (this runner)

`write_kaggle_credentials()` returned **False**. `KAGGLE_USERNAME`, `KAGGLE_KEY`, and `KAGGLE_API_TOKEN` are unset; `~/.kaggle/kaggle.json` was not written. No `kernels push` / `competition_submit_code` from Cloud. Handoff is the substantial cycle02 docs + `config_patch: {"ENTROPY_WEIGHT": 1.0}` so casmi-loop slot 2 can reuse them after merge.
