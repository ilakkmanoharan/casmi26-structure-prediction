# Hypotheses — 2026-11-05 cycle02

## H1 — Higher hybrid similarity floor (THIS SLOT)

**Statement.** Raising `MIN_SIMILARITY` from 0.05 → **0.12** drops near-zero hybrid ties from the per-query top-120 so true-structure near-matches occupy more of the 25-SMILES list, raising public MRR@25 vs the last scored 0.143 retrieval baseline.

**Why.** After Flash Entropy 20 mDa pairing and the 128-peak ladder, `hybrid_similarity` (`0.75·entropy + 0.25·modcos`) routinely scores isobaric decoys in the 0.05–0.11 band on two or three shared mid-intensity ions. Those rows currently enter `retrieve.py`'s candidate pool. Flash Entropy's documented `min_similarity=0.01` is a numerical noise gate; Li et al. 2021's **0.75** is an identity-level FDR operating point that would empty most CE-shifted NP lists. 0.12 sits between those two published numbers and is the smallest unused constant change that actually filters the list.

**Expected MRR direction.** Up vs 0.143 if decoys in 0.05–0.11 were crowding rank-1/2 slots. Neutral if public scoring stays delayed (every 11-01…11-05 submit still `publicScore=null`). Down if sparse 2–3 peak queries lose their only library neighbors and return empty / mass-only backfill.

**Failure mode.** Empty candidate lists on noisy or precursor-only spectra. Mitigant: mass-window backfill at 80 ppm and `TOP_K=120` stay unchanged; 0.12 is well below the 0.5 / 0.75 identity gates in JASMS 2024 / Li 2021.

## H2 — Tighter precursor mass window (next unused real ablation)

`MASS_TOL_PPM` 35 → 10 (keep backfill 80). After the floor is raised, the 35 ppm identity window is the next decoy source. Do **not** run this in the same slot.

## H3 — Pure entropy (later slot)

`ENTROPY_WEIGHT` 0.75 → 1.0. Draft Cloud PR #73. Only informative after H1 has actually been *submitted*, not just drafted.

## H4 — Analog / MS2Query channel (not this kernel)

Needed for Class-2/3. Requires extra wheels or embeddings. Out of scope. Retrieval cannot claim Class-3 de novo is solved.

## Ablation this slot

**Run H1 only.** `config_patch = {"MIN_SIMILARITY": 0.12}`.
