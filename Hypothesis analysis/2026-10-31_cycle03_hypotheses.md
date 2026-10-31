# Hypotheses 2026-10-31_cycle03

## H1 — H-min-sim (this slot)

Raising `MIN_SIMILARITY` from 0.05 to 0.12 drops weak hybrid decoys from `search_candidates` so true-structure near-matches rank higher in the top-25.

- **Expected MRR:** up vs 0.143 if decoys currently occupy rank 1–5; flat if most public molecules already lack a ≥0.12 library hit.
- **Failure mode:** cross-instrument / CE-mismatched true hits sit in 0.05–0.12 and disappear. 0.12 is well below Li/Fiehn 0.75 and JASMS 0.55, so this is the conservative first step.
- **Config:** `{"MIN_SIMILARITY": 0.12}`

## H2 — H-peaks (next unused after H1)

`TOP_PEAKS` 128→160 after the 1% intensity floor. Only after the admission floor is live; do **not** reset `MIN_SIMILARITY`.

## H3 — H-peak-mz (already live)

`PEAK_MZ_TOL=0.02` is on main after Actions cycle02. Replaying it wastes a ticket.

## H4 — analog / fingerprint (later)

Public 0.33→0.52 path. Not a one-knob slot; do not claim Class-3 de novo is solved by retrieval.

## Chosen ablation

**H1 / H-min-sim.** One major factor vs live main. Retarget Actions slot-2/3 → H-min-sim, slot-4 → H-peaks (`TOP_PEAKS=160` only).
