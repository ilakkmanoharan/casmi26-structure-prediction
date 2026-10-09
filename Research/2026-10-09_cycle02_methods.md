# Research 2026-10-09_cycle02 — MS/MS methods that can raise MRR@25

Competition: `enveda-CASMI26-molecule-id-mass-spectra`  
Metric: public **MRR@25**  
Constraint: notebook-only, **internet off**, one major ablation this slot.  
Chicago day start: 01:00 America/Chicago (this run 06:01 UTC = 01:01 CDT).

## Sources reviewed

1. Li, Kind, Folz, Vaniya, Mehta, van der Hooft, Fiehn. *Spectral entropy outperforms MS/MS dot product similarity for small-molecule compound identification.* Nature Methods 18, 1524–1531 (2021). https://www.nature.com/articles/s41592-021-01331-z  
   PDF: https://escholarship.org/content/qt0249w6hk/qt0249w6hk.pdf  
   Benchmark: remove ions **&lt;1% of base-peak intensity** before entropy / 42-algorithm comparison; FDR &lt; 10% at entropy similarity **0.75**.
2. MSEntropy `clean_spectrum` / `msentropy_similarity`. Default `noise_threshold=0.01` (drop intensity &lt; 0.01 × max), then top-N, then sum-normalize.  
   https://msentropy.readthedocs.io/en/latest/_modules/ms_entropy/spectra/tools.html  
   https://cran.r-project.org/web/packages/msentropy/refman/msentropy.html
3. Kong, Shen, Li, Bashar, Bird, Fiehn. *Denoising Search doubles the number of metabolite and exposome annotations in human plasma using an Orbitrap Astral mass spectrometer.* Nature Methods (2025). https://www.nature.com/articles/s41592-025-02646-x  
   PMC: https://pmc.ncbi.nlm.nih.gov/articles/PMC11302682/  
   Chemical + electronic noise can exceed true fragments by **&gt;150×**; denoising raised median entropy similarity and annotation count (Astral + Denoising Search ≈ 2.3–2.5× vs raw Exploris).
4. Intensity-cutoff caution (Anal. Chem. / PMC 2025): a **fixed 5%** base-peak cut can drop nearly half of structurally explainable ions; **1–2%** retains interpretable fragments. https://pmc.ncbi.nlm.nih.gov/articles/PMC12311886/
5. Flash Entropy Search default fragment tolerance **20 mDa**. Our live `PEAK_MZ_TOL` is still **0.01** (Cloud PR #22 H-peak-mz unmerged).
6. CLIST prize table (fetched 2026-10-09T06:05Z): https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/  
   **pikachu 0.48**, MarvinTMB 0.47, Oliver Ford / vukpetar / Yuuki Aikawa 0.46. Community analog / quad-channel notebooks still ~0.328–0.339 on the Code tab.
7. de Jonge et al. *MS2Query* (Nat Commun 2023). Analogue search without a tight precursor prefilter. https://www.nature.com/articles/s41467-023-37446-4  
   Out of scope for a one-constant internet-off kernel slot.

## Methods to consider

### 1. Raise `INTENSITY_FLOOR` 0.001 → 0.01 — **P0 this slot**

**Why.** `clean_spectrum()` max-normalizes, then keeps `inten >= intensity_floor`, *then* applies `TOP_PEAKS`. Live `INTENSITY_FLOOR=0.001` is a 0.1% relative cut — an order of magnitude below Li/Fiehn and MSEntropy’s **1%** default. After `TOP_PEAKS=128` landed on `main`, those extra 128 slots are filled with electronic / chemical noise ions that entropy similarity still treats as evidence (Li et al. noted low-abundant ions inflate S and hurt ID). Kong/Fiehn 2025 show the same failure mode at scale: noise ions collapse entropy similarity until they are removed.

**How it improves score.** Dropping sub-1% peaks before the top-N cut reduces false fragment matches on noisy GNPS / MoNA / MassBank library rows. Wrong inchikey14s lose support; true-structure neighbors that share a mid-intensity ladder (already kept by the 1% rule) keep theirs. This is the unused cleaner knob that the literature already assumes.

**Why not 5%.** The 2025 intensity-cutoff study shows a 5% floor deletes structurally explainable ions. 1% is the documented default; 0.01 is the existing constant’s literature value.

### 2. Flash 20 mDa (`PEAK_MZ_TOL` 0.01 → 0.02) — P1, not this slot

Cloud PR #22 (2026-10-08 cycle02) already specifies this and is still a draft. Do not confound H-intensity with a second matching-tolerance change.

### 3. Higher `MIN_SIMILARITY` (0.12) — P1 later

Li/Fiehn FDR argument. PRs #11/#12 unmerged. Raise the rank gate only after the peak list is cleaned.

### 4. Analogue / multi-channel ranking — P2 architecture

Public 0.33–0.48 scores come from analogue expansion + multi-evidence rankers, not from a 0.1% vs 1% floor. Out of scope. Do **not** claim Class-3 de novo is solved by retrieval.

### 5. Keep exact-dup ban — P0 already on

Exact test↔train copies in `enveda-180` carry train labels ≠ competition GT. `EXCLUDE_EXACT_DUPLICATES=True` stays.

## Priority table (notebook-only, internet off)

| Pri | Method | Fits this kernel? | This slot? |
|-----|--------|-------------------|------------|
| P0 | `INTENSITY_FLOOR` 0.001→0.01 | Yes, existing constant | **Yes — one major ablation** |
| P0 | Keep exact-dup ban | Already on | Keep |
| P1 | `PEAK_MZ_TOL` 0.02 | Yes; unmerged PR #22 | Next unused |
| P1 | `MIN_SIMILARITY` 0.12 | Yes; unmerged PRs #11/#12 | After cleaner peak list |
| P2 | Spec2Vec / MS2Deepscore / MS2Query | Weights + internet or huge cache | No |

## Out of scope this cycle

- CSV `competitions submit` (notebook-only competition).
- Claiming Class-3 de novo from library retrieval.
- Re-applying live `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, mass-wide 35/80 (Actions slot-2 H-entropy is a **no-op** on current `main`).
- Merging yesterday’s still-open draft PRs by hand; this cycle implements the next unused lever on a fresh tree.
