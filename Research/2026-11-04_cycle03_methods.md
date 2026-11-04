# Research — 2026-11-04 cycle03

Late `0 6 * * *` Cloud cron at **12:04 UTC / 06:04 CST** (between the Chicago 05:30 and 07:00 suggested slots). US DST ended 2026-11-01, so America/Chicago is CST (UTC−6). Chicago competition day **2026-11-04 is open** (01:00 CST Nov 4 = 07:00 UTC). UTC calendar 2026-11-04 already has Actions cycle01 (H-top-peaks) and cycle02 (H-peak-mz no-op) on `main`. Next unused cycle on `main` is **cycle03**.

Prior Cloud H-min-sim PRs **#38–#70** stayed draft. After #66 (12:00Z Nov 3), Actions spent later tickets on already-live or immediately-reverted knobs:

- 15:57Z → 11-03 cycle03 H-peak-mz (already-live `PEAK_MZ_TOL=0.02`)
- 21:40Z → 11-03 cycle04 H-peaks (`TOP_PEAKS=160`; a real ablation, public score still null)
- 01:59Z Nov 4 → 11-04 cycle01 H-top-peaks (`TOP_PEAKS=128`, undoing cycle04)
- 08:59Z Nov 4 → 11-04 cycle02 H-peak-mz (Kaggle **57979390**, kernel **v192**, already-live `PEAK_MZ_TOL=0.02`)

The 10:32Z Cloud run opened **#70** with the same unused floor raise, asking for a merge before **11:00 UTC**. That hourly **did not fire**. `MIN_SIMILARITY=0.12` has **never** been submitted. 10:00, 11:00, and 12:00 UTC casmi-loop also did **not** fire. Next unused casmi-loop hourly is **13:00 UTC**.

## Sources reviewed

- Li, Kind, Fiehn — *Spectral entropy outperforms MS/MS dot product similarity* (Nature Methods 2021). Entropy similarity at **0.75** gave FDR <10% on 37,299 natural-product spectra vs NIST20. Scores >0.75 are the identification band; our live hybrid floor of 0.05 is not. https://www.nature.com/articles/s41592-021-01331-z · https://pubmed.ncbi.nlm.nih.gov/34857935/
- de Jonge et al. — *Weighting Low-Intensity MS/MS Ions and m/z Frequency* (JASMS 2024). Optimal **entropy** cutoffs for structure-similar vs dissimilar pairs were **0.55 unweighted / 0.56 weighted**; modified-cosine optima were much higher (0.88 / 0.67). https://doi.org/10.1021/jasms.3c00353 · https://pmc.ncbi.nlm.nih.gov/articles/PMC10854760/
- Scheubert, Hufsky, Petras, Wang, Nothias, Dührkop, Bandeira, Dorrestein, Böcker — *Significance estimation for large scale metabolomics annotations by spectral matching* (Nature Communications 2017). Spectral-match FDR is threshold-dependent; GNPS community four-star annotations at cosine **0.7** were ~91% correct. A 0.05 floor is far below that operating point. https://www.nature.com/articles/s41467-017-01318-5
- Li & Fiehn — *Flash Entropy Search* (Nature Methods 2023). After the 1% noise cut, fragment pairing uses **±20 mDa**. That window is already live (`PEAK_MZ_TOL=0.02`). https://doi.org/10.1038/s41592-023-02012-9 · https://pmc.ncbi.nlm.nih.gov/articles/PMC11511675/ · https://github.com/YuanyueLi/FlashEntropySearch
- MSEntropy API — `search(..., ms2_tolerance_in_da=0.02, noise_threshold=0.01)` is the live pairing/noise pair. `get_topn_matches(..., min_similarity=0.01)` / `get_topn_spec_idx_and_similarity(..., min_similarity=0.1)` are *return* floors, not identification cutoffs. 0.12 sits just above the 0.1 return floor. https://msentropy.readthedocs.io/en/latest/entropy_search_api.html
- matchms `FlashSimilarity` / entropy module default: spectral entropy, `tolerance=0.02`, `noise_cutoff=0.01` — already live. It does not set a 0.05 identification floor. https://matchms.readthedocs.io/en/development/api/matchms.similarity.entropy.html
- Huber, van der Hooft et al. — *MS2DeepScore* (J Cheminform 2021) and Huber et al. — *Spec2Vec* (PLOS Comput Biol 2021). Embeddings correlate better with Tanimoto than cosine, but need offline weights. https://jcheminf.biomedcentral.com/articles/10.1186/s13321-021-00558-4 · https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1008724
- MS2Query (de Jonge, Huber, van der Hooft — Nature Communications 2023). Scores >0.7 are generally reliable; **<0.6 are often discarded**. Our live hybrid floor of 0.05 is an order of magnitude below that practice. https://www.nature.com/articles/s41467-023-37446-4
- Wang, Li et al. — *Entropy-based decoy generation methods for accurate FDR estimation* (bioRxiv 2023). Ion-entropy decoys show that unfiltered library search at loose FDR still admits a large false-positive fraction; a 0.05 hybrid floor has no FDR control. https://doi.org/10.1101/2023.07.02.547371
- GNPS library search defaults still require cosine ≥0.5 and ≥6 matched peaks — also far above 0.05. https://ccms-ucsd.github.io/GNPSDocumentation/librarysearch/
- Analog / community public notebooks: Flexonafft / midx exact-dedup-fill still badge **0.479**; heliosli `casmi26-0.481` badges **0.481**. Analog / fingerprint / two-engine fusion, not a 0.05 admission floor. https://www.kaggle.com/code/baidalinadilzhan/casmi26-midx-exact-dedup-fill-0-479 · https://www.kaggle.com/code/heliosli/casmi26-0-481
- Public analog / ICEBERG+GLACIER fusion notebooks remain the 0.45–0.48 cluster (Analog Propagation V43 at 0.456; Gluzdov attributed pipeline). They do not use a 0.05 hybrid admission floor. https://www.kaggle.com/code/prvsiyan/analog-propagation-casmi-2026-baseline · https://www.kaggle.com/datasets/dmitriigluzdov/casmi26-attributed-v4g-reproduction-assets
- CLIST standings (re-fetched 12:04Z; page updated ~2h earlier): **Shehab 0.54**, Savko **0.52**, Parfionov **0.52**, democat **0.51**, pikachu / CHU1PC **0.50**. Community analog notebooks still badge **0.479–0.481**. https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/

## Methods to consider

| ID | Method | Why | How it could raise MRR@25 | Fit (notebook, internet off) |
|----|--------|-----|---------------------------|------------------------------|
| **P0** | Raise `MIN_SIMILARITY` 0.05→0.12 | Live floor is below every literature identification cutoff. `retrieve_for_spectrum` admits any hybrid score ≥0.05 into `TOP_K_SPECTRA=120`, then structure aggregation fills 25 slots with weak decoys. | Drops noisy library hits so true-structure near-matches (and later analog/formula cues) can occupy rank 1–5. | One constant. |
| P1 | `TOP_PEAKS` 128→160 | More fragments after the 1% floor can help entropy on rich spectra. | Already submitted as 11-03 cycle04 (57961369); then undone by 11-04 cycle01. Public score still null. Do not restack on H1. | One constant. Next unused after this merge if 160 stays unscored. |
| P1 | Analog / mass-shift channel | Public 0.33→0.54 gains came from analog transfer / fingerprint / fusion, not from another 0.02 Da replay. | Real path to Class-2; larger than a one-knob slot. | New retrieve path; later cycle. |
| P2 | Entropy ID cutoff 0.55–0.75 | Li/Fiehn and JASMS numbers. | Too aggressive for our hybrid entropy/modcos + cross-library CE; would empty many candidate lists. | Not this slot. |
| P2 | MS2Query / Spec2Vec / MS2Deepscore | Strong analog ranking in literature; public analog notebooks sit at 0.456–0.481. | Heavy offline weights; 9h kernel budget; internet off. | Out of scope this slot. |

## Why this slot is the admission floor

Live main after Actions 11-04 cycle02: `TOP_PEAKS=128`, `PEAK_MZ_TOL=0.02`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, mass-wide 35/80, **`MIN_SIMILARITY=0.05`**. Slot-3 fallback still replays `PEAK_MZ_TOL=0.02` (already live; next unused UTC slot). Slot-4 `H-peaks` currently **resets** `MIN_SIMILARITY` to 0.05, which would undo this ablation. Next unused casmi-loop hourly is **13:00 UTC**.

0.12 is a conservative step: well above the 0.05 noise floor, just above MSEntropy’s 0.1 return floor, and well below Li/Fiehn 0.75, JASMS 0.55, GNPS cosine 0.5, and MS2Query’s “discard below 0.6” band, so recall on cross-instrument near-matches should survive.

## Out of scope this cycle

- Class-3 de novo (retrieval cannot solve it).
- CSV `competitions submit`.
- Dispatching casmi-loop before this patch is on `main` (would waste UTC ticket 3 on already-live `PEAK_MZ_TOL=0.02`).
- Analog / ICEBERG / fingerprint ranker (needs a dedicated implement, not a one-knob slot).
