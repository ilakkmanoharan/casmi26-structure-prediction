# Research 2026-10-07_cycle02

Competition-day slot 2 (Chicago clock starts 01:00 America/Chicago). Notebook-only,
internet-off kernel. Goal: raise public **MRR@25** versus our scored 0.143 ceiling.

## Sources reviewed

1. Li & Fiehn, *Nature Methods* (2021). Spectral entropy outperforms MS/MS dot
   product; entropy similarity is robust to added noise ions; FDR &lt; 10% at
   entropy similarity **0.75**.
   https://www.nature.com/articles/s41592-021-01331-z
2. *Anal. Chem.* / PMC (2025). Noise filtering raises homologous-spectrum
   similarity and cleans molecular networks. A **fixed 5% base-peak cutoff
   can drop nearly half of structurally explainable ions**; a data-dependent
   cutoff near **1–2%** (or a simple intensity-based denoiser) retains
   interpretable fragments without collapsing the network.
   https://pmc.ncbi.nlm.nih.gov/articles/PMC12311886/
3. Xing, Houriet, Fiehn, *Nature Methods* (2025). Spectral Denoising Search
   doubles plasma annotations; robust even when noise ions are &gt;150× true
   fragments. Electronic-noise rule: drop ions that share an identical
   intensity bin too often.
   https://www.nature.com/articles/s41592-025-02646-x
4. GNPS library-search docs. Intensity / SNR filters before cosine; high-confidence
   annotations need cosine &gt; 0.9 *and* balance &gt; 60%.
   https://ccms-ucsd.github.io/GNPSDocumentation/gc-ms-library-molecular-network/
5. Flash Entropy Search default fragment tolerance is **20 mDa** (our live
   `PEAK_MZ_TOL` is still 0.01). Cloud PR #20 (H-peak-mz) is unmerged.

## Methods to consider

| Method | Why | How it could raise MRR@25 |
|--------|-----|---------------------------|
| **Raise `INTENSITY_FLOOR` 0.001→0.01** | Live 0.1% relative floor keeps electronic / chemical noise after max-normalization. Literature 1–2% intensity denoiser removes those ions before entropy/modcos. | Fewer false peak matches → less support for wrong inchikey14s, especially on noisy GNPS/MoNA/MassBank rows. |
| Flash 20 mDa (`PEAK_MZ_TOL` 0.02) | Default of Flash Entropy Search; still unmerged (PR #20). | Next unused after this slot. |
| Higher `MIN_SIMILARITY` (0.12) | Li/Fiehn FDR argument; PRs #11/#12 unmerged. | After a cleaner spectrum, raise the rank gate. |
| Analog / quad-channel rankers | Community notebooks 0.328–0.339; CLIST top now **0.48**. | Out of scope for this one-factor kernel slot. |

## Priority (notebook, internet off)

| Pri | Change | Fit |
|-----|--------|-----|
| **P0** | `INTENSITY_FLOOR = 0.01` | Config-only; applied in `clean_spectrum` after max-norm, before `TOP_PEAKS`. |
| P1 | `PEAK_MZ_TOL = 0.02` | Already specified in unmerged Cloud PR #20. |
| P1 | `MIN_SIMILARITY = 0.12` | After a cleaner peak list. |
| P2 | Learned embedders (MSBERT, Spec2Vec) | Need weights + internet or a new dataset. |

## Out of scope this cycle

- Class-3 de novo / ICEBERG / GLACIER / PubChem join (those drive 0.40+ notebooks).
- Changing `ENTROPY_WEIGHT` (already 0.75 on main; Actions slot-2 no-op).
- CSV `competitions submit`.
- Re-applying live `TOP_PEAKS=128` / mass-wide 35/80.
