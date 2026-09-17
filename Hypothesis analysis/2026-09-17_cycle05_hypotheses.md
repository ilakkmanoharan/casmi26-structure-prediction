# Hypotheses — 2026-09-17 cycle05

Context: exact-dup ban is on; mass window last set to 10 / 15 ppm (cycle04); hybrid still `ENTROPY_WEIGHT=0.55`; only scored public MRR is **0.143**. Leaders ~**0.33**.

## H1 (run this slot) — Entropy-dominant hybrid lifts MRR@25

**Statement:** Raising `ENTROPY_WEIGHT` from **0.55 → 0.70** (`0.70·entropy + 0.30·modified_cosine`) improves public MRR@25 vs the current 0.55 hybrid, with exact-dup exclusion still on and mass tolerances unchanged.

**Why:** Li & Fiehn (2021, 2023) show entropy similarity beats dot-product for small-molecule ID by up-weighting low-abundance fragments. After banning identical leaked rows, remaining candidates are *near* matches where cosine saturates. Cycle02 specified this ablation; kernel v4 ERROR’d, so it is still untested on the LB.

**Expected direction:** public MRR@25 **up** vs 0.143 if the dup-ban + entropy ranking recovers non-identical correct structures; still well below 0.33 if true structures are absent from train.

**Failure mode:** entropy over-rewards noisy peaks → wrong isobars rise; or remaining evidence is still dominated by near-duplicate poisoned neighbors that are not byte-identical. Score stays ~0.14.

## H2 — Mass-window already saturated (do not ablate)

**Statement:** Further `MASS_TOL_PPM` / `MASS_TOL_PPM_BACKFILL` moves (cycle03 5/10, cycle04 10/15) are second-order vs ranking-function error.

**Why:** Two consecutive slots already swept ppm. Changing it again would confound H1.

**This slot:** hold at 10 / 15.

## H3 — More neighbors recover sparse queries (next slot)

**Statement:** `TOP_K_SPECTRA_PER_QUERY` 80 → 120 plus slightly lower `MIN_SIMILARITY` raises Hit@25 when the dup-ban empties the top of the list.

**This slot:** **not** combined with H1.

## H4 — Domain-prior boost on NP libs (later)

**Statement:** Boosting `enveda-np-examples` / `gnps` domain prior helps when spectral scores tie.

**Risk:** re-elevates poisoned enveda-180 neighbors. Defer.

## One major ablation this slot

**H1 only.**

```json
{"ENTROPY_WEIGHT": 0.70}
```

Keep `EXCLUDE_EXACT_DUPLICATES=true`, `MASS_TOL_PPM=10`, `MASS_TOL_PPM_BACKFILL=15`.
