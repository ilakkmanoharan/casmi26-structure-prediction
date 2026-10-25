# Hypotheses — 2026-10-25 cycle02

## H1 — H-peaks (run this slot)

**Claim.** Raising `TOP_PEAKS` from **128** to **160** keeps more mid-intensity diagnostic ions after the live 1% floor and 20 mDa fragment window, improving public MRR@25 versus the 0.143 plateau.

**Mechanism.** `clean_spectrum` normalizes to max intensity, drops ions below `INTENSITY_FLOOR=0.01`, then keeps the tallest `TOP_PEAKS`. Index and retrieve both call this cleaner, so library and query stay consistent. Flash Entropy / ms_entropy default `max_peak_num=None`; 128 is an arbitrary leftover cap from the “restore the ladder from 5” era. The 2024 JASMS low-intensity weighting paper argues those extra ions carry structure. Now that `PEAK_MZ_TOL=0.02` can pair 12–18 mDa centroid disagreements, the extra 32 ions are no longer dead weight.

**Expected MRR direction.** Small-to-moderate positive if true-structure recall is limited by discarded mid-intensity fragments; near-zero if the first 128 already dominate entropy/modcos. Failure mode: more noise ions inflate decoy similarities and push GT down the list (MRR down). That is acceptable to measure — it is a real ablation, unlike replaying `PEAK_MZ_TOL=0.02`.

## H2 — MIN_SIMILARITY 0.05 → 0.12 (next unused)

**Claim.** Li/Fiehn FDR work implies very low hybrid scores are mostly decoys. Raising the floor may stop packing the top-25 with noise.

**Why not now.** Confounds H1: a tighter score floor plus a longer ladder moves two knobs. Measure the peak cap first. Retarget slot-3 fallback to this hypothesis so the following unused hour does not replay H-peak-mz.

## H3 — Still-wider peak cap (200 / None)

**Claim.** Closer to ms_entropy `max_peak_num=None`.

**Why not now.** Kernel time and noise risk. Measure 160 first.

## H4 — Analog / MS2Deepscore (out of scope)

Needs extra wheels or embeddings. Out of scope for a one-constant ablation. Do not claim Class-3 de novo is solved by retrieval.

## One major ablation this slot

Run **H1 only**. `config_patch: {"TOP_PEAKS": 160}`.
