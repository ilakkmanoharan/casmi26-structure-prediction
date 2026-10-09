# Hypotheses 2026-10-09_cycle02

Built from `Research/2026-10-09_cycle02_methods.md` and `Analysis/2026-10-09_cycle02_submission.md`.

## H1 — 1% intensity floor (major ablation this slot)

**Statement.** Raising `INTENSITY_FLOOR` from 0.001 to 0.01 raises public MRR@25 versus the live kernel, because `clean_spectrum` then matches Li/Fiehn and MSEntropy’s 1% base-peak noise cut before the 128-peak cap, so entropy/modcos stop matching electronic / chemical noise ions to the wrong inchikey14.

**Expected direction.** MRR@25 **up** from the last scored 0.143 (and from any unscored 0.1%-floor submit). Ceiling still well below the 0.48 analogue-ranker LB top — this is retrieval denoising, not de novo.

**Failure mode.** True fragments between 0.1% and 1% of base peak disappear; sparse natural-product spectra become emptier and rank the true structure worse. If GT is almost never in the library after the exact-dup ban, MRR stays flat. A 5% floor would be worse (literature: drops ~half of explainable ions) — we stay at 1%.

## H2 — Entropy weight is already saturated

**Statement.** `ENTROPY_WEIGHT=0.75` is already on `main` (Li/Fiehn FDR&lt;10% threshold). Re-submitting H-entropy wastes a daily ticket.

**This slot.** Do **not** change `ENTROPY_WEIGHT`. Retarget Actions slot-2 away from H-entropy.

## H3 — Peak m/z tolerance is a different factor

**Statement.** `PEAK_MZ_TOL` 0.01→0.02 (Flash Entropy 20 mDa) is the next unused matching-tolerance lever (unmerged PR #22). Combining it with the intensity floor would confound the ablation.

**This slot.** Leave `PEAK_MZ_TOL=0.01`. Revisit after H1 is scored.

## H4 — Analogue / multi-channel ranking (later)

**Statement.** Public 0.33–0.48 scores come from analogue expansion + multi-evidence ranking (MS2Query-like), not from a 0.1% vs 1% floor.

**This slot.** Out of scope (new architecture). Do not claim Class-3 de novo is solved.

## Ablation chosen

**H1 only:** `INTENSITY_FLOOR=0.01`. Keep `EXCLUDE_EXACT_DUPLICATES=True`, `TOP_PEAKS=128`, `ENTROPY_WEIGHT=0.75`, mass-wide 35/80, `PEAK_MZ_TOL=0.01`, `MIN_SIMILARITY=0.05`.
