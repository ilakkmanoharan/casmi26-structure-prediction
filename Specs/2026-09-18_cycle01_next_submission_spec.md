# Spec — 2026-09-18 cycle01 next submission

## Objective

One major ablation vs kernel v13 / current `main`: restore spectral peak budget so entropy + modified-cosine retrieval can use fragment ladders instead of 5-ion cartoons.

## config_patch

```json
{"TOP_PEAKS": 128}
```

| Constant | Current (`main` / cycle05) | This slot | Why unchanged / changed |
|----------|----------------------------|-----------|-------------------------|
| `TOP_PEAKS` | **5** | **128** | **Major factor.** v0.2 spec; well below msentropy `max_peak_num=1000`. |
| `MASS_TOL_PPM` | 10 | 10 | already ablated 2026-09-17 |
| `MASS_TOL_PPM_BACKFILL` | 15 | 15 | already ablated |
| `PEAK_MZ_TOL` | 0.01 | 0.01 | HRMS-like; leave |
| `INTENSITY_FLOOR` | 0.001 | 0.001 | H4 later |
| `TOP_K_SPECTRA_PER_QUERY` | 80 | 80 | leave |
| `TOP_CANDIDATES_PER_SPECTRUM` | 25 | 25 | leave |
| `MIN_SIMILARITY` | 0.08 | 0.08 | do not mix with peak-count |
| `ENTROPY_WEIGHT` | 0.6 | 0.6 | H3 later |
| `EXCLUDE_EXACT_DUPLICATES` | true | true | still required |
| `MAX_CANDIDATES` | 25 | 25 | MRR@25 |

No `domain_prior_boost`.

## Implementation tasks

1. Set `TOP_PEAKS = 128` in `casmi26/config.py`.
2. Add a unit test that `clean_spectrum(..., top_peaks=128)` retains more than 5 peaks on a 40-peak synthetic spectrum, and that `casmi26.config.TOP_PEAKS == 128`.
3. Rebuild `kaggle_kernel/` via `scripts/casmi_loop/build_kernel.py` (internet **off**; RDKit wheels dataset `ilakkmanoharan/rdkit-cp312-wheels-casmi26`).
4. Reliability: `scripts/casmi_loop/chatgpt_spec.py` `_openai_json` must catch HTTP 429/5xx and return `None` so orchestrate uses `FALLBACK_ABLATIONS` instead of crashing (Actions 35311548455).
5. `kaggle kernels push -p kaggle_kernel` then poll until `COMPLETE`.
6. `competition_submit_code` with kernel `ilakkmanoharan/casmi26-retrieval-symbolic-v01` and the **parsed kernel version**. Never CSV submit.

## Message string

`2026-09-18_cycle01 TOP_PEAKS 5→128 restore entropy fragment ladder`

## Acceptance

- pytest green
- Kernel metadata `enable_internet: false`
- Submission appears on `enveda-CASMI26-molecule-id-mass-spectra` **or** Analysis records an explicit auth/quota skip
- `agent/state.json` appended for `2026-09-18_cycle01`
