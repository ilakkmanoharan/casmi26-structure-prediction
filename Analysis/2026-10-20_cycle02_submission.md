# Analysis — 2026-10-20 cycle02

## Clock and quota

- Trigger: Cursor Cloud Automation cron `0 6 * * *` at **2026-10-20T06:00:50Z**.
- Chicago competition day **2026-10-20** starts **01:00 CDT = 06:00 UTC**.
- Cloud env has **no** `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN` (confirmed empty before any CLI call). `write_kaggle_credentials()` returned **False**. `~/.kaggle/kaggle.json` was **not** written. Direct `kernels push` / `competition_submit_code` is impossible from this runner.
- Actions *does* have those secrets. UTC-day quota (Kaggle midnight reset, what Actions `competition_day()` counts):

| UTC slot | When (UTC) | Kaggle id | Kernel | Hypothesis | Live change? |
|----------|------------|-----------|--------|------------|--------------|
| 1 | 04:18Z (Actions 39367460297) | **57421540** | v124 | H-top-peaks | No (`TOP_PEAKS` already 128) |
| 2–5 | unused | — | — | would be H-entropy / H-intensity / H-peaks / H-domain | H-entropy and H-intensity already live |

- Chicago-clock submits since 01:00 CDT: **0/5** at this trigger (the UTC slot-1 ticket landed at 04:18Z, *before* 06:00 UTC).
- Combined: **do not skip for quota**. Remaining Kaggle UTC tickets today: **4/5**. This Cloud cycle is **cycle02** (next unused tag; cycle01 docs already exist from Actions).

## Public scores

- Our best scored public MRR@25 remains **0.143** (v0.1). Later code submits list `publicScore=None` while pending/unscored in the CLI dump Actions recorded.
- Actions cycle01 briefing (04:18Z) newest-first:

  - 57421540 score=None COMPLETE `2026-10-20_cycle01 H-top-peaks`
  - 57412696 score=None COMPLETE `2026-10-19_cycle05 H-domain`
  - 57407066 score=None COMPLETE `2026-10-19_cycle04 H-peaks`
  - 57396819 score=None COMPLETE `2026-10-19_cycle03 H-intensity`
  - 57385301 score=None COMPLETE `2026-10-19_cycle02 H-entropy`
  - 57376181 score=None COMPLETE `2026-10-19_cycle01 H-top-peaks`
  - 57364413 score=None COMPLETE `2026-10-18_cycle05 H-domain`
  - 57358116 score=None COMPLETE `2026-10-18_cycle04 H-peaks`
  - 57351264 score=None COMPLETE `2026-10-18_cycle03 grok-docs`
  - 57341340 score=None COMPLETE `2026-10-18_cycle02 H-entropy`

- Public LB (Kaggle page ~2026-10-20T06:00Z): **CHU1PC 0.495**, pikachu 0.495, Oleksandr Parfionov 0.493, MarvinTMB 0.484, Oliver Ford 0.482. Community analog/forward notebooks historically ~0.32–0.42. Gap vs us: **~0.35**.

## Why the score is still low

1. **Poisoned exact duplicates (v0.1 failure).** Exact test↔train spectrum copies exist in `enveda-180` whose train labels ≠ competition GT. A perfect library hit ranks the wrong SMILES #1. `EXCLUDE_EXACT_DUPLICATES=True` is live; it does not recover Class-3 or missing-structure cases.
2. **Retrieval-only ceiling.** Rank-25 library search cannot invent a structure that is absent or whose only evidence is a poisoned row. Do not claim Class-3 de novo is solved.
3. **Slot rotation has been a no-op for weeks.** Live main after Actions 10-20 cycle01: `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, mass-wide 35/80, `TOP_K=120`, `MIN_SIMILARITY=0.05`, **`PEAK_MZ_TOL=0.01`**. Replaying H-entropy / H-intensity / H-domain does not change scoring.
4. **10 mDa fragment window is tighter than the literature default.** Flash Entropy matches fragments at **20 mDa**. CE / instrument / centroid error near 10–15 mDa currently fails `_greedy_match`, so true hits lose entropy and modified-cosine credit.

## What to change next (this slot)

Implement **one** major ablation: `PEAK_MZ_TOL` **0.01 → 0.02**.

Also retarget Actions **slot-2** fallback from H-entropy (already live) to **H-peak-mz**, and write substantial cycle02 docs so `write_cycle_docs` reuses this `config_patch` if the PR reaches main before the next unused hourly (`~07:00 UTC`).

If this PR is **not** merged before that slot, Actions will spend UTC ticket 2 on `ENTROPY_WEIGHT=0.75` — a second no-op today.

## Cloud submit status

- `kaggle kernels push` / `competition_submit_code`: **skipped** (`cloud_missing_kaggle_secrets`).
- Do **not** CSV-submit.
- Kernel metadata stays `enable_internet: false`; RDKit from `ilakkmanoharan/rdkit-cp312-wheels-casmi26`.
