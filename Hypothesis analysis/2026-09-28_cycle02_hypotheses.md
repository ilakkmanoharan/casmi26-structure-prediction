# Hypotheses — 2026-09-28 cycle02

## H1 — H-min-sim (this slot)

Raising `MIN_SIMILARITY` from **0.05 → 0.12** drops weak hybrid ties that occupy the top-25 after the exact-dup inchikey14 ban.

- **Mechanism.** `retrieve_for_spectrum` only keeps `sim >= cfg.min_similarity`. A 0.05 floor is far below Li/Fiehn entropy 0.75 (FDR<10%) and below MS2Query’s “discard below ~0.6” guidance. 0.12 is a conservative first step (prior 2026-09-26 cycle02 P1 band 0.12–0.15).
- **Expected MRR.** Up if decoys currently sit above the true structure; flat/down if true remaining neighbors are themselves weak (CE-shifted, sparse peaks) and get filtered.
- **Failure mode.** Sparse 2–3 peak queries produce empty primary lists → backfill at 80 ppm or ethanol placeholder (`CCO`) → those molecules score 0. Mitigant: keep `MASS_TOL_PPM_BACKFILL=80` and do **not** raise the floor to 0.55 this slot.

## H2 — H-entropy (already applied; do not resubmit)

`ENTROPY_WEIGHT=0.75` matches Li 2021’s FDR operating point and is already on main / kernel v28. Slot-2 Actions fallback would be a no-op.

## H3 — H-intensity-floor (later)

Raising `INTENSITY_FLOOR` (0.001 → 0.005) would denoise before matching (Xing 2024). Orthogonal to the similarity *gate*; save for a later unused slot.

## H4 — Analogue / MS2Query channel (out of scope)

Public 0.33+ notebooks use analogue rankers when GT is absent from train. Needs offline embeddings. Not a one-constant ablation.

## This slot

**Run H1 only.** One major factor vs previous submission (`TOP_PEAKS=128` restore).
