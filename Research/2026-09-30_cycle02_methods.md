# Research — 2026-09-30 cycle02

## Goal

Raise public MRR@25 above the only scored retrieval baseline (**0.143**, v0.1) toward the live public leaderboard (top **pikachu 0.464** as of 2026-09-30T06:12Z). This slot is the first Chicago competition-day cycle after 01:00 CDT. One major, notebook-only, internet-off change.

## Sources reviewed

1. **Li, Kind, Folz et al., Nat. Methods (2021)** — Spectral entropy similarity. Noise ions below **1% of base-peak intensity** were removed before benchmarking; entropy similarity still beat 42 alternatives including dot product. FDR &lt; 10% at entropy similarity **0.75** on experimental natural-product spectra.  
   https://www.nature.com/articles/s41592-021-01331-z

2. **msentropy `clean_spectrum` / `calculate_entropy_similarity` (Li)** — Default `noise_threshold=0.01` (drop peaks `&lt; 0.01 * max_intensity`), centroid, then keep top-N, then entropy. Python and R wrappers share this default.  
   https://msentropy.readthedocs.io/en/latest/classical_entropy_similarity.html  
   https://msentropy.readthedocs.io/en/latest/entropy_search_api.html  
   https://cran.r-project.org/web/packages/msentropy/refman/msentropy.html

3. **Li et al., Nat. Methods (2023) — Flash Entropy Search** — Identity / open / neutral-loss / hybrid search at library scale; identity search still uses a precursor-mass window. Speed, not a new scoring function.  
   https://www.nature.com/articles/s41592-023-02012-9

4. **Huber et al., Nat. Commun. (2023) — MS2Query** — Spec2Vec + MS2Deepscore + analog random forest. Finds chemical analogues when exact library hits are missing (35% analog recall, mean Tanimoto 0.63 vs 0.45 for modified cosine at the same recall). Needs offline embeddings and extra datasets. Public CASMI26 notebooks in this family sit ~0.23–0.34. Out of scope for this internet-off kernel.  
   https://www.nature.com/articles/s41467-023-37446-4

5. **Watrous / Bittremieux modified cosine** — Neutral-loss alignment remains useful for analogs; cosine is more noise-sensitive than entropy. Our hybrid is `0.75·entropy + 0.25·modcos`, so leftover 0.1%-of-base peaks still move rank via the cosine term.

6. **Competition metric / data notes** — MRR@25 on tautomer-canonical InChIKey14. Public LB ~33% of test. `enveda-180` is instrument-matched but **synthetic drug-like**; test chemistry is NP-like.  
   https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra/

## Methods to consider (this kernel)

| Priority | Method | Why it can lift MRR@25 | How in this notebook |
|----------|--------|------------------------|----------------------|
| **P0** | **1% intensity floor (msentropy default)** | Current `INTENSITY_FLOOR=0.001` keeps 10× more noise than the Li/Fiehn protocol. Noise ions inflate modified-cosine, promote analog decoys, and can change which 128 peaks survive `TOP_PEAKS`. Aligning the floor to 0.01 matches the entropy literature we already score with. | `INTENSITY_FLOOR = 0.01` |
| P0 | Keep exact-dup InChIKey14 ban | v0.1: identical `enveda-180` spectra, train labels ≠ GT → 0.143. Still required. | already on |
| P0 | Entropy-dominant hybrid 0.75 | FDR&lt;10% at 0.75; already live on main. | already on |
| P1 | Analog / fingerprint ranker over ChEBI–COCONUT | Public notebooks ~0.33; this is the real LB gap. | extra datasets; not this slot |
| P1 | Tighter `MIN_SIMILARITY` (0.12–0.15) | Drops junk into the 25-list. Cloud PRs #11/#12 never merged. | next unused after this floor |
| P2 | Flash entropy / open search | Coverage for glycosides / analogs without formula. | runtime + rewrite |
| P3 | De novo (DiffMS, MSNovelist) | Class-3 only. Retrieval cannot claim this. | out of scope |

## How this cycle’s method improves score

1. Query and library spectra are cleaned with the **same 1% floor** (`index.py` and `retrieve.py` both pass `cfg.intensity_floor`).
2. `TOP_PEAKS=128` then keeps the strongest real fragments instead of 128 peaks that include 0.1%-level noise.
3. Hybrid entropy/modcos sees fewer spurious peak matches → fewer high-scoring wrong InChIKey14s occupying ranks 1–5 (the MRR-sensitive slots).
4. Exact-dup ban still applies after cleaning; a slightly stricter floor can *change* which rows look “identical,” which is desirable if the 0.001 view was matching on shared noise.

## Out of scope this cycle

MS2Query / MS2Deepscore weights; formula→candidate DB; unconstrained de novo SMILES; CSV `competitions submit`; another mass/peaks/entropy sweep (those four fallbacks already rotate daily and are live on main).
