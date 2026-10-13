# Hypotheses — 2026-10-13 cycle02

## H1 (this slot) — H-intensity

Raising `INTENSITY_FLOOR` from **0.001 → 0.01** (Flash Entropy `noise_threshold` / matchms 1% relative cut) removes isolation-window junk from both queries and library spectra. Entropy/modcos then compare real fragments. **Expected MRR@25: up**, especially on noisy ESI-MS/MS queries where sub-1% peaks currently steal `TOP_PEAKS=128` slots.

**Failure mode:** true low-abundance diagnostic ions (e.g. 1–2% glycosidic / diagnostic losses) get dropped, sparse spectra lose neighbors, Hit@25 falls. Revert to 0.001.

## H2 — H-peak-mz (next unused)

`PEAK_MZ_TOL` 0.01 → 0.02 matches the Flash Entropy 20 mDa fragment window. Still unused on main (draft PRs #20/#22/#24/#26). Do **not** combine with H1 this slot.

## H3 — H-min-sim

`MIN_SIMILARITY` 0.05 → 0.12 after the noise cut, so weak chance matches do not fill the 25-candidate list. Draft PRs #11/#12.

## H4 — do not resubmit H-entropy

`ENTROPY_WEIGHT=0.75` is already live. Another slot-2 entropy submit is a wasted ticket (H1 is the replacement).

## Slot choice

Run **H1 only**. Config patch: `{"INTENSITY_FLOOR": 0.01}`. Keep exact-dup ban, entropy 0.75, mass-wide 35/80, `TOP_PEAKS=128`.
