# Research — 2026-09-23 cycle01

## Goal

Raise public **MRR@25** for `enveda-CASMI26-molecule-id-mass-spectra` above the only scored baseline (**0.143**, v0.1). Notebook-only, internet-off kernel. Retrieval is necessary but **not** sufficient for Class-3 de novo.

## Sources reviewed

1. **Li, Kind, Folz, Vaniya, Mehta, Kind & Fiehn, Nat. Methods (2021)** — Spectral entropy similarity outperforms MS/MS dot product (and 42 other algorithms) for small-molecule library ID. Gain comes in part from **up-weighting low-abundance fragment ions**, which carry metabolite-specific ladders.  
   https://www.nature.com/articles/s41592-021-01331-z · https://doi.org/10.1038/s41592-021-01331-z
2. **Li & Fiehn, Nat. Methods (2023)** — Flash Entropy Search: identity / open / neutral-loss / hybrid modes; spectra are **centroided and denoised**, not truncated to a handful of base-peak ions. Default `ms-entropy` clean uses `noise_threshold=0.01` (~1% BPI) and `max_peak_num=None`.  
   https://www.nature.com/articles/s41592-023-02012-9 · https://doi.org/10.1038/s41592-023-02012-9 · https://pmc.ncbi.nlm.nih.gov/articles/PMC11511675/ · https://msentropy.readthedocs.io/en/latest/entropy_search_api.html
3. **Bittremieux et al., JASMS (2022)** — Modified cosine beats cosine and neutral-loss-only alignment for structurally related MS/MS pairs.  
   https://doi.org/10.1021/jasms.2c00153
4. **de Jonge et al., Nat. Commun. (2023)** — MS2Query: MS2Deepscore preselect + Spec2Vec + precursor Δm/z + RF re-rank. Better analogue ranking than modified cosine, but heavy weights; not a drop-in for this kernel.  
   https://www.nature.com/articles/s41467-023-37446-4 · https://github.com/iomega/ms2query
5. **Competition data card** — `enveda-180` is instrument-matched but **synthetic drug-like**; `enveda-np-examples` is the closest chemical space. Exact test↔train spectrum copies in `enveda-180` can carry train labels ≠ GT.  
   https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra/data

## Methods (why / how they can raise MRR@25)

| Priority | Method | Why / how | Notebook-off fit |
|----------|--------|-----------|------------------|
| **P0** | **Restore `TOP_PEAKS` 5→128** (this slot) | Cycle05 / kernel v13 / Kaggle 56298621 set `TOP_PEAKS=5`. That discards the low-intensity ions entropy similarity is designed to use, so hybrid scores collapse toward 5-peak cosine. Flash Entropy / Li & Fiehn keep ions above ~1% BPI, not top-5. Cycle02 already specified 128. | Single constant |
| **P0** | Keep `EXCLUDE_EXACT_DUPLICATES=True` | Poisoned exact hits place wrong SMILES at rank 1 (v0.1 ~0.143 despite sim=1.0). | Already on |
| **P0** | Keep entropy/modcos hybrid | Entropy for identity; modcos for CE-shifted / analogue fragments. | Already on (`ENTROPY_WEIGHT=0.6`) |
| **P1** | Widen `MASS_TOL_PPM` after peaks are restored | Cycle05 also tightened 10/15 ppm; NP adduct/mass error may need 20–25 ppm + wider backfill. **Next slot**, not this one. | Config only |
| **P1** | Multi-spectrum / CE aggregation | Reward structures supported across CEs/adducts (`TOP_K_SPECTRA_PER_QUERY`). | Already implemented |
| **P2** | MS2Query / Spec2Vec / MS2Deepscore | SOTA analogue ranking | Heavy weights + deps; 9h risk |
| **P2** | Formula→candidate (SIRIUS-style) | Needed when true structure is absent from train libs | Not in pipeline |
| **Out** | Pure Class-3 de novo | Retrieval alone does not solve CASMI Class-3 | Out of scope |

## Operational recipe for this slot

1. Do **not** re-enable trusting exact duplicates.
2. Ablate **one** knob vs last submitted kernel (v13 / 56298621): `TOP_PEAKS` 5 → **128**.
3. Leave mass / entropy / min-sim knobs unchanged so the peak-count effect is identifiable.
4. Submit via notebook `competition_submit_code` only — never CSV `competitions submit`.

## Out of scope this cycle

MS2Query embedding stack; SIRIUS in-kernel; training deep models; claiming Class-3 solved by library search; changing `MASS_TOL_PPM` in the same slot.
