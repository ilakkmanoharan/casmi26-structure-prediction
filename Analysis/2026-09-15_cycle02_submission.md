# Analysis — 2026-09-15 cycle02

## Submission log (known)

| Version | Source | Public score | Notes |
|---------|--------|--------------|-------|
| **v0.1** | `ilakkmanoharan/casmi26-retrieval-symbolic-v01` (kernel v2) | **0.143** | preferred-libs, modified cosine only; COMPLETE |
| **v0.2** (cycle01) | same kernel line; message `v0.2 ban-poisoned-exact-dup-IKs + entropy/modcos hybrid + all-libs` | **unknown / pending** | `agent/state.json` marks cycle01 `submitted: true`, `public_score: null` |
| Leaderboard context (cycle01 note) | — | Top ≈ **0.285** | ~2× v0.1 |

**Kaggle CLI** is not available on this research box (`kaggle` not installed; no `~/.kaggle`). Scores above are from committed Analysis + `agent/state.json` only — **no invented scores**.

Chicago competition day **2026-09-15** (anchor 01:00 America/Chicago): state reports **1/5** slots used → **4 remaining**. A `casmi-loop` Actions run was in progress at research time (run `35040180158`).

## Why v0.1 score is low (evidence)

From `Analysis/2026-09-15_cycle01_submission.md` / local diagnostics:

1. **Exact test↔train duplicate contamination (primary).** Every molecule had rank-1 `best_similarity = 1.0`, `mass_error_ppm = 0`, library **enveda-180**. Spot checks: cleaned (and raw) test peaks byte-identical to train rows. Rank-1 SMILES inchikey14 agreed 400/400 with that train label, yet public MRR@25 = **0.143** ⇒ for ~86% of molecules the duplicated train label ≠ competition GT. Trusting exact dups actively ranks wrong structures #1.
2. **Cosine saturation.** With sim=1.0 on poisoned hits, aggregation (domain prior, support, CE coverage) cannot recover; decoys are under-ranked.
3. **Preferred-lib index omitted large slices** (e.g. `pluskal_ms2`) — coverage gap for structures absent from enveda/NP preferred set.
4. **Misleading local CV.** Known-spectrum MRR=1.0 recovered train labels, not GT; unseen-structure MRR=0 by construction.

## Cycle01 intended fix (v0.2) — status

Spec shipped: exclude exact-dup evidence, hybrid `0.55·entropy + 0.45·modcos`, index **all** libs, `TOP_PEAKS=128`, `MASS_TOL_PPM=25`, `MIN_SIMILARITY=0.08`. Config on main already has `EXCLUDE_EXACT_DUPLICATES=True`, `ENTROPY_WEIGHT=0.55`. Public score for that submit is **not yet recorded** in state — treat v0.2 as unvalidated until LB updates.

## Concrete next-slot improvements

1. **Major ablation:** raise `ENTROPY_WEIGHT` toward entropy dominance (Li & Fiehn 2021) once exact-dup ban is on — better separation among near-isobars than a 50/50 hybrid.
2. Keep `EXCLUDE_EXACT_DUPLICATES=True` (do not ablate this off).
3. If v0.2 score lands still ≪ 0.20: next slots try tighter `MASS_TOL_PPM` (decoy control after all-libs) or higher `TOP_K_SPECTRA_PER_QUERY` (multi-CE support).
4. Proxy validation must force-exclude identical rows (never reward recovering poisoned labels).
5. Always notebook code submit path.

## Naive baselines (local, not LB)

Mass-only known-spectrum CV MRR@25 ≈ 0.73 — informative only when labels are consistent; not comparable to public LB under contamination.
