# Research 2026-11-01_cycle03

`0 6 * * *` Cloud cron (01:00 America/Chicago / first suggested Cloud cadence) fired late at **09:03 UTC / 03:03 CST**. US DST ended at 02:00 CDT → 01:00 CST. Chicago competition day **2026-11-01** opened at the first 01:00 CDT (06:00 UTC). Prior Cloud cycle02 PRs **#54** (06:03Z) and **#55** (07:34Z) stayed draft. 07:00 and 08:00 UTC `casmi-loop` hours did not fire; **09:00 UTC casmi-loop completed** on `main` (Actions `41291447254` → Kaggle **57867206**, kernel v181) as fallback **H-peak-mz** (`PEAK_MZ_TOL=0.02`, already live). Next unused cycle after that run is **cycle03**.

## Sources reviewed

- Li, Kind, Fiehn — *Spectral entropy outperforms MS/MS dot product similarity* (Nature Methods 2021). Entropy similarity at **0.75** gave FDR <10% on 37,299 natural-product spectra vs NIST20. Scores >0.75 are the identification band; our live hybrid floor of 0.05 is not. https://www.nature.com/articles/s41592-021-01331-z · https://pubmed.ncbi.nlm.nih.gov/34857935/ · https://escholarship.org/content/qt0249w6hk/qt0249w6hk.pdf
- de Jonge et al. — *Weighting Low-Intensity MS/MS Ions and m/z Frequency* (JASMS 2024). Optimal **entropy** cutoffs for structure-similar vs dissimilar pairs were **0.55 unweighted / 0.56 weighted**; modified-cosine optima were much higher (0.88 / 0.67). https://doi.org/10.1021/jasms.3c00353
- Li & Fiehn — *Flash Entropy Search* (Nature Methods 2023 / PMC11511675). After the 1% noise cut, fragment pairing uses **±20 mDa**. That window is already live (`PEAK_MZ_TOL=0.02`). https://pmc.ncbi.nlm.nih.gov/articles/PMC11511675/ · https://doi.org/10.1038/s41592-023-02012-9
- MSEntropy API — `get_topn_matches(..., min_similarity=0.01)` / `get_topn_spec_idx_and_similarity(..., min_similarity=0.1)` are *return* floors, not identification cutoffs. Production Flash Entropy / matchms workflows still apply a higher admission threshold after search. https://msentropy.readthedocs.io/en/latest/entropy_search_useful_functions.html · https://msentropy.readthedocs.io/en/latest/entropy_search_basic_usage.html
- matchms `FlashSimilarity` default: `score_type="spectral_entropy"`, `tolerance=0.02`, `noise_cutoff=0.01` — already live. It does not set a 0.05 identification floor. https://matchms.readthedocs.io/en/stable/api/matchms.similarity.FlashSimilarity.html
- Huber, van der Hooft et al. — *MS2DeepScore* (J Cheminform 2021) and Huber et al. — *Spec2Vec* (PLOS Comput Biol 2021). Embeddings correlate better with Tanimoto than cosine, but need offline weights. https://link.springer.com/article/10.1186/s13321-021-00558-4 · https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1008724
- MS2Query (de Jonge, Huber, van der Hooft — Nature Communications 2023). Scores >0.7 are generally reliable; 0.6–0.7 need caution; **<0.6 are often discarded**. Our live hybrid floor of 0.05 is an order of magnitude below that practice. https://www.nature.com/articles/s41467-023-37446-4
- GNPS library search defaults still require cosine ≥0.5 and ≥6 matched peaks — also far above 0.05. https://ccms-ucsd.github.io/GNPSDocumentation/librarysearch/
- Analog Propagation / community public notebooks (checked ~09:10Z): `CASMI26 LB 0.479 | MIDX Exact Dedup Fill` still badges **0.479**; Flexonafft `CASMI26: Closing the Evidence Gap` V56 also **0.479**; other public forks sit at 0.477. Analog / fingerprint rerank, not a 0.05 admission floor. https://www.kaggle.com/code?tagIds=7402-Chemistry · https://www.kaggle.com/code/flexonafft/casmi26-closing-the-evidence-gap
- CASMI 2026 public-chain notes — 4-channel retrieval (library entropy/cosine + analog + MetFrag-lite + fingerprint) is what moved public scores from ~0.14–0.16 to ~0.33–0.47. Pure library search saturates when weak decoys fill the top-25. https://m0-ar.github.io/casmi-2026/RESEARCH.md
- CLIST standings (page “updated 16 hours ago” at 09:10Z): Savko **0.52**, Parfionov **0.52**, pikachu / Shehab / CHU1PC / democatXamer **0.50**. https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/

## Methods to consider

| ID | Method | Why | How it could raise MRR@25 | Fit (notebook, internet off) |
|----|--------|-----|---------------------------|------------------------------|
| **P0** | Raise `MIN_SIMILARITY` 0.05→0.12 | Live floor is below every literature identification cutoff. `retrieve_for_spectrum` admits any hybrid score ≥0.05 into `TOP_K_SPECTRA=120`, then structure aggregation fills 25 slots with weak decoys. | Drops noisy library hits so true-structure near-matches (and later analog/formula cues) can occupy rank 1–5. | One constant. |
| P1 | `TOP_PEAKS` 128→160 | More fragments after the 1% floor can help entropy on rich spectra. | Secondary; only after the admission floor is no longer 0.05. | One constant. Next unused after this merge. |
| P1 | Analog / mass-shift channel | Public 0.33→0.48 gains came from analog transfer, not from another 0.02 Da replay. | Real path to Class-2; larger than a one-knob slot. | New retrieve path; later cycle. |
| P2 | Entropy ID cutoff 0.55–0.75 | Li/Fiehn and JASMS numbers. | Too aggressive for our hybrid entropy/modcos + cross-library CE; would empty many candidate lists. | Not this slot. |
| P2 | MS2Query / Spec2Vec / MS2Deepscore | Strong analog ranking in literature; public analog notebooks sit at 0.479. | Heavy offline weights; 9h kernel budget; internet off. | Out of scope this slot. |

## Why this slot is the admission floor

Live main after Actions 11-01 cycle02: `TOP_PEAKS=128`, `PEAK_MZ_TOL=0.02`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, mass-wide 35/80, **`MIN_SIMILARITY=0.05`**. Slot-2/3 fallbacks still replay `PEAK_MZ_TOL=0.02` (already live) — 09:00 UTC Actions spent ticket 2 on that no-op (57867206). Slot-4 `H-peaks` currently **resets** `MIN_SIMILARITY` to 0.05, which would undo this ablation.

0.12 is a conservative step: well above the 0.05 noise floor, well below Li/Fiehn 0.75, JASMS 0.55, GNPS cosine 0.5, and MS2Query’s “discard below 0.6” band, so recall on cross-instrument near-matches should survive.

## Out of scope this cycle

- Class-3 de novo (retrieval cannot solve it).
- CSV `competitions submit`.
- Dispatching casmi-loop before this patch is on `main` (09:00 UTC already running H-peak-mz; a second dispatch would race).
- Analog / ICEBERG / fingerprint ranker (needs a dedicated implement, not a one-knob slot).
