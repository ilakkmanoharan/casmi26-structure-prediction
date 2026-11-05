# Research — 2026-11-05 cycle02

## Goal

Raise public MRR@25 above the v0.1 plateau (**0.143**) toward the live public frontier (~**0.54** on CLIST). This Cloud slot is 01:35 America/Chicago on 2026-11-05 — the first Chicago-clock ticket of the day. Actions already spent **UTC slot 1** on a no-op (`TOP_PEAKS=128`, already live). Target: **stop mixing modified cosine into entropy similarity**, not another replay of already-live retrieval knobs.

## Sources reviewed

1. **Li, Kind, Folz, Vaniya, Mehta, Fiehn — *Nat. Methods* (2021)**  
   [Spectral entropy outperforms MS/MS dot product](https://www.nature.com/articles/s41592-021-01331-z) · [PubMed 34857935](https://pubmed.ncbi.nlm.nih.gov/34857935/) · [author PDF](https://yuanyue.li/project/spectral_entropy/Yuanyue-spectral_entropy.pdf)  
   Entropy similarity beat **42** alternatives, including (weighted) dot product, on **434,287** NIST20 queries (AUC 0.958). On **37,299** experimental natural-product spectra, **entropy similarity ≥ 0.75** yielded **FDR < 10%**. Cosine never reached comparable FDR even above 0.95. Noise-ion robustness was unique to entropy: a single intense noise peak collapses cosine; entropy holds. The **0.75 figure is an identification cutoff on the entropy score**, not a mix weight with cosine.

2. **Li & Fiehn — *Nat. Methods* (2023)**  
   [Flash Entropy Search](https://www.nature.com/articles/s41592-023-02012-9) · [ms_entropy search API](https://msentropy.readthedocs.io/en/latest/entropy_search_api.html) · [classical entropy similarity](https://msentropy.readthedocs.io/en/latest/classical_entropy_similarity.html)  
   Production library search uses **entropy similarity alone** (`calculate_entropy_similarity`, default `ms2_tolerance_in_da=0.02`). Flash Entropy’s identity / open / neutral-loss / hybrid *search modes* are peak-shift strategies, not a 75/25 blend with modified cosine. `matchms.FlashSimilarity` likewise scores entropy, not cosine.

3. **Our `hybrid_similarity` (live)**  
   [`casmi26/spectrum.py`](casmi26/spectrum.py) returns `w * entropy + (1-w) * modified_cosine` with live `ENTROPY_WEIGHT=0.75`. That still injects **25% cosine** into every rank decision — the measure Li 2021 showed saturates on shared fragments and noise. The 0.75 mix was copied from the FDR *threshold*, a category error previous cycles locked in.

4. **CASMI / Enveda competition notes**  
   [Kaggle competition](https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra) · [CLIST standings](https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/) · [Pilkwang overview](https://pilkwangkim.github.io/posts/CASMI-2026-From-Mass-Spectra-to-Molecular-Structures/)  
   Metric is MRR@25. Retrieval-only cannot claim Class-3 de novo. Exact test↔train spectrum duplicates in `enveda-180` still poison rank-1 when train labels ≠ GT — exact-dup exclusion stays on.

5. **Public analog notebooks / community**  
   Analog-propagation notebooks remain ~0.43–0.46 public. They typically rank with entropy or learned embeddings, not a 25% cosine blend. The 0.464 notebook cluster on the public LB is unrelated to our 0.143 retrieval plateau.

## Methods to consider

| Priority | Method | Why it can lift MRR@25 | How (notebook, internet off) |
|----------|--------|------------------------|------------------------------|
| **P0** | **Pure entropy (`ENTROPY_WEIGHT` 0.75 → 1.0)** | Live mix is `0.75·entropy + 0.25·modcos`. Li 2021’s winning scorer is entropy **alone**; cosine is the thing it beat. The 0.75 number is an FDR cutoff, not a blend. Dropping cosine re-orders the same mass-window / 20 mDa / 128-peak candidates without changing coverage. | One config constant. Already wired through `hybrid_similarity(..., entropy_weight=cfg.entropy_weight)` in `casmi26/retrieve.py`. |
| P1 | Higher `MIN_SIMILARITY` (0.05 → 0.12) | Very low hybrid scores are mostly decoys. Raising the floor may stop packing the top-25 with noise. Cloud PR **#72** already specified this and stayed draft; do not stack it on H1. | Config only. Slot-3 fallback this cycle. |
| P1 | `TOP_PEAKS` 128 → 160 | Longer ladder after the 1% floor. | Slot-4 fallback. |
| P2 | Tighter `MASS_TOL_PPM` (35 → 10) | Orbitrap-like precursor window cuts isobaric decoys. Early cycles tried 5–15 ppm; 35 ppm is the live wide net. | Next unused day after H1 is scored. |
| P2 | MS2Query / Spec2Vec / MS2Deepscore | Strong analog ranking in literature; public analog notebooks sit at 0.43–0.46. | Heavy offline weights; 9h kernel budget; internet off. |
| P3 | Formula → candidate DB / de novo | Needed for Class-3 when the structure is absent or labels are poisoned. | Out of scope. Retrieval cannot solve Class-3. |

## Why this slot is pure entropy, not another slot-rotation knob

Actions already burned UTC slot 1 today:

- **H-top-peaks** (`TOP_PEAKS=128`, already live; Kaggle **58012064**, kernel **v195**, Actions **41976074079** at 06:06Z)

Slot 2’s fallback is **H-peak-mz** (`PEAK_MZ_TOL=0.02`) — also already live since 2026-10-24. Replaying it would waste UTC ticket 2. The first unused constant that actually changes the **score object** (not the pair window, already 20 mDa) is `ENTROPY_WEIGHT` → **1.0**.

Cloud PR **#72** (draft, 06:07Z) specified `MIN_SIMILARITY` 0.05→0.12 for this same cycle02 tag. That ablation is real, but this run picks a **distinct** major factor so two unmerged drafts are not identical, and so Actions slot-2 fallback can land a score-function change rather than a candidate-floor change.

## Out of scope this cycle

- CSV `competitions submit` (notebook-only competition).
- Claiming Class-3 de novo is solved by library retrieval.
- Training MS2Deepscore / Spec2Vec inside the kernel.
- Merging prior Cloud H-min-sim PRs #65–#72 (those stay historical; this cycle implements H-entropy-pure on current main).
