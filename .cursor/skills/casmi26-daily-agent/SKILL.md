---
name: casmi26-daily-agent
description: >-
  Daily Enveda CASMI 2026 improvement agent. Starts at 1 AM America/Chicago,
  runs research→analysis→hypothesis→spec→implement→Kaggle submit every 90
  minutes until 5 daily submissions are used. Use when the user asks to run
  the CASMI daily agent, agent1, or the 90-minute submission loop.
---

# CASMI 2026 Daily Improvement Agent

## Mission

Improve the public MRR@25 for **enveda-CASMI26-molecule-id-mass-spectra** under the 5-submission daily quota.

## Schedule

- **Day start:** 01:00 America/Chicago (CST/CDT)
- **Cadence:** every **90 minutes**
- **Stop when:** 5 submissions already made for the competition day, or day ends

Run via:

```bash
PYTHONPATH=. python agent/run_daily_loop.py          # blocks, respects schedule
PYTHONPATH=. python agent/run_cycle.py --cycle N     # one cycle immediately
```

## One cycle (mandatory order)

1. **Research** — web/papers on MS/MS ID methods; write `Research/YYYY-MM-DD_cycleNN_methods.md`
2. **Analysis** — pull Kaggle submission logs/scores + local `outputs/` evidence; write `Analysis/YYYY-MM-DD_cycleNN_submission.md`
3. **Hypothesis** — combine Research+Analysis into `Hypothesis analysis/YYYY-MM-DD_cycleNN_hypotheses.md`
4. **Spec** — actionable next-submission plan in `Specs/YYYY-MM-DD_cycleNN_next_submission_spec.md`
5. **Implement + submit** — change one major factor (per competition experiment discipline); push Kaggle notebook (`enable_internet: false`); submit with `competition_submit_code`
6. **Record** — append row to `agent/state.json` (score, config hash, notebook version, hypothesis id)

## Hard constraints

- Notebook-only competition: never rely on CSV `competitions submit`
- Internet **disabled** in kernel metadata
- Do not claim Class-3 de novo solved by retrieval
- Prefer ablations: one major change per submission slot
- Keep `private/` out of git; Research/Analysis/Hypothesis analysis/Specs are committed artifacts

## Score context (update each cycle)

- Track our best public score vs leaderboard top
- Known failure mode (v0.1): exact test↔train spectrum duplicates exist with train labels that do **not** match competition GT (public ~0.143 despite perfect library match). Prefer non-identical spectral evidence, entropy similarity, full libraries, structure-level exact mass.
