# Research — 2026-10-31 cycle03

## Goal

Raise public MRR@25 above the v0.1 plateau (**0.143**) toward the live public frontier (~**0.50–0.52** on CLIST). This Cloud slot is the late **01:00 CDT / 06:00 UTC** cron that fired at **07:33 UTC** — after Actions already spent UTC ticket 2. Target: **library-hit admission floor**, not another replay of `PEAK_MZ_TOL=0.02` or `TOP_PEAKS=128`.

## Sources reviewed

1. **Li, Kind, Folz, Vaniya, Mehta, Fiehn — *Nat. Methods* (2021)**  
   [Spectral entropy outperforms MS/MS dot product](https://www.nature.com/articles/s41592-021-01331-z) · [eScholarship PDF](https://escholarship.org/content/qt0249w6hk/qt0249w6hk.pdf)  
   Entropy similarity beat 42 alternatives on NIST20. On 37,299 experimental natural-product spectra, **entropy similarity ≥ 0.75** yielded **FDR < 10%**. Classic metabolomics practice still uses score floors of **>0.7 or >0.8** before calling an annotation likely. Our live hybrid is already entropy-dominant (`ENTROPY_WEIGHT=0.75`) but admits any hit with hybrid score **≥ 0.05**. That is an order of magnitude below the Li/Fiehn operating point and far below the 0.7–0.8 community cutoff. Raising the floor toward **0.12** is a conservative first step: it drops obvious decoys without jumping to the 0.75 identification threshold (which would empty too many rank lists for MRR@25).

2. **Li & Fiehn — Flash Entropy Search (2023)**  
   [PMC11511675](https://pmc.ncbi.nlm.nih.gov/articles/PMC11511675/)  
   After the 1% noise cut and precursor-ion removal, Flash Entropy matches fragments inside **±20 mDa**. That window is already live (`PEAK_MZ_TOL=0.02`). The remaining unused knob on the similarity object is the admission floor, not the pair window.

3. **ms_entropy / matchms FlashSimilarity**  
   [`FlashEntropySearch.search(..., ms2_tolerance_in_da=0.02)`](https://msentropy.readthedocs.io/en/latest/entropy_search_api.html) · [matchms.similarity.FlashSimilarity](https://matchms.readthedocs.io/en/latest/_modules/matchms/similarity/FlashSimilarity.html)  
   Default fragment tolerance 0.02 Da and `noise_cutoff=0.01` already match live main. Neither library recommends admitting entropy/modcos scores of 0.05 into a top-25 ranking list.

4. **GNPS library search / MASST / Passatutto FDR**  
   [GNPS Spectral Library Search](https://lfnothias.github.io/GNPSDocumentation/librarysearch/) (default cosine **0.5**, 6 matched peaks) · [MASST](https://ccms-ucsd.github.io/GNPSDocumentation/masst/) (default cosine **0.7**) · [Scheubert et al., *Nat. Commun.* 2017 — Passatutto](https://pmc.ncbi.nlm.nih.gov/articles/PMC5684233/)  
   Living-data GNPS uses **0.7 / 6 peaks**. Passatutto FDR on 70 GNPS datasets typically lands 1% FDR at cosine **0.60–0.65** and 5% FDR at **0.50–0.55**. Our 0.05 floor is far below every published operating point. 0.12 is still a *candidate-admission* floor for MRR@25, not an annotation call — it only drops the weakest tail.

5. **CASMI / Enveda competition notes**  
   [Kaggle competition](https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra) · [CLIST standings](https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/) · [independent 2026-10-06 research write-up](https://m0-ar.github.io/casmi-2026/RESEARCH.md)  
   Metric is MRR@25. Retrieval-only cannot claim Class-3 de novo. Exact test↔train spectrum duplicates in `enveda-180` still poison rank-1 when train labels ≠ GT — exact-dup exclusion stays on. Public tops ~0.50–0.52 remain leak-sensitive; a documented honest ceiling around **0.339–0.350** is a better calibration target than CLIST rank.

6. **Public analog / ranker pipelines (community)**  
   [shiferaxa/casmi26](https://github.com/shiferaxa/casmi26) (library + analog + fragment + FPNet ranker) and score-sorted public notebooks (~**0.472–0.477**) sit well above our 0.143 retrieval plateau. They apply a real library-hit floor, not 0.05.

## Methods to consider

| Priority | Method | Why it can lift MRR@25 | How (notebook, internet off) |
|----------|--------|------------------------|------------------------------|
| **P0** | **Raise `MIN_SIMILARITY` 0.05 → 0.12** | Live admission floor is 0.05. Li/Fiehn FDR work, GNPS 0.5–0.7 defaults, and classic 0.7–0.8 cutoffs imply scores in the 0.05–0.11 band are almost all decoys. Those decoys fill the 25-slot list, so reciprocal rank of the true structure (if present at a higher score) is diluted. Raising the floor to 0.12 drops the weakest library hits without changing mass windows, peak cleaning, or the 0.75 entropy mix. | One config constant. Already wired in `casmi26/retrieve.py` (`if sim >= cfg.min_similarity`). |
| P1 | `TOP_PEAKS` 128 → 160 | Longer ladder after the 1% floor can keep diagnostic mid-intensity ions. Risk: more noise if the floor is already doing its job. | Slot-4 fallback. Do **not** reset `MIN_SIMILARITY` when trying 160. |
| P2 | CE-aware aggregation / domain prior | Already live; H-domain fallback is a no-op on current `DOMAIN_PRIOR`. | Skip. |
| P2 | MS2Query / Spec2Vec / MS2Deepscore / analog ranker | Literature analogue search; public analog notebooks sit at 0.47–0.48. | Heavy offline weights; 9h kernel budget; internet off. |
| P3 | Formula → candidate DB / de novo | Needed for Class-3 when the structure is absent or labels are poisoned. | Out of scope. Retrieval cannot solve Class-3. |

## Why this slot is the admission floor, not another slot-rotation knob

Actions already burned UTC slots 1 and 2 today:

- **H-top-peaks** (`TOP_PEAKS=128`, already live; Kaggle **57821778**, kernel v175 at ~00:44Z — before Chicago 01:00 CDT)
- **H-peak-mz** (`PEAK_MZ_TOL=0.02`, already live since 2026-10-24; Kaggle **57830376**, kernel v176 at ~07:05Z)

Slot 3 fallback on main is still **H-peak-mz**. Replaying it at the next unused hourly (**08:00 UTC**) would waste UTC ticket 3 on a no-op. The first unused constant that actually changes which library hits enter the rank list is `MIN_SIMILARITY`.

Prior Cloud H-min-sim PRs **#38–#49** already specified this ablation and stayed draft/unmerged; Actions later spent those days’ next unused slot on the fallback no-op (`PEAK_MZ_TOL=0.02`). This cycle re-implements on current main (after Actions 10-31 cycle02) and retargets Actions **slot-2 and slot-3** fallbacks to H-min-sim so a 429/no-key hourly run cannot replay 0.02.

## Out of scope this cycle

- CSV `competitions submit` (notebook-only competition).
- Claiming Class-3 de novo is solved by library retrieval.
- Training MS2Deepscore / Spec2Vec inside the kernel.
- Merging prior Cloud H-min-sim PRs #38–#49 (those stay historical; this cycle re-implements on current main).
