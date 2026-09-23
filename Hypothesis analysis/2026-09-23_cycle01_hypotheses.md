# Hypotheses — 2026-09-23 cycle01

## H1 (this slot) — Restore the fragment ladder

**Claim:** Setting `TOP_PEAKS=128` (from cycle05’s `5`) will raise public MRR@25 relative to kernel v13 / Kaggle 56298621 because entropy similarity and modified cosine both need more than five ions to discriminate near-isobaric NP candidates after exact-dup InChIKeys are banned.

**Mechanism:** Li & Fiehn (2021/2023) show entropy’s gain over cosine comes from low-abundance fragments. `clean_spectrum(..., top_peaks=5)` keeps only the five strongest peaks after the 0.1% intensity floor, so hybrid scores lose the ladder and many true hits fall below `MIN_SIMILARITY=0.08` or rank below decoys.

**Expected MRR direction:** up vs 0.143 / vs unscored v13. Not expected to reach GUAM 0.332 (retrieval still cannot invent missing Class-3 structures).

**Failure mode:** more peaks also admit more noise matches; if `MIN_SIMILARITY` is too low, decoys could fill the top 25. Mitigate by leaving `MIN_SIMILARITY=0.08` and mass windows unchanged so the peak-count effect is isolated.

## H2 — OpenAI 429 is why quota is unused, not Kaggle

**Claim:** Actions 35823205794 counted `kaggle=0` then crashed in `_openai_json`. Catching HTTP 429 / URL errors (return `None` → `FALLBACK_ABLATIONS`) will let later hourly slots submit.

**Failure mode:** fallback patch could disagree with this spec if docs are not on `main` yet. This cycle writes substantial Research/Analysis/Hypothesis so `write_cycle_docs` reuses them and applies `config_patch` from the spec. Slot-1 fallback is also aligned to `TOP_PEAKS=128`.

## H3 (next slot, not now) — Mass window after peaks are restored

Cycle05 also tightened `MASS_TOL_PPM` to 10 / backfill 15. After H1 scores, a **separate** slot should test 20–25 ppm + wider backfill if coverage is thin.

## One major ablation this slot

**H1 only:** `TOP_PEAKS` 5 → 128. Do not change entropy weight or mass tolerances in the same submit.
