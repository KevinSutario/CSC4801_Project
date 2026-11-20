"""Candidate application operations."""

import sqlite3

from app import audit
from app.db import now_iso, transaction
from app.errors import Conflict, Forbidden, NotFound, ValidationError
from app.jobs.service import get_job


def apply(conn: sqlite3.Connection, candidate_id: int, job_id: int, cover_note: str) -> int:
    """Apply once to an existing job, returning the new application id."""
    get_job(conn, job_id)
    cover_note = cover_note.strip()
    if len(cover_note) > 2000:
        raise ValidationError({"cover_note": "Cover note must be 2000 characters or fewer."})
    existing = conn.execute(
        "SELECT id FROM applications WHERE job_id = ? AND candidate_id = ?",
        (job_id, candidate_id),
    ).fetchone()
    if existing:
        raise Conflict("You have already applied to this job.")
    try:
        with transaction(conn, immediate=True):
            cursor = conn.execute(
                "INSERT INTO applications"
                " (job_id, candidate_id, status, cover_note, created_at, updated_at)"
                " VALUES (?, ?, 'pending', ?, ?, ?)",
                (job_id, candidate_id, cover_note, now_iso(), now_iso()),
            )
            application_id = cursor.lastrowid
            audit.log_event(conn, candidate_id, "application.submit", "application", application_id)
    except sqlite3.IntegrityError as exc:
        if "uq_application" in str(exc) or "UNIQUE constraint failed" in str(exc):
            raise Conflict("You have already applied to this job.") from exc
        raise
    return application_id


def get_own_application(
    conn: sqlite3.Connection, candidate_id: int, application_id: int
) -> dict:
    """Fetch one application with job, company and optional booking data."""
    row = conn.execute(
        "SELECT a.id, a.job_id, a.candidate_id, a.status, a.cover_note, a.created_at,"
        " j.title AS job_title, j.location, j.employment_type,"
        " c.name AS company_name, b.slot_id, s.starts_at, s.ends_at"
        " FROM applications AS a"
        " JOIN jobs AS j ON j.id = a.job_id"
        " JOIN companies AS c ON c.id = j.company_id"
        " LEFT JOIN bookings AS b ON b.application_id = a.id"
        " LEFT JOIN interview_slots AS s ON s.id = b.slot_id"
        " WHERE a.id = ?",
        (application_id,),
    ).fetchone()
    if row is None:
        raise NotFound()
    if row["candidate_id"] != candidate_id:
        raise Forbidden()
    application = dict(row)
    slot_id = application.pop("slot_id")
    starts_at = application.pop("starts_at")
    ends_at = application.pop("ends_at")
    application["booking"] = (
        {"slot_id": slot_id, "starts_at": starts_at, "ends_at": ends_at}
        if slot_id is not None else None
    )
    return application


def list_for_candidate(conn: sqlite3.Connection, candidate_id: int) -> list[dict]:
    """List the candidate's applications newest first, including optional bookings."""
    rows = conn.execute(
        "SELECT a.id, a.job_id, a.candidate_id, a.status, a.cover_note, a.created_at,"
        " j.title AS job_title, j.location, j.employment_type,"
        " c.name AS company_name, b.slot_id, s.starts_at, s.ends_at"
        " FROM applications AS a"
        " JOIN jobs AS j ON j.id = a.job_id"
        " JOIN companies AS c ON c.id = j.company_id"
        " LEFT JOIN bookings AS b ON b.application_id = a.id"
        " LEFT JOIN interview_slots AS s ON s.id = b.slot_id"
        " WHERE a.candidate_id = ? ORDER BY a.created_at DESC, a.id DESC",
        (candidate_id,),
    ).fetchall()
    applications = []
    for row in rows:
        application = dict(row)
        slot_id = application.pop("slot_id")
        starts_at = application.pop("starts_at")
        ends_at = application.pop("ends_at")
        application["booking"] = (
            {"slot_id": slot_id, "starts_at": starts_at, "ends_at": ends_at}
            if slot_id is not None else None
        )
        applications.append(application)
    return applications
