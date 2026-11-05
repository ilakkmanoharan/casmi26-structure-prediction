# Research — 2026-11-05 cycle02

## Goal

Raise public MRR@25 above the last scored retrieval baseline (**0.143**) toward the live public leaderboard top (**Shehab Alshehabi 0.54** on CLIST, snapshot ~4 h stale at 2026-11-05T12:04Z). Chicago competition day **2026-11-05** is open (01:00 America/Chicago = 07:00 UTC). Actions already spent UTC ticket 1 at 06:06Z (`TOP_PEAKS=128`, Kaggle **58012064**, kernel v195) *before* the Chicago day start. The next unused one-factor ablation on `origin/main` is the **hybrid similarity floor**.

Live knobs after that submit: `TOP_PEAKS=128`, `PEAK_MZ_TOL=0.02`, `INTENSITY_FLOOR=0.01`, `ENTROPY_WEIGHT=0.75`, mass-wide 35/80 ppm, `TOP_K=120`, **`MIN_SIMILARITY=0.05`**. Replaying `PEAK_MZ_TOL=0.02` (current slot-2/3 fallbacks) is a no-op.

## Sources reviewed

1. **Li, Kind, Folz, Vaniya, Mehta, Kind & Fiehn, Nature Methods (2021)** — Spectral entropy outperforms MS/MS dot product; entropy beat 42 alternatives on 434,287 spectra vs NIST20; on 37,299 experimental natural-product spectra, **FDR < 10% at entropy similarity 0.75**. That 0.75 is an *identity-level* cutoff, not a neighbor-admission floor.  
   https://www.nature.com/articles/s41592-021-01331-z · https://yuanyue.li/publication/li-spectral-2021/
2. **Li & Fiehn, Nature Methods (2023)** — Flash Entropy Search: identity / open / neutral-loss / hybrid entropy search at library scale. Default fragment tolerance **0.02 Da**.  
   https://www.nature.com/articles/s41592-023-02012-9 · https://github.com/YuanyueLi/FlashEntropySearch
3. **ms_entropy `get_topn_matches`** — official helper takes `min_similarity` and drops library rows below it before top-N. The documented example uses **0.01** as a near-zero noise gate (keep anything that is not a numerical tie at 0). That is the role of our `MIN_SIMILARITY`, not Li's 0.75 identity operating point.  
   https://msentropy.readthedocs.io/en/latest/entropy_search_useful_functions.html
4. **msentropy / mums2 defaults** — `ms2_tolerance_in_da=0.02`, `noise_threshold=0.01`, `max_peak_num=100`. Confirms the peak-ladder / 20 mDa / 1% floor stack already live on main.  
   https://cran.r-project.org/web/packages/msentropy/refman/msentropy.html · https://www.mums2.org/mums2/reference/spec_entropy_params.html
5. **Morehouse, Mojdehi, Codreanu, Sherrod, McLean, JASMS (2024)** — weighting low-intensity ions and m/z frequency. Unweighted cosine returns the most matches above 0.9; at looser gates (0.5 / 0.7) weighted entropy / fidelity drop weak ties and keep structurally related hits. A **0.5 identity threshold** empties ~10% of 25k queries; that is far too aggressive for our hybrid mix.  
   https://doi.org/10.1021/jasms.3c00353
6. **ChemRxiv 2024 comparative continuous similarity measures** — ROC evaluation of Shannon/Tsallis entropy vs cosine; authors emphasize **dataset-specific** thresholds rather than transferring NIST 0.75 blindly.  
   https://doi.org/10.26434/chemrxiv-2024-5fm7t
7. **de Jonge et al., Nature Communications (2023)** — MS2Query (Spec2Vec + MS2DeepScore + precursor + RF). Needed when GT is absent from the library (Class-2/3). Internet-off kernel cannot pull those weights this slot.  
   https://www.nature.com/articles/s41467-023-37446-4
8. **Live public LB (CLIST, updated ~4 h before this cycle)** — Shehab **0.54**, Savko **0.52**, Parfionov **0.52**, democat **0.51**, pikachu / Biernat / CHU1PC **0.50**. Community analog/fusion notebooks sit ~0.46–0.50. Gap vs 0.143 is not another `PEAK_MZ_TOL` replay.  
   https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/  
   https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra/leaderboard

## Methods to consider

| Priority | Method | Why it can lift MRR@25 | How (this kernel) |
|----------|--------|------------------------|-------------------|
| **P0** | **Raise `MIN_SIMILARITY` 0.05 → 0.12** | `retrieve.py` admits every hybrid score `>= cfg.min_similarity` into the per-query top-120, then structure-aggregates to 25 SMILES. Hybrid is `0.75·entropy + 0.25·modcos`. A decoy with entropy 0.05 and cosine 0.08 scores ~0.057 and currently occupies a top-25 slot. At 0.12 those near-zero ties drop; a plausible analog (entropy 0.20 / cosine 0.15 → ~0.19) still enters. Flash Entropy's documented `min_similarity=0.01` is a numerical noise gate; 0.12 is a slightly stricter gate after 20 mDa pairing already landed, not Li's 0.75 identity cutoff (which would empty most CE-shifted NP lists). | One existing constant. |
| P0 | Keep exact-dup IK ban + structure-level mass filter | v0.1 failure: exact `enveda-180` spectrum copies with train labels ≠ GT (~0.143). | Already on. |
| P1 | Tighten `MASS_TOL_PPM` 35 → 10 | After the floor is raised, a 35 ppm window still floods the index range with isobaric decoys. | Next unused real ablation. |
| P1 | Pure entropy (`ENTROPY_WEIGHT` 0.75 → 1.0) | Li 2021's metric without the 0.25 cosine mixer. Draft Cloud PR #73; never scored. | After H-min-sim is *submitted*, not just drafted. |
| P2 | Flash Entropy C-extension identity+open search | Same metric, faster full-library open/neutral-loss. | Needs `ms-entropy` wheel in the offline dataset. |
| P2 | MS2Query / MS2DeepScore analogue channel | How 0.46–0.54 notebooks score Class-2. | Heavy weights; internet-off; not this slot. |
| P3 | Formula → candidate DB / de novo | Class-3 only. Retrieval cannot claim this is solved. | Out of scope. |

## Why this cycle is the similarity floor, not another peak-m/z tweak

Actions 11-05 cycle01 restored `TOP_PEAKS=128`. `PEAK_MZ_TOL=0.02` and `ENTROPY_WEIGHT=0.75` are already live. Slot-2/3 fallbacks still say `PEAK_MZ_TOL=0.02`. If this PR is not merged before the next unused `casmi-loop` hour, UTC ticket 2 is another no-op. Cloud drafts #62–#75 already specified H-min-sim and stayed unmerged — the lever is still unused on main.

`MIN_SIMILARITY=0.12` sits between Flash Entropy's 0.01 noise gate and Li 2021's 0.75 identity FDR point. It is the smallest unused change that actually filters the candidate list.

## Out of scope this cycle

MS2Query / Spec2Vec / MS2DeepScore weights; Flash Entropy C-extension; unconstrained LLM SMILES; claiming Class-3 de novo is solved by library retrieval; CSV `competitions submit`.
