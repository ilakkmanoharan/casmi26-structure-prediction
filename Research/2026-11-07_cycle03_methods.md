# Research — 2026-11-07 cycle03

## Goal

Raise public MRR@25 above the v0.1 plateau (**0.143**) toward the live public frontier (~**0.54** on CLIST). This Chicago-day Cloud slot (04:31 CST / 10:31 UTC) is the first unused **real** ablation after Actions already spent UTC tickets 1–2 on no-ops (`TOP_PEAKS=128`, `PEAK_MZ_TOL=0.02`, both already live). Target: **peak-ladder length after the 1% noise cut**, not another replay of already-live retrieval knobs.

## Sources reviewed

1. **Li, Kind, Folz, Vaniya, Mehta, Fiehn — *Nat. Methods* (2021)**  
   [Spectral entropy outperforms MS/MS dot product](https://www.nature.com/articles/s41592-021-01331-z)  
   Entropy similarity beat 42 alternatives on NIST20. On 37,299 experimental natural-product spectra, **entropy similarity ≥ 0.75** yielded **FDR < 10%**. Scores stayed robust after adding noise ions — extra fragment peaks after a 1% relative floor are not the failure mode that cosine matching suffers from. Mix weight `ENTROPY_WEIGHT=0.75` is already live.

2. **Li & Fiehn — *Nat. Methods* (2023)**  
   [Flash Entropy Search](https://www.nature.com/articles/s41592-023-02012-9) · [PDF](https://yuanyue.li/project/flash_entropy_search/Yuanyue-flash_entropy_search.pdf) · [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11511675/)  
   After precursor-ion removal (`m/z > precursor − 1.6`) and the **1% of max fragment intensity** noise cut, Flash Entropy matches remaining ions inside **±20 mDa**. It does **not** then clip to a 128-peak ladder. Low-abundance ions can err by ~10 mDa, which is why the pair window is 20 mDa (already live as `PEAK_MZ_TOL=0.02`).

3. **ms_entropy API**  
   [`clean_spectrum_for_search(..., noise_threshold=0.01, max_peak_num=0)`](https://msentropy.readthedocs.io/en/latest/_modules/ms_entropy/entropy_search/flash_entropy_search.html) · [basic usage](https://msentropy.readthedocs.io/en/latest/entropy_search_basic_usage.html)  
   Default **`max_peak_num=0` / `None` means no peak-count cap**. `noise_threshold=0.01` matches our live `INTENSITY_FLOOR`. Optional `max_num_peaks` is only for speed, not accuracy. Our live `TOP_PEAKS=128` is an extra clip that the reference implementation does not apply.

4. **matchms `FlashSimilarity` / `EntropySearch`**  
   [FlashSimilarity](https://matchms.readthedocs.io/en/latest/_modules/matchms/similarity/FlashSimilarity.html) · [EntropySearch](https://matchms.readthedocs.io/en/development/_modules/matchms/similarity/entropy_search.html)  
   Default `noise_cutoff=0.01`, fragment `tolerance` 0.01–0.02 Da. No 128-peak cap. Entropy weighting already down-weights intense ions, so keeping the full post-noise ladder helps identity search on rich NP spectra (GNPS / Enveda / RIKEN often >128 centroided peaks after a 1% floor).

5. **CASMI / Enveda competition notes**  
   [Kaggle competition](https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra) · [CLIST standings](https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/) · [Pilkwang overview](https://pilkwangkim.github.io/posts/CASMI-2026-From-Mass-Spectra-to-Molecular-Structures/)  
   Metric is MRR@25. Retrieval-only cannot claim Class-3 de novo. Exact test↔train spectrum duplicates in `enveda-180` still poison rank-1 when train labels ≠ GT — exact-dup exclusion stays on.

6. **Public analog / formula-pool notebooks (community)**  
   Analog-propagation / COCONUT-pool notebooks sit at public MRR@25 ~0.43–0.48 (e.g. Analog Propagation V43 at 0.456; ensemble notebooks ~0.480). They keep the post-noise ladder rather than a 128-peak clip. Leaderboard top is **not** a 128-peak entropy library search.

## Methods to consider

| Priority | Method | Why it can lift MRR@25 | How (notebook, internet off) |
|----------|--------|------------------------|------------------------------|
| **P0** | **`TOP_PEAKS` 128 → 256** | Live 128-peak clip is stricter than Flash Entropy / ms_entropy (`max_peak_num=0`). After the 1% floor, NP MS/MS routinely keep 130–200 centroided ions. Entropy similarity is robust to extra noise (Li 2021); clipping diagnostic mid-intensity ions hurts identity search across GNPS/MassBank/MONA vs Enveda CE. 256 is a bounded stand-in for “no cap” that still fits the ~20 min kernel. | One config constant. Already wired through `clean_spectrum(..., top_peaks=cfg.top_peaks)` in `casmi26/index.py` and `retrieve.py`. |
| P1 | `MIN_SIMILARITY` 0.05 → 0.12 | Li/Fiehn FDR work implies very low hybrid scores are mostly decoys. Raising the floor may stop packing the top-25 with noise. | Config only. Unmerged Cloud drafts #76–#82 already specify this; **not this slot** (keep one major factor). Slot-4 fallback retargeted here so the next hourly ticket is not `TOP_PEAKS=160` (a regression once 256 is live). |
| P1 | `MASS_TOL_PPM` 35 → 15 | Tighter HRMS precursor gate (timsTOF-class). Draft #83. | Next unused slot after H-sim-gate. |
| P1 | `ENTROPY_WEIGHT` 0.75 → 1.0 | Pure Li/Fiehn entropy after 20 mDa pairing is live. Draft #84. | Distinct; not this slot. |
| P2 | `TOP_K_SPECTRA_PER_QUERY` 120 → 240 | More CE/adduct library hits before aggregation. | Later slot. |
| P2 | MS2Query / Spec2Vec / MS2Deepscore | Strong analog ranking; public analog notebooks 0.43–0.48. | Heavy offline weights; 9h kernel budget; internet off. |
| P3 | Formula → candidate DB / de novo | Needed for Class-3 when the structure is absent or labels are poisoned. | Out of scope. Retrieval cannot solve Class-3. |

## Why this slot is peak-ladder length, not another slot-rotation knob

Actions already burned UTC slots 1–2 today:

- **H-top-peaks** (`TOP_PEAKS=128`, already live; Kaggle **58076904**, kernel v202 at 02:53Z)
- **H-peak-mz** (`PEAK_MZ_TOL=0.02`, already live; Kaggle **58088101**, kernel v203 at 10:02Z)

Slot 3’s fallback is **another H-peak-mz** (`PEAK_MZ_TOL=0.02`) — also already live. Replaying it would waste UTC ticket 3. The first unused constant that actually changes the cleaned spectrum object is `TOP_PEAKS` (128 → 256). Flash Entropy’s default is *no* cap after the 1% floor; 256 is the bounded notebook equivalent.

Unmerged Cloud drafts today (#82 H-sim-gate, #83 H-mass-tight, #84 H-entropy-pure) target other knobs. This cycle stays distinct.

## Out of scope this cycle

- CSV `competitions submit` (notebook-only competition).
- Claiming Class-3 de novo is solved by library retrieval.
- Training MS2Deepscore / Spec2Vec inside the kernel.
- Merging drafts #82/#83/#84 (those stay historical; this cycle re-implements on current main).
