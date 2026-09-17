# Research — 2026-09-17 cycle05

## Goal

Raise public **MRR@25** above the only scored baseline (**0.143**, v0.1) toward current leaders (~**0.33–0.34**). Notebook-only, internet-off kernel. Retrieval can recover library structures; it does **not** solve Class-3 de novo.

## Sources reviewed

1. **Li, Kind, Folz et al., Nat. Methods (2021)** — Spectral entropy similarity outperforms MS/MS dot product (and 42 other algorithms) for small-molecule library ID; low FDR near entropy similarity ~0.75 on natural-product spectra.  
   https://www.nature.com/articles/s41592-021-01331-z · https://doi.org/10.1038/s41592-021-01331-z
2. **Li & Fiehn, Nat. Methods (2023)** — Flash Entropy Search: identity / open / neutral-loss / hybrid entropy search at library scale without accuracy loss; extra weight on low-abundance fragments that cosine under-uses.  
   https://doi.org/10.1038/s41592-023-02012-9 · https://github.com/YuanyueLi/MSEntropy · https://msentropy.readthedocs.io/
3. **Bittremieux et al., JASMS (2022)** — Modified cosine remains strong for analog / CE-shifted pairs vs cosine or neutral-loss-only alignment. Keep a non-zero cosine term in the hybrid.  
   https://doi.org/10.1021/jasms.2c00153
4. **de Jonge et al., Nat. Commun. (2023)** — MS2Query: MS2Deepscore preselect + Spec2Vec + precursor Δm/z + RF re-rank. Better analog ranking than modified cosine, but too heavy (GB embeddings) for this internet-off notebook slot.  
   https://www.nature.com/articles/s41467-023-37446-4 · https://github.com/iomega/ms2query
5. **Enveda PRISM** — foundation-model pretraining on ~1.2B spectra improved library matching ~23% vs a non-pretrained ML baseline; not deployable in this kernel.  
   https://enveda.com/prism-a-foundation-model-for-lifes-chemistry/
6. **Prior cycle docs** — `Research/2026-09-15_cycle01_methods.md`, `Research/2026-09-15_cycle02_methods.md` (entropy-weight ablation specified but kernel v4 **ERROR**, never scored). Cycles 03–04 only moved mass ppm.

## Methods to consider

| Priority | Method | Why it can lift MRR@25 | How in this kernel |
|----------|--------|------------------------|--------------------|
| **P0** | **Entropy-dominant hybrid** (`ENTROPY_WEIGHT` 0.55 → **0.70**) | After exact-dup exclusion, remaining hits are *near* matches. Entropy reweights low-intensity fragments that distinguish isobars; 0.55 still lets cosine dominate when both scores are high. Cycle02 planned this; it never landed. | One constant in `casmi26/config.py` |
| **P0** | Keep `EXCLUDE_EXACT_DUPLICATES=True` | v0.1: identical `enveda-180` rows with train labels ≠ GT; perfect match ⇒ public 0.143. | Already on |
| **P0** | Keep modified cosine in the hybrid | Analog / CE-shifted fragments still need precursor-shift matching (Bittremieux). | `hybrid = 0.70·entropy + 0.30·modcos` |
| **P1** | Wider neighbor list (`TOP_K_SPECTRA_PER_QUERY`) | Sparse queries after dup-ban need more non-identical evidence | Next slot if entropy is flat |
| **P1** | Mass-window (already ablated 03/04) | Cycle03: 5/10 ppm; cycle04: 10/15 ppm. Do **not** re-ablate this slot. | Leave at 10 / 15 |
| **P2** | MS2Query / Spec2Vec / MS2Deepscore / PRISM | SOTA analog ranking | Offline weights, internet-off, runtime |
| **Out** | Unconstrained de novo SMILES | Retrieval ≠ Class-3 solution | Out of scope |

## Operational recipe for this slot

1. Do **not** trust exact test↔train spectrum duplicates.
2. **One major ablation:** `ENTROPY_WEIGHT → 0.70`.
3. Leave mass tolerances at cycle04 values (`MASS_TOL_PPM=10`, `MASS_TOL_PPM_BACKFILL=15`).
4. Submit with `competition_submit_code` only.

## Out of scope this cycle

MS2Query embedding stack; SIRIUS in-kernel; training a deep model; claiming Class-3 de novo is solved by library search.
