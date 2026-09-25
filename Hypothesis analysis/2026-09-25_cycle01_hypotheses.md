# Hypotheses 2026-09-25_cycle01

Built from `Research/2026-09-25_cycle01_methods.md` and `Analysis/2026-09-25_cycle01_submission.md`.

## H1 — Fragment-ladder restore (major ablation this slot)

**Statement.** Increasing `TOP_PEAKS` from 5 to 128 raises public MRR@25 versus the cycle05/`main` kernel, because entropy + modified cosine recover diagnostic ions that a 5-peak spectrum discards.

**Expected direction.** MRR@25 **up** from the last scored 0.143 (and from any unscored 5-peak submit). Ceiling still well below the 0.425 analogue-ranker LB top — this is retrieval repair, not de novo.

**Failure mode.** Extra noise ions dilute entropy similarity (Li et al. showed robustness, but our cleaner is not identical to MSEntropy). Runtime grows with peak count; must stay inside the ~20 min kernel / 70 min Actions budget. If GT is almost never in the library after the exact-dup ban, MRR stays flat.

## H2 — Entropy weight only helps after the ladder exists

**Statement.** Moving `ENTROPY_WEIGHT` to 0.70 while `TOP_PEAKS=5` cannot express Li & Fiehn’s advantage.

**This slot.** Do **not** change `ENTROPY_WEIGHT`. Revisit after H1 is scored.

## H3 — Process hypothesis (Actions 429)

**Statement.** If `_openai_json` returns `None` on HTTP 429 instead of raising, slot 1 uses the deterministic `{TOP_PEAKS: 128}` fallback and `casmi-loop` can reach `kernels push` + `competition_submit_code`.

**Expected.** Next Actions hour on a tree that includes this fallback submits instead of dying in `write_cycle_docs`.

**Failure mode.** Other errors (Kaggle 401, kernel ERROR, push to `main` rejected) still block a score.

## H4 — Analogue / multi-channel ranking (later)

**Statement.** Public 0.39–0.425 scores come from analogue expansion + multi-evidence ranking (MS2Query-like), not from tighter ppm alone.

**This slot.** Out of scope (new architecture). Do not claim Class-3 de novo is solved.

## Ablation chosen

**H1 only:** `TOP_PEAKS=128`. Keep `EXCLUDE_EXACT_DUPLICATES=True`, `ENTROPY_WEIGHT=0.6`, mass tols unchanged.
