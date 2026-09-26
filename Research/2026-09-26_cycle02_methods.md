# Research — 2026-09-26 cycle02

## Goal

Raise public MRR@25 above the last scored retrieval baseline (**0.143**) toward the live public leaderboard top (**Ozymandias31415 0.425** as of 2026-09-26T06:16Z). This cycle is the first Chicago-clock slot after 01:00 America/Chicago on 2026-09-26; Actions already used UTC-day slot 1 at 01:33Z (`TOP_PEAKS=128`, Kaggle 56565919). One major unused ablation: make the hybrid ranker **entropy-dominant**.

## Sources reviewed

1. **Li, Kind, Folz, et al., Nature Methods (2021)** — Spectral entropy outperforms MS/MS dot product for small-molecule ID; entropy similarity beat 42 alternatives on 434,287 spectra vs NIST20; **FDR < 10% at entropy similarity 0.75** on 37,299 natural-product spectra.  
   https://www.nature.com/articles/s41592-021-01331-z · https://doi.org/10.1038/s41592-021-01331-z · PDF https://yuanyue.li/project/spectral_entropy/Yuanyue-spectral_entropy.pdf
2. **Li & Fiehn, Nature Methods (2023)** — Flash Entropy Search: identity / open / neutral-loss / hybrid entropy search at library scale without accuracy loss.  
   https://www.nature.com/articles/s41592-023-02012-9 · https://pmc.ncbi.nlm.nih.gov/articles/PMC11511675/ · `ms-entropy` API https://msentropy.readthedocs.io/en/latest/entropy_search_api.html
3. **YuanyueLi/SpectralEntropy** — reference implementation of entropy + unweighted-entropy vs cosine / weighted-dot-product.  
   https://github.com/YuanyueLi/SpectralEntropy
4. **de Jonge et al., Nature Communications (2023)** — MS2Query: Spec2Vec + MS2DeepScore + precursor mass + RF re-rank for exact *and* analogue hits (no precursor prefilter). Strong when the true structure is absent from the library.  
   https://www.nature.com/articles/s41467-023-37446-4 · GNPS2 notes https://wang-bioinformatics-lab.github.io/GNPS2_Documentation/ms2query_doc/
5. **Live Kaggle public LB + Code (2026-09-26)** — top public **0.425**; public notebooks titled analog/quad-channel rankers report **0.33–0.34**, confirming that retrieval + analogue re-rank, not cosine-only library search, is what moves MRR@25.  
   https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra/leaderboard

## Methods to consider

| Priority | Method | Why it can lift MRR@25 | How (this kernel) |
|----------|--------|------------------------|-------------------|
| **P0** | **Entropy-dominant hybrid (`ENTROPY_WEIGHT=0.75`)** | Current hybrid is `0.6·entropy + 0.4·modcos`. Li 2021's operating point for FDR<10% is entropy similarity **0.75**; cosine still saturates on noisy/CE-shifted NP spectra and on the poisoned exact-dup rows. Raising the mix toward entropy re-orders the same mass-window candidates without changing coverage. | One config constant. Already implemented in `casmi26/spectrum.py:hybrid_similarity`. |
| P0 | Keep exact-dup IK ban + structure-level mass filter | v0.1 failure mode is unchanged: identical `enveda-180` spectra with train labels ≠ GT. | Already on (`EXCLUDE_EXACT_DUPLICATES=True`, backfill 80 ppm). |
| P1 | Domain-prior boost for Enveda/GNPS NP libs | Soft re-rank after retrieval; unused Actions fallback (slot 5). Weaker than changing the similarity that *selects* neighbors. | `domain_prior_boost` only. |
| P1 | Raise `MIN_SIMILARITY` toward 0.12–0.15 | Drops weak cosine ties that fill the top-25 with decoys. Risk: empty lists on sparse queries. | Next unused slot. |
| P2 | Flash Entropy identity+hybrid search | Same metric, faster / full-library open search. | Needs `ms-entropy` wheel in the offline dataset; not this slot. |
| P2 | MS2Query / MS2DeepScore analogue channel | Public 0.33+ notebooks use analogue rankers; needed when GT is absent from train. | Heavy weights, internet-off; not this slot. |
| P3 | Formula → candidate DB / de novo | Class-3 only. Retrieval cannot claim this is solved. | Out of scope. |

## Why this cycle is entropy weight, not another mass/peaks tweak

Actions 09-25 already swept **mass-tight (15/40)**, **mass-wide (35/80 + top-k 120)**, **peaks 160 / min_sim 0.05**, then 09-26 UTC slot 1 restored **TOP_PEAKS=128**. All public scores still **null**. Repeating a mass window wastes a quota slot. Entropy weight has been specified in draft Cloud PRs (0.70) but **never scored**. Literature gives a concrete target (0.75).

## Out of scope this cycle

MS2Query / Spec2Vec / MS2DeepScore weights; Flash Entropy C-extension; unconstrained LLM SMILES; claiming Class-3 de novo is solved by library retrieval.
