# Research 2026-10-06_cycle02

## Goal

Raise public MRR@25 above our scored v0.1 **0.143** toward the current CLIST prize table (pikachu / MarvinTMB **0.47**). This slot is a single-factor ablation that can run in the internet-off kernel.

## Sources reviewed

1. **Li & Fiehn, Nat. Methods (2021)** — Spectral entropy outperforms 42 similarity algorithms on NIST20; FDR < 10% near entropy similarity 0.75.  
   https://www.nature.com/articles/s41592-021-01331-z
2. **Li et al., Nat. Methods (2024) / PMC11511675** — Flash Entropy Search. Fragment matching uses a **20 mDa** window because “maximum mass errors may occur for low-abundant ions at 10-mDa difference”; they “select a generous 20-mDa-wide window for fragment ion-matching to also account for possible measurement errors in library spectra.”  
   https://pmc.ncbi.nlm.nih.gov/articles/PMC11511675/
3. **msentropy FlashEntropySearch API** — `search(..., ms2_tolerance_in_da=0.02, noise_threshold=0.01, min_ms2_difference_in_da=0.05)`. Default fragment tolerance is **0.02 Da**, not 0.01.  
   https://msentropy.readthedocs.io/en/latest/entropy_search_api.html
4. **msentropy classical entropy similarity** — recommended cleaning: drop ions above precursor−1.6 Da; remove peaks below 1% of max intensity; centroid/merge within 0.05 Da.  
   https://msentropy.readthedocs.io/en/latest/classical_entropy_similarity.html
5. **Community notebooks (Kaggle code tab, 2026-10-06)** — analog / quad-channel public kernels still sit at **0.328–0.339**; a newer “Transparent Retrieval” notebook is **0.174**. Retrieval-only remains far below the 0.47 prize pack.

## Methods to consider

| Priority | Method | Why it can lift MRR@25 | How (this kernel) |
|----------|--------|------------------------|-------------------|
| **P0** | **Widen `PEAK_MZ_TOL` 0.01 → 0.02** | Our hybrid entropy/modcos matcher uses `cfg.peak_mz_tol` for greedy 1-1 peak pairs. At 10 mDa we miss the low-abundance / cross-library pairs Flash treats as in-tolerance. More true fragment matches raise entropy similarity of the correct IK and can move it inside the MRR@25 window. | One constant |
| P1 | `INTENSITY_FLOOR` 0.001 → 0.01 | Li/Fiehn 1% noise floor. Cloud PRs #13–#19 already implement this; they remain unmerged drafts. | Config only |
| P1 | Keep `EXCLUDE_EXACT_DUPLICATES` | v0.1 exact test↔train dups in `enveda-180` have train labels ≠ GT. | Already on |
| P2 | `MIN_SIMILARITY` 0.05 → 0.12 | Drops weak decoys; Cloud PRs #11–#12 never merged. | Config only |
| P2 | Domain prior / analog channels | Community 0.33+ notebooks; not a one-constant change. | Larger code |

## Why PEAK_MZ_TOL this slot

Live main already has `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, mass-wide 35/80, `MIN_SIMILARITY=0.05`, `PEAK_MZ_TOL=0.01`. Actions slot-2 fallback is still `ENTROPY_WEIGHT=0.75` — a no-op that wasted 2026-10-05 UTC slot 2. Aligning the fragment window with Flash’s **0.02 Da** default is the unused major factor that is not already sitting in seven open H-intensity PRs.

## Out of scope this cycle

MS2Query / Spec2Vec / MS2Deepscore weights (internet off, no attached embedding dataset). Formula→candidate de novo. Claiming Class-3 structures are solved by retrieval.
