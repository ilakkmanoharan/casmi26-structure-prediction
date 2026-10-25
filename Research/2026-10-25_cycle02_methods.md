# Research — 2026-10-25 cycle02

## Goal

Raise public MRR@25 above the v0.1 plateau (**0.143**) toward the live public frontier (~**0.50** on CLIST). This Chicago-day Cloud slot (01:00 CDT / 06:00 UTC) is the first unused **real** ablation after Actions already spent UTC ticket 1 on a live-constant replay. Target: **longer fragment ladder after the 1% floor**, not another replay of already-live `PEAK_MZ_TOL` / `ENTROPY_WEIGHT`.

## Sources reviewed

1. **Li, Kind, Folz, Vaniya, Mehta, Fiehn — *Nat. Methods* (2021)**  
   [Spectral entropy outperforms MS/MS dot product](https://www.nature.com/articles/s41592-021-01331-z) · [PMC11492813](https://pmc.ncbi.nlm.nih.gov/articles/PMC11492813/)  
   Entropy similarity beat 42 alternatives on NIST20. On 37,299 experimental natural-product spectra, **entropy similarity ≥ 0.75** yielded **FDR < 10%**. That mix weight is already live (`ENTROPY_WEIGHT=0.75`). The remaining retrieval-knob mismatch is how many cleaned ions enter the entropy/modcos objects.

2. **Li & Fiehn — Flash Entropy Search (2023)**  
   [PMC11511675](https://pmc.ncbi.nlm.nih.gov/articles/PMC11511675/) · [preprint](https://doi.org/10.21203/rs.3.rs-2693233/v1)  
   After the 1% noise cut and precursor-ion removal, Flash Entropy matches fragments inside a **±20 mDa** window and does **not** collapse the spectrum to a short top-N list. Low-abundance ions can err by ~10 mDa; the paper therefore chooses a generous 20 mDa window. Our live `PEAK_MZ_TOL=0.02` now matches that window (merged via 10-24 Cloud H-peak-mz). The next unused literature lever is **keeping more ions after the 1% cut**.

3. **ms_entropy / DynamicEntropySearch API**  
   [`search_topn_matches`](https://msentropy.readthedocs.io/en/latest/dynamic_basic_usage_search.html) · [`FlashEntropySearch.search`](https://msentropy.readthedocs.io/en/latest/entropy_search_api.html)  
   Defaults: `ms2_tolerance_in_da=0.02`, `noise_threshold=0.01`, **`max_peak_num=None`** (keep every ion that survives cleaning). Our live `TOP_PEAKS=128` still truncates that cleaned ladder. Raising 128 → 160 is a conservative step toward the unrestricted default without blowing the internet-off kernel budget.

4. **ms_entropy `get_topn_matches`**  
   [flash_entropy_search source](https://msentropy.readthedocs.io/en/latest/_modules/ms_entropy/entropy_search/flash_entropy_search.html)  
   Default retrieval floor is `min_similarity=0.01`. Our live `MIN_SIMILARITY=0.05` is already stricter. Raising it further this slot would confound the peak-count ablation and could drop true-structure near-matches that the newly widened 20 mDa window just recovered.

5. **Moreta-Casademunt, Huber, et al. — *J. Am. Soc. Mass Spectrom.* (2024)**  
   [Weighting low-intensity MS/MS ions](https://pubs.acs.org/doi/10.1021/jasms.3c00359)  
   Low-intensity and high-*m/z* ions carry structural information that unweighted cosine/entropy under-use. Truncating the cleaned ladder at 128 discards exactly those mid/low ions after the 1% floor. A 160-peak cap keeps more of them once `PEAK_MZ_TOL=0.02` can actually pair them.

6. **MS2Query (de Jonge et al., bioRxiv / *Nat. Commun.* line)**  
   [bioRxiv 10.1101/2022.07.22.501125](https://www.biorxiv.org/content/10.1101/2022.07.22.501125v1.full-text)  
   Analog search (MS2Deepscore + Spec2Vec + modified cosine) is how public notebooks sit at ~0.43–0.46. Heavy offline weights; out of scope for a one-constant internet-off kernel slot.

7. **CASMI / Enveda competition notes**  
   [Kaggle competition](https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra) · [CLIST standings](https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/) · [shiferaxa/casmi26 pipeline notes](https://github.com/shiferaxa/casmi26)  
   Metric is MRR@25. Public top ~**0.50** (Oleksandr Parfionov / pikachu / Savko / CHU1PC). Retrieval-only cannot claim Class-3 de novo. Exact test↔train spectrum duplicates in `enveda-180` still poison rank-1 when train labels ≠ GT — exact-dup exclusion stays on.

## Methods to consider

| Priority | Method | Why it can lift MRR@25 | How (notebook, internet off) |
|----------|--------|------------------------|------------------------------|
| **P0** | **`TOP_PEAKS` 128 → 160** | Flash Entropy / ms_entropy keep **all** ions after the 1% cut (`max_peak_num=None`). Live 128 still drops mid-intensity diagnostic fragments. After `PEAK_MZ_TOL=0.02` those extra ions can pair; the 2024 JASMS weighting paper says they carry structure. Slot-4 fallback already names this pair (`160` + `MIN_SIMILARITY=0.05`). | One config constant. Wired through `clean_spectrum(..., top_peaks=cfg.top_peaks)` in index + retrieve. |
| P1 | Higher `MIN_SIMILARITY` (0.05 → 0.12) | Li/Fiehn FDR work implies very low hybrid scores are mostly decoys. Raising the floor may stop packing the top-25 with noise. | Config only. Next unused slot after H-peaks (retarget slot-3 fallback). |
| P2 | Still-wider peak cap (200 / None) | Closer to ms_entropy default. Risk: kernel time + noise ions if the 1% floor is imperfect. | Later slot. Measure 160 first. |
| P2 | CE-aware aggregation / domain prior | Already live; H-domain fallback is a no-op on current `DOMAIN_PRIOR`. | Skip this slot. |
| P2 | MS2Query / Spec2Vec / MS2Deepscore | Strong analog ranking; public analog notebooks ~0.43–0.46. | Heavy offline weights; 9h kernel budget; internet off. |
| P3 | Formula → candidate DB / de novo | Needed for Class-3 when the structure is absent or labels are poisoned. | Out of scope. Retrieval cannot solve Class-3. |

## Why this slot is peak count, not another slot-rotation knob

Actions already burned UTC slot 1 today:

- **H-top-peaks** (`TOP_PEAKS=128`, already live; Kaggle **57612600**, kernel v149 at ~01:16Z, Actions **40148909273**)

Slot 2’s fallback is still **H-peak-mz** (`PEAK_MZ_TOL=0.02`) — also already live on main after the 10-24 Cloud merge (`838a974`). Replaying it would waste UTC ticket 2. The first unused constant that actually changes the cleaned spectrum object is `TOP_PEAKS` 128 → 160.

`MIN_SIMILARITY` 0.12 is the next unused lever after this slot; do not stack it here.

## Out of scope this cycle

- CSV `competitions submit` (notebook-only competition).
- Claiming Class-3 de novo is solved by library retrieval.
- Training MS2Deepscore / Spec2Vec inside the kernel.
- Replaying `PEAK_MZ_TOL=0.02`, `ENTROPY_WEIGHT=0.75`, or `INTENSITY_FLOOR=0.01`.
