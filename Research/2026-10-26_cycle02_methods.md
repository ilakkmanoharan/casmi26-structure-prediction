# Research — 2026-10-26 cycle02

## Goal

Raise public MRR@25 above the v0.1 plateau (**0.143**) toward the current public frontier (~**0.50**). This cycle targets the **library-hit admission floor**, not another replay of already-live peak-cleaning knobs.

## Sources reviewed

1. **Li, Kind, Folz, Vaniya, Mehta, Fiehn — *Nat. Methods* (2021)**  
   [Spectral entropy outperforms MS/MS dot product](https://www.nature.com/articles/s41592-021-01331-z)  
   Entropy similarity beat 42 alternatives on NIST20. On 37,299 experimental natural-product spectra, **entropy similarity ≥ 0.75** yielded **FDR < 10%**. The paper also says results should be *ranked* rather than treated as a single top hit — relevant for MRR@25. Identity-grade 0.75 is too harsh for analog ranking, but it is strong evidence that scores near 0.05 are mostly decoys.

2. **Li & Fiehn — Flash Entropy Search (PMC11511675, 2024)**  
   [Flash entropy search to query all mass spectral libraries in real time](https://pmc.ncbi.nlm.nih.gov/articles/PMC11511675/)  
   Default cleaning: drop ions **< 1% of base peak**, drop *m/z* > precursor − 1.6 Da, fragment match at **20 mDa**. Those cleaning defaults are already live (`INTENSITY_FLOOR=0.01`, `PEAK_MZ_TOL=0.02`). The remaining unused lever on the scoring path is the **minimum similarity admitted into `top_k_spectra`**.

3. **ms_entropy API**  
   [`FlashEntropySearch.search(..., ms2_tolerance_in_da=0.02, noise_threshold=0.01, max_peak_num=None)`](https://msentropy.readthedocs.io/en/latest/entropy_search_api.html)  
   [`clean_spectrum(..., noise_threshold=0.01)`](https://msentropy.readthedocs.io/en/latest/classical_spectral_entropy.html)  
   Confirms cleaning is already aligned. Search still returns a full score vector; downstream rankers typically cut low scores before aggregation.

4. **mzmine analog spectral library search**  
   [Analog spectral library search](https://mzmine.github.io/mzmine_documentation/latest/module_docs/id_spectral_library_analog_search/analog-spectral-library-search.html)  
   Analog modules keep a **minimum similarity** so fragment-overlap noise does not flood the annotation column. Default DreaMS-style analog floors sit far above 0.05.

5. **CASMI / Enveda notes**  
   [Kaggle competition](https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra) · [official LB](https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra/leaderboard) · [CLIST](https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/)  
   Metric is MRR@25. Retrieval-only cannot claim Class-3 de novo. Exact test↔train spectrum duplicates in `enveda-180` still poison rank-1 when labels ≠ GT.

## Methods to consider

| Priority | Method | Why it can lift MRR@25 | How (notebook, internet off) |
|----------|--------|------------------------|------------------------------|
| **P0** | **Raise `MIN_SIMILARITY` 0.05 → 0.12** | Live 0.05 lets near-noise hybrid entropy/modcos hits into `top_k_spectra` (120). Those decoys consume the 25-candidate list and dilute `mean_top_k_similarity` / `support_log`. A modest 0.12 floor (still far below Li/Fiehn identity 0.75) should drop junk without starving true analog support. Never submitted. | One config constant already wired in `retrieve.py`. |
| P1 | Keep more peaks (`TOP_PEAKS` 128 → 160) | After the 1% floor, Flash Entropy prefers not to hard-cap the ladder. Submitted yesterday as cycle04, then reset to 128 by today’s UTC cycle01. | Config only. Retarget Actions slot-3 so it is the *next* unused ticket, not this one. |
| P1 | Replay `PEAK_MZ_TOL=0.02` | Already live since 10-24. Slot-2/slot-3 fallbacks still point here → **wasted tickets**. | Do not submit. Retarget fallbacks away. |
| P2 | Domain-prior / CE aggregation | H-domain fallback is a no-op on current `DOMAIN_PRIOR`. | Skip. |
| P2 | MS2Query / Spec2Vec / MS2Deepscore | Strong analog ranking in literature. | Heavy offline weights; 9h kernel; internet off. |
| P3 | Formula → candidate DB / de novo | Needed when the structure is absent or the only library row is poisoned. | Out of scope. Retrieval cannot solve Class-3. |

## Why this slot is the admission floor, not peak-m/z again

Actions already burned UTC slot 1 today on **H-top-peaks** (`TOP_PEAKS=128`, already live). Slot 2’s fallback is **H-peak-mz** (`PEAK_MZ_TOL=0.02`) — also already live. Replaying it would waste the next hourly ticket. The first unused constant that actually changes which library spectra enter the ranker is `MIN_SIMILARITY`.

## Out of scope this cycle

- CSV `competitions submit` (notebook-only competition).
- Claiming Class-3 de novo is solved by library retrieval.
- Training MS2Deepscore / Spec2Vec inside the kernel.
- Jumping straight to Li/Fiehn identity cutoff 0.75 (would empty analog lists).
- Merging stale Cloud PRs #20–#37 (historical; this cycle re-implements on current main).
