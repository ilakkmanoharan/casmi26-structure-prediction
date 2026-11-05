# Hypotheses — 2026-11-05 cycle02

## H1 — H-min-sim (run this slot)

**Claim.** Raising `MIN_SIMILARITY` from **0.05** to **0.12** drops near-zero hybrid entropy/modcos decoys from the per-spectrum candidate list so true-structure near-matches (and their CE/adduct support) can occupy more of the MRR@25 list.

**Mechanism.** `retrieve_for_spectrum` only forwards hits with `sim >= cfg.min_similarity`. Those hits are then truncated to `TOP_CANDIDATES_PER_SPECTRUM=25` and aggregated. At 0.05, Flash Entropy pairing (already 20 mDa) plus a 128-peak ladder produces many weak matches that fill the 25 before a mid-score true analog is seen. Li/Fiehn (*Nat. Methods* 2021) report FDR < 10% only at entropy ≥ 0.75; scores near 0.05 are the decoy regime. 0.12 is still far below 0.75, so identity-quality and decent analog hits remain. Backfill (`MASS_TOL_PPM_BACKFILL=80`, score × 0.1) still pads short lists.

**Expected MRR direction.** Small-to-moderate positive if decoy packing is the bottleneck; near-zero if the true structure’s hybrid score is already well above 0.12 and rank is decided by aggregation weights. Failure mode: true analogs / CE-shifted library spectra score 0.05–0.12 and disappear, increasing `fallback_used` / `placeholder_used` and lowering MRR. That is acceptable to measure — it is a real ablation, unlike replaying `PEAK_MZ_TOL=0.02`.

## H2 — MASS_TOL_PPM 35 → 10 (next unused)

**Claim.** A 10 ppm primary structure-level mass window (Li/Fiehn NIST search; historical CASMI 5–10 ppm) would cut isobar decoys. Keep backfill at 80 ppm.

**Why not now.** Confounds H1: a tighter mass window plus a tighter score floor moves two knobs. Measure the floor first.

## H3 — ENTROPY_WEIGHT 0.75 → 1.0 (later; already drafted as PR #73)

**Claim.** Drop the 25% modified-cosine mix so retrieval ranks with Li/Fiehn entropy similarity alone. The 0.75 figure in Li 2021 is an FDR cutoff, not a blend weight.

**Why not now.** Mix weight is already at the published FDR operating point. Smaller lever than the admission floor. PR #73 specified this as an alternate cycle02; do not stack it on H1.

## H4 — Analog / MS2Deepscore (out of scope)

Needs extra wheels or embeddings. Out of scope for a one-constant ablation. Do not claim Class-3 de novo is solved by retrieval.

## One major ablation this slot

Run **H1 only**. `config_patch: {"MIN_SIMILARITY": 0.12}`.
