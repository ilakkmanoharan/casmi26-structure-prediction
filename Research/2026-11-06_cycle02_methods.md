# Research — 2026-11-06 cycle02

Cloud Automation cron `0 6 * * *` fired late at **10:30 UTC / 04:30 CST**. Chicago competition day **2026-11-06** is open (started 01:00 CST = 07:00 UTC). Goal: raise public **MRR@25** on `enveda-CASMI26-molecule-id-mass-spectra` under a notebook-only, internet-off kernel.

## Sources reviewed

- Li & Fiehn, *Nature Methods* 2021 — spectral entropy vs 42 similarity algorithms; FDR &lt; 10% on 37,299 natural-product spectra at entropy similarity **0.75**. Very low scores are mostly decoys; the paper still recommends ranking several close hits rather than trusting only rank-1. https://www.nature.com/articles/s41592-021-01331-z
- Li, Fiehn et al. PDF (eScholarship) — NIST20 FDR curves; information-poor spectra (entropy S &lt; 1) still show FDR &gt; 23% at score 0.9. https://escholarship.org/content/qt0249w6hk/qt0249w6hk.pdf
- Li, Fiehn et al., *Nature Methods* 2023 — Flash Entropy Search; open-search fragment window **20 mDa** (Δm/z = 20 mDa lookup) because 10 mDa misses low-abundance centroid error. Spectra are denoised at **1%** max intensity. https://www.nature.com/articles/s41592-023-02012-9
- PMC full text of Flash Entropy — ion matching uses a 20 mDa window; precursor ions above precursor−1.6 Da are removed. https://pmc.ncbi.nlm.nih.gov/articles/PMC11511675/
- `ms_entropy` API — `ms2_tolerance_in_da=0.02`, `noise_threshold=0.01` defaults. https://msentropy.readthedocs.io/en/latest/entropy_search_api.html
- de Jonge et al., *Nature Communications* 2023 — MS2Query analogue search (MS2DeepScore prefilter + Spec2Vec / Δm/z / neighborhood Tanimoto random forest). A **minimum threshold** on the model score is how unreliable library hits are dropped. https://www.nature.com/articles/s41467-023-37446-4
- GNPS2 MS2Query docs — score &gt; 0.7 is generally reliable; 0.6–0.7 needs caution; **&lt; 0.6 is often discarded**. That is a much higher gate than our live 0.05 hybrid floor. https://wang-bioinformatics-lab.github.io/GNPS2_Documentation/ms2query_doc/
- Scheubert, Böcker et al., *Nature Communications* 2017 — FDR for spectral matching is **project-specific**; default GNPS cosine 0.7 / 6 matched ions is often too strict *or* too loose. Thresholds must be measured, not copied. https://www.nature.com/articles/s41467-017-01318-5
- Bushuiev et al., MassSpecGym (arXiv:2410.23326) — de novo / retrieval benchmark; CASMI-style challenges remain small and retrieval-only does not solve unseen structures. https://arxiv.org/abs/2410.23326
- Prior committed cycle notes: `Research/2026-10-24_cycle03_methods.md`, `Hypothesis analysis/2026-10-24_cycle03_hypotheses.md`. Unmerged Cloud drafts #77/#78/#79 already specified this H-sim-gate ablation and never landed on `main`.

## Methods to consider

| Method | Why | How it could raise MRR@25 |
|--------|-----|---------------------------|
| **Raise hybrid admission floor (`MIN_SIMILARITY` 0.05 → 0.12)** | Live gate is 15× below Li/Fiehn’s 0.75 annotation cutoff and far below MS2Query’s “discard below ~0.6” practice. `retrieve_for_spectrum` keeps every mass-window hit with `sim >= cfg.min_similarity` (`casmi26/retrieve.py` line 146). At 0.05, random isobars with a couple of shared ions fill `TOP_K_SPECTRA=120` and then the MRR@25 list. | Drop weak decoys before aggregation. True near-matches after Flash Entropy 20 mDa pairing typically sit well above 0.12; Class-1 library IDs are not the ones dying at 0.05–0.12. 0.12 is still a *soft* decoy filter, not a 0.75 identity cut, so sparse queries keep some neighbors. |
| Entropy / modified-cosine hybrid at 0.75 | Already live (`ENTROPY_WEIGHT=0.75`). Matches Li/Fiehn mix; not an unused lever. | Skip this slot. Next unused contrast is 0.75 → 1.0 (pure entropy). |
| Flash Entropy 20 mDa pairing | Already live (`PEAK_MZ_TOL=0.02`). Slot-2/3 Actions fallbacks on `main` still replay this no-op. | Do not spend a ticket on it. Retarget fallbacks. |
| Intensity floor 1% + 128-peak ladder | Already live (`INTENSITY_FLOOR=0.01`, `TOP_PEAKS=128`). UTC ticket 1 today already replayed H-top-peaks (kernel v198 / Kaggle 58042294). | Skip. |
| Tighter precursor mass (`MASS_TOL_PPM` 35 → 10) | 35 ppm on a 400 Da ion is ±0.014 Da; many unrelated formulas share that window. | Next unused after H-sim-gate. Risk: adduct/isotope error on timsTOF. |
| MS2Query / Spec2Vec / MS2DeepScore | Better analogue ranking for Class-2. Needs pretrained embeddings and extra deps. The *idea* of a score gate is in-scope; the models are not. | Out of scope this cycle (internet off; no embedding dataset attached). |
| SIRIUS / CSI:FingerID / ICEBERG | Formula → fingerprint → structure; how public 0.46–0.54 notebooks score Class-2. | Out of scope: heavy binaries, not in current kernel. |
| Class-3 de novo | MassSpecGym / MSNovelist-style generation. | **Not claimed.** Retrieval cannot solve structures absent from every library. |

## Priority (notebook-only, internet off)

| P | Change | Fit |
|---|--------|-----|
| **P0** | **`MIN_SIMILARITY` 0.05 → 0.12** | One existing constant. Changes which spectra enter the rank list. First unused lever after Flash Entropy pairing / noise-cut / 0.75 mix / 128-peak ladder are live. |
| P1 | `MASS_TOL_PPM` 35 → 10 | Next unused real ablation after H-sim-gate lands. |
| P1 | `ENTROPY_WEIGHT` 0.75 → 1.0 | Pure entropy vs hybrid; orthogonal to the gate. |
| P2 | `TOP_PEAKS` 128 → 160 | Slot-4 fallback already tries 160 + min_sim 0.05 (a *lower* gate — useful contrast only after 0.12 is live). |
| P2 | Domain-prior boost | Slot-5 fallback; values already match live `DOMAIN_PRIOR`. |

## Out of scope this cycle

- Attaching MS2Query / SIRIUS / ICEBERG weights.
- Claiming Class-3 de novo is solved by retrieval.
- CSV `competitions submit` (notebook-only competition).
- Replaying `PEAK_MZ_TOL=0.02`, `TOP_PEAKS=128`, or `INTENSITY_FLOOR=0.01`.
