# Research — 2026-10-30 cycle03

## Goal

Raise public MRR@25 above the v0.1 plateau (**0.143**) toward the live public frontier (~**0.50–0.52** on CLIST). This Cloud slot is **05:30 America/Chicago / 10:34 UTC** — the first unused **real** ablation after Actions already spent UTC tickets 1–2 on no-ops (`TOP_PEAKS=128` already live; `PEAK_MZ_TOL=0.02` already live, then replayed as cycle02). Target: **library-hit admission floor** (`MIN_SIMILARITY` 0.05 → 0.12), not another replay of already-live retrieval knobs.

Prior Cloud cycle03 PR **#46** (09:05Z) specified this same ablation and stayed draft; GitHub’s 09:00 and 10:00 UTC `casmi-loop` hours did not fire, so UTC ticket 3 is still free. This run re-implements on current `main` so the next unused hourly (**11:00 UTC**) can submit it.

## Sources reviewed

1. **Li, Kind, Folz, Vaniya, Mehta, Fiehn — *Nat. Methods* (2021)**  
   [Spectral entropy outperforms MS/MS dot product](https://www.nature.com/articles/s41592-021-01331-z)  
   Entropy similarity beat 42 alternatives on NIST20. On 37,299 experimental natural-product spectra, **entropy similarity ≥ 0.75** yielded **FDR < 10%**. That mix weight is already live (`ENTROPY_WEIGHT=0.75`). The remaining mismatch vs a library *call* is the admission floor: live `MIN_SIMILARITY=0.05` is an order of magnitude below the 0.75 FDR threshold, so near-noise hybrid scores still enter the rank list.

2. **Li & Fiehn — Flash Entropy Search (PMC11511675)**  
   [Flash entropy search to query all mass spectral libraries in real time](https://pmc.ncbi.nlm.nih.gov/articles/PMC11511675/)  
   After the 1% noise cut, Flash Entropy pairs fragments in a **±20 mDa** window (low-abundance ions can err ~10 mDa). That window is already live (`PEAK_MZ_TOL=0.02`, Actions cycle02 kernel v172). The paper does **not** recommend keeping every match down to 0.05 similarity.

3. **LibGen (Xing, Fiehn et al., 2024 / PMC11492814)**  
   [LibGen: Generating High Quality Spectral Libraries of Natural Products](https://pmc.ncbi.nlm.nih.gov/articles/PMC11492814/)  
   Curated NP libraries drop sparse spectra at entropy **S < 0.5** and treat entropy similarity **> 0.75** as the isomer/identity bar. Confirms that scores in the 0.05–0.12 band are not identity-grade evidence for MRR@25.

4. **Scheubert et al. — *Nat. Commun.* (2017)**  
   [Significance estimation for large scale metabolomics annotations by spectral matching](https://www.nature.com/articles/s41467-017-01318-5)  
   Cosine cutoffs that hold ~1% FDR typically sit **0.50–0.60** when ≥8 ions match (higher still with fewer ions). GNPS library search defaults to cosine **0.5** and **6** matched peaks ([GNPS library search](https://ccms-ucsd.github.io/GNPSDocumentation/librarysearch/)). Live 0.05 is far below every validated identity cutoff; **0.12** is a conservative first step, still well below 0.5 / 0.75.

5. **matchms / GNPS-style identity search**  
   [matchms.similarity.FlashSimilarity](https://matchms.readthedocs.io/en/stable/api/matchms.similarity.FlashSimilarity.html) (default `tolerance=0.02` Da, already live). A conservative step to **0.12** stays below a 0.75 *call*, so sparse-but-real Class-1 hits can remain.

6. **CASMI / Enveda competition notes**  
   [Kaggle competition](https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra) · [CLIST standings](https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/)  
   Metric is public MRR@25. Retrieval-only cannot claim Class-3 de novo. Exact test↔train spectrum duplicates in `enveda-180` still poison rank-1 when train labels ≠ GT — exact-dup exclusion stays on.

7. **Public analog notebooks (community)**  
   Analog-propagation notebooks still sit ~0.43–0.46; copied-notebook pile ~0.464. Public notebooks that score 0.47+ typically filter weak analog hits rather than packing top-25 with 0.05-floor decoys.

## Methods to consider

| Priority | Method | Why it can lift MRR@25 | How (notebook, internet off) |
|----------|--------|------------------------|------------------------------|
| **P0** | **Raise `MIN_SIMILARITY` 0.05 → 0.12** | Live 0.05 admits near-noise hybrid scores into `retrieve.py` (`if sim >= cfg.min_similarity` before `top_k` truncation). Li/Fiehn FDR work, Scheubert 1% FDR cosine bands, and GNPS 0.5 defaults all say those hits are decoys. Dropping them frees top-25 slots for higher-support structures. 0.12 is well below a 0.75 *call* threshold, so sparse-but-real hits still enter. | One config constant. Already wired. |
| P1 | `TOP_PEAKS` 128 → 160 | Longer ladder after the 1% floor. Risk: more noise ions if the floor is already doing its job. Yesterday cycle04 tried 160; today’s cycle01 restored 128. Slot-4 fallback after this PR (`TOP_PEAKS=160` only; do not reset `MIN_SIMILARITY`). | Next unused after H-min-sim. |
| P2 | CE-aware aggregation / domain prior | Already live; H-domain fallback is a no-op on current `DOMAIN_PRIOR`. | Skip this slot. |
| P2 | MS2Query / Spec2Vec / MS2Deepscore | Strong analog ranking in literature; public analog notebooks sit at 0.43–0.46. | Heavy offline weights; 9h kernel budget; internet off. |
| P3 | Formula → candidate DB / de novo | Needed for Class-3 when the structure is absent or labels are poisoned. | Out of scope. Retrieval cannot solve Class-3. |

## Why this slot is MIN_SIMILARITY, not another slot-rotation knob

Actions already burned UTC slots 1–2 today:

- **H-top-peaks** (`TOP_PEAKS=128`, already live; Kaggle **57789094**, kernel v171 at ~02:00Z)
- **H-peak-mz** (`PEAK_MZ_TOL=0.02`, already live since 10-24/10-25; Kaggle **57799491**, kernel v172 at ~08:36Z)

Slot 3’s fallback is **still H-peak-mz** (`PEAK_MZ_TOL=0.02`) — the same no-op just submitted. Replaying it would waste UTC ticket 3. GitHub’s hourly `casmi-loop` last succeeded at **08:17Z**; 09:00 and 10:00 UTC hours did not fire. Next unused hourly is **11:00 UTC**. The first unused constant that actually changes which library hits enter the rank list is `MIN_SIMILARITY`.

Cloud PRs **#45** (cycle02 H-min-sim) and **#46** (cycle03 H-min-sim, 09:05Z) plus prior H-min-sim PRs #38–#44 stayed draft/unmerged. This cycle re-implements on current main (after cycle02) and retargets the Actions slot-2/slot-3 fallbacks so a 429/no-key hourly run cannot replay 0.02.

## Out of scope this cycle

- CSV `competitions submit` (notebook-only competition).
- Claiming Class-3 de novo is solved by library retrieval.
- Training MS2Deepscore / Spec2Vec inside the kernel.
- Jumping `MIN_SIMILARITY` to GNPS 0.5 / Li–Fiehn 0.75 (too aggressive for MRR@25 coverage).
- Merging prior Cloud H-min-sim PRs #38–#46 or H-peaks PR #42 (those stay historical; this cycle re-implements on current main).
