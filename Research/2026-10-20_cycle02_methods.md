# Research — 2026-10-20 cycle02

## Goal

Raise public MRR@25 above the v0.1 plateau (**0.143**) toward the current public frontier (**0.495**). This cycle targets the **fragment m/z match window**, not another no-op replay of already-live `TOP_PEAKS` / `ENTROPY_WEIGHT` / `INTENSITY_FLOOR`.

## Sources reviewed

1. **Li & Fiehn — *Nat. Methods* (2023), PMC11511675**  
   [Flash Entropy Search](https://pmc.ncbi.nlm.nih.gov/articles/PMC11511675/)  
   Fragment ions are matched inside a generous **±20 mDa** window. The paper notes maximum mass errors on low-abundance ions near 10 mDa and chooses 20 mDa to cover measurement error in both query and library spectra. Lowering the window speeds search but can miss true pairs after CE / instrument shift.

2. **ms_entropy API**  
   [`FlashEntropySearch.search(..., ms2_tolerance_in_da=0.02)`](https://msentropy.readthedocs.io/en/latest/entropy_search_api.html)  
   Default MS2 tolerance is **0.02 Da**. Index constructor default `max_ms2_tolerance_in_da=0.024`. `calculate_entropy_similarity(..., ms2_tolerance_in_da=0.02)` uses the same window. Our live `PEAK_MZ_TOL = 0.01` is **half** that default.

3. **Li, Kind, Folz, Vaniya, Mehta, Fiehn — *Nat. Methods* (2021)**  
   [Spectral entropy outperforms MS/MS dot product](https://www.nature.com/articles/s41592-021-01331-z)  
   Entropy similarity ≥ 0.75 → FDR < 10% on 37,299 experimental NP spectra. Entropy is already our dominant hybrid weight (`ENTROPY_WEIGHT=0.75`). A too-tight fragment window under-counts matched ions and depresses true-hit entropy before that 0.75 threshold.

4. **CASMI / Enveda competition notes**  
   [Kaggle competition](https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra) · [Kaggle leaderboard](https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra/leaderboard) · [CLIST standings](https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/) · [Pilkwang overview](https://pilkwangkim.github.io/posts/CASMI-2026-From-Mass-Spectra-to-Molecular-Structures/)  
   Public LB snapshot ~2026-10-20T06:00Z: **CHU1PC 0.495**, pikachu 0.495, Oleksandr Parfionov 0.493, MarvinTMB 0.484, Oliver Ford 0.482. Community analog/forward notebooks historically ~0.32–0.42. Retrieval-only cannot claim Class-3 de novo. Exact test↔train spectrum duplicates in `enveda-180` still poison rank-1 when labels ≠ GT.

5. **Community analog / forward write-ups**  
   [Senanur Cetin 2026 case study](https://senanur-cetin.vercel.app/projects/kaggle-competitions-2026) (own retrieval ~0.309; fused forward+popularity ~0.422). High-scoring public notebooks use wider fragment matching plus analog propagation, not 10 mDa identity search.

## Methods to consider

| Priority | Method | Why it can lift MRR@25 | How (notebook, internet off) |
|----------|--------|------------------------|------------------------------|
| **P0** | **Fragment *m/z* window 0.02 Da (`PEAK_MZ_TOL`)** | Flash Entropy / ms_entropy default is 20 mDa. Live 10 mDa drops true fragment pairs after CE/instrument/centroid error, which under-scores true structures in both entropy and modified-cosine. | One config constant. Already wired through `hybrid_similarity` → `entropy_similarity` + `modified_cosine` (`tol=cfg.peak_mz_tol`). |
| P1 | Higher `MIN_SIMILARITY` (0.05 → 0.12) | Li/Fiehn FDR work implies very low hybrid scores are mostly decoys. Raising the floor may stop packing the top-25 with noise. | Config only. Next unused after this slot. |
| P1 | `TOP_PEAKS` 128 → 160 | Keep more of the cleaned ladder after the 1% intensity floor. | Config only. Slot-4 fallback already tries 160 + `MIN_SIMILARITY=0.05`. |
| P2 | CE-aware aggregation / domain prior | Already live; H-domain fallback is a no-op on current `DOMAIN_PRIOR`. | Skip this slot. |
| P2 | MS2Query / Spec2Vec / MS2Deepscore | Strong analog ranking in literature. | Heavy offline weights; 9h kernel budget; internet off. |
| P3 | Formula → candidate DB / de novo | Needed for Class-3 when the structure is absent or labels are poisoned. | Out of scope. Retrieval cannot solve Class-3. |

## Why this slot is fragment-window, not another slot-rotation knob

Actions already burned UTC slot 1 today (04:18Z) on **H-top-peaks** (`TOP_PEAKS=128`, already live). Slot 2’s fallback is still **H-entropy** (`ENTROPY_WEIGHT=0.75`, already live). Replaying it would waste UTC ticket 2. `INTENSITY_FLOOR=0.01` is also live. The first unused constant that actually changes scoring is `PEAK_MZ_TOL`.

Prior Cloud H-peak-mz PRs **#20 / #22 / #24 / #26 / #32** proposed the same 0.02 window and remain draft/unmerged, so main still scores at 0.01.

## Out of scope this cycle

- CSV `competitions submit` (notebook-only competition).
- Claiming Class-3 de novo is solved by library retrieval.
- Training MS2Deepscore / Spec2Vec inside the kernel.
- Merging prior Cloud H-peak-mz PRs (those stay historical; this cycle re-implements on current main).
