# Hypotheses — 2026-10-30 cycle02

## H1 — H-min-sim (run this slot)

**Claim.** Raising `MIN_SIMILARITY` from **0.05** to **0.12** drops low-confidence hybrid library hits that currently pad the top-25, improving public MRR@25 versus the 0.143 plateau.

**Mechanism.** `retrieve.py` admits a library spectrum when `sim >= cfg.min_similarity` *before* truncating to `TOP_K_SPECTRA_PER_QUERY=120` and aggregating to 25 structures. At 0.05, near-noise entropy/modcos ties fill that list. Li/Fiehn (2021) place a 10% FDR *call* near entropy similarity 0.75; GNPS-style identity search typically starts near 0.5–0.7. **0.12** is a conservative step: high enough to drop junk, low enough that sparse-but-real Class-1 hits still enter. Other live knobs stay fixed (`PEAK_MZ_TOL=0.02`, `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`).

**Expected MRR direction.** Small-to-moderate positive if decoy padding is the bottleneck; near-zero if true-structure scores already sit well above 0.12. Failure mode: true structures whose best library hit is in (0.05, 0.12) fall out of the rank list (MRR down, possibly empty lists on sparse queries). That is acceptable to measure — it is a real ablation, unlike replaying `PEAK_MZ_TOL=0.02`.

## H2 — TOP_PEAKS 128 → 160 (next unused)

**Claim.** A longer ladder after the 1% intensity floor can keep diagnostic mid-intensity ions.

**Why not now.** Confounds H1: more peaks plus a tighter score floor moves two knobs. Measure the floor first. Slot-3/4 fallback after this PR is `TOP_PEAKS=160` only (do not reset `MIN_SIMILARITY`). Yesterday cycle04 already tried 160; today’s cycle01 restored 128, so 160 is still a real next ablation.

## H3 — Replay PEAK_MZ_TOL=0.02 (do not run)

Already live. Slot-2 fallback today would waste UTC ticket 2 on it unless this PR retargets that fallback.

## H4 — Analog / MS2Deepscore (out of scope)

Needs extra wheels or embeddings. Out of scope for a one-constant ablation. Do not claim Class-3 de novo is solved by retrieval.

## One major ablation this slot

Run **H1 only**. `config_patch: {"MIN_SIMILARITY": 0.12}`.
