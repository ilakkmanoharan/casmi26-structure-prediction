# Analysis — 2026-09-29 cycle02

## Clock and quota (checked 2026-09-29T06:02Z / 01:02 CDT)

Competition day starts **01:00 America/Chicago**. This Cloud Automation is the first Chicago-day slot.

| Clock | Submits counting toward limit | Remaining |
|-------|-------------------------------|-----------|
| Chicago 01:00 (CLOUD_CYCLE_PROMPT) | **0 / 5** | 5 |
| UTC calendar (Kaggle reset + Actions `competition_day()`) | **1 / 5** | 4 |

Quota is **not** exhausted. Do not exit.

UTC slot 1 already ran: GitHub Actions [36508585186](https://github.com/ilakkmanoharan/casmi26-structure-prediction/actions/runs/36508585186) at 02:00Z (21:00 CDT 09-28) → Kaggle **56659366**, kernel v32, `2026-09-29_cycle01 H-top-peaks` (`TOP_PEAKS=128`). That timestamp is **before** 01:00 CDT, so it belongs to the previous Chicago day even though Actions tagged it 2026-09-29.

## Kaggle CLI from this Cloud pod

`KAGGLE_USERNAME`, `KAGGLE_KEY`, and `KAGGLE_API_TOKEN` are **absent** (same failure as Cloud cycles 2026-09-18…09-28). `write_kaggle_credentials()` returned False; `~/.kaggle/kaggle.json` was not written. **No `kaggle kernels push` and no `competition_submit_code` from this pod.** Counts below are from Actions logs + committed `agent/state.json` + the **public** leaderboard. No secret values.

## Recent submissions (from Actions 36508585186 list + `agent/state.json`)

Newest first; **publicScore is null on every recent row** (Kaggle has not published scores for these code submits, or they are still pending).

| id | desc | kernel | when (UTC) |
|----|------|--------|------------|
| 56659366 | 2026-09-29_cycle01 H-top-peaks | v32 | 2026-09-29 02:00 |
| 56653270 | 2026-09-28_cycle04 H-peaks | v31 | 2026-09-28 22:04 |
| 56645352 | 2026-09-28_cycle03 H-mass-wide | v30 | 2026-09-28 15:30 |
| 56632216 | 2026-09-28_cycle02 H-entropy | v29 | 2026-09-28 06:50 |
| 56624265 | 2026-09-28_cycle01 H-top-peaks | v28 | 2026-09-28 00:47 |
| 56620606 | 2026-09-27_cycle05 H-domain | v27 | 2026-09-27 22:18 |

Best **scored** public result we own is still **0.143** (v0.1, 2026-09-15). All later kernels are unscored in our records.

## Public leaderboard (fetched 2026-09-29T06:02Z)

https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra/leaderboard

| Rank | Team | Public MRR@25 |
|------|------|----------------|
| 1 | pikachu | **0.440** |
| 2 | Ozymandias31415 | 0.425 |
| 3 | Udam Liyanage | 0.414 |
| 4 | Randy | 0.411 |
| 5 | Komil Parmar | 0.409 |

Gap vs our scored 0.143 is **~3×**. Public code notebooks in the analog / multi-channel family report ~0.23–0.34 (Analog Propagation 0.335; Four-Channel Ranker 0.333; community analog ranker 0.236). Those use extra candidate DBs and fingerprint models we do not ship in this internet-off kernel.

## Why score is low (evidence, unchanged root cause)

1. **Poisoned exact duplicates (v0.1 diagnostics).** Every molecule had rank-1 `best_similarity = 1.0` on an `enveda-180` row whose train InChIKey14 ≠ competition GT. Perfect library match ⇒ MRR 0.143 ⇒ ~86% of those labels are wrong. `EXCLUDE_EXACT_DUPLICATES=True` is on; we must not re-trust those IKs.

2. **Daily fallbacks no longer change the live scorer.** Main already has `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, `MASS_TOL_PPM=35` / backfill 80, `TOP_K=120`, `MIN_SIMILARITY=0.05`. Slot 1–4 fallbacks are near no-ops. Slot 5 `H-domain` boosts priors that are already 1.0 / 1.0 / 0.85.

3. **Cleaning is looser than the entropy papers we cite.** `INTENSITY_FLOOR=0.001` keeps peaks at 0.1% of base intensity. Li/Fiehn and `msentropy.clean_spectrum` use **1%**. The 25% modified-cosine term in the hybrid is noise-sensitive; leftover ions also steal slots in the 128-peak ladder.

4. **Library / chemistry mismatch.** `enveda-180` is synthetic drug-like; test is NP-like. Domain priors cannot fix wrong structures.

5. **No analog / formula channel.** Leaders and public 0.33 notebooks add fingerprint / candidate-DB rankers. Retrieval-only cannot claim Class-3 de novo.

## Concrete improvement for this slot

**One major factor:** `INTENSITY_FLOOR` 0.001 → **0.01**. Unused in the fallback rotation. Scientifically aligned with entropy cleaning. Does not repeat H-min-sim Cloud PRs #11/#12 (still draft, never merged).

If this Cloud pod cannot `kernels push`, retarget Actions slot-2 fallback to the same patch so the next hourly `casmi-loop` (07:00Z) can `competition_submit_code` after this PR lands on main.

## Do not do this slot

Another `TOP_PEAKS` / `ENTROPY_WEIGHT` / mass-window sweep. CSV submit. Claiming retrieval solves Class-3.
