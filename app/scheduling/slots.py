"""Interview slot service (FP-SCHED-1). Owned by T12.

Slots belong to the employer (no job_id, D13), are exactly 30 minutes, start in
the future, are stored in UTC with the entry zone recorded, and never overlap
another slot of the same employer (overlap rule is DEFAULT, not in brief).
Booked slots cannot be deleted and are listed with booked=True so pages never
show them as available. Writes are audited (slot.create / slot.delete).
"""

import sqlite3
from datetime import datetime

from app import audit, timeutil
from app.db import now_iso, transaction
from app.errors import Conflict, Forbidden, NotFound, ValidationError


def create_slot(conn: sqlite3.Connection, employer_id: int, date_str: str, start_str: str,
                end_str: str, tz_name: str) -> int:
    """Create the employer's slot from local values in tz_name. Returns the slot id."""
    errors: dict[str, str] = {}

    try:
        timeutil.validate_tz(tz_name)
    except ValueError:
        errors["timezone"] = "Choose a valid time zone."
        tz_name = "UTC"  # placeholder; never used when errors is non-empty

    starts_at = ends_at = None
    if not errors:
        try:
            datetime.strptime(date_str, "%Y-%m-%d")  # date alone -> its own error
        except ValueError:
            errors["date"] = "Enter a valid date (YYYY-MM-DD)."
        if "date" not in errors:
            try:
                starts_at = timeutil.local_to_utc(date_str, start_str, tz_name)
            except ValueError:
                errors["start"] = "Enter a valid start time (the time must exist)."
            try:
                ends_at = timeutil.local_to_utc(date_str, end_str, tz_name)
            except ValueError:
                errors["end"] = "Enter a valid end time (the time must exist)."

    if starts_at is not None and ends_at is not None:
        if ends_at <= starts_at:
            errors["end"] = "End must be after start."
        elif (timeutil.parse_iso(ends_at) - timeutil.parse_iso(starts_at)).total_seconds() != 1800:
            errors["end"] = "A slot must be exactly 30 minutes."
        elif starts_at <= now_iso():
            errors["start"] = "Start must be in the future."
        else:
            overlap = conn.execute(
                "SELECT id FROM interview_slots WHERE employer_id = ? AND starts_at < ?"
                " AND ends_at > ?",
                (employer_id, ends_at, starts_at),
            ).fetchone()
            if overlap is not None:
                errors["start"] = "This overlaps another of your slots."

    if errors:
        raise ValidationError(errors)

    with transaction(conn):
        cursor = conn.execute(
            "INSERT INTO interview_slots (employer_id, starts_at, ends_at, created_tz,"
            " created_at) VALUES (?, ?, ?, ?, ?)",
            (employer_id, starts_at, ends_at, tz_name, now_iso()),
        )
        slot_id = cursor.lastrowid
        audit.log_event(conn, employer_id, "slot.create", "slot", slot_id,
                        f"{starts_at}/{ends_at} {tz_name}")
    return slot_id


def delete_slot(conn: sqlite3.Connection, employer_id: int, slot_id: int) -> None:
    """Delete the employer's own, unbooked slot.

    NotFound if missing; Forbidden if another employer's (D9); Conflict if booked
    (409 is DEFAULT, not in brief).
    """
    row = conn.execute(
        "SELECT id, employer_id FROM interview_slots WHERE id = ?", (slot_id,)
    ).fetchone()
    if row is None:
        raise NotFound()
    if row["employer_id"] != employer_id:
        raise Forbidden()
    booked = conn.execute(
        "SELECT 1 FROM bookings WHERE slot_id = ?", (slot_id,)
    ).fetchone()
    if booked is not None:
        raise Conflict("This slot is booked and cannot be deleted.")
    with transaction(conn):
        conn.execute("DELETE FROM interview_slots WHERE id = ?", (slot_id,))
        audit.log_event(conn, employer_id, "slot.delete", "slot", slot_id)


def list_slots_for_employer(conn: sqlite3.Connection, employer_id: int) -> list[dict]:
    """The employer's slots with a booked bool, start ascending (one query)."""
    rows = conn.execute(
        "SELECT s.id, s.starts_at, s.ends_at, s.created_tz, s.created_at,"
        " (b.id IS NOT NULL) AS booked"
        " FROM interview_slots s LEFT JOIN bookings b ON b.slot_id = s.id"
        " WHERE s.employer_id = ? ORDER BY s.starts_at ASC, s.id ASC",
        (employer_id,),
    ).fetchall()
    result = []
    for row in rows:
        slot = dict(row)
        slot["booked"] = bool(slot["booked"])
        result.append(slot)
    return result
