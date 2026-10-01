# Analysis 2026-10-01_cycle01 — why MRR is stuck and what to change

Competition day: **2026-10-01** (anchor 01:00 America/Chicago).
Triggered at **06:00 UTC** (01:00 CDT). Cycle **01** of 5.

## Quota check (do not submit if 5 already used)

Cloud Agent env still has **no** `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN` (same as 2026-09-18…09-30 cloud cycles). Could not write `~/.kaggle/kaggle.json` or call `kaggle competitions submissions`. Quota below is reconstructed from GitHub Actions + `agent/state.json` + public pages (no secret values).

| Clock | Used / 5 | Evidence |
|-------|----------|----------|
| Chicago 01:00 day **2026-10-01** | **0 / 5** | No `agent/state.json` cycle with `day=2026-10-01`. Last successful submit is `2026-09-30_cycle05` (Kaggle **56721177**, kernel v40, 23:16Z 09-30 = 18:16 CDT 09-30). |
| UTC calendar **2026-10-01** (Actions `competition_day()`) | **0 / 5** | Same last kaggle_id is still on 2026-09-30 UTC. |

Actions `casmi-loop` run **36803139818** started 2026-10-01T01:52:16Z on `main` @ `1281b82`. Job step **Run one slot** was **cancelled** at 01:58Z (~6 min). The workflow still lists `in_progress` (zombie); no new `kaggle_id` and no commit on `main` after cycle05. Treat as **no submit**.

**Quota is not exhausted. Proceed with cycle01.**

Recent scored/unscored Actions submits (newest first, from `agent/state.json`):

- id=56721177 score=null COMPLETE `2026-09-30_cycle05 H-domain` (empty patch / no-op)
- id=56716784 score=null COMPLETE `2026-09-30_cycle04 H-peaks`
- id=56709128 score=null COMPLETE `2026-09-30_cycle03 H-mass-wide`
- id=56699747 score=null COMPLETE `2026-09-30_cycle02 H-entropy`
- id=56692019 score=null COMPLETE `2026-09-30_cycle01 H-top-peaks`

Public scores on these rows stay **null** in state. Last **scored** public we trust is still **0.143** (v0.1).

## Public leaderboard context (fetched 2026-10-01 ~06:05Z)

CLIST standings (https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/):

| Rank | Team | Public MRR@25 |
|------|------|----------------|
| 1 | pikachu | **0.46** |
| 2 | Randy | 0.44 |
| 3 | Ozymandias31415 | 0.43 |
| — | Our last **scored** public | **0.143** (v0.1) |

Gap to #1: **~0.32**. Kaggle Code-tab notebooks (“analog ranker”, “quad-channel evidence ranker”, “two ranker W80”) still report **0.32–0.34**.

## Why score is low (evidence)

1. **Poisoned exact duplicates (v0.1).** Exact test↔train spectrum copies in `enveda-180` have train labels ≠ competition GT. Perfect library match of those rows yields ~0.143 public. `EXCLUDE_EXACT_DUPLICATES=True` is on and must stay on.

2. **The Actions fallback carousel is exhausted as science.** For a week, slots 1–5 have been `TOP_PEAKS=128` / `ENTROPY_WEIGHT=0.75` / mass-wide 35/80 / `TOP_PEAKS=160+MIN_SIM=0.05` / empty `H-domain`. All of those constants are **already live on `main`**. Repeating them cannot move MRR.

3. **Cleaning is still 10× too permissive vs entropy literature.** `INTENSITY_FLOOR=0.001` (0.1% of base peak). Li/Fiehn, msentropy, and matchms FlashSimilarity all use **0.01**. With `TOP_PEAKS=160` we keep a long tail of noise ions that entropy then *up-weights*. Cloud PRs **#13/#14** (`H-intensity`) specified this exact patch and **never merged**, so Actions never submitted it.

4. **Unscored later submits.** Kernel versions 14–40 completed on Kaggle but publicScore stayed null in logs. We cannot treat the carousel as validated.

5. **Runner split.** Actions has Kaggle secrets and is the only path that actually `kernels push`. This Cloud pod does not. Docs + config must land on git so the next `casmi-loop` hour can reuse them (`chatgpt_spec` prefers substantial pre-written cycle files).

## Concrete improvements for this slot

1. **Major ablation (one factor):** `INTENSITY_FLOOR` 0.001 → **0.01**.
2. **Unblock Actions slot 1:** retarget `FALLBACK_ABLATIONS[0]` from `H-top-peaks` (already live, would only shuffle 160→128) to `H-intensity` so the next unused UTC slot applies this patch even if OpenAI is missing / 429.
3. **Do not** change entropy weight, mass windows, `TOP_PEAKS`, or domain priors in the same slot.
4. **Do not** CSV-submit.

If this Cloud run still cannot `kernels push`, record the skip and open a PR. **This PR must reach `main` before the next hourly `casmi-loop`** or slot 1 will spend a quota ticket on `TOP_PEAKS=128` again.
