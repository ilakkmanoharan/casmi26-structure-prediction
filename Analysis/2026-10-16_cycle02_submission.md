# Analysis 2026-10-16_cycle02

Chicago competition day **2026-10-16** opened at 01:00 CDT (06:00 UTC). Cloud cron fired ~06:00 UTC.

## Quota (reconstructed; Kaggle API not callable from this pod)

`KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN` are **absent** in this Cursor Cloud environment, so `~/.kaggle/kaggle.json` could not be written and `kaggle competitions submissions` was not run. Count is from `agent/state.json` + GitHub Actions `casmi-loop`.

| Clock | Used / 5 | Evidence |
| --- | --- | --- |
| **Kaggle UTC day 2026-10-16** | **1/5** | Actions [38832985450](https://github.com/ilakkmanoharan/casmi26-structure-prediction/actions/runs/38832985450) (01:03Z) → Kaggle **57250397**, kernel v104, `2026-10-16_cycle01 H-top-peaks` |
| **Chicago clock since 01:00 CDT** | **0/5** | UTC submit was 01:26Z = 20:26 CDT Oct 15, *before* today's 01:00 CDT anchor |
| In-progress casmi-loop | none | Latest run completed success ~23m |
| Next hourly Actions | **07:00 UTC** | Will take UTC slot 2 unless this PR merges first |

Quota is **not** exhausted. This cycle should still implement + (if secrets exist) submit. Secrets missing → **skip kernels push / competition_submit_code**.

## Recent submissions (from `agent/state.json`)

| Kaggle id | Tag | Hypothesis | Public score |
| --- | --- | --- | --- |
| 57250397 | 2026-10-16_cycle01 | H-top-peaks (`TOP_PEAKS=128`) | null (best known still **0.143**) |
| 57245447 | 2026-10-15_cycle05 | H-domain | null |
| 57241970 | 2026-10-15_cycle04 | H-peaks | null |
| 57233778 | 2026-10-15_cycle03 | H-mass-wide | null |
| 57224771 | 2026-10-15_cycle02 | H-entropy | null |

Public scores on our kernels keep coming back empty/0.143-class. v0.1 failure still holds: exact test↔train spectrum duplicates in `enveda-180` with train labels ≠ competition GT.

## Leaderboard (public, ~31% of test; fetched 2026-10-16 ~06:05Z)

| Rank | Team | Score |
| --- | --- | --- |
| 1 | pikachu | **0.495** |
| 2 | Oleksandr Parfionov | 0.493 |
| 3 | CHU1PC | 0.491 |
| 4 | MarvinTMB | 0.484 |
| 5 | Oliver Ford | 0.468 |

Gap vs our best scored public **0.143** is ~3.5×. Community analog + fingerprint + forward-MS/MS notebooks sit ~0.32–0.42. Retrieval-only will not close that by itself.

## Why score is still low

1. **Poisoned exact dups** in `enveda-180` (train IK ≠ GT) — `EXCLUDE_EXACT_DUPLICATES=True` is already on; remaining hits are analog/near-dup, not identity.
2. **Live cleaning is too permissive.** `INTENSITY_FLOOR=0.001` keeps ions entropy/Flash Entropy would drop at 1%. Noise ions inflate modified-cosine support and scramble the hybrid rank.
3. **Actions slot-2 fallback is a no-op.** `ENTROPY_WEIGHT` is already 0.75 on main. If this PR is not merged before 07:00 UTC, casmi-loop will spend a ticket restating H-entropy.
4. Unmerged Cloud PRs **#13–#19, #21, #23, #25, #27, #28, #29** (H-intensity) and **#20/#22/#24/#26** (H-peak-mz) never landed, so the 1% floor has **never been Kaggle-scored**.

## What to do this slot

One major change vs live main:

- `INTENSITY_FLOOR`: **0.001 → 0.01**
- Retarget Actions `FALLBACK_ABLATIONS[1]` from H-entropy → H-intensity so the next unused casmi-loop slot actually tests this.

Do **not** re-submit TOP_PEAKS=128 / ENTROPY_WEIGHT=0.75 / mass-wide 35/80.
