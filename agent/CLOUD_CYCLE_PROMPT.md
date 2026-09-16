# CASMI 2026 — Cloud daily cycle prompt

Optional **Cursor Cloud Automation** prompt. Prefer the GitHub Actions loop
(`.github/workflows/casmi-loop.yml` + `scripts/casmi_loop/orchestrate.py`) for
everyday laptop-off submits — see `agent/how-github-submits-work.md`.
Local copy of the workflow in `private/agent/agent1.md` (that path is gitignored).

## Mission

Improve public MRR@25 for **enveda-CASMI26-molecule-id-mass-spectra** under the **5 submissions / competition-day** quota. Work in repo `ilakkmanoharan/casmi26-structure-prediction`.

## Schedule (competition clock)

- **Day start:** 01:00 America/Chicago (CST/CDT)
- **Cadence:** every **90 minutes** after day start
- **Suggested automation slots (local):** 01:00, 02:30, 04:00, 05:30, 07:00 America/Chicago  
  Convert to UTC when configuring cron (CDT = UTC−5, CST = UTC−6). Example CDT UTC crons:
  - `0 6,9,12 * * *` and `30 7,10 * * *` (covers the five slots)
- **Stop when:** 5 Kaggle submissions already exist for this competition day, or the agent determines quota is exhausted via API + `agent/state.json`

Scheduled triggers may fire late; **always re-check quota** before submitting.

## Secrets (Cloud Agent)

Expect environment / Cursor secrets:

- `KAGGLE_USERNAME`
- `KAGGLE_KEY`

Write `~/.kaggle/kaggle.json` with mode `0600` before calling the Kaggle CLI/API:

```json
{"username":"<KAGGLE_USERNAME>","key":"<KAGGLE_KEY>"}
```

## One cycle (mandatory order)

1. **Research** — search the web / papers for MS/MS structure-ID techniques that can raise MRR@25. Write `Research/YYYY-MM-DD_cycleNN_methods.md` (create `Research/` if missing). Cover methods to consider, why, and how they improve score.

2. **Analysis** — pull prior submission logs/scores (`kaggle competitions submissions -c enveda-CASMI26-molecule-id-mass-spectra`), leaderboard context, and any committed notes / prior cycle docs. Write `Analysis/YYYY-MM-DD_cycleNN_submission.md` (create `Analysis/` if missing): why score is low and how to improve.

3. **Hypothesis** — from Research + Analysis, write `Hypothesis analysis/YYYY-MM-DD_cycleNN_hypotheses.md` (create folder if missing).

4. **Spec** — from Research + Analysis + Hypothesis, write `Specs/YYYY-MM-DD_cycleNN_next_submission_spec.md` with an actionable implementation plan (one major ablation preferred).

5. **Implement + submit**
   - Change code per the spec (prefer one major factor vs previous submission).
   - Rebuild Kaggle notebook under `kaggle_kernel/` if needed (`enable_internet: false`; RDKit wheels dataset `ilakkmanoharan/rdkit-cp312-wheels-casmi26`).
   - `kaggle kernels push -p kaggle_kernel`
   - Poll until kernel `COMPLETE` (do **not** busy-wait a full 9h Kaggle training window if push+poll+submit can finish sooner; Kaggle runs the notebook asynchronously).
   - Submit with **code** API only (`competition_submit_code`), kernel `ilakkmanoharan/casmi26-retrieval-symbolic-v01`. Never use CSV `competitions submit`.
   - Competition: `enveda-CASMI26-molecule-id-mass-spectra`

6. **Record** — append a cycle object to [`agent/state.json`](state.json) (see schema there). Commit and push:
   - `Research/`, `Analysis/`, `Hypothesis analysis/`, `Specs/`
   - code / `kaggle_kernel/` / skill updates if changed
   - updated `agent/state.json`  
   Prefer a clear commit message. Opening a PR is allowed if direct push to `main` is blocked.

## Pre-flight checks (every run)

1. Read `agent/state.json`.
2. Query Kaggle submissions for today’s competition day; count successful/pending submits toward the 5-slot limit.
3. If `submissions_today >= 5`, write a short note under `Analysis/` that quota is exhausted and **exit without submitting**.
4. Choose `cycle` number = next unused for that day (`YYYY-MM-DD_cycleNN`).

## Hard constraints

- Notebook-only competition — CSV upload fails.
- Kernel metadata: `enable_internet: false`.
- Do not commit `data/`, `private/`, `outputs/`, `artifacts/`, credentials, or large parquet/npz caches.
- Do not claim Class-3 de novo is solved by retrieval alone.
- One major experimental change per submission slot when possible.
- `train.parquet` (~3GB) is **not** in git — download from Kaggle on demand into `data/` (gitignored) when needed for local/cloud pipeline runs.

## Known context (update each cycle)

- Track best public score vs leaderboard top in analysis + `agent/state.json`.
- v0.1 failure mode: exact test↔train spectrum duplicates in `enveda-180` with train labels ≠ competition GT (~0.143 public). Prefer non-identical evidence, entropy similarity, full libraries, structure-level mass filters; ban poisoned exact-dup inchikey14s when still relevant.

## Deliverables checklist

- [ ] Research markdown committed
- [ ] Analysis markdown committed
- [ ] Hypothesis markdown committed
- [ ] Spec markdown committed
- [ ] Code/notebook updated if submitting
- [ ] Kaggle code submission created (or explicit skip for quota)
- [ ] `agent/state.json` updated and pushed
