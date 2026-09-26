# Hypotheses — 2026-09-26 cycle02

## H1 — Entropy-dominant hybrid (THIS SLOT)

**Statement.** Raising `ENTROPY_WEIGHT` from 0.6 → **0.75** (hybrid = `0.75·entropy + 0.25·modified_cosine`) will move true structures up the MRR@25 list on queries where cosine ties noisy or CE-shifted library spectra, without changing the mass window or peak ladder.

**Why.** Li et al., *Nat. Methods* (2021) report FDR < 10% at entropy similarity **0.75** on natural-product MS/MS. Our kernel already computes entropy similarity; the mix has been stuck at 0.6 through all scored and pending submits. Draft Cloud PRs asked for 0.70 but never landed a Kaggle score.

**Expected MRR direction.** Up vs 0.143 if non-identical entropy neighbors outrank cosine-saturated decoys. Neutral if public scoring is still delayed. Down if the remaining 0.25 cosine term was the only thing keeping analog-ish hits in the top-25.

**Failure mode.** Entropy under-weights diagnostic high-intensity fragments after `_entropy_weights`; sparse 2–3 peak spectra collapse. Mitigant: keep modified cosine at 0.25 and `MIN_SIMILARITY=0.05`.

## H2 — Domain-prior NP boost (next unused)

Boost `enveda-np-examples` / `enveda-180` / `gnps` priors. Soft re-rank only; does not change who enters the candidate pool. Weaker than H1.

## H3 — Higher similarity floor (later slot)

`MIN_SIMILARITY` 0.05 → 0.12. Drops weak decoys; risk of empty candidate lists on sparse queries.

## H4 — Flash Entropy / MS2Query (not this kernel)

Needs extra wheels or embeddings. Out of scope for a one-constant ablation.

## Ablation this slot

**Run H1 only.** `config_patch = {"ENTROPY_WEIGHT": 0.75}`.
