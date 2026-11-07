# Research — 2026-11-07 cycle02

## Goal

Raise public MRR@25 above the v0.1 plateau (**0.143**) toward the live public frontier (**0.54** on CLIST). This Cloud slot is the first unused **real** ablation after Actions already spent UTC ticket 1 on a no-op replay of live `TOP_PEAKS=128`. Target: **structure-level precursor / exact-mass window**, not another replay of already-live fragment knobs.

## Sources reviewed

1. **Li, Kind, Folz, Vaniya, Mehta, Fiehn — *Nat. Methods* (2021)**  
   [Spectral entropy outperforms MS/MS dot product](https://www.nature.com/articles/s41592-021-01331-z)  
   Entropy similarity beat 42 alternatives on NIST20. Live mix is already `ENTROPY_WEIGHT=0.75`. Remaining retrieval error is candidate-pool pollution, not mix weight.

2. **Li & Fiehn — *Nat. Methods* (2023) / Flash Entropy Search**  
   [PMC11511675](https://pmc.ncbi.nlm.nih.gov/articles/PMC11511675/) · [ms_entropy API](https://msentropy.readthedocs.io/en/latest/entropy_search_api.html)  
   Fragment pairing default is **±0.02 Da** (already live as `PEAK_MZ_TOL=0.02`). Identity search still gates on precursor *m/z*. A 35 ppm structure window at 400 Da is **±0.014 Da**, several times a timsTOF precursor error; it admits many wrong formulas into the top-25.

3. **de Jonge, Hecht, van der Hooft et al. — *Nat. Commun.* (2023)**  
   [MS2Query analogue search](https://www.nature.com/articles/s41467-023-37446-4)  
   Exact-match library search saturates; analogue / fingerprint channels lift chemical neighbors when the true structure is absent or labels are poisoned. Out of scope for this one-constant slot (needs embeddings). Motivates not packing the 25 slots with off-mass decoys.

4. **ibnmarzuk CASMI baseline (public, 2026)**  
   [ibnmarzuk/casmi26-molecule-id](https://github.com/ibnmarzuk/casmi26-molecule-id)  
   Precursor filter **±15 ppm**, then modified cosine + spectral entropy + RRF. Matches timsTOF-class precursor precision. Our live primary window is **35 ppm** — more than 2× that gate.

5. **shiferaxa CASMI pipeline (public, 2026)**  
   [shiferaxa/casmi26](https://github.com/shiferaxa/casmi26)  
   Neutral mass from precursor+adduct; candidate pool is every structure within **8.5 ppm** of the target mass in ~712k structures. Four evidence channels (library entropy, analog Tanimoto, fragmentation, spectrum-to-fingerprint). Public methods at the 0.5 MRR band use **single-digit to mid-teens ppm**, not 35.

6. **CASMI / Enveda competition notes**  
   [Kaggle competition](https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra) · [CLIST standings](https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/) · [Pilkwang overview](https://pilkwangkim.github.io/posts/CASMI-2026-From-Mass-Spectra-to-Molecular-Structures/)  
   Metric is MRR@25. Retrieval-only cannot claim Class-3 de novo. Exact test↔train spectrum duplicates in `enveda-180` still poison rank-1 when train labels ≠ GT — exact-dup exclusion stays on.

## Methods to consider

| Priority | Method | Why it can lift MRR@25 | How (notebook, internet off) |
|----------|--------|------------------------|------------------------------|
| **P0** | **Primary mass window 15 ppm (`MASS_TOL_PPM` 35 → 15)** | Live 35 ppm index window floods `retrieve_for_spectrum` with off-formula neighbors. ibnmarzuk uses 15 ppm; shiferaxa uses 8.5 ppm. Tightening the *primary* gate (keep `MASS_TOL_PPM_BACKFILL=80` for empty lists) removes decoys from the scored top-k so true near-matches can occupy MRR ranks. | One config constant. Already wired through `index.mass_window` + contradiction penalty in `casmi26/retrieve.py`. |
| P1 | `MASS_TOL_PPM` 15 → 8.5 | Match shiferaxa’s structure pool. Risk: adduct / isotope inference error drops true hits before backfill. | Next unused slot after H-mass-tight if 15 ppm is not too tight. |
| P1 | `MIN_SIMILARITY` 0.05 → 0.12 | Li/Fiehn FDR work implies very low hybrid scores are mostly decoys. | Config only. Do not confound with mass window this slot. |
| P1 | `TOP_PEAKS` 128 → 160 | Tried yesterday as UTC 2026-11-06 cycle04 (Kaggle **58071327**, kernel v201) but GitHub push failed; cycle01 today reset main to 128. | Slot-4 fallback already tries 160. Not this slot. |
| P2 | Analog Tanimoto / MS2Query-style channel | Public 0.43–0.54 pipelines use analog evidence when exact library match is poisoned. | Fingerprints + extra ranking; too large for one hourly kernel change. |
| P2 | MS2Deepscore / Spec2Vec | Strong analog ranking in literature. | Heavy offline weights; internet off. |
| P3 | Formula → candidate DB / de novo | Needed for Class-3 when the structure is absent. | Out of scope. Retrieval cannot solve Class-3. |

## Why this slot is mass-window, not another slot-rotation knob

Actions already burned UTC slot 1 today:

- **H-top-peaks** (`TOP_PEAKS=128`, already live; Kaggle **58076904**, kernel v202 at 02:53Z)

Slot 2’s fallback is **H-peak-mz** (`PEAK_MZ_TOL=0.02`) — also already live since mid-October. Slot 3 is the same no-op. Replaying either wastes UTC tickets 2–3.

`MASS_TOL_PPM=15` was last applied around 2026-09-25, **before** live fragment settings (`PEAK_MZ_TOL=0.02`, `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`). Retrying the tighter window *on top of* those fragment defaults is a new combination, not a no-op.

## Out of scope this cycle

- CSV `competitions submit` (notebook-only competition).
- Claiming Class-3 de novo is solved by library retrieval.
- Training MS2Deepscore / Spec2Vec / analog Tanimoto inside the kernel.
- Changing `MASS_TOL_PPM_BACKFILL` (keep 80 ppm so sparse queries still fill 25 slots).
