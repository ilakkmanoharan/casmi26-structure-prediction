# Analysis — 2026-10-11 cycle02

## Quota (re-checked 2026-10-11T06:05Z)

Competition day starts **01:00 America/Chicago**. Wall clock at this Cloud run: **2026-10-11 01:05 CDT**.

| Clock | Submits counted | Slots left | Notes |
|-------|-----------------|------------|-------|
| **Chicago 01:00** (CLOUD_CYCLE_PROMPT) | **0 / 5** | 5 | Actions 38102538649 → Kaggle **57058992** (kernel v83, H-top-peaks) started 01:39Z / recorded 02:00Z = **21:00 CDT Oct 10**, *before* today's 01:00 CDT reset |
| **UTC calendar** (Actions `competition_day()` / Kaggle reset) | **1 / 5** | 4 | Same 57058992 already on the UTC Oct 11 ledger |

Could **not** call `kaggle competitions submissions` from this Cloud VM: `KAGGLE_USERNAME`, `KAGGLE_KEY`, and `KAGGLE_API_TOKEN` are absent from the process environment (same Cloud failure as 2026-09-25…2026-10-10). Count above is from `agent/state.json` + `gh run list` for `casmi-loop`. **Not quota-exhausted — do not exit.**

## Leaderboard / score context

- Our **best scored public MRR@25** remains **0.143** (v0.1). Later code submits (57026616 … 57058992) still show `publicScore=None` in the Actions briefing — scoring lag, not a new number.
- CLIST prize table (fetched this cycle): **MarvinTMB 0.48**, **pikachu 0.48**, Kucing Garong 0.47, then a 0.46 pack (CHU1PC, Oliver Ford, David Zapata, Sho Saga, vukpetar, Yuuki Aikawa). Gap to top is still ~0.34.  
  https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/

## Recent submissions (from 2026-10-11_cycle01 Analysis + state)

- 57058992 COMPLETE — 2026-10-11_cycle01 H-top-peaks (`TOP_PEAKS=128`) — UTC day, pre-Chicago
- 57053929 COMPLETE — 2026-10-10_cycle05 H-domain
- 57050636 COMPLETE — 2026-10-10_cycle04 H-peaks
- 57043905 COMPLETE — 2026-10-10_cycle03 H-mass-wide
- 57034605 COMPLETE — 2026-10-10_cycle02 H-entropy
- 57026616 COMPLETE — 2026-10-10_cycle01 H-top-peaks

Actions fallbacks have been rotating the **same five already-live knobs**. Live main after cycle01: `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, `MASS_TOL_PPM=35`, `MASS_TOL_PPM_BACKFILL=80`, `TOP_K_SPECTRA_PER_QUERY=120`, `MIN_SIMILARITY=0.05`, **`INTENSITY_FLOOR=0.001`**, **`PEAK_MZ_TOL=0.01`**.

## Why the score is still low

1. **Poisoned exact dups** in `enveda-180`: test↔train spectrum identity with train labels ≠ competition GT. Exact-match retrieval scores 1.0 on the wrong InChIKey14 (v0.1 ~0.143). `EXCLUDE_EXACT_DUPLICATES` is on; that only unblocks the problem.
2. **No-op Actions slots.** Slot 2 (`ENTROPY_WEIGHT=0.75`) is already the live value. Another entropy submit cannot move MRR.
3. **Too-low intensity floor.** `clean_spectrum` keeps peaks at 0.1% of max. Flash Entropy / matchms treat those as noise. With `TOP_PEAKS=128` they occupy the fragment ladder, inflate entropy, and create chance matches to unrelated library spectra — exactly the failure mode that pushes wrong SMILES into the MRR@25 list.
4. Unmerged Cloud PRs (#13–#24) never landed `INTENSITY_FLOOR=0.01` or `PEAK_MZ_TOL=0.02` on main.

## What to change this slot

One major factor vs live main: **`INTENSITY_FLOOR` 0.001 → 0.01**. Retarget Actions slot-2 fallback to `H-intensity` so the next hourly `casmi-loop` submits this ablation instead of wasting UTC slot 2 on entropy 0.75.

If this Cloud VM still cannot `kernels push`, merge this PR before the next scheduled Actions hour (~07:00Z pattern).
