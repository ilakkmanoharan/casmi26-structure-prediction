# Hypotheses — 2026-11-06 cycle02

From Research + Analysis. One major ablation this slot.

## H1 — MIN_SIMILARITY 0.05 → 0.12 (**this slot**)

**Mechanism.** `retrieve_for_spectrum` admits a library row only when `hybrid_similarity >= cfg.min_similarity`. Live 0.05 is far below Li/Fiehn’s 0.75 annotation cutoff and below typical “maybe related” cosine/entropy scores. After Flash Entropy 20 mDa pairing, more fragment pairs survive, so *more* unrelated isobars clear 0.05 and occupy `TOP_K_SPECTRA=120`. Raising the floor to 0.12 drops those decoys before molecule-level aggregation, which should move true InChIKey14s up inside the MRR@25 list on Class-1 queries.

**Expected MRR direction.** Flat to modest **up** on public (Class-1 subset). Will not jump toward 0.50.

**Failure mode.** Sparse / low-entropy queries lose their only weak neighbors and fall back to mass-only placeholders → MRR **down** on those molecules. 0.12 is still well below 0.75, so this is a decoy filter, not a high-confidence ID cut.

## H2 — MASS_TOL_PPM 35 → 10 (next unused after H1 lands)

**Mechanism.** Narrower precursor window removes unrelated formulas before similarity. Orthogonal to the admission floor.

**Why not now.** One factor per slot. Mass-window shrinkage can drop true adduct/isotope partners on timsTOF; gate first, then mass.

## H3 — ENTROPY_WEIGHT 0.75 → 1.0 (later)

**Mechanism.** Drop the modified-cosine mix; score with pure entropy as in Li/Fiehn identity search.

**Why not now.** Mix weight is already at the literature default. Changing it together with the gate would confound the result.

## H4 — TOP_PEAKS 128 → 160 (slot-4 fallback)

Keep as the existing slot-4 fallback, which also resets `MIN_SIMILARITY=0.05`. Only useful *after* 0.12 is live, as a contrast that lengthens the ladder and lowers the gate.

## This slot

Run **H1** only. `config_patch: {"MIN_SIMILARITY": 0.12}`. Hypothesis id: **H-sim-gate**.
