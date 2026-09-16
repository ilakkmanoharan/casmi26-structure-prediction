---
name: casmi26-grok-watchdog
description: >-
  Grok Bot skill to check Enveda CASMI casmi-loop GitHub Actions health and
  dispatch workflow_dispatch runs when quota remains or the last run failed.
  Use when asked to watch casmi-loop, trigger Actions, or babysit daily Kaggle
  submits with Grok Bot.
---

# CASMI Grok Bot — Actions watchdog

## Job

Own **monitoring + dispatch** for the unattended CASMI submit loop. Do **not**
re-implement research/submit yourself — GitHub Actions runs
`scripts/casmi_loop/orchestrate.py`. You only check status and trigger
**Actions → casmi-loop → Run workflow** when needed.

Repo: `ilakkmanoharan/casmi26-structure-prediction`  
Workflow: `.github/workflows/casmi-loop.yml`  
Docs: `agent/how-github-submits-work.md`

## Access required

- GitHub plugin / `gh` authenticated to `ilakkmanoharan` (repo + `workflow` scope)
- Optional: browser signed into GitHub Actions UI as fallback

Never print `KAGGLE_*`, `OPENAI_API_KEY`, or other secret values.

## Check procedure (every run)

1. Read `agent/state.json` on `main` (via `gh api` or clone).
2. Run:

```bash
python3 scripts/casmi_loop/check_and_dispatch.py
```

   Or equivalent:

```bash
gh run list -R ilakkmanoharan/casmi26-structure-prediction --workflow=casmi-loop.yml --limit 5
```

3. Decide using these rules:

| Situation | Action |
|-----------|--------|
| Run `queued` / `in_progress` | Do nothing; report URL |
| `submitted_slots` already 1–5 for Chicago competition day | Do nothing (quota full) |
| Last run `failure` and slots remain | `--dispatch` recovery run |
| No successful submit yet today and hour ≥ 01:00 America/Chicago and no in-progress run | `--dispatch` |
| Cron healthy (recent success within ~2h) and quota not full | Do nothing |
| User explicitly asks to run | `--dispatch` (honor `--skip-submit` if they say dry-run) |

4. To dispatch:

```bash
python3 scripts/casmi_loop/check_and_dispatch.py --dispatch
# dry-run (no Kaggle submit):
python3 scripts/casmi_loop/check_and_dispatch.py --dispatch --skip-submit
```

Equivalent UI: GitHub → Actions → **casmi-loop** → **Run workflow**.

5. Reply in the Bot conversation with:
   - competition day + slots used / remaining
   - last run conclusion + link
   - whether you dispatched (yes/no + why)
   - any failure summary (last ~40 log lines via `gh run view <id> --log-failed`)

## Approval boundary

- **Allowed without asking:** read Actions status, read `agent/state.json`, dispatch `casmi-loop` when rules above say so, post a status note in this Bot chat.
- **Ask first:** changing workflow YAML, rotating secrets, force-dispatch after quota full (`--force`), canceling in-progress jobs, anything outside this repo.

## Suggested routine

Ask the Bot (after enabling this skill):

> Every 90 minutes between 01:00 and 12:00 America/Chicago, run the
> `casmi26-grok-watchdog` skill. Check casmi-loop health and dispatch a
> workflow run only when quota remains and no run is in progress (or the
> last run failed). Post a short status in this conversation. Never print
> secrets.

Use **Test run** once after creating the routine.

## Related

- Primary submit path: GitHub Actions hourly cron (not this Bot)
- This Bot is a **watchdog / manual trigger**, not a replacement for `casmi-loop`
