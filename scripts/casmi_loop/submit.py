"""Kaggle list / kernels push / poll / competition_submit_code."""

from __future__ import annotations

import json
import os
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


DONE_STATES = ("COMPLETE", "COMPLETED", "SUCCESS")
FAIL_STATES = ("ERROR", "FAILED", "CANCELLED", "CANCELED", "CANCEL_REQUESTED", "CANCEL_ACKNOWLEDGED")
ACTIVE_STATES = ("QUEUED", "RUNNING", "PENDING", "STARTING")


def _status_text(status: Any) -> str:
    """Normalize Kaggle status (enum, dict, or response object) to a bare word."""
    raw = None
    for getter in (
        lambda: getattr(status, "status", None),
        lambda: status.get("status") if isinstance(status, dict) else None,
        lambda: getattr(status, "_status", None),
    ):
        raw = getter()
        if raw is not None:
            break
    if raw is None:
        return ""
    # Enums stringify as 'KernelWorkerStatus.ERROR'; prefer .name.
    text = str(getattr(raw, "name", raw))
    return text.rsplit(".", 1)[-1].strip().upper()


def _failure_message(status: Any) -> str | None:
    for attr in ("failure_message", "failureMessage", "_failure_message"):
        val = getattr(status, attr, None)
        if val:
            return str(val)
    return None


def kernel_log_tail(lines: int = 25) -> str:
    """Best-effort tail of the kernel log, for diagnosing a failed run."""
    import json
    import tempfile
    from pathlib import Path

    api = authenticate()
    try:
        with tempfile.TemporaryDirectory() as tmp:
            api.kernels_output(KERNEL, path=tmp)
            logs = list(Path(tmp).glob("*.log"))
            if not logs:
                return "(no kernel log found)"
            rows = json.loads(logs[0].read_text(encoding="utf-8"))
            texts = [str(r.get("data", "")).rstrip() for r in rows]
            return "\n".join(t for t in texts[-lines:] if t)
    except Exception as exc:
        return "(could not read kernel log: %s)" % exc


def wait_kernel_complete(
    *,
    timeout_sec: int | None = None,
    poll_sec: int = 60,
    stale_guard_sec: int = 600,
) -> dict[str, Any]:
    """Poll until the kernel finishes.

    A terminal status seen before the new version starts is the *previous*
    run, so ignore terminal states until we observe an active one or
    stale_guard_sec elapses.
    """
    if timeout_sec is None:
        timeout_sec = int(os.environ.get("CASMI_KERNEL_TIMEOUT_SEC", 5 * 3600))
    api = authenticate()
    started = time.time()
    deadline = started + timeout_sec
    seen_active = False
    state_s = ""

    while time.time() < deadline:
        try:
            status = api.kernels_status(KERNEL)
            state_s = _status_text(status)
            elapsed = int(time.time() - started)
            print("kernel status %s (%ss)" % (state_s or "UNKNOWN", elapsed))

            if state_s in ACTIVE_STATES:
                seen_active = True
            elif state_s in DONE_STATES:
                if seen_active or elapsed >= stale_guard_sec:
                    return {"status": state_s, "elapsed_sec": elapsed}
                print("ignoring stale COMPLETE from previous version")
            elif state_s in FAIL_STATES:
                if seen_active or elapsed >= stale_guard_sec:
                    detail = _failure_message(status) or "(no failureMessage)"
                    raise SystemExit(
                        "kernel %s: %s\n--- kernel log tail ---\n%s"
                        % (state_s, detail, kernel_log_tail())
                    )
                print("ignoring stale %s from previous version" % state_s)
        except SystemExit:
            raise
        except Exception as exc:
            print("status poll error:", exc)
        time.sleep(poll_sec)

    raise SystemExit(
        "kernel poll timed out after %ss (last status %s)" % (timeout_sec, state_s or "UNKNOWN")
    )


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
