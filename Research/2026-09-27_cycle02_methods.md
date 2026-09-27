# Research — 2026-09-27 cycle02

## Goal

Raise public MRR@25 above the last scored retrieval baseline (**0.143**) toward the live public leaderboard top (**Ozymandias31415 0.425** as of 2026-09-27T06:05Z). This Cloud run is the first Chicago-clock slot after **01:00 America/Chicago** on 2026-09-27. Actions already used UTC-day slot 1 at 01:33Z (`TOP_PEAKS=128`, Kaggle 56594353). One major unused ablation among existing `casmi26/config.py` constants: raise the neighbor **similarity floor**.

## Sources reviewed

1. **Li, Kind, Folz, et al., Nature Methods (2021)** — Spectral entropy outperforms 42 MS/MS similarity algorithms including dot product on 434,287 spectra vs NIST20. On 37,299 natural-product spectra, **FDR < 10% at entropy similarity 0.75**. Low-score neighbors are mostly decoys; a floor well below the identity operating point still drops noise without requiring 0.75 as a hard retrieval cutoff.  
   https://www.nature.com/articles/s41592-021-01331-z · https://doi.org/10.1038/s41592-021-01331-z · PDF https://yuanyue.li/project/spectral_entropy/Yuanyue-spectral_entropy.pdf
2. **Li & Fiehn, Nature Methods (2023)** — Flash Entropy Search: identity / open / neutral-loss / hybrid entropy search at library scale. Identity search still uses a similarity cutoff; open/hybrid search is for analogues, not for dumping near-zero cosine ties into the top-25.  
   https://www.nature.com/articles/s41592-023-02012-9 · https://pmc.ncbi.nlm.nih.gov/articles/PMC11511675/
3. **Scheubert et al., Nature Communications (2017)** — Passatutto / target-decoy FDR for metabolomics spectral matching. Score thresholds matter: ranking every mass-window hit (including ~0.05 hybrid ties) inflates false annotations.  
   https://www.nature.com/articles/s41467-017-01318-5
4. **de Jonge et al., Nature Communications (2023)** — MS2Query: no precursor prefilter; MS2DeepScore top-2000 then RF re-rank with Spec2Vec + Δm/z. Public CASMI notebooks in the 0.33–0.34 band advertise analogue / multi-channel rankers. Heavy weights; internet-off kernel cannot add this this slot.  
   https://www.nature.com/articles/s41467-023-37446-4 · https://github.com/iomega/ms2query
5. **Live Kaggle public LB + Code (2026-09-27T06:05Z)** — top public **0.425** (Ozymandias31415); #2 pikachu 0.421; #3 Udam Liyanage 0.412. Public notebooks titled analog/quad-channel rankers report **~0.33–0.34**.  
   https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra/leaderboard

## Methods to consider

| Priority | Method | Why it can lift MRR@25 | How (this kernel) |
|----------|--------|------------------------|-------------------|
| **P0** | **Raise `MIN_SIMILARITY` 0.05 → 0.12** | Hybrid is now entropy-dominant (`ENTROPY_WEIGHT=0.75`). Neighbors with hybrid < 0.12 are far below Li 2021's 0.75 identity operating point and typically fill the top-25 with mass-window decoys after the exact-dup ban. Raising the floor re-ranks the same 128-peak, 35/80 ppm search without changing coverage of real near-matches. | One config constant. Applied in `casmi26/retrieve.py:retrieve_for_spectrum` (`sim >= cfg.min_similarity`). Backfill uses the same floor; ethanol placeholder still prevents empty lists. |
| P0 | Keep exact-dup IK ban + structure-level mass filter | v0.1 failure mode is unchanged: identical `enveda-180` spectra with train labels ≠ GT. | Already on (`EXCLUDE_EXACT_DUPLICATES=True`, backfill 80 ppm). |
| P1 | Domain-prior boost for Enveda/GNPS NP libs | Soft re-rank after retrieval. Actions already ran H-domain on 2026-09-26 cycle05. | Skip; already used. |
| P1 | `TOP_PEAKS` 160 | Extra fragment ions; already swept 2026-09-25/26 cycle04. | Skip. |
| P2 | Flash Entropy identity+hybrid search | Same metric, faster / full-library open search. | Needs `ms-entropy` wheel in the offline dataset; not this slot. |
| P2 | MS2Query / MS2DeepScore analogue channel | Public 0.33+ notebooks use analogue rankers; needed when GT is absent from train. | Heavy weights, internet-off; not this slot. |
| P3 | Formula → candidate DB / de novo | Class-3 only. Retrieval cannot claim this is solved. | Out of scope. |

## Why this cycle is the similarity floor, not another mass/peaks/entropy tweak

Actions 09-25 swept **mass-tight (15/40)**, **mass-wide (35/80 + top-k 120)**, **peaks 160 / min_sim 0.05**, then 09-26/09-27 UTC slot 1 restored **TOP_PEAKS=128**. 09-26 cycle02 landed **ENTROPY_WEIGHT=0.75**. Current main already has that mix plus mass-wide + 128 peaks. Slot-2 fallback is still `H-entropy` (no-op). All later public scores still **null**. Repeating entropy/mass/peaks wastes a quota slot.

`MIN_SIMILARITY` has never been the *major* factor: cycle04 only restated `0.05` while changing `TOP_PEAKS`. Prior research (2026-09-26 cycle02 H3) reserved **0.12–0.15** as the next unused lever. 0.12 is conservative vs Li's 0.75 identity cutoff: it drops weak ties, not true analogues that still score 0.2–0.6.

## Out of scope this cycle

MS2Query / Spec2Vec / MS2DeepScore weights; Flash Entropy C-extension; unconstrained LLM SMILES; claiming Class-3 de novo is solved by library retrieval.
