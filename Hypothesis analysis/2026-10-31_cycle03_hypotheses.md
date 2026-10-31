# Hypotheses 2026-10-31_cycle03

## H1 — H-min-sim (run this slot)

**Claim.** Raising `MIN_SIMILARITY` from **0.05** to **0.12** drops weak hybrid entropy/modcos decoys from `TOP_K_SPECTRA=120` so true-structure near-matches can occupy rank 1–5 and raise public MRR@25 versus the 0.143 plateau.

**Mechanism.** `retrieve_for_spectrum` (`casmi26/retrieve.py`) keeps every library hit with `sim >= cfg.min_similarity`. At 0.05 the list fills with cross-library noise that still aggregates into the top-25. 0.12 is well above that noise floor and well below Li/Fiehn 0.75, de Jonge entropy ~0.55, and MS2Query’s “discard below 0.6” band, so recall on CE-shifted true matches should survive.

**Expected MRR direction.** Small positive if the top-25 is currently packed with weak decoys; near-zero if true-structure scores already sit well above 0.12. Failure mode: true matches that only score 0.05–0.12 disappear and MRR drops. That is acceptable to measure — it is a real ablation, unlike replaying `PEAK_MZ_TOL=0.02`.

## H2 — TOP_PEAKS 128 → 160 (next unused after merge)

**Claim.** A longer ladder after the 1% intensity floor can keep diagnostic mid-intensity ions.

**Why not now.** Confounds H1. Slot-4 fallback should try 160 **without** resetting `MIN_SIMILARITY`.

## H3 — Analog / mass-shift channel (later)

**Claim.** Public 0.33→0.46 gains came from analog transfer, not from another library-search knob.

**Why not now.** Larger than a one-constant slot. Do not claim Class-3 de novo is solved by retrieval.

## H4 — Entropy ID cutoff 0.55–0.75 (too aggressive)

Would empty many candidate lists on our hybrid + cross-library CE mix. Not this slot.

## One major ablation this slot

Run **H1 only**. `config_patch: {"MIN_SIMILARITY": 0.12}`.
