# Research — 2026-10-02 cycle02

## Goal

Raise public MRR@25 above the last scored retrieval baseline (**0.143**) toward the live public leaderboard top (**GUAM 0.332** on Kaggle as of 2026-10-02T06:05Z; public analog/quad-channel notebooks report **0.33–0.339**). Chicago competition day 2026-10-02 opened at 01:00 CDT. This slot is the first *Chicago-clock* ticket of the day; Actions already burned UTC-day slot 1 at 01:23Z on a no-op `TOP_PEAKS=128` restore (`56763204`). One unused major factor remains: align spectrum cleaning with the Li/Fiehn **1% noise floor**.

## Sources reviewed

1. **Li, Kind, Folz, Vaniya, Mehta, Kind & Fiehn, Nature Methods (2021)** — Spectral entropy similarity outperforms MS/MS dot product; operating point **FDR < 10% at entropy similarity 0.75** on 37,299 natural-product spectra.  
   https://www.nature.com/articles/s41592-021-01331-z · https://doi.org/10.1038/s41592-021-01331-z
2. **Li & Fiehn, Nature Methods (2023) / PMC11511675** — Flash Entropy Search. Cleaning step: “possible fragment ions at **<1% the maximal fragment ion abundance** carry a high probability to stem from other sources than the precursor ion and are removed.” Precursor ions with m/z > (precursor − 1.6 Da) are also dropped.  
   https://www.nature.com/articles/s41592-023-02012-9 · https://pmc.ncbi.nlm.nih.gov/articles/PMC11511675/
3. **ms-entropy API (`clean_spectrum` / `FlashEntropySearch.search`)** — default `noise_threshold=0.01` (peaks with intensity `< 0.01 * max(intensity)` removed). Default fragment tolerance `ms2_tolerance_in_da=0.02`.  
   https://msentropy.readthedocs.io/en/latest/entropy_search_api.html · https://msentropy.readthedocs.io/en/latest/dynamic_basic_usage_search.html
4. **de Jonge et al., Nature Communications (2023)** — MS2Query analogue + exact ranking. Public 0.33+ notebooks use analogue channels; retrieval-only cannot claim Class-3 de novo.  
   https://www.nature.com/articles/s41467-023-37446-4
5. **Live Kaggle public LB + Code (2026-10-02)** — prize-contender top **GUAM 0.332**; CLIST snapshot ~0.33. Community “analog ranker / quad-channel” kernels 0.33–0.339. Our best *scored* public remains **0.143**.  
   https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra/leaderboard · https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/

## Methods to consider

| Priority | Method | Why it can lift MRR@25 | How (this kernel) |
|----------|--------|------------------------|-------------------|
| **P0** | **Raise `INTENSITY_FLOOR` 0.001 → 0.01** | Current cleaner keeps 0.1%-of-max ions that Flash Entropy treats as isolation-window / instrument noise. Those peaks dilute entropy weights and create false modified-cosine matches, especially on poisoned exact-dup neighbors we already skip. Matching the literature 1% floor re-ranks the *same* mass window without changing coverage. | One existing config constant. `clean_spectrum` already applies `inten >= intensity_floor` after max-normalize. |
| P0 | Keep exact-dup IK ban + entropy hybrid 0.75 | v0.1 failure mode unchanged: identical `enveda-180` spectra with train labels ≠ GT. Entropy mix already at Li 2021 0.75. | Already on. |
| P1 | `PEAK_MZ_TOL` 0.01 → 0.02 | Flash Entropy default fragment Da window. Next unused slot. | Config only. |
| P1 | `MIN_SIMILARITY` 0.05 → 0.12 | Drops weak decoys filling top-25. Draft Cloud PRs #11/#12 never merged. | Later slot. |
| P2 | Flash Entropy C-extension / identity+hybrid search | Same metric, faster open search. | Needs `ms-entropy` wheel in the offline dataset. |
| P2 | MS2Query / MS2DeepScore analogue channel | What public 0.33+ notebooks do when GT is absent from train. | Heavy weights; internet-off. |
| P3 | Formula → candidate DB / de novo | Class-3 only. Retrieval cannot claim this is solved. | Out of scope. |

## Why this cycle is intensity floor, not another entropy / peaks / mass tweak

Actions 09-25 through 10-01 already swept **H-top-peaks (128)**, **H-entropy (0.75)**, **H-mass-wide (35/80 + top-k 120)**, **H-peaks (160 / min_sim 0.05)**, **H-domain (no-op prior rewrite)**. All public scores still **null** except the original 0.143. Repeating slot-2 fallback `ENTROPY_WEIGHT=0.75` would be a wasted ticket — that constant is already live on main. Cloud PRs #13/#14/#15 specified `INTENSITY_FLOOR=0.01` but stayed draft; Actions never submitted it. Literature gives a concrete default (1%).

## Out of scope this cycle

MS2Query / Spec2Vec / MS2DeepScore weights; Flash Entropy C-extension; unconstrained LLM SMILES; claiming Class-3 de novo is solved by library retrieval.
