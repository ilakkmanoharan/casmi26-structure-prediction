# Research — 2026-10-19 cycle03

## Goal

Raise public MRR@25 above the v0.1 plateau (**0.143**) toward the current public frontier (~**0.50** on CLIST). This cycle targets **fragment-ion matching tolerance**, not another replay of already-live retrieval knobs (`TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`).

## Sources reviewed

1. **Li & Fiehn — *Nat. Methods* (2023) / PMC11511675**  
   [Flash Entropy Search](https://pmc.ncbi.nlm.nih.gov/articles/PMC11511675/)  
   Fragment ions are matched inside a **±20 mDa** window. The paper notes that low-abundance ions can err by ~10 mDa and library spectra can add another ~10 mDa, so they chose a generous **20 mDa** match width. Our live `PEAK_MZ_TOL = 0.01` (10 mDa) is **half** that window.

2. **ms_entropy API**  
   [`FlashEntropySearch.search(..., ms2_tolerance_in_da=0.02)`](https://msentropy.readthedocs.io/en/latest/entropy_search_api.html)  
   Default MS2 tolerance is **0.02 Da**. Index `max_ms2_tolerance_in_da` defaults to 0.024 Da. This is the same constant our hybrid entropy/modcos scorer should use for 1–1 peak matching.

3. **Li, Kind, Folz, Vaniya, Mehta, Fiehn — *Nat. Methods* (2021)**  
   [Spectral entropy outperforms MS/MS dot product](https://www.nature.com/articles/s41592-021-01331-z)  
   Entropy similarity ≥ 0.75 gave FDR < 10% on experimental natural-product spectra. Entropy is robust to residual noise **after** cleaning, but unmatched true fragments (tolerance too tight across CE / instrument) still lower both entropy and modified cosine.

4. **matchms ModifiedCosine**  
   Default fragment `tolerance=0.1` Da (unit-resolution / analog-friendly). High-res identity search commonly uses 0.01–0.02 Da. Our hybrid already runs entropy at weight 0.75; widening match from 10→20 mDa is the Flash Entropy identity-search setting, not the 0.1 Da analog default.

5. **CASMI / Enveda competition notes**  
   [Kaggle competition](https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra) · [CLIST standings](https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/) · community analog/forward notebooks still ~0.32–0.42. Metric is MRR@25. Retrieval-only cannot claim Class-3 de novo. Exact test↔train spectrum duplicates in `enveda-180` still poison rank-1 when labels ≠ GT.

## Methods to consider

| Priority | Method | Why it can lift MRR@25 | How (notebook, internet off) |
|----------|--------|------------------------|------------------------------|
| **P0** | **20 mDa fragment match** (`PEAK_MZ_TOL` 0.01 → 0.02) | Live 10 mDa window drops true fragment pairs that Flash Entropy would merge. Orbitrap/QTOF CE differences and centroid jitter often sit in the 10–20 mDa band. Recovering those pairs raises entropy and modified-cosine for the true structure without changing the candidate pool. | One config constant. Already wired through `hybrid_similarity` → `_greedy_match`. |
| P1 | Higher `MIN_SIMILARITY` (0.05 → 0.12) | Li/Fiehn FDR work implies very low hybrid scores are mostly decoys. Raising the floor may stop packing the top-25 with noise. | Config only. Next unused after this slot. |
| P1 | `TOP_PEAKS` 128 → 160 | Keep more cleaned fragments after the 1% intensity cut. Slot-4 fallback already does this plus `MIN_SIMILARITY=0.05` (no-op on min-sim). | Config only. |
| P2 | CE-aware aggregation / domain prior | Already live; H-domain fallback is a no-op on current `DOMAIN_PRIOR`. | Skip this slot. |
| P2 | MS2Query / Spec2Vec / MS2Deepscore | Strong analog ranking in literature; public analog notebooks sit ~0.32–0.42. | Heavy offline weights; 9h kernel budget; internet off. |
| P3 | Formula → candidate DB / de novo | Needed for Class-3 when the structure is absent or labels are poisoned. | Out of scope. Retrieval cannot solve Class-3. |

## Why this slot is matching-window, not another slot-rotation knob

UTC slot 1 already burned on **H-top-peaks** (`TOP_PEAKS=128`, already live). UTC slot 2 landed as **H-entropy** (`ENTROPY_WEIGHT=0.75`, already live; Kaggle **57385301** kernel v120). Slot 3’s fallback is **H-intensity** (`INTENSITY_FLOOR=0.01`) — also already live after yesterday’s merge. Replaying it would waste a ticket. The first unused constant that actually changes peak pairing is `PEAK_MZ_TOL`.

## Out of scope this cycle

- CSV `competitions submit` (notebook-only competition).
- Claiming Class-3 de novo is solved by library retrieval.
- Training MS2Deepscore / Spec2Vec inside the kernel.
- Merging prior Cloud H-peak-mz PRs #20/#22/#24/#26 (those stay historical; this cycle re-implements on current main).
