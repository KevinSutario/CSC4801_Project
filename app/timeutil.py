"""Time zone helpers. Owned by T12. Pure module: no imports from the rest of app.

All slots are stored as UTC ISO-8601 strings ("YYYY-MM-DDTHH:MM:SSZ"). Employers
enter a local date/time plus an IANA zone name; local_to_utc converts (rejecting
local times that do not exist because of a DST jump), utc_to_local converts back
for display. The entry zone is documented per slot (interview_slots.created_tz).
"""

from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

# Zones offered in the select box (task card step 2).
COMMON_TIMEZONES: tuple[str, ...] = (
    "UTC",
    "Asia/Hong_Kong",
    "Asia/Shanghai",
    "Asia/Jakarta",
    "Asia/Singapore",
    "Europe/London",
    "America/New_York",
)

_UTC_ISO = "%Y-%m-%dT%H:%M:%SZ"


def validate_tz(name: str) -> str:
    """Return the zone name if it is a valid IANA zone; ValueError otherwise."""
    try:
        ZoneInfo(name)
    except (ZoneInfoNotFoundError, ValueError) as exc:
        raise ValueError(f"Unknown time zone: {name!r}") from exc
    return name


def local_to_utc(date_str: str, time_str: str, tz_name: str) -> str:
    """Convert a local date ("YYYY-MM-DD") and time ("HH:MM") in tz_name to a
    UTC ISO string ("YYYY-MM-DDTHH:MM:SSZ").

    ValueError for a bad date/time format, an unknown zone, or a local time that
    does not exist (DST gap): the converted time is converted back and compared
    with the input.
    """
    validate_tz(tz_name)
    try:
        naive = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    except ValueError as exc:
        raise ValueError(f"Invalid date or time: {date_str} {time_str}") from exc
    zone = ZoneInfo(tz_name)
    local = naive.replace(tzinfo=zone)
    utc = local.astimezone(timezone.utc)
    if utc.astimezone(zone).replace(tzinfo=None) != naive:
        # The wall clock never shows this time (spring-forward gap).
        raise ValueError(f"{date_str} {time_str} does not exist in {tz_name}")
    return utc.strftime(_UTC_ISO)


def utc_to_local(utc_iso: str, tz_name: str) -> datetime:
    """Convert a stored UTC ISO string to an aware datetime in tz_name."""
    return parse_iso(utc_iso).astimezone(ZoneInfo(validate_tz(tz_name)))


def format_local(utc_iso: str, tz_name: str) -> str:
    """One time point as "Mon 30 Nov 2026, 10:00 (Asia/Hong_Kong)"."""
    return utc_to_local(utc_iso, tz_name).strftime("%a %d %b %Y, %H:%M") + f" ({tz_name})"


def parse_iso(utc_iso: str) -> datetime:
    """Parse a stored UTC ISO string into an aware UTC datetime."""
    return datetime.strptime(utc_iso, _UTC_ISO).replace(tzinfo=timezone.utc)
