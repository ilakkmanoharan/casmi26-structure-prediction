# Research — 2026-10-11 cycle02

## Goal

Raise public **MRR@25** on **enveda-CASMI26-molecule-id-mass-spectra** above the scored v0.1 baseline (**0.143**). Notebook-only, internet-off kernel. Retrieval is necessary but **not** sufficient for Class-3 de novo.

This slot's major lever: align `INTENSITY_FLOOR` with the Flash Entropy Search / Li–Fiehn 1% noise cut (`0.001 → 0.01`). Live main already has `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, mass-wide 35/80 ppm, `MIN_SIMILARITY=0.05`, `PEAK_MZ_TOL=0.01`. Repeating Actions slot-2 `ENTROPY_WEIGHT=0.75` is a no-op.

## Sources reviewed

1. **Li & Fiehn, Nat. Methods (2023) — Flash Entropy Search.** Library and query spectra drop fragment ions below **1% of the maximum fragment intensity** (`noise_threshold=0.01`) before entropy weighting. Sub-1% ions are treated as isolation-window / instrument noise, not precursor fragments.  
   https://www.nature.com/articles/s41592-023-02012-9 · https://doi.org/10.1038/s41592-023-02012-9 · https://pmc.ncbi.nlm.nih.gov/articles/PMC11511675/ · PDF: https://escholarship.org/content/qt33d9t00t/qt33d9t00t.pdf
2. **msentropy API / `clean_spectrum`.** Default `noise_threshold=0.01` removes `intensity < 0.01 * max(intensity)`, then centroids and L1-normalizes. Search default fragment window is 20 mDa.  
   https://msentropy.readthedocs.io/en/latest/entropy_search_api.html · https://msentropy.readthedocs.io/en/latest/entropy_search_basic_usage.html
3. **Li, Kind, Folz et al., Nat. Methods (2021) — Spectral entropy.** Entropy similarity outperforms cosine / modified cosine for small-molecule ID; FDR &lt;10% near score 0.75 on NP-like spectra. Noise peaks inflate spectral entropy and dilute weights.  
   https://www.nature.com/articles/s41592-021-01331-z
4. **matchms cleaning.** `select_by_relative_intensity(..., intensity_from=0.01)` is the common GNPS / library-clean recipe (Huber et al., J. Cheminf. 2024).  
   https://matchms.readthedocs.io/en/latest/api/matchms.filtering.html · https://link.springer.com/article/10.1186/s13321-024-00878-1
5. **Prior cycle evidence.** v0.1 exact test↔train dups in `enveda-180` with train labels ≠ GT (~0.143). Cloud H-intensity PRs #13–#19, #21, #23 and H-peak-mz PRs #20/#22/#24 remain unmerged drafts.

## Methods (why / how they can raise MRR@25)

| Priority | Method | Why / how | Notebook-off fit |
|----------|--------|-----------|------------------|
| **P0 this slot** | **`INTENSITY_FLOOR` 0.001→0.01** | Current 0.1% floor keeps isolation-window junk that Flash Entropy and matchms drop. Those peaks steal `TOP_PEAKS=128` slots and add spurious entropy/modcos matches → wrong InChIKey14s in the top-25. | Single constant |
| **P0 keep** | `EXCLUDE_EXACT_DUPLICATES=True` | Poisoned exact hits still put wrong SMILES at rank 1 | Already on |
| **P1** | `PEAK_MZ_TOL` 0.01→0.02 | Flash Entropy default 20 mDa fragment window; still unused on main | Next unused after this PR |
| **P1** | `MIN_SIMILARITY` 0.05→0.12 | Drop low-evidence neighbors after noise cut | PRs #11/#12 |
| **P2** | MS2Query / Spec2Vec / MS2Deepscore | SOTA analogue ranking | Heavy weights; 9h risk |
| **Out** | Class-3 de novo (DiffMS, unconstrained LLM SMILES) | Retrieval alone does not solve CASMI Class-3 | Out of scope |

## Operational recipe for this slot

1. Do **not** re-enable trusting exact duplicates.
2. Ablate **one** knob: `INTENSITY_FLOOR → 0.01` (Li/Fiehn + matchms 1% relative cut).
3. Retarget Actions **slot-2** fallback `H-entropy` → `H-intensity` so the next hourly `casmi-loop` does not waste a UTC ticket on a no-op `ENTROPY_WEIGHT=0.75`.
4. Submit via notebook / `competition_submit_code` only — never CSV `competitions submit`.

## Out of scope this cycle

MS2Query embeddings; SIRIUS in-kernel; changing `PEAK_MZ_TOL` in the same slot; claiming Class-3 solved by library search.
