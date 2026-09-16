# `agent/state.json` schema (documentation)

Committed state for the daily CASMI agent. GitHub Actions (`casmi-loop`) is the primary laptop-off updater.

## Top-level fields

| Field | Type | Description |
|-------|------|-------------|
| `competition` | string | Kaggle competition slug |
| `daily_limit` | number | Max submissions per competition day (5) |
| `interval_minutes` | number | Minutes between cycles (60 for Actions hourly cron) |
| `day_start_local` | string | Local day-start clock (`01:00`) |
| `timezone` | string | IANA TZ (`America/Chicago`) |
| `best_public_score` | number \| null | Best observed public LB score |
| `github_actions` | object \| null | Primary unattended runner metadata |
| `cloud_automation` | object \| null | Optional Cursor Automations metadata |
| `cycles` | array | Append-only cycle records |

## `github_actions` (primary)

| Field | Type | Description |
|-------|------|-------------|
| `enabled` | boolean | Whether GitHub Actions is enabled |
| `primary_runner` | boolean | Prefer Actions over Cursor Automations |
| `workflow` | string | `.github/workflows/casmi-loop.yml` |
| `secrets` | string[] | `OPENAI_API_KEY`, `KAGGLE_USERNAME`, `KAGGLE_KEY` |
| `kernel` | string | Default Kaggle kernel `owner/slug` |

## `cloud_automation` (optional)

| Field | Type | Description |
|-------|------|-------------|
| `enabled` | boolean | Alternate Cursor Automations runner (usually false) |
| `prompt_path` | string | Tracked prompt, usually `agent/CLOUD_CYCLE_PROMPT.md` |
| `dashboard_url` | string | `https://cursor.com/automations` |
| `secrets` | string[] | Expected secret names (`KAGGLE_USERNAME`, `KAGGLE_KEY`) |
| `kernel` | string | Default Kaggle kernel `owner/slug` |
| `last_runner` | string | `github_actions` \| `cursor_cloud` \| `local` \| `manual` |

## Each `cycles[]` entry

| Field | Type | Description |
|-------|------|-------------|
| `day` | string | Competition day key `YYYY-MM-DD` (anchored at 01:00 America/Chicago) |
| `cycle` | number | 1-based cycle index for that day |
| `tag` | string | `YYYY-MM-DD_cycleNN` |
| `started_at` | string | ISO-8601 timestamp (optional) |
| `runner` | string | `github_actions` \| `cursor_cloud` \| `local` \| `manual` |
| `submitted` | boolean | Whether a Kaggle code submission was created |
| `skipped_reason` | string \| null | e.g. `quota_exhausted` |
| `kernel` | string | Kaggle kernel slug |
| `kernel_version` | number \| null | Version from `kaggle kernels push` |
| `submit_ref` | string \| null | Kaggle submission ref id if known |
| `message` | string | Kaggle submission message |
| `prior_public_score` | number \| null | Best/public score before this cycle |
| `public_score` | number \| null | Score after this cycle if available |
| `hypothesis` | string | Short id e.g. `H1+H2` |
| `artifacts` | object | Paths to Research / Analysis / Hypothesis / Spec markdown |

Do not store secrets in this file.
