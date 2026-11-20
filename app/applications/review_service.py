"""Employer applicant review (FP-EMP-3). Owned by T15.

list_applicants returns, per applicant, exactly the keys in 07-CONTRACTS, scored
by the shared engine and sorted score desc, then case-insensitive candidate name,
then candidate id (D15). set_status moves an application between the four statuses
without ever touching its booking (FP-SCHED-2).
"""

import sqlite3

from app import audit
from app.db import now_iso, transaction
from app.errors import Forbidden, NotFound, ValidationError
from app.jobs.service import get_owned_job
from app.matching.engine import score

from .statuses import STATUSES


def list_applicants(conn: sqlite3.Connection, employer_id: int, job_id: int) -> list[dict]:
    """Applicants for the employer's own job, scored and ordered per FP-EMP-3/D15.

    Fixed query count: get_owned_job, then one query each for applications,
    candidate skills, and bookings.
    """
    get_owned_job(conn, employer_id, job_id)  # Forbidden/NotFound

    job_skills = {
        r["name"] for r in conn.execute(
            "SELECT s.name FROM job_skills js JOIN skills s ON s.id = js.skill_id"
            " WHERE js.job_id = ?",
            (job_id,),
        )
    }

    app_rows = conn.execute(
        "SELECT a.id AS application_id, a.candidate_id, a.status, a.created_at AS applied_at,"
        " u.display_name AS candidate_name, p.headline AS headline"
        " FROM applications a"
        " JOIN users u ON u.id = a.candidate_id"
        " LEFT JOIN candidate_profiles p ON p.user_id = a.candidate_id"
        " WHERE a.job_id = ?",
        (job_id,),
    ).fetchall()
    if not app_rows:
        return []

    candidate_ids = [r["candidate_id"] for r in app_rows]

    skills_by_candidate: dict[int, list[str]] = {cid: [] for cid in candidate_ids}
    for r in conn.execute(
        "SELECT cs.candidate_id, s.name FROM candidate_skills cs"
        " JOIN skills s ON s.id = cs.skill_id"
        " JOIN applications a ON a.candidate_id = cs.candidate_id"
        " WHERE a.job_id = ? ORDER BY s.name",
        (job_id,),
    ):
        if r["candidate_id"] in skills_by_candidate:
            skills_by_candidate[r["candidate_id"]].append(r["name"])

    booking_by_app: dict[int, dict] = {}
    for r in conn.execute(
        "SELECT b.application_id, b.slot_id, s.starts_at, s.ends_at"
        " FROM bookings b JOIN interview_slots s ON s.id = b.slot_id"
        " JOIN applications a ON a.id = b.application_id"
        " WHERE a.job_id = ?",
        (job_id,),
    ):
        booking_by_app[r["application_id"]] = {
            "slot_id": r["slot_id"], "starts_at": r["starts_at"], "ends_at": r["ends_at"],
        }

    applicants: list[dict] = []
    for r in app_rows:
        skills = skills_by_candidate.get(r["candidate_id"], [])
        result = score(set(skills), job_skills)
        applicants.append({
            "application_id": r["application_id"],
            "candidate_id": r["candidate_id"],
            "candidate_name": r["candidate_name"],
            "headline": r["headline"] or "",
            "skills": sorted(skills),
            "score": result["score"],
            "matched": result["matched"],
            "missing": result["missing"],
            "status": r["status"],
            "applied_at": r["applied_at"],
            "booking": booking_by_app.get(r["application_id"]),
        })

    applicants.sort(
        key=lambda a: (-a["score"], a["candidate_name"].lower(), a["candidate_id"])
    )
    return applicants


def set_status(conn: sqlite3.Connection, employer_id: int, application_id: int,
               new_status: str) -> None:
    """Set an application's status (owner only). Never touches its booking."""
    row = conn.execute(
        "SELECT a.id, a.status, c.owner_id AS owner_id FROM applications a"
        " JOIN jobs j ON j.id = a.job_id JOIN companies c ON c.id = j.company_id"
        " WHERE a.id = ?",
        (application_id,),
    ).fetchone()
    if row is None:
        raise NotFound()
    if row["owner_id"] != employer_id:
        raise Forbidden()
    if new_status not in STATUSES:
        raise ValidationError({"status": "Choose a valid status."})
    if new_status == row["status"]:
        raise ValidationError({"status": "The application already has that status."})
    with transaction(conn):
        conn.execute(
            "UPDATE applications SET status = ?, updated_at = ? WHERE id = ?",
            (new_status, now_iso(), application_id),
        )
        audit.log_event(conn, employer_id, "application.status", "application",
                        application_id, f"{row['status']} -> {new_status}")
