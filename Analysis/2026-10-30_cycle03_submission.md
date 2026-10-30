# Analysis — 2026-10-30 cycle03

Cloud Automation 12:02 UTC / 07:00 CDT (last suggested Cloud cadence). Competition day started 01:00 America/Chicago (06:00 UTC).

## Quota (pre-flight)

Kaggle CLI/API **could not be queried**: `KAGGLE_USERNAME` and `KAGGLE_KEY` are absent from this Cloud environment (same as every prior Cloud cycle). Counts below come from committed `agent/state.json` plus `gh run list` on `casmi-loop`.

| Clock | Used | Limit | Notes |
|-------|------|-------|-------|
| **Chicago** (01:00 CDT anchor) | **1** | 5 | Only Kaggle **57799491** (08:36Z / 03:36 CDT) is after 01:00 CDT. |
| **UTC calendar** (Actions `competition_day()`) | **2** | 5 | **57789094** at ~02:00Z + **57799491** at ~08:36Z. |

Quota is **not** exhausted. Do not exit.

09:00, 10:00, and 11:00 UTC `casmi-loop` hours did not fire (last successful schedule: 41025442759 at 08:17Z → cycle02). Next unused hourly window is **13:00 UTC**.

## Recent submissions (newest first, from `agent/state.json`)

| Kaggle id | Kernel | Score | Status | Message | Patch |
|-----------|--------|-------|--------|---------|-------|
| 57799491 | v172 | null | COMPLETE | 2026-10-30_cycle02 H-peak-mz | `PEAK_MZ_TOL=0.02` (already live) |
| 57789094 | v171 | null | COMPLETE | 2026-10-30_cycle01 H-top-peaks | `TOP_PEAKS=128` (already live) |
| 57783593 | v170 | null | COMPLETE | 2026-10-29_cycle04 H-peaks | `TOP_PEAKS=160`, `MIN_SIMILARITY=0.05` |
| 57777563 | v169 | null | COMPLETE | 2026-10-29_cycle03 H-peak-mz | `PEAK_MZ_TOL=0.02` |
| 57767052 | v168 | null | COMPLETE | 2026-10-29_cycle02 H-peak-mz | `PEAK_MZ_TOL=0.02` |
| 57756058 | v167 | null | COMPLETE | 2026-10-29_cycle01 H-top-peaks | `TOP_PEAKS=128` |

Best scored public still **0.143** (v0.1). Every later code submit is **unscored** (`publicScore=null` in state).

## Leaderboard context

CLIST ([standings](https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/), page “updated 11 hours ago” at 12:02Z):

- **Oleksandr Parfionov 0.52**
- **Savko 0.51**
- pikachu / Shehab Alshehabi / CHU1PC **0.50**

Public analog notebooks now badge **0.472–0.477**. Gap vs our 0.143 is still ~0.33–0.38. Retrieval-only with a 0.05 admission floor cannot close that gap; it can at least stop packing the top-25 with noise.

## Why score is low

1. **v0.1 failure mode still applies.** Exact test↔train spectrum duplicates in `enveda-180` carry train labels that are **not** competition GT. Exact-dup exclusion stays on (`EXCLUDE_EXACT_DUPLICATES=True`).

2. **Admission floor is still 0.05.** `retrieve.py` keeps every hybrid entropy/modcos hit with `sim >= cfg.min_similarity`. Live `MIN_SIMILARITY=0.05` lets weak decoys occupy the 25-slot list. Li/Fiehn FDR work treats entropy similarity 0.75 as the <10% FDR operating point; classic practice uses 0.7–0.8. Scores in 0.05–0.11 are almost certainly decoys.

3. **Slot rotation has been a no-op for days.** Live main after Actions 10-30 cycle02: `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, mass-wide 35/80, `TOP_K=120`, **`PEAK_MZ_TOL=0.02`**, **`MIN_SIMILARITY=0.05`**. Replaying H-peak-mz (slot-2/3 fallback) does not change the spectrum object. Cloud H-min-sim PRs **#38–#47** stayed draft; Actions later burned the next UTC ticket on already-live `PEAK_MZ_TOL=0.02`.

## Concrete improvements for this slot

- **One major ablation:** `MIN_SIMILARITY` 0.05 → **0.12**.
- Retarget Actions **slot-2 and slot-3** fallbacks to H-min-sim so the next unused hourly run (`13:00 UTC` or later) does not replay 0.02.
- Retarget **slot-4** to `{TOP_PEAKS: 160}` only — do **not** reset the floor back to 0.05.
- Hold every other live knob.
- Do **not** dispatch `casmi-loop` until this change is on `main`. An unmerged dispatch would spend UTC ticket 3 on `PEAK_MZ_TOL=0.02`.
