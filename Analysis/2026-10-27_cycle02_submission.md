# Analysis — 2026-10-27 cycle02

## Quota (pre-flight)

Competition day starts **01:00 America/Chicago**. Trigger: **2026-10-27T06:01Z** = 01:01 CDT.

| Clock | Used / 5 | Notes |
|-------|----------|-------|
| Chicago 01:00 | **0 / 5** | Day just opened. Actions 57685058 landed at 01:34 UTC (20:34 CDT Oct 26) — still yesterday on the Chicago clock. |
| UTC calendar (Kaggle reset) | **1 / 5** | Actions `casmi-loop` run 40431611852 → Kaggle **57685058**, kernel v158, `2026-10-27_cycle01 H-top-peaks`. |

`KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN` are **absent** in this Cloud environment (`~/.kaggle/` empty). Could not run `kaggle competitions submissions`. Count is from `agent/state.json` + `gh run list` on `casmi-loop.yml`. Quota is **not** exhausted; do not exit.

## Recent submissions (from `agent/state.json`, newest first)

| Kaggle id | Kernel | Status | Description | Public score |
|-----------|--------|--------|-------------|--------------|
| 57685058 | v158 | COMPLETE | 2026-10-27_cycle01 H-top-peaks · `TOP_PEAKS=128` | null |
| 57679305 | v157 | COMPLETE | 2026-10-26_cycle04 H-peaks · `TOP_PEAKS=160`, `MIN_SIMILARITY=0.05` | null |
| 57673078 | v156 | COMPLETE | 2026-10-26_cycle03 H-peak-mz · `PEAK_MZ_TOL=0.02` | null |
| 57662597 | v155 | COMPLETE | 2026-10-26_cycle02 H-peak-mz · `PEAK_MZ_TOL=0.02` | null |
| 57652978 | v154 | COMPLETE | 2026-10-26_cycle01 H-top-peaks · `TOP_PEAKS=128` | null |
| 57642549 | v153 | COMPLETE | 2026-10-25_cycle05 H-domain | null |
| 57638558 | — | COMPLETE | 2026-10-25_cycle04 H-peaks | null |
| 57631300 | — | COMPLETE | 2026-10-25_cycle03 H-peak-mz | null |
| 57621786 | — | COMPLETE | 2026-10-25_cycle02 H-peak-mz | null |
| 57612600 | — | COMPLETE | 2026-10-25_cycle01 H-top-peaks | null |

Kaggle has not written a public score on any of these rows. Best **scored** public remains **0.143** (v0.1).

## Leaderboard context

CLIST mirror ([standings](https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/), updated ~3h before this cycle, scores rounded):

1. Savko savchenko **0.51**
2. Oleksandr Parfionov **0.50**
3. pikachu **0.50**
4. Shehab Alshehabi **0.50**
5. CHU1PC **0.50**

Official Kaggle leaderboard fetch timed out this run. Prior official snapshot (~2026-10-26): Parfionov 0.504, Savko 0.503, pikachu 0.499. Community analog notebooks still cluster ~0.43–0.46; a large copied-notebook pile sits at **0.464**. Our 0.143 is ~0.36 below the frontier — a few extra rank-1 hits on the ~132-molecule public slice, not a retrieval-solved Class-3 problem.

## Why the score is low

1. **Poisoned exact duplicates (v0.1).** Exact test↔train spectrum copies exist in `enveda-180` whose train labels ≠ competition GT. Perfect library match on those rows yields ~0.143, not 1.0. `EXCLUDE_EXACT_DUPLICATES=True` stays on.

2. **Admission floor is still 0.05.** `search_spectra` in `casmi26/retrieve.py` keeps every `hybrid_similarity >= cfg.min_similarity`. After pairing was widened to 20 mDa (`PEAK_MZ_TOL=0.02`, live since 10-24 / 10-26 Actions), more decoy fragments pair, so even more junk clears 0.05 and occupies the 25-slot list. Li/Fiehn recommend entropy similarity ≳ 0.75 for FDR < 10%; 0.12 is a conservative first step that still admits weak-but-real analog hits.

3. **Slot rotation has been a no-op for weeks.** Live main after Actions 10-27 cycle01: `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, mass-wide 35/80, `PEAK_MZ_TOL=0.02`, **`MIN_SIMILARITY=0.05`**. Next unused Actions fallback on main is H-peak-mz (`PEAK_MZ_TOL=0.02`) — already live. Replaying it wastes UTC ticket 2.

4. **Cloud H-min-sim PR #38 stayed draft.** Yesterday’s Cloud cycle implemented this exact ablation; Actions later submitted H-peak-mz / H-peaks instead.

## Concrete improvement this slot

Raise **`MIN_SIMILARITY` 0.05 → 0.12** only. Hold peak count, pairing window, mix weight, mass window, and exact-dup ban. Retarget Actions slot-2 → H-min-sim and slot-3 → H-peaks (`TOP_PEAKS=160` only, do not reset `MIN_SIMILARITY`) so the next unused hourly cron cannot replay 0.02.

If Cloud cannot `kernels push` (missing secrets), leave `submitted=false` and rely on a merge before the next unused `casmi-loop` hour (~07:00 UTC). Do **not** dispatch Actions from this branch — an unmerged dispatch would still run main’s H-peak-mz no-op.
