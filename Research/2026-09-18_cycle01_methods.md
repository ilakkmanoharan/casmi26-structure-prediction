# Research — 2026-09-18 cycle01

## Goal

Raise public MRR@25 above the last scored notebook (**0.143**, v0.1) toward the current public leaders (~**0.33**). Focus on methods that fit an internet-off Kaggle notebook using the existing hybrid entropy / modified-cosine retrieval stack.

## Sources reviewed

1. **Li, Kind, Folz, Vaniya, Mehta & Fiehn, Nat. Methods (2021)** — Spectral entropy similarity outperforms dot product for small-molecule ID. Noise ions below **1% of base-peak intensity** are removed; remaining fragment ions are kept (no “top-5 peaks” cut). Matching used **0.05 Da**. https://www.nature.com/articles/s41592-021-01331-z and PDF https://yuanyue.li/project/spectral_entropy/Yuanyue-spectral_entropy.pdf
2. **msentropy / `clean_spectrum` docs** — Default `noise_threshold=0.01`, `max_peak_num=-1` (keep all peaks after the 1% floor). Optional cap exists for speed, not for accuracy. https://msentropy.readthedocs.io/en/latest/classical_spectral_entropy.html
3. **Li & Fiehn, Nat. Methods (2023) Flash Entropy Search** — Same 1% noise cut; `max_peak_num` default **0 / unlimited**. Precursor and ions above `precursor_mz − 1.6 Da` are removed; fragment matching often **~20 mDa**. https://doi.org/10.1038/s41592-023-02012-9 and API https://msentropy.readthedocs.io/en/latest/entropy_search_api.html
4. **matchms `FlashSimilarity`** — Built-in cleanup: 1% `noise_cutoff`, optional precursor window 1.6 Da, entropy weighting. No 5-peak truncation. https://matchms.readthedocs.io/en/latest/api/matchms.similarity.FlashSimilarity.html
5. **de Jonge et al., Nat. Commun. (2023) MS2Query** — Analog search without precursor-mass prefilter; MS2Deepscore → top-2000 → RF rerank with Spec2Vec + Δm/z. Strong method, but weights/models are out of scope for this internet-off kernel. https://www.nature.com/articles/s41467-023-37446-4
6. **Prior cycle research** — `Research/2026-09-15_cycle01_methods.md` already prioritized exclude-exact-dups, entropy hybrid, and full libraries. v0.2 spec asked for `top_peaks=128`.

## Methods to consider

| Priority | Method | Why it can lift MRR@25 | How (this kernel) |
|----------|--------|------------------------|-------------------|
| **P0** | **Stop truncating spectra to 5 peaks** | Entropy similarity and modified cosine need the fragment ladder, not just the 5 tallest ions. Li/Fiehn and Flash Entropy keep *all* ions above 1% BPI (`max_peak_num` unlimited or 1000). Current `TOP_PEAKS=5` (cycle05) throws away most matching signal and also makes the exact-dup detector compare 5-peak fingerprints, so unrelated spectra can look “identical.” | Set `TOP_PEAKS=128` (v0.2 spec; still well below msentropy’s 1000, kernel-runtime safe). |
| P1 | Align noise floor with literature (1% BPI) | 0.1% floor + 128 peaks may keep some noise; 1% is the entropy-search default. | Later slot: `INTENSITY_FLOOR=0.01` as its own ablation. |
| P1 | Entropy weight toward literature entropy similarity | Cycle02 specified `ENTROPY_WEIGHT=0.70` but never scored (kernel ERROR). Current 0.60 is a mild hybrid. | Later slot after peak-count is restored. |
| P1 | Structure-level ExactMolWt gate | Filters adduct-inconsistent decoys after poisoned exact-dups are banned. | Already a soft contradiction penalty; keep for a later isolated ablation. |
| P2 | Flash Entropy hybrid fragment+neutral-loss index | Faster / more complete library scan than linear mass-window scan. | Rewrite `index.py`; too large for one slot. |
| P2 | MS2Query / MS2Deepscore analog path | Recovers structures absent from the exact-mass window (true Class-3 analogs). | Needs offline embeddings; internet off. |
| P3 | De novo (DiffMS, MSNovelist) | Class-3 only; retrieval cannot invent missing structures. | Out of scope. Do not claim retrieval solves de novo. |

## How this improves score (operational)

1. Cycle05’s `TOP_PEAKS=5` is the largest remaining self-inflicted failure mode in config. Restore a literature-compatible peak budget **before** retuning mass ppm or entropy weight again.
2. Keep `EXCLUDE_EXACT_DUPLICATES=true`: v0.1 still teaches that exact test↔train clones in `enveda-180` have labels ≠ competition GT (~0.143 despite sim=1.0).
3. With 128 peaks, entropy/modcos can actually discriminate near-isobars instead of comparing 5-ion cartoons.
4. Exact-dup bans become stricter (true clones still match; coincidental top-5 clones no longer poison the IK ban list).

## Out of scope this cycle

- MS2Deepscore / Spec2Vec / MS2Query weights
- Unconstrained LLM SMILES / de novo generation
- Changing mass tolerances (already ablated on 2026-09-17)
- CSV `competitions submit` (notebook-only competition)
