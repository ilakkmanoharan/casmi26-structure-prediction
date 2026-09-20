# Hypotheses 2026-09-20_cycle01

Built from `Research/2026-09-20_cycle01_methods.md` and
`Analysis/2026-09-20_cycle01_submission.md`.

## H1 — Fragment-ladder restore (MAJOR ablation this slot)

**Claim.** Raising `TOP_PEAKS` from 5 → 128 increases public MRR@25 versus
kernel v13 (56298621) because entropy/modcos regain diagnostic ions and
exact-dup poisoning uses a real peak vector.

**Expected direction.** MRR@25 **up** from the last scored 0.143, still
well below 0.332 if poisoned labels remain. A flat or down score would
mean (a) public GT is dominated by cases where 5-peak match already
sufficed, or (b) extra peaks add noise that entropy does not down-weight
enough (`INTENSITY_FLOOR=0.001` already drops <0.1% BPI-ish ions).

**Failure mode.** Kernel runtime grows (more peaks in hybrid similarity).
If the 20-min Actions budget is exceeded, drop to 64 next slot — not 5.

## H2 — Entropy-dominant hybrid (next slot, not this one)

**Claim.** After H1 is scored, `ENTROPY_WEIGHT` 0.60 → 0.70 (Li 2021)
further lifts rank of the true structure. Stacking it now would confound
the TOP_PEAKS result.

## H3 — Actions 429 is why quota is idle, not Kaggle

**Claim.** Every hourly `casmi-loop` since 2026-09-18 05:37Z had Kaggle
auth and `kaggle=0` remaining, then aborted in `_openai_json`. Catching
HTTP 429/URL errors and returning `None` lets the deterministic fallback
run implement+submit. Independent of H1 science.

## H4 — Cloud secrets still block this runner

**Claim.** Without `KAGGLE_USERNAME`/`KAGGLE_KEY` on the Cursor
Automation, this cycle cannot create a Kaggle code submission even with
quota remaining. False if secrets appear mid-run.

## One major ablation

**H1 only:** `TOP_PEAKS=128`. Keep mass ppm, entropy mix, duplicate ban,
and library priors identical to cycle05.
