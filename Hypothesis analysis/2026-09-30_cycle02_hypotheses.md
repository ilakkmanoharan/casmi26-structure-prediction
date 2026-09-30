# Hypotheses — 2026-09-30 cycle02

## H1 (this slot) — 1% intensity floor

**Claim:** Raising `INTENSITY_FLOOR` from `0.001` to `0.01` (msentropy / Li–Fiehn default) removes noise ions that currently inflate the 0.25 modified-cosine term and steal slots in the 128-peak ladder, so true library hits move up in the top-25 and public MRR@25 rises.

**Why this one:** It is the only unused `casmi26/config.py` constant that is both literature-aligned and not already live. `ENTROPY_WEIGHT=0.75`, `TOP_PEAKS=128`, and mass-wide 35/80 already sit on main. Cloud PR #13 tried this yesterday and never merged; Actions then wasted UTC slot 2 on a no-op `H-entropy`.

**Expected MRR direction:** Up vs 0.143 if noise was promoting decoys into ranks 1–5. Flat if publicScore stays unpublished (recent code submits have null scores). Down if genuine low-intensity diagnostic fragments (NP glycosides, in-source fragments) are required for the remaining true hits.

**Failure mode:** Spectra with a huge base peak and chemically informative 0.2–0.8% ions lose those ions; analog-ish true neighbors drop below `MIN_SIMILARITY`. Exact-dup ban can also change if “identity” was noise-driven.

## H2 — Tighter min similarity (next unused)

`MIN_SIMILARITY` 0.05 → 0.12. Drops junk from the 25-list. Cloud PRs #11/#12 never merged. Run only after H1 is scored.

## H3 — Real domain-prior shift

`H-domain` fallback currently writes the same 1.0 / 1.0 / 0.85 already in `DOMAIN_PRIOR`. A real boost would raise `gnps`/`riken` and cut `enveda-180` so poisoned synthetic drugs rank lower. Separate from cleaning.

## H4 — Analog / MS2Query channel (not this kernel)

Leaders (~0.46) and public analog notebooks (~0.33) add fingerprint / candidate-DB rankers. Retrieval-only cannot close the Class-3 gap. Out of scope until extra offline datasets are attached.

## Slot decision

Run **H1 only**. One major factor. `config_patch: {"INTENSITY_FLOOR": 0.01}`.
