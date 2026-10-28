# Research — 2026-10-28 cycle02

## Goal

Raise public MRR@25 above the v0.1 plateau (**0.143**) toward the live public frontier (~**0.50–0.51** on CLIST). This Cloud slot (01:00 CDT / 06:00 UTC, Chicago day open) is the first unused **real** ablation after Actions already spent UTC ticket 1 on a `TOP_PEAKS=128` replay. Target: **library-hit admission floor** (`MIN_SIMILARITY` 0.05 → 0.12), not another replay of already-live pairing / peak-ladder knobs.

## Sources reviewed

1. **Li, Kind, Folz, Vaniya, Mehta, Fiehn — *Nat. Methods* (2021)**  
   [Spectral entropy outperforms MS/MS dot product](https://www.nature.com/articles/s41592-021-01331-z)  
   Entropy similarity beat 42 alternatives on NIST20. On 37,299 experimental natural-product spectra, **entropy similarity ≥ 0.75** yielded **FDR < 10%**. The paper also states that **similarity scores > 0.75** should be used in untargeted MS/MS searches to keep FDRs acceptable, and that results should be ranked by score gaps rather than trusting a lone top hit. Our mix weight is already live (`ENTROPY_WEIGHT=0.75`). The remaining mismatch is the **admission floor**: we currently keep every hybrid score ≥ **0.05**, which is far below any published FDR-aware cutoff and fills `top_k` with decoys.

2. **Li & Fiehn — *Nat. Methods* (2023)**  
   [Flash Entropy Search](https://doi.org/10.1038/s41592-023-02012-9) · [ms_entropy API](https://msentropy.readthedocs.io/en/latest/entropy_search_api.html)  
   After the 1% noise cut and precursor-ion removal, Flash Entropy matches fragments inside a **±20 mDa** window (`ms2_tolerance_in_da=0.02`, `noise_threshold=0.01`). That pairing window and intensity floor are already live (`PEAK_MZ_TOL=0.02`, `INTENSITY_FLOOR=0.01`). Flash Entropy is a search accelerator, not an admission-threshold paper — it does not justify keeping 0.05 hits.

3. **matchms modified cosine**  
   [`ModifiedCosineGreedy(tolerance=0.1)`](https://matchms.readthedocs.io/en/latest/api/matchms.similarity.ModifiedCosineGreedy.html)  
   Default **0.1 Da** is a peak-pairing window, not a score floor. Ranking still depends on a caller-supplied score cutoff. Our hybrid uses the tighter Flash Entropy 0.02 Da pairing already live; the unused knob is who is allowed into `top_k`.

4. **de Jonge et al. — *Nat. Commun.* (2023)**  
   [MS2Query: reliable analogue search](https://www.nature.com/articles/s41467-023-37446-4) · [GNPS2 interpretation notes](https://wang-bioinformatics-lab.github.io/GNPS2_Documentation/ms2query_doc/)  
   Library/analogue tools apply a **minimum score** before emitting a hit. MS2Query’s own model score is treated as unreliable below ~0.6 and generally reliable above ~0.7. Modified-cosine analogue search in the same paper also sweeps a 0–1 threshold rather than admitting near-zero scores. Our 0.05 floor is an order of magnitude below those operating points.

5. **CASMI / Enveda competition notes**  
   [Kaggle competition](https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra) · [CLIST standings](https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/)  
   Metric is MRR@25. Retrieval-only cannot claim Class-3 de novo. Exact test↔train spectrum duplicates in `enveda-180` still poison rank-1 when train labels ≠ GT — exact-dup exclusion stays on. CLIST (~2026-10-28T01:00Z, rounded): **Savko 0.51**, **Parfionov 0.51**, pikachu/Shehab/CHU1PC **0.50**.

6. **Public analog notebooks (community)**  
   Analog-propagation notebooks report public MRR@25 ~0.43–0.46 (e.g. Analog Propagation V43 at 0.456; copied-notebook pile ~0.464). They typically use ~0.02 Da fragment matching and do **not** admit near-zero library hits into a 25-slot list.

## Methods to consider

| Priority | Method | Why it can lift MRR@25 | How (notebook, internet off) |
|----------|--------|------------------------|------------------------------|
| **P0** | **Higher `MIN_SIMILARITY` (0.05 → 0.12)** | Li/Fiehn FDR work implies very low entropy/modcos scores are mostly decoys. Live `retrieve.py` keeps every `hybrid_similarity >= cfg.min_similarity` in `top_k`. At 0.05 the top-25 is packed with junk that crowds out mid-score true structures. Raising the floor to 0.12 is a conservative step toward published cutoffs without jumping to 0.75 (which would empty many sparse queries). | One config constant. Already wired in `casmi26/retrieve.py`. |
| P1 | `TOP_PEAKS` 128 → 160 | Longer ladder after the 1% floor. Risk: more noise ions. | Slot-3 fallback after this cycle. Do not stack on H-min-sim. |
| P1 | Tighter `ENTROPY_WEIGHT` / mass window | Mix 0.75 and mass-wide 35/80 already live. Replaying them is a no-op. | Skip. |
| P2 | CE-aware aggregation / domain prior | Already live; H-domain fallback is a no-op on current `DOMAIN_PRIOR`. | Skip this slot. |
| P2 | MS2Query / Spec2Vec / MS2Deepscore | Strong analog ranking in literature; public analog notebooks sit at 0.43–0.46. | Heavy offline weights; 9h kernel budget; internet off. |
| P3 | Formula → candidate DB / de novo | Needed for Class-3 when the structure is absent or labels are poisoned. | Out of scope. Retrieval cannot solve Class-3. |

## Why this slot is the admission floor, not another slot-rotation knob

Actions already burned UTC slot 1 today (UTC calendar, Kaggle reset):

- **H-top-peaks** (`TOP_PEAKS=128`, already live after yesterday’s cycle04 `TOP_PEAKS=160` then cycle01 restore; Kaggle **57724850**, kernel v163 at ~05:02Z)

Live main after that submit: `TOP_PEAKS=128`, `PEAK_MZ_TOL=0.02`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, mass-wide 35/80, **`MIN_SIMILARITY=0.05`**.

Slot 2’s fallback on main is still **H-peak-mz** (`PEAK_MZ_TOL=0.02`) — already live. Replaying it would waste UTC ticket 2. The first unused constant that actually changes who enters the rank list is `MIN_SIMILARITY`.

Cloud PRs #38 (2026-10-26) and **#39 (2026-10-27)** already specified this ablation and stayed unmerged; Actions later spent those days’ remaining tickets on H-peak-mz / H-peaks. This cycle re-implements on current main and retargets the Actions slot-2 and slot-3 fallbacks so a 429/no-key hourly run cannot replay 0.02 / 0.02.

## Out of scope this cycle

- CSV `competitions submit` (notebook-only competition).
- Claiming Class-3 de novo is solved by library retrieval.
- Training MS2Deepscore / Spec2Vec inside the kernel.
- Jumping `MIN_SIMILARITY` to 0.75 in one step (too many empty lists on sparse queries).
- Merging prior Cloud H-min-sim PRs #38/#39 (historical; this cycle re-implements on current main).
