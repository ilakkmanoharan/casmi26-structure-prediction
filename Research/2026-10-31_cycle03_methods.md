# Research 2026-10-31_cycle03

`0 6,9,12 * * *` Cloud cron (07:00 CDT / last suggested Cloud cadence) fired at **12:03 UTC**. Next unused cycle on `main` after Actions cycle02 is still **cycle03**. Prior Cloud cycle03 PRs #50 (07:36Z), #51 (09:07Z), and #52 (10:36Z) stayed draft; 07:00 / 08:00 / 09:00 / 10:00 / 11:00 / **12:00** UTC casmi-loop hours did **not** fire.

## Sources reviewed

- Li, Kind, Fiehn — *Spectral entropy outperforms MS/MS dot product similarity* (Nature Methods 2021). Entropy similarity at **0.75** gave FDR <10% on 37,299 natural-product spectra vs NIST20. https://www.nature.com/articles/s41592-021-01331-z · https://pubmed.ncbi.nlm.nih.gov/34857935/
- de Jonge et al. — *Weighting Low-Intensity MS/MS Ions and m/z Frequency* (JASMS 2024). Optimal **entropy** cutoffs for structure-similar vs dissimilar pairs were **0.55 unweighted / 0.56 weighted**; modified-cosine optima were much higher (0.88 / 0.67). https://doi.org/10.1021/jasms.3c00353
- Li & Fiehn — *Flash Entropy Search* (Nature Methods 2023 / PMC11511675). After the 1% noise cut, fragment pairing uses **±20 mDa**. That window is already live (`PEAK_MZ_TOL=0.02`). https://pmc.ncbi.nlm.nih.gov/articles/PMC11511675/
- MSEntropy API — `get_topn_matches(..., min_similarity=0.01)` default is a *return* floor, not an identification cutoff. Production Flash Entropy / matchms workflows still apply a higher admission threshold after search. https://msentropy.readthedocs.io/en/latest/entropy_search_useful_functions.html
- Anekwe, Jarmusch, et al. — *Evaluating the Effects of Acquisition and Search Parameters on Repository-Scale MS/MS Matching* (JASMS 2026). Six matching peaks keep FDR <1% across cosine 0.7–1.0; fewer peaks need a stricter score. Weak hybrid hits without enough paired ions are the decoys our 0.05 floor currently admits. https://pubs.acs.org/doi/10.1021/jasms.6c00332
- MS2Query (de Jonge, Huber, van der Hooft — Nature Communications 2023). Scores >0.7 are generally reliable; 0.6–0.7 need caution; **<0.6 are often discarded**. Our live hybrid floor of 0.05 is an order of magnitude below that practice. https://www.nature.com/articles/s41467-023-37446-4 · https://wang-bioinformatics-lab.github.io/GNPS2_Documentation/ms2query_doc/
- Analog Propagation public notebook (prvsiyan V43) — public MRR@25 **0.456**. Library cosine/entropy plus analog transfer, not a 0.05 admission floor. https://www.kaggle.com/code/prvsiyan/analog-propagation-casmi-2026-baseline
- CASMI 2026 public-chain notes — 4-channel retrieval (library entropy/cosine + analog + MetFrag-lite + fingerprint) is what moved public scores from ~0.14–0.16 to ~0.33–0.47. Pure library search saturates when weak decoys fill the top-25. https://m0-ar.github.io/casmi-2026/RESEARCH.md
- Cubres public-notebook notes (2026-10-21) — analog notebooks now badge ~0.456–0.477; Kaggle public score covers ~31% of test molecules. https://github.com/cubres/enveda-casmi-2026/blob/main/README.md
- Public Kaggle notebooks (checked 12:04Z): `CASMI26 LB 0.477 | 0.472 Weights + Fragment Check` badges **0.477**; several forks sit at 0.469–0.472. https://www.kaggle.com/code?tagIds=7402-Chemistry
- CLIST standings (page “updated 15 hours ago” at 12:04Z): Parfionov **0.52**, Savko **0.52**, pikachu / Shehab / CHU1PC **0.50**. https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/

## Methods to consider

| ID | Method | Why | How it could raise MRR@25 | Fit (notebook, internet off) |
|----|--------|-----|---------------------------|------------------------------|
| **P0** | Raise `MIN_SIMILARITY` 0.05→0.12 | Live floor is below every literature identification cutoff. `retrieve.search_candidates` / `retrieve_for_spectrum` admits any hybrid score ≥0.05 into `TOP_K_SPECTRA=120`, then structure aggregation fills 25 slots with weak decoys. | Drops noisy library hits so true-structure near-matches (and later analog/formula cues) can occupy rank 1–5. | One constant. |
| P1 | `TOP_PEAKS` 128→160 | More fragments after the 1% floor can help entropy on rich spectra. | Secondary; only after the admission floor is no longer 0.05. | One constant. Next unused after this merge. |
| P1 | Analog / mass-shift channel | Public 0.33→0.46 gains came from analog transfer, not from another 0.02 Da replay. | Real path to Class-2; larger than a one-knob slot. | New retrieve path; later cycle. |
| P2 | Entropy ID cutoff 0.55–0.75 | Li/Fiehn and JASMS numbers. | Too aggressive for our hybrid entropy/modcos + cross-library CE; would empty many candidate lists. | Not this slot. |
| P2 | MS2Query / Spec2Vec / MS2Deepscore | Strong analog ranking in literature; public analog notebooks sit at 0.456–0.477. | Heavy offline weights; 9h kernel budget; internet off. | Out of scope this slot. |

## Why this slot is the admission floor

Live main after Actions 10-31 cycle02: `TOP_PEAKS=128`, `PEAK_MZ_TOL=0.02`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, mass-wide 35/80, **`MIN_SIMILARITY=0.05`**. Slot-2/3 fallbacks still replay `PEAK_MZ_TOL=0.02` (already live). Slot-4 `H-peaks` currently **resets** `MIN_SIMILARITY` to 0.05, which would undo this ablation.

0.12 is a conservative step: well above the 0.05 noise floor, well below Li/Fiehn 0.75, JASMS 0.55, and MS2Query’s “discard below 0.6” band, so recall on cross-instrument near-matches should survive.

## Out of scope this cycle

- Class-3 de novo (retrieval cannot solve it).
- CSV `competitions submit`.
- Dispatching casmi-loop before this patch is on `main` (would spend UTC ticket 3 on already-live `PEAK_MZ_TOL=0.02`).
- Analog / ICEBERG / fingerprint ranker (needs a dedicated implement, not a one-knob slot).
