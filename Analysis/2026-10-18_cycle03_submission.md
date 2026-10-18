# Analysis — 2026-10-18 cycle03

## Clock and quota

- Trigger: Cursor Cloud Automation cron `0 6 * * *` at **2026-10-18T06:01:05Z**.
- Chicago competition day **2026-10-18** starts **01:00 CDT = 06:00 UTC**.
- Cloud env has **no** `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN` (confirmed empty before any CLI call). `~/.kaggle/kaggle.json` was **not** written. Direct `kernels push` / `competition_submit_code` is impossible from this runner.
- Actions *does* have those secrets. UTC-day quota (Kaggle midnight reset, what Actions `competition_day()` counts):

| UTC slot | When (UTC) | Kaggle id | Kernel | Hypothesis | Live change? |
|----------|------------|-----------|--------|------------|--------------|
| 1 | 01:06Z (Actions 39083766596) | **57332661** | v114 | H-top-peaks | No (`TOP_PEAKS` already 128) |
| 2 | 05:53Z (Actions 39100851291) | **57341340** | v115 | H-entropy | No (`ENTROPY_WEIGHT` already 0.75) |
| 3–5 | unused | — | — | would be H-mass-wide / H-peaks / H-domain | H-mass-wide also already live |

- Chicago-clock submits since 01:00 CDT: **0/5** at this trigger (both Actions tickets landed *before* 06:00 UTC).
- Combined: **do not skip for quota**. Remaining Kaggle UTC tickets today: **3/5**. This Cloud cycle is **cycle03** (next unused tag).

## Public scores

- Our best scored public MRR@25 remains **0.143** (v0.1). Later code submits list `publicScore=None` while pending/unscored in the CLI dump Actions recorded.
- Actions cycle02 briefing (05:53Z) newest-first:

  - 57332661 score=None COMPLETE `2026-10-18_cycle01 H-top-peaks`
  - 57323437 score=None COMPLETE `2026-10-17_cycle05 H-domain`
  - 57318257 score=None COMPLETE `2026-10-17_cycle04 H-peaks`
  - 57312187 score=None COMPLETE `2026-10-17_cycle03 H-mass-wide`
  - 57303658 score=None COMPLETE `2026-10-17_cycle02 H-entropy`

- Public LB context (CLIST snapshot used by prior Cloud notes; official Kaggle page rate-limited this run): **pikachu 0.50**, Oleksandr Parfionov 0.49, CHU1PC 0.49, MarvinTMB 0.48, Oliver Ford 0.47. Community analog/forward notebooks historically ~0.32–0.42. Gap vs us: **~0.36**.

## Why the score is still low

1. **Poisoned exact duplicates (v0.1 failure).** Exact test↔train spectrum copies exist in `enveda-180` whose train labels ≠ competition GT. A perfect library hit ranks the wrong SMILES #1. `EXCLUDE_EXACT_DUPLICATES=True` is live; it does not recover Class-3 or missing-structure cases.
2. **Retrieval-only ceiling.** Rank-25 library search cannot invent a structure that is absent or whose only evidence is a poisoned row. Do not claim Class-3 de novo is solved.
3. **Slot rotation has been a no-op for weeks.** Live main after Actions 10-18 cycle02: `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, mass-wide 35/80, `TOP_K=120`, `MIN_SIMILARITY=0.05`, `PEAK_MZ_TOL=0.01`, **`INTENSITY_FLOOR=0.001`**. Replaying H-entropy / H-mass-wide / H-domain does not change the spectrum object.
4. **0.1% intensity floor is too permissive vs literature.** Flash Entropy and ms_entropy default to a **1%** relative cut. Keeping 0.1–1% ions lets isolation-window noise contribute to entropy and modified-cosine, which inflates similarity for decoys and wastes the 128-peak ladder.

## What to change next (this slot)

Implement **one** major ablation: `INTENSITY_FLOOR` **0.001 → 0.01**.

Also retarget Actions **slot-3** fallback from H-mass-wide (already live) to **H-intensity**, and write substantial cycle03 docs so `write_cycle_docs` reuses this `config_patch` if the PR reaches main before the next unused hourly (`~07:00 UTC`).

If this PR is **not** merged before that slot, Actions will spend UTC ticket 3 on `MASS_TOL_PPM=35` / `MASS_TOL_PPM_BACKFILL=80` / `TOP_K=120` — a third no-op today.

## Cloud submit status

- `kaggle kernels push` / `competition_submit_code`: **skipped** (`cloud_missing_kaggle_secrets`).
- Do **not** CSV-submit.
- Kernel metadata stays `enable_internet: false`; RDKit from `ilakkmanoharan/rdkit-cp312-wheels-casmi26`.
