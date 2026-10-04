# Research — 2026-10-04 cycle02

## Goal

Raise public **MRR@25** for `enveda-CASMI26-molecule-id-mass-spectra` above the only scored retrieval floor (**0.143**, v0.1 poisoned exact-dup) toward current prize-table leaders (~**0.47**). Notebook-only, internet-off kernel. One major `casmi26/config.py` ablation.

This is the first Chicago-clock slot after **01:00 America/Chicago** on 2026-10-04. Actions already burned UTC-day slot 1 at 05:21Z (`2026-10-04_cycle01` H-top-peaks, Kaggle 56815069, kernel v54) — that run was **before** 01:00 CDT, so Chicago-clock quota is still 0/5. Slot-2 fallback on main is still `H-entropy` (`ENTROPY_WEIGHT=0.75`), which is already live and would be a no-op ticket.

## Sources reviewed

1. **Li, Kind, Folz, Vaniya, Mehta, Fiehn — *Nat. Methods* (2021)**  
   [Spectral entropy outperforms MS/MS dot product similarity](https://www.nature.com/articles/s41592-021-01331-z)  
   Entropy similarity beat 42 algorithms (including cosine) on 434,287 spectra vs NIST20. On 37,299 experimental natural-product spectra, **entropy similarity 0.75 ⇒ FDR < 10%**. Robustness to added noise ions assumes **cleaning first**.

2. **Li & Fiehn — *Nat. Methods* (2023) / PMC11511675**  
   [Flash Entropy Search](https://pmc.ncbi.nlm.nih.gov/articles/PMC11511675/)  
   Library/query cleaning: drop precursor and ions above precursor−1.6 Da; **remove peaks below 1% of the strongest fragment** (`noise_threshold=0.01`); match fragments in a **±20 mDa** window; normalize ΣI = 0.5 before entropy.

3. **msentropy API / FlashEntropySearch**  
   [classical entropy similarity](https://msentropy.readthedocs.io/en/latest/classical_entropy_similarity.html), [FlashEntropySearch.search](https://msentropy.readthedocs.io/en/latest/_modules/ms_entropy/entropy_search/flash_entropy_search.html)  
   Defaults: `noise_threshold=0.01` (peaks < 1% of max intensity removed), `ms2_tolerance_in_da=0.02`, `precursor_ions_removal_da=1.6`. `calculate_entropy_similarity(..., clean_spectra=True)` applies the same 1% floor.

4. **Huber et al. — MS2Query (*Nat. Commun.* 2023)**  
   Spec2Vec + MS2Deepscore analog ranking. Community CASMI notebooks that copy analog / multi-channel rankers sit at **0.32–0.34** public code scores — well above our retrieval-only 0.143, but they need offline embeddings we do not ship in this kernel.

5. **Competition + community notebooks (2026-10-04T06:15Z)**  
   Prize-table ([CLIST](https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/)): pikachu **0.47**, Shehab / chopper / Randy **0.44**, Xolotl / Arun / Ozymandias31415 **0.43**. Public code notebooks: quad-channel / analog rankers **0.328–0.339**.

6. **Repo failure mode (v0.1)**  
   Exact test↔train spectrum duplicates in `enveda-180` carry train labels ≠ competition GT. A perfect library hit of a poisoned row produces ~0.143 public. `EXCLUDE_EXACT_DUPLICATES=True` is already on.

## Methods to consider

| Priority | Method | Why it can lift MRR@25 | How (this kernel) |
|----------|--------|------------------------|-------------------|
| **P0** | **1% intensity floor (`INTENSITY_FLOOR=0.01`)** | Flash / msentropy default. Current `0.001` keeps 0.1% noise ions that greedy-match into entropy and modified-cosine. After 128-peak restore, those noise rungs dilute the fragment ladder and inflate similarity to the wrong IK. | Config only |
| P1 | Fragment m/z window `PEAK_MZ_TOL` 0.01→0.02 | Flash default ±20 mDa; 10 mDa can miss Orbitrap/QTOF library mismatch | Config only |
| P1 | `MIN_SIMILARITY` 0.05→0.12 | Drop low-support decoys before aggregation; Cloud PRs #11/#12 never merged | Config only |
| P1 | Analog / multi-channel ranker | Community 0.33–0.34; prize 0.42–0.47 | New code; not this slot |
| P2 | MS2Deepscore / Spec2Vec / MS2Query | Analog recall when exact structure is missing or poisoned | Offline weights; internet off |
| P2 | Formula → candidate DB | Recovers Class-3 / poisoned-label molecules | Non-trivial |
| P3 | De novo (MSNovelist, DiffMS) | Class-3 only | Out of scope; retrieval does not solve Class-3 |

## Why this cycle is intensity floor, not H-entropy again

Live main already has `ENTROPY_WEIGHT=0.75`, `TOP_PEAKS=128`, mass-wide 35/80 ppm, `MIN_SIMILARITY=0.05`. Actions slot-2 fallback is still `H-entropy`, which would push a no-op kernel and burn a UTC ticket. Cloud PRs #13–#17 proposed `INTENSITY_FLOOR=0.01` and stayed unmerged; the 1% floor is still unused on main. Literature gives a concrete default (`noise_threshold=0.01`).

## Out of scope this cycle

MS2Query / Spec2Vec / MS2DeepScore weights; Flash Entropy C-extension; unconstrained LLM SMILES; claiming Class-3 de novo is solved by library retrieval.
