# Research 2026-10-10_cycle02

Notebook-only, internet-off kernel. Metric: public **MRR@25**. One major factor this slot: fragment **m/z match tolerance** for the entropy / modified-cosine hybrid.

## Sources reviewed

- Li, Kind, Folz, Vaniya, Mehta, Fiehn, *Nature Methods* (2021): [Spectral entropy outperforms MS/MS dot product similarity](https://www.nature.com/articles/s41592-021-01331-z). NIST20 / MassBank.us ions were matched at **0.05 Da**. FDR &lt; 10% near entropy similarity **0.75**. Low-abundance ions &lt; **1% of base peak** were dropped before scoring.
- Li & Fiehn, *Nature Methods* (2023): [Flash entropy search](https://www.nature.com/articles/s41592-023-02012-9) / [PMC11511675](https://pmc.ncbi.nlm.nih.gov/articles/PMC11511675/). Open search matches fragments in a **±20 mDa** window because low-abundance ions can already err by ~10 mDa and library peaks add more error. `MSEntropy` API default is [`ms2_tolerance_in_da=0.02`](https://msentropy.readthedocs.io/en/latest/entropy_search_api.html); `noise_threshold=0.01`.
- matchms library search: `ModifiedCosineGreedy(tolerance=0.02)` is the documented analog / identity workflow ([workflows](https://cdn.jsdelivr.net/npm/pi-scientific-skills@1.1.0/skills/matchms/references/workflows.md)). Cosine-family `tolerance` is **absolute Da**, not ppm.
- Community analog / quad-channel notebooks on the [CASMI 2026 code tab](https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra/code) sit at **0.328–0.339**. Prize-table public scores (CLIST) remain 0.45–0.48. Those jumps need analog / multi-channel rankers, not another recycle of live knobs.

## Methods to consider

| Method | Why | How it could raise MRR@25 |
| --- | --- | --- |
| **Widen `PEAK_MZ_TOL` 0.01 → 0.02** | `retrieve.py` calls `hybrid_similarity(..., tol=cfg.peak_mz_tol)`. Live **0.01 Da** is matchms-tight / Orbitrap-ish. Flash Entropy Search and matchms library-search examples use **0.02 Da**. Mixed GNPS / MassBank / MONA / RIKEN centroids are often worse than 10 mDa. | More true fragment pairs survive `_greedy_match`, so correct InChIKey14s get higher hybrid scores and climb the top-25. |
| Noise floor `INTENSITY_FLOOR` 0.001 → 0.01 | Li/Fiehn + Flash drop ions &lt; 1% of base peak. Still unused on `main` (draft PRs #13–#19, #21, #23). | Fewer noise–noise matches; keep for the next unused slot. |
| Raise `MIN_SIMILARITY` 0.05 → 0.12 | Cuts junk neighbors before molecule aggregation. Draft PRs #11/#12. | Helps precision; risk of empty lists on sparse queries. |
| Analog / formula / PubChem join | How 0.40+ public kernels jump Class-2/3. | Extra candidate generation; not a one-constant ablation. |

## Priority (this kernel)

| Pri | Change | Fit |
| --- | --- | --- |
| **P0** | `PEAK_MZ_TOL` 0.01 → **0.02** | One existing constant; Flash / matchms default; unused on `main`. |
| P1 | `INTENSITY_FLOOR` 0.01 | Next unused lever after this slot (still draft). |
| P1 | `MIN_SIMILARITY` 0.12 | After peak-mz / intensity. |
| P2 | Analog / de novo / PubChem | Not this cycle; retrieval does not solve Class-3. |

## Out of scope

- Claiming Class-3 de novo is solved by library retrieval.
- CSV `competitions submit` (notebook-only).
- Re-applying live no-ops: `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, mass-wide 35/80, `TOP_K=120`.
- Repeating yesterday’s Cloud H-intensity PR (#23, still draft).
