# Hypotheses 2026-10-07_cycle02

## H1 — H-intensity (THIS SLOT)

Raising `INTENSITY_FLOOR` from **0.001 → 0.01** (1% of base peak after
max-normalization, before `TOP_PEAKS` truncation) drops electronic / chemical
noise ions that currently enter entropy and modified-cosine greedy matches.

- **Expected MRR direction:** up if noise ions were creating false support for
  wrong inchikey14s; flat if the 0.1% tail was already unused after top-128.
- **Failure mode:** true low-intensity diagnostic fragments (especially
  natural-product side-chain ions) get removed, entropy scores fall, and
  MRR stays 0.143 or dips. 1% is the literature-typical intensity denoiser
  (PMC12311886); 5% would be too aggressive.

## H2 — H-peak-mz (next unused)

`PEAK_MZ_TOL` 0.01 → 0.02 (Flash Entropy 20 mDa). Specified in unmerged
Cloud PR #20. Do **not** combine with H1 on this ticket.

## H3 — H-min-sim (later)

`MIN_SIMILARITY` 0.05 → 0.12 after a cleaner peak list. PRs #11/#12.

## H4 — do not re-run H-entropy

`ENTROPY_WEIGHT` is already 0.75 on main. Slot-2 fallback H-entropy is a
wasted submission.

## Chosen ablation

**H1 / H-intensity only.** One config constant. Rebuild kernel, internet off.
