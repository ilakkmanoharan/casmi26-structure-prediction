# Hypotheses — 2026-09-15 cycle01

Derived from `Research/2026-09-15_cycle01_methods.md` and `Analysis/2026-09-15_cycle01_submission.md`.

## H1 — Exact-duplicate penalty (primary)

**Statement:** Excluding train spectra whose cleaned peaks+precursor match a test spectrum (or downweighting their contribution to 0) will free rank-1 for structures supported by non-identical evidence and raise public MRR@25.

**Rationale:** v0.1 rank-1 is always the enveda-180 exact duplicate label; public score 0.143 shows those labels ≠ GT.

**Ablation:** submit v0.2 with duplicate exclusion only (+ minor entropy hybrid).

## H2 — Entropy + modified-cosine hybrid

**Statement:** Scoring `0.55·entropy + 0.45·modified_cosine` on mass-filtered candidates improves discrimination among near-isobars vs cosine alone.

**Rationale:** Li & Fiehn (2021); cosine saturates at 1.0 on our cleaned top-64 views.

## H3 — Full-library index

**Statement:** Including `pluskal_ms2` and other libs increases Hit@25 / MRR by recovering structures absent from preferred NP/enveda slices.

**Rationale:** Coverage gap; soft domain prior still prefers enveda when evidence ties.

## H4 — Soften domain prior

**Statement:** Reducing `enveda-180` prior weight (or zeroing it) prevents poisoned enveda hits from beating stronger spectral evidence from other libs.

## H5 — Structure ExactMolWt gate

**Statement:** Filtering candidates by RDKit exact mass vs inferred neutral mass (±20–35 ppm) removes adduct-inconsistent decoys better than spectrum-neutral-mass alone.

## Cycle-01 chosen bet

Ship **H1 + H2 + H3** together as v0.2 (one coherent “don’t trust leaked labels + better similarity + more coverage” package). Reserve H4/H5 for slots 3–4 if v0.2 underperforms.
