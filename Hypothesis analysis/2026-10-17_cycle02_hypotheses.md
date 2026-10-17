# Hypotheses 2026-10-17_cycle02

## H1 — 1% relative intensity floor (this slot)

**Claim:** Raising `INTENSITY_FLOOR` from 0.001 to 0.01 removes noise ions that currently match library peaks and dilute entropy/modcos hybrid ranks.

**Why now:** Live kernel already uses `ENTROPY_WEIGHT=0.75` (Li/Fiehn FDR<10% threshold) but still scores with a 0.1% floor. Flash Entropy / msentropy default is 1%. This is the unused P0 config ablation; prior Cloud H-intensity PRs (#13–#19, #21, #23, #25, #27–#30) never merged.

**Expected MRR direction:** Small **up** if noise matches currently outrank true fragments; **flat/down** if true low-intensity diagnostic ions (esp. NP libraries) get dropped.

**Failure mode:** Sparse queries lose too many peaks and fall back to mass-only neighbors (wrong IK14s, including remaining poisoned-adjacent hits).

## H2 — 20 mDa fragment window (next unused)

`PEAK_MZ_TOL` 0.01 → 0.02 (Flash Entropy open-search default). Independent of H1. Unmerged PRs #20/#22/#24/#26.

## H3 — Raise `MIN_SIMILARITY` to 0.12

Drop weak library hits that fill the @25 list. Unmerged PRs #11/#12.

## H4 — Analog / fingerprint / forward (not this kernel slot)

Needed to approach 0.45+ public. Out of scope for one config constant. Do not claim Class-3 de novo is solved by retrieval.

## Slot decision

**Run H1 only.** `config_patch: {"INTENSITY_FLOOR": 0.01}`. Also retarget Actions slot-2 fallback so a merge before 07:00 UTC spends the next ticket on this ablation instead of the live ENTROPY_WEIGHT=0.75 no-op.
