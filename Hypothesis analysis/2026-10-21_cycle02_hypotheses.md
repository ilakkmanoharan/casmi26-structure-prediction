# Hypotheses — 2026-10-21 cycle02

## H1 — H-peak-mz (this slot)

**Claim.** Raising `PEAK_MZ_TOL` from **0.01 Da (10 mDa)** to **0.02 Da (20 mDa)** aligns fragment matching with Flash Entropy / matchms FlashSimilarity and recovers CE / instrument *m/z* shifts, improving public MRR@25 versus the 0.143 plateau.

**Mechanism.** `retrieve._rank_library_hits` calls `hybrid_similarity(..., tol=cfg.peak_mz_tol)`. Both entropy similarity and modified cosine use `_greedy_match`, which requires `|mz_a − mz_b| ≤ tol` (or the precursor-shift equivalent). A 15 mDa offset — common when mixing timsTOF queries with Orbitrap / QTOF library peaks — currently fails at 0.01 and succeeds at 0.02. Cleaning (`INTENSITY_FLOOR=0.01`, `TOP_PEAKS=128`) and the hybrid mix (`ENTROPY_WEIGHT=0.75`) stay fixed, so this is one major factor.

**Expected MRR direction.** Small positive if true-structure ions were being dropped by the tight window; near-zero if most true matches already sit inside 10 mDa. Failure mode: more coincidental peak matches, more analog decoys in the top 25, MRR flat or down. That is acceptable to measure — it is a real ablation, unlike replaying `ENTROPY_WEIGHT=0.75`.

**Major factor vs previous submission.** Previous ticket (57464825) was H-top-peaks with no live-config change. This slot changes peak pairing.

## H2 — H-min-sim (next unused if H1 merges)

**Claim.** `MIN_SIMILARITY` 0.05 → 0.12 discards low-confidence library hits that currently pad rank lists.

**Failure mode.** Empty candidate lists on sparse queries; more placeholder / fallback molecules.

## H3 — H-peaks-160

**Claim.** `TOP_PEAKS` 128 → 160 keeps more mid-intensity fragments after the 1% floor.

**Failure mode.** Extra noise ions survive on dense spectra and inflate decoy similarity.

## H4 — (rejected this slot) H-entropy / H-intensity / H-domain

Already live on main. Would waste UTC ticket 2.

## This slot

Run **H1 only**. `config_patch: {"PEAK_MZ_TOL": 0.02}`.
