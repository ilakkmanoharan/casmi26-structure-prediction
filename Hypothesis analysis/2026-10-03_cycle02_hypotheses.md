# Hypotheses — 2026-10-03 cycle02

## H1 (this slot) — H-intensity

**Claim.** Raising `INTENSITY_FLOOR` from `0.001` to `0.01` increases public MRR@25 relative to the current 128-peak / entropy-0.75 / mass-wide stack.

**Mechanism.** Flash Entropy Search and msentropy drop fragments below 1% of the base peak before scoring. Our cleaner still keeps 0.1% ions. Those ions (a) occupy the 128-peak budget, (b) greedy-match to library noise, and (c) inflate hybrid entropy/modcos for the wrong InChIKey — including remaining near-duplicates after the exact-dup ban.

**Expected MRR direction.** Small **up** if noise matches currently outrank true non-identical evidence; **flat** if the 0.143 cap is still dominated by poisoned labels that survive the exact-dup filter; **down** if true diagnostic fragments sit between 0.1% and 1% (failure mode).

**Failure mode.** Sparse / low-CE queries lose the last real fragments and fall back to mass-only / placeholder ranks.

## H2 — H-mz-tol (next unused)

`PEAK_MZ_TOL` 0.01 → 0.02 (Flash ±20 mDa). Helps QTOF vs Orbitrap library mismatch. Risk: more coincidental fragment matches.

## H3 — H-min-sim (Cloud PRs #11/#12, never merged)

`MIN_SIMILARITY` 0.05 → 0.12. Drops weak decoys before aggregation. Risk: empty candidate lists on sparse spectra.

## H4 — analog / multi-channel (not this kernel)

Community 0.33–0.34 and prize 0.42–0.47 come from analog propagation + multi-score rankers, not another ppm tweak. Out of scope for a one-constant ablation.

## Slot choice

Run **H1 only**. H-entropy / H-top-peaks / H-mass-wide are already live on `main` and are no-ops.
