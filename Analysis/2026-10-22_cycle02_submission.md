# Analysis — 2026-10-22 cycle02

## Clock and quota

- Trigger: Cursor Cloud Automation cron `0 6 * * *` at **2026-10-22T06:00:17Z**.
- Chicago competition day **2026-10-22** starts **01:00 CDT = 06:00 UTC**.
- Cloud env has **no** `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN` (confirmed empty before any CLI call). `~/.kaggle/kaggle.json` was **not** written. Direct `kernels push` / `competition_submit_code` is impossible from this runner.
- Actions *does* have those secrets. UTC-day quota (Kaggle midnight reset, what Actions `competition_day()` counts):

| UTC slot | When (UTC) | Kaggle id | Kernel | Hypothesis | Live change? |
|----------|------------|-----------|--------|------------|--------------|
| 1 | 04:08Z (Actions 39719156929) | **57508910** | v134 | H-top-peaks | No (`TOP_PEAKS` already 128) |
| 2–5 | unused | — | — | would be H-entropy / H-intensity / H-peaks / H-domain | H-entropy and H-intensity already live |

- Chicago-clock submits since 01:00 CDT: **0/5** at this trigger (the Actions ticket landed *before* 06:00 UTC, so it still sits on Chicago day 2026-10-21).
- Combined: **do not skip for quota**. Remaining Kaggle UTC tickets today: **4/5**. This Cloud cycle is **cycle02** (next unused tag).

## Public scores

- Our best scored public MRR@25 remains **0.143** (v0.1). Later code submits list `publicScore=None` while pending/unscored in the CLI dump Actions recorded.
- Actions cycle01 briefing (04:08Z) newest-first:

  - 57508910 score=None COMPLETE `2026-10-22_cycle01 H-top-peaks`
  - 57499982 score=None COMPLETE `2026-10-21_cycle05 H-domain`
  - 57494907 score=None COMPLETE `2026-10-21_cycle04 H-peaks`
  - 57487491 score=None COMPLETE `2026-10-21_cycle03 H-intensity`
  - 57475663 score=None COMPLETE `2026-10-21_cycle02 H-entropy`
  - 57464825 score=None COMPLETE `2026-10-21_cycle01 H-top-peaks`

- Public LB context (CLIST snapshot fetched this run; official Kaggle page rate-limited): **pikachu 0.50**, Oleksandr Parfionov 0.50, CHU1PC 0.50, MarvinTMB 0.48, Oliver Ford 0.48. Community analog/forward notebooks historically ~0.43–0.46. Gap vs us: **~0.36**.

## Why the score is still low

1. **Poisoned exact duplicates (v0.1 failure).** Exact test↔train spectrum copies exist in `enveda-180` whose train labels ≠ competition GT. A perfect library hit ranks the wrong SMILES #1. `EXCLUDE_EXACT_DUPLICATES=True` is live; it does not recover Class-3 or missing-structure cases.
2. **Retrieval-only ceiling.** Rank-25 library search cannot invent a structure that is absent or whose only evidence is a poisoned row. Do not claim Class-3 de novo is solved.
3. **Slot rotation has been a no-op for weeks.** Live main after Actions 10-22 cycle01: `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, mass-wide 35/80, `TOP_K=120`, `MIN_SIMILARITY=0.05`, **`PEAK_MZ_TOL=0.01`**. Replaying H-entropy / H-intensity / H-domain does not change peak pairing.
4. **10 mDa fragment window is tighter than the literature default.** Flash Entropy and ms_entropy default to **20 mDa**. A 15 mDa CE / calibration / instrument shift currently fails `_greedy_match` and contributes 0 to entropy and modified cosine.

## What to change next (this slot)

Implement **one** major ablation: `PEAK_MZ_TOL` **0.01 → 0.02**.

Also retarget Actions **slot-2** fallback from H-entropy (already live) to **H-peak-mz**, and write substantial cycle02 docs so `write_cycle_docs` reuses this `config_patch` if the PR reaches main before the next unused hourly (`~07:00 UTC`).

If this PR is **not** merged before that slot, Actions will spend UTC ticket 2 on `ENTROPY_WEIGHT=0.75` — a second no-op today.

## Cloud submit status

- `kaggle kernels push` / `competition_submit_code`: **skipped** (`cloud_missing_kaggle_secrets`).
- Do **not** CSV-submit.
- Kernel metadata stays `enable_internet: false`; RDKit from `ilakkmanoharan/rdkit-cp312-wheels-casmi26`.
