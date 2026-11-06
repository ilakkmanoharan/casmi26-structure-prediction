# Research — 2026-11-06 cycle02

## Goal

Raise public MRR@25 above the v0.1 plateau (**0.143**) toward the live public frontier (**~0.54** on CLIST). UTC slot 1 already spent ticket 1/5 on **H-top-peaks** (`TOP_PEAKS=128`, already live). This cycle’s unused real knob is the **hybrid similarity floor**, not another replay of already-live Flash Entropy pairing or peak-count constants.

## Sources reviewed

1. **Li, Kind, Folz, Vaniya, Mehta, Fiehn — *Nat. Methods* (2021)**  
   [Spectral entropy outperforms MS/MS dot product](https://www.nature.com/articles/s41592-021-01331-z)  
   Entropy similarity beat 42 alternatives on NIST20. On 37,299 experimental natural-product spectra, **entropy similarity ≥ 0.75** yielded **FDR < 10%**. Our mix weight is already that operating point (`ENTROPY_WEIGHT=0.75`), but the **admission gate** into the ranked list is `MIN_SIMILARITY=0.05` — an order of magnitude below the FDR-controlled identification threshold. Almost any mass-window hit therefore occupies a top-25 slot.

2. **Scheubert et al. — *Nat. Commun.* (2017)**  
   [Significance estimation for large scale metabolomics annotations](https://www.nature.com/articles/s41467-017-01318-5)  
   Spectral-matching thresholds must be project-specific; GNPS-style default score cutoffs under- or over-annotate. At cosine ~0.7, community four-star ratings implied ~1% incorrect / ~91% correct. A 0.05 hybrid floor is far below that regime and is expected to flood MRR@25 with decoys.

3. **Li & Fiehn — *Nat. Methods* (2023) / ms_entropy**  
   [Flash Entropy Search](https://www.nature.com/articles/s41592-023-02012-9) · [API `ms2_tolerance_in_da=0.02`](https://msentropy.readthedocs.io/en/latest/entropy_search_api.html)  
   Fragment pairing default is **0.02 Da**; noise cut **0.01**. Both are already live (`PEAK_MZ_TOL=0.02`, `INTENSITY_FLOOR=0.01`). Replaying them cannot change the similarity object.

4. **matchms `FlashSimilarity`**  
   [matchms.similarity.FlashSimilarity](https://matchms.readthedocs.io/en/stable/api/matchms.similarity.FlashSimilarity.html)  
   Defaults: `tolerance=0.02`, `noise_cutoff=0.01`, `score_type="spectral_entropy"`. No default as low as 0.05 for keeping a hit; identity search is gated by precursor tolerance, not a near-zero score floor.

5. **Wang et al. — *Briefings in Bioinformatics* (2024)**  
   [Ion entropy and accurate entropy-based FDR estimation](https://doi.org/10.1093/bib/bbae056)  
   Entropy-based target-decoy FDR is most accurate in the **0–0.10 FDR** band. Unfiltered libraries at low score cutoffs annotate <10% of spectra at 1% FDR, then rise at 5–10% FDR. A 0.05 admission gate is not an FDR operating point; it is an open door for mass-isobar decoys.

6. **Huber et al. / MS2Query — *Nat. Commun.* (2023)**  
   [MS2Query analogue search](https://www.nature.com/articles/s41467-023-37446-4)  
   Modified cosine collapses under multiple modifications; Spec2Vec / MS2Deepscore are stronger analogue proxies. Out of scope this slot (internet-off kernel, no extra wheels). Retrieval still cannot claim Class-3 de novo.

7. **CASMI / Enveda competition + public LB**  
   [Kaggle](https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra) · [CLIST standings](https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/) (updated ~2h before this run)  
   Metric is MRR@25. Public top: **Shehab Alshehabi 0.54**, Savko 0.53, Oleksandr Parfionov 0.52. Gap vs 0.143 is not a missing `TOP_PEAKS` or `PEAK_MZ_TOL` constant.

## Methods to consider

| Priority | Method | Why it can lift MRR@25 | How (notebook, internet off) |
|----------|--------|------------------------|------------------------------|
| **P0** | **Raise `MIN_SIMILARITY` 0.05 → 0.12** | Live 0.05 lets weak hybrid scores (mostly decoys per Li/Fiehn and Scheubert FDR work) fill 25 ranks. MRR@25 only rewards the *first* correct InChIKey14; packing the list with 0.05–0.11 mass-isobars pushes GT down or off the list. 0.12 is a conservative step toward the 0.7 identification regime without jumping to 0.75 (which would empty many CE-mismatched true hits). | One config constant. Already wired in `retrieve_for_spectrum` (`if sim >= cfg.min_similarity`). |
| P1 | `TOP_PEAKS` 128 → 160 | Longer ladder after the 1% floor. Slot-4 fallback already tries 160 + min_sim 0.05. Do not stack on P0. | Next unused slot after H-sim-gate. |
| P1 | Tighter structure-level `MASS_TOL_PPM` (35 → 10–15) | Orbitrap-class IDs are typically ≤10 ppm; 35 ppm admits extra formulas. Tried once (H-mass-tight 15/40) then reverted by H-mass-wide replays. | Later slot; confounds H-sim-gate. |
| P2 | `ENTROPY_WEIGHT` 0.75 → 1.0 | Pure entropy. Mix weight already matches Li 2021 FDR point; the admission gate is the unused lever. | Skip. |
| P2 | MS2Query / Spec2Vec / MS2Deepscore | Public analog notebooks ~0.43–0.46. | Extra weights; 9h kernel; internet off. |
| P3 | Formula → candidate DB / de novo | Needed for Class-3 when the structure is absent or labels are poisoned. | Out of scope. Retrieval cannot solve Class-3. |

## Why this slot is the similarity floor, not another slot-rotation knob

Actions already burned UTC slot 1 today:

- **H-top-peaks** (`TOP_PEAKS=128`, already live; Kaggle **58042294**, kernel **v198** at 02:22Z)

Slot 2’s fallback is **H-peak-mz** (`PEAK_MZ_TOL=0.02`) — also already live. Replaying it wastes UTC ticket 2. The first unused constant that actually changes *which* library hits enter aggregation is `MIN_SIMILARITY`.

Cloud PRs **#67–#76** (2026-11-04/05) already specified this ablation and stayed **draft/unmerged**; Actions later spent those days’ next unused slot on the fallback no-op (`PEAK_MZ_TOL=0.02` or `TOP_PEAKS=128`). This cycle re-implements on current main and retargets the Actions slot-2 and slot-3 fallbacks so a 429/no-key hourly run cannot replay 0.02 Da.

## Out of scope this cycle

- CSV `competitions submit` (notebook-only competition).
- Claiming Class-3 de novo is solved by library retrieval.
- Training MS2Deepscore / Spec2Vec inside the kernel.
- Merging prior Cloud H-min-sim PRs #67–#76 (those stay historical; this cycle re-implements on current main).
