# Hypotheses — 2026-11-06 cycle03

## H1 — H-sim-gate (run this slot)

**Claim.** Raising `MIN_SIMILARITY` from **0.05** to **0.12** drops weak hybrid scores that currently pad the top-25 with mass-window decoys, improving public MRR@25 versus the 0.143 plateau.

**Mechanism.** `retrieve_for_spectrum` admits a library row only when `hybrid_similarity(...) >= cfg.min_similarity` (`casmi26/retrieve.py`). At 0.05, two shared ions inside the now-live 20 mDa Flash Entropy window are enough to occupy a `TOP_K_SPECTRA=120` slot. Those decoys then compete in `aggregate_molecule_candidates` and crowd GT off the MRR@25 list. Li/Fiehn 2021 treat entropy similarity ≪ 0.75 as mostly false; MS2Query practice discards model scores < ~0.6. 0.12 is a *soft* decoy filter — well below identity cutoffs — so sparse queries still keep near-neighbors after 20 mDa pairing.

**Expected MRR direction.** Small-to-moderate positive if the top-25 is decoy-saturated; near-zero if GT library hits already score ≫ 0.12 and the remaining error is Class-2/3 absence. Failure mode: sparse 2–3 peak queries whose true-structure hybrid sits in 0.05–0.12 get empty candidate lists (MRR down on those molecules). That is acceptable to measure — it is a real ablation, unlike replaying `PEAK_MZ_TOL=0.02`.

## H2 — MASS_TOL_PPM 35 → 10 (next unused)

**Claim.** A tighter precursor window reduces isobar clutter before similarity is computed.

**Why not now.** Confounds H1: fewer candidates *and* a higher score floor move two knobs. Measure the gate first.

## H3 — ENTROPY_WEIGHT 0.75 → 1.0 (later)

**Claim.** Pure entropy (no modified-cosine blend) may further down-weight high-intensity diagnostic mismatches.

**Why not now.** Orthogonal to the admission floor. Do not stack it on H1.

## H4 — Analog / MS2Deepscore (out of scope)

Needs extra wheels or embeddings. Out of scope for a one-constant ablation. Do not claim Class-3 de novo is solved by retrieval.

## One major ablation this slot

Run **H1 only**. `config_patch: {"MIN_SIMILARITY": 0.12}`.
