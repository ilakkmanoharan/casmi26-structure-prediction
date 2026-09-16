# How everyday CASMI Kaggle submissions run with the Mac off

Date written: 2026-09-15

Same pattern as Adaptive-Farm-Agent / Kaggriculture: **GitHub Actions**, not Cursor Cloud Automations, is the laptop-off submit path.

## Short answer

1. Repo: [github.com/ilakkmanoharan/casmi26-structure-prediction](https://github.com/ilakkmanoharan/casmi26-structure-prediction).
2. Workflow: `.github/workflows/casmi-loop.yml` — `cron: "0 * * * *"` (every hour UTC).
3. Each hour a GitHub Ubuntu runner checks out `main`, injects secrets, runs `scripts/casmi_loop/orchestrate.py`.
4. That script writes Research/Analysis/Hypothesis/Specs, applies one config ablation, rebuilds `kaggle_kernel/`, `kaggle kernels push`, polls until COMPLETE, then `competition_submit_code`, and pushes artifacts back to GitHub.
5. After **5 successful uploads for the Chicago competition day** (day starts **01:00 America/Chicago**), later hourly runs exit without submitting.

Your Mac is only needed to push code, edit secrets, or **Actions → casmi-loop → Run workflow**. It is not in the submit path.

## Why Kaggriculture looked “automatic” without Cursor Automations

Kaggriculture uses the same design: GitHub cron → orchestrator → Kaggle upload → git commit/push. Cursor Cloud Agents are optional there (`CURSOR_API_KEY`); ChatGPT / fallbacks write the bot. CASMI now mirrors that.

## Where the loop lives

| Piece | Path / place |
|---|---|
| Scheduler | `.github/workflows/casmi-loop.yml` |
| Orchestrator | `scripts/casmi_loop/orchestrate.py` |
| Slot bookkeeping | `agent/state.json` |
| Specs / research | `Research/`, `Analysis/`, `Hypothesis analysis/`, `Specs/` |
| Kernel | `kaggle_kernel/` (rebuilt from `casmi26/`) |
| Secrets | GitHub repo → Settings → Secrets and variables → Actions |

Required secrets:

- `KAGGLE_USERNAME`
- `KAGGLE_KEY` (from `~/.kaggle/kaggle.json`)
- `OPENAI_API_KEY` (optional but recommended; without it, deterministic config ablations run)

## One hourly run

```
GitHub cron (top of hour UTC)
        │
        ▼
   Ubuntu runner checks out main
        │
        ▼
   Write ~/.kaggle/{kaggle.json,access_token}
        │
        ▼
   python3 scripts/casmi_loop/orchestrate.py
        │
        ├─ next unused Chicago competition-day slot (1–5)
        ├─ if 5 already done → exit 0
        ├─ list Kaggle submissions → briefing
        ├─ ChatGPT (or fallback) → Research/Analysis/Hypothesis/Specs + config_patch
        ├─ apply patch to casmi26/config.py
        ├─ rebuild kaggle_kernel notebook (embed package sources)
        ├─ kaggle kernels push → poll COMPLETE
        ├─ competition_submit_code (never CSV submit)
        └─ git commit + push docs + casmi26 + kaggle_kernel + agent/state.json
```

## One-time setup

1. Push this repo to GitHub with Actions enabled.
2. Add secrets at  
   https://github.com/ilakkmanoharan/casmi26-structure-prediction/settings/secrets/actions
3. **Actions → casmi-loop → Run workflow** once (optionally `skip_submit=1` first).
4. Leave the hourly schedule on; Mac can stay off.

## Hard constraints

- Notebook-only competition — CSV `competitions submit` fails.
- Kernel internet **off**; RDKit via `ilakkmanoharan/rdkit-cp312-wheels-casmi26`.
- Do not commit `data/`, `private/`, credentials, or large caches.
- Job timeout is 360 minutes so the runner can wait on long Kaggle kernel runs.

## How to check

1. [Actions → casmi-loop](https://github.com/ilakkmanoharan/casmi26-structure-prediction/actions/workflows/casmi-loop.yml)
2. [Kaggle Submissions](https://www.kaggle.com/competitions/enveda-CASMI26-molecule-id-mass-spectra/submissions)
3. New cycle markdown under `Research/` / `Analysis/` / … and updates to `agent/state.json` on `main`

## Grok Bot roles

| Skill | Owns |
|-------|------|
| [`casmi26-grok-research`](../.cursor/skills/casmi26-grok-research/SKILL.md) | agent1 steps 1–3: `Research/`, `Analysis/`, `Hypothesis analysis/` (+ optional `Specs/`), then push + dispatch |
| [`casmi26-grok-watchdog`](../.cursor/skills/casmi26-grok-watchdog/SKILL.md) | Check Actions health; re-run workflow on failure / missed slot |

If Grok pushes substantial cycle markdown first, `casmi-loop` **reuses** those files instead of regenerating them with OpenAI.
