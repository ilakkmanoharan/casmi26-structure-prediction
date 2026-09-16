# Research — 2026-09-15 cycle02

## Goal

Improve public **MRR@25** beyond the v0.1 baseline (**0.143**) and the cycle01 v0.2 package (exact-dup exclusion + entropy/modcos hybrid + all-libs). Leaders remain ~**0.28**. Notebook-only, internet-off Kaggle kernel; retrieval is necessary but **not** sufficient for Class-3 de novo.

## Sources reviewed

1. **Li, Kind, Folz et al., Nat. Methods (2021)** — Spectral entropy similarity outperforms MS/MS dot product (and 42 other algorithms) for small-molecule library ID; FDR &lt;10% near entropy similarity 0.75 on natural-product spectra.  
   https://www.nature.com/articles/s41592-021-01331-z · https://doi.org/10.1038/s41592-021-01331-z
2. **Li & Fiehn, Nat. Methods (2023)** — Flash Entropy Search: scales entropy similarity to billion-scale libraries without accuracy loss; identity / open / neutral-loss / hybrid modes.  
   https://www.nature.com/articles/s41592-023-02012-9 · https://doi.org/10.1038/s41592-023-02012-9 · https://github.com/YuanyueLi/MSEntropy
3. **Bittremieux et al., JASMS (2022)** — Modified cosine outperforms cosine and neutral-loss-only alignment for structurally related MS/MS pairs (peptides + small molecules).  
   https://doi.org/10.1021/jasms.2c00153 · https://pubmed.ncbi.nlm.nih.gov/35960544/
4. **de Jonge et al., Nat. Commun. (2023)** — MS2Query: MS2Deepscore preselect + Spec2Vec + precursor Δm/z + RF re-rank for exact + analogue search; improves chemical similarity vs modified cosine alone.  
   https://www.nature.com/articles/s41467-023-37446-4 · https://github.com/iomega/ms2query
5. **SIRIUS / CSI:FingerID** — Formula from isotope + fragmentation trees, then fingerprint→structure DB; complementary when library coverage fails (not a drop-in for this kernel yet).  
   https://v6.docs.sirius-ms.io/methods-background/ · https://en.wikipedia.org/wiki/SIRIUS_(software)
6. **Cycle01 local evidence** (`Analysis/2026-09-15_cycle01_submission.md`) — exact test↔train duplicates in `enveda-180` with train labels ≠ GT; rank-1 sim=1.0 everywhere under v0.1.

## Methods (why / how they can raise MRR@25)

| Priority | Method | Why / how | Notebook-off fit |
|----------|--------|-----------|------------------|
| **P0** | Keep **EXCLUDE_EXACT_DUPLICATES** | Poisoned exact hits place wrong SMILES at #1; removing them frees ranking for non-identical evidence | Already in `config.py` |
| **P0** | **Raise ENTROPY_WEIGHT** (major ablation this cycle) | Li & Fiehn: entropy ≫ cosine for ID; after dups removed, near-matches need better discrimination than balanced 0.55 hybrid | Single constant flip |
| **P0** | Retain modified cosine in hybrid | Bittremieux: modcos still best for analogs / CE-shifted fragments | Already implemented |
| **P1** | Multi-spectrum / CE aggregation (`TOP_K_SPECTRA_PER_QUERY`) | Reward structures supported across CEs/adducts; raises Hit@25 when single best hit is noisy | Config + existing aggregator |
| **P1** | Mass-window + peak-tol tuning | Tighter `MASS_TOL_PPM` / `PEAK_MZ_TOL` cuts decoys after all-libs index; looser backfill recovers sparse queries | Config only |
| **P1** | Cleaning views (`TOP_PEAKS`, `INTENSITY_FLOOR`) | Entropy is noise-robust but top-N / floor still change which peaks survive | Config only |
| **P2** | MS2Query / Spec2Vec / MS2Deepscore | SOTA analogue ranking | Heavy weights + deps; 9h budget risk |
| **P2** | Formula→candidate (SIRIUS-style) | Needed when true structure absent from train libs | Not in current pipeline |
| **Out** | Pure Class-3 de novo (DiffMS, MSNovelist, unconstrained LLM SMILES) | Does not solve CASMI by retrieval alone; defer | High risk / out of scope |

## Operational recipe for this slot

1. Do **not** re-enable trusting exact duplicates.
2. Ablate **one** knob: push hybrid toward entropy (`ENTROPY_WEIGHT → 0.70`).
3. Keep mass/peak defaults from cycle01 unless evidence shows coverage collapse.
4. Submit via notebook/`competition_submit_code` only — never CSV-only `competitions submit`.

## Out of scope this cycle

Full MS2Query embedding stack; SIRIUS binary in kernel; training deep models; claiming Class-3 solved by library search.
