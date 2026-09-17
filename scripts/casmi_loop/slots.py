"""Submission-day clock helpers.

Kaggle resets the 5-per-day quota at midnight UTC, so the loop counts days in
UTC. That keeps "5 submissions each day" aligned with what Kaggle enforces.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from .config import DAY_START_HOUR, TIMEZONE


def now_utc(now: datetime | None = None) -> datetime:
    if now is None:
        return datetime.now(timezone.utc)
    if now.tzinfo is None:
        return now.replace(tzinfo=timezone.utc)
    return now.astimezone(timezone.utc)


def competition_day(now: datetime | None = None) -> date:
    """Quota day key (UTC calendar date, matching Kaggle's reset)."""
    return now_utc(now).date()


def now_local(now: datetime | None = None) -> datetime:
    """Chicago wall clock, kept for cycle documentation timestamps."""
    tz = ZoneInfo(TIMEZONE)
    if now is None:
        return datetime.now(tz)
    if now.tzinfo is None:
        return now.replace(tzinfo=tz)
    return now.astimezone(tz)


def chicago_day(now: datetime | None = None) -> date:
    """Competition-clock day anchored at DAY_START_HOUR America/Chicago."""
    local = now_local(now)
    anchor = local.replace(hour=DAY_START_HOUR, minute=0, second=0, microsecond=0)
    if local < anchor:
        anchor -= timedelta(days=1)
    return anchor.date()
