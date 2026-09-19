# Hypotheses — 2026-09-19 cycle01

## H1 (run this slot) — Fragment-ladder restore

**Statement:** Raising `TOP_PEAKS` from **5 → 128**, holding every other cycle05 constant, increases public MRR@25 because entropy and modified-cosine retrieval regain diagnostic ions that Li/Fiehn keep above ~1% BPI.

**Mechanism:** `clean_spectrum` currently keeps only the five strongest peaks. That (a) starves hybrid similarity of the fragment ladder and (b) makes exact-dup IK bans unreliable after the same aggressive clean.

**Expected direction:** MRR@25 **up** vs 0.143 if the kernel finishes and is scored. Even a small lift is a successful ablation.

**Failure mode:** More peaks add noise / decoy matches (`MIN_SIMILARITY=0.08` still admits weak hits) or push kernel runtime. If MRR falls, next slot try `TOP_PEAKS=100` (msentropy default) or raise `INTENSITY_FLOOR` to 0.01.

## H2 — Actions 429 is why Sep 18 had zero submits

**Statement:** casmi-loop will produce a Kaggle code submit on this Chicago day if `_openai_json` returns `None` on HTTP 429/5xx instead of raising.

**Not a scoring ablation.** Required so H1 can actually be uploaded.

## H3 (next slot, do not stack) — Entropy-dominant hybrid

**Statement:** After peaks are restored, `ENTROPY_WEIGHT=0.70` (cycle02, never scored) should beat 0.60 for identity ranking (Li & Fiehn).

## H4 (later) — Peak-match window

**Statement:** `PEAK_MZ_TOL` 0.02–0.05 Da (literature) recovers CE-shifted fragments that 0.01 Da misses.

## One major ablation this slot

**H1 only:** `TOP_PEAKS=128`. Keep `EXCLUDE_EXACT_DUPLICATES=True`, `ENTROPY_WEIGHT=0.6`, mass-tol 10/15 ppm.
