# Research — 2026-11-07 cycle02

## Goal

Raise public MRR@25 above the v0.1 plateau (**0.143**) toward the live public frontier (~**0.54** on CLIST). Actions already spent UTC ticket 1 today on a no-op (`TOP_PEAKS=128`, already live). This Cloud slot is the first unused **real** ablation: raise the hybrid-similarity floor that currently packs the top-25 with weak decoys.

## Sources reviewed

1. **Li, Kind, Folz, Vaniya, Mehta, Fiehn — *Nat. Methods* (2021)**  
   [Spectral entropy outperforms MS/MS dot product](https://www.nature.com/articles/s41592-021-01331-z) · [author PDF](https://yuanyue.li/project/spectral_entropy/Yuanyue-spectral_entropy.pdf)  
   Entropy similarity beat 42 alternatives on NIST20. On 37,299 experimental natural-product spectra, **entropy similarity ≥ 0.75** yielded **FDR < 10%**. The paper also states similarity scores **> 0.75** should be used for untargeted ID. Our mix weight is already `ENTROPY_WEIGHT=0.75`; the **admission floor** into the rank list is still `MIN_SIMILARITY=0.05` — far below any published FDR operating point. Weak hybrid scores in the 0.05–0.12 band are expected to be mostly decoys, yet they still consume top-25 slots after exact-dup exclusion.

2. **Li & Fiehn — Flash Entropy / ms_entropy (2023)**  
   [ms_entropy entropy similarity](https://msentropy.readthedocs.io/en/latest/classical_entropy_similarity.html)  
   Default fragment window **0.02 Da**, 1% noise cut. Those cleaning defaults are already live (`PEAK_MZ_TOL=0.02`, `INTENSITY_FLOOR=0.01`). Remaining mismatch vs the literature pipeline is the **score gate**, not pairing or noise.

3. **matchms `FlashSimilarity` / `Entropy`**  
   [matchms.similarity.FlashSimilarity](https://matchms.readthedocs.io/en/stable/api/matchms.similarity.html) (default `tolerance=0.02`, `noise_cutoff=0.01`)  
   Confirms the live fragment window and 1% floor. Does not recommend admitting entropy/cosine scores near 0.05 into a 25-candidate list.

4. **CASMI / Enveda competition notes**  
   [Kaggle competition](https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra) · [CLIST standings](https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/)  
   Metric is MRR@25. Retrieval-only cannot claim Class-3 de novo. Exact test↔train spectrum duplicates in `enveda-180` still poison rank-1 when train labels ≠ GT — exact-dup exclusion stays on. Public top (CLIST ~4h stale at 2026-11-07T06:00Z): **Shehab Alshehabi 0.54**, Savko 0.53, Oleksandr Parfionov 0.52, democat 0.51, pikachu / Paweł Biernat / CHU1PC 0.50.

5. **Public analog / ensemble notebooks (community)**  
   Analog-propagation notebooks historically ~0.43–0.46; [enveda-0480-ensemble](https://www.kaggle.com/code/ndaedzomukhuba/enveda-0480-ensemble) reports ~0.480 with neural + PubChem-prior reranking. Those stacks are out of scope for a one-constant, internet-off kernel ablation.

## Methods to consider

| Priority | Method | Why it can lift MRR@25 | How (notebook, internet off) |
|----------|--------|------------------------|------------------------------|
| **P0** | **Raise `MIN_SIMILARITY` 0.05 → 0.12** | After exact-dup ban, `retrieve_for_spectrum` still admits hybrid scores ≥ 0.05 into `top_k_spectra`. Li/Fiehn FDR work says scores that low are mostly decoys; they crowd the 25-slot MRR list and bury true near-matches that survive the 0.02 Da window. 0.12 is a moderate gate (not the 0.75 ID cutoff, which would empty sparse queries). | One config constant. Gate is already `if sim >= cfg.min_similarity` in `casmi26/retrieve.py`. |
| P1 | Pure entropy (`ENTROPY_WEIGHT` 0.75 → 1.0) | Drops the 0.25 modified-cosine term that saturates on noisy NP spectra. Mix is already at Li's 0.75 operating point; measure the floor first. | Next unused slot. |
| P1 | Tighter precursor `MASS_TOL_PPM` 35 → 15 | Orbitrap-class precursors are usually ≪ 35 ppm; a wide window adds same-mass decoys. Confounds the score-floor test. | Later slot. |
| P2 | `TOP_K_SPECTRA_PER_QUERY` 120 → 200 | More CE/adduct support after the floor is raised. | After H-sim-gate. |
| P2 | MS2Query / Spec2Vec / MS2Deepscore | Strong analog ranking in literature and public 0.43–0.48 notebooks. | Heavy offline weights; 9h kernel budget; internet off. |
| P3 | Formula → candidate DB / de novo | Needed for Class-3 when the structure is absent or labels are poisoned. | Out of scope. Retrieval cannot solve Class-3. |

## Why this slot is the similarity floor, not another slot-rotation knob

Actions already burned UTC slot 1 today and the last four Chicago-day tickets on no-ops or already-live constants:

- **H-top-peaks** (`TOP_PEAKS=128`, already live; Kaggle **58076904**, kernel v202 at 02:53Z)
- **H-peak-mz** (`PEAK_MZ_TOL=0.02`, already live; 58055178 / 58065731)
- **H-peaks** (`TOP_PEAKS=160`, `MIN_SIMILARITY=0.05`; Kaggle **58071327**, kernel v201 at 23:09Z — git push of that cycle failed)

Slot 2’s fallback is still **H-peak-mz** (`PEAK_MZ_TOL=0.02`) — a no-op. Replaying it would waste UTC ticket 2. The first unused constant that actually changes who enters the top-25 is `MIN_SIMILARITY`.

## Out of scope this cycle

- CSV `competitions submit` (notebook-only competition).
- Claiming Class-3 de novo is solved by library retrieval.
- Training MS2Deepscore / Spec2Vec inside the kernel.
- Jumping straight to Li's 0.75 *identification* cutoff (too aggressive for MRR@25 recall).
- Merging prior Cloud H-sim-gate PRs #72–#81 (those stay historical; this cycle re-implements on current main).
