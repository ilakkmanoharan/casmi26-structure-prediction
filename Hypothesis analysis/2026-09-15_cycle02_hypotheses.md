# Hypotheses — 2026-09-15 cycle02

Derived from `Research/2026-09-15_cycle02_methods.md` and `Analysis/2026-09-15_cycle02_submission.md`.

## H1 — Entropy-dominant hybrid (MAJOR ABLATION this slot)

**Statement:** Raising `ENTROPY_WEIGHT` from **0.55 → 0.70** (hybrid ≈ `0.70·entropy + 0.30·modified_cosine`) improves public MRR@25 vs the cycle01 0.55 setting, given exact-duplicate exclusion remains on.

**Rationale:** Li & Fiehn (Nat. Methods 2021) show entropy similarity outperforms cosine for library ID; Bittremieux (JASMS 2022) still supports keeping some modcos for analog/CE-shift cases. After removing sim=1.0 poisoned hits, ranking lives in the near-match regime where entropy’s noise robustness and intensity reweighting matter most.

**Expected MRR direction:** **↑** (modest absolute lift if v0.2 already fixed rank-1 poisoning; larger if 0.55 hybrid still over-weights modcos ties).

**Failure mode:** Entropy overweight hurts analog-heavy queries where modcos captures precursor-shifted fragments better → MRR flat or ↓; also possible if entropy implementation differs from Li-style cleaning.

## H2 — Keep exact-dup exclusion (control, not ablated)

**Statement:** Turning `EXCLUDE_EXACT_DUPLICATES` off would collapse back toward v0.1 behavior (wrong SMILES at #1).

**Expected:** Do not test off this slot. Treat as invariant until LB proves otherwise.

## H3 — Tighter mass window (candidate for later slot)

**Statement:** `MASS_TOL_PPM: 25 → 15` (+ backfill 60 → 40) reduces false library hits after all-libs indexing and raises MRR@25.

**Failure mode:** True structures with adduct/ppm edge cases drop out of candidate set → Hit@25 ↓.

## H4 — Broader neighbor pool / CE aggregation (later slot)

**Statement:** `TOP_K_SPECTRA_PER_QUERY: 80 → 120` improves multi-CE support features and mean-top-k similarity, lifting MRR when single-spectrum evidence is ambiguous.

**Failure mode:** Runtime / noise from weak neighbors; diluted scores.

## Cycle-02 chosen bet

**One major ablation:** **H1** — `config_patch: {"ENTROPY_WEIGHT": 0.70}` only.  
Keep `EXCLUDE_EXACT_DUPLICATES=True` and other cycle01 defaults. Reserve H3/H4 for slots 3–4 after v0.2 public score is known.
