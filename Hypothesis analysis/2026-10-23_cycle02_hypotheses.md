# Hypotheses — 2026-10-23 cycle02

## H1 — H-peak-mz (this slot)

**Claim.** Raising `PEAK_MZ_TOL` from **0.01 Da (10 mDa)** to **0.02 Da (20 mDa)** — Flash Entropy / ms_entropy / matchms default fragment-match window — will recover CE- and instrument-shifted true-structure hits that currently miss the pair window, and will improve public MRR@25 versus the 0.143 plateau.

**Mechanism.** `casmi26/retrieve.py` scores every mass-window library row with `hybrid_similarity(..., tol=cfg.peak_mz_tol)`. Both entropy similarity and modified cosine pair ions only inside that Da window. Live 10 mDa is tighter than Li & Fiehn 2023’s ±20 mDa choice (low-abundance ions already err by ~10 mDa). Widening to 20 mDa increases true-pair recall across GNPS / MassBank / MONA / Enveda libraries without changing mass-ppm gates, peak cleaning, or the 0.75 entropy mix.

**Expected MRR direction.** Small-to-moderate positive if CE-shifted true hits were falling below `MIN_SIMILARITY`; near-zero if 10 mDa already captures the ions that dominate the hybrid score. Failure mode: more coincidental peak matches, more analog decoys in the top 25, MRR flat or down. That is acceptable to measure — it is a real ablation, unlike replaying `ENTROPY_WEIGHT=0.75`.

**Major factor vs previous submission.** Previous ticket (57548841) was H-top-peaks with no live-config change. This slot changes the similarity object.

## H2 — H-min-sim (next unused if H1 merges)

**Claim.** `MIN_SIMILARITY` 0.05 → 0.12 discards low-confidence library hits that currently pad rank lists.

**Failure mode.** Empty candidate lists on sparse queries; more placeholder / fallback molecules.

## H3 — H-peaks-160

**Claim.** `TOP_PEAKS` 128 → 160 keeps more of the 1%-floor ladder for entropy/modcos.

**Failure mode.** Extra mid-intensity noise ions if the 1% floor is already sufficient.

## H4 — (rejected this slot) H-entropy / H-intensity / H-domain

Already live on main (`ENTROPY_WEIGHT=0.75`, `INTENSITY_FLOOR=0.01`, current `DOMAIN_PRIOR`). Would waste UTC ticket 2.

## This slot

Run **H1 only**. `config_patch: {"PEAK_MZ_TOL": 0.02}`.
