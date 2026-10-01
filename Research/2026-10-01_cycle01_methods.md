# Research 2026-10-01_cycle01 — entropy cleaning vs analog rankers

Competition day **2026-10-01** (anchor 01:00 America/Chicago). Cycle **01** of 5.
Notebook-only, internet-off kernel. Metric: public **MRR@25**.

## Sources reviewed

| Source | Why it matters |
|--------|----------------|
| Li, Kind, Folz, Vaniya, Mehta, Fiehn. *Spectral entropy outperforms MS/MS dot product similarity…* Nature Methods (2021). https://www.nature.com/articles/s41592-021-01331-z | Entropy similarity beat 42 alternatives on NIST20. FDR **&lt;10%** at similarity **0.75** on 37,299 experimental natural-product spectra. Low-abundance ions must be *weighted*, not treated as equal to chemical noise. |
| Li & Fiehn. *Flash entropy search…* Nat Biotechnol / PMC11511675. https://pmc.ncbi.nlm.nih.gov/articles/PMC11511675/ | Production entropy search: **20 mDa** fragment window, precursor drop above `precursor_mz − 1.6 Da`, **1% of base-peak** noise cut before scoring. |
| MSEntropy docs (`noise_threshold`). https://msentropy.readthedocs.io/en/latest/entropy_search_basic_usage.html | Peaks with intensity `&lt; noise_threshold * max(I)` are removed. Default literature value is **0.01**. |
| matchms `FlashSimilarity`. https://matchms.readthedocs.io/en/latest/api/matchms.similarity.FlashSimilarity.html | Same stack: `noise_cutoff=0.01`, `tolerance=0.02` Da, optional hybrid / neutral-loss modes, `normalize_to_half=True`. |
| Huber et al. / matchms analog eval (modified cosine vs ML). https://exa.ai/library/publication/0vn9z33qspl | When the exact InChIKey is **absent**, modified-cosine analog retrieval remains competitive with learned embeddings. Exact-ID retrieval and analog retrieval are different jobs. |
| Bittremieux / intensity+m/z weighting. https://exa.ai/library/publication/krbqnm0jz5j | Weighting *informative* low-intensity fragments helps; keeping *uninformative* noise does not. A 1% floor is the usual first cut before re-weighting. |
| Goldman et al. MS2Mol (CASMI 2022 / EnvedaLight). https://exa.ai/library/publication/jr07ygw9lzq | De novo transformers help Class-3 / library-absent molecules. CSI:FingerID still wins exact-match when the structure is in a DB. **Retrieval alone does not solve Class-3 de novo.** |
| Kaggle Code tab + CLIST standings (fetched 2026-10-01T06:05Z) | Public notebooks branded “analog / quad-channel / two ranker” report **0.32–0.34**. CLIST public top: **pikachu 0.46**, Randy 0.44, Ozymandias31415 0.43. |

## Methods to consider

1. **1% intensity floor (`INTENSITY_FLOOR=0.01`)** — P0 this slot.
   - *Why:* `casmi26.spectrum.clean_spectrum` currently keeps peaks down to **0.1% of base peak** (`0.001`). Flash entropy / matchms / msentropy all drop anything below **1%** before entropy weighting. Keeping chemical noise and electronic spikes inflates hybrid entropy/modcos, especially with `TOP_PEAKS=160`.
   - *How it can raise MRR@25:* fewer false high-similarity hits on poisoned or near-noise ladders; remaining peaks are the ones entropy was calibrated on. Rank of the first correct InChIKey14 should move up if we are currently matching junk.

2. **Analog / modified-cosine channel (already on, do not retune today).**
   - Top public notebooks are analog/multi-evidence rankers, not 5-peak cosine. We already mix entropy + modified cosine (`ENTROPY_WEIGHT=0.75`) plus neutral-loss. Further analog work is a later slot (separate evidence channel), not this ablation.

3. **MIN_SIMILARITY 0.05 → ~0.12** — P1 next unused.
   - Li/Fiehn treat 0.75 as a *library-ID* cutoff (FDR). MRR@25 wants recall of the right structure *somewhere* in 25, so a hard 0.75 gate is too harsh. 0.12 is a conservative noise floor used in Cloud PRs #11/#12 (never merged).

4. **PEAK_MZ_TOL 0.01 → 0.02 Da** — P1.
   - Flash entropy’s default fragment window is **20 mDa**. We are tighter (10 mDa). One-factor later.

5. **Domain-prior / formula+exact-mass rerank** — P2.
   - Current `H-domain` fallback is a no-op (`config_patch: {}` with priors already at those values). A real boost would change `DOMAIN_PRIOR` numbers, not re-apply the same dict.

6. **Class-3 de novo (MS2Mol / CSI:FingerID-style)** — out of scope this kernel.
   - Internet off, no SIRIUS, no GPU transformer. Do **not** claim retrieval solves de novo.

## Priority for a notebook-only, internet-off kernel

| Pri | Method | Fit |
|-----|--------|-----|
| **P0** | `INTENSITY_FLOOR` 0.001 → **0.01** | One existing constant; never submitted on `main`; literature default |
| P1 | `MIN_SIMILARITY` 0.05 → 0.12 | Cloud PRs #11/#12; next slot if this lands |
| P1 | `PEAK_MZ_TOL` 0.01 → 0.02 | Flash default; do not stack today |
| P2 | Real `DOMAIN_PRIOR` boost | Current H-domain fallback is a no-op |
| out | CSV submit, internet-on kernel, “de novo solved” | Forbidden |

## Explicitly out of scope this cycle

- Changing `TOP_PEAKS` (already 160 on `main`; slot-1 fallback `H-top-peaks` would be a no-op / regression).
- Changing `ENTROPY_WEIGHT` (already 0.75).
- Widening mass windows again (already 35/80 ppm + `TOP_K=120`).
- Training Spec2Vec / MS2DeepScore / MS2Query (no internet, no extra datasets).
- Claiming Class-3 coverage from library retrieval.
