# Research — 2026-11-07 cycle02

## Goal

Raise public MRR@25 above the v0.1 plateau (**0.143**) toward the live public frontier (**0.54** on CLIST). This Cloud slot (09:04 UTC / 03:04 CST, Chicago day open) is the first unused **real** ablation after Actions already spent UTC ticket 1 on a no-op replay of live `TOP_PEAKS=128`. Target: **pure Li/Fiehn entropy similarity**, not another replay of already-live fragment knobs and not a duplicate of unmerged Cloud drafts #82 (H-sim-gate) / #83 (H-mass-tight).

## Sources reviewed

1. **Li, Kind, Folz, Vaniya, Mehta, Fiehn — *Nat. Methods* (2021)**  
   [Spectral entropy outperforms MS/MS dot product](https://www.nature.com/articles/s41592-021-01331-z) · [PMC11492813](https://pmc.ncbi.nlm.nih.gov/articles/PMC11492813/)  
   Entropy similarity beat 42 alternatives on NIST20 (AUC **0.958**), including classic dot product. On 37,299 experimental natural-product spectra, **entropy similarity ≥ 0.75** yielded **FDR < 10%**. That 0.75 figure is a *score threshold*, not a mix weight. Our live `ENTROPY_WEIGHT=0.75` is a *blend*: `0.75·entropy + 0.25·modified_cosine`. The remaining 25% cosine still ranks candidates the 2021 paper showed entropy already beats.

2. **Li & Fiehn — *Nat. Methods* (2023) / Flash Entropy Search**  
   [eScholarship PDF](https://escholarship.org/content/qt33d9t00t/qt33d9t00t.pdf) · [ms_entropy API](https://msentropy.readthedocs.io/en/latest/entropy_search_api.html)  
   Flash Entropy identity / hybrid / open search all **return entropy similarity**, not a cosine blend. Hybrid search here means “match fragment *or* unused-peak neutral loss, each peak at most once” — still scored as entropy. Default fragment window is **±0.02 Da**, already live as `PEAK_MZ_TOL=0.02`. The leftover mismatch vs that recipe is our 0.25 modified-cosine mix.

3. **matchms `EntropyFlash` / `FlashSimilarity`**  
   [matchms.similarity.flash_similarity](https://matchms.readthedocs.io/en/development/_modules/matchms/similarity/flash_similarity.html)  
   EntropyFlash accumulates entropy similarity from indexed peak matches. Default `tolerance=0.02` Da. Community analog notebooks at ~0.43–0.46 MRR also sit on 20 mDa entropy-style pairing, not a 75/25 hybrid.

4. **Stein & Scott (1994) + Bittremieux et al. (2022) on modified cosine**  
   [Stein & Scott, *JASMS* 1994](https://doi.org/10.1016/1044-0305(94)87009-8) · [Bittremieux, *JASMS* 2022](https://doi.org/10.1021/jasms.2c00153)  
   Dot-product / modified cosine is the right tool for **analogue discovery** (GNPS molecular networking; shifted fragments). This competition metric is **identity MRR@25** after tautomer-canonical InChIKey14. Mixing analogue-oriented cosine into identity ranking dilutes entropy’s FDR advantage on near-matches and can promote CE-shifted decoys that share a few intense ions.

5. **de Jonge, Hecht, van der Hooft et al. — *Nat. Commun.* (2023)**  
   [MS2Query analogue search](https://www.nature.com/articles/s41467-023-37446-4)  
   Exact-match library search saturates; analogue / fingerprint channels lift chemical neighbors when the true structure is absent. Out of scope for this one-constant slot (needs embeddings). Motivates *not* using modified cosine as a cheap analogue substitute inside identity search — that job belongs to a later channel, not a 0.25 mix.

6. **CASMI / Enveda competition notes**  
   [Kaggle competition](https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra) · [CLIST standings](https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/) · [shiferaxa/casmi26](https://github.com/shiferaxa/casmi26)  
   Metric is MRR@25. Public 0.5-band pipelines treat library entropy as one evidence *channel*, not a cosine hybrid. Retrieval-only cannot claim Class-3 de novo. Exact test↔train spectrum duplicates in `enveda-180` still poison rank-1 when train labels ≠ GT — exact-dup exclusion stays on.

## Methods to consider

| Priority | Method | Why it can lift MRR@25 | How (notebook, internet off) |
|----------|--------|------------------------|------------------------------|
| **P0** | **Pure entropy (`ENTROPY_WEIGHT` 0.75 → 1.0)** | Live hybrid still injects 25% modified cosine into every `hybrid_similarity` call. Li 2021 showed entropy ≫ cosine for identity; Flash Entropy scores identity search with entropy only. After 20 mDa pairing landed, the mix is the leftover mismatch vs that recipe. Dropping cosine re-orders the same mass-window candidates so true near-matches are not outranked by intense-ion cosine decoys. | One config constant. Already wired through `hybrid_similarity(..., entropy_weight=cfg.entropy_weight)` in `casmi26/retrieve.py`. |
| P1 | `MIN_SIMILARITY` 0.05 → 0.12 | Li/Fiehn FDR work implies very low entropy scores are mostly decoys. Draft PR **#82** already implements this; do not duplicate it this slot. | Config only. Slot-3 fallback retarget. |
| P1 | `MASS_TOL_PPM` 35 → 15 | ibnmarzuk 15 ppm / shiferaxa 8.5 ppm vs our live 35 ppm. Draft PR **#83** already implements 15 ppm; do not duplicate it this slot. | Config only. Slot-4 fallback retarget. |
| P2 | Analog Tanimoto / MS2Query-style channel | Public 0.43–0.54 pipelines use analog evidence when exact library match is poisoned. | Fingerprints + extra ranking; too large for one hourly kernel change. |
| P2 | MS2Deepscore / Spec2Vec | Strong analog ranking in literature. | Heavy offline weights; internet off. |
| P3 | Formula → candidate DB / de novo | Needed for Class-3 when the structure is absent. | Out of scope. Retrieval cannot solve Class-3. |

## Why this slot is pure entropy, not another slot-rotation knob

Actions already burned UTC slot 1 today:

- **H-top-peaks** (`TOP_PEAKS=128`, already live; Kaggle **58076904**, kernel v202 at 02:53Z)

Slot 2’s fallback on `origin/main` is **H-peak-mz** (`PEAK_MZ_TOL=0.02`) — also already live since mid-October. Slot 3 is the same no-op. Replaying either wastes UTC tickets 2–3.

`ENTROPY_WEIGHT=0.75` has been live since ~2026-09-26. It has **not** been tried at **1.0** on top of the current fragment defaults (`PEAK_MZ_TOL=0.02`, `TOP_PEAKS=128`, `INTENSITY_FLOOR=0.01`). That combination is a new ablation, not a no-op.

Unmerged Cloud drafts already occupy the other two unused real levers (**#82** H-sim-gate, **#83** H-mass-tight). This cycle implements the remaining lever so whichever PR merges, UTC ticket 2 is a real change.

## Out of scope this cycle

- CSV `competitions submit` (notebook-only competition).
- Claiming Class-3 de novo is solved by library retrieval.
- Training MS2Deepscore / Spec2Vec / analog Tanimoto inside the kernel.
- Changing `MIN_SIMILARITY` or `MASS_TOL_PPM` in the same kernel (leave those for later slots / the other drafts).
- Merging prior Cloud H-sim-gate / H-mass-tight PRs (those stay historical; this cycle re-implements a *different* constant on current main).
