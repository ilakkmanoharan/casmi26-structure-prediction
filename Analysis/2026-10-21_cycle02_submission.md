# Analysis — 2026-10-21 cycle02

## Clock and quota

- Trigger: Cursor Cloud Automation cron `0 6 * * *` at **2026-10-21T06:00:22Z**.
- Chicago competition day **2026-10-21** starts **01:00 CDT = 06:00 UTC**.
- Cloud env has **no** `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN` (confirmed empty before any CLI call). `~/.kaggle/kaggle.json` was **not** written. Kaggle CLI 2.2.4 requires `KAGGLE_API_TOKEN` or `~/.kaggle/access_token`. Direct `kernels push` / `competition_submit_code` is impossible from this runner.
- Actions *does* have those secrets. UTC-day quota (Kaggle midnight reset, what Actions `competition_day()` counts):

| UTC slot | When (UTC) | Kaggle id | Kernel | Hypothesis | Live change? |
|----------|------------|-----------|--------|------------|--------------|
| 1 | 04:08Z (Actions 39540912374) | **57464825** | v129 | H-top-peaks | No (`TOP_PEAKS` already 128) |
| 2–5 | unused | — | — | would be H-entropy / H-intensity / H-peaks / H-domain | H-entropy and H-intensity already live |

- Chicago-clock submits since 01:00 CDT: **0/5** at this trigger (the UTC ticket landed at 04:08Z = 23:08 CDT Oct 20, *before* 06:00 UTC).
- Combined: **do not skip for quota**. Remaining Kaggle UTC tickets today: **4/5**. Remaining Chicago-clock tickets: **5/5**. This Cloud cycle is **cycle02** (next unused tag after Actions' 2026-10-21_cycle01 files).

## Public scores

- Our best scored public MRR@25 remains **0.143** (v0.1). Later code submits list `publicScore=None` in the CLI dumps Actions recorded.
- Actions cycle01 briefing / `agent/state.json` newest-first:

  - 57464825 score=None COMPLETE `2026-10-21_cycle01 H-top-peaks`
  - 57455748 score=None COMPLETE `2026-10-20_cycle05 H-domain`
  - 57450775 score=None COMPLETE `2026-10-20_cycle04 H-peaks`
  - 57442950 score=None COMPLETE `2026-10-20_cycle03 H-intensity`
  - 57433041 score=None COMPLETE `2026-10-20_cycle02 H-entropy`
  - 57421540 score=None COMPLETE `2026-10-20_cycle01 H-top-peaks`

- Public LB (Kaggle, fetched 2026-10-21T06:02Z): **CHU1PC 0.495**, pikachu 0.495, Oleksandr Parfionov 0.493, MarvinTMB 0.484, Oliver Ford 0.482. ~3713 teams. Community analog/evidence notebooks historically ~0.43–0.46. Gap vs us: **~0.35**.

## Why the score is still low

1. **Poisoned exact duplicates (v0.1 failure).** Exact test↔train spectrum copies exist in `enveda-180` whose train labels ≠ competition GT. A perfect library hit ranks the wrong SMILES #1. `EXCLUDE_EXACT_DUPLICATES=True` is live; it does not recover Class-3 or missing-structure cases.
2. **Retrieval-only ceiling.** Rank-25 library search cannot invent a structure that is absent or whose only evidence is a poisoned row. Do not claim Class-3 de novo is solved.
3. **Slot rotation has been a no-op for weeks.** Live main after Actions 10-21 cycle01: `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, mass-wide 35/80, `TOP_K=120`, `MIN_SIMILARITY=0.05`, **`PEAK_MZ_TOL=0.01`**. Replaying H-entropy / H-intensity / H-domain does not change peak pairing.
4. **10 mDa fragment window is tighter than the literature default.** Flash Entropy and matchms FlashSimilarity match fragments at **20 mDa**. Hidden test is Bruker timsTOF; train mixes instruments and CEs. Ions off by 11–20 mDa currently fail `_greedy_match` and contribute 0 to entropy/modcos.

## What to change next (this slot)

Implement **one** major ablation: `PEAK_MZ_TOL` **0.01 → 0.02**.

Also retarget Actions **slot-2** fallback from H-entropy (already live) to **H-peak-mz**, and write substantial cycle02 docs so `write_cycle_docs` reuses this `config_patch` if the PR reaches main before the next unused hourly (`~07:00 UTC`).

If this PR is **not** merged before that slot, Actions will spend UTC ticket 2 on `ENTROPY_WEIGHT=0.75` — a second no-op today.

## Cloud submit status

- `kaggle kernels push` / `competition_submit_code`: **skipped** (`cloud_missing_kaggle_secrets`).
- Do **not** CSV-submit.
- Kernel metadata stays `enable_internet: false`; RDKit from `ilakkmanoharan/rdkit-cp312-wheels-casmi26`.
