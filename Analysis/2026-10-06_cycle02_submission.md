# Analysis 2026-10-06_cycle02

## Quota (re-checked before any submit)

Competition day for this Cloud Automation prompt starts **01:00 America/Chicago**. Wall clock at run start: **2026-10-06 01:03 CDT / 06:03 UTC**.

| Clock | Used / 5 | Evidence |
|-------|----------|----------|
| **Chicago 01:00** | **0 / 5** | No `agent/state.json` submit after 2026-10-06 06:00Z. Actions 37395182349 → Kaggle **56866331** ran at **01:04Z** (20:04 CDT Oct 5), i.e. the previous Chicago day. |
| **UTC calendar (Kaggle reset)** | **1 / 5** | 56866331 `2026-10-06_cycle01 H-top-peaks` kernel v62. |

**Not exhausted.** Cloud cannot confirm via `kaggle competitions submissions` because `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN` are absent in this environment (same blocker as 2026-09-25…10-05 Cloud crons). Count is from `agent/state.json` + `gh run list` on `casmi-loop.yml`.

## Recent submissions (from state + last Actions analysis dump)

Public scores on our tickets remain **unpopulated** (`publicScore=None`) in CLI dumps; scored best is still **0.143** (v0.1). Newest recorded:

- 56866331 COMPLETE — 2026-10-06_cycle01 H-top-peaks (`TOP_PEAKS=128`)
- 56859251 COMPLETE — 2026-10-05_cycle03 H-mass-wide
- 56848014 COMPLETE — 2026-10-05_cycle02 H-entropy (no-op vs live `ENTROPY_WEIGHT=0.75`)
- 56839604 COMPLETE — 2026-10-05_cycle01 H-top-peaks

## Why the public score is low

1. **Poisoned exact dups (v0.1).** Exact test↔train spectrum copies in `enveda-180` carry train labels that do **not** match competition GT. A perfect library hit still scores ~0.143. `EXCLUDE_EXACT_DUPLICATES=true` is on; we still need non-identical evidence.
2. **Fragment match window is tighter than the entropy literature.** `PEAK_MZ_TOL=0.01` (10 mDa) is half of Flash Entropy Search’s default **20 mDa**. Cross-library / low-abundance ions that differ by 10–20 mDa never enter the greedy match, so entropy/modcos of the true structure stays low and MRR@25 never moves.
3. **Actions fallbacks are saturated.** Slot 1 `TOP_PEAKS=128` and slot 2 `ENTROPY_WEIGHT=0.75` are already live on main. Repeating them burns quota with no config change.
4. **Leaderboard gap.** CLIST 2026-10-06T06:10Z: **pikachu 0.47**, **MarvinTMB 0.47**, then a 0.44 pack (Nicolas / Bertan / Shehab / Sho / chopper / Randy / Xolotl). Ozymandias31415 **0.43**. Community analog/quad-channel notebooks **0.328–0.339**. We remain at scored **0.143**.

## Concrete improvement for this slot

Ablate **only** `PEAK_MZ_TOL` 0.01 → **0.02**. Retarget Actions `FALLBACK_ABLATIONS[1]` from H-entropy to H-peak-mz so the next hourly `casmi-loop` slot 2 does not waste another ticket on `ENTROPY_WEIGHT=0.75`.

## Cloud submit status

`~/.kaggle/kaggle.json` was **not** written (secrets missing). **No** `kernels push` / `competition_submit_code` from this runner. Merge this PR before the next hourly Actions run or UTC slot 2 repeats the H-entropy no-op.
