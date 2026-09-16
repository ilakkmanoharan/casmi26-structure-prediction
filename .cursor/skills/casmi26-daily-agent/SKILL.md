---
name: casmi26-daily-agent
description: >-
  Daily Enveda CASMI 2026 improvement agent. Starts at 1 AM America/Chicago,
  runs research→analysis→hypothesis→spec→implement→Kaggle submit every 90
  minutes until 5 daily submissions are used. Use when the user asks to run
  the CASMI daily agent, agent1, cloud automation, or the 90-minute submission loop.
---

# CASMI 2026 Daily Improvement Agent

## Mission

Improve the public MRR@25 for **enveda-CASMI26-molecule-id-mass-spectra** under the 5-submission daily quota.

## Laptop-off runner (primary)

**GitHub Actions** — same pattern as Adaptive-Farm-Agent / Kaggriculture.

1. Workflow: [`.github/workflows/casmi-loop.yml`](../../../.github/workflows/casmi-loop.yml) (hourly UTC cron).
2. Orchestrator: `python3 scripts/casmi_loop/orchestrate.py`
3. Secrets (repo → Settings → Secrets → Actions): `KAGGLE_USERNAME`, `KAGGLE_KEY`, optional `OPENAI_API_KEY`.
4. After 5 Chicago competition-day submits, later hours no-op.
5. Details: [`agent/how-github-submits-work.md`](../../agent/how-github-submits-work.md)

**Grok Bot (agent1 steps 1–3):** enable [`casmi26-grok-research`](../casmi26-grok-research/SKILL.md) so the Bot writes `Research/`, `Analysis/`, `Hypothesis analysis/` every ~90 minutes, pushes, then dispatches Actions for implement+submit. Use [`casmi26-grok-watchdog`](../casmi26-grok-watchdog/SKILL.md) for failure recovery.

**Cursor Cloud Automations** are optional; do not rely on them for everyday submits.

## Laptop-on fallback

```bash
PYTHONPATH=. python3 scripts/casmi_loop/orchestrate.py --slot 1
PYTHONPATH=. python agent/run_daily_loop.py          # local scaffolding loop
PYTHONPATH=. python agent/run_cycle.py --cycle N
```

## Schedule

- **Day start:** 01:00 America/Chicago (CST/CDT)
- **Cadence:** GitHub hourly cron; script takes next unused slot 1–5
- **Stop when:** 5 submissions already made for the competition day

## One cycle (mandatory order)

1. **Research** — write `Research/YYYY-MM-DD_cycleNN_methods.md`
2. **Analysis** — write `Analysis/YYYY-MM-DD_cycleNN_submission.md`
3. **Hypothesis** — write `Hypothesis analysis/YYYY-MM-DD_cycleNN_hypotheses.md`
4. **Spec** — write `Specs/YYYY-MM-DD_cycleNN_next_submission_spec.md`
5. **Implement + submit** — one config ablation; rebuild `kaggle_kernel/`; `kernels push` + `competition_submit_code`
6. **Record** — append row to `agent/state.json`; commit/push artifacts

## Hard constraints

- Notebook-only competition: never rely on CSV `competitions submit`
- Internet **disabled** in kernel metadata
- Do not claim Class-3 de novo solved by retrieval
- Prefer ablations: one major change per submission slot
- Keep `private/` out of git; Research/Analysis/Hypothesis analysis/Specs are committed artifacts
- Do not commit `data/`, credentials, or large caches

## Score context (update each cycle)

- Track our best public score vs leaderboard top
- Known failure mode (v0.1): exact test↔train spectrum duplicates exist with train labels that do **not** match competition GT (public ~0.143 despite perfect library match). Prefer non-identical spectral evidence, entropy similarity, full libraries, structure-level exact mass; ban poisoned exact-dup inchikey14s when relevant.
