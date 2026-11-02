# Research — 2026-11-02 cycle03

Late `0 6 * * *` Cloud cron (pre-DST 01:00 CDT slot) fired at **07:32 UTC / 01:32 CST**, after US DST ended 2026-11-01. Chicago competition day **2026-11-02** is open (01:00 CST = 07:00 UTC). Actions `casmi-loop` **41406414674** is already in progress on `main` (started 07:27Z, checkout `3b6c562`) and will spend UTC ticket 2 on the live slot-2 fallback **H-peak-mz** (`PEAK_MZ_TOL=0.02`). This Cloud cycle is therefore **cycle03**: the next unused tag after Actions cycle01 (on main) and the in-flight cycle02.

Prior Cloud H-min-sim PRs **#38–#59** stayed draft. Live main is still `MIN_SIMILARITY=0.05`. The unused real ablation is the library-hit admission floor.

## Sources reviewed

- Li, Kind, Fiehn — *Spectral entropy outperforms MS/MS dot product similarity* (Nature Methods 2021). Entropy similarity at **0.75** gave FDR <10% on 37,299 natural-product spectra vs NIST20. Scores >0.75 are the identification band; our live hybrid floor of 0.05 is not. https://www.nature.com/articles/s41592-021-01331-z · https://pubmed.ncbi.nlm.nih.gov/34857935/ · https://escholarship.org/content/qt0249w6hk/qt0249w6hk.pdf
- de Jonge et al. — *Weighting Low-Intensity MS/MS Ions and m/z Frequency* (JASMS 2024). Optimal **entropy** cutoffs for structure-similar vs dissimilar pairs were **0.55 unweighted / 0.56 weighted**; modified-cosine optima were much higher (0.88 / 0.67). https://doi.org/10.1021/jasms.3c00353
- Li & Fiehn — *Flash Entropy Search* (Nature Methods 2023 / PMC11511675). After the 1% noise cut, fragment pairing uses **±20 mDa**. That window is already live (`PEAK_MZ_TOL=0.02`). https://pmc.ncbi.nlm.nih.gov/articles/PMC11511675/ · https://doi.org/10.1038/s41592-023-02012-9
- Mohler, Bittremieux et al. — *Evaluating the Effects of Acquisition and Search Parameters on Repository-Scale MS/MS Matching* (JASMS 2026). Six matched peaks keep FDR <1% across cosine 0.7–1.0; fewer peaks need a much higher cosine. Our 0.05 hybrid floor admits hits that would fail that repository-search bar. https://pubs.acs.org/doi/10.1021/jasms.6c00332
- MSEntropy API — `get_topn_matches(..., min_similarity=0.01)` / `get_topn_spec_idx_and_similarity(..., min_similarity=0.1)` are *return* floors, not identification cutoffs. Production Flash Entropy / matchms workflows still apply a higher admission threshold after search. https://msentropy.readthedocs.io/en/latest/_modules/ms_entropy/entropy_search/flash_entropy_search.html · https://msentropy.readthedocs.io/en/latest/dynamic_api.html
- matchms `FlashSimilarity` default: `score_type="spectral_entropy"`, `tolerance=0.02`, `noise_cutoff=0.01` — already live. It does not set a 0.05 identification floor. https://matchms.readthedocs.io/en/stable/api/matchms.similarity.FlashSimilarity.html
- Huber, van der Hooft et al. — *MS2DeepScore* (J Cheminform 2021) and Huber et al. — *Spec2Vec* (PLOS Comput Biol 2021). Embeddings correlate better with Tanimoto than cosine, but need offline weights. https://jcheminf.biomedcentral.com/articles/10.1186/s13321-021-00558-4 · https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1008724
- MS2Query (de Jonge, Huber, van der Hooft — Nature Communications 2023; iomega/ms2query). Scores >0.7 are generally reliable; 0.6–0.7 need caution; **<0.6 are often discarded**. Our live hybrid floor of 0.05 is an order of magnitude below that practice. https://www.nature.com/articles/s41467-023-37446-4 · https://github.com/iomega/ms2query
- GNPS library search defaults still require cosine ≥0.5 and ≥6 matched peaks — also far above 0.05. https://ccms-ucsd.github.io/GNPSDocumentation/librarysearch/
- Analog / community public notebooks: Flexonafft `CASMI26: Closing the Evidence Gap` still badges **0.479**; prvsiyan Analog Propagation V43 is **0.456**. Analog / fingerprint rerank, not a 0.05 admission floor. https://www.kaggle.com/code/flexonafft/casmi26-closing-the-evidence-gap · https://www.kaggle.com/code/prvsiyan/analog-propagation-casmi-2026-baseline
- CASMI 2026 public-chain notes — 4-channel retrieval (library entropy/cosine + analog + MetFrag-lite + fingerprint) is what moved public scores from ~0.14–0.16 to ~0.33–0.47. Pure library search saturates when weak decoys fill the top-25. https://m0-ar.github.io/casmi-2026/RESEARCH.md
- CLIST standings (re-fetched 07:35Z): Savko **0.52**, Parfionov **0.52**, democat **0.51**, pikachu / Shehab / CHU1PC **0.50**. https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/

## Methods to consider

| ID | Method | Why | How it could raise MRR@25 | Fit (notebook, internet off) |
|----|--------|-----|---------------------------|------------------------------|
| **P0** | Raise `MIN_SIMILARITY` 0.05→0.12 | Live floor is below every literature identification cutoff. `retrieve_for_spectrum` admits any hybrid score ≥0.05 into `TOP_K_SPECTRA=120`, then structure aggregation fills 25 slots with weak decoys. | Drops noisy library hits so true-structure near-matches (and later analog/formula cues) can occupy rank 1–5. | One constant. |
| P1 | `TOP_PEAKS` 128→160 | More fragments after the 1% floor can help entropy on rich spectra. | Secondary; only after the admission floor is no longer 0.05. | One constant. Next unused after this merge. |
| P1 | Analog / mass-shift channel | Public 0.33→0.48 gains came from analog transfer, not from another 0.02 Da replay. | Real path to Class-2; larger than a one-knob slot. | New retrieve path; later cycle. |
| P2 | Entropy ID cutoff 0.55–0.75 | Li/Fiehn and JASMS numbers. | Too aggressive for our hybrid entropy/modcos + cross-library CE; would empty many candidate lists. | Not this slot. |
| P2 | MS2Query / Spec2Vec / MS2Deepscore | Strong analog ranking in literature; public analog notebooks sit at 0.456–0.479. | Heavy offline weights; 9h kernel budget; internet off. | Out of scope this slot. |

## Why this slot is the admission floor

Live main after Actions 11-02 cycle01: `TOP_PEAKS=128`, `PEAK_MZ_TOL=0.02`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, mass-wide 35/80, **`MIN_SIMILARITY=0.05`**. Slot-2/3 fallbacks still replay `PEAK_MZ_TOL=0.02` (already live) — that is what the 07:27Z Actions run is executing. Slot-4 `H-peaks` currently **resets** `MIN_SIMILARITY` to 0.05, which would undo this ablation. Next unused casmi-loop hourly after that in-flight job is **08:00 UTC**.

0.12 is a conservative step: well above the 0.05 noise floor, well below Li/Fiehn 0.75, JASMS 0.55, GNPS cosine 0.5, and MS2Query’s “discard below 0.6” band, so recall on cross-instrument near-matches should survive.

## Out of scope this cycle

- Class-3 de novo (retrieval cannot solve it).
- CSV `competitions submit`.
- Dispatching casmi-loop while 41406414674 is in progress, or before this patch is on `main` (would waste another UTC ticket on already-live `PEAK_MZ_TOL=0.02`).
- Analog / ICEBERG / fingerprint ranker (needs a dedicated implement, not a one-knob slot).
