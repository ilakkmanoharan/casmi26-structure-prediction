# Research 2026-11-07_cycle03 — precursor-ion removal for entropy identity search

Competition day: **2026-11-07** (anchor 01:00 America/Chicago). Cycle **03** of 5.
Goal: raise public **MRR@25** for `enveda-CASMI26-molecule-id-mass-spectra` without claiming Class-3 de novo is solved by retrieval.

## Sources reviewed

1. **Li, Kind, Folz et al., *Nat. Methods* (2021)** — Spectral entropy outperforms 42 MS/MS similarity algorithms (including dot product) on NIST20; FDR &lt; 10% at entropy similarity 0.75. [PMC11492813](https://pmc.ncbi.nlm.nih.gov/articles/PMC11492813/)
2. **Li et al., *Nat. Methods* (2023) / Flash Entropy Search** — identity / open / neutral-loss / hybrid (modified-cosine-like) search; default fragment window **20 mDa**; identity search constrained by precursor mass. [PMC11511675](https://pmc.ncbi.nlm.nih.gov/articles/PMC11511675/), [doi:10.1038/s41592-023-02012-9](https://doi.org/10.1038/s41592-023-02012-9)
3. **ms_entropy docs (classical entropy similarity)** — *“eliminating ions with m/z values higher than the precursor ion’s m/z − 1.6 considerably enhances the spectral identification performance.”* Default noise floor 1% of base peak; `precursor_ions_removal_da=1.6`. [msentropy.readthedocs.io](https://msentropy.readthedocs.io/en/latest/classical_entropy_similarity.html)
4. **Flash Entropy source (`flash_entropy_search`)** — `precursor_ions_removal_da: float = 1.6`, `noise_threshold=0.01`, `ms2_tolerance_in_da=0.02`. [msentropy docs module](https://msentropy.readthedocs.io/en/latest/_modules/ms_entropy/entropy_search/flash_entropy_search.html)
5. **GNPS / matchms modified cosine** — fragment tolerance ~0.02–0.025 Da; cosine threshold 0.85 is an *annotation* gate, not a retrieval floor. [GNPS GC-MS docs](https://ccms-ucsd.github.io/GNPSDocumentation/gc-ms-library-molecular-network/)
6. **CASMI 2026 writeup (Pilkwang)** — metric is MRR@25 on tautomer-canonical InChIKey14; cosine/entropy retrieval cannot invent missing structures. [pilkwangkim.github.io](https://pilkwangkim.github.io/posts/CASMI-2026-From-Mass-Spectra-to-Molecular-Structures/)
7. **Public campaign notes (cubres, Oct 2026)** — live public LB top ~**0.499** (pikachu); analog-propagation + candidate-DB methods sit 0.45–0.47. Retrieval-only notebooks remain far below that. [cubres/enveda-casmi-2026](https://github.com/cubres/enveda-casmi-2026/blob/main/README.md)

## Methods to consider

| Priority | Method | Why it can lift MRR@25 | How (notebook, internet off) |
|----------|--------|------------------------|------------------------------|
| **P0** | **Drop precursor-window ions (m/z > precursor − 1.6 Da)** | Precursor / isotope / adduct peaks are shared by every isobar in a mass window. They inflate entropy and modified cosine for *wrong* structures and drown diagnostic fragments. ms_entropy measured a clear ID gain from this cut on NIST20 and MassBank.us. | Set `MAX_PEAKS_ABOVE_PRECURSOR_DA = -1.6` and pass it through `clean_spectrum` on **both** index build and query. |
| P1 | Raise `MIN_SIMILARITY` from 0.05 toward 0.15–0.25 | Li 2021: entropy ≥ 0.75 ⇒ FDR &lt; 10%. Our 0.05 floor lets near-random mass-consistent hits occupy the 25 slots. | Config-only; next slot if P0 is a no-op or hurts coverage. |
| P1 | Tighten `MASS_TOL_PPM` 35 → 10–15 | NIST20 identity search used ~10 ppm precursor windows. Wide 35 ppm admits many isobars that then rank on precursor-peak similarity. | Config-only; do **not** combine with P0 this slot. |
| P2 | Entropy weight 0.75 → 0.90 | Li 2021 ranked entropy above cosine; hybrid still keeps analog-friendly modcos. | Config-only. |
| P2 | CE-aware aggregation | Reward library hits whose collision energy matches the query CE list. | Small `retrieve.py` change; later slot. |
| P3 | MS2Query / Spec2Vec / MS2Deepscore | Strong analog ranking in literature. | Heavy weights; internet-off kernel cannot download them. |
| P3 | Formula → candidate DB / de novo | Needed when the true structure is absent or labels are poisoned. | Out of scope for a retrieval ablation. |

## Why this cycle is *not* another TOP_PEAKS / PEAK_MZ_TOL re-apply

`casmi26/config.py` already has `TOP_PEAKS=128` and `PEAK_MZ_TOL=0.02`. GitHub Actions fallbacks for slots 1–2 (and the old slot-3 duplicate) re-wrote those same values, so recent kernels were **no-ops**. Public scores on those rows stayed `None` / our last scored public is still **0.143**. Slot 3 must change a factor that currently affects scoring.

`MAX_PEAKS_ABOVE_PRECURSOR_DA` was **2.0 and unused**: `clean_spectrum` defaulted to keeping ions up to precursor **+2 Da**. Wiring it to **−1.6** is the first time this kernel matches the entropy-search cleaner.

## How precursor cut improves score

1. Identity search should compare **product-ion ladders**, not the unfragmented precursor that every candidate of the same nominal mass shares.
2. After the cut, entropy/modcos ranks structures that share fragments; poisoned exact-dup InChIKeys remain banned via `EXCLUDE_EXACT_DUPLICATES`.
3. Index and query use the same cleaner, so `spectra_identical` (poisoned-label guard) stays consistent.

## Out of scope this cycle

- Training embeddings (MS2Deepscore, Spec2Vec) or downloading extra libraries.
- CSV `competitions submit` (notebook-only).
- Claiming retrieval solves Class-3 de novo.
- Combining a second config knob (min similarity / mass ppm) with the precursor cut.
