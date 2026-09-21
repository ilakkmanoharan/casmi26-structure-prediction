# Hypotheses 2026-09-21_cycle01

Grounded in `Research/2026-09-21_cycle01_methods.md` and `Analysis/2026-09-21_cycle01_submission.md`.

## H1 (this slot) — restoring the fragment ladder raises hybrid similarity for the true structure

**Claim.** With `TOP_PEAKS=5` (kernel v13 / 56298621), entropy similarity and modified cosine see at most five ions. Li/Fiehn Flash Entropy keep ions above ~1% BPI and routinely 100 peaks. Restoring `TOP_PEAKS=128` increases matched-ion overlap for the correct library structure inside the 10–15 ppm mass window, which should raise public MRR@25 relative to v13 (and relative to the last *scored* 0.143 if v13 never scored).

**Ablation:** one constant, vs last submitted kernel.

```json
{"TOP_PEAKS": 128}
```

Keep `EXCLUDE_EXACT_DUPLICATES=true`, `ENTROPY_WEIGHT=0.6`, `MASS_TOL_PPM=10`, `MASS_TOL_PPM_BACKFILL=15`.

**Expected direction:** public MRR@25 **up** vs 0.143 if v13 is unscored or harmful; at worst flat if the public split is dominated by poisoned exact-dups that 128-peak `spectra_identical` already bans.

**Failure mode:** more peaks make two different molecules look similar (noise ions), or make poisoned exact-dups *less* identical after cleaning so the ban misses them. Mitigant: `INTENSITY_FLOOR=0.001` still drops tiny noise; exact-dup check uses the same cleaner on both sides.

## H2 — entropy-dominant hybrid after peaks are restored

`ENTROPY_WEIGHT=0.70` was specified 2026-09-15 cycle02 but the kernel ERRORed and never scored. **Do not stack** on this slot.

## H3 — OpenAI 429 must not consume the implement+submit path

Not an MRR hypothesis. If `_openai_json` returns `None` on 429, `FALLBACK_ABLATIONS` or pre-written docs let Actions push a kernel. Without this, quota remaining is wasted every hour (observed 2026-09-18 → 2026-09-21).

## H4 — tighter mass window is not the next lever

Cycles 03–05 already moved ppm. PublicScore still null. Revisit only after H1 has a scored kernel.

## Slot decision

**Run H1 only** (`TOP_PEAKS` 5→128). Ship H3 as infrastructure so the next Actions hour can submit this config.
