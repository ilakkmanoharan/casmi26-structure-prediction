# Hypotheses — 2026-09-24 cycle01

## H1 (this slot) — Fragment-ladder restore

**Claim.** Setting `TOP_PEAKS=128` (from 5) raises public MRR@25 versus the last scored 0.143 baseline, because entropy similarity and modified cosine regain mid-intensity fragment matches that cycle05 discarded.

**Mechanism.** `clean_spectrum` currently keeps five ions on query and library rows. Matched-peak entropy (Li 2021) and modified cosine then have almost no alignment support. 128 peaks is the 2026-09-15 spec value and the unmerged 09-18…09-23 Cloud ablation.

**Expected direction.** MRR@25 **up** (toward 0.20–0.28 if libraries contain the GT; smaller if public GT is mostly out-of-library).

**Failure mode.** Extra noise ions dilute entropy weights; poisoned near-duplicates that are not *exact* after 5-peak truncation become exact at 128 and get banned (good) or, if the ban misses them, rank a wrong IK #1 (bad). Runtime stays inside the ~20 min kernel budget (peak cap is still small).

## H2 — Actions 429 is why quota is unused

**Claim.** Catching OpenAI HTTP 429 and falling back to a deterministic `config_patch` is necessary for *any* post-09-17 code submit. Without it, hourly Actions will keep reporting `kaggle=0` and then crash.

**Expected direction.** Not a score hypothesis. It is the submit-path hypothesis: after merge, the next `casmi-loop` should push a kernel and `competition_submit_code`.

**Failure mode.** Fallback patch is empty / wrong constant name → `implement.py` applies the default `ENTROPY_WEIGHT=0.65` instead of 128 peaks.

## H3 (next slot, not now) — Entropy-dominant hybrid

Raise `ENTROPY_WEIGHT` 0.60 → 0.70 only **after** H1 has a public score. Mixing both changes would confound attribution.

## H4 (later) — Mass-window / ExactMolWt backfill

Widen `MASS_TOL_PPM_BACKFILL` only if H1 scores and diagnostics show empty candidate lists from adduct error — not because cycle03–05 “felt” like mass-tol work (those scores are still null).

## Ablation chosen this slot

**H1 only:** `TOP_PEAKS=128`. Plus the H2 engineering fix so Actions can actually ship H1.

## Out of scope

MS2Query embeddings; de novo generation; claiming Class-3 solved by retrieval.
