# Research 2026-09-25_cycle01 — MS/MS methods that can raise MRR@25

Competition: `enveda-CASMI26-molecule-id-mass-spectra`  
Metric: public **MRR@25**  
Constraint: notebook-only, **internet off**, one major ablation this slot.

## Sources reviewed

- Li, Kind, Folz, Vaniya, Mehta, van der Hooft, Fiehn. *Spectral entropy outperforms MS/MS dot product similarity for small-molecule compound identification.* Nature Methods 18, 1524–1531 (2021). https://www.nature.com/articles/s41592-021-01331-z and PDF https://yuanyue.li/project/spectral_entropy/Yuanyue-spectral_entropy.pdf
- MSEntropy docs (`clean_spectrum`, `max_peak_num`, noise threshold). https://msentropy.readthedocs.io/en/latest/classical_spectral_entropy.html
- `msentropy` R / Python wrappers: default `noise_threshold=0.01`, `max_peak_num` 100–1000, fragment ion matching at ~0.02–0.05 Da. https://cran.r-project.org/web/packages/msentropy/msentropy.pdf
- de Jonge, Huber, Kremer, Rehfeldt, Witting, van der Hooft. *MS2Query: reliable and scalable MS2 mass spectra-based analogue search.* Nature Communications 14 (2023). https://www.nature.com/articles/s41467-023-37446-4
- Enveda CASMI 2026 overview / data / leaderboard (fetched 2026-09-25). https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra/ and https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra/leaderboard
- C&EN: *Metabolomics has a data problem. Could this competition fix it?* (2026-09). https://cen.acs.org/analytical-chemistry/mass-spectrometry/competition-identify-small-molecules-capture/104/web/2026/09
- Public notebooks on the competition Code tab (analog / multi-channel rankers scoring ~0.32–0.34+). https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra/code

## Methods to consider

### 1. Restore a real fragment ladder (`TOP_PEAKS` ≫ 5) — **P0 this slot**

**Why.** Entropy similarity and modified cosine both need the fragment ion series, not just the five tallest peaks. Li & Fiehn’s cleaner keeps ions above ~1% of base peak and does **not** collapse a spectrum to five peaks; MSEntropy’s `max_peak_num` defaults are 100–1000. `clean_spectrum()` already L2-normalizes after a top-N cut. With `TOP_PEAKS=5` (main, cycle05), two true-structure spectra that share a diagnostic mid-intensity ladder can score near zero, so MRR@25 is capped by missing evidence rather than ranking.

**How it improves score.** Restoring 128 peaks (near `clean_spectrum`’s historical default of 64, and below MSEntropy’s 1000) lets entropy/modcos see the same ions the literature scores were designed for. This is the single largest remaining retrieval-knob change on `main`.

### 2. Entropy-dominant hybrid (already partially on) — P1 later

**Why.** Entropy similarity beat 42 alternatives including dot product on NIST20 (Li et al. 2021) and is more robust to noise ions. We already blend entropy + modified cosine (`ENTROPY_WEIGHT=0.6`) with exact-dup exclusion.

**How.** After the peak ladder is restored, a later slot can move `ENTROPY_WEIGHT` toward 0.70–0.80. Doing that *while* `TOP_PEAKS=5` is uninformative.

### 3. Analogue / multi-channel ranking (MS2Query-style) — P1, not this kernel

**Why.** MS2Query ranks analogues without a precursor-mass prefilter, using Spec2Vec / MS2Deepscore + a random forest. Public CASMI notebooks titled “analog ranker” / “quad-channel evidence ranker” sit near 0.33–0.34 on the Code tab, and the live public LB top is now **0.425**. That is far above our last scored 0.143.

**How.** Offline embeddings + analogue expansion could recover structures that are not exact library hits. Out of scope for a one-constant ablation in an internet-off kernel this slot; do not claim Class-3 de novo is solved by retrieval.

### 4. Structure-level exact mass + CE/adduct aggregation — P1 keep

**Why.** CASMI scores per `molecule_id`, not per spectrum. Aggregation across collision energies and adducts is already in `casmi26/retrieve.py`. Tight structure-level mass filters remain useful once spectral evidence is non-degenerate.

### 5. Exact-duplicate / poisoned-label guard — P0 keep (already on)

**Why.** Exact test↔train spectrum copies in `enveda-180` carry train InChIKeys that are **not** competition GT. `EXCLUDE_EXACT_DUPLICATES=True` must stay on.

## Priority table (notebook-only, internet off)

| Pri | Method | Fits this kernel? | This slot? |
|-----|--------|-------------------|------------|
| P0 | Restore `TOP_PEAKS` 5→128 | Yes, existing constant | **Yes — one major ablation** |
| P0 | Keep exact-dup ban | Already on | Keep |
| P1 | Entropy weight 0.70+ | Yes | After peak ladder is scored |
| P1 | Analogue / multi-channel ranker | Needs new code + embeddings | Later |
| P2 | Spec2Vec / MS2Deepscore | Weights + internet or huge local cache | No |
| P2 | Formula → candidate enumeration | Slow / incomplete without web DBs | No |

## Out of scope this cycle

- CSV `competitions submit` (notebook-only competition).
- Claiming Class-3 de novo structure elucidation from library retrieval.
- Training Spec2Vec / MS2Deepscore in the kernel.
- Changing more than one major factor (`TOP_PEAKS` only).
- Merging yesterday’s still-open draft PRs by hand; this cycle re-implements the same P0 on a fresh branch with today’s docs.
