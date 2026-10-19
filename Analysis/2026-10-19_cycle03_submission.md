# Analysis — 2026-10-19 cycle03

## Clock and quota

- Trigger: Cursor Cloud Automation cron `0 6 * * *` at **2026-10-19T06:02:27Z**.
- Chicago competition day **2026-10-19** starts **01:00 CDT = 06:00 UTC**.
- Cloud env has **no** `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN` (confirmed empty before any CLI call). `~/.kaggle/kaggle.json` was **not** written. Direct `kernels push` / `competition_submit_code` is impossible from this runner.
- Actions *does* have those secrets. UTC-day quota (Kaggle midnight reset, what Actions `competition_day()` counts):

| UTC slot | When (UTC) | Kaggle id | Kernel | Hypothesis | Live change? |
|----------|------------|-----------|--------|------------|--------------|
| 1 | 01:14Z (Actions 39182970206) | **57376181** | v119 | H-top-peaks | No (`TOP_PEAKS` already 128) |
| 2 | 06:12Z (Actions 39206929458, started 05:54Z) | **57385301** | v120 | H-entropy | No (`ENTROPY_WEIGHT` already 0.75) |
| 3–5 | unused | — | — | would be H-intensity / H-peaks / H-domain | H-intensity also already live |

- Chicago-clock submits since 01:00 CDT: **1/5** (slot 1 at 01:14Z is still Chicago Oct 18; slot 2 **submitted** at 06:12Z = 01:12 CDT, after the Chicago day anchor).
- Combined: **do not skip for quota**. Remaining Kaggle UTC tickets today: **3/5**. This Cloud cycle is **cycle03** (next unused tag).

## Public scores

- Our best scored public MRR@25 remains **0.143** (v0.1). Later code submits list `publicScore=None` while pending/unscored in the CLI dump Actions recorded.
- Actions cycle01 briefing (01:14Z) newest-first from committed Analysis:

  - 57364413 score=None COMPLETE `2026-10-18_cycle05 H-domain`
  - 57358116 score=None COMPLETE `2026-10-18_cycle04 H-peaks`
  - 57351264 score=None COMPLETE `2026-10-18_cycle03 grok-docs`
  - 57341340 score=None COMPLETE `2026-10-18_cycle02 H-entropy`
  - 57332661 score=None COMPLETE `2026-10-18_cycle01 H-top-peaks`

- Then from `agent/state.json` after Actions 39206929458 finished: 57376181 `2026-10-19_cycle01 H-top-peaks` (kernel v119); **57385301** `2026-10-19_cycle02 H-entropy` (kernel v120).
- Public LB (CLIST fetched this run): **CHU1PC 0.50**, pikachu 0.50, Oleksandr Parfionov 0.49, MarvinTMB 0.48, Oliver Ford 0.47. Community analog/forward notebooks historically ~0.32–0.42. Gap vs us: **~0.36**.

## Why the score is still low

1. **Poisoned exact duplicates (v0.1 failure).** Exact test↔train spectrum copies exist in `enveda-180` whose train labels ≠ competition GT. A perfect library hit ranks the wrong SMILES #1. `EXCLUDE_EXACT_DUPLICATES=True` is live; it does not recover Class-3 or missing-structure cases.
2. **Retrieval-only ceiling.** Rank-25 library search cannot invent a structure that is absent or whose only evidence is a poisoned row. Do not claim Class-3 de novo is solved.
3. **Slot rotation has been a no-op for weeks.** Live main after Actions 10-19 cycle01: `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, mass-wide 35/80, `TOP_K=120`, `MIN_SIMILARITY=0.05`, `INTENSITY_FLOOR=0.01`, **`PEAK_MZ_TOL=0.01`**. Replaying H-entropy / H-intensity / H-domain does not change peak pairing.
4. **10 mDa fragment window is tighter than Flash Entropy.** Li/Fiehn match fragments at **20 mDa**; ms_entropy defaults `ms2_tolerance_in_da=0.02`. A 10 mDa cut drops true pairs in the 10–20 mDa jitter band (CE / centroid / library calibration), which lowers both entropy and modified cosine for the correct structure.

## What to change next (this slot)

Implement **one** major ablation: `PEAK_MZ_TOL` **0.01 → 0.02**.

Also retarget Actions **slot-3** fallback from H-intensity (already live) to **H-peak-mz**, and write substantial cycle03 docs so `write_cycle_docs` reuses this `config_patch` if the PR reaches main before the next unused hourly (`~07:00 UTC`).

If this PR is **not** merged before that slot, Actions will spend UTC ticket 3 on `INTENSITY_FLOOR=0.01` — a third no-op today.

## Cloud submit status

- `kaggle kernels push` / `competition_submit_code`: **skipped** (`cloud_missing_kaggle_secrets`).
- Do **not** CSV-submit.
- Kernel metadata stays `enable_internet: false`; RDKit from `ilakkmanoharan/rdkit-cp312-wheels-casmi26`.
