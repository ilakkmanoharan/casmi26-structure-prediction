"""Persisted per-day slot bookkeeping in agent/state.json."""

from __future__ import annotations

import json
from datetime import date
from typing import Any

from .config import COMPETITION, KERNEL, MAX_SUBMITS_PER_DAY, STATE_FILE


def _default() -> dict[str, Any]:
    return {
        "competition": COMPETITION,
        "daily_limit": MAX_SUBMITS_PER_DAY,
        "interval_minutes": 60,
        "day_start_local": "01:00",
        "timezone": "America/Chicago",
        "best_public_score": None,
        "github_actions": {
            "enabled": True,
            "workflow": ".github/workflows/casmi-loop.yml",
            "secrets": ["OPENAI_API_KEY", "KAGGLE_USERNAME", "KAGGLE_KEY"],
            "kernel": KERNEL,
            "primary_runner": True,
        },
        "cycles": [],
    }


def load() -> dict[str, Any]:
    if not STATE_FILE.is_file():
        return _default()
    try:
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return _default()
    data.setdefault("cycles", [])
    data.setdefault("daily_limit", MAX_SUBMITS_PER_DAY)
    return data


def save(data: dict[str, Any]) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def submitted_slots(day: date, data: dict[str, Any] | None = None) -> set[int]:
    data = load() if data is None else data
    day_s = day.isoformat()
    out: set[int] = set()
    for c in data.get("cycles", []):
        if c.get("day") != day_s:
            continue
        if c.get("submitted") or c.get("submit_ref") or c.get("kaggle_id"):
            try:
                out.add(int(c.get("cycle", 0)))
            except (TypeError, ValueError):
                continue
    return out


def next_unused_slot(day: date, data: dict[str, Any] | None = None) -> int | None:
    used = submitted_slots(day, data)
    for slot in (1, 2, 3, 4, 5):
        if slot not in used:
            return slot
    return None


def append_cycle(record: dict[str, Any]) -> dict[str, Any]:
    data = load()
    data.setdefault("cycles", []).append(record)
    score = record.get("public_score")
    if score is not None:
        try:
            score_f = float(score)
            best = data.get("best_public_score")
            if best is None or score_f > float(best):
                data["best_public_score"] = score_f
        except (TypeError, ValueError):
            pass
    save(data)
    return record
