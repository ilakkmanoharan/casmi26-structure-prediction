# Research 2026-10-16_cycle02

Notebook-only, internet-off kernel. One major ablation this slot: **relative intensity noise floor**.

## Sources reviewed

| Source | Why it matters |
| --- | --- |
| Li, Kind, Folz, Fiehn et al., *Nat. Methods* 2021 — [Spectral entropy outperforms MS/MS dot product](https://www.nature.com/articles/s41592-021-01331-z) | Entropy similarity FDR <10% at score 0.75; recommended cleaning before scoring. |
| [msentropy classical entropy docs](https://msentropy.readthedocs.io/en/latest/classical_entropy_similarity.html) | Default `clean_spectra=True` drops ions below **1% of base-peak intensity**. |
| [msentropy R wrapper](https://rdrr.io/cran/msentropy/src/R/msentropy_similarity.R) | `noise_threshold = 0.01` (set `-1` to disable). |
| Li & Fiehn, Flash Entropy Search (Nat. Biotechnol. / CDC stack) — [PDF](https://stacks.cdc.gov/view/cdc/168541/cdc_168541_DS1.pdf) | Ions **<1% of max fragment abundance** are treated as likely non-precursor noise and removed before entropy weighting. |
| Ameria et al., *Anal. Chem.* 2025 — [noise filtering in MS/MS / molecular networks](https://pubs.acs.org/ancham/article/97/29/15873/3615078/Improving-Spectral-Similarity-and-Molecular) | Fixed 1–2% base-peak cutoffs sit near the empirical optimum; 5% is a common but harsher alternative. |
| [matchms `select_by_relative_intensity`](https://matchms.readthedocs.io/en/latest/api/matchms.filtering.peak_processing.select_by_relative_intensity.html) | Community default recipe uses `intensity_from=0.01` even though the library default is 0.0. |
| SIRIUS 6 methods — [library identity + analog search](https://v6.docs.sirius-ms.io/methods-background/) | Cosine on squared intensities, ignore precursor; analog via modified cosine. Too heavy for this kernel, but confirms precursor/noise hygiene. |
| [MS2Query](https://github.com/iomega/MS2Query) | Embedding analog search (MS2DeepScore + RF). Out of scope: extra models, internet off. |
| Community analog/forward notebooks (e.g. [gnshx pipeline](https://github.com/gnshx/Enveda-CASMI-2026---Molecule-ID-From-Mass-Spectra), prvsiyan analog-propagation) | Public ~0.32–0.42 via analog + fingerprint + forward MS/MS. Class-3 de novo is **not** solved by retrieval. |

## Methods to consider

| Method | Why | How it could raise MRR@25 |
| --- | --- | --- |
| **1% relative intensity floor** | Flash Entropy / msentropy default; our live `INTENSITY_FLOOR=0.001` still keeps 0.1%-level ions that entropy treats as noise | Fewer spurious peak matches → cleaner entropy/modcos hybrid ranks |
| 20 mDa fragment tolerance (`PEAK_MZ_TOL=0.02`) | Flash Entropy open-search default | Next unused after this slot (unmerged PRs #20/#22/#24/#26) |
| Analog / adduct-shifted modified cosine | Community jump 0.14 → ~0.33 | Needs ranking features beyond current retrieve loop |
| Spectrum-to-fingerprint + PubChem/COCONUT rerank | Top public ~0.45–0.495 | Extra datasets/weights; not this cycle |
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
