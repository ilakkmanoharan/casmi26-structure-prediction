# Hypotheses — 2026-10-29 cycle03

## H1 — H-peaks (run this slot)

**Claim.** Raising `TOP_PEAKS` from **128** to **160** keeps additional mid-intensity fragment ions after the 1% noise floor, improving entropy/modcos overlap and public MRR@25 versus the 0.143 plateau.

**Mechanism.** `clean_spectrum` already drops ions below `INTENSITY_FLOOR=0.01`, then keeps only the top-N remaining peaks (`casmi26/spectrum.py`). Flash Entropy / ms_entropy default to **no** hard cap after that floor. 128 was the restore-from-5 step (Actions cycle01 today, already live). 160 is a bounded next step: more diagnostic ions on fragment-rich NP spectra without opening the kernel to unbounded peak lists.

**Expected MRR direction.** Small positive if 128 is truncating true-structure ladders; near-zero if most spectra already have ≤128 peaks above 1%. Failure mode: extra noise ions that survived the 1% cut dilute entropy similarity and promote decoys (MRR down). That is acceptable to measure — it is a real ablation, unlike replaying `PEAK_MZ_TOL=0.02`.

## H2 — MIN_SIMILARITY 0.05 → 0.12 (not this slot; slot-2 fallback)

**Claim.** Raising the library-hit admission floor drops junk hybrid scores from `top_k`.

**Why not now.** Cloud cycle02 (PR #41) already implements this and is still draft. Applying it here would move **two** knobs vs live main and collide with cycle02 files. Slot-2 fallback is retargeted to `{MIN_SIMILARITY: 0.12}` so the next unused Actions ticket can take it without replaying 0.02.

## H3 — Remove the peak cap entirely (not this slot)

**Claim.** `max_peak_num=None` matches ms_entropy.

**Why not now.** Unbounded lists risk kernel-time and memory on dirty library spectra. 160 is the one-factor step.

## H4 — Analog / MS2Deepscore (out of scope)

Needs extra wheels or embeddings. Out of scope for a one-constant ablation. Do not claim Class-3 de novo is solved by retrieval.

## One major ablation this slot

Run **H1 only**. `config_patch: {"TOP_PEAKS": 160}`.
