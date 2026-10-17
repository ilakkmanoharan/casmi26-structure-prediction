# Analysis 2026-10-17_cycle02

Chicago competition day **2026-10-17** opened at 01:00 CDT (06:00 UTC). Cloud cron fired ~06:02 UTC.

## Quota (reconstructed; Kaggle API not callable from this pod)

`KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN` are **absent** in this Cursor Cloud environment, so `~/.kaggle/kaggle.json` could not be written and `kaggle competitions submissions` was not run. Count is from `agent/state.json` + GitHub Actions `casmi-loop`.

| Clock | Used / 5 | Evidence |
| --- | --- | --- |
| **Kaggle UTC day 2026-10-17** | **1/5** | Actions [38999313388](https://github.com/ilakkmanoharan/casmi26-structure-prediction/actions/runs/38999313388) (03:34Z, 23m success) → Kaggle **57294186**, kernel v109, `2026-10-17_cycle01 H-top-peaks` |
| **Chicago clock since 01:00 CDT** | **0/5** | UTC submit started 03:57Z = 22:57 CDT Oct 16, *before* today's 01:00 CDT anchor |
| In-progress casmi-loop | none | Latest run completed success; next hourly **07:00 UTC** |

Quota is **not** exhausted (need 5 used to skip). This cycle should still implement + (if secrets exist) submit. Secrets missing → **skip kernels push / competition_submit_code**.

## Recent submissions (from `agent/state.json`)

| Kaggle id | Tag | Hypothesis | Public score |
| --- | --- | --- | --- |
| 57294186 | 2026-10-17_cycle01 | H-top-peaks (`TOP_PEAKS=128`) | null (best known still **0.143**) |
| 57283308 | 2026-10-16_cycle05 | H-domain | null |
| 57277899 | 2026-10-16_cycle04 | H-peaks | null |
| 57269064 | 2026-10-16_cycle03 | H-mass-wide | null |
| 57259588 | 2026-10-16_cycle02 | H-entropy | null |
| 57250397 | 2026-10-16_cycle01 | H-top-peaks | null |

Public scores on our kernels keep coming back empty/0.143-class. v0.1 failure still holds: exact test↔train spectrum duplicates in `enveda-180` with train labels ≠ competition GT.

## Leaderboard (public, ~31% of test; CLIST ~2026-10-17T06:05Z)

| Rank | Team | Score |
| --- | --- | --- |
| 1 | pikachu | **0.50** |
| 2 | Oleksandr Parfionov | 0.49 |
| 3 | CHU1PC | 0.49 |
| 4 | MarvinTMB | 0.48 |
| 5 | Oliver Ford | 0.47 |

Gap vs our best scored public **0.143** is ~3.5×. Community analog + fingerprint + forward-MS/MS notebooks sit ~0.32–0.42. Retrieval-only will not close that by itself.

## Why score is still low

1. **Poisoned exact dups** in `enveda-180` (train IK ≠ GT) — `EXCLUDE_EXACT_DUPLICATES=True` is already on; remaining hits are analog/near-dup, not identity.
2. **Live cleaning is too permissive.** `INTENSITY_FLOOR=0.001` keeps ions entropy/Flash Entropy would drop at 1%. Noise ions inflate modified-cosine support and scramble the hybrid rank.
3. **Actions slot-2 fallback is a no-op.** `ENTROPY_WEIGHT` is already 0.75 on main. If this PR is not merged before 07:00 UTC, casmi-loop will spend a ticket restating H-entropy.
4. Unmerged Cloud PRs **#13–#19, #21, #23, #25, #27, #28, #29, #30** (H-intensity) and **#20/#22/#24/#26** (H-peak-mz) never landed, so the 1% floor has **never been Kaggle-scored**.

## What to do this slot

One major change vs live main:

- `INTENSITY_FLOOR`: **0.001 → 0.01**
- Retarget Actions `FALLBACK_ABLATIONS[1]` from H-entropy → H-intensity so the next unused casmi-loop slot actually tests this.

Do **not** re-submit TOP_PEAKS=128 / ENTROPY_WEIGHT=0.75 / mass-wide 35/80.
