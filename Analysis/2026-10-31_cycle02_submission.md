# Analysis — 2026-10-31 cycle02

## Quota (re-checked at 2026-10-31T06:02Z)

Competition day for this Cloud prompt starts **01:00 America/Chicago** (06:00 UTC on CDT). Kaggle’s enforced reset is midnight UTC (`scripts/casmi_loop/slots.py`).

Cloud runner has **no** `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN`, so `write_kaggle_credentials()` returned False and the CLI list could not be refreshed here. Counts below come from `origin/main` `agent/state.json` after Actions run **41150722176** (cycle01 push `80c3e2d`) plus `gh run list`.

| Clock | Used | Remaining | Notes |
|-------|------|-----------|-------|
| UTC calendar 2026-10-31 | **1 / 5** | 4 | 57821778 (00:44Z, before Chicago day start) |
| Chicago 01:00 (since 06:00 UTC) | **0 / 5** | 5 | UTC ticket 1 landed *before* 01:00 CDT |
| Quota exhausted? | **No** | — | Do not exit; implement + hand off |

## Recent Kaggle submissions (newest first, from state.json)

| Kaggle id | Kernel | Score | Status | Message | Patch |
|-----------|--------|-------|--------|---------|-------|
| 57821778 | v175 | null | COMPLETE | 2026-10-31_cycle01 H-top-peaks | `TOP_PEAKS=128` (already live) |
| 57816688 | v174 | null | COMPLETE | 2026-10-30_cycle04 H-peaks | `TOP_PEAKS=160`, `MIN_SIMILARITY=0.05` |
| 57810528 | v173 | null | COMPLETE | 2026-10-30_cycle03 H-peak-mz | `PEAK_MZ_TOL=0.02` (already live) |
| 57799491 | v172 | null | COMPLETE | 2026-10-30_cycle02 H-peak-mz | `PEAK_MZ_TOL=0.02` (already live) |
| 57789094 | v171 | null | COMPLETE | 2026-10-30_cycle01 H-top-peaks | `TOP_PEAKS=128` (already live) |
| 57783593 | v170 | null | COMPLETE | 2026-10-29_cycle04 H-peaks | `TOP_PEAKS=160`, `MIN_SIMILARITY=0.05` |
| 57777563 | v169 | null | COMPLETE | 2026-10-29_cycle03 H-peak-mz | `PEAK_MZ_TOL=0.02` |
| 57767052 | v168 | null | COMPLETE | 2026-10-29_cycle02 H-peak-mz | `PEAK_MZ_TOL=0.02` |
| 57756058 | v167 | null | COMPLETE | 2026-10-29_cycle01 H-top-peaks | `TOP_PEAKS=128` |

Best scored public still **0.143** (v0.1). Every later code submit is **unscored** (`publicScore=null` in state).

## Leaderboard context (CLIST ~2026-10-31T06:05Z, page “updated 11 hours ago”)

Public top: **Oleksandr Parfionov 0.52**, **Savko 0.52**, pikachu / Shehab Alshehabi / CHU1PC **0.50**, then a long 0.49 / 0.48 band. Community analog notebooks now badge **0.472–0.477**. Gap vs our 0.143 is not a missing `TOP_PEAKS` or `PEAK_MZ_TOL` constant — those are already live.

## Why the score is low

1. **v0.1 failure mode still applies.** Exact test↔train spectrum duplicates in `enveda-180` carry train labels that are **not** competition GT. Exact-dup exclusion stays on (`EXCLUDE_EXACT_DUPLICATES=True`).

2. **Admission floor is still 0.05.** `retrieve.py` keeps every hybrid entropy/modcos hit with `sim >= cfg.min_similarity`. Live `MIN_SIMILARITY=0.05` lets weak decoys occupy the 25-slot list. Li/Fiehn FDR work treats entropy similarity 0.75 as the <10% FDR operating point; GNPS living-data uses 0.7 / 6 peaks; Passatutto 5% FDR typically sits at cosine 0.50–0.55. Scores in 0.05–0.11 are almost certainly decoys.

3. **Slot rotation has been a no-op for days.** Live main after Actions 10-31 cycle01: `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, mass-wide 35/80, `TOP_K=120`, **`PEAK_MZ_TOL=0.02`**, **`MIN_SIMILARITY=0.05`**. Replaying H-peak-mz (slot-2/3 fallback) does not change the spectrum object. Cloud H-min-sim PRs **#38–#48** stayed draft; Actions later burned the next UTC ticket on already-live `PEAK_MZ_TOL=0.02`.

## Concrete improvements for this slot

- **One major ablation:** `MIN_SIMILARITY` 0.05 → **0.12**.
- Retarget Actions **slot-2 and slot-3** fallbacks to H-min-sim so the next unused hourly run (`07:00 UTC`) does not replay 0.02.
- Retarget **slot-4** to `{TOP_PEAKS: 160}` only — do **not** reset the floor back to 0.05.
- Hold every other live knob.
- Do **not** dispatch `casmi-loop` until this change is on `main`. An unmerged dispatch would spend UTC ticket 2 on `PEAK_MZ_TOL=0.02`.

## Cloud submit attempt (this runner)

`write_kaggle_credentials()` returned **False**. `KAGGLE_USERNAME`, `KAGGLE_KEY`, and `KAGGLE_API_TOKEN` are unset; `~/.kaggle/kaggle.json` was not written. No `kernels push` / `competition_submit_code` from Cloud. Handoff is the substantial cycle02 docs + `config_patch: {"MIN_SIMILARITY": 0.12}` so casmi-loop slot 2 can reuse them after merge.
