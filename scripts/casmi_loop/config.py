"""Paths, competition constants, and secret loading. Never print secret values."""

from __future__ import annotations

import os
from datetime import date
from pathlib import Path

COMPETITION = "enveda-CASMI26-molecule-id-mass-spectra"
KERNEL = "ilakkmanoharan/casmi26-retrieval-symbolic-v01"
TIMEZONE = "America/Chicago"
# Competition day starts at 01:00 America/Chicago (not midnight).
DAY_START_HOUR = 1
MAX_SUBMITS_PER_DAY = 5
LAST_SUBMIT_DATE = date(2026, 12, 31)

ROOT = Path(__file__).resolve().parents[2]
STATE_FILE = ROOT / "agent" / "state.json"
KERNEL_DIR = ROOT / "kaggle_kernel"
PACKAGE_DIR = ROOT / "casmi26"


def secret(name: str) -> str | None:
    env = os.environ.get(name)
    if env and env.strip():
        return env.strip()
    return None


def require_secret(name: str) -> str:
    value = secret(name)
    if not value:
        raise SystemExit(
            "missing %s (set GitHub Actions secret or env var)" % name
        )
    return value


def github_repo_url() -> str | None:
    explicit = os.environ.get("CASMI_LOOP_REPO_URL") or os.environ.get("GITHUB_REPO_URL")
    if explicit:
        return explicit.rstrip(".git")
    slug = os.environ.get("GITHUB_REPOSITORY")
    if slug:
        return "https://github.com/%s" % slug
    return "https://github.com/ilakkmanoharan/casmi26-structure-prediction"


def tag_for(day: date, slot: int) -> str:
    return "%s_cycle%02d" % (day.isoformat(), slot)
