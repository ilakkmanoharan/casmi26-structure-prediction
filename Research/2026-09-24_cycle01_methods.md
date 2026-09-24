# Research — 2026-09-24 cycle01

## Goal

Raise public MRR@25 above the last scored retrieval baseline (**0.143**, v0.1) toward the current public leaders (~**0.33**). This cycle is a notebook-only, internet-off Kaggle kernel: keep one major ablation that the existing `casmi26` stack can run without new weights or network.

## Sources reviewed

1. **Li, Kind, Folz, Vaniya, Mehta & Fiehn, Nat. Methods (2021)** — *Spectral entropy outperforms MS/MS dot product similarity for small-molecule compound identification*. Entropy similarity beat 42 alternatives, including dot product, on 434,287 queries vs NIST20; FDR &lt; 10% near score 0.75 on natural-product spectra.  
   https://www.nature.com/articles/s41592-021-01331-z  
   https://pubmed.ncbi.nlm.nih.gov/34857935/

2. **MS-Entropy docs (Li)** — Cleaning guidance that matches our kernel constraints: drop ions above precursor−1.6 Da, drop &lt;1% base-peak noise, then entropy-weight intensities. Default `calculate_entropy_similarity` assumes cleaned, centroided peaks.  
   https://msentropy.readthedocs.io/en/latest/classical_entropy_similarity.html

3. **Li & Fiehn, Nat. Methods (2023)** — *Flash entropy search to query all mass spectral libraries in real time*. Identity / open / neutral-loss / hybrid search; same entropy metric at library scale. Our mass-window + hybrid score is a small-library analogue, not Flash Entropy itself.  
   https://doi.org/10.1038/s41592-023-02012-9

4. **de Jonge, Louwen, Huber & van der Hooft, Nat. Commun. (2023)** — *MS2Query*. Spec2Vec + MS2Deepscore + precursor m/z + RF re-rank; analogue search without a hard precursor prefilter. Better chemical-similarity recall than modified cosine at the same 35% recall, but needs offline embeddings we do not ship in this kernel.  
   https://www.nature.com/articles/s41467-023-37446-4

5. **Kaggle / CLIST public LB (fetched 2026-09-24 ~06:10 UTC)** — Public slice (~33% of test). Top: **GUAM 0.332**, Minal kharat123 0.324, Preechanon Chatthai 0.319, Amaan 0.311, Ben Pepper 0.310. Ozymandias31415 listed at 0.298 (the 0.415 figure from 09-22 is stale).  
   https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra/leaderboard  
   https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/

6. **Committed cycle notes (2026-09-15…17) + Actions briefing 35953065654** — v0.1 exact test↔train dups in `enveda-180` with train labels ≠ GT; cycle05 left `TOP_PEAKS=5` on `main`.

## Methods to consider

| Priority | Method | Why it can lift MRR@25 | How in this kernel |
|----------|--------|------------------------|--------------------|
| **P0** | Restore a real fragment ladder (`TOP_PEAKS` 5→128) | Entropy similarity and modified cosine both need matched fragment ions. Five peaks after cleaning collapses both scores toward noise / precursor-only matches. Li 2021 and MS-Entropy cleaning assume a cleaned *spectrum*, not a 5-ion stub. | Config only. Same `clean_spectrum` on query + library. |
| **P0** | Keep exact-dup InChIKey14 ban | Perfect library match on leaked `enveda-180` rows produced ~0.143 because those train labels are not competition GT. | Already on `main` (`EXCLUDE_EXACT_DUPLICATES=True`). |
| **P1** | Entropy-dominant hybrid (raise `ENTROPY_WEIGHT`) | Li 2021: entropy &gt; cosine for ID; still keep some modified cosine for analog / CE-shifted pairs. | Next slot after the peak-ladder restore is scored. |
| **P1** | Structure-level ExactMolWt + slightly wider backfill | Recovers candidates when adduct inference is off; 10/15 ppm on cycle05 is tight if adduct strings are noisy. | `MASS_TOL_PPM` / `MASS_TOL_PPM_BACKFILL` only. |
| **P2** | Flash Entropy / MS2Query embeddings | Literature SOTA for coverage + analogues. | Out of scope: extra wheels, internet-off weights, 9h risk. |
| **P3** | Class-3 de novo (MSNovelist, DiffMS, …) | Needed when the structure is absent from every library. | Retrieval cannot claim this. Deferred. |

## How this cycle should improve score

1. Stop throwing away mid-intensity diagnostic fragments (`TOP_PEAKS=128`).
2. Keep poisoned exact-dup InChIKeys banned.
3. Do **not** retune mass windows or entropy weight in the same slot — otherwise we cannot attribute a score move.
4. Unblock GitHub Actions: `_openai_json` must fall back on HTTP 429 so the hourly runner can apply this ablation and `competition_submit_code`.

## Out of scope this cycle

MS2Deepscore / Spec2Vec / MS2Query weights; Flash Entropy GPU index; CFM-ID predicted spectra; unconstrained de novo SMILES; CSV `competitions submit`.
