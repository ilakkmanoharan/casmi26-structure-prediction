#!/usr/bin/env python3
"""Run a single CASMI daily-agent cycle (research → submit hooks)."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
TZ = ZoneInfo("America/Chicago")
STATE_PATH = ROOT / "agent" / "state.json"


def now_cst() -> datetime:
    return datetime.now(TZ)


def load_state() -> dict:
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text())
    return {
        "competition": "enveda-CASMI26-molecule-id-mass-spectra",
        "daily_limit": 5,
        "cycles": [],
        "best_public_score": None,
    }


def save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2, default=str))


def competition_day_key(dt: datetime) -> str:
    """Competition day anchored at 01:00 America/Chicago."""
    local = dt.astimezone(TZ)
    anchor = local.replace(hour=1, minute=0, second=0, microsecond=0)
    if local < anchor:
        # still previous competition day
        from datetime import timedelta

        anchor = anchor - timedelta(days=1)
    return anchor.strftime("%Y-%m-%d")


def submissions_today(state: dict, day_key: str) -> int:
    return sum(1 for c in state.get("cycles", []) if c.get("day") == day_key and c.get("submitted"))


def next_cycle_num(state: dict, day_key: str) -> int:
    nums = [c.get("cycle", 0) for c in state.get("cycles", []) if c.get("day") == day_key]
    return (max(nums) + 1) if nums else 1


def ensure_dirs() -> None:
    for name in ("Research", "Analysis", "Hypothesis analysis", "Specs", "agent"):
        (ROOT / name).mkdir(parents=True, exist_ok=True)


def write_stub_if_missing(path: Path, body: str) -> None:
    if not path.exists():
        path.write_text(body)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cycle", type=int, default=None)
    parser.add_argument("--skip-submit", action="store_true")
    parser.add_argument("--implement-cmd", type=str, default="")
    args = parser.parse_args()

    ensure_dirs()
    state = load_state()
    dt = now_cst()
    day = competition_day_key(dt)
    used = submissions_today(state, day)
    cycle = args.cycle or next_cycle_num(state, day)
    tag = f"{day}_cycle{cycle:02d}"

    print(f"[agent] day={day} cycle={cycle} submissions_used={used}/{state['daily_limit']} now={dt.isoformat()}")
    if used >= state["daily_limit"]:
        print("[agent] daily quota exhausted — stop")
        return 0

    # Placeholders / expect human+LLM to fill; cycle runner records structure.
    write_stub_if_missing(
        ROOT / "Research" / f"{tag}_methods.md",
        f"# Research {tag}\n\n(filled by agent cycle)\n",
    )
    write_stub_if_missing(
        ROOT / "Analysis" / f"{tag}_submission.md",
        f"# Analysis {tag}\n\n(filled by agent cycle)\n",
    )
    write_stub_if_missing(
        ROOT / "Hypothesis analysis" / f"{tag}_hypotheses.md",
        f"# Hypotheses {tag}\n\n(filled by agent cycle)\n",
    )
    write_stub_if_missing(
        ROOT / "Specs" / f"{tag}_next_submission_spec.md",
        f"# Spec {tag}\n\n(filled by agent cycle)\n",
    )

    submitted = False
    submit_ref = None
    if args.implement_cmd and not args.skip_submit:
        print(f"[agent] running implement_cmd: {args.implement_cmd}")
        proc = subprocess.run(args.implement_cmd, shell=True, cwd=str(ROOT))
        if proc.returncode != 0:
            print("[agent] implement_cmd failed", proc.returncode)
            return proc.returncode
        submitted = True
    elif args.skip_submit:
        print("[agent] skip-submit set")
    else:
        print("[agent] no --implement-cmd; artifacts ensured. Fill docs then implement.")

    state.setdefault("cycles", []).append(
        {
            "day": day,
            "cycle": cycle,
            "started_at": dt.isoformat(),
            "submitted": submitted,
            "submit_ref": submit_ref,
            "tag": tag,
        }
    )
    save_state(state)
    print(f"[agent] state written → {STATE_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
