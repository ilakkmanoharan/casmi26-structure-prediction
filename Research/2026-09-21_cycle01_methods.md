# Research 2026-09-21_cycle01 — MS/MS methods for MRR@25

Competition: [enveda-CASMI26-molecule-id-mass-spectra](https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra/).  
Kernel constraint: notebook-only, **internet off**, RDKit from `ilakkmanoharan/rdkit-cp312-wheels-casmi26`.

## Sources reviewed

| Source | Why it matters for this slot |
| --- | --- |
| Li & Fiehn, *Flash entropy search…*, Nat Methods 2023, [doi:10.1038/s41592-023-02012-9](https://doi.org/10.1038/s41592-023-02012-9) | Entropy similarity + library cleaning: drop precursor-region ions, drop peaks below ~1% BPI, centroid-merge, **keep up to ~100 peaks** (or unlimited). |
| `ms_entropy` docs: [clean_spectrum / search](https://msentropy.readthedocs.io/en/latest/entropy_search_api.html), [basic usage](https://msentropy.readthedocs.io/en/latest/entropy_search_basic_usage.html) | Default `noise_threshold=0.01`, `max_peak_num` typically 100 or unset — never 5. |
| [FlashEntropySearch GitHub](https://github.com/YuanyueLi/FlashEntropySearch) | Confirms the cleaning order used in production entropy search. |
| de Jonge et al., *MS2Query*, Nat Commun 2023, [doi:10.1038/s41467-023-37446-4](https://www.nature.com/articles/s41467-023-37446-4) | Modified cosine + Spec2Vec/MS2Deepscore analogue search; exact-match still uses a **precursor mass window**, not a 5-peak spectrum. |
| SIRIUS 6 [methods](https://v6.docs.sirius-ms.io/methods-background/) | Library identity search uses cosine on **full fragment sets** (precursor ignored); analogue uses modified cosine. |
| Fiehn Lab [CASMI 2022](https://fiehnlab.ucdavis.edu/casmi) | Structure ID is still formula → candidates → ranking; retrieval alone is not Class-3 de novo. |
| Kaggle LB [competition leaderboard](https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra/leaderboard) | Public top **GUAM 0.332** (2026-09-21); our last scored public is **0.143**. |

## Methods to consider

### 1. Restore fragment-ion count (`TOP_PEAKS` 5 → 128) — this slot

**Why.** Kernel v13 / Kaggle 56298621 (2026-09-17 cycle05) set `TOP_PEAKS=5`. Entropy similarity and modified cosine both score matched *ions*. Five peaks:

- discards the diagnostic ladder Li/Fiehn keep above 1% BPI;
- coarsens exact-duplicate detection (`spectra_identical` compares cleaned arrays), so poisoned enveda-180 dups may slip through or true near-dups may be over-merged;
- makes `INTENSITY_FLOOR=0.001` almost irrelevant because the cap already throws away mid-intensity fragments.

**How it raises MRR@25.** More true fragment matches → higher entropy/modcos for the correct InChIKey14 vs near-isobars inside the 10–15 ppm mass window. This is a one-knob ablation against the last *submitted* kernel.

Flash Entropy’s own cleaner keeps `max_peak_num` around 100 (docs) with `noise_threshold=0.01`. Our `INTENSITY_FLOOR=0.001` is already stricter than 1% BPI; 128 peaks is the documented pre-cycle05 setting (2026-09-15 cycle02 spec) and sits next to ms_entropy’s 100.

### 2. Entropy-dominant hybrid (`ENTROPY_WEIGHT` 0.70)

Still un-scored (2026-09-15 cycle02 kernel ERROR). Valid **after** the fragment ladder is restored; otherwise entropy is computed on 5 ions.

### 3. Mass-window / neighbor count

Cycle03–05 already moved `MASS_TOL_PPM` 5→10 and backfill 10→15. Public scores for those submits are still **null**. Do not restack ppm until 56298621 / 56290985 / 56290242 score or we restore peaks.

### 4. MS2Query / Spec2Vec / MS2Deepscore / SIRIUS CSI:FingerID

Strong methods, **out of scope this slot**: no internet, no pretrained embeddings in the attached dataset, SIRIUS is not a pip wheel we ship.

## Priority (notebook, internet off)

| Pri | Method | Fit |
| --- | --- | --- |
| **P0** | `TOP_PEAKS=128` (restore vs v13) | Config-only; matches Flash Entropy peak budget |
| P1 | `ENTROPY_WEIGHT=0.70` | Next slot after peaks are live |
| P1 | Keep `EXCLUDE_EXACT_DUPLICATES=True` | Poisoned exact-dup IKs in enveda-180 |
| P2 | Domain prior boost gnps/riken | Only after similarity is on a real spectrum |
| P2 | Wider `TOP_K_SPECTRA_PER_QUERY` | Cost vs sparse queries |

## Out of scope this cycle

- Claiming Class-3 de novo from retrieval.
- CSV `competitions submit`.
- Training Spec2Vec/MS2Deepscore in-kernel.
- Changing mass ppm **and** peaks in the same slot.
