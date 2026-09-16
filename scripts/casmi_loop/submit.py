"""Kaggle list / kernels push / poll / competition_submit_code."""

from __future__ import annotations

import json
import subprocess
import time
from typing import Any

from .config import COMPETITION, KERNEL, KERNEL_DIR


def authenticate() -> Any:
    from kaggle.api.kaggle_api_extended import KaggleApi

    api = KaggleApi()
    try:
        api.authenticate()
    except Exception as exc:
        raise SystemExit(
            "Kaggle auth failed (%s). Set secrets KAGGLE_USERNAME and KAGGLE_KEY." % exc
        ) from exc
    return api


def list_submissions(limit: int = 20) -> list[dict[str, Any]]:
    api = authenticate()
    rows = []
    for s in (api.competition_submissions(COMPETITION) or [])[:limit]:
        rows.append(
            {
                "ref": getattr(s, "ref", None),
                "publicScore": getattr(s, "publicScore", None),
                "privateScore": getattr(s, "privateScore", None),
                "date": str(getattr(s, "date", "")),
                "description": getattr(s, "description", None),
                "status": str(getattr(s, "status", "")),
                "fileName": getattr(s, "fileName", None),
            }
        )
    return rows


def briefing_from_submissions(subs: list[dict[str, Any]]) -> str:
    lines = ["Recent Kaggle submissions (newest first):"]
    for s in subs[:10]:
        lines.append(
            "- id=%s score=%s status=%s desc=%s"
            % (s.get("ref"), s.get("publicScore"), s.get("status"), s.get("description"))
        )
    if not subs:
        lines.append("(none yet)")
    return "\n".join(lines)


def kernels_push() -> dict[str, Any]:
    if not (KERNEL_DIR / "kernel-metadata.json").is_file():
        raise SystemExit("missing %s/kernel-metadata.json" % KERNEL_DIR)
    proc = subprocess.run(
        ["kaggle", "kernels", "push", "-p", str(KERNEL_DIR)],
        capture_output=True,
        text=True,
    )
    out = (proc.stdout or "") + "\n" + (proc.stderr or "")
    if proc.returncode != 0:
        raise SystemExit("kaggle kernels push failed:\n%s" % out[-2000:])
    print(out.strip())
    return {"ok": True, "output": out[-2000:]}


def wait_kernel_complete(*, timeout_sec: int = 5 * 3600, poll_sec: int = 60) -> dict[str, Any]:
    api = authenticate()
    deadline = time.time() + timeout_sec
    last = {}
    while time.time() < deadline:
        try:
            status = api.kernels_status(KERNEL)
            if hasattr(status, "__dict__"):
                last = dict(status.__dict__)
            elif isinstance(status, dict):
                last = status
            else:
                last = {"raw": str(status)}
            # common fields: status / hasStatus / failureMessage
            state = (
                last.get("status")
                or last.get("hasStatus")
                or getattr(status, "status", None)
                or ""
            )
            state_s = str(state).upper()
            print("kernel status", state_s)
            if state_s in ("COMPLETE", "COMPLETED", "SUCCESS"):
                return {"status": state_s, "detail": last}
            if state_s in ("ERROR", "FAILED", "CANCELLED", "CANCELED"):
                raise SystemExit("kernel failed: %s" % last)
        except SystemExit:
            raise
        except Exception as exc:
            print("status poll error:", exc)
        time.sleep(poll_sec)
    raise SystemExit("kernel poll timed out after %ss last=%s" % (timeout_sec, last))


def competition_submit_code(message: str) -> dict[str, Any]:
    api = authenticate()
    before = {getattr(s, "ref", None) for s in (api.competition_submissions(COMPETITION) or [])}
    result = api.competition_submit_code(
        file_name="submission.csv",
        message=message,
        competition=COMPETITION,
        kernel=KERNEL,
    )
    print("competition_submit_code result", result)
    new_id = None
    score = None
    status = "unknown"
    for _ in range(15):
        time.sleep(2)
        for s in api.competition_submissions(COMPETITION) or []:
            ref = getattr(s, "ref", None)
            if ref and ref not in before:
                new_id = ref
                score = getattr(s, "publicScore", None)
                status = str(getattr(s, "status", ""))
                break
        if new_id:
            break
    return {
        "kaggle_id": new_id,
        "publicScore": score,
        "status": status,
        "message": message,
        "kernel": KERNEL,
        "api_result": str(result),
    }


def push_and_submit(message: str, *, skip_wait: bool = False) -> dict[str, Any]:
    push = kernels_push()
    if skip_wait:
        return {"pushed": push, "skipped_wait": True}
    wait = wait_kernel_complete()
    submit = competition_submit_code(message)
    return {"pushed": push, "wait": wait, "submit": submit}
