# Analysis — 2026-09-28 cycle02

## Quota (pre-flight)

Competition day starts **01:00 America/Chicago**. This Cloud run fired at **2026-09-28T06:02Z** (= 01:02 CDT).

| Clock | Submits counted | Source |
|-------|-----------------|--------|
| UTC calendar 2026-09-28 (Kaggle reset) | **1 / 5** | `agent/state.json` cycle01 + Actions run 36362065777 |
| Chicago 01:00 2026-09-28 → now | **0 / 5** | cycle01 was 00:47Z = 19:47 CDT on 2026-09-27 |

**Quota is not exhausted.** A submit is allowed.

Kaggle CLI/API could **not** be queried from this Cloud Agent: `KAGGLE_USERNAME`, `KAGGLE_KEY`, and `KAGGLE_API_TOKEN` are absent (same as 2026-09-25/26 Cloud cycles). `write_kaggle_credentials()` returned false; `~/.kaggle/kaggle.json` was not written. Therefore this runner **cannot** `kernels push` or `competition_submit_code`. Actions on `main` remains the submit path.

## Recent submissions (from committed state; API list unavailable)

| id | public | status | message / patch |
|----|--------|--------|-----------------|
| 56624265 | null | COMPLETE | 2026-09-28_cycle01 H-top-peaks · `TOP_PEAKS=128` · kernel v28 · 00:47Z |
| 56620606 | null | COMPLETE | 2026-09-27_cycle05 H-domain |
| 56616355 | null | COMPLETE | 2026-09-27_cycle04 H-peaks |
| 56610673 | null | COMPLETE | 2026-09-27_cycle03 H-mass-wide |
| 56603111 | null | COMPLETE | 2026-09-27_cycle02 H-entropy |
| 56594353 | null | COMPLETE | 2026-09-27_cycle01 H-top-peaks |

Best **recorded** public MRR@25 remains **0.143** (v0.1). Recent COMPLETE rows still show `publicScore=None` in the loop briefing — treat post-v0.1 ablations as **unscored**, not as proven lifts.

## Leaderboard context (public page, 2026-09-28T06:04Z)

https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra/leaderboard

- #1 Ozymandias31415 **0.425**
- #2 pikachu **0.421**
- #3 Udam Liyanage **0.414**
- #4 Randy 0.411 · #5 Shehab Alshehabi 0.406

Gap vs our last scored run: **0.425 − 0.143 = 0.282**. Retrieval + analogue re-rank is what moves the public LB; cosine-only library search is not.

## Why the score is still low

1. **Poisoned exact duplicates (v0.1).** Exact test↔train spectra in `enveda-180` carry train labels that do **not** match competition GT. Perfect library match → wrong SMILES → public ~0.143. Ban is on (`EXCLUDE_EXACT_DUPLICATES=True`) but removes the easy hits.
2. **Weak hybrid ties fill the top-25.** After the ban, `MIN_SIMILARITY=0.05` still admits near-noise neighbors. Aggregation then ranks decoys into the MRR@25 window. Literature identity/analogue gates are 0.55–0.75 (Li 2021; MS2Query GNPS2).
3. **Slot-2 fallback is a no-op today.** `ENTROPY_WEIGHT` is already 0.75; `TOP_PEAKS` already 128; mass window already 35/80. Repeating H-entropy wastes the UTC slot.
4. **No Class-3 channel.** Retrieval cannot invent missing structures. Do not claim de novo is solved.

## Concrete improvement for this slot

Raise **`MIN_SIMILARITY` 0.05 → 0.12** only. Hold entropy 0.75, peaks 128, mass 35/80, exact-dup ban. Conservative vs literature (0.55+) so sparse queries still backfill. If Actions merges these docs before the next hourly cron, `casmi-loop` will reuse them (`_substantial` ≥400 chars) instead of the H-entropy fallback.

## Skip / handoff

This Cloud cycle implements the ablation and rebuilds `kaggle_kernel/` but **does not submit**. Next Actions slot on UTC 2026-09-28 should apply `config_patch: {"MIN_SIMILARITY": 0.12}` and `competition_submit_code` (never CSV).
