# Hypotheses — 2026-11-07 cycle03

## H1 (this slot) — H-top-peaks-256

**Claim:** After the live 1% intensity floor and 20 mDa pairing, clipping the fragment ladder at 128 peaks drops diagnostic mid-intensity ions on NP MS/MS. Raising `TOP_PEAKS` 128 → 256 (Flash Entropy `max_peak_num=0` bounded for the notebook) will raise identity-search hybrid scores for true structures that currently miss rank-25.

**Expected MRR direction:** up, if a non-trivial fraction of test molecules have >128 post-noise peaks that match library ions of the true InChIKey14. Flat if almost all spectra already have ≤128 peaks after `INTENSITY_FLOOR=0.01`.

**Failure mode:** more noise ions enter entropy/modcos matching and promote decoys into the top-25, lowering MRR. Entropy weighting (Li 2021) is specifically robust to that; if MRR falls, next slot should revert to 128 and try H-sim-gate instead.

**Major ablation this slot:** `TOP_PEAKS` 128 → 256 only.

## H2 — H-sim-gate (next unused after H1)

Raising `MIN_SIMILARITY` 0.05 → 0.12 drops decoys that currently fill ranks 5–25. Unmerged drafts #76–#82. Slot-4 fallback retargeted here so it is not `TOP_PEAKS=160` (a regression once 256 is live).

## H3 — H-mass-tight

`MASS_TOL_PPM` 35 → 15 (draft #83). Tighter precursor gate. Hold until H1 is scored.

## H4 — H-entropy-pure

`ENTROPY_WEIGHT` 0.75 → 1.0 (draft #84). Pure Li/Fiehn entropy. Hold until H1 is scored.

## This slot

Run **H1 only**. Do not confound with H2/H3/H4. Retrieval still does not claim Class-3 de novo.
