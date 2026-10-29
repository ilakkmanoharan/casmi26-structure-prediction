# Research — 2026-10-29 cycle03

## Goal

Raise public MRR@25 above the v0.1 plateau (**0.143**) toward the live public frontier (~**0.50–0.52** on CLIST). This Cloud slot is **05:30 America/Chicago / 10:30 UTC** — the first unused **real** ablation after Actions already spent UTC tickets 1–2 on no-ops (`TOP_PEAKS=128` already live; `PEAK_MZ_TOL=0.02` already live). Target: **library-hit admission floor** (`MIN_SIMILARITY` 0.05 → 0.12), not another replay of already-live retrieval knobs.

## Sources reviewed

1. **Li, Kind, Folz, Vaniya, Mehta, Fiehn — *Nat. Methods* (2021)**  
   [Spectral entropy outperforms MS/MS dot product](https://www.nature.com/articles/s41592-021-01331-z) · [PDF](https://escholarship.org/content/qt0249w6hk/qt0249w6hk.pdf)  
   Entropy similarity beat 42 alternatives on NIST20 (AUC 0.958). On 37,299 experimental natural-product spectra, **entropy similarity ≥ 0.75** yielded **FDR < 10%**. That mix weight is already live (`ENTROPY_WEIGHT=0.75`). The 0.75 figure is a *call* threshold for claiming an annotation, **not** an admission floor into a top-25 rank list. Scores well below 0.75 are mostly decoys; packing them into MRR@25 wastes slots.

2. **Li & Fiehn — Flash Entropy Search (2023)**  
   [PMC11511675](https://pmc.ncbi.nlm.nih.gov/articles/PMC11511675/) · [ms_entropy default `ms2_tolerance_in_da=0.02`](https://msentropy.readthedocs.io/en/latest/entropy_search_api.html)  
   Fragment pairing at 20 mDa and the 1% intensity floor are already live (`PEAK_MZ_TOL=0.02`, `INTENSITY_FLOOR=0.01`). Remaining retrieval leak is which weak hits are allowed into the rank list after pairing.

3. **GNPS spectral library search / MASST**  
   [Library search](https://ccms-ucsd.github.io/GNPSDocumentation/librarysearch/) default cosine **0.5**, min 6 matched peaks.  
   [MASST](https://ccms-ucsd.github.io/GNPSDocumentation/masst/) default cosine **0.7**.  
   [microbeMASST](https://ccms-ucsd.github.io/GNPSDocumentation/microbemasst/) default cosine **0.7**, min 3 matched peaks.  
   Our live `MIN_SIMILARITY=0.05` is an order of magnitude below every GNPS admission default. Raising it to **0.12** is a conservative step toward those floors without jumping to 0.5–0.7, which would empty too many CASMI rank lists (MRR@25 needs up to 25 candidates per query).

4. **matchms modified cosine**  
   [matchms.similarity](https://matchms.readthedocs.io/en/stable/api/matchms.similarity.html)  
   Cosine / modified-cosine are similarity *scores*, not rank-list padders. A low score should not occupy a top-25 slot if a better-supported structure exists.

5. **CASMI / Enveda competition notes**  
   [Kaggle competition](https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra) · [CLIST standings](https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/) · [Pilkwang overview](https://pilkwangkim.github.io/posts/CASMI-2026-From-Mass-Spectra-to-Molecular-Structures/)  
   Metric is MRR@25. Retrieval-only cannot claim Class-3 de novo. Exact test↔train spectrum duplicates in `enveda-180` still poison rank-1 when train labels ≠ GT — exact-dup exclusion stays on.

6. **Public analog notebooks (community)**  
   Analog-propagation notebooks report public MRR@25 ~0.43–0.46 (e.g. Analog Propagation V43 at 0.456). They rank by analog evidence, not by packing sub-0.05 library hits. Copied-notebook pile ~0.464. Gap vs 0.143 is not a missing `PEAK_MZ_TOL` constant — that is already live.

## Methods to consider

| Priority | Method | Why it can lift MRR@25 | How (notebook, internet off) |
|----------|--------|------------------------|------------------------------|
| **P0** | **Raise `MIN_SIMILARITY` 0.05 → 0.12** | Live 0.05 admits near-noise hybrid scores into `retrieve.py` (`if sim >= cfg.min_similarity` before `top_k` truncation). Li/Fiehn FDR work and GNPS 0.5–0.7 defaults both say those hits are decoys. Dropping them frees top-25 slots for higher-support structures. 0.12 is well below a 0.75 *call* threshold, so sparse-but-real hits still enter. | One config constant. Already wired. |
| P1 | `TOP_PEAKS` 128 → 160 | Longer ladder after the 1% floor. Risk: more noise ions if the floor is already doing its job. | Slot-4 fallback after this PR (TOP_PEAKS=160 only; do not reset MIN_SIMILARITY). |
| P2 | CE-aware aggregation / domain prior | Already live; H-domain fallback is a no-op on current `DOMAIN_PRIOR`. | Skip this slot. |
| P2 | MS2Query / Spec2Vec / MS2Deepscore | Strong analog ranking in literature; public analog notebooks sit at 0.43–0.46. | Heavy offline weights; 9h kernel budget; internet off. |
| P3 | Formula → candidate DB / de novo | Needed for Class-3 when the structure is absent or labels are poisoned. | Out of scope. Retrieval cannot solve Class-3. |

## Why this slot is MIN_SIMILARITY, not another slot-rotation knob

Actions already burned UTC slots 1–2 today:

- **H-top-peaks** (`TOP_PEAKS=128`, already live; Kaggle **57756058**, kernel v167 at ~02:33Z)
- **H-peak-mz** (`PEAK_MZ_TOL=0.02`, already live; Kaggle **57767052**, kernel v168 at ~09:53Z)

Slot 3’s fallback is a **second copy of H-peak-mz** — also already live. Replaying it would waste UTC ticket 3. The first unused constant that actually changes which library hits enter the rank list is `MIN_SIMILARITY`.

Earlier Cloud PRs #38/#39/#40/#41 already specified this ablation and stayed draft/unmerged; Actions later spent those days’ next unused slot on the fallback no-op. This cycle re-implements on current main (after Actions cycle02) and retargets the Actions **slot-3** fallback so a 429/no-key hourly run cannot replay 0.02 Da.

## Out of scope this cycle

- CSV `competitions submit` (notebook-only competition).
- Claiming Class-3 de novo is solved by library retrieval.
- Training MS2Deepscore / Spec2Vec inside the kernel.
- Jumping `MIN_SIMILARITY` to GNPS 0.5 / Li–Fiehn 0.75 (too aggressive for MRR@25 coverage).
- Merging prior Cloud H-min-sim PRs #38/#39/#40/#41 or H-peaks PR #42 (those stay historical; this cycle re-implements on current main).
