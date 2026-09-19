# Analysis — 2026-09-19 cycle01

## Competition-day quota

- **Chicago day:** 2026-09-19 starting 01:00 America/Chicago (06:00 UTC). This run started 06:04 UTC.
- **Kaggle count:** **0 / 5** used for 2026-09-19. Source: casmi-loop run [35421305696](https://github.com/ilakkmanoharan/casmi26-structure-prediction/actions/runs/35421305696) at 04:27 UTC printed `submissions used today (2026-09-19): local=0 kaggle=0` and listed the five newest rows (all older than this Chicago day). No successful Actions submit since 2026-09-17 07:20 UTC (run 35194073264 → Kaggle `56298621`).
- Cloud Agent env still has **empty** `KAGGLE_USERNAME` / `KAGGLE_KEY` / `KAGGLE_API_TOKEN`, so this cycle cannot call the Kaggle API itself. Quota is **not** exhausted.

## Recent Kaggle submissions (from Actions 35421305696)

| id | publicScore | message |
|----|-------------|---------|
| 56298621 | *null* | cycle05: broader libs + entropy/modcos + `TOP_PEAKS=5` |
| 56290985 | *null* | cycle04: mass-tol 10/15 ppm + exact-dup exclude |
| 56290242 | *null* | cycle03: mass-tol 5/10 ppm |
| 56289785 | *null* | 2026-09-16 v10 rdkit-install + all-libs |
| 56289779 | *null* | probe v3 |

Best recorded public score in `agent/state.json` remains **0.143** (v0.1). Later code submits have not posted a public number in Actions logs.

## Leaderboard context (2026-09-19)

Public LB (~33% of test): **GUAM 0.332**, Minal kharat123 0.324, Preechanon Chatthai 0.319, then ~0.31 down through ~0.25 in the top 40. Gap vs 0.143 is still ~2.3×.  
https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra/leaderboard

## Why the score is low

1. **v0.1 poisoned exact dups** — test↔train identical spectra in `enveda-180` with train labels ≠ competition GT. Rank-1 similarity 1.0 on the wrong SMILES. Guard (`EXCLUDE_EXACT_DUPLICATES`) is on, but later submits never scored.
2. **cycle05 `TOP_PEAKS=5` is still on `main`** — entropy similarity and modified cosine both need mid-intensity fragments. Li/Fiehn / Flash Entropy / msentropy keep ions above ~1% BPI and typically up to ~100 peaks. Five peaks:
   - collapse hybrid scores toward the few strongest ions (often precursor-related);
   - make `spectra_identical` too coarse (two different spectra can match after a 5-peak clean), so the poison-ban set is wrong.
3. **Unmerged 2026-09-18 cycle01** (PR #4) already specified `TOP_PEAKS=128` + OpenAI 429 fallback, but it is still a draft. Actions has **failed every hourly run since 2026-09-18 05:37 UTC** on `urllib.error.HTTPError: HTTP Error 429` inside `chatgpt_spec._openai_json` — **before** implement/submit. That burned Sep 18’s slots without a Kaggle upload.
4. Entropy-dominant hybrid (`ENTROPY_WEIGHT=0.70`, cycle02) never scored (kernel ERROR, then 429 loop).

## Concrete improvements this slot

1. Restore **`TOP_PEAKS=128`** (one major ablation vs `main`).
2. Catch OpenAI **429/5xx/URL errors** and use the existing deterministic fallback so casmi-loop can still implement + `competition_submit_code`.
3. Write `~/.kaggle/kaggle.json` + `access_token` when Cloud secrets exist (kaggle CLI 2.2).
4. Do **not** change mass-tol / entropy / min-sim this slot.

## Cloud submit status

`~/.kaggle/kaggle.json` was **not** written: secrets `KAGGLE_USERNAME` and `KAGGLE_KEY` are unset in this Cloud Agent. After the docs/code land, hourly casmi-loop (which **does** have those secrets) can reuse these files and submit if the 429 crash is fixed.
