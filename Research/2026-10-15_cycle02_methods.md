# Research 2026-10-15_cycle02 — 1% intensity floor

Competition: `enveda-CASMI26-molecule-id-mass-spectra`
Metric: public **MRR@25**
Constraint: notebook-only, **internet off**, one major ablation this slot.

## Sources reviewed

- Li, Kind, Folz, Vaniya, Mehta, Fiehn. *Spectral entropy outperforms MS/MS dot product similarity for small-molecule compound identification.* Nature Methods 18, 1524–1531 (2021). https://www.nature.com/articles/s41592-021-01331-z — NIST20 benchmark; entropy similarity 0.75 → FDR < 10% on 37,299 natural-product spectra; entropy remains robust when noise ions are added, which is the cleaning problem this slot addresses.
- MSEntropy `clean_spectrum_for_search(..., noise_threshold=0.01)`: drop peaks with intensity < **0.01 × max intensity**. Source: https://msentropy.readthedocs.io/en/latest/_modules/ms_entropy/entropy_search/flash_entropy_search.html
- Li, Fiehn. *Flash entropy search to query all mass spectral libraries in real time.* Nature Methods 20, 1475–1478 (2023). https://doi.org/10.1038/s41592-023-02012-9 · PMC https://pmc.ncbi.nlm.nih.gov/articles/PMC11511675/ — “possible fragment ions at <1% the maximal fragment ion abundance carry a high probability to stem from other sources than the precursor ion and are removed.”
- Huber et al. *matchms — processing and similarity evaluation of mass spectrometry data.* JOSS 5, 2411 (2020). https://doi.org/10.21105/joss.02411 — `select_by_relative_intensity(..., intensity_from=0.001)` is the conservative 0.1% example; Flash Entropy / matchms entropy search default to **0.01**.
- de Jonge et al. *MS2Query: reliable and scalable MS2 mass spectra-based analogue search.* Nature Communications 14 (2023). https://www.nature.com/articles/s41467-023-37446-4 — analogue expansion is how public 0.32–0.49 notebooks move; out of scope for this one-constant kernel.
- CLIST public standings snapshot ~2026-10-15T06:05Z: **CHU1PC 0.49**, pikachu 0.49, MarvinTMB 0.48, Oleksandr Parfionov 0.48, Dmitrii Khizbullin 0.47. https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/
- Community analog / ICEBERG+GLACIER + PubChem-prior notebooks public ~0.32–0.42. Example write-up: https://senanur-cetin.vercel.app/projects/kaggle-competitions-2026

## Methods to consider

### 1. Raise the relative intensity floor (`INTENSITY_FLOOR` 0.001→0.01) — **P0 this slot**

**Why.** `casmi26/spectrum.py:clean_spectrum` already normalizes to the base peak, then keeps `inten >= intensity_floor`. Live `main` still uses **0.001** (0.1% of max). Flash Entropy / MSEntropy default to **0.01**. With `TOP_PEAKS=128`, sub-1% isolation-window junk occupies the fragment ladder, inflates spectral entropy, and creates chance matches to unrelated library spectra — exactly the decoys that fill the MRR@25 list after the poisoned exact-dup ban.

**How it improves score.** A 1% cut removes noise ions from **both** queries and library spectra before entropy/modcos. True-structure neighbors that share a real fragment series rise in `best_similarity` / `mean_top_k_similarity`. One existing constant. Cloud draft PRs #13–#19, #21, #23, #25, #27, **#28** already specified this; none merged.

### 2. Fragment match window (`PEAK_MZ_TOL` 0.01→0.02) — P1 next unused

**Why.** MSEntropy `calculate_entropy_similarity` defaults to `ms2_tolerance_in_da=0.02`. Live main still uses 0.01 Da. Draft Cloud PRs #20/#22/#24/#26. Do **not** combine with H1 this slot.

### 3. Entropy-dominant hybrid — already on

`ENTROPY_WEIGHT=0.75` is live (Actions 2026-10-13_cycle02 → 57135691, and every later slot-2). Actions slot-2 fallback still reapplies this no-op every UTC day and wastes a ticket. Retarget slot 2 to this cycle’s patch.

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
