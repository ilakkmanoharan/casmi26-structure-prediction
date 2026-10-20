# Hypotheses — 2026-10-20 cycle02

## H1 — H-peak-mz (this slot)

**Claim.** Raising `PEAK_MZ_TOL` from **0.01 Da (10 mDa)** to **0.02 Da (20 mDa)**, matching Flash Entropy / ms_entropy `ms2_tolerance_in_da=0.02`, will recover true fragment pairs after CE / instrument / centroid error and improve public MRR@25 versus the 0.143 plateau.

**Mechanism.** `hybrid_similarity` already passes `tol=cfg.peak_mz_tol` into both `entropy_similarity` and `modified_cosine`. Those call `_greedy_match` with that window. Live 10 mDa is half the literature default; ions shifted ~12–18 mDa currently miss. Widening to 20 mDa lets the 0.75 entropy / 0.25 modcos hybrid credit the same fragments Flash Entropy would match, without changing cleaning (`INTENSITY_FLOOR=0.01`, `TOP_PEAKS=128`).

**Expected MRR direction.** Small positive if true library neighbors were under-scored by missed fragment pairs. Failure mode: more coincidental peak matches, more analog decoys in the top 25 (MRR down). That is acceptable to measure — it is a real ablation, unlike replaying `ENTROPY_WEIGHT=0.75`.

**Major factor vs previous submission.** Previous ticket (57421540) was H-top-peaks with no live-config change. This slot changes the similarity match window.

## H2 — H-min-sim (next unused if H1 merges)

**Claim.** `MIN_SIMILARITY` 0.05 → 0.12 discards low-confidence library hits that currently pad rank lists.

**Failure mode.** Empty candidate lists on sparse queries; more placeholder / fallback molecules.

## H3 — H-peaks-160

**Claim.** `TOP_PEAKS` 128 → 160 keeps more of the cleaned ladder after the 1% intensity floor.

**Failure mode.** Extra noise ions after the floor dilute entropy.

## H4 — (rejected this slot) H-entropy / H-intensity / H-domain

Already live on main. Would waste UTC ticket 2.

## This slot

Run **H1 only**. `config_patch: {"PEAK_MZ_TOL": 0.02}`.
