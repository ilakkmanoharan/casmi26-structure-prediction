# Hypotheses — 2026-10-27 cycle02

## H1 — H-min-sim (run this slot)

**Claim.** Raising `MIN_SIMILARITY` from **0.05** to **0.12** drops low-confidence entropy/modcos library hits that currently pad `top_k` and the MRR@25 list, improving public MRR@25 versus the 0.143 plateau.

**Mechanism.** `search_spectra` only appends a library row when `hybrid_similarity(...) >= cfg.min_similarity`. At 0.05, after the live 20 mDa pair window, many decoy spectra clear the floor and occupy the 120-spectrum / 25-candidate budgets. Li & Fiehn (2021) treat entropy similarity ≳ 0.75 as the FDR-aware operating point; 0.12 is a one-factor step toward that regime without emptying sparse queries. Exact-dup inchikey14s stay banned.

**Expected MRR direction.** Small-to-moderate positive if the top-25 is decoy-saturated; near-zero if true structures already sit above 0.12. Failure mode: true-structure near-matches that only score 0.05–0.12 fall out and lists go empty on sparse queries (MRR down). That is acceptable to measure — it is a real ablation, unlike replaying `PEAK_MZ_TOL=0.02`.

## H2 — TOP_PEAKS 128 → 160 (next unused / slot-3 fallback)

**Claim.** A longer ladder after the 1% intensity floor can keep diagnostic mid-intensity ions.

**Why not now.** Confounds H1. Slot-3 fallback after this cycle tries 160 **without** resetting `MIN_SIMILARITY`.

## H3 — Replay PEAK_MZ_TOL=0.02 (do not run)

Already live (Actions 10-26 cycle02/03 and kernel v158 pairing). Slot-2 fallback on main still points here; retarget it so the next hourly cron cannot waste UTC ticket 2.

## H4 — Analog / MS2Deepscore (out of scope)

Needs extra wheels or embeddings. Out of scope for a one-constant ablation. Do not claim Class-3 de novo is solved by retrieval.

## One major ablation this slot

Run **H1 only**. `config_patch: {"MIN_SIMILARITY": 0.12}`.
