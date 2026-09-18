# Hypotheses — 2026-09-18 cycle01

Derived from `Research/2026-09-18_cycle01_methods.md` and `Analysis/2026-09-18_cycle01_submission.md`.

## H1 — Restoring peak count recovers entropy/modcos signal (primary)

**Statement:** Raising `TOP_PEAKS` from **5 → 128**, holding every other retrieval constant, increases public MRR@25 relative to kernel v13 because entropy similarity and modified cosine regain fragment-ladder evidence that cycle05 discarded.

**Rationale:** Li & Fiehn (2021) and Flash Entropy Search (2023) remove ions below 1% BPI and otherwise keep the spectrum (`max_peak_num` unlimited or 1000). Five peaks is not a published cleaning rule; it is a ChatGPT/config accident from cycle05. Entropy similarity on 5 ions is nearly a discrete overlap toy, not the NIST20-validated metric.

**Expected MRR direction:** **up** vs 0.143 if later kernels never scored, and **up vs v13** even if v13 scored, because v13’s cleaned spectra are information-poor.

**Failure mode:** Kernel runtime grows (more peaks × mass-window scan). 128 is still far below msentropy’s 1000; cycle05 kernel finished in ~15–17 min, so 128 should stay inside the 50 min poll budget. If many queries still hit only poisoned clones, MRR may stay near 0.143 until analog search exists — but it should not get *worse* than 5 peaks.

## H2 — Five-peak identity checks over-ban true structures

**Statement:** `spectra_identical()` on 5-peak views flags coincidental top-5 matches as exact dups, adding those inchikey14s to the poison ban list and dropping the true molecule from the ranking.

**Rationale:** With 128 peaks, identity requires a much longer fingerprint, so only real test↔train clones are banned (the v0.1 failure mode).

**Not the isolated ablation this slot** (it is a consequence of H1). If H1 lands and MRR is still ~0.14, inspect `n_banned_poisoned` in kernel diagnostics next.

## H3 — Entropy weight 0.70 still untested

**Statement:** `ENTROPY_WEIGHT=0.70` (cycle02, kernel ERROR, never scored) would beat 0.60 once spectra are not truncated to 5 peaks.

**Defer.** Mixing H1 and H3 would confound the slot. Keep 0.60.

## H4 — 1% intensity floor (literature default)

**Statement:** `INTENSITY_FLOOR=0.01` after restoring peak count matches Flash Entropy / msentropy noise removal and may cut decoy fragments.

**Defer** to a later slot so H1 stays one factor.

## Cycle-01 chosen bet

Ship **H1 only**: `TOP_PEAKS=128`. Do not retune ppm, entropy weight, min similarity, or domain priors in this submission.
