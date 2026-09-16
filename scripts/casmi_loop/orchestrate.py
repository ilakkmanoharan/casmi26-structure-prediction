#!/usr/bin/env python3
"""One slot of the unattended CASMI loop (GitHub Actions primary).

  python3 scripts/casmi_loop/orchestrate.py
  python3 scripts/casmi_loop/orchestrate.py --slot 1 --date 2026-09-15
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import date, datetime
from pathlib import Path

if __name__ == "__main__" and __package__ is None:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    __package__ = "scripts.casmi_loop"

from scripts.casmi_loop.chatgpt_spec import write_cycle_docs
from scripts.casmi_loop.config import KERNEL, LAST_SUBMIT_DATE, ROOT
from scripts.casmi_loop.github_push import GitPushError, push_paths
from scripts.casmi_loop.implement import apply_ablation
from scripts.casmi_loop.slots import competition_day
from scripts.casmi_loop import state
from scripts.casmi_loop.submit import (
    briefing_from_submissions,
    list_submissions,
    push_and_submit,
)


def _parse_date(raw: str | None) -> date | None:
    if not raw:
        return None
    return date.fromisoformat(raw)


def resolve_slot(args: argparse.Namespace) -> tuple[date, int] | None:
    day = _parse_date(args.date) if args.date else competition_day()
    if args.slot:
        return day, int(args.slot)
    unused = state.next_unused_slot(day)
    if unused is None:
        return None
    return day, unused


def should_push_github(submitted: bool, skip_github: bool) -> bool:
    if skip_github:
        return False
    if os.environ.get("CASMI_LOOP_PUSH") == "0":
        return False
    if submitted:
        return True
    return os.environ.get("CASMI_LOOP_PUSH") == "1"


def main() -> int:
    p = argparse.ArgumentParser(description="CASMI 5x/day GitHub Actions loop")
    p.add_argument("--slot", type=int, choices=(1, 2, 3, 4, 5))
    p.add_argument("--date", help="YYYY-MM-DD competition day (Chicago 01:00 anchor)")
    p.add_argument("--skip-submit", action="store_true")
    p.add_argument("--skip-implement", action="store_true")
    p.add_argument("--skip-github", action="store_true")
    p.add_argument("--force", action="store_true")
    args = p.parse_args()

    resolved = resolve_slot(args)
    if resolved is None:
        print("all 5 slots already submitted for this competition day; exiting")
        return 0
    day, slot = resolved
    if day > LAST_SUBMIT_DATE:
        print("past final deadline %s; no submit" % LAST_SUBMIT_DATE)
        return 0

    data = state.load()
    used = state.submitted_slots(day, data)
    if slot in used and not args.force:
        print("slot %s %s already submitted; exiting" % (day, slot))
        return 0

    print("=== casmi-loop %s slot %s ===" % (day.isoformat(), slot))
    prior_score = data.get("best_public_score")
    try:
        prior_score = float(prior_score) if prior_score is not None else None
    except (TypeError, ValueError):
        prior_score = None

    subs: list = []
    try:
        subs = list_submissions()
        print("kaggle submissions", [(s.get("ref"), s.get("publicScore"), s.get("description")) for s in subs[:5]])
        for s in subs:
            sc = s.get("publicScore")
            try:
                if sc is not None and (prior_score is None or float(sc) > prior_score):
                    prior_score = float(sc)
            except (TypeError, ValueError):
                pass
    except Exception as exc:
        print("list submissions failed:", exc)

    briefing = briefing_from_submissions(subs)
    plan = write_cycle_docs(day=day, slot=slot, briefing=briefing, prior_score=prior_score)
    print("wrote docs", plan.get("artifacts"))

    if not args.skip_implement:
        apply_ablation(plan)
    else:
        print("skip implement")

    result: dict = {"skipped": True}
    if not args.skip_submit:
        try:
            result = push_and_submit(str(plan["message"]))
        except SystemExit:
            raise
        except Exception as exc:
            print("kaggle submit failed:", exc)
            raise SystemExit("kaggle submit failed: %s" % exc) from exc
        print("submitted", json.dumps({k: result.get(k) for k in ("submit",)}, default=str)[:500])
    else:
        print("skip submit")

    submit_info = result.get("submit") or {}
    kid = submit_info.get("kaggle_id")
    pub = submit_info.get("publicScore")
    try:
        pub_f = float(pub) if pub not in (None, "") else None
    except (TypeError, ValueError):
        pub_f = None

    submitted = (not args.skip_submit) and result.get("skipped") is not True
    record = {
        "day": day.isoformat(),
        "cycle": slot,
        "tag": plan["tag"],
        "started_at": datetime.utcnow().isoformat() + "Z",
        "runner": "github_actions",
        "submitted": bool(submitted and (kid or submit_info.get("status"))),
        "skipped_reason": None if submitted else ("skip_submit" if args.skip_submit else None),
        "kernel": KERNEL,
        "kernel_version": None,
        "submit_ref": str(kid) if kid is not None else None,
        "kaggle_id": kid,
        "message": plan.get("message"),
        "prior_public_score": prior_score,
        "public_score": pub_f,
        "hypothesis": plan.get("hypothesis_id"),
        "artifacts": plan.get("artifacts"),
        "config_patch": plan.get("config_patch"),
    }
    # Mark submitted if we got an API result even when id lookup lagged.
    if submitted and not record["submitted"]:
        record["submitted"] = True
    state.append_cycle(record)
    print("state cycle recorded", record["tag"], "submitted=", record["submitted"])

    # Push docs/code after a real submit, or when CASMI_LOOP_PUSH=1 (CI default).
    push_ok = should_push_github(bool(record["submitted"]), args.skip_github)
    if not push_ok and os.environ.get("CASMI_LOOP_PUSH") == "1" and not args.skip_github:
        push_ok = True
    if push_ok:
        paths = [ROOT / rel for rel in (plan.get("artifacts") or {}).values()]
        paths.extend([ROOT / "casmi26", ROOT / "kaggle_kernel", ROOT / "agent" / "state.json"])
        msg = "Submit %s to Kaggle%s: docs + code" % (
            plan["tag"],
            " %s" % kid if kid else "",
        )
        try:
            pushed = push_paths(paths, msg)
            print("github", pushed)
        except GitPushError as exc:
            print("github push failed:", exc)
            return 2
    else:
        print("skip github push")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
