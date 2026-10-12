# Research 2026-10-12_cycle02 — fragment m/z matching tolerance

Competition: `enveda-CASMI26-molecule-id-mass-spectra`  
Metric: public **MRR@25**  
Constraint: notebook-only, **internet off**, one major ablation this slot.

## Sources reviewed

- Li, Kind, Folz, Vaniya, Mehta, Fiehn. *Spectral entropy outperforms MS/MS dot product similarity for small-molecule compound identification.* Nature Methods 18, 1524–1531 (2021). https://www.nature.com/articles/s41592-021-01331-z and PDF https://yuanyue.li/project/spectral_entropy/Yuanyue-spectral_entropy.pdf — NIST20/MassBank.us benchmark matched ions at **0.05 Da**; 1% base-peak noise cut; entropy 0.75 → FDR &lt; 10% on 37,299 NP spectra.
- MSEntropy / Flash Entropy docs: `calculate_entropy_similarity(..., ms2_tolerance_in_da=0.02)` and `EntropySearch.search(..., ms2_tolerance_in_da=0.02)`. Default fragment match is **0.02 Da**, not 0.01. https://msentropy.readthedocs.io/en/latest/classical_entropy_similarity.html and https://msentropy.readthedocs.io/en/latest/entropy_search_api.html
- YuanyueLi/MSEntropy examples use `ms2_tolerance_in_da = 0.05` (paper) and 0.02 (library search default). https://github.com/YuanyueLi/MSEntropy
- Li, Fiehn. *Flash entropy search to query all mass spectral libraries in real time.* Nature Methods 20, 1475–1478 (2023). https://doi.org/10.1038/s41592-023-02012-9
- de Jonge et al. *MS2Query: reliable and scalable MS2 mass spectra-based analogue search.* Nature Communications 14 (2023). https://www.nature.com/articles/s41467-023-37446-4
- Community pipelines (analog / ICEBERG+GLACIER + PubChem prior) public ~0.32–0.42. https://github.com/gnshx/Enveda-CASMI-2026---Molecule-ID-From-Mass-Spectra and https://github.com/shiferaxa/casmi26
- CLIST public standings (fetched 2026-10-12T06:05Z): MarvinTMB / pikachu / CHU1PC **0.48**. https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/
- Kaggle competition page. https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra/

## Methods to consider

### 1. Align fragment match window with MSEntropy default (`PEAK_MZ_TOL` 0.01→0.02) — **P0 this slot**

**Why.** `casmi26/spectrum.py` greedy-matches peaks for both entropy and modified cosine using `tol=cfg.peak_mz_tol`. Live `main` still uses **0.01 Da**. Flash Entropy / MSEntropy library search defaults to **0.02 Da**; the 2021 paper matched at **0.05 Da**. A 0.01 Da window is tighter than the algorithm our hybrid was designed around, so true-structure library spectra that differ by centroiding, binning, or instrument calibration lose fragment pairs and drop below `MIN_SIMILARITY`.

**How it improves score.** Doubling the match window to 0.02 Da recovers fragment pairs that entropy/modcos should have counted, raising `best_similarity` / `mean_top_k_similarity` for the correct InChIKey14 without changing the precursor mass filter, peak ladder, or entropy mix. One existing constant.

### 2. 1% intensity floor (`INTENSITY_FLOOR` 0.001→0.01) — P1 next unused

**Why.** `clean_spectrum` / MSEntropy `noise_threshold` default is 0.01 (1% of base peak). We still keep 0.1% ions. Cloud draft PRs #13–#19, #21, #23, #25 implement this; none merged. Alternate-day slot after peak-mz.

### 3. Entropy-dominant hybrid — already on

`ENTROPY_WEIGHT=0.75` is live. Actions slot-2 fallback still reapplies this no-op every UTC day and wastes a ticket. Retarget slot 2 to this cycle’s patch.

### 4. Analogue / multi-channel / forward models — P1, not this kernel

Public 0.32–0.48 entries use analogue expansion, ICEBERG/GLACIER simulation, and PubChem priors. Out of scope for a one-constant, internet-off ablation. Do not claim Class-3 de novo is solved by retrieval.

### 5. Exact-duplicate / poisoned-label guard — P0 keep

Exact test↔train copies in `enveda-180` carry train InChIKeys ≠ competition GT. `EXCLUDE_EXACT_DUPLICATES=True` stays on.

## Priority table (notebook-only, internet off)

| Pri | Method | Fits this kernel? | This slot? |
|-----|--------|-------------------|------------|
| P0 | `PEAK_MZ_TOL` 0.01→0.02 (MSEntropy default) | Yes, existing constant | **Yes — one major ablation** |
| P0 | Keep exact-dup ban | Already on | Keep |
| P1 | `INTENSITY_FLOOR` 0.001→0.01 | Yes; draft PRs unmerged | Next unused |
| P1 | Analogue / forward / popularity ranker | New code + datasets | Later |
| P2 | Spec2Vec / MS2Deepscore | Weights + cache | No |
| P2 | Formula → candidate enumeration | Slow / needs web DBs | No |

## Out of scope this cycle

- CSV `competitions submit` (notebook-only competition).
- Claiming Class-3 de novo structure elucidation from library retrieval.
- Training Spec2Vec / MS2Deepscore in the kernel.
- Changing more than one major factor (`PEAK_MZ_TOL` only).
- Merging yesterday’s still-open draft PRs by hand; this cycle re-implements H-peak-mz on a fresh branch with today’s docs.
