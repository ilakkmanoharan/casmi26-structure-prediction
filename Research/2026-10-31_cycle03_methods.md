# Research 2026-10-31_cycle03

Late `0 6 * * *` Cloud cron (01:00 CDT slot) fired at **09:04 UTC**. Next unused cycle on `main` after Actions cycle02 is **cycle03**. Prior Cloud cycle03 PR #50 (07:33Z H-min-sim) stayed draft; 08:00 and 09:00 UTC casmi-loop hours did **not** fire.

## Sources reviewed

- Li, Kind, Fiehn — *Spectral entropy outperforms MS/MS dot product similarity* (Nature Methods 2021). Entropy similarity at **0.75** gave FDR <10% on 37,299 natural-product spectra vs NIST20. https://yuanyue.li/publication/li-spectral-2021/
- de Jonge et al. — *Weighting Low-Intensity MS/MS Ions and m/z Frequency* (JASMS 2024). Optimal **entropy** cutoffs for structure-similar vs dissimilar pairs were **0.55 unweighted / 0.56 weighted**; modified-cosine optima were much higher (0.88 / 0.67). https://doi.org/10.1021/jasms.3c00353
- MSEntropy API — `get_topn_matches(..., min_similarity=0.01)` default is a *return* floor, not an identification cutoff. Production Flash Entropy / matchms workflows still apply a higher admission threshold after search. https://msentropy.readthedocs.io/en/latest/entropy_search_api.html
- matchms `EntropyFlash` — hybrid fragment + neutral-loss matching; default pairing 0.02 Da. https://matchms.readthedocs.io/en/development/api/matchms.similarity.entropy.html
- Analog Propagation public notebook (prvsiyan V43) — public MRR@25 **0.456**. Library cosine/entropy plus analog transfer, not a 0.05 admission floor. https://www.kaggle.com/code/prvsiyan/analog-propagation-casmi-2026-baseline
- CASMI 2026 public-chain notes — 4-channel retrieval (library entropy/cosine + analog + MetFrag-lite + fingerprint) is what moved public scores from ~0.14–0.16 to ~0.33–0.47. Pure library search saturates when weak decoys fill the top-25. https://m0-ar.github.io/casmi-2026/RESEARCH.md
- Pilkwang Kim write-up — analog support is one reranker feature; a weak spectral neighbor should not dominate the candidate list. https://pilkwangkim.github.io/posts/CASMI-2026-From-Mass-Spectra-to-Molecular-Structures/
- CLIST standings (page “updated 14 hours ago” at 09:05Z): Parfionov **0.52**, Savko **0.52**, pikachu / Shehab / CHU1PC **0.50**. https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/

## Methods to consider

| ID | Method | Why | How it could raise MRR@25 | Fit (notebook, internet off) |
|----|--------|-----|---------------------------|------------------------------|
| P0 | Raise `MIN_SIMILARITY` 0.05→0.12 | Live floor is below every literature identification cutoff. `retrieve.search_candidates` admits any hybrid score ≥0.05 into `TOP_K_SPECTRA=120`, then structure aggregation fills 25 slots with weak decoys. | Drops noisy library hits so true-structure near-matches (and later analog/formula cues) can occupy rank 1–5. | One constant. |
| P1 | `TOP_PEAKS` 128→160 | More fragments after the 1% floor can help entropy on rich spectra. | Secondary; only after the admission floor is no longer 0.05. | One constant. |
| P1 | Analog / mass-shift channel | Public 0.33→0.46 gains came from analog transfer, not from another 0.02 Da replay. | Real path to Class-2; larger than a one-knob slot. | New retrieve path; later cycle. |
| P2 | Entropy ID cutoff 0.55–0.75 | Li/Fiehn and JASMS numbers. | Too aggressive for our hybrid entropy/modcos + cross-library CE; would empty many candidate lists. | Not this slot. |

## Why this slot is the admission floor

Live main after Actions 10-31 cycle02: `TOP_PEAKS=128`, `PEAK_MZ_TOL=0.02`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, mass-wide 35/80, **`MIN_SIMILARITY=0.05`**. Slot-2/3 fallbacks still replay `PEAK_MZ_TOL=0.02` (already live). Slot-4 `H-peaks` currently **resets** `MIN_SIMILARITY` to 0.05, which would undo this ablation.

0.12 is a conservative step: well above the 0.05 noise floor, well below Li/Fiehn 0.75 and JASMS 0.55, so recall on cross-instrument near-matches should survive.

## Out of scope this cycle

- Class-3 de novo (retrieval cannot solve it).
- CSV `competitions submit`.
- Dispatching casmi-loop before this patch is on `main` (would spend UTC ticket 3 on already-live `PEAK_MZ_TOL=0.02`).
- Analog / ICEBERG / fingerprint ranker (needs a dedicated implement, not a one-knob slot).
