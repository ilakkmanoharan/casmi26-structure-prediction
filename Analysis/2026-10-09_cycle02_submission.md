# Analysis 2026-10-09_cycle02 — why MRR is low and what to change

Competition day: **2026-10-09** (anchor 01:00 America/Chicago).  
Triggered at 06:00 UTC (01:00 CDT). Cycle **02** of 5 for the UTC filename (Actions already used `2026-10-09_cycle01` before the Chicago day opened).

## Quota check (do not submit if 5 already used)

Cloud Agent env still has **no** `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN`. Direct `kaggle competitions submissions` could not be run from this pod. Quota inferred from `agent/state.json` + Actions run **37871612881**.

Actions 37871612881 (2026-10-09T01:49Z schedule → slot work 02:06Z):

```
submissions used today (2026-10-09): local=0 kaggle=0
=== casmi-loop 2026-10-09 slot 1 ===
kaggle submissions [
  (56973849, None, '2026-10-08_cycle04 H-peaks'),
  (56960977, None, '2026-10-08_cycle03 H-mass-wide'),
  (56941831, None, '2026-10-08_cycle02 H-entropy'),
  (56927100, None, '2026-10-08_cycle01 H-top-peaks'),
  (56921568, None, '2026-10-07_cycle04 H-peaks')
]
applied config patch {'TOP_PEAKS': 128}
competition_submit_code result ref=56985213
kernel_version=74  message=2026-10-09_cycle01 H-top-peaks
```

Clock split (CDT = UTC−5):

| Clock | Window | Used / 5 | Notes |
|-------|--------|----------|-------|
| **Chicago 01:00** (this prompt) | 2026-10-09 06:00Z → 2026-10-10 06:00Z | **0 / 5** | Day just opened. Quota **not** exhausted. |
| UTC calendar (`casmi-loop`) | 2026-10-09 00:00Z → 24:00Z | **1 / 5** | 56985213 at 02:06Z (21:06 CDT **Oct 8**) |

Would submit this cycle if Kaggle secrets were present. Because they are not, implement + retarget Actions slot-2 and open a PR.

## Public leaderboard context (fetched 2026-10-09T06:05Z)

CLIST prize table:

| Rank | Team | Public MRR@25 |
|------|------|----------------|
| 1 | pikachu (jzhpfn) | **0.48** |
| 2 | MarvinTMB | 0.47 |
| 3–5 | Oliver Ford / vukpetar / Yuuki Aikawa | 0.46 |
| 6–10 | Sho Saga / Sls2 / Savko / toolazyhhh123 / Shehab | 0.45 |
| — | Community analog / quad-channel notebooks | 0.328–0.339 |
| — | Our last **scored** public | **0.143** (v0.1) |

Gap to #1: **0.337**. Later kernel versions 14–74 still show `publicScore=None` in Actions logs — we cannot treat H-top-peaks / H-entropy / H-mass-wide / H-peaks as validated lifts.

## Why our score is low (evidence)

1. **Poisoned exact duplicates (v0.1).** Exact test↔train spectrum copies in `enveda-180` have train labels ≠ competition GT. Perfect library match of those rows yields ~0.143 public. `EXCLUDE_EXACT_DUPLICATES=True` is on and must stay on.

2. **Live cleaner is not Li/Fiehn.** `main` after Actions 10-09 cycle01: `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, mass-wide 35/80, `MIN_SIMILARITY=0.05`, **`INTENSITY_FLOOR=0.001`**, **`PEAK_MZ_TOL=0.01`**. Entropy similarity was benchmarked after a **1%** base-peak cut. A 0.1% floor + 128-peak cap keeps noise ions that inflate spectral entropy and create false fragment matches.

3. **Actions slot-2 is a no-op.** Fallback `H-entropy` writes `ENTROPY_WEIGHT=0.75`, already live. Next hourly `casmi-loop` (≈07:00 UTC) will burn a UTC ticket unless slot-2 is retargeted and this PR merges.

4. **Cloud PRs remain drafts.** H-intensity PRs #13–#19, #21 and H-peak-mz PRs #20, #22 never merged. `main` never received the 1% floor.

5. **Architecture gap.** 0.33–0.48 public scores come from analogue / multi-channel rankers, not from recycling the five fallback knobs. This slot still does one retrieval-cleaner ablation; it does not claim Class-3 de novo.

## Concrete improvements for this slot

1. **Major ablation:** `INTENSITY_FLOOR` 0.001 → **0.01** (1% of base peak after max-normalization in `clean_spectrum`).
2. **Retarget Actions slot-2 fallback** from `H-entropy` / `{ENTROPY_WEIGHT: 0.75}` to `H-intensity` / `{INTENSITY_FLOOR: 0.01}` so the next hourly run submits a new factor even if OpenAI is absent.
3. **Do not** change `PEAK_MZ_TOL`, `MIN_SIMILARITY`, mass windows, or entropy weight in the same slot.
4. **Do not** CSV-submit.

If this Cloud run still cannot `kernels push`, the code + docs must land on git so Actions (which *has* Kaggle secrets) can submit after merge.
