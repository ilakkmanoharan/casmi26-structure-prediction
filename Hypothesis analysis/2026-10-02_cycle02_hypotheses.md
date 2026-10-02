# Hypotheses — 2026-10-02 cycle02

## H1 — Li/Fiehn 1% intensity floor (THIS SLOT)

**Statement.** Raising `INTENSITY_FLOOR` from 0.001 → **0.01** (drop fragment ions below 1% of the base peak after max-normalization) will move true structures up the MRR@25 list on queries where 0.1%-level noise currently creates false entropy / modified-cosine matches, without changing the mass window, peak-count cap, or hybrid mix.

**Why.** Li & Fiehn, *Nat. Methods* (2023) remove ions <1% of max fragment abundance before entropy search; `ms-entropy` defaults `noise_threshold=0.01`. Our cleaner is 10× more permissive. After the exact-dup IK ban, remaining neighbors are compared on noisy peak ladders — the leftover 0.1% ions are the cheapest unused ranking lever.

**Expected MRR direction.** Up vs 0.143 if noise peaks were inflating decoy similarity. Neutral if public scoring stays delayed. Down if true NP fragments live in the 0.1–1% band and get dropped (sparse 2–4 peak spectra).

**Failure mode.** Over-cleaning sparse or low-SNR query spectra empties the peak list or collapses hybrid similarity below `MIN_SIMILARITY=0.05`. Mitigant: keep `TOP_PEAKS=128` and the 0.05 similarity floor; backfill mass window stays 80 ppm.

## H2 — Flash Entropy fragment Da window (next unused)

`PEAK_MZ_TOL` 0.01 → 0.02 (ms-entropy default `ms2_tolerance_in_da`). Changes matching, not cleaning. Hold for a later slot so this ticket is one-factor.

## H3 — Higher similarity floor (later slot)

`MIN_SIMILARITY` 0.05 → 0.12. Draft Cloud PRs #11/#12. Drops weak decoys; risk of empty candidate lists. Do not stack with H1.

## H4 — Analogue / MS2Query channel (not this kernel)

Public 0.33+ notebooks. Needs embeddings or extra wheels. Out of scope. Retrieval cannot claim Class-3 de novo is solved.

## Ablation this slot

**Run H1 only.**

```json
{"INTENSITY_FLOOR": 0.01}
```
