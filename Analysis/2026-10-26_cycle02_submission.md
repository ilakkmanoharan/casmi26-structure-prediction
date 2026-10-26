# Analysis — 2026-10-26 cycle02

## Clock and quota

- Trigger: Cursor Cloud Automation cron `0 6 * * *` at **2026-10-26T06:02:43Z**.
- Chicago competition day **2026-10-26** starts **01:00 CDT = 06:00 UTC**.
- Cloud env has **no** `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN` (confirmed empty `printenv` before any CLI call). `~/.kaggle/kaggle.json` was **not** written. Direct `kernels push` / `competition_submit_code` is impossible from this runner.
- Actions *does* have those secrets. UTC-day quota (Kaggle midnight reset, what Actions `competition_day()` counts):

| UTC slot | When (UTC) | Kaggle id | Kernel | Hypothesis | Live change? |
|----------|------------|-----------|--------|------------|--------------|
| 1 | ~04:06Z (Actions [40266236098](https://github.com/ilakkmanoharan/casmi26-structure-prediction/actions/runs/40266236098)) | **57652978** | v154 | H-top-peaks | No (`TOP_PEAKS` already 128) |
| 2–5 | unused | — | — | would be H-peak-mz / H-peak-mz / H-peaks / H-domain | H-peak-mz **already live** (`PEAK_MZ_TOL=0.02`) |

- Chicago-clock submits since 01:00 CDT: **0/5** at this trigger (the Actions ticket landed at 04:06Z, *before* 06:00 UTC).
- Combined: **do not skip for quota**. Remaining Kaggle UTC tickets today: **4/5**. This Cloud cycle is **cycle02** (next unused tag). Cycle01 docs/state already exist from the UTC-day Actions run.

## Public scores

- Our best scored public MRR@25 remains **0.143** (v0.1). Later code submits list `publicScore=None` while pending/unscored in the CLI dump Actions recorded.
- Actions cycle01 briefing (04:06Z) newest-first:

  - 57642549 score=None COMPLETE `2026-10-25_cycle05 H-domain`
  - 57638558 score=None COMPLETE `2026-10-25_cycle04 H-peaks`
  - 57631300 score=None COMPLETE `2026-10-25_cycle03 H-peak-mz`
  - 57621786 score=None COMPLETE `2026-10-25_cycle02 H-peak-mz`
  - 57612600 score=None COMPLETE `2026-10-25_cycle01 H-top-peaks`

  After that run, Kaggle id **57652978** is `2026-10-26_cycle01 H-top-peaks` (PENDING at submit time).

- Official public LB (fetched 2026-10-26T06:10Z): **Oleksandr Parfionov 0.504**, Savko 0.503, pikachu 0.499, Shehab Alshehabi 0.495, CHU1PC 0.495, Paweł Biernat 0.490, JJ 0.489. CLIST rounds the same cluster to **0.50 / 0.49 / 0.48**. Community analog notebooks historically ~0.43–0.46. Gap vs us: **~0.36**.

## Why the score is still low

1. **Poisoned exact duplicates (v0.1 failure).** Exact test↔train spectrum copies exist in `enveda-180` whose train labels ≠ competition GT. A perfect library hit ranks the wrong SMILES #1. `EXCLUDE_EXACT_DUPLICATES=True` is live; it does not recover Class-3 or missing-structure cases.
2. **Retrieval-only ceiling.** Rank-25 library search cannot invent a structure that is absent or whose only evidence is a poisoned row. Do not claim Class-3 de novo is solved.
3. **Slot rotation is about to waste tickets again.** Live main after Actions 10-26 cycle01: `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, mass-wide 35/80, `MIN_SIMILARITY=0.05`, **`PEAK_MZ_TOL=0.02`**. Slot-2 and slot-3 fallbacks are both `{"PEAK_MZ_TOL": 0.02}` — already live. Yesterday Actions burned *two* UTC tickets (cycle02 + cycle03) on that no-op.
4. **Admission floor is too low.** `retrieve.py` keeps every hybrid entropy/modcos hit with `sim >= 0.05` up to `TOP_K_SPECTRA_PER_QUERY=120`. Li/Fiehn identity work puts acceptable FDR near **0.75**; analog search can sit lower, but 0.05 still packs the ranker with fragment-overlap noise and dilutes `mean_top_k_similarity` / `support_log` / the 25-candidate list.

## What to change next (this slot)

Implement **one** major ablation: `MIN_SIMILARITY` **0.05 → 0.12**.

Also retarget Actions **slot-2** fallback from H-peak-mz (already live) to **H-min-sim**, and **slot-3** from the second H-peak-mz copy to **H-peaks** (`TOP_PEAKS=160`). Write substantial cycle02 docs so `write_cycle_docs` reuses this `config_patch` if the PR reaches main before the next unused hourly (`~07:00 UTC`).

If this PR is **not** merged before that slot, Actions will spend UTC ticket 2 on `PEAK_MZ_TOL=0.02` — a second no-op today, same failure as 2026-10-25 cycle02/03.

## Cloud submit status

- `kaggle kernels push` / `competition_submit_code`: **skipped** (`cloud_missing_kaggle_secrets`).
- Do **not** CSV-submit.
- Kernel metadata stays `enable_internet: false`; RDKit from `ilakkmanoharan/rdkit-cp312-wheels-casmi26`.
