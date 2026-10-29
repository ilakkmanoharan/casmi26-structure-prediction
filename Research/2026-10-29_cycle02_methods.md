# Research — 2026-10-29 cycle02

## Goal

Raise public MRR@25 above the v0.1 plateau (**0.143**) toward the live public frontier (~**0.52** on CLIST). This Chicago-day Cloud slot (01:00 CDT / 06:00 UTC) is the first unused **real** ablation after Actions already spent UTC ticket 1 on a no-op. Target: **library-hit admission floor** (`MIN_SIMILARITY` 0.05 → 0.12), not another replay of already-live retrieval knobs.

## Sources reviewed

1. **Li, Kind, Folz, Vaniya, Mehta, Fiehn — *Nat. Methods* (2021)**  
   [Spectral entropy outperforms MS/MS dot product](https://www.nature.com/articles/s41592-021-01331-z)  
   Entropy similarity beat 42 alternatives on NIST20. On 37,299 experimental natural-product spectra, **entropy similarity ≥ 0.75** yielded **FDR < 10%**. The paper also notes that untargeted practice often uses **>0.7 or >0.8** similarity cutoffs, and that information-poor spectra (spectral entropy S < 1) still show FDR > 23% even at 0.9. Our live mix weight already matches the 0.75 FDR operating point (`ENTROPY_WEIGHT=0.75`). The admission floor that actually gates `top_k` is still **0.05** — far below any literature ID threshold — so junk hybrid scores fill the rank list.

2. **Li & Fiehn — *Nat. Methods* (2023) / PMC11511675**  
   [Flash Entropy Search](https://pmc.ncbi.nlm.nih.gov/articles/PMC11511675/)  
   After the 1% noise cut and precursor-ion removal, Flash Entropy matches fragment ions inside a **±20 mDa** window. That window is already live (`PEAK_MZ_TOL=0.02`). Remaining mismatch vs the papers is the **score floor**, not the pair window or the mix weight.

3. **ms_entropy / matchms defaults**  
   [`FlashEntropySearch.search(..., ms2_tolerance_in_da=0.02)`](https://msentropy.readthedocs.io/en/latest/entropy_search_api.html) · [matchms.similarity.FlashSimilarity](https://matchms.readthedocs.io/en/stable/api/matchms.similarity.FlashSimilarity.html)  
   Default **0.02 Da** pair window and `noise_cutoff=0.01` are already live. Neither library recommends admitting hits at 0.05 similarity.

4. **CASMI / Enveda competition notes**  
   [Kaggle competition](https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra) · [CLIST standings](https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/) · [Pilkwang overview](https://pilkwangkim.github.io/posts/CASMI-2026-From-Mass-Spectra-to-Molecular-Structures/)  
   Metric is MRR@25. Retrieval-only cannot claim Class-3 de novo. Exact test↔train spectrum duplicates in `enveda-180` still poison rank-1 when train labels ≠ GT — exact-dup exclusion stays on.

5. **Public analog notebooks (community, ~2026-10-21)**  
   Analog-propagation notebooks report public MRR@25 ~0.43–0.46 (e.g. Analog Propagation V43 at 0.456; Gluzdov V16 0.464). They typically keep a higher analog/library floor than 0.05 so decoys do not occupy the top-25.

## Methods to consider

| Priority | Method | Why it can lift MRR@25 | How (notebook, internet off) |
|----------|--------|------------------------|------------------------------|
| **P0** | **Raise `MIN_SIMILARITY` 0.05 → 0.12** | Live 0.05 admits near-random hybrid scores into `top_k` (`casmi26/retrieve.py` keeps a hit iff `sim >= cfg.min_similarity`). Li/Fiehn FDR work implies scores in the 0.05–0.12 band are almost all decoys. Raising the floor stops packing the top-25 with noise without jumping to the 0.75 identification cutoff (that would empty sparse queries). | One config constant. Already wired. |
| P1 | `TOP_PEAKS` 128 → 160 | Longer ladder after the 1% floor. Risk: more noise ions if the floor is already doing its job. | Slot-3/4 fallback this cycle (`TOP_PEAKS=160` only — do **not** reset `MIN_SIMILARITY`). |
| P2 | CE-aware aggregation / domain prior | Already live; H-domain fallback is a no-op on current `DOMAIN_PRIOR`. | Skip this slot. |
| P2 | MS2Query / Spec2Vec / MS2Deepscore | Strong analog ranking in literature; public analog notebooks sit at 0.43–0.46. | Heavy offline weights; 9h kernel budget; internet off. |
| P3 | Formula → candidate DB / de novo | Needed for Class-3 when the structure is absent or labels are poisoned. | Out of scope. Retrieval cannot solve Class-3. |

## Why this slot is the admission floor, not another slot-rotation knob

Actions already burned UTC slot 1 today:

- **H-top-peaks** (`TOP_PEAKS=128`, already live; Kaggle **57756058**, kernel v167 at ~02:33Z)

Yesterday’s remaining tickets were also no-ops vs current main: H-peak-mz (`PEAK_MZ_TOL=0.02`, already live) and H-peaks (`TOP_PEAKS=160` then reset to 128 by today’s cycle01). Slot 2’s fallback is still **H-peak-mz** — also already live. Replaying it would waste UTC ticket 2. The first unused constant that actually changes which library hits enter the rank list is `MIN_SIMILARITY`.

Cloud PRs #38/#39/#40 already specified this ablation and stayed draft/unmerged; Actions later spent those days’ next unused slot on the fallback no-op. This cycle re-implements on current main and retargets the Actions slot-2 fallback to H-min-sim, and slot-3/4 to H-peaks (`TOP_PEAKS=160` only) so a 429/no-key hourly run cannot replay 0.02 / reset the floor to 0.05.

## Out of scope this cycle

- CSV `competitions submit` (notebook-only competition).
- Claiming Class-3 de novo is solved by library retrieval.
- Training MS2Deepscore / Spec2Vec inside the kernel.
- Jumping `MIN_SIMILARITY` all the way to 0.75 (Li/Fiehn ID cutoff) — too aggressive for MRR@25 recall on sparse queries.
- Merging prior Cloud H-min-sim PRs #38/#39/#40 (those stay historical; this cycle re-implements on current main).
