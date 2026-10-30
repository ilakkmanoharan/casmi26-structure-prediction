# Research — 2026-10-30 cycle02

## Goal

Raise public MRR@25 above the v0.1 plateau (**0.143**) toward the live public frontier (~**0.50–0.52** on CLIST). This Cloud slot is **02:30 America/Chicago / 07:32 UTC** — the first unused **real** ablation after Actions already spent UTC ticket 1 on a no-op (`TOP_PEAKS=128`, already live after yesterday’s cycle04 briefly set 160 then cycle01 restored 128). Target: **library-hit admission floor** (`MIN_SIMILARITY` 0.05 → 0.12), not another replay of already-live retrieval knobs.

## Sources reviewed

1. **Li, Kind, Folz, Vaniya, Mehta, Fiehn — *Nat. Methods* (2021)**  
   [Spectral entropy outperforms MS/MS dot product](https://www.nature.com/articles/s41592-021-01331-z)  
   Entropy similarity beat 42 alternatives on NIST20. On 37,299 experimental natural-product spectra, **entropy similarity ≥ 0.75** yielded **FDR < 10%**. That mix weight is already live (`ENTROPY_WEIGHT=0.75`). The remaining mismatch vs literature is the **admission floor**: we still keep hybrid hits at 0.05, an order of magnitude below the 0.75 *call* threshold.

2. **Li & Fiehn — Flash Entropy Search (2023)**  
   [PMC11511675](https://pmc.ncbi.nlm.nih.gov/articles/PMC11511675/)  
   After the 1% noise cut, Flash Entropy pairs fragments inside ±20 mDa. That window is already live (`PEAK_MZ_TOL=0.02`). Raising the score floor does not undo that pairing; it only drops near-noise *scores*.

3. **matchms `FlashSimilarity`**  
   [matchms.similarity.FlashSimilarity](https://matchms.readthedocs.io/en/stable/api/matchms.similarity.html)  
   Default `tolerance=0.02` Da, `noise_cutoff=0.01`. Cleanup already matches live `INTENSITY_FLOOR=0.01` and `PEAK_MZ_TOL=0.02`. matchms does **not** auto-admit 0.05 scores into a top-25; GNPS-style library search typically starts much higher.

4. **LibGen (2024) — high-quality NP libraries**  
   [PMC11492814](https://pmc.ncbi.nlm.nih.gov/articles/PMC11492814/)  
   Identity-search annotation used **entropy similarity 0.75** for unambiguous calls with minimized FDR. That is a *call* threshold, not an MRR@25 admission floor — jumping our kernel to 0.75 would empty too many CASMI rank lists. **0.12** is a conservative step toward that literature without claiming a 10% FDR cut.

5. **Comparative similarity measures (2025)**  
   [Chemometrics and Intelligent Laboratory Systems](https://doi.org/10.1016/j.chemolab.2025.105417)  
   Weighted cosine with intensity transform can match or beat Shannon entropy on accuracy; Tsallis entropy is more expensive. We already mix entropy 0.75 / modified cosine 0.25. The bottleneck for MRR@25 is **which hits enter the rank list**, not a new kernel.

6. **CASMI / Enveda competition notes**  
   [Kaggle competition](https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra) · [CLIST standings](https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/) · [community analog pipeline](https://github.com/shiferaxa/casmi26)  
   Metric is MRR@25. Retrieval-only cannot claim Class-3 de novo. Exact test↔train spectrum duplicates in `enveda-180` still poison rank-1 when train labels ≠ GT — exact-dup exclusion stays on. Public analog notebooks sit ~0.43–0.46; copied-notebook pile ~0.464; live CLIST top **Parfionov 0.52**.

## Methods to consider

| Priority | Method | Why it can lift MRR@25 | How (notebook, internet off) |
|----------|--------|------------------------|------------------------------|
| **P0** | **Raise `MIN_SIMILARITY` 0.05 → 0.12** | Live 0.05 admits near-noise hybrid scores into `retrieve.py` (`if sim >= cfg.min_similarity` before `top_k` truncation). Li/Fiehn FDR work and GNPS-style 0.5–0.7 defaults both say those hits are decoys. Dropping them frees top-25 slots for higher-support structures. 0.12 is well below a 0.75 *call* threshold, so sparse-but-real hits still enter. | One config constant. Already wired. |
| P1 | `TOP_PEAKS` 128 → 160 | Longer ladder after the 1% floor. Risk: more noise ions if the floor is already doing its job. Yesterday cycle04 tried 160; today’s cycle01 restored 128. Slot-3/4 fallback after this PR (`TOP_PEAKS=160` only; do not reset `MIN_SIMILARITY`). | Next unused after H-min-sim. |
| P2 | CE-aware aggregation / domain prior | Already live; H-domain fallback is a no-op on current `DOMAIN_PRIOR`. | Skip this slot. |
| P2 | Analog / MS2Query / Spec2Vec / MS2Deepscore | Strong analog ranking in literature; public analog notebooks sit at 0.43–0.46. | Heavy offline weights; 9h kernel budget; internet off. |
| P3 | Formula → candidate DB / de novo | Needed for Class-3 when the structure is absent or labels are poisoned. | Out of scope. Retrieval cannot solve Class-3. |

## Why this slot is MIN_SIMILARITY, not another slot-rotation knob

Actions already burned UTC slot 1 today:

- **H-top-peaks** (`TOP_PEAKS=128`, already live; Kaggle **57789094**, kernel v171 at ~02:00Z)

Slot 2’s fallback is **H-peak-mz** (`PEAK_MZ_TOL=0.02`) — also already live since 10-24/10-25. Replaying it would waste UTC ticket 2. GitHub’s hourly `casmi-loop` last succeeded at **01:41Z**; next unused hourly is **08:00 UTC**. The first unused constant that actually changes which library hits enter the rank list is `MIN_SIMILARITY`.

Cloud PRs #38/#39/#40/#41/#43/#44 already specified this ablation and stayed unmerged; Actions later spent those days’ next unused slot on the fallback no-op. This cycle re-implements on current main (after cycle01) and retargets the Actions **slot-2** fallback so a 429/no-key hourly run cannot replay 0.02.

## Out of scope this cycle

- CSV `competitions submit` (notebook-only competition).
- Claiming Class-3 de novo is solved by library retrieval.
- Training MS2Deepscore / Spec2Vec inside the kernel.
- Jumping `MIN_SIMILARITY` to GNPS 0.5 / Li–Fiehn 0.75 (too aggressive for MRR@25 coverage).
- Merging prior Cloud H-min-sim PRs #38/#39/#40/#41/#43/#44 or H-peaks PR #42 (those stay historical; this cycle re-implements on current main).
