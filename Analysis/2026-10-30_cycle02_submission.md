# Analysis — 2026-10-30 cycle02

## Quota (re-checked at 2026-10-30T07:33Z)

Competition day for this Cloud prompt starts **01:00 America/Chicago** (06:00 UTC). Kaggle’s enforced reset is midnight UTC (`scripts/casmi_loop/slots.py`).

Cloud runner has **no** `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN`, so the CLI list could not be refreshed here. Counts below come from Actions run **40987360854** logs + `origin/main` `agent/state.json` after the ~02:00Z push (`dea2af3`).

| Clock | Used | Remaining | Notes |
|-------|------|-----------|-------|
| UTC calendar 2026-10-30 | **1 / 5** | 4 | 57789094 (~02:00Z) |
| Chicago 01:00 (since 06:00 UTC) | **0 / 5** | 5 | The UTC ticket landed *before* 01:00 CDT |
| Quota exhausted? | **No** | — | Do not exit; implement + hand off |

## Recent Kaggle submissions (newest first, from Actions log + state)

- id=**57789094** score=None status=PENDING (at submit) desc=`2026-10-30_cycle01 H-top-peaks` kernel **v171** (Actions 40987360854, ~02:00Z)
- id=**57783593** score=None status=COMPLETE desc=`2026-10-29_cycle04 H-peaks` kernel **v170**
- id=**57777563** score=None status=COMPLETE desc=`2026-10-29_cycle03 H-peak-mz` kernel **v169**
- id=**57767052** score=None status=COMPLETE desc=`2026-10-29_cycle02 H-peak-mz` kernel **v168**
- id=**57756058** score=None status=COMPLETE desc=`2026-10-29_cycle01 H-top-peaks` kernel **v167**
- id=57750957 score=None status=COMPLETE desc=`2026-10-28_cycle04 H-peaks`

All recent public scores are **null**. Best scored public remains **0.143** (v0.1).

## Leaderboard context (CLIST, page said “updated 11 hours ago” at 07:33Z)

Public top: **Oleksandr Parfionov 0.52**, **Savko 0.51**, **pikachu / Shehab Alshehabi / CHU1PC 0.50**, team051 / Paweł Biernat / JJ 0.49, then a long 0.48 band. Community analog notebooks still ~0.43–0.46; copied-notebook pile ~0.464. Gap vs our 0.143 is not a missing `TOP_PEAKS` or `PEAK_MZ_TOL` constant — those are already live (`TOP_PEAKS=128` after today’s cycle01, `PEAK_MZ_TOL=0.02`).

## Why the score is low

1. **Poisoned exact duplicates (v0.1 failure).** Exact test↔train spectrum copies exist in `enveda-180` whose train InChIKey14 ≠ competition GT. Exact-dup exclusion is on; that prevents the 0.143 “perfect library match” trap from repeating, but it also removes the easy rank-1 hits.

2. **Weak library hits pad the top-25.** `retrieve.py` keeps every hybrid score `>= cfg.min_similarity` before truncating to `TOP_K_SPECTRA_PER_QUERY=120`. Live `MIN_SIMILARITY=0.05` is far below GNPS library-search / MASST admission defaults and far below Li/Fiehn’s 0.75 *call* threshold. Decoys occupy rank-list slots that MRR@25 then treats as plausible.

3. **Slot rotation has been a no-op for weeks, and it is about to happen again.** Live main after Actions 10-30 cycle01: `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, mass-wide 35/80, `TOP_K=120`, `PEAK_MZ_TOL=0.02`, **`MIN_SIMILARITY=0.05`**. Replaying H-peak-mz (slot-2 fallback) does not change the spectrum object. Cloud PRs #38–#44 (H-min-sim / H-peaks) stayed unmerged; if this PR is not merged before the 08:00 UTC hourly, Actions will spend UTC ticket 2 on already-live `PEAK_MZ_TOL=0.02`.

## Concrete improvement for this slot

Implement **one** major ablation: `MIN_SIMILARITY` **0.05 → 0.12**.

Retarget Actions **slot-2** (next unused hourly, historically 08:00 UTC) from already-live H-peak-mz to **H-min-sim**. Retarget **slot-3** and **slot-4** to `TOP_PEAKS=160` only so they do not reset `MIN_SIMILARITY` back to 0.05.

If this PR is **not** merged before that slot, Actions will spend UTC ticket 2 on `PEAK_MZ_TOL=0.02` — a second no-op today.

## Cloud submit attempt (this runner)

`write_kaggle_credentials()` returned **False**. `KAGGLE_USERNAME`, `KAGGLE_KEY`, and `KAGGLE_API_TOKEN` are unset; `~/.kaggle/kaggle.json` was not written. Kaggle CLI 2.2.5 is installed but cannot authenticate (`kaggle auth login` / `KAGGLE_API_TOKEN` required). No `kernels push` / `competition_submit_code` from Cloud. Did **not** dispatch casmi-loop (unmerged dispatch would replay `PEAK_MZ_TOL=0.02`). Handoff is the substantial cycle02 docs + `config_patch: {"MIN_SIMILARITY": 0.12}` so casmi-loop slot 2 can reuse them after merge.
