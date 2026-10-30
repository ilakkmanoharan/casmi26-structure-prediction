# Hypotheses — 2026-10-30 cycle03

## H1 — H-min-sim (run this slot)

**Claim.** Raising `MIN_SIMILARITY` from **0.05** to **0.12** drops low-confidence hybrid library hits that currently pad the top-25, improving public MRR@25 versus the 0.143 plateau.

**Mechanism.** `retrieve.py` admits a library spectrum when `sim >= cfg.min_similarity` *before* truncating to `TOP_K_SPECTRA_PER_QUERY=120` and aggregating to 25 structures. At 0.05, near-noise entropy/modcos ties fill that list. Li/Fiehn (2021) place a 10% FDR *call* near entropy similarity 0.75; GNPS-style identity search typically starts near 0.5–0.7. **0.12** is a conservative step: high enough to drop junk, low enough that sparse-but-real Class-1 hits still enter. Other live knobs stay fixed (`PEAK_MZ_TOL=0.02`, `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`).

**Expected direction.** Public MRR@25 **up** if decoys currently occupy ranks 1–25; **flat** if true hits already score ≫ 0.12; **down** if sparse true structures sit in 0.05–0.12.

**Failure mode.** Empty or short candidate lists on noisy/sparse queries, so MRR@25 falls. Revert to 0.05. Do not jump to 0.5/0.75 in the same slot.

## H2 — TOP_PEAKS 128 → 160 (next unused)

**Claim.** Keeping 160 cleaned peaks after the 1% intensity floor recovers mid-ladder diagnostic ions that 128 drops.

**Why not now.** Confounds H1: more peaks plus a tighter score floor moves two knobs. Measure the floor first. Slot-4 fallback after this PR is `TOP_PEAKS=160` only (do not reset `MIN_SIMILARITY`). Yesterday cycle04 already tried 160; today’s cycle01 restored 128, so 160 is still a real next ablation.

## H3 — domain prior / H-domain (skip)

**Claim.** Boosting `enveda-np-examples` / `enveda-180` / `gnps` would lift NP queries.

**Why not now.** Those priors are already 1.0 / 1.0 / 0.85. Slot-5 H-domain is a no-op.

## H4 — replay PEAK_MZ_TOL=0.02 (do not run)

Already live, and Actions just spent UTC ticket 2 on it (kernel v172 / 57799491). Slot-3 fallback is still this no-op until this PR retargets it.

## Ablation this slot

Run **H1 only**. `config_patch: {"MIN_SIMILARITY": 0.12}`.
