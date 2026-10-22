# Research — 2026-10-22 cycle02

## Goal

Raise public MRR@25 above the v0.1 plateau (**0.143**) toward the current public frontier (~**0.50** on CLIST). This cycle targets **fragment peak pairing**, not another no-op replay of already-live retrieval knobs.

## Sources reviewed

1. **Li, Kind, Folz, Vaniya, Mehta, Fiehn — *Nat. Methods* (2021)**  
   [Spectral entropy outperforms MS/MS dot product](https://www.nature.com/articles/s41592-021-01331-z)  
   Entropy similarity beat 42 alternatives on NIST20. On 37,299 experimental natural-product spectra, **entropy similarity ≥ 0.75** yielded **FDR < 10%**. Already live as `ENTROPY_WEIGHT=0.75`. Remaining score movement depends on *which* ions pair, not the mix weight.

2. **Li & Fiehn — *Nat. Methods* (2023) / PMC11511675**  
   [Flash Entropy Search](https://pmc.ncbi.nlm.nih.gov/articles/PMC11511675/)  
   Fragment ions are matched inside a **20 mDa** window: “maximum mass errors may occur for low-abundant ions at 10-mDa difference, we select a generous 20-mDa-wide window … to also account for possible measurement errors in library spectra.” Default cleaning: drop ions with intensity < 1% of the base peak (already live).

3. **ms_entropy API**  
   [`FlashEntropySearch.search(..., ms2_tolerance_in_da=0.02)`](https://msentropy.readthedocs.io/en/latest/entropy_search_api.html)  
   Default fragment tolerance is **0.02 Da**, not 0.01. Same default in `clean_spectrum` / identity / open / hybrid search.

4. **matchms ModifiedCosineGreedy**  
   [docs](https://matchms.readthedocs.io/en/stable/api/matchms.similarity.ModifiedCosineGreedy.html)  
   Default fragment tolerance is **0.1 Da** (unit-resolution / analog-friendly). Our 10 mDa window is an order of magnitude tighter than matchms and half of Flash Entropy. Community analog notebooks still score ~0.43–0.46.

5. **de Jonge et al. — *Nat. Commun.* (2023)**  
   [MS2Query analogue search](https://www.nature.com/articles/s41467-023-37446-4)  
   Analog ranking beats raw modified cosine for Tier-2 (known structure, no public spectrum). Out of scope this slot: needs offline weights and is heavier than a config ablation. Relevant only as the next unused *method* after peak pairing is aligned.

6. **CASMI / Enveda competition notes**  
   [Kaggle competition](https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra) · [CLIST standings](https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/) · [Pilkwang overview](https://pilkwangkim.github.io/posts/CASMI-2026-From-Mass-Spectra-to-Molecular-Structures/)  
   Metric is MRR@25. Retrieval-only cannot claim Class-3 de novo. Exact test↔train spectrum duplicates in `enveda-180` still poison rank-1 when labels ≠ GT.

## Methods to consider

| Priority | Method | Why it can lift MRR@25 | How (notebook, internet off) |
|----------|--------|------------------------|------------------------------|
| **P0** | **Fragment *m/z* window 0.02 Da** (`PEAK_MZ_TOL` 0.01 → 0.02) | Live 10 mDa matching is tighter than Flash Entropy / ms_entropy (20 mDa). Hidden test is Bruker timsTOF; train mixes Orbitrap / QTOF / timsTOF. A 15 mDa CE or calibration shift currently fails `_greedy_match` and zeros that ion's entropy/modcos contribution. Widening to 20 mDa recovers those ions without changing cleaning or the hybrid mix. | One config constant. Already wired through `hybrid_similarity(..., tol=cfg.peak_mz_tol)` in `retrieve.py`. |
| P1 | `MIN_SIMILARITY` 0.05 → 0.12 | Li/Fiehn FDR work implies very low entropy/modcos scores are mostly decoys. Raising the floor may stop packing the top-25 with noise. | Config only. |
| P1 | `TOP_PEAKS` 128 → 160 | H-peaks fallback also resets `MIN_SIMILARITY` to the already-live 0.05. Extra peaks after the 1% floor can help dense NP spectra; lower priority than the match window. | Config only. |
| P2 | CE-aware aggregation / domain prior | Already live; H-domain fallback is a no-op on current `DOMAIN_PRIOR`. | Skip this slot. |
| P2 | MS2Query / Spec2Vec / MS2Deepscore | Strong analog ranking in literature. | Heavy offline weights; 9h kernel budget; internet off. |
| P3 | Formula → candidate DB / de novo | Needed for Class-3 when the structure is absent or labels are poisoned. | Out of scope. Retrieval cannot solve Class-3. |

## Why this slot is peak pairing, not another slot-rotation knob

Actions already burned UTC slot 1 today on **H-top-peaks** (`TOP_PEAKS=128`, already live) at 04:08Z — still Chicago day 2026-10-21. Slot 2's fallback is **H-entropy** (`ENTROPY_WEIGHT=0.75`) — also already live. Replaying it would waste a ticket. `INTENSITY_FLOOR=0.01` is live after the 10-18 merge. The first unused constant that actually changes *peak pairing* is `PEAK_MZ_TOL`. Prior Cloud PRs #20/#22/#24/#26/#32/#33/#34 implemented this and stayed draft.

## Out of scope this cycle

- CSV `competitions submit` (notebook-only competition).
- Claiming Class-3 de novo is solved by library retrieval.
- Training MS2Deepscore / Spec2Vec / MS2Query inside the kernel.
- Merging prior Cloud H-peak-mz PRs #20/#22/#24/#26/#32/#33/#34 (those stay historical; this cycle re-implements on current main).
