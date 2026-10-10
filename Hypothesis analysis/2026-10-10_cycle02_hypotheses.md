# Hypotheses 2026-10-10_cycle02

## H1 — `PEAK_MZ_TOL` 0.01 → 0.02 (this slot)

**Claim.** Widening the greedy fragment-match window from 10 mDa to the Flash Entropy Search / matchms default of **20 mDa** raises hybrid entropy+modcos scores for true library hits on mixed-resolution public libraries, moving the correct InChIKey14 up in the MRR@25 list.

**Why now.** Live `main` is already at Li/Fiehn `ENTROPY_WEIGHT=0.75` and `TOP_PEAKS=128`. The remaining unused matcher constant is `PEAK_MZ_TOL`. Yesterday’s Cloud cycle (#23) targeted `INTENSITY_FLOOR`; this cycle alternates to the other unused lever so we do not stack another unmerged 1% floor PR.

**Expected MRR direction.** Small public lift if any (0.143 → maybe 0.15–0.20). Failure mode: extra false fragment pairs inflate near-isobar decoys and MRR stays flat or drops. Still one factor; does not close the 0.33–0.48 analog-ranker gap.

## H2 — `INTENSITY_FLOOR` 0.001 → 0.01 (next unused)

Li/Fiehn + Flash drop ions &lt; 1% of base peak. Draft PRs #13–#19, #21, #23. Hold for the next Cloud / Actions slot after H1 merges or is rejected.

## H3 — `MIN_SIMILARITY` 0.05 → 0.12 (later)

Cuts low-support neighbors before aggregation (PRs #11/#12). Precision-oriented; risk of empty candidate lists.

## H4 — analog / formula expansion (out of scope)

Needed to approach 0.40+ public scores. Not a one-constant notebook ablation; does not claim Class-3 de novo.

## This slot

Run **H1 only**. Retarget Actions fallback slot 2 to `H-peak-mz` so the next hourly `casmi-loop` submits `{PEAK_MZ_TOL: 0.02}` instead of the live no-op `{ENTROPY_WEIGHT: 0.75}`.
