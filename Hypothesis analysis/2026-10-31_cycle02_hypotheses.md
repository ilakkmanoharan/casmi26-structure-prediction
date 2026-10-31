# Hypotheses — 2026-10-31 cycle02

## H1 — H-min-sim (run this slot)

**Claim.** Raising `MIN_SIMILARITY` from **0.05** to **0.12** drops weak hybrid entropy/modcos library hits that currently pad the top-25 with decoys, improving public MRR@25 versus the 0.143 plateau.

**Mechanism.** `casmi26/retrieve.py` keeps a library spectrum only when `hybrid_similarity(...) >= cfg.min_similarity`. At 0.05, noisy or CE-shifted decoys from GNPS / MassBank / MONA / Enveda still enter `scores` and occupy rank slots. Li/Fiehn (2021) treat entropy similarity **0.75** as the FDR<10% operating point; GNPS living-data uses **0.7 / 6 peaks**; Passatutto 5% FDR typically sits at cosine **0.50–0.55**. 0.12 is a conservative first step: it removes the weakest tail without emptying sparse queries the way a 0.75 floor would. Mass windows, peak cleaning, fragment *m/z* tolerance (already 0.02), and the 0.75 entropy mix stay fixed.

**Expected MRR direction.** Small-to-moderate positive if decoy-padding of the top-25 is the bottleneck; near-zero or slightly negative if true-structure near-matches currently score in 0.05–0.11 and get dropped (empty or shorter lists → MRR down). That is acceptable to measure — it is a real ablation, unlike replaying `PEAK_MZ_TOL=0.02` or `TOP_PEAKS=128`.

## H2 — TOP_PEAKS 128 → 160 (next unused / slot-4)

**Claim.** A longer ladder after the 1% intensity floor can keep diagnostic mid-intensity ions.

**Why not now.** Confounds H1 if stacked. Slot-4 fallback should try 160 **without** resetting `MIN_SIMILARITY`. After H1 merges, this is the next unused real ablation.

## H3 — Replay PEAK_MZ_TOL=0.02 (do not run)

Already live since 2026-10-24. Slot-2/3 fallbacks on main still point here. Replaying it wastes a UTC ticket. Do not run.

## H4 — Analog / MS2Deepscore (out of scope)

Needs extra wheels or embeddings. Out of scope for a one-constant ablation. Do not claim Class-3 de novo is solved by retrieval.

## One major ablation this slot

Run **H1 only**. `config_patch: {"MIN_SIMILARITY": 0.12}`.
