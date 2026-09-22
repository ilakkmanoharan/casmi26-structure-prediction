# Research 2026-09-22_cycle01 — MS/MS methods that can raise MRR@25

Competition: `enveda-CASMI26-molecule-id-mass-spectra` (notebook-only, internet **off**).
Metric: public **MRR@25**. Kernel cannot download embeddings, SIRIUS, or MS2Query weights.

## Sources reviewed

| Source | Link | Takeaway for this kernel |
| --- | --- | --- |
| Li, Kind, Fiehn et al., *Nat Methods* 2021 — spectral entropy | https://www.nature.com/articles/s41592-021-01331-z | Entropy similarity beat 42 scores on NIST20. Discriminative signal lives in **low-abundance ions**; ATP vs ADP is an example where dot product looks high and entropy uses the weak ions. |
| Li & Fiehn, *Nat Methods* 2023 — Flash Entropy | https://doi.org/10.1038/s41592-023-02012-9 | Same score, 10⁴× faster. Default keep ions ≳1% BPI; `max_peak_num` is 100 or unlimited — **not 5**. |
| SpectralEntropy / msentropy | https://github.com/YuanyueLi/SpectralEntropy | Reference implementation for clean + entropy. |
| de Jonge, Huber, van der Hooft, *Nat Commun* 2023 — MS2Query | https://www.nature.com/articles/s41467-023-37446-4 | Analog search: MS2Deepscore + no precursor prefilter + RF rerank beats modified cosine. Needs pretrained embeddings → **out of kernel**. |
| MassSpecGym (NeurIPS 2024) | https://github.com/pluskal-lab/MassSpecGym | Standard retrieval / de novo / spectrum-sim benchmark; reports Recall@K and ranking, not just cosine. |
| GLMR (AAAI 2026) | https://doi.org/10.1609/aaai.v40i2.37132 | Generative retrieval; JESTR top-1 still <20% on MassSpecGym. Retrieval ≠ Class-3 de novo. |
| FlexMS (2026) | https://arxiv.org/pdf/2602.22822v3 | CASMI-style retrieval after mass-based candidate lists; entropy used as a diagnostic, not a 5-peak toy spectrum. |
| Public Kaggle LB 2026-09-22 | https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra/leaderboard | Top public **0.415** (Ozymandias31415). ~0.33–0.34 analog / multi-channel notebooks are the open SOTA cluster. |
| Public code: Analog Ranker ~0.337; Quad-Channel ~0.339; Strong Retrieval ~0.335 | https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra/code | Community is scoring analogs + multi-channel rankers, not 5-peak exact-lib hits. Notes: sort order moves MRR (~0.03 / 250 queries); decoys cost ~16.5%; tight ppm drops ~122k library spectra. |

## Methods to consider

### P0 — Restore the fragment ladder (`TOP_PEAKS` 5 → 128)

Cycle05 (kernel v13 / Kaggle 56298621) set `TOP_PEAKS=5`. `clean_spectrum()` then keeps only the five strongest peaks before entropy and modified cosine. That:

1. Throws away the weak ions entropy was designed to use (Li & Fiehn 2021 Fig. 4 / Ext. Data 4).
2. Makes two different full spectra look identical after cleaning, so the poisoned-dup InChIKey ban is both too aggressive and too coarse.
3. Caps analog evidence that current 0.33–0.41 public notebooks are exploiting.

Flash Entropy / msentropy keep ~100 peaks or all peaks above ~1% BPI. 128 is the smallest restore that matches that literature and previous unmerged 09-18…09-21 cloud cycles.

**How it raises MRR@25:** more true library / analog hits enter the top-25; fewer false “identical” bans; better rank of the first correct InChIKey.

### P1 — Analog / wider-mass hybrid (later slot)

MS2Query and the 0.337 analog-ranker notebooks do **not** require exact precursor match. Our `MASS_TOL_PPM=10` + structure-level mass filter is identity search. A later slot can widen `MASS_TOL_PPM_BACKFILL` or drop structure-mass contradiction for analog fill only. Not this slot — one major factor.

### P1 — Ranker / sort order (later slot)

Community writeups claim sort order alone moved MRR by ~0.03. Our `WEIGHTS` already mix similarity, support, mass error, contradiction. Touching ranker weights while `TOP_PEAKS=5` would confound the ablation.

### P2 — Entropy weight 0.70; CE aggregation; tautomer-aware fill

Still valid. 2026-09-15 cycle02 specified `ENTROPY_WEIGHT=0.70` but the kernel ERRORed and never scored. Do not stack on this slot.

## Priority table (internet-off notebook)

| Pri | Method | Kernel-feasible? | This slot? |
| --- | --- | --- | --- |
| P0 | `TOP_PEAKS=128` fragment ladder | yes | **yes** |
| P1 | Analog / wider mass backfill | yes | no |
| P1 | Ranker / sort-order weights | yes | no |
| P2 | `ENTROPY_WEIGHT=0.70` | yes | no |
| P2 | MS2Query / Spec2Vec / MS2Deepscore | no (weights + internet) | no |
| P2 | SIRIUS / Class-3 de novo | no | no |

## Out of scope this cycle

- Claiming Class-3 de novo is solved by retrieval.
- CSV `competitions submit`.
- Training embeddings or enabling kernel internet.
- Changing mass tolerances or entropy weight in the same submit as the peak restore.
