# Analysis 2026-10-08_cycle02

**Competition day:** 2026-10-08, clock starts 01:00 America/Chicago (CDT = UTC−5 → 06:00 UTC).  
**This Cloud slot:** 06:01 UTC cron (`0 6 * * *`).  
**Best scored public (ours):** **0.143** (v0.1 exact-dup retrieval). Later code submits often list `publicScore=None` in CLI snapshots.

## Quota (re-checked this run)

| Clock | Used / 5 | Evidence |
| --- | --- | --- |
| UTC calendar 2026-10-08 | **1 / 5** | Actions `37709655430` → Kaggle **56927100** `2026-10-08_cycle01 H-top-peaks` kernel v70 at **01:04Z** (20:04 CDT Oct 7, *before* Chicago day start). |
| Chicago 01:00 CDT → now | **0 / 5** | No code submit since 06:00 UTC. |
| Cloud env Kaggle API | **unavailable** | `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN` absent (same as every Cloud cron). Could not write `~/.kaggle/kaggle.json` or call `competitions submissions`. |

Quota is **not** exhausted. Proceed with implement; skip `kernels push` / `competition_submit_code` until secrets exist or Actions merges this patch.

## Last known Kaggle rows (from cycle01 Actions briefing)

- id=56921568 score=None COMPLETE `2026-10-07_cycle04 H-peaks`
- id=56913966 score=None COMPLETE `2026-10-07_cycle03 H-mass-wide`
- id=56903778 score=None COMPLETE `2026-10-07_cycle02 H-entropy`
- id=56895779 score=None COMPLETE `2026-10-07_cycle01 H-top-peaks`
- plus the new **56927100** H-top-peaks (UTC Oct 8 cycle01)

Actions slot-2 fallback on `main` is still **H-entropy `ENTROPY_WEIGHT=0.75`**, which is already live — a wasted ticket if this PR is not merged before the next hourly `casmi-loop` (~07:00Z).

## Leaderboard context (CLIST 2026-10-08 ~06:10Z)

[CLIST standings](https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/): **pikachu 0.48**, **MarvinTMB 0.47**, then Oliver Ford / Sho Saga / Sls2 / vukpetar **0.45**, then a **0.44** pack. Community analog/quad-channel notebooks **0.328–0.339**. Gap vs our 0.143 is retrieval-only + poisoned exact-dup labels, not a missing 0.01-wide peak bin by itself.

## Why score stays low

1. **Poisoned exact dups** in `enveda-180`: test↔train spectra match, train InChIKey ≠ competition GT. `EXCLUDE_EXACT_DUPLICATES=True` is live; v0.1 still scored ~0.143 on the remaining easy hits.
2. **Live config already includes** the rotating Actions no-ops: `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, `MASS_TOL_PPM=35`, `MASS_TOL_PPM_BACKFILL=80`, `TOP_K_SPECTRA_PER_QUERY=120`, `MIN_SIMILARITY=0.05`.
3. **`PEAK_MZ_TOL` is still 0.01** — tighter than Flash Entropy Search’s 0.02 Da default. Mixed-library fragment alignment is the unused lever this slot.
4. **`INTENSITY_FLOOR` is still 0.001** (Cloud H-intensity PRs #13–#19, #21 remain draft).
5. Retrieval cannot invent Class-3 structures absent from the train libraries.

## Concrete next-slot improvement

Apply **one** unused constant: `PEAK_MZ_TOL` 0.01 → **0.02**. Retarget Actions `FALLBACK_ABLATIONS[1]` from H-entropy to H-peak-mz so the next hourly runner submits this factor instead of a no-op. Do **not** CSV-submit.
