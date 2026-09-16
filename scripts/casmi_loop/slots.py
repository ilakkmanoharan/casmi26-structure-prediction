"""Competition-day clock helpers (America/Chicago, day starts 01:00)."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from .config import DAY_START_HOUR, TIMEZONE


def now_local(now: datetime | None = None) -> datetime:
    tz = ZoneInfo(TIMEZONE)
    if now is None:
        return datetime.now(tz)
    if now.tzinfo is None:
        return now.replace(tzinfo=tz)
    return now.astimezone(tz)


def competition_day(now: datetime | None = None) -> date:
    """Day key anchored at 01:00 America/Chicago."""
    local = now_local(now)
    anchor = local.replace(hour=DAY_START_HOUR, minute=0, second=0, microsecond=0)
    if local < anchor:
        anchor -= timedelta(days=1)
    return anchor.date()
