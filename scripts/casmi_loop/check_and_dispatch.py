#!/usr/bin/env python3
"""Check casmi-loop health and optionally dispatch a GitHub Actions run.

Used by Grok Bot / humans:

  python3 scripts/casmi_loop/check_and_dispatch.py
  python3 scripts/casmi_loop/check_and_dispatch.py --dispatch
  python3 scripts/casmi_loop/check_and_dispatch.py --dispatch --skip-submit
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    __package__ = "scripts.casmi_loop"

from scripts.casmi_loop.slots import competition_day
from scripts.casmi_loop import state

REPO = os.environ.get("GITHUB_REPOSITORY") or "ilakkmanoharan/casmi26-structure-prediction"
WORKFLOW = "casmi-loop.yml"


def _gh(args: list[str]) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    return subprocess.run(
        ["gh", *args],
        text=True,
        capture_output=True,
        env=env,
    )


def recent_runs(limit: int = 5) -> list[dict]:
    proc = _gh(
        [
            "run",
            "list",
            "-R",
            REPO,
            "--workflow",
            WORKFLOW,
            "--limit",
            str(limit),
            "--json",
            "databaseId,status,conclusion,event,createdAt,displayTitle,url",
        ]
    )
    if proc.returncode != 0:
        raise SystemExit("gh run list failed: %s" % (proc.stderr or proc.stdout)[:500])
    return json.loads(proc.stdout or "[]")


def dispatch(*, skip_submit: bool = False, slot: int | None = None) -> str:
    args = ["workflow", "run", WORKFLOW, "-R", REPO]
    if skip_submit:
        args += ["-f", "skip_submit=1"]
    if slot is not None:
        args += ["-f", "slot=%s" % slot]
    proc = _gh(args)
    if proc.returncode != 0:
        raise SystemExit("gh workflow run failed: %s" % (proc.stderr or proc.stdout)[:500])
    return "dispatched %s on %s" % (WORKFLOW, REPO)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dispatch", action="store_true", help="Trigger casmi-loop workflow")
    p.add_argument("--skip-submit", action="store_true", help="Pass skip_submit=1")
    p.add_argument("--slot", type=int, choices=(1, 2, 3, 4, 5))
    p.add_argument("--force", action="store_true", help="Dispatch even if quota full / run in progress")
    args = p.parse_args()

    day = competition_day()
    data = state.load()
    used = sorted(state.submitted_slots(day, data))
    next_slot = state.next_unused_slot(day, data)
    runs = []
    try:
        runs = recent_runs()
    except SystemExit as exc:
        print("WARN:", exc)
    in_progress = [r for r in runs if r.get("status") in ("queued", "in_progress", "pending")]
    last = runs[0] if runs else None

    report = {
        "checked_at": datetime.utcnow().isoformat() + "Z",
        "competition_day": day.isoformat(),
        "submitted_slots": used,
        "next_slot": next_slot,
        "quota_remaining": None if next_slot is None else (5 - len(used)),
        "last_run": last,
        "in_progress": in_progress,
        "actions_url": "https://github.com/%s/actions/workflows/%s" % (REPO, WORKFLOW),
    }
    print(json.dumps(report, indent=2))

    if not args.dispatch:
        return 0

    if in_progress and not args.force:
        print("skip dispatch: run already in progress")
        return 0
    if next_slot is None and not args.force:
        print("skip dispatch: daily quota exhausted")
        return 0
    if last and last.get("conclusion") == "failure" and next_slot is not None:
        print("last run failed; dispatching recovery run")

    msg = dispatch(skip_submit=args.skip_submit, slot=args.slot or next_slot)
    print(msg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
