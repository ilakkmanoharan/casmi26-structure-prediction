# Spec — next submission v0.2 (cycle01)

## Objective

Public MRR@25 ≫ 0.143 by not trusting exact test↔train duplicate labels, adding entropy similarity, and indexing all libraries.

## Config changes

| Parameter | v0.1 | v0.2 |
|-----------|------|------|
| Libraries | preferred only | **all** `ingest_lib` |
| Exact duplicate handling | trusted | **exclude from scoring** (skip train rows with identical cleaned peaks+precursor to current query) |
| Similarity | modified cosine | **hybrid** `0.55·entropy + 0.45·modcos` |
| `top_peaks` | 64 | **128** |
| `mass_tol_ppm` | 20 | **25** (backfill 60) |
| Domain prior | strong enveda | keep soft (unchanged weights initially) |
| `min_similarity` | 0.05 | **0.08** |

## Implementation tasks

1. `spectrum.py`: add `entropy_similarity()` (Li-style intensity-weighted entropy similarity on centroid peaks).
2. `retrieve.py`: when comparing query to a train row, if peaks+precursor identical → skip; else hybrid score.
3. `run_pipeline.py` / Kaggle notebook: drop `--preferred-libs-only`; rebuild index.
4. Rebuild `artifacts/spectrum_index.npz`; regenerate `submission.csv` + evidence ledger.
5. Push notebook `casmi26-retrieval-symbolic-v01` (or v02 slug), internet off, submit via `competition_submit_code`.

## Acceptance

- Unit tests still pass (adducts + submission)
- No placeholders on test
- Evidence shows rank-1 `best_similarity` **not** identically 1.0 for all 400 (or identical rows skipped)
- Notebook completes &lt; 9 h offline
- Submission appears on Kaggle with new public score

## Message string

`v0.2 exclude-exact-dupes + entropy/modcos hybrid + all-libs`
