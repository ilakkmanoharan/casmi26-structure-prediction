# Research — 2026-10-24 cycle03

## Goal

Raise public MRR@25 above the v0.1 plateau (**0.143**) toward the live public frontier (~**0.50** on CLIST). This Chicago-day Cloud slot (01:00 CDT / 06:00 UTC) is the first unused **real** ablation after Actions already spent UTC tickets 1–2 on no-ops. Target: **fragment *m/z* matching tolerance**, not another replay of already-live retrieval knobs.

## Sources reviewed

1. **Li, Kind, Folz, Vaniya, Mehta, Fiehn — *Nat. Methods* (2021)**  
   [Spectral entropy outperforms MS/MS dot product](https://www.nature.com/articles/s41592-021-01331-z)  
   Entropy similarity beat 42 alternatives on NIST20 (AUC 0.958). On 37,299 experimental natural-product spectra, **entropy similarity ≥ 0.75** yielded **FDR < 10%**. That mix weight is already live (`ENTROPY_WEIGHT=0.75`). The remaining mismatch vs Flash Entropy is the fragment-pair window, not the mix weight.

2. **Li & Fiehn — *Nat. Methods* (2023) / PMC11511675**  
   [Flash Entropy Search](https://pmc.ncbi.nlm.nih.gov/articles/PMC11511675/)  
   After the 1% noise cut and precursor-ion removal, Flash Entropy matches fragment ions inside a **±20 mDa** window. The paper notes low-abundance ions can err by ~10 mDa and therefore chooses a generous 20 mDa window to also cover library measurement error. Our live `PEAK_MZ_TOL=0.01` is half that window.

3. **ms_entropy API**  
   [`FlashEntropySearch.search(..., ms2_tolerance_in_da=0.02)`](https://msentropy.readthedocs.io/en/latest/entropy_search_api.html)  
   Default **0.02 Da**. Same default in `flash_entropy_search_core.search`. Index construction uses `max_ms2_tolerance_in_da=0.024`, so 0.02 Da is a valid operating point.

4. **matchms `FlashSimilarity`**  
   [matchms.similarity.FlashSimilarity](https://matchms.readthedocs.io/en/stable/api/matchms.similarity.FlashSimilarity.html)  
   Default `tolerance=0.02` Da (`use_ppm=False`). Cleanup already matches our live intensity floor (`noise_cutoff=0.01`).

5. **CASMI / Enveda competition notes**  
   [Kaggle competition](https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra) · [CLIST standings](https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/) · [Pilkwang overview](https://pilkwangkim.github.io/posts/CASMI-2026-From-Mass-Spectra-to-Molecular-Structures/)  
   Metric is MRR@25. Retrieval-only cannot claim Class-3 de novo. Exact test↔train spectrum duplicates in `enveda-180` still poison rank-1 when train labels ≠ GT — exact-dup exclusion stays on.

6. **Public analog notebooks (community, ~2026-10-21)**  
   Analog-propagation notebooks report public MRR@25 ~0.43–0.46 (e.g. Analog Propagation V43 at 0.456). They typically use ~0.02 Da fragment matching, not 10 mDa.

## Methods to consider

| Priority | Method | Why it can lift MRR@25 | How (notebook, internet off) |
|----------|--------|------------------------|------------------------------|
| **P0** | **Fragment *m/z* window 0.02 Da (`PEAK_MZ_TOL` 0.01 → 0.02)** | Live 10 mDa pairing is tighter than Flash Entropy / ms_entropy / matchms defaults (20 mDa). CE and instrument shifts between GNPS / MassBank / MONA / Enveda libraries routinely exceed 10 mDa on mid-intensity ions. Widening the pair window recovers true-structure near-matches that currently score below `MIN_SIMILARITY` and never enter the top-25. | One config constant. Already wired through `hybrid_similarity(..., tol=cfg.peak_mz_tol)` in `casmi26/retrieve.py`. |
| P1 | Higher `MIN_SIMILARITY` (0.05 → 0.12) | Li/Fiehn FDR work implies very low entropy/modcos scores are mostly decoys. Raising the floor may stop packing the top-25 with noise. | Config only. Next unused slot after H-peak-mz. |
| P1 | `TOP_PEAKS` 128 → 160 | Longer ladder after the 1% floor. Risk: more noise ions if the floor is already doing its job. | Slot-4 fallback already tries 160 + min_sim 0.05. |
| P2 | CE-aware aggregation / domain prior | Already live; H-domain fallback is a no-op on current `DOMAIN_PRIOR`. | Skip this slot. |
| P2 | MS2Query / Spec2Vec / MS2Deepscore | Strong analog ranking in literature; public analog notebooks sit at 0.43–0.46. | Heavy offline weights; 9h kernel budget; internet off. |
| P3 | Formula → candidate DB / de novo | Needed for Class-3 when the structure is absent or labels are poisoned. | Out of scope. Retrieval cannot solve Class-3. |

## Why this slot is fragment tolerance, not another slot-rotation knob

Actions already burned UTC slots 1–2 today:

- **H-top-peaks** (`TOP_PEAKS=128`, already live; Kaggle **57576969**, kernel v144 at 00:39Z)
- **H-entropy** (`ENTROPY_WEIGHT=0.75`, already live; Kaggle **57584149**, kernel v145 at 05:48Z)

Slot 3’s fallback is **H-intensity** (`INTENSITY_FLOOR=0.01`) — also already live. Replaying it would waste UTC ticket 3. The first unused constant that actually changes the similarity object is `PEAK_MZ_TOL`.

Cloud PRs #20/#22/#24/#26/#32/#33/#34/#35/#36 already specified this ablation and stayed draft/unmerged; Actions later spent those days’ next unused slot on the fallback no-op. This cycle re-implements on current main and retargets the Actions slot-2 and slot-3 fallbacks so a 429/no-key hourly run cannot replay 0.75 / 0.01.

## Out of scope this cycle

- CSV `competitions submit` (notebook-only competition).
- Claiming Class-3 de novo is solved by library retrieval.
- Training MS2Deepscore / Spec2Vec inside the kernel.
- Merging prior Cloud H-peak-mz PRs #20/#22/#24/#26/#32/#33/#34/#35/#36 (those stay historical; this cycle re-implements on current main).
