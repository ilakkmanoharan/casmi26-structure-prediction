# Hypotheses — 2026-11-04 cycle03

## H1 — H-min-sim (run this slot)

**Claim.** Raising `MIN_SIMILARITY` from **0.05** to **0.12** drops weak hybrid library hits that currently pad `TOP_K_SPECTRA=120` and the MRR@25 list, improving public MRR@25 versus the 0.143 plateau.

**Mechanism.** `retrieve_for_spectrum` keeps a hit only when `sim >= cfg.min_similarity` (`casmi26/retrieve.py`). At 0.05, almost any two spectra that share a couple of 20 mDa-paired fragments enter the candidate pool. Structure aggregation then fills 25 slots with decoys. 0.12 is a conservative step: above MSEntropy’s 0.1 return floor, well below Li/Fiehn 0.75 / JASMS 0.55 / GNPS 0.5 / MS2Query 0.6 identification bands.

**Expected MRR direction.** Small-to-moderate positive if decoy packing is the bottleneck after exact-dup exclusion. Failure mode: sparse or cross-instrument true-structure near-matches fall below 0.12 and lists go empty / fallback-heavy (MRR down). That is acceptable to measure — it is a real ablation, unlike replaying `PEAK_MZ_TOL=0.02`.

## H2 — TOP_PEAKS 128 → 160 (next unused)

**Claim.** A longer ladder after the 1% intensity floor can keep diagnostic mid-intensity ions.

**Why not now.** Already submitted as 11-03 cycle04 (57961369) then undone by 11-04 cycle01. Do not stack it on H1. Slot-4 fallback tries 160 only after this merge.

## H3 — Analog / mass-shift channel (later)

**Claim.** Public 0.33→0.54 gains came from analog transfer / fingerprint / fusion.

**Why not now.** Needs a new retrieve path, not a one-constant ablation.

## H4 — Entropy ID cutoff 0.55–0.75 (out of scope)

Li/Fiehn / JASMS identification bands. Too aggressive for our hybrid + cross-library CE mix. Do not claim Class-3 de novo is solved by retrieval.

## One major ablation this slot

Run **H1 only**. `config_patch: {"MIN_SIMILARITY": 0.12}`.
