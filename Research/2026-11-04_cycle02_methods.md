# Research — 2026-11-04 cycle02

`0 6 * * *` Cloud cron at **06:00 UTC / 00:00 CST**. US DST ended 2026-11-01, so America/Chicago is CST (UTC−6). Chicago competition day **2026-11-03 is still open** (01:00 CST Nov 3 = 07:00 UTC Nov 3 through 01:00 CST Nov 4 = 07:00 UTC Nov 4). Chicago day **2026-11-04 opens in ~1 hour**. UTC calendar 2026-11-04 already has Actions cycle01 (H-top-peaks) on `main`. Next unused cycle on `main` is **cycle02**.

Prior Cloud H-min-sim PRs **#38–#66** stayed draft. After #66 (12:00Z Nov 3), Actions **did** fire three more times and spent those tickets on already-live or immediately-reverted knobs:

- 15:57Z → 11-03 cycle03 H-peak-mz (already-live `PEAK_MZ_TOL=0.02`)
- 21:40Z → 11-03 cycle04 H-peaks (`TOP_PEAKS=160`; a real ablation, public score still null)
- 01:59Z Nov 4 → 11-04 cycle01 H-top-peaks (`TOP_PEAKS=128`, undoing cycle04)

`MIN_SIMILARITY=0.12` has **never** been submitted. Next unused casmi-loop hourly is **07:00 UTC**.

## Sources reviewed

- Li, Kind, Fiehn — *Spectral entropy outperforms MS/MS dot product similarity* (Nature Methods 2021). Entropy similarity at **0.75** gave FDR <10% on 37,299 natural-product spectra vs NIST20. Scores >0.75 are the identification band; our live hybrid floor of 0.05 is not. https://www.nature.com/articles/s41592-021-01331-z · https://pubmed.ncbi.nlm.nih.gov/34857935/
- de Jonge et al. — *Weighting Low-Intensity MS/MS Ions and m/z Frequency* (JASMS 2024). Optimal **entropy** cutoffs for structure-similar vs dissimilar pairs were **0.55 unweighted / 0.56 weighted**; modified-cosine optima were much higher (0.88 / 0.67). https://doi.org/10.1021/jasms.3c00353 · https://pmc.ncbi.nlm.nih.gov/articles/PMC10854760/
- Scheubert, Hufsky, Petras, Wang, Nothias, Dührkop, Bandeira, Dorrestein, Böcker — *Significance estimation for large scale metabolomics annotations by spectral matching* (Nature Communications 2017). Spectral-match FDR is threshold-dependent; GNPS community four-star annotations at cosine **0.7** were ~91% correct. A 0.05 floor is far below that operating point. https://www.nature.com/articles/s41467-017-01318-5
- Li & Fiehn — *Flash Entropy Search* (Nature Methods 2023). After the 1% noise cut, fragment pairing uses **±20 mDa**. That window is already live (`PEAK_MZ_TOL=0.02`). https://doi.org/10.1038/s41592-023-02012-9 · https://github.com/YuanyueLi/FlashEntropySearch
- MSEntropy API — `search(..., ms2_tolerance_in_da=0.02, noise_threshold=0.01)` is the live pairing/noise pair. `get_topn_matches(..., min_similarity=0.01)` / `get_topn_spec_idx_and_similarity(..., min_similarity=0.1)` are *return* floors, not identification cutoffs. 0.12 sits just above the 0.1 return floor. https://msentropy.readthedocs.io/en/latest/entropy_search_api.html
- matchms `FlashSimilarity` default: `score_type="spectral_entropy"`, `tolerance=0.02`, `noise_cutoff=0.01` — already live. It does not set a 0.05 identification floor. https://matchms.readthedocs.io/en/latest/_modules/matchms/similarity/FlashSimilarity.html
- Huber, van der Hooft et al. — *MS2DeepScore* (J Cheminform 2021) and Huber et al. — *Spec2Vec* (PLOS Comput Biol 2021). Embeddings correlate better with Tanimoto than cosine, but need offline weights. https://jcheminf.biomedcentral.com/articles/10.1186/s13321-021-00558-4 · https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1008724
- MS2Query (de Jonge, Huber, van der Hooft — Nature Communications 2023). Scores >0.7 are generally reliable; **<0.6 are often discarded**. Our live hybrid floor of 0.05 is an order of magnitude below that practice. https://www.nature.com/articles/s41467-023-37446-4
- GNPS library search defaults still require cosine ≥0.5 and ≥6 matched peaks — also far above 0.05. https://ccms-ucsd.github.io/GNPSDocumentation/librarysearch/
- Analog / community public notebooks: Flexonafft / midx exact-dedup-fill still badge **0.479**; heliosli `casmi26-0.481` badges **0.481**; prvsiyan Analog Propagation V43 is **0.456**. Analog / fingerprint / two-engine fusion, not a 0.05 admission floor. https://www.kaggle.com/code/baidalinadilzhan/casmi26-midx-exact-dedup-fill-0-479 · https://www.kaggle.com/code/heliosli/casmi26-0-481
- CLIST standings (re-fetched 06:05Z; page updated ~17h earlier): **Shehab 0.53**, Savko **0.52**, Parfionov **0.52**, democat **0.51**, pikachu / CHU1PC **0.50**. Community analog notebooks still badge **0.479–0.481**. https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/

## Methods to consider

| ID | Method | Why | How it could raise MRR@25 | Fit (notebook, internet off) |
|----|--------|-----|---------------------------|------------------------------|
| **P0** | Raise `MIN_SIMILARITY` 0.05→0.12 | Live floor is below every literature identification cutoff. `retrieve_for_spectrum` admits any hybrid score ≥0.05 into `TOP_K_SPECTRA=120`, then structure aggregation fills 25 slots with weak decoys. | Drops noisy library hits so true-structure near-matches (and later analog/formula cues) can occupy rank 1–5. | One constant. |
| P1 | `TOP_PEAKS` 128→160 | More fragments after the 1% floor can help entropy on rich spectra. | Already submitted as 11-03 cycle04 (57961369); then undone by 11-04 cycle01. Public score still null. Do not restack on H1. | One constant. Next unused after this merge if 160 stays unscored. |
| P1 | Analog / mass-shift channel | Public 0.33→0.53 gains came from analog transfer / fingerprint / fusion, not from another 0.02 Da replay. | Real path to Class-2; larger than a one-knob slot. | New retrieve path; later cycle. |
| P2 | Entropy ID cutoff 0.55–0.75 | Li/Fiehn and JASMS numbers. | Too aggressive for our hybrid entropy/modcos + cross-library CE; would empty many candidate lists. | Not this slot. |
| P2 | MS2Query / Spec2Vec / MS2Deepscore | Strong analog ranking in literature; public analog notebooks sit at 0.456–0.481. | Heavy offline weights; 9h kernel budget; internet off. | Out of scope this slot. |

## Why this slot is the admission floor

Live main after Actions 11-04 cycle01: `TOP_PEAKS=128`, `PEAK_MZ_TOL=0.02`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, mass-wide 35/80, **`MIN_SIMILARITY=0.05`**. Slot-2 fallback still replays `PEAK_MZ_TOL=0.02` (already live; next unused UTC slot). Slot-4 `H-peaks` currently **resets** `MIN_SIMILARITY` to 0.05, which would undo this ablation. Next unused casmi-loop hourly is **07:00 UTC**.

0.12 is a conservative step: well above the 0.05 noise floor, just above MSEntropy’s 0.1 return floor, and well below Li/Fiehn 0.75, JASMS 0.55, GNPS cosine 0.5, and MS2Query’s “discard below 0.6” band, so recall on cross-instrument near-matches should survive.

## Out of scope this cycle

- Class-3 de novo (retrieval cannot solve it).
- CSV `competitions submit`.
- Dispatching casmi-loop before this patch is on `main` (would waste UTC ticket 2 on already-live `PEAK_MZ_TOL=0.02`).
- Analog / ICEBERG / fingerprint ranker (needs a dedicated implement, not a one-knob slot).
