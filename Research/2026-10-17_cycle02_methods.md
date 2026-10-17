# Research 2026-10-17_cycle02

Notebook-only, internet-off kernel. One major ablation this slot: **relative intensity noise floor**.

## Sources reviewed

| Source | Why it matters |
| --- | --- |
| Li, Kind, Folz, Fiehn et al., *Nat. Methods* 2021 — [Spectral entropy outperforms MS/MS dot product](https://www.nature.com/articles/s41592-021-01331-z) | Entropy similarity FDR <10% at score 0.75; recommended cleaning before scoring. |
| Li & Fiehn, *Nat. Methods* 2023 — [Flash Entropy Search](https://www.nature.com/articles/s41592-023-02012-9) ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11511675/)) | Ions **<1% of max fragment abundance** are treated as likely non-precursor noise and removed before entropy weighting. Open-search fragment window is 20 mDa. |
| [msentropy FlashEntropySearch API](https://msentropy.readthedocs.io/en/latest/entropy_search_api.html) | Default `noise_threshold=0.01`: drop peaks with intensity `< noise_threshold * max(intensity)`. |
| [matchms `select_by_relative_intensity`](https://matchms.readthedocs.io/en/stable/api/matchms.filtering.peak_processing.select_by_relative_intensity.html) | Library default `intensity_from=0.0`, but the [tutorial pipeline](https://matchms.github.io/matchms-docs/notebooks/matchms_tutorial_01_building_analysis_pipeline.html) uses `intensity_from=0.01`. |
| Ameria et al., *Anal. Chem.* 2025 — [noise filtering in MS/MS / molecular networks](https://pubs.acs.org/ancham/article/97/29/15873/3615078/Improving-Spectral-Similarity-and-Molecular) | Fixed 1–2% base-peak cutoffs sit near the empirical optimum; 5% is a common but harsher alternative. |
| SIRIUS 6 methods — [library identity + analog search](https://v6.docs.sirius-ms.io/methods-background/) | Cosine on squared intensities, ignore precursor; analog via modified cosine. Too heavy for this kernel, but confirms precursor/noise hygiene. |
| [MS2Query](https://github.com/iomega/MS2Query) | Embedding analog search (MS2DeepScore + RF). Out of scope: extra models, internet off. |
| Community analog/forward notebooks (e.g. [gnshx pipeline](https://github.com/gnshx/Enveda-CASMI-2026---Molecule-ID-From-Mass-Spectra)) | Public ~0.32–0.42 via analog + fingerprint + forward MS/MS. Class-3 de novo is **not** solved by retrieval. |

## Methods to consider

| Method | Why | How it could raise MRR@25 |
| --- | --- | --- |
| **1% relative intensity floor** | Flash Entropy / msentropy default; our live `INTENSITY_FLOOR=0.001` still keeps 0.1%-level ions that entropy treats as noise | Fewer spurious peak matches → cleaner entropy/modcos hybrid ranks |
| 20 mDa fragment tolerance (`PEAK_MZ_TOL=0.02`) | Flash Entropy open-search default | Next unused after this slot (unmerged PRs #20/#22/#24/#26) |
| Analog / adduct-shifted modified cosine | Community jump 0.14 → ~0.33 | Needs ranking features beyond current retrieve loop |
| Spectrum-to-fingerprint + PubChem/COCONUT rerank | Top public ~0.45–0.50 | Extra datasets/weights; not this cycle |
| SIRIUS / CSI:FingerID / MSNovelist | Formula + fingerprint + de novo | Not embeddable internet-off in this kernel |

## Priority (this kernel)

| Pri | Ablation | Fit |
| --- | --- | --- |
| **P0** | `INTENSITY_FLOOR` 0.001 → **0.01** | Config-only; aligns cleaner with entropy we already weight at 0.75 |
| P1 | `PEAK_MZ_TOL` 0.01 → 0.02 | Flash Entropy fragment window |
| P1 | `MIN_SIMILARITY` 0.05 → 0.12 | Drop low-support library hits |
| P2 | Analog / fingerprint / forward models | Score gap vs LB, but not one config constant |

## Out of scope this cycle

- CSV `competitions submit`
- Claiming Class-3 de novo is solved by retrieval
- New constants, extra datasets, internet-on kernels
- Re-running live no-ops: `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, mass-wide 35/80
