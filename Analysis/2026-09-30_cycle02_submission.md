# Analysis — 2026-09-30 cycle02

## Clock and quota (checked 2026-09-30T06:12Z / 01:12 CDT)

Competition day starts **01:00 America/Chicago**. This Cloud Automation is the first Chicago-day slot.

| Clock | Submits counting toward limit | Remaining |
|-------|-------------------------------|-----------|
| Chicago 01:00 (CLOUD_CYCLE_PROMPT) | **0 / 5** | 5 |
| UTC calendar (Kaggle reset + Actions `competition_day()`) | **1 / 5** | 4 |

Quota is **not** exhausted. Do not exit.

UTC slot 1 already ran: GitHub Actions [36648798697](https://github.com/ilakkmanoharan/casmi26-structure-prediction/actions/runs/36648798697) at 00:08Z (19:08 CDT 09-29) → Kaggle **56692019**, kernel v36, `2026-09-30_cycle01 H-top-peaks` (`TOP_PEAKS=128`). That timestamp is **before** 01:00 CDT, so it belongs to the previous Chicago day even though Actions tagged it 2026-09-30.

## Kaggle CLI from this Cloud pod

`KAGGLE_USERNAME`, `KAGGLE_KEY`, and `KAGGLE_API_TOKEN` are **absent** (same failure as Cloud cycles 2026-09-18…09-29). Environment scan found no Kaggle-related env vars and no `~/.kaggle/kaggle.json`. `write_kaggle_credentials()` cannot run. **No `kaggle kernels push` and no `competition_submit_code` from this pod.** Counts below are from Actions logs + committed `agent/state.json` + the **public** leaderboard. No secret values.

Cursor Automation `5d386e14-b158-11f1-a3d8-362438fd9788` is enabled but does not inject those secrets into the Cloud pod.

## Recent submissions (from Actions 36648798697 + `agent/state.json`)

Newest first; **publicScore is null on every recent row** (Kaggle has not published scores for these code submits, or they are still pending).

| id | desc | kernel | when (UTC) |
|----|------|--------|------------|
| 56692019 | 2026-09-30_cycle01 H-top-peaks | v36 | 2026-09-30 00:30 |
| 56687445 | 2026-09-29_cycle04 H-peaks | v35 | 2026-09-29 20:56 |
| 56681117 | 2026-09-29_cycle03 H-mass-wide | v34 | 2026-09-29 15:54 |
| 56669000 | 2026-09-29_cycle02 H-entropy | v33 | 2026-09-29 08:26 |
| 56659366 | 2026-09-29_cycle01 H-top-peaks | v32 | 2026-09-29 02:00 |
| 56653270 | 2026-09-28_cycle04 H-peaks | v31 | 2026-09-28 22:04 |

Best **scored** public result we own is still **0.143** (v0.1, 2026-09-15). All later kernels are unscored in our records.

## Public leaderboard (fetched 2026-09-30T06:12Z)

https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra/leaderboard

| Rank | Team | Public MRR@25 |
|------|------|----------------|
| 1 | pikachu | **0.464** |
| 2 | Randy | 0.435 |
| 3 | Ozymandias31415 | 0.425 |
| 4 | chopper | 0.415 |
| 5 | Udam Liyanage | 0.414 |

Gap vs our scored 0.143 is **~3.2×**. Public code notebooks in the analog / multi-channel family report ~0.23–0.34 (CASMI26 Quad-Channel Evidence Ranker 0.339; Analog Propagation ~0.33). Those use extra candidate DBs and fingerprint models we do not ship in this internet-off kernel.

## Why score is low (evidence, unchanged root cause)

1. **Poisoned exact duplicates (v0.1 diagnostics).** Every molecule had rank-1 `best_similarity = 1.0` on an `enveda-180` row whose train InChIKey14 ≠ competition GT. Perfect library match ⇒ MRR 0.143 ⇒ ~86% of those labels are wrong. `EXCLUDE_EXACT_DUPLICATES=True` is on; we must not re-trust those IKs.

2. **Daily fallbacks no longer change the live scorer.** Main already has `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, `MASS_TOL_PPM=35` / backfill 80, `TOP_K=120`, `MIN_SIMILARITY=0.05`. Slot 1–4 fallbacks are near no-ops. Slot 5 `H-domain` boosts priors that are already 1.0 / 1.0 / 0.85.

3. **Cleaning is looser than the entropy papers we cite.** `INTENSITY_FLOOR=0.001` keeps peaks at 0.1% of base intensity. Li/Fiehn and `msentropy.clean_spectrum` use **1%**. The 25% modified-cosine term in the hybrid is noise-sensitive; leftover ions also steal slots in the 128-peak ladder.

4. **Library / chemistry mismatch.** `enveda-180` is synthetic drug-like; test is NP-like. Domain priors cannot fix wrong structures.

5. **No analog / formula channel.** Leaders and public 0.33 notebooks add fingerprint / candidate-DB rankers. Retrieval-only cannot claim Class-3 de novo.

6. **Yesterday’s Cloud PR #13 (H-intensity) is still draft / unmerged.** Actions therefore submitted another no-op `H-entropy` at 08:26Z on 09-29. The unused knob is still `INTENSITY_FLOOR`.

## Concrete improvement for this slot

**One major factor:** `INTENSITY_FLOOR` 0.001 → **0.01**. Unused in the fallback rotation. Scientifically aligned with entropy cleaning. Repeats the unmerged Cloud PR #13 ablation so Actions can actually submit it today.

If this Cloud pod cannot `kernels push`, retarget Actions slot-2 fallback to the same patch so the next hourly `casmi-loop` (07:00Z) can `competition_submit_code` after this PR lands on main.

## Do not do this slot

Another `TOP_PEAKS` / `ENTROPY_WEIGHT` / mass-window sweep. CSV submit. Claiming retrieval solves Class-3.
