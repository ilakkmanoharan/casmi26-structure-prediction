# Research — 2026-09-28 cycle02

## Goal

Raise public MRR@25 above the last scored retrieval baseline (**0.143**) toward the live public leaderboard top (**Ozymandias31415 0.425** as of 2026-09-28T06:04Z). This is the first Chicago-clock slot after 01:00 America/Chicago on 2026-09-28. Actions already used UTC-day slot 1 at 00:47Z (`TOP_PEAKS=128`, Kaggle **56624265**, kernel v28). Main already has `ENTROPY_WEIGHT=0.75`, mass-wide 35/80 ppm, and `TOP_PEAKS=128`. Repeating the slot-2 fallback (`ENTROPY_WEIGHT=0.75`) would be a no-op. One unused scoring ablation: **raise `MIN_SIMILARITY`**.

## Sources reviewed

1. **Li, Kind, Folz, et al., Nature Methods (2021)** — Spectral entropy outperforms MS/MS dot product for small-molecule ID; entropy similarity beat 42 alternatives on 434,287 spectra vs NIST20; **FDR < 10% at entropy similarity 0.75** on 37,299 natural-product spectra.  
   https://www.nature.com/articles/s41592-021-01331-z · PDF https://yuanyue.li/project/spectral_entropy/Yuanyue-spectral_entropy.pdf
2. **Aron et al. / low-intensity ion weighting** — Optimal modified-cosine cutoffs for structurally similar pairs sit near **0.67–0.88**; entropy cutoffs near **0.55–0.56**. Common 0.7 cosine cutoffs are not MRR-optimal. Our current `MIN_SIMILARITY=0.05` is an order of magnitude below every published identity/analogue gate.  
   https://exa.ai/library/publication/krbqnm0jz5j
3. **de Jonge et al., Nature Communications (2023)** — MS2Query: Spec2Vec + MS2DeepScore + precursor mass + RF re-rank for exact *and* analogue hits. GNPS2 notes: scores **>0.7** are often good analogues/exact matches; **<0.6** are frequently discarded.  
   https://www.nature.com/articles/s41467-023-37446-4 · https://wang-bioinformatics-lab.github.io/GNPS2_Documentation/ms2query_doc/
4. **Xing et al., Denoising Search (2024)** — Orbitrap Astral denoising + entropy identity search; entropy 0.75 remains a stable FDR operating point after noise removal. Supports dropping low-intensity / weakly matching fragments rather than keeping every hybrid tie.  
   https://pmc.ncbi.nlm.nih.gov/articles/PMC11302682/
5. **mzmine spectral similarity docs** — Library search exposes an explicit *minimum cosine similarity*; unmatched peaks should still penalize the score (KEEP ALL AND MATCH TO ZERO). A floor is the standard way to stop decoys occupying the rank list.  
   https://mzmine.github.io/mzmine_documentation/module_docs/id_spectral_library_search/spectral-similarity-measures.html
6. **Live Kaggle public LB (2026-09-28T06:04Z)** — top **Ozymandias31415 0.425**, #2 pikachu 0.421, #3 Udam Liyanage 0.414. Confirms retrieval-only ~0.143 is far from the public frontier.  
   https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra/leaderboard

## Methods to consider

| Priority | Method | Why it can lift MRR@25 | How (this kernel) |
|----------|--------|------------------------|-------------------|
| **P0** | **Raise `MIN_SIMILARITY` 0.05 → 0.12** | After the exact-dup IK ban, weak hybrid ties (`>=0.05`) still fill the top-25 with decoys. Literature identity/analogue gates are 0.55–0.75; 0.12 is a conservative first step that drops near-noise matches without jumping to an empty-list regime. | One config constant. Gate is `casmi26/retrieve.py` (`sim >= cfg.min_similarity`). |
| P0 | Keep exact-dup IK ban + structure-level mass filter | v0.1 failure mode is unchanged: identical `enveda-180` spectra with train labels ≠ GT. | Already on. |
| P1 | Entropy-dominant hybrid (`ENTROPY_WEIGHT=0.75`) | Li 2021 FDR<10% operating point. **Already on main / last UTC slot.** | Do not resubmit. |
| P1 | Domain-prior boost for Enveda/GNPS NP libs | Soft re-rank after retrieval; unused Actions fallback (slot 5) is currently a no-op patch. | Later slot. |
| P2 | Flash Entropy / MS2Query analogue channel | Public 0.33+ notebooks use analogue rankers when GT is absent from train. | Needs offline weights; not this slot. |
| P3 | Formula → candidate DB / de novo | Class-3 only. Retrieval cannot claim this is solved. | Out of scope. |

## Why this cycle is min-similarity, not entropy/mass/peaks

Actions 09-25–09-27 already swept **mass-tight, mass-wide, peaks 160, entropy 0.75, domain-prior**. All public scores still **null** in the Kaggle list (best recorded remains 0.143). Slot-2 fallback would re-apply `ENTROPY_WEIGHT=0.75`, which is already the committed default. `MIN_SIMILARITY` has been recommended as the next unused gate since 2026-09-26 cycle02 research and has **never been scored above 0.05**.

## Out of scope this cycle

MS2Query / Spec2Vec / MS2DeepScore weights; Flash Entropy C-extension; unconstrained LLM SMILES; claiming Class-3 de novo is solved by library retrieval.
