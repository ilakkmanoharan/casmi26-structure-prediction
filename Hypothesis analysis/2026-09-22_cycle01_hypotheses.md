# Hypotheses 2026-09-22_cycle01

Built from `Research/2026-09-22_cycle01_methods.md` and `Analysis/2026-09-22_cycle01_submission.md`.

## H1 — Restoring `TOP_PEAKS` 5 → 128 raises public MRR@25 (this slot)

**Claim.** Cycle05’s 5-peak cap is the largest live self-inflicted loss. Entropy similarity (Li & Fiehn 2021) and Flash Entropy keep ions ≳1% BPI / up to 100+ peaks. Analog-ranker notebooks at 0.33–0.34 and the 0.415 leader need those ions. Restoring 128 should move us off the 0.143 / unscored-v13 plateau toward the open 0.15–0.25 retrieval band (not yet 0.41).

**Test.** One code submit with only `TOP_PEAKS=128` changed vs 56298621 (`MASS_TOL_PPM=10`, `MASS_TOL_PPM_BACKFILL=15`, `ENTROPY_WEIGHT=0.6`, `EXCLUDE_EXACT_DUPLICATES=True`, `PEAK_MZ_TOL=0.01`).

**Expected direction.** Public MRR@25 **up** vs 0.143 if the kernel scores; null if Kaggle still hides the score.

**Failure modes.** (a) Kernel timeout / ERROR (more peaks = more match work). (b) Weaker exact-dup detection lets a poisoned InChIKey back in (dup check uses cleaned peaks). (c) Cloud cannot push, so the hypothesis is not scored until Actions merges this branch.

## H2 — Analog / wider-mass backfill (later)

Public 0.33–0.41 methods look like analog search. Widening `MASS_TOL_PPM` now would confound H1.

## H3 — Ranker / sort-order weights (later)

Community note: sort order moved MRR by ~0.03 on 250 queries. Touch `WEIGHTS` only after the fragment ladder is live.

## H4 — `ENTROPY_WEIGHT=0.70` (later)

Specified 2026-09-15 cycle02; kernel ERRORed; never scored. Still a clean single-factor follow-up after H1.

## This slot

**Run H1 only.** Do not stack H2–H4 on the same kernel version.
