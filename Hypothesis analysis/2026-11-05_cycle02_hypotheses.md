# Hypotheses — 2026-11-05 cycle02

## H1 — H-entropy-pure (run this slot)

**Claim.** Setting `ENTROPY_WEIGHT` from **0.75** to **1.0** ranks candidates with Li/Fiehn entropy similarity **alone** (no 25% modified cosine) and improves public MRR@25 versus the 0.143 plateau.

**Mechanism.** `hybrid_similarity` is `w * entropy_similarity + (1-w) * modified_cosine`. At `w=0.75`, every library hit still gets a 25% vote from cosine, which Li 2021 showed is dominated by shared-fragment saturation and single noise ions. The 0.75 figure in that paper is an **FDR cutoff on the entropy score**, not a mix weight. Setting `w=1.0` makes `hybrid_similarity` identical to `entropy_similarity` and re-orders the same 35 ppm / 20 mDa / 128-peak candidate pool. Exact-dup exclusion, mass window, and peak cleaning stay fixed.

**Expected MRR direction.** Small-to-moderate positive if cosine is currently promoting decoys that share a few intense fragments with the query. Near-zero if entropy and cosine already agree on the top-25. Failure mode: CE-shifted true hits that cosine’s precursor-neutral-loss term was rescuing drop in rank (MRR down). That is acceptable to measure — it is a real ablation, unlike replaying `PEAK_MZ_TOL=0.02` or `TOP_PEAKS=128`.

## H2 — MIN_SIMILARITY 0.05 → 0.12 (next unused / slot-3 fallback)

**Claim.** Li/Fiehn FDR work implies very low scores are mostly decoys. Raising the floor may stop packing the top-25 with noise.

**Why not now.** Confounds H1: a tighter score floor plus a new score function moves two knobs. Cloud PR #72 already specified this ablation; measure pure entropy first.

## H3 — TOP_PEAKS 128 → 160 (slot-4 fallback)

**Claim.** A longer ladder after the 1% intensity floor can keep diagnostic mid-intensity ions.

**Why not now.** Do not stack it on H1. Slot-4 fallback tries 160 peaks only (no `MIN_SIMILARITY` rollback).

## H4 — Analog / MS2Deepscore (out of scope)

Needs extra wheels or embeddings. Out of scope for a one-constant ablation. Do not claim Class-3 de novo is solved by retrieval.

## One major ablation this slot

Run **H1 only**. `config_patch: {"ENTROPY_WEIGHT": 1.0}`.
