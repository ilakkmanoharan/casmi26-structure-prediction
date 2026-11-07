# Hypotheses — 2026-11-07 cycle02

## H1 — H-sim-gate (run this slot)

**Claim.** Raising `MIN_SIMILARITY` from **0.05** to **0.12** drops weak hybrid (entropy + modified-cosine) decoys that currently fill the MRR@25 list after exact-dup exclusion, improving public MRR@25 versus the 0.143 plateau.

**Mechanism.** `retrieve_for_spectrum` admits a library row when `hybrid_similarity(...) >= cfg.min_similarity`, then keeps `top_k_spectra` of those hits. At 0.05, almost any overlapping fragment pair after the 0.02 Da window survives. Li/Fiehn (2021) treat entropy scores well below 0.75 as high-FDR; 0.12 is a *recall-preserving* floor (not an identification cutoff) so sparse queries can still fill a list, but the worst decoys leave the 25-slot ranking.

**Expected MRR direction.** Small-to-moderate positive if decoy crowding is the bottleneck after H-peak-mz; near-zero if true structures also score 0.05–0.12 and get dropped. Failure mode: empty or short candidate lists on noisy queries (MRR down for those molecules). That is acceptable to measure — it is a real ablation, unlike replaying `TOP_PEAKS=128` or `PEAK_MZ_TOL=0.02`.

## H2 — ENTROPY_WEIGHT 0.75 → 1.0 (next unused)

**Claim.** Pure entropy (drop the 0.25 modified-cosine term) further down-weights noisy NP cosine ties.

**Why not now.** Confounds H1: a tighter floor plus a mix-weight change moves two knobs. Measure the floor first.

## H3 — MASS_TOL_PPM 35 → 15 (later)

**Claim.** A tighter precursor window cuts same-mass isomers that sneak in at 35 ppm.

**Why not now.** Changes *who is scored*, not *which scores enter the list*. Orthogonal to H1; reserve for a later slot.

## H4 — Analog / MS2Deepscore (out of scope)

Needs extra wheels or embeddings. Out of scope for a one-constant ablation. Do not claim Class-3 de novo is solved by retrieval.

## One major ablation this slot

Run **H1 only**. `config_patch: {"MIN_SIMILARITY": 0.12}`.
