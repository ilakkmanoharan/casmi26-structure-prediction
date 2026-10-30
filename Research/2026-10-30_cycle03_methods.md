# Research — 2026-10-30 cycle03

## Goal

Raise public MRR@25 above the v0.1 plateau (**0.143**) toward the live public frontier (~**0.50–0.52** on CLIST). This Cloud slot is **07:00 CDT / 12:02 UTC** — the last suggested Cloud cadence of the Chicago day. Actions already spent UTC tickets 1–2 on already-live knobs. Target: **library-hit admission floor**, not another replay of `PEAK_MZ_TOL=0.02` or `TOP_PEAKS=128`.

## Sources reviewed

1. **Li, Kind, Folz, Vaniya, Mehta, Fiehn — *Nat. Methods* (2021)**  
   [Spectral entropy outperforms MS/MS dot product](https://www.nature.com/articles/s41592-021-01331-z) · [eScholarship PDF](https://escholarship.org/content/qt0249w6hk/qt0249w6hk.pdf)  
   Entropy similarity beat 42 alternatives on NIST20. On 37,299 experimental natural-product spectra, **entropy similarity ≥ 0.75** yielded **FDR < 10%**. Classic metabolomics practice still uses score floors of **>0.7 or >0.8** before calling an annotation likely. Our live hybrid is already entropy-dominant (`ENTROPY_WEIGHT=0.75`) but admits any hit with hybrid score **≥ 0.05**. That is an order of magnitude below the Li/Fiehn operating point and far below the 0.7–0.8 community cutoff. Raising the floor toward **0.12** is a conservative first step: it drops obvious decoys without jumping to the 0.75 identification threshold (which would empty too many rank lists for MRR@25).

2. **Li & Fiehn — Flash Entropy Search (2023)**  
   [PMC11511675](https://pmc.ncbi.nlm.nih.gov/articles/PMC11511675/)  
   After the 1% noise cut and precursor-ion removal, Flash Entropy matches fragments in a **±20 mDa** window. That pair window is already live (`PEAK_MZ_TOL=0.02`). The remaining mismatch vs the paper is the **admission threshold**, not the pair window.

3. **ms_entropy / matchms defaults**  
   [`FlashEntropySearch.search(..., ms2_tolerance_in_da=0.02)`](https://msentropy.readthedocs.io/en/latest/entropy_search_api.html) · [matchms.similarity.FlashSimilarity](https://matchms.readthedocs.io/en/stable/api/matchms.similarity.FlashSimilarity.html)  
   Default fragment tolerance **0.02 Da**; cleanup `noise_cutoff=0.01`. Both already live. Neither library recommends keeping cosine/entropy scores of 0.05 in a top-25.

4. **de Jonge, Huber et al. — *Nat. Commun.* (2023)**  
   [MS2Query: reliable analogue search](https://www.nature.com/articles/s41467-023-37446-4)  
   Embedding analogue search (MS2Deepscore + Spec2Vec + precursor *m/z*) finds reliable analogues for ~35% of spectra (mean Tanimoto 0.63) vs modified-cosine 0.45 at the same recall. Strong P2 for later; needs offline weights and is out of scope for a one-constant internet-off ablation.

5. **CASMI / Enveda competition notes**  
   [Kaggle competition](https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra) · [CLIST standings](https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/) · [Pilkwang overview](https://pilkwangkim.github.io/posts/CASMI-2026-From-Mass-Spectra-to-Molecular-Structures/)  
   Metric is MRR@25. Retrieval-only cannot claim Class-3 de novo. Exact test↔train spectrum duplicates in `enveda-180` still poison rank-1 when train labels ≠ GT — exact-dup exclusion stays on.

6. **Public analog notebooks (community, ~2026-10-30)**  
   Public notebooks now badge **0.472–0.477** (e.g. “CASMI26 LB 0.477 | 0.472 Weights + Fragment Check”, “CASMI 2026 Flagship Hybrid SOTA” 0.472). They typically use analogue expansion, not a 0.05 hybrid floor. CLIST page (updated ~11 h before 12:02Z): **Parfionov 0.52**, **Savko 0.51**, pikachu / Shehab / CHU1PC **0.50**.

## Methods to consider

| Priority | Method | Why it can lift MRR@25 | How (notebook, internet off) |
|----------|--------|------------------------|------------------------------|
| **P0** | **Raise `MIN_SIMILARITY` 0.05 → 0.12** | Live admission floor is 0.05. Li/Fiehn FDR work and classic 0.7–0.8 cutoffs imply scores in the 0.05–0.11 band are almost all decoys. Those decoys fill the 25-slot list, so reciprocal rank of the true structure (if present at a higher score) is diluted. Raising the floor to 0.12 drops the weakest library hits without changing mass windows, peak cleaning, or the 0.75 entropy mix. | One config constant. Already wired in `casmi26/retrieve.py` (`if sim >= cfg.min_similarity`). |
| P1 | `TOP_PEAKS` 128 → 160 | Longer ladder after the 1% floor can keep diagnostic mid-intensity ions. Risk: more noise if the floor is already doing its job. | Slot-4 fallback. Do **not** reset `MIN_SIMILARITY` when trying 160. |
| P2 | CE-aware aggregation / domain prior | Already live; H-domain fallback is a no-op on current `DOMAIN_PRIOR`. | Skip. |
| P2 | MS2Query / Spec2Vec / MS2Deepscore | Literature analogue search; public analog notebooks sit at 0.47–0.48. | Heavy offline weights; 9h kernel budget; internet off. |
| P3 | Formula → candidate DB / de novo | Needed for Class-3 when the structure is absent or labels are poisoned. | Out of scope. Retrieval cannot solve Class-3. |

## Why this slot is the admission floor, not another slot-rotation knob

Actions already burned UTC slots 1–2 today:

- **H-top-peaks** (`TOP_PEAKS=128`, already live; Kaggle **57789094**, kernel v171 at ~02:00Z)
- **H-peak-mz** (`PEAK_MZ_TOL=0.02`, already live; Kaggle **57799491**, kernel v172 at ~08:36Z)

Slot 2 and slot 3 fallbacks on main are still **H-peak-mz** (`PEAK_MZ_TOL=0.02`). 09:00, 10:00, and 11:00 UTC `casmi-loop` hours did not fire. Replaying the slot-3 fallback would waste UTC ticket 3 on a no-op. The first unused constant that actually changes which library hits enter the rank list is `MIN_SIMILARITY`.

Prior Cloud H-min-sim PRs **#38–#47** already specified this ablation and stayed draft/unmerged; Actions later spent those days’ next unused slot on the fallback no-op. This cycle re-implements on current main (after Actions cycle02) and retargets Actions **slot-2 and slot-3** fallbacks to H-min-sim so a 429/no-key hourly run cannot replay 0.02.

## Out of scope this cycle

- CSV `competitions submit` (notebook-only competition).
- Claiming Class-3 de novo is solved by library retrieval.
- Training MS2Deepscore / Spec2Vec inside the kernel.
- Merging prior Cloud H-min-sim PRs #38–#47 (those stay historical; this cycle re-implements on current main).
