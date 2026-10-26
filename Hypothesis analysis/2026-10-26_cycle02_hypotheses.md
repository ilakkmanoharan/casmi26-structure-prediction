# Hypotheses — 2026-10-26 cycle02

## H1 (this slot) — H-min-sim

Raising `MIN_SIMILARITY` from **0.05 → 0.12** drops near-noise hybrid entropy/modcos library hits before they enter `top_k_spectra`. The ranker then aggregates fewer decoys, so the true analog (when it exists and scores ≥ 0.12) moves up the 25-candidate list and public MRR@25 rises.

- **Expected direction:** MRR@25 up vs the 0.143 plateau *if* true analog support usually sits above 0.12. Neutral if most of our current rank-1s are already high-similarity (poisoned exact-dup path or strong identity hits).
- **Failure mode:** True analog / CE-shifted matches cluster in 0.05–0.12 and get dropped, emptying `top_k` for some queries and hurting MRR. Mitigate by keeping 0.12 far below Li/Fiehn identity 0.75 and by leaving `TOP_K=120` / `TOP_PEAKS=128` unchanged (one factor).
- **Why not 0.75:** That cutoff is for high-confidence *identity* annotation FDR, not analog MRR@25.

## H2 — H-peaks (next unused after this)

`TOP_PEAKS` 128 → 160 after the 1% intensity floor. Flash Entropy prefers not to hard-cap the ladder. Submitted yesterday as cycle04, then reset to 128 by today’s UTC cycle01. Retarget Actions **slot-3** to `{"TOP_PEAKS": 160}` only (do not reset `MIN_SIMILARITY`).

## H3 — H-peak-mz (reject this slot)

`PEAK_MZ_TOL=0.02` is already live. Replaying it is a documented wasted ticket (2026-10-25 cycle02 and cycle03).

## H4 — retrieval ceiling (not this slot)

Even a perfect admission floor cannot recover Class-3 structures that are absent from the library or whose only row is a poisoned `enveda-180` exact duplicate. Do not claim de novo is solved.

## Ablation for this slot

**One major change:** `MIN_SIMILARITY=0.12` (H1). No peak-count, mass-window, or domain-prior edits in the same kernel.
