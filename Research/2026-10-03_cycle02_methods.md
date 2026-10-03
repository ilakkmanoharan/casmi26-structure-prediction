# Research — 2026-10-03 cycle02

## Goal

Raise public **MRR@25** for `enveda-CASMI26-molecule-id-mass-spectra` above the scored v0.1 floor (**0.143**) toward current prize-table leaders (~**0.47**). This cycle is a notebook-only, internet-off kernel change: one major `casmi26/config.py` ablation.

## Sources reviewed

1. **Li, Kind, Folz, Vaniya, Mehta, Fiehn — *Nat. Methods* (2021)**  
   [Spectral entropy outperforms MS/MS dot product similarity](https://www.nature.com/articles/s41592-021-01331-z)  
   Entropy similarity beat 42 algorithms (including cosine) on 434,287 spectra vs NIST20. On 37,299 experimental natural-product spectra, **entropy similarity 0.75 ⇒ FDR < 10%**. Entropy remains robust after adding noise ions — but that robustness assumes **cleaning first**.

2. **Li & Fiehn — *Nat. Methods* (2023) / PMC11511675**  
   [Flash Entropy Search](https://pmc.ncbi.nlm.nih.gov/articles/PMC11511675/)  
   Library/query cleaning: drop precursor and ions above precursor−1.6 Da; **remove peaks below 1% of the strongest fragment** (`noise_threshold=0.01`); match fragments in a **±20 mDa** window; normalize ΣI = 0.5 before entropy.

3. **msentropy API / FlashEntropySearch**  
   [entropy_search_api](https://msentropy.readthedocs.io/en/latest/entropy_search_api.html), [basic search usage](https://msentropy.readthedocs.io/en/latest/dynamic_basic_usage_search.html)  
   Defaults: `noise_threshold=0.01`, `ms2_tolerance_in_da=0.02`, `ms1_tolerance_in_da=0.01`, `precursor_ions_removal_da=1.6`.

4. **Huber et al. — MS2Query (*Nat. Commun.* 2023)**  
   Spec2Vec + MS2Deepscore analog ranking. Community CASMI notebooks that copy analog / multi-channel rankers sit at **0.32–0.34** public code scores — well above our retrieval-only 0.143, but they need offline embeddings we do not ship in this kernel.

5. **Competition + community notebooks (2026-10-03)**  
   Prize-table (CLIST): pikachu **0.47**, chopper / Randy **0.44**, Ozymandias31415 **0.43**. Public code notebooks: four-channel / analog rankers **0.328–0.339**.

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

## Why this slot is intensity floor, not another fallback

Live `main` already has the Actions fallback stack baked in:

- `TOP_PEAKS=128` (H-top-peaks — cycle01 today, no-op)
- `ENTROPY_WEIGHT=0.75` (H-entropy — default slot-2 fallback, **no-op**)
- `MASS_TOL_PPM=35`, `MASS_TOL_PPM_BACKFILL=80`, `TOP_K_SPECTRA_PER_QUERY=120` (H-mass-wide)
- `MIN_SIMILARITY=0.05`, `EXCLUDE_EXACT_DUPLICATES=True`

Repeating H-entropy wastes a Chicago-day ticket. `INTENSITY_FLOOR` is still **0.001**. Raising it to **0.01** is the unused Li/Fiehn cleaning default and the only remaining one-line change that matches the entropy papers we already cite.

## Out of scope this cycle

- Embedding analog rankers / MS2Query
- Changing `PEAK_MZ_TOL` or `MIN_SIMILARITY` in the same submit
- Claiming Class-3 de novo is solved by retrieval
- CSV `competitions submit`
