"""Time and datetime utilities in UTC."""

from datetime import datetime, timezone


def utcnow() -> datetime:
    """Return the current datetime in UTC with timezone set."""
    return datetime.now(timezone.utc)


def format_iso(dt: datetime | None = None) -> str:
    """Format a datetime to standard ISO-8601 string in UTC."""
    target = dt or utcnow()
    if target.tzinfo is None:
        target = target.replace(tzinfo=timezone.utc)
    return target.isoformat()


def parse_iso(iso_str: str) -> datetime:
    """Parse an ISO-8601 string to timezone-aware UTC datetime."""
    dt = datetime.fromisoformat(iso_str)
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)
