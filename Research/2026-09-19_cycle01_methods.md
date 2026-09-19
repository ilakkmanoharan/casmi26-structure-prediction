# Research — 2026-09-19 cycle01

## Goal

Raise public **MRR@25** on **enveda-CASMI26-molecule-id-mass-spectra** above the v0.1 ceiling (**0.143**). Leaders are now ~**0.33** (GUAM 0.332; Minal kharat123 0.324; Preechanon Chatthai 0.319). Notebook-only, internet-off kernel. Retrieval can close part of the gap; it does **not** solve Class-3 de novo.

## Sources reviewed

1. **Li, Kind, Folz, Fiehn et al., Nat. Methods (2021)** — Spectral entropy beats MS/MS dot product and 42 other algorithms on NIST20; FDR &lt;10% near entropy similarity 0.75 on natural-product spectra. Cleaning recipe: drop ions &lt;1% base-peak intensity, match at ~0.05 Da.  
   https://www.nature.com/articles/s41592-021-01331-z · https://doi.org/10.1038/s41592-021-01331-z · PDF https://yuanyue.li/project/spectral_entropy/Yuanyue-spectral_entropy.pdf
2. **Li & Fiehn, Nat. Methods (2023) — Flash Entropy Search** — Same scoring, billion-scale identity / open / neutral-loss / hybrid modes. Precursor and ions &gt; precursor−1.6 Da removed; ions &lt;1% max fragment abundance treated as noise; **no 5-peak cap**.  
   https://www.nature.com/articles/s41592-023-02012-9 · https://doi.org/10.1038/s41592-023-02012-9
3. **msentropy (CRAN / YuanyueLi)** — Default `noise_threshold=0.01`, `max_peak_num=100` (or unlimited). Cycle05’s `TOP_PEAKS=5` is an order of magnitude below this default.  
   https://cran.r-project.org/web/packages/msentropy/refman/msentropy.html · https://github.com/YuanyueLi/MSEntropy
4. **Bittremieux et al., JASMS (2022)** — Modified cosine outperforms cosine and neutral-loss-only alignment for structurally related MS/MS pairs. Keep modcos in the hybrid.  
   https://doi.org/10.1021/jasms.2c00153
5. **de Jonge et al., Nat. Commun. (2023) — MS2Query** — MS2Deepscore + Spec2Vec + precursor Δm/z analogue search. Strong when the true structure is absent; too heavy for this internet-off kernel this slot.  
   https://www.nature.com/articles/s41467-023-37446-4
6. **ChemEmbed (bioRxiv 2025)** — Multi-CE merged spectra + Mol2vec candidate ranking; reports CASMI 2016/2022 gains vs SIRIUS. Out of scope (weights + PubChem-scale embeddings).  
   https://doi.org/10.1101/2025.02.07.637102
7. **Public LB (fetched 2026-09-19)** — https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra/leaderboard — top ~0.33 vs our 0.143.

## Methods (why / how they can raise MRR@25)

| Priority | Method | Why / how | Notebook-off fit |
|----------|--------|-----------|------------------|
| **P0** | **Restore `TOP_PEAKS` 5 → 128** (major ablation this cycle) | Entropy and modified cosine need the fragment ladder. `TOP_PEAKS=5` (2026-09-17 cycle05) discards mid-intensity diagnostic ions that Li/Fiehn keep above 1% BPI; it also coarsens exact-dup detection (`spectra_identical` after the same 5-peak clean). | Single constant |
| **P0** | Keep `EXCLUDE_EXACT_DUPLICATES=True` | Poisoned enveda-180 exact dups still place wrong SMILES at #1 | Already on |
| **P0** | Keep entropy/modcos hybrid | Entropy for identity, modcos for CE/analogue shift | Already on (`ENTROPY_WEIGHT=0.6`) |
| **P1** | `max_peak_num≈100` + 1% floor (msentropy defaults) | Next-slot refinement if 128 still noisy | Config (`TOP_PEAKS`, `INTENSITY_FLOOR`) |
| **P1** | `PEAK_MZ_TOL` 0.02–0.05 Da | Literature match windows; current 0.01 Da may miss CE-shifted fragments | Config |
| **P1** | `ENTROPY_WEIGHT→0.70` | Cycle02 spec never scored (kernel ERROR / 429 loop) | Config; **next** slot after peaks restored |
| **P2** | MS2Query / ChemEmbed / SIRIUS-style formula | Needed when GT is absent from train libs | Heavy; not this kernel |
| **Out** | Pure Class-3 de novo SMILES | Retrieval alone does not solve CASMI Class-3 | Out of scope |

## Operational recipe for this slot

1. Do **not** re-enable trusting exact duplicates.
2. Ablate **one** knob: restore the fragment ladder (`TOP_PEAKS → 128`).
3. Leave mass / entropy / min-sim at the cycle05 values so the score delta is attributable to peaks.
4. Unblock GitHub Actions: OpenAI HTTP 429/5xx must fall back to deterministic docs instead of crashing before `kernels push`.
5. Submit via notebook / `competition_submit_code` only.

## Out of scope this cycle

MS2Query embeddings; SIRIUS binary; ChemEmbed weights; claiming Class-3 solved by library search; CSV-only `competitions submit`.
