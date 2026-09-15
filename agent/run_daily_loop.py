#!/usr/bin/env python3
"""
Block until 01:00 America/Chicago (if before day start), then run cycles every 90 minutes
until 5 submissions are recorded for the competition day.
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
TZ = ZoneInfo("America/Chicago")
STATE_PATH = ROOT / "agent" / "state.json"
INTERVAL_SEC = 90 * 60


def now() -> datetime:
    return datetime.now(TZ)


def day_anchor(dt: datetime) -> datetime:
    local = dt.astimezone(TZ)
    anchor = local.replace(hour=1, minute=0, second=0, microsecond=0)
    if local < anchor:
        anchor -= timedelta(days=1)
    return anchor


def load_state() -> dict:
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text())
    return {"daily_limit": 5, "cycles": []}


def submissions_for_day(state: dict, day_key: str) -> int:
    return sum(1 for c in state.get("cycles", []) if c.get("day") == day_key and c.get("submitted"))


def sleep_until(target: datetime) -> None:
    while True:
        n = now()
        remaining = (target - n).total_seconds()
        if remaining <= 0:
            return
        print(f"[daily-loop] sleeping {remaining/60:.1f} min until {target.isoformat()}")
        time.sleep(min(remaining, 300))


def main() -> int:
    n = now()
    anchor = day_anchor(n)
    next_start = anchor if n >= anchor else anchor
    # If we're past today's 1 AM, start immediately; else wait for 1 AM
    if n < day_anchor(n) + timedelta(days=0) and n.hour < 1:
        sleep_until(anchor)

    print(f"[daily-loop] starting competition day {day_anchor(now()).strftime('%Y-%m-%d')}")
    while True:
        state = load_state()
        day_key = day_anchor(now()).strftime("%Y-%m-%d")
        used = submissions_for_day(state, day_key)
        limit = int(state.get("daily_limit", 5))
        print(f"[daily-loop] {now().isoformat()} used={used}/{limit}")
        if used >= limit:
            print("[daily-loop] quota done for today")
            return 0

        # Invoke cycle; Cursor agent / human should have filled implement path.
        # Default: run cycle scaffolding only — implementation is via agent session.
        cmd = [sys.executable, str(ROOT / "agent" / "run_cycle.py")]
        subprocess.run(cmd, cwd=str(ROOT), check=False)

        state = load_state()
        used = submissions_for_day(state, day_key)
        if used >= limit:
            print("[daily-loop] quota done after cycle")
            return 0

        next_t = now() + timedelta(seconds=INTERVAL_SEC)
        # Stop if next slot crosses into tomorrow's pre-1AM dead zone without quota — still ok to continue until 5
        print(f"[daily-loop] next cycle at {next_t.isoformat()}")
        sleep_until(next_t)


if __name__ == "__main__":
    sys.exit(main())
