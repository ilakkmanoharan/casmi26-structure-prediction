# Research 2026-10-08_cycle02

Notebook-only, internet-off kernel. Metric: public **MRR@25**. One major factor this slot: fragment **m/z match tolerance** for the entropy / modified-cosine hybrid.

## Sources reviewed

- Li & Fiehn, *Nature Methods* (2021): [Spectral entropy outperforms MS/MS dot product](https://www.nature.com/articles/s41592-021-01331-z). NIST20 / MassBank.us benchmark matched ions at **0.05 Da**. FDR &lt; 10% near entropy similarity **0.75**.
- Flash Entropy Search / `MSEntropy` API: [search defaults](https://msentropy.readthedocs.io/en/latest/entropy_search_api.html) use `ms2_tolerance_in_da=0.02`. Classical entropy similarity [defaults to 0.02 Da](https://msentropy.readthedocs.io/en/latest/classical_entropy_similarity.html) (examples still show 0.05 Da).
- matchms `Entropy`: [default fragment tolerance 0.01 Da](https://matchms.readthedocs.io/en/development/api/matchms.similarity.entropy.html) — tighter than Flash, closer to Orbitrap-only matching.
- Community analog / quad-channel notebooks on the [CASMI 2026 code tab](https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra/code) sit at **0.328–0.339**. Public write-ups (e.g. [gnshx engine notes](https://github.com/gnshx/Enveda-CASMI-2026---Molecule-ID-From-Mass-Spectra)) credit library match + analog / PubChem join for 0.40+; those are out of scope for this retrieval-only kernel.

## Methods to consider

| Method | Why | How it could raise MRR@25 |
| --- | --- | --- |
| **Widen `PEAK_MZ_TOL` 0.01 → 0.02** | Our hybrid calls `entropy_similarity` / `modified_cosine` with `tol=cfg.peak_mz_tol`. Live 0.01 Da is matchms-tight; Flash Entropy Search’s default is **20 mDa**. Mixed GNPS / MassBank / MONA / RIKEN peaks are often centroided worse than 10 mDa. | More true fragment pairs survive `_greedy_match`, so correct structures get higher hybrid scores and move up the top-25. |
| Noise floor `INTENSITY_FLOOR` 0.001 → 0.01 | Li/Fiehn and Flash both drop ions &lt; 1% of base peak. Still unused on `main` (draft PRs #13–#19, #21). | Fewer noise–noise matches; keep for a later slot. |
| Raise `MIN_SIMILARITY` 0.05 → 0.12 | Cuts junk neighbors before molecule aggregation. Draft PRs #11/#12. | Helps precision; risk of empty lists on sparse queries. |
| Analog / formula / PubChem join | How 0.40+ public kernels jump Class-2/3. | Needs extra candidate generation; not a one-constant ablation. |

## Priority (this kernel)

| Pri | Change | Fit |
| --- | --- | --- |
| **P0** | `PEAK_MZ_TOL` 0.01 → **0.02** | One existing constant; literature default; unused on `main`. |
| P1 | `INTENSITY_FLOOR` 0.01 | Next unused lever after this slot. |
| P1 | `MIN_SIMILARITY` 0.12 | After intensity / peak-mz. |
| P2 | Analog / de novo / PubChem | Not this cycle; retrieval does not solve Class-3. |

## Out of scope

- Claiming Class-3 de novo is solved by library retrieval.
- CSV `competitions submit` (notebook-only).
- Re-applying live no-ops: `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, mass-wide 35/80, `TOP_K=120`.
- Repeating yesterday’s Cloud H-intensity PR (#21, still draft).
