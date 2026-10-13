# Analysis — 2026-10-13 cycle02

## Quota (re-checked 2026-10-13T06:05Z)

Competition day starts **01:00 America/Chicago**. Wall clock at this Cloud run: **2026-10-13 01:05 CDT**.

| Clock | Submits counted | Slots left | Notes |
|-------|-----------------|------------|-------|
| **Chicago 01:00** (CLOUD_CYCLE_PROMPT) | **0 / 5** | 5 | Actions 38326601721 → Kaggle **57124847** (kernel v90, H-top-peaks) started 00:18Z / recorded 00:43Z = **19:43 CDT Oct 12**, *before* today's 01:00 CDT reset |
| **UTC calendar** (Actions `competition_day()` / Kaggle reset) | **1 / 5** | 4 | Same 57124847 already on the UTC Oct 13 ledger |

Could **not** call `kaggle competitions submissions` from this Cloud VM: `KAGGLE_USERNAME`, `KAGGLE_KEY`, and `KAGGLE_API_TOKEN` are absent from the process environment (same Cloud failure as 2026-09-25…2026-10-12). Count above is from `agent/state.json` + `gh run list` for `casmi-loop`. **Not quota-exhausted — do not exit.**

## Leaderboard / score context

- Our **best scored public MRR@25** remains **0.143** (v0.1). Later code submits (57090053 … 57124847) still show `publicScore=None` in the Actions briefing — scoring lag, not a new number.
- CLIST prize table (fetched 2026-10-13T06:05Z): **CHU1PC 0.49**, MarvinTMB 0.48, pikachu 0.48, Kucing Garong 0.47, then a 0.46 pack (JJ, Oliver Ford, Oleksandr Parfionov, David Zapata, vukpetar, Sho Saga). Gap to top is still ~0.35.  
  https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/

## Recent submissions (from 2026-10-13_cycle01 Analysis + state)

- 57124847 COMPLETE — 2026-10-13_cycle01 H-top-peaks (`TOP_PEAKS=128`) — UTC day, pre-Chicago
- 57114938 COMPLETE — 2026-10-12_cycle03 H-mass-wide
- 57099716 COMPLETE — 2026-10-12_cycle02 H-entropy
- 57090053 COMPLETE — 2026-10-12_cycle01 H-top-peaks
- 57084837 COMPLETE — 2026-10-11_cycle04 H-peaks
- 57078867 COMPLETE — 2026-10-11_cycle03 H-mass-wide
- 57068674 COMPLETE — 2026-10-11_cycle02 H-entropy
- 57058992 COMPLETE — 2026-10-11_cycle01 H-top-peaks

Actions fallbacks have been rotating the **same five already-live knobs**. Live main after cycle01: `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, `MASS_TOL_PPM=35`, `MASS_TOL_PPM_BACKFILL=80`, `TOP_K_SPECTRA_PER_QUERY=120`, `MIN_SIMILARITY=0.05`, **`INTENSITY_FLOOR=0.001`**, **`PEAK_MZ_TOL=0.01`**.

## Why the score is still low

1. **Poisoned exact dups** in `enveda-180`: test↔train spectrum identity with train labels ≠ competition GT. Exact-match retrieval scores 1.0 on the wrong InChIKey14 (v0.1 ~0.143). `EXCLUDE_EXACT_DUPLICATES` is on; that only unblocks the problem.
2. **No-op Actions slots.** Slot 2 (`ENTROPY_WEIGHT=0.75`) is already the live value. Another entropy submit cannot move MRR.
3. **Too-low intensity floor.** `clean_spectrum` keeps peaks at 0.1% of max. Flash Entropy / matchms treat those as noise. With `TOP_PEAKS=128` they occupy the fragment ladder, inflate entropy, and create chance matches to unrelated library spectra — exactly the failure mode that pushes wrong SMILES into the MRR@25 list.
4. Unmerged Cloud PRs (#13–#26) never landed `INTENSITY_FLOOR=0.01` or `PEAK_MZ_TOL=0.02` on main. Yesterday’s Cloud cycle02 (PR #26) retargeted slot 2 to H-peak-mz; it did not merge, so today’s Actions slot 2 will still waste a ticket on entropy 0.75 unless this PR lands first.

## What to change this slot

One major factor vs live main: **`INTENSITY_FLOOR` 0.001 → 0.01**. Retarget Actions slot-2 fallback to `H-intensity` so the next hourly `casmi-loop` submits this ablation instead of wasting UTC slot 2 on entropy 0.75.

If this Cloud VM still cannot `kernels push`, merge this PR before the next scheduled Actions hour (~07:00Z pattern).
