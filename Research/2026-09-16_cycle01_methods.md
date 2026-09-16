# Research — 2026-09-16 cycle01

## Goal

Raise public **MRR@25** for `enveda-CASMI26-molecule-id-mass-spectra` above our scored v0.1 baseline (**0.143**). Public leaders are now **~0.332** (GUAM; fetched 2026-09-16), up from ~0.285 in cycle01 notes. Notebook-only, internet-off kernel. Retrieval is necessary but **not** sufficient for Class-3 de novo.

## Sources reviewed

1. **Li, Kind, Folz, Vaniya, Mehta & Fiehn, Nat. Methods (2021)** — Spectral entropy similarity outperforms MS/MS dot product and 42 other algorithms on NIST20 (434,287 queries). FDR &lt;10% near entropy similarity **0.75** on 37k natural-product spectra. Intensity reweighting: if spectral entropy **S &lt; 3**, raise intensity to `0.25·(1+S)`; else leave intensities unchanged.  
   https://www.nature.com/articles/s41592-021-01331-z · https://doi.org/10.1038/s41592-021-01331-z · PubMed 34857935
2. **msentropy docs / Li implementation** — `apply_weight_to_intensity` only reweights when entropy &lt; 3; similarity is `1 - (2S_ab − S_a − S_b)/ln(4)`.  
   https://msentropy.readthedocs.io/en/latest/_modules/ms_entropy/spectra/entropy.html · https://github.com/YuanyueLi/MSEntropy
3. **Li & Fiehn, Nat. Methods (2023)** — Flash Entropy Search: identity / open / neutral-loss / hybrid modes at library scale.  
   https://www.nature.com/articles/s41592-023-02012-9 · https://doi.org/10.1038/s41592-023-02012-9
4. **Bittremieux et al., JASMS (2022)** — Modified cosine still strongest among cosine-family scores for analog / precursor-shifted pairs.  
   https://doi.org/10.1021/jasms.2c00153
5. **de Jonge et al., Nat. Commun. (2023)** — MS2Query (MS2Deepscore + Spec2Vec + Δm/z + RF) for exact + analogue search. Too heavy for this internet-off slot.  
   https://www.nature.com/articles/s41467-023-37446-4
6. **Kuo, Wang, Broeckling, Prenni, JASMS (2024)** — Revisit of 42 similarity metrics; entropy weighting remains a strong library-ID prior.  
   https://doi.org/10.1021/jasms.3c00353
7. **Competition leaderboard (public, ~33% test)** — Top **0.332** / 155 teams / 510 submissions as of this cycle.  
   https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra/leaderboard

## Methods (why / how they can raise MRR@25)

| Priority | Method | Why / how | Notebook-off fit |
|----------|--------|-----------|------------------|
| **P0** | Keep **EXCLUDE_EXACT_DUPLICATES** | Poisoned exact test↔train hits in `enveda-180` place wrong SMILES at #1 (v0.1 MRR 0.143 with sim=1.0 everywhere) | Already on |
| **P0** | **Raise ENTROPY_WEIGHT 0.55 → 0.70** (major ablation this slot) | Literature: entropy ≫ cosine for identity search once near-matches (not exact dups) drive ranking. Cycle02 intended this but **never landed a scored submit** (kernel v4 ERROR) | Single constant |
| **P0** | **Kernel reliability** (poller + RDKit wheels) | Sep 15 slot 2 pushed kernel v4 then polled `KERNELWORKERSTATUS.ERROR` for 5 h because the poller only matches exact `"ERROR"`. Without a COMPLETE kernel, **no MRR change is possible** | Code, not a scoring knob |
| **P1** | Literature-faithful entropy reweight (`S&lt;3` gate) | Our `_entropy_weights` always applies `I^w`; Li only reweights low-entropy spectra. Candidate for a later slot (do not mix with weight ablation) | `spectrum.py` |
| **P1** | Structure-level ExactMolWt vs inferred neutral mass | Index currently stores spectrum-inferred mass as `exact_mass`, not RDKit ExactMolWt | RDKit already in kernel |
| **P1** | `TOP_K_SPECTRA_PER_QUERY` / tighter `MASS_TOL_PPM` | Multi-CE support vs decoy control after all-libs | Config |
| **P2** | MS2Query / Spec2Vec / MS2Deepscore | SOTA analogue ranking | Weights + deps; 9 h risk |
| **Out** | Class-3 de novo (DiffMS, MSNovelist, unconstrained LLM SMILES) | Does not solve CASMI by retrieval alone | Out of scope |

## Operational recipe for this slot

1. Do **not** re-enable trusting exact duplicates.
2. Ablate **one** scoring knob: `ENTROPY_WEIGHT → 0.70` (entropy-dominant hybrid; keep 0.30 modified cosine for analogs).
3. Fix kernel status parsing so `KERNELWORKERSTATUS.ERROR` fails fast, and bootstrap RDKit from `ilakkmanoharan/rdkit-cp312-wheels-casmi26` before `import rdkit`.
4. Submit via `kaggle kernels push` + `competition_submit_code` only.

## Out of scope this cycle

Full MS2Query stack; SIRIUS in-kernel; training embeddings; claiming Class-3 solved by library search; mixing mass-window changes with the entropy-weight ablation.
