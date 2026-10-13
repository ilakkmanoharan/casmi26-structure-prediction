# Research 2026-10-13_cycle02 — 1% intensity floor

Competition: `enveda-CASMI26-molecule-id-mass-spectra`  
Metric: public **MRR@25**  
Constraint: notebook-only, **internet off**, one major ablation this slot.

## Sources reviewed

- Li, Kind, Folz, Vaniya, Mehta, Fiehn. *Spectral entropy outperforms MS/MS dot product similarity for small-molecule compound identification.* Nature Methods 18, 1524–1531 (2021). https://www.nature.com/articles/s41592-021-01331-z — NIST20 benchmark; entropy similarity 0.75 → FDR < 10% on 37,299 natural-product spectra; cleaning keeps ions above ~1% of the base peak.
- MSEntropy `clean_spectrum(..., noise_threshold=0.01)`: drop peaks with intensity < **0.01 × max intensity**. Docs: https://msentropy.readthedocs.io/en/latest/classical_api.html and source https://msentropy.readthedocs.io/en/latest/_modules/ms_entropy/spectra/tools.html
- Flash Entropy `clean_spectrum_for_search(..., noise_threshold=0.01)`. https://msentropy.readthedocs.io/en/latest/entropy_search_api.html
- Li, Fiehn. *Flash entropy search to query all mass spectral libraries in real time.* Nature Methods 20, 1475–1478 (2023). https://doi.org/10.1038/s41592-023-02012-9
- matchms `select_by_relative_intensity` default lower bound is 1% of base peak (same relative cut).
- de Jonge et al. *MS2Query: reliable and scalable MS2 mass spectra-based analogue search.* Nature Communications 14 (2023). https://www.nature.com/articles/s41467-023-37446-4
- Community analog / ICEBERG+GLACIER + PubChem-prior notebooks public ~0.32–0.42. Example write-up: https://senanur-cetin.vercel.app/projects/kaggle-competitions-2026
- CLIST public standings (fetched 2026-10-13T06:05Z): **CHU1PC 0.49**, MarvinTMB 0.48, pikachu 0.48, Kucing Garong 0.47, then a 0.46 pack. https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/
- Kaggle competition page. https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra/

## Methods to consider

### 1. Raise the relative intensity floor (`INTENSITY_FLOOR` 0.001→0.01) — **P0 this slot**

**Why.** `casmi26/spectrum.py:clean_spectrum` already normalizes to the base peak, then keeps `inten >= intensity_floor`. Live `main` still uses **0.001** (0.1% of max). Flash Entropy / MSEntropy / matchms all default to **0.01**. With `TOP_PEAKS=128`, sub-1% isolation-window junk occupies the fragment ladder, inflates spectral entropy, and creates chance matches to unrelated library spectra — exactly the decoys that fill the MRR@25 list after the poisoned exact-dup ban.

**How it improves score.** A 1% cut removes noise ions from **both** queries and library spectra before entropy/modcos. True-structure neighbors that share a real fragment series rise in `best_similarity` / `mean_top_k_similarity`. One existing constant. Cloud draft PRs #13–#19, #21, #23, #25 already specified this; none merged.

### 2. Fragment match window (`PEAK_MZ_TOL` 0.01→0.02) — P1 next unused

**Why.** MSEntropy `calculate_entropy_similarity` defaults to `ms2_tolerance_in_da=0.02`. Live main still uses 0.01 Da. Draft Cloud PRs #20/#22/#24/#26. Do **not** combine with H1 this slot.

### 3. Entropy-dominant hybrid — already on

`ENTROPY_WEIGHT=0.75` is live. Actions slot-2 fallback still reapplies this no-op every UTC day and wastes a ticket. Retarget slot 2 to this cycle’s patch.

### 4. Analogue / multi-channel / forward models — P1, not this kernel

Public 0.32–0.49 entries use analogue expansion, ICEBERG/GLACIER simulation, and PubChem priors. Out of scope for a one-constant, internet-off ablation. Do not claim Class-3 de novo is solved by retrieval.

### 5. Exact-duplicate / poisoned-label guard — P0 keep

Exact test↔train copies in `enveda-180` carry train InChIKeys ≠ competition GT. `EXCLUDE_EXACT_DUPLICATES=True` stays on.

## Priority table (notebook-only, internet off)

| Pri | Method | Fits this kernel? | This slot? |
|-----|--------|-------------------|------------|
| P0 | `INTENSITY_FLOOR` 0.001→0.01 (Flash Entropy / matchms 1% cut) | Yes, existing constant | **Yes — one major ablation** |
| P0 | Keep exact-dup ban | Already on | Keep |
| P1 | `PEAK_MZ_TOL` 0.01→0.02 | Yes; draft PRs unmerged | Next unused |
| P1 | `MIN_SIMILARITY` 0.05→0.12 | Yes; draft PRs #11/#12 | Later |
| P1 | Analogue / forward / popularity ranker | New code + datasets | Later |
| P2 | Spec2Vec / MS2Deepscore | Weights + cache | No |
| P2 | Formula → candidate enumeration | Slow / needs web DBs | No |

## Out of scope this cycle

- CSV `competitions submit` (notebook-only competition).
- Claiming Class-3 de novo structure elucidation from library retrieval.
- Training Spec2Vec / MS2Deepscore in the kernel.
- Changing more than one major factor (`INTENSITY_FLOOR` only).
- Merging yesterday’s still-open draft PRs by hand; this cycle re-implements H-intensity on a fresh branch with today’s docs.
