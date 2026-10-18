# Hypotheses — 2026-10-18 cycle03

## H1 — H-intensity (this slot)

**Claim.** Raising `INTENSITY_FLOOR` from **0.001 (0.1%)** to **0.01 (1%)** of the base peak, matching Flash Entropy / ms_entropy `noise_threshold=0.01`, will drop isolation-window junk before entropy/modcos hybrid scoring and improve public MRR@25 versus the 0.143 plateau.

**Mechanism.** `clean_spectrum` already normalizes to max intensity, then keeps `inten >= intensity_floor`, then takes `TOP_PEAKS` (128). A 1% cut removes the lowest decade of relative ions that Li/Fiehn treat as noise, so the 128-peak ladder is spent on real fragments. Index and retrieve both call this cleaner, so library and query stay consistent.

**Expected MRR direction.** Small positive if decoy similarities were noise-inflated; near-zero if the remaining 128 peaks already dominate the score. Failure mode: sparse true spectra lose the last diagnostic ions below 1% and recall drops (MRR down). That is acceptable to measure — it is a real ablation, unlike replaying `ENTROPY_WEIGHT=0.75`.

**Major factor vs previous submission.** Previous ticket (57341340) was H-entropy with no live-config change. This slot changes the spectrum object.

## H2 — H-peak-mz (next unused if H1 merges)

**Claim.** `PEAK_MZ_TOL` 0.01 → 0.02 aligns fragment matching with Flash Entropy’s ~20 mDa window and recovers CE / instrument shifts.

**Failure mode.** More coincidental peak matches, more analog decoys in the top 25.

## H3 — H-min-sim

**Claim.** `MIN_SIMILARITY` 0.05 → 0.12 discards low-confidence library hits that currently pad rank lists.

**Failure mode.** Empty candidate lists on sparse queries; more placeholder / fallback molecules.

## H4 — (rejected this slot) H-mass-wide / H-domain

Already live on main. Would waste UTC ticket 3.

## This slot

Run **H1 only**. `config_patch: {"INTENSITY_FLOOR": 0.01}`.
