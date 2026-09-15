# Analysis — 2026-09-15 cycle01 (submission v0.1)

## Submission log

| Field | Value |
|-------|-------|
| Notebook | `ilakkmanoharan/casmi26-retrieval-symbolic-v01` v2 |
| Description | v0.1 retrieval+symbolic preferred-libs modified-cosine |
| Status | COMPLETE |
| **Public score** | **0.143** |
| Submitted (UTC) | 2026-09-15 11:20:21 |
| Leaderboard context | Top ≈ 0.285 (≈2× our score) |

## Local diagnostics (`outputs/candidate_evidence.parquet`)

- 400 / 400 molecules produced ≥1 candidate; **0 placeholders**
- Mean candidates / molecule ≈ 24.2
- Fallback rate ≈ 19.5%
- **Every molecule** had rank-1 `best_similarity = 1.0`, `mass_error_ppm = 0`, library **enveda-180**
- Rank-1 `n_supporting_spectra` mean **3.03** = mean spectra / molecule → each query spectrum contributed a perfect hit to the same structure
- Spot checks: cleaned (and raw) test peaks are **byte-identical** to train rows at the same precursor m/z
- Submission rank-1 SMILES inchikey14 **agrees 400/400** with that exact-match train label

## Why the score is low

1. **Label–GT mismatch on leaked duplicates (primary).**  
   Perfect spectrum→structure library match should yield MRR≈1 if train labels equal competition GT. Observed MRR=0.143 ⇒ for ~86% of molecules the structure attached to the identical train spectrum is **not** the scored answer. Trusting exact duplicates actively places wrong SMILES at rank 1.

2. **Cosine saturation / no ranking signal among decoys.**  
   When sim=1.0 for the poisoned hit, aggregation weights (domain prior, support) cannot recover; secondary candidates are under-ranked.

3. **Preferred-lib index omitted pluskal_ms2 (~0.5M spectra).**  
   Possible missed correct structures living only there.

4. **Known-spectrum local CV was misleading.**  
   Unseen-structure MRR=0 (by construction); known-spectrum MRR=1.0 measured recovery of train labels, **not** competition GT.

5. **Data refresh note.**  
   Kaggle file timestamps moved to 2026-09-15 14:32Z after our submit — re-download before v0.2 in case leakage / schema changed.

## What would improve the score

- Drop or heavily penalize exact-duplicate train spectra when building evidence
- Re-rank with entropy + modified cosine on **near** matches (including other CE/adducts)
- Index full train (all `ingest_lib`)
- Soften domain prior so spectral evidence dominates
- Validate on a proxy that does **not** reward recovering poisoned labels (e.g. force-exclude identical rows in CV)

## Naive baseline reference

Mass-only known-spectrum CV MRR@25 ≈ 0.73 (local) — not comparable to public LB, but shows mass prior is informative when labels are consistent.
