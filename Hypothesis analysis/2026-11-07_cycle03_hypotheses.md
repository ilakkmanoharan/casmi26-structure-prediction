# Hypotheses 2026-11-07_cycle03

Prior public MRR@25: **0.143**. Metric: mean reciprocal rank of the first tautomer-canonical InChIKey14 in ≤25 SMILES. Retrieval cannot invent missing structures.

## H1 (this slot) — H-precursor-cut

**Claim.** Dropping ions with `m/z > precursor_mz − 1.6` Da on both library and query spectra raises MRR@25 relative to the current cleaner (`mz ≤ precursor + 2 Da`).

**Mechanism.** Precursor and near-precursor peaks are shared by every mass-window isobar. They inflate hybrid entropy/modcos for wrong InChIKeys and dilute diagnostic fragments. ms_entropy / Flash Entropy set `precursor_ions_removal_da=1.6` after measuring an ID gain on NIST20 and MassBank.us.

**Major ablation (only one):** `MAX_PEAKS_ABOVE_PRECURSOR_DA: -1.6`, wired through `RunConfig` into every `clean_spectrum` call (index build, poisoned-dup scan, per-query retrieval, backfill).

**Expected MRR direction:** up vs the 0.143 / unscored no-op kernels, if enough true structures remain in the index after the cut.

**Failure mode:** sparse or precursor-dominated MS/MS (common at low CE) fall below the index’s 3-peak keep rule, shrinking recall and hurting MRR. Exact-dup poisoning is unchanged: banned IKs stay banned because query and index share the same cleaner.

## H2 — raise min similarity (next slot if H1 is flat)

`MIN_SIMILARITY` 0.05 → 0.15–0.25. Li 2021: entropy 0.75 ⇒ FDR &lt; 10%. A 0.05 floor admits junk into the 25 slots. **Not combined with H1.**

## H3 — tighten precursor mass window (later)

`MASS_TOL_PPM` 35 → 10–15 to match identity-search practice. Wide windows feed H1’s isobar problem from the other side. **Not this slot.**

## H4 — entropy weight 0.75 → 0.90 (later)

Closer to pure entropy (Li 2021 winner vs 42 metrics). Hybrid 0.75 already leans entropy; smaller expected effect than H1.

## Chosen ablation

**H1 / H-precursor-cut only.**
