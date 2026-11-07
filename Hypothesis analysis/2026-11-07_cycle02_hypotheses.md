# Hypotheses — 2026-11-07 cycle02

## H1 — ENTROPY_WEIGHT 0.75 → 1.0 (this slot)

**Statement.** After Flash Entropy 20 mDa pairing (`PEAK_MZ_TOL=0.02`) is live, dropping the remaining 25% modified-cosine mix so `hybrid_similarity` returns pure Li/Fiehn entropy similarity raises public MRR@25 vs the 0.75 hybrid.

**Mechanism.** `casmi26/retrieve.py` scores every mass-window library row with `hybrid_similarity(..., entropy_weight=cfg.entropy_weight)`. At 0.75 the rank list is a convex combination of entropy (identity-optimal per Li 2021, AUC 0.958 on NIST20) and modified cosine (analogue-oriented; Stein/Scott 1994, GNPS networking, Bittremieux 2022). Flash Entropy identity search does **not** mix cosine: it returns entropy similarity after fragment / unused-peak-loss matching. The 0.25 cosine term can lift CE-shifted decoys that share a few intense ions above true-structure near-matches whose entropy is higher but cosine is lower, especially once poisoned exact-dup InChIKey14s are banned. Setting the mix to 1.0 re-orders the **same** 35 ppm / 120-neighbor pool without changing coverage, peak cleaning, or the 0.05 score floor.

**Expected MRR direction.** Small-to-moderate positive if cosine-promoted decoys currently occupy ranks 1–25; near-zero if entropy and cosine already agree on the live pool. Failure mode: CE-shifted or adduct-shifted *true* structures that entropy under-scores relative to cosine fall out of the top-25 (MRR down). That is acceptable to measure — it is a real ablation, unlike replaying `PEAK_MZ_TOL=0.02`.

**Why now.** Slot-1 today already replayed live `TOP_PEAKS=128`. Unmerged drafts #82 / #83 occupy H-sim-gate and H-mass-tight. Pure entropy is the remaining unused constant that actually changes the score object.

## H2 — MIN_SIMILARITY 0.05 → 0.12 (next unused)

**Statement.** Raising the admission floor after H1 stops packing the top-25 with entropy scores that Li/Fiehn put in the high-FDR regime.

**Why not now.** One major factor per slot. Draft PR #82 already implements this; slot-3 fallback is retargeted to it.

## H3 — MASS_TOL_PPM 35 → 15 (later)

**Statement.** Tightening the primary structure-level window (ibnmarzuk 15 ppm / shiferaxa 8.5 ppm vs live 35 ppm) removes off-formula neighbors from `TOP_K_SPECTRA_PER_QUERY`. Keep `MASS_TOL_PPM_BACKFILL=80`.

**Why not now.** Draft PR #83 already implements 15 ppm; slot-4 fallback is retargeted to it. Do not confound H1 with a smaller candidate pool.

## H4 — Analog / MS2Query channel (out of scope)

Public 0.43–0.54 pipelines use analog Tanimoto or spectrum-to-fingerprint evidence when library identity is poisoned. That is a new ranking channel, not a config constant. Retrieval still does not claim Class-3 de novo.

## One major ablation this slot

**H1** — `config_patch: {"ENTROPY_WEIGHT": 1.0}` only.
