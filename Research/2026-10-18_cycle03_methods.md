# Research — 2026-10-18 cycle03

## Goal

Raise public MRR@25 above the v0.1 plateau (**0.143**) toward the current public frontier (~**0.50** on CLIST). This cycle targets **spectrum cleaning**, not another no-op replay of already-live retrieval knobs.

## Sources reviewed

1. **Li, Kind, Folz, Vaniya, Mehta, Fiehn — *Nat. Methods* (2021)**  
   [Spectral entropy outperforms MS/MS dot product](https://www.nature.com/articles/s41592-021-01331-z)  
   Entropy similarity beat 42 alternatives on NIST20 (AUC 0.958). On 37,299 experimental natural-product spectra, **entropy similarity ≥ 0.75** yielded **FDR < 10%**. Entropy remains robust after synthetic noise ions are added — but only after low-abundance junk is down-weighted / removed.

2. **Li & Fiehn — *Nat. Methods* (2023) / PMC11511675**  
   [Flash Entropy Search](https://pmc.ncbi.nlm.nih.gov/articles/PMC11511675/)  
   Default cleaning: drop ions with **intensity < 1% of the base peak**, drop *m/z* > precursor − 1.6 Da, centroid within 0.05 Da, then entropy-weight. The paper argues ions below 1% of max fragment abundance are more likely isolation-window / instrument noise than true fragments.

3. **ms_entropy API**  
   [`FlashEntropySearch.search(..., noise_threshold=0.01)`](https://msentropy.readthedocs.io/en/latest/entropy_search_api.html)  
   Peaks with `intensity < noise_threshold * max(intensity)` are removed. Default **0.01**. Same default in `clean_spectrum_for_search`.

4. **matchms / community analog notebooks (CASMI 2026 write-ups)**  
   Public analog-propagation notebooks still score ~0.32–0.42. They typically apply a relative intensity cut before modified-cosine / entropy. Our live `INTENSITY_FLOOR = 0.001` (0.1%) is **10× more permissive** than Flash Entropy’s default.

5. **CASMI / Enveda competition notes**  
   [Kaggle competition](https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra) · [CLIST standings](https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/) · [Pilkwang overview](https://pilkwangkim.github.io/posts/CASMI-2026-From-Mass-Spectra-to-Molecular-Structures/)  
   Metric is MRR@25. Retrieval-only cannot claim Class-3 de novo. Exact test↔train spectrum duplicates in `enveda-180` still poison rank-1 when labels ≠ GT.

## Methods to consider

| Priority | Method | Why it can lift MRR@25 | How (notebook, internet off) |
|----------|--------|------------------------|------------------------------|
| **P0** | **1% relative intensity floor** (`INTENSITY_FLOOR` 0.001 → 0.01) | Live 0.1% floor keeps isolation-window junk that entropy/modcos still score. Flash Entropy / ms_entropy default is 1%. Cutting those ions should reduce false high-similarity hits on poisoned or analog-near decoys and free the top-128 ladder for real fragments. | One config constant. Already wired through `clean_spectrum` → index + retrieve. |
| P1 | Fragment *m/z* window 0.02 Da (`PEAK_MZ_TOL`) | Flash Entropy uses ~20 mDa fragment matching; we still score at 0.01 Da. Slightly wider matching can recover CE/instrument shifts. | Config only. Prior Cloud PRs #20/#22/#24/#26 (unmerged). |
| P1 | Higher `MIN_SIMILARITY` (0.05 → 0.12) | Li/Fiehn FDR work implies very low entropy/modcos scores are mostly decoys. Raising the floor may stop packing the top-25 with noise. | Config only. |
| P2 | CE-aware aggregation / domain prior | Already live; H-domain fallback is a no-op on current `DOMAIN_PRIOR`. | Skip this slot. |
| P2 | MS2Query / Spec2Vec / MS2Deepscore | Strong analog ranking in literature. | Heavy offline weights; 9h kernel budget; internet off. |
| P3 | Formula → candidate DB / de novo | Needed for Class-3 when the structure is absent or labels are poisoned. | Out of scope. Retrieval cannot solve Class-3. |

## Why this slot is cleaning, not another slot-rotation knob

Actions already burned UTC slots 1–2 today on **H-top-peaks** (`TOP_PEAKS=128`, already live) and **H-entropy** (`ENTROPY_WEIGHT=0.75`, already live). Slot 3’s fallback is **H-mass-wide** (35/80 ppm + `TOP_K=120`) — also already live. Replaying it would waste a ticket. The first unused constant that actually changes the spectrum object is `INTENSITY_FLOOR`.

## Out of scope this cycle

- CSV `competitions submit` (notebook-only competition).
- Claiming Class-3 de novo is solved by library retrieval.
- Training MS2Deepscore / Spec2Vec inside the kernel.
- Merging prior Cloud H-intensity PRs #13–#19, #21, #23, #25, #27–#31 (those stay historical; this cycle re-implements on current main).
