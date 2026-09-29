# Research — 2026-09-29 cycle02

## Goal

Raise public MRR@25 above the only scored retrieval baseline (**0.143**, v0.1) toward the live public leaderboard (top **pikachu 0.440** as of 2026-09-29T06:00Z). This slot is the first Chicago competition-day cycle after 01:00 CDT. One major, notebook-only, internet-off change.

## Sources reviewed

1. **Li & Fiehn, Nat. Methods (2021)** — Spectral entropy similarity. Noise ions below **1% of base-peak intensity** were removed before benchmarking; entropy similarity still beat 42 alternatives including dot product. FDR < 10% at entropy similarity **0.75**.  
   https://www.nature.com/articles/s41592-021-01331-z  
   PDF: https://yuanyue.li/project/spectral_entropy/Yuanyue-spectral_entropy.pdf

2. **msentropy `clean_spectrum` (Li)** — Default `noise_threshold=0.01` (drop peaks `< 0.01 * max_intensity`), then keep top-N, then entropy.  
   https://msentropy.readthedocs.io/en/latest/classical_spectral_entropy.html

3. **Li & Fiehn, Nat. Methods (2023) — Flash Entropy Search** — Identity / open / neutral-loss / hybrid search at library scale; identity search still uses a precursor-mass window. Speed, not a new scoring function.  
   https://www.nature.com/articles/s41592-023-02012-9

4. **MoNA entropy quality flags** — “noisy” if raw entropy ≥ 3.0 and normalized entropy ≥ 0.8. Complements peak-floor cleaning.  
   https://mona.fiehnlab.ucdavis.edu/documentation/entropy

5. **Watrous / Bittremieux modified cosine** — Neutral-loss alignment remains useful for analogs; cosine is more noise-sensitive than entropy. Our hybrid is `0.75·entropy + 0.25·modcos`, so leftover 0.1%-of-base peaks still move rank via the cosine term.

6. **MS2Query (Nat. Commun. 2023)** — Spec2Vec + MS2Deepscore + analog RF. Strong for Class-3 / out-of-library, but needs offline embeddings and extra datasets. Public CASMI26 notebooks in this family sit ~0.23–0.34 (e.g. Analog Propagation 0.335; community analog ranker 0.236). Out of scope for this kernel.

7. **Competition metric / data notes** — MRR@25 on tautomer-canonical InChIKey14 (RDKit 2026.03.3). Public LB ~33% of test. `enveda-180` is instrument-matched but **synthetic drug-like**; test chemistry is NP-like.  
   https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra/

## Methods to consider (this kernel)

| Priority | Method | Why it can lift MRR@25 | How in this notebook |
|----------|--------|------------------------|----------------------|
| **P0** | **1% intensity floor (msentropy default)** | Current `INTENSITY_FLOOR=0.001` keeps 10× more noise than the Li/Fiehn protocol. Noise ions inflate modified-cosine, promote analog decoys, and can change which 128 peaks survive `TOP_PEAKS`. Aligning the floor to 0.01 matches the entropy literature we already score with. | `INTENSITY_FLOOR = 0.01` |
| P0 | Keep exact-dup InChIKey14 ban | v0.1: identical `enveda-180` spectra, train labels ≠ GT → 0.143. Still required. | already on |
| P0 | Entropy-dominant hybrid 0.75 | FDR<10% at 0.75; already live on main. | already on |
| P1 | Analog / fingerprint ranker over ChEBI–COCONUT | Public notebooks ~0.33; this is the real LB gap. | extra datasets; not this slot |
| P1 | Tighter `MIN_SIMILARITY` (0.12–0.15) | Drops junk into the 25-list. Previous Cloud PRs never merged. | next unused after this floor |
| P2 | Flash entropy / open search | Coverage for glycosides / analogs without formula. | runtime + rewrite |
| P3 | De novo (DiffMS, MSNovelist) | Class-3 only. Retrieval cannot claim this. | out of scope |

## How this cycle’s method improves score

1. Query and library spectra are cleaned with the **same 1% floor** (`index.py` and `retrieve.py` both pass `cfg.intensity_floor`).
2. `TOP_PEAKS=128` then keeps the strongest real fragments instead of 128 peaks that include 0.1%-level noise.
3. Hybrid entropy/modcos sees less spurious peak matches → fewer high-scoring wrong InChIKey14s occupying ranks 1–5 (the MRR-sensitive slots).
4. Exact-dup ban still applies after cleaning; a slightly stricter floor can *change* which rows look “identical,” which is desirable if the 0.001 view was matching on shared noise.

## Out of scope this cycle

MS2Query / MS2Deepscore weights; formula→candidate DB; unconstrained de novo SMILES; CSV `competitions submit`; another mass/peaks/entropy sweep (those four fallbacks already rotate daily and are live on main).
