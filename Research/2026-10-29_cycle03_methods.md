# Research — 2026-10-29 cycle03

## Goal

Raise public MRR@25 above the v0.1 plateau (**0.143**) toward the live public frontier (~**0.52** on CLIST). This Cloud slot is **04:00 CDT / 09:00 UTC**, the third suggested Chicago-day cadence after Actions spent UTC ticket 1 on a no-op H-top-peaks replay and Cloud cycle02 (PR #41, still draft) already specified the admission-floor ablation. Target: **longer fragment ladder** (`TOP_PEAKS` 128 → 160). One major unused constant vs live main after kernel v167.

## Sources reviewed

1. **Li, Kind, Folz, Vaniya, Mehta, Fiehn — *Nat. Methods* (2021)**  
   [Spectral entropy outperforms MS/MS dot product](https://www.nature.com/articles/s41592-021-01331-z)  
   Entropy similarity beat 42 alternatives on NIST20. Low-abundance fragment ions carry structure-discriminating information, especially for low-entropy small-molecule spectra (S < 3); the paper therefore *weights* those ions rather than discarding them. A hard top-N cap after the 1% noise cut can drop exactly those diagnostic mid-intensity ions.

2. **Li & Fiehn — *Nat. Methods* (2023) / PMC11511675**  
   [Flash Entropy Search](https://pmc.ncbi.nlm.nih.gov/articles/PMC11511675/)  
   Cleaning is: precursor-ion removal, **<1% base-peak noise cut**, then fragment matching inside **±20 mDa**. The algorithm does **not** require a small hard peak cap; speed comes from skipping spectra with no shared ions, not from truncating the ladder. Our live `INTENSITY_FLOOR=0.01` and `PEAK_MZ_TOL=0.02` already match this paper. Remaining mismatch: we still hard-cap at 128 peaks.

3. **ms_entropy `clean_spectrum` defaults**  
   [API: `max_peak_num` defaults to keep all peaks](https://msentropy.readthedocs.io/en/latest/entropy_search_api.html) · [`FlashEntropySearch.search(..., max_peak_num=None)`](https://msentropy.readthedocs.io/en/latest/_modules/ms_entropy/entropy_search/flash_entropy_search.html)  
   After the 1% noise threshold, the reference implementation keeps the full cleaned ladder (`max_peak_num=None` / `-1`). 128 is an arbitrary cap from our v0.2 restore-from-5 step, not a literature default.

4. **Yen, Horlacher, Riffle, et al. — *MCP* (2009)**  
   [A Simulated MS/MS Library for Spectrum-to-spectrum Searching](https://doi.org/10.1074/mcp.m800384-mcp200)  
   BiblioSpec assignments to standard proteins **increased** as the peak budget went 20 → 50 → 100, with little change in decoy hits. That is the same direction as raising `TOP_PEAKS` after a noise floor is already in place.

5. **CASMI / Enveda competition notes**  
   [Kaggle competition](https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra) · [CLIST standings](https://clist.by/standings/enveda-casmi-2026-molecule-id-from-mass-spectra-biology-chemistry-custom-metric-70420499/) · [Pilkwang overview](https://pilkwangkim.github.io/posts/CASMI-2026-From-Mass-Spectra-to-Molecular-Structures/)  
   Metric is MRR@25. Retrieval-only cannot claim Class-3 de novo. Exact test↔train spectrum duplicates in `enveda-180` still poison rank-1 when train labels ≠ GT — exact-dup exclusion stays on.

## Methods to consider

| Priority | Method | Why it can lift MRR@25 | How (notebook, internet off) |
|----------|--------|------------------------|------------------------------|
| **P0 this slot** | **`TOP_PEAKS` 128 → 160** | Live 128 still truncates cleaned ladders that Flash Entropy would keep in full after the 1% floor. Extra mid-intensity ions improve entropy/modcos overlap on fragment-rich NP spectra. | One config constant. Already wired in `casmi26/spectrum.py`. |
| P0 next Actions | `MIN_SIMILARITY` 0.05 → 0.12 | Live 0.05 admits near-random hybrid scores into `top_k`. Cycle02 PR #41 already specified this and is still draft. | Slot-2 fallback this cycle (do **not** change the live constant here — one factor). |
| P2 | CE-aware aggregation / domain prior | Already live; H-domain fallback is a no-op on current `DOMAIN_PRIOR`. | Skip. |
| P2 | MS2Query / Spec2Vec / MS2Deepscore | Public analog notebooks ~0.43–0.46. | Heavy offline weights; internet off. |
| P3 | Formula → candidate DB / de novo | Needed for Class-3 when the structure is absent or labels are poisoned. | Out of scope. Retrieval cannot solve Class-3. |

## Why this slot is the peak ladder, not the admission floor

Actions already burned UTC slot 1 today:

- **H-top-peaks** (`TOP_PEAKS=128`, already live; Kaggle **57756058**, kernel v167 at ~02:33Z)

Cloud cycle02 (PR #41, 06:05Z, still **draft**) already implemented `MIN_SIMILARITY` 0.05 → 0.12. Re-implementing that same constant here would collide with those cycle02 files and confound the next unused factor. This 09:00 UTC slot therefore takes the **next unused real ablation vs live main**: raise the hard cap from 128 to 160 **without** resetting `MIN_SIMILARITY`.

Slot 2’s fallback on `main` is still **H-peak-mz** (`PEAK_MZ_TOL=0.02`, already live). This cycle retargets:

- slot-2 → H-min-sim (`MIN_SIMILARITY=0.12`) so a later hourly run does not replay 0.02
- slot-3 / slot-4 → H-peaks (`TOP_PEAKS=160` only)

## Out of scope this cycle

- CSV `competitions submit` (notebook-only competition).
- Claiming Class-3 de novo is solved by library retrieval.
- Training MS2Deepscore / Spec2Vec inside the kernel.
- Applying `MIN_SIMILARITY=0.12` in `casmi26/config.py` this slot (that is cycle02 / slot-2; one factor here).
- Removing the peak cap entirely (`max_peak_num=None`) — 160 is a bounded step vs 128, not an unbounded kernel-time risk.
