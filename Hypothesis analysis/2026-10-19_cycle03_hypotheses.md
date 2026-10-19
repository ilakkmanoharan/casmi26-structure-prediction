# Hypotheses — 2026-10-19 cycle03

## H1 — H-peak-mz (this slot)

**Claim.** Raising `PEAK_MZ_TOL` from **0.01 Da (10 mDa)** to **0.02 Da (20 mDa)**, matching Flash Entropy / ms_entropy `ms2_tolerance_in_da=0.02`, will recover true fragment pairs that currently miss and improve public MRR@25 versus the 0.143 plateau.

**Mechanism.** `hybrid_similarity` passes `cfg.peak_mz_tol` into `modified_cosine` and `entropy_similarity`, both of which call `_greedy_match(..., tol)`. A 15 mDa CE/centroid shift currently fails to pair at 10 mDa and succeeds at 20 mDa, so entropy and modified cosine both rise for the true library neighbor without changing mass windows or the candidate pool.

**Expected MRR direction.** Small positive if true spectra were under-matched across instruments/CEs; near-zero if most true pairs already sit inside 10 mDa. Failure mode: more coincidental peak matches, analog decoys enter the top 25, MRR stays flat or drops. That is acceptable to measure — it is a real ablation, unlike replaying `ENTROPY_WEIGHT=0.75` or `INTENSITY_FLOOR=0.01`.

**Major factor vs previous submission.** Previous tickets 57376181 (H-top-peaks) and 57385301 (H-entropy) made no live-config change. This slot changes peak pairing.

## H2 — H-min-sim (next unused if H1 merges)

**Claim.** `MIN_SIMILARITY` 0.05 → 0.12 discards low-confidence library hits that currently pad rank lists (Li/Fiehn entropy FDR work).

**Failure mode.** Empty candidate lists on sparse queries; more placeholder / fallback molecules.

## H3 — H-peaks 160

**Claim.** `TOP_PEAKS` 128 → 160 keeps more fragments after the live 1% intensity cut.

**Failure mode.** Extra noise peaks if the 1% floor is still too low on some libraries; kernel runtime grows.

## H4 — (rejected this slot) H-entropy / H-intensity / H-domain

Already live on main. Would waste UTC ticket 3 (H-intensity) or the in-flight ticket 2 (H-entropy).

## This slot

Run **H1 only**. `config_patch: {"PEAK_MZ_TOL": 0.02}`.
