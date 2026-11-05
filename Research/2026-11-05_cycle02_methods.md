# Research — 2026-11-05 cycle02

## Goal

Raise public MRR@25 above the v0.1 plateau (**0.143**) toward the live public frontier (**~0.54**). This Cloud slot is the first unused **real** ablation after weeks of Actions fallbacks that only replay already-live knobs (`TOP_PEAKS` 128/160, `PEAK_MZ_TOL` 0.02). Target: **hybrid-score admission floor**, not another peak-count or fragment-window replay.

This run is the late `0 6 * * *` Cloud cron (triggered **2026-11-05T10:33Z**, Chicago **04:33 CST**). Chicago day **2026-11-05 is open** (day start 01:00 CST = 07:00 UTC). Actions UTC slot 1 already landed; 07:00 / 08:00 / 09:00 / 10:00 UTC `casmi-loop` hours did **not** fire. Next unused hourly is ~**11:00 UTC**.

## Sources reviewed

1. **Li, Kind, Folz, Vaniya, Mehta, Fiehn — *Nat. Methods* (2021)**  
   [Spectral entropy outperforms MS/MS dot product](https://www.nature.com/articles/s41592-021-01331-z)  
   Entropy similarity beat 42 alternatives on NIST20. On 37,299 experimental natural-product spectra, **entropy similarity ≥ 0.75** yielded **FDR < 10%**. The paper is explicit that ranks should consider several close scores rather than the top hit alone (fits MRR@25). Our mix weight is already `ENTROPY_WEIGHT=0.75`. The remaining mismatch is the **admission floor**: live `MIN_SIMILARITY=0.05` is 15× below that FDR cutoff, so decoys with almost no shared ions still enter the per-spectrum top-25.

2. **Li & Fiehn — *Nat. Methods* (2023)**  
   [Flash Entropy Search](https://doi.org/10.1038/s41592-023-02012-9) · [PMC11511675](https://pmc.ncbi.nlm.nih.gov/articles/PMC11511675/) · [ms_entropy API](https://msentropy.readthedocs.io/en/latest/entropy_search_basic_usage.html)  
   After the 1% noise cut and precursor-ion removal, Flash Entropy matches fragments inside **±20 mDa**. That window is already live (`PEAK_MZ_TOL=0.02`). Replaying it cannot change the similarity object. `max_num_peaks` / `noise_threshold` defaults are also already live (`TOP_PEAKS=128`, `INTENSITY_FLOOR=0.01`).

3. **Historical CASMI / MOLGEN-MS/MS (Meringer & Schymanski, *Metabolites* 2013)**  
   [PMC3901272](https://pmc.ncbi.nlm.nih.gov/articles/PMC3901272/)  
   High-res CASMI formula/structure search used **5 ppm MS** and **10 ppm MS/MS** when data were quoted as <5 ppm. Precursor-window tightening is a valid *next* unused slot (live `MASS_TOL_PPM=35` is wide); do not stack it on the score floor this cycle.

4. **Oberacher library search vs MetFrag (CASMI Category 2 recap)**  
   [PMC3901266](https://pmc.ncbi.nlm.nih.gov/articles/PMC3901266/)  
   Library search is strong when the compound is in the library and weak when it is not. Filling a 25-slot list with near-zero hybrid scores does not create true hits; it only dilutes rank of the few real ones. Retrieval still cannot claim Class-3 de novo.

5. **NIST 20 tandem search guidance**  
   [NIST tandem-library notes](https://www.chemdata.nist.gov/dokuwiki/lib/exe/fetch.php?media=peptidew%3Atandem-library.pdf)  
   Identity MS/MS already constrains by precursor. Product-ion pairing at ~0.01–0.02 Da is live. The missing control is “do not keep spectra that barely match.”

6. **Competition / standings**  
   [Kaggle](https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra) · [CLIST standings](https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/) (updated ~4 h before this 10:33Z run)  
   Public top: **Shehab Alshehabi 0.54**, Savko / Oleksandr Parfionov 0.52, democat 0.51, pikachu / Paweł Biernat / CHU1PC 0.50. Metric is MRR@25 (first correct InChIKey14 in the 25-list). Gap vs our 0.143 is not another `TOP_PEAKS` replay.

## Methods to consider

| Priority | Method | Why it can lift MRR@25 | How (notebook, internet off) |
|----------|--------|------------------------|------------------------------|
| **P0** | **Raise hybrid admission floor (`MIN_SIMILARITY` 0.05 → 0.12)** | Live 0.05 lets near-zero entropy/modcos hits occupy `TOP_CANDIDATES_PER_SPECTRUM=25` and then the molecule top-25. Li/Fiehn FDR work says scores in this band are mostly decoys. A 0.12 floor (still far below the 0.75 FDR cutoff) drops obvious noise without requiring the true structure to be a high-confidence identity hit. Aggregation (`best_similarity`, `mean_top_k`, support) then ranks remaining structures. Backfill at 80 ppm still fills short lists. | One config constant. Wired in `retrieve_for_spectrum` (`sim >= cfg.min_similarity`). |
| P1 | Tighter primary mass window (`MASS_TOL_PPM` 35 → 10) | Li/Fiehn used a 10 ppm precursor window; historical CASMI used 5 ppm. Live 35 ppm admits many isobars. Keep `MASS_TOL_PPM_BACKFILL=80` so lists still fill. | Next unused slot. Do not stack on H-min-sim. |
| P1 | `ENTROPY_WEIGHT` 0.75 → 1.0 (pure entropy) | Li 2021’s 0.75 is an FDR cutoff, not a blend weight. Cloud draft PR **#73** already specified this as an alternate cycle02. Smaller lever than the admission floor. | Later slot if H-min-sim lands. |
| P2 | Analog / MS2Query / Spec2Vec / MS2Deepscore | Community analog notebooks sit ~0.43–0.46; LB top is ~0.54. | Heavy offline weights; 9 h kernel; internet off. |
| P3 | Formula → candidate DB / de novo | Needed when the structure is absent or labels are poisoned. | Out of scope. Retrieval cannot solve Class-3. |

## Why this slot is the score floor, not another slot-rotation knob

Actions fallbacks for the last several UTC days have been:

1. **H-top-peaks** (`TOP_PEAKS=128`) — already a real ladder  
2. **H-peak-mz** (`PEAK_MZ_TOL=0.02`) — already the Flash Entropy / matchms default  
3. **H-peaks** (`TOP_PEAKS=160`, `MIN_SIMILARITY=0.05`) — *re-asserts the 0.05 floor*

Live main after 2026-11-05 cycle01 (kernel v195 / Kaggle **58012064**): `TOP_PEAKS=128`, `PEAK_MZ_TOL=0.02`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, mass-wide 35/80, `TOP_K=120`, **`MIN_SIMILARITY=0.05`**. Cycle01 only rolled the peak ladder 160→128. The first unused constant that actually changes *who enters the rank list* is `MIN_SIMILARITY`.

Cloud drafts **#62–#74** already specified this ablation and stayed unmerged; Actions then spent those hours on the fallback no-op (or did not fire). PR **#73** (07:39Z) specified H-entropy-pure instead. This 10:33Z cycle re-implements H-min-sim on current main and retargets Actions **slot-2 and slot-3** fallbacks to H-min-sim so a 429/no-key hourly run cannot replay `PEAK_MZ_TOL=0.02`.

## Out of scope this cycle

- CSV `competitions submit` (notebook-only competition).
- Claiming Class-3 de novo is solved by library retrieval.
- Training MS2Deepscore / Spec2Vec inside the kernel.
- Stacking `MASS_TOL_PPM` or `ENTROPY_WEIGHT` on the same ticket.
- Merging prior Cloud H-min-sim drafts #62–#74 (those stay historical; this cycle re-implements on current main).
