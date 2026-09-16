# Hypotheses — 2026-09-16 cycle01

Derived from `Research/2026-09-16_cycle01_methods.md` and `Analysis/2026-09-16_cycle01_submission.md`.

## H1 — Entropy-dominant hybrid (MAJOR ABLATION this slot)

**Statement:** Raising `ENTROPY_WEIGHT` from **0.55 → 0.70** (hybrid ≈ `0.70·entropy + 0.30·modified_cosine`), with exact-duplicate exclusion still on, improves public MRR@25 vs the last *scored* kernel (v0.1 cosine-only, 0.143) and vs the unscored v0.2 0.55 hybrid.

**Rationale:** Li & Fiehn (Nat. Methods 2021) show entropy similarity outperforms cosine for library ID; Bittremieux (JASMS 2022) still supports keeping some modified cosine for analog/CE-shift cases. After removing sim=1.0 poisoned hits, ranking lives in the near-match regime. This is the same bet as 2026-09-15 cycle02, which **did not produce a Kaggle code submission**.

**Expected MRR direction:** **↑** vs 0.143 if v0.2 already removed rank-1 poisoning; modest additional lift vs 0.55 hybrid. Still far from 0.332 unless coverage/formula methods land later.

**Failure mode:** Entropy overweight hurts analog-heavy queries; or v0.2 already entropy-saturated → flat. If the kernel errors again, score is undefined (treat as infrastructure miss, not a negative of H1).

## H2 — Keep exact-dup exclusion (control, not ablated)

**Statement:** Turning `EXCLUDE_EXACT_DUPLICATES` off would collapse toward v0.1 (wrong SMILES at #1).

**Expected:** Do not test off this slot.

## H3 — Kernel status / RDKit bootstrap (infrastructure, not a scoring ablation)

**Statement:** Treating `KERNELWORKERSTATUS.ERROR` as terminal and installing RDKit from `ilakkmanoharan/rdkit-cp312-wheels-casmi26` when needed raises the probability that this slot yields a COMPLETE notebook and therefore a scored submit.

**Failure mode:** Kernel still ERROR for an unrelated reason (frozen kernel, OOM on all-libs index). Then skip `competition_submit_code`.

## H4 — Tighter mass window (later slot)

**Statement:** `MASS_TOL_PPM: 25 → 15` reduces decoys after all-libs indexing. **Not this slot** — kernel v4 already tried a 15/20 ppm pair and never completed.

## Cycle-01 chosen bet

**One major ablation:** **H1** — `config_patch: {"ENTROPY_WEIGHT": 0.70}` only.  
Ship H3 as submit-path hardening so H1 can actually be measured. Reserve H4 and literature-faithful `S&lt;3` entropy reweighting for later Chicago slots.
