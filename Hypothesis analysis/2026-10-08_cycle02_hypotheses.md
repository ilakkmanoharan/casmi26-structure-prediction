# Hypotheses 2026-10-08_cycle02

## H1 — H-peak-mz (this slot)

**Claim:** Raising `PEAK_MZ_TOL` from 0.01 to **0.02** Da increases true fragment matches between Enveda queries and mixed-resolution library spectra (GNPS / MassBank / MONA / RIKEN), so hybrid entropy+modcos scores on the correct structure rise and MRR@25 moves up.

**Why now:** Flash Entropy Search defaults to 20 mDa; Li/Fiehn benchmarked 50 mDa. Live 10 mDa is matchms-tight and unused as an ablation on `main`. Actions slot 2 would otherwise re-send live `ENTROPY_WEIGHT=0.75`.

**Expected MRR direction:** small **up** on library-present (Class 1/2) queries; near-zero on Class-3.

**Failure mode:** wider bins pair unrelated fragments → decoy scores inflate and true rank falls. Cap is still `MIN_SIMILARITY=0.05` and top-k 120.

## H2 — H-intensity (next unused)

`INTENSITY_FLOOR` 0.001 → 0.01 (Li/Fiehn 1% noise cut). Drafted many times (PRs #13–#19, #21); still not on `main`. Defer until H-peak-mz is submitted.

## H3 — H-min-sim

`MIN_SIMILARITY` 0.05 → 0.12 to drop junk neighbors. Draft PRs #11/#12. Risk: empty candidate lists.

## H4 — analog / formula (not this kernel)

0.40+ public kernels use analog shift + candidate injection. Out of scope for a one-constant retrieval ablation. Does **not** claim Class-3 de novo is solved.

## Chosen ablation

**H1 / H-peak-mz** only: `{"PEAK_MZ_TOL": 0.02}`.
