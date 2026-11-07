# Analysis 2026-11-07_cycle03 — why MRR is stuck and what to change

Competition day: **2026-11-07** (anchor 01:00 America/Chicago / CST). Triggered **2026-11-07T12:01Z** (06:01 CST). Cycle **03** of 5.

## Quota check (do not submit if 5 already used)

This Cloud Agent pod has **no** `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN` in the environment (same class of gap as earlier cloud cycles). `~/.kaggle/kaggle.json` could not be written from secrets. Direct `kaggle competitions submissions` is therefore unavailable here.

Quota inferred from GitHub Actions `casmi-loop` (which *does* hold Kaggle secrets):

| Run | Started (UTC) | Slot | Kaggle count at start | Submit |
|-----|---------------|------|------------------------|--------|
| [42330089426](https://github.com/ilakkmanoharan/casmi26-structure-prediction/actions/runs/42330089426) | 2026-11-07T02:36Z | 1 | local=0 kaggle=0 | **58076904** `2026-11-07_cycle01 H-top-peaks` kernel v202 |
| [42361044458](https://github.com/ilakkmanoharan/casmi26-structure-prediction/actions/runs/42361044458) | 2026-11-07T09:45Z | 2 | local=1 kaggle=1 | **58088101** `2026-11-07_cycle02 H-peak-mz` kernel v203 |

Newest Kaggle rows logged at cycle02 start:

- id=58076904 score=None status=COMPLETE desc=`2026-11-07_cycle01 H-top-peaks`
- id=58071327 score=None status=COMPLETE desc=`2026-11-06_cycle04 H-peaks`
- id=58065731 score=None status=COMPLETE desc=`2026-11-06_cycle03 H-peak-mz`
- id=58055178 score=None status=COMPLETE desc=`2026-11-06_cycle02 H-peak-mz`
- id=58042294 score=None status=COMPLETE desc=`2026-11-06_cycle01 H-top-peaks`

**Used today:**

- Kaggle UTC calendar day (API reset): **2 / 5** after cycle02 (58076904 at 02:53Z + 58088101 at 10:02Z).
- Chicago 01:00 clock: cycle01 is **before** 07:00Z / 01:00 CST; cycle02 is after. Chicago-clock count **1 / 5** (or 2 if counting the UTC-tagged cycle01 row).

**Quota is not exhausted.** Remaining slots: at least 3. This cycle proceeds as `2026-11-07_cycle03`.

## Public leaderboard context

- Our last **scored** public MRR@25 remains **0.143** (`agent/state.json` `best_public_score`). Recent code submits still show `publicScore=None` in Actions logs (scoring lag or identical predictions).
- Independent Oct 2026 snapshot of the live public LB: **pikachu 0.499**, Oleksandr Parfionov / CHU1PC **0.495** ([cubres README](https://github.com/cubres/enveda-casmi-2026/blob/main/README.md)). Gap to top is ~0.35, not a 0.01 tuning problem.
- Top public methods mix analog-shifted library search, large candidate DBs, and learned rankers. Our kernel is still **mass-window retrieval + hybrid entropy/modcos** on train libraries only.

## Why score is low (evidence)

1. **Poisoned exact duplicates (v0.1 failure mode, still in force).** Exact test↔train spectra in `enveda-180` carry train labels ≠ competition GT. Perfect library match ranked the *wrong* SMILES #1 and capped public MRR near 0.143. `EXCLUDE_EXACT_DUPLICATES=True` is already on; that only *removes* those IKs — it does not create a better #1 from non-identical evidence.
2. **Recent slots were no-ops.** `config.py` already has `TOP_PEAKS=128` and `PEAK_MZ_TOL=0.02`. Cycle01 re-applied 128; cycle02 re-applied 0.02. Kernel versions 202–203 did not change scoring behavior.
3. **Precursor ions still dominate similarity.** `clean_spectrum` kept peaks up to precursor **+2 Da**. Every isobar in the 35 ppm mass window shares that precursor (and nearby isotopes). Entropy and modified cosine then look more similar than the fragment ladder justifies. ms_entropy explicitly warns that *not* cutting at precursor−1.6 Da hurts identification.
4. **`MIN_SIMILARITY=0.05` is far below the Li 2021 0.75 FDR gate**, so weak matches fill the 25 slots after the true hit is missed or poisoned. Not this slot’s knob.

## Concrete improvement for this slot

**One major factor:** strip precursor-window ions (`m/z > precursor − 1.6 Da`) on index **and** query, matching Flash Entropy / ms_entropy.

Keep entropy weight 0.75, peak m/z 0.02, top peaks 128, exact-dup ban. Do not also retune mass ppm or min similarity in the same kernel.

Expected direction: **up** if wrong isobars were riding shared precursor peaks; **flat/down** if many true hits are precursor-only spectra that drop below 3 peaks and leave the index. Failure mode is recorded in the hypothesis file.

## Cloud submit path

`write_kaggle_credentials()` returned **False** in this pod (no `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN`). `kaggle kernels push` was not authenticated. Implement + rebuild `kaggle_kernel/` here; `casmi-loop` (hourly UTC, secrets present) should `kernels push` + `competition_submit_code` using these pre-written docs (they exceed the orchestrator’s “substantial” threshold). Do not CSV-submit.
