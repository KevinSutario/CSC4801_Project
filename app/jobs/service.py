"""Jobs service. Owned by T10.

Create/edit/delete jobs with a required-skills list (may be empty). No cascade on
delete: a job with any application cannot be deleted (409). No open/closed state
(D18). All limits are DEFAULT (not in brief) per the T10 card. Writes are audited.
"""

import sqlite3

from app import audit
from app.db import now_iso, transaction
from app.errors import Conflict, Forbidden, NotFound, ValidationError
from app.skills import get_or_create_skill_ids, parse_skill_list

EMPLOYMENT_TYPES: tuple[str, ...] = ("full-time", "part-time", "contract", "internship")

_TITLE_MAX = 120
_DESC_MAX = 5000
_LOCATION_MAX = 80
_SALARY_MAX = 10_000_000
_SKILLS_MAX = 30


def _parse_salary(raw: str, field: str, errors: dict) -> int | None:
    """Parse a salary form string. '' -> None. Reject non-numbers and out-of-range."""
    text = (raw or "").strip()
    if text == "":
        return None
    try:
        value = int(text)
    except ValueError:
        errors[field] = "Salary must be a whole number."
        return None
    if value < 0 or value > _SALARY_MAX:
        errors[field] = f"Salary must be between 0 and {_SALARY_MAX}."
        return None
    return value


def _validate(title, description, location, employment_type, salary_min, salary_max,
              skills_text) -> tuple[dict, dict]:
    """Return (clean, errors). errors empty when valid."""
    errors: dict[str, str] = {}
    clean: dict = {}

    clean["title"] = (title or "").strip()
    if not (1 <= len(clean["title"]) <= _TITLE_MAX):
        errors["title"] = f"Title is required (1 to {_TITLE_MAX} characters)."

    clean["description"] = (description or "").strip()
    if not (1 <= len(clean["description"]) <= _DESC_MAX):
        errors["description"] = f"Description is required (1 to {_DESC_MAX} characters)."

    clean["location"] = (location or "").strip()
    if len(clean["location"]) > _LOCATION_MAX:
        errors["location"] = f"Location must be at most {_LOCATION_MAX} characters."

    clean["employment_type"] = (employment_type or "").strip()
    if clean["employment_type"] not in EMPLOYMENT_TYPES:
        errors["employment_type"] = "Choose a valid employment type."

    smin = _parse_salary(salary_min, "salary_min", errors)
    smax = _parse_salary(salary_max, "salary_max", errors)
    if smin is not None and smax is not None and smin > smax:
        errors["salary_max"] = "Maximum salary must be at least the minimum."
    clean["salary_min"] = smin
    clean["salary_max"] = smax

    clean["skills"] = parse_skill_list(skills_text or "")
    if len(clean["skills"]) > _SKILLS_MAX:
        errors["skills"] = f"At most {_SKILLS_MAX} skills."

    return clean, errors


def _company_id_for(conn: sqlite3.Connection, employer_id: int) -> int | None:
    row = conn.execute(
        "SELECT id FROM companies WHERE owner_id = ?", (employer_id,)
    ).fetchone()
    return row["id"] if row else None


def _set_skills(conn: sqlite3.Connection, job_id: int, skills: list[str]) -> None:
    conn.execute("DELETE FROM job_skills WHERE job_id = ?", (job_id,))
    for skill_id in get_or_create_skill_ids(conn, skills):
        conn.execute(
            "INSERT OR IGNORE INTO job_skills (job_id, skill_id) VALUES (?, ?)",
            (job_id, skill_id),
        )


def create_job(conn: sqlite3.Connection, employer_id: int, title: str, description: str,
               location: str, employment_type: str, salary_min: str, salary_max: str,
               skills_text: str) -> int:
    """Create a job for the employer's company. Returns the job id."""
    clean, errors = _validate(title, description, location, employment_type,
                              salary_min, salary_max, skills_text)
    company_id = _company_id_for(conn, employer_id)
    if company_id is None:
        errors["company"] = "Create your company profile first."
    if errors:
        raise ValidationError(errors)
    with transaction(conn):
        cursor = conn.execute(
            "INSERT INTO jobs (company_id, title, description, location, employment_type,"
            " salary_min, salary_max, created_at, updated_at)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (company_id, clean["title"], clean["description"], clean["location"],
             clean["employment_type"], clean["salary_min"], clean["salary_max"],
             now_iso(), now_iso()),
        )
        job_id = cursor.lastrowid
        _set_skills(conn, job_id, clean["skills"])
        audit.log_event(conn, employer_id, "job.create", "job", job_id)
    return job_id


def update_job(conn: sqlite3.Connection, employer_id: int, job_id: int, title: str,
               description: str, location: str, employment_type: str, salary_min: str,
               salary_max: str, skills_text: str) -> None:
    """Update the employer's own job. Forbidden/NotFound via get_owned_job."""
    get_owned_job(conn, employer_id, job_id)
    clean, errors = _validate(title, description, location, employment_type,
                              salary_min, salary_max, skills_text)
    if errors:
        raise ValidationError(errors)
    with transaction(conn):
        conn.execute(
            "UPDATE jobs SET title=?, description=?, location=?, employment_type=?,"
            " salary_min=?, salary_max=?, updated_at=? WHERE id=?",
            (clean["title"], clean["description"], clean["location"], clean["employment_type"],
             clean["salary_min"], clean["salary_max"], now_iso(), job_id),
        )
        _set_skills(conn, job_id, clean["skills"])
        audit.log_event(conn, employer_id, "job.update", "job", job_id)


def count_dependants(conn: sqlite3.Connection, job_id: int) -> int:
    """Number of applications on the job (its only dependants; slots are employer-owned)."""
    return conn.execute(
        "SELECT COUNT(*) AS n FROM applications WHERE job_id = ?", (job_id,)
    ).fetchone()["n"]


def delete_job(conn: sqlite3.Connection, employer_id: int, job_id: int) -> None:
    """Delete the employer's own job. Conflict (409) if it has any application."""
    get_owned_job(conn, employer_id, job_id)
    if count_dependants(conn, job_id) > 0:
        raise Conflict("This job has applications and cannot be deleted.")
    with transaction(conn):
        conn.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
        audit.log_event(conn, employer_id, "job.delete", "job", job_id)


def get_owned_job(conn: sqlite3.Connection, employer_id: int, job_id: int) -> dict:
    """Return the job row (as dict) if the employer owns it. NotFound/Forbidden otherwise."""
    row = conn.execute(
        "SELECT j.*, c.owner_id AS owner_id FROM jobs j"
        " JOIN companies c ON c.id = j.company_id WHERE j.id = ?",
        (job_id,),
    ).fetchone()
    if row is None:
        raise NotFound()
    if row["owner_id"] != employer_id:
        raise Forbidden()
    return dict(row)


def get_job(conn: sqlite3.Connection, job_id: int) -> dict:
    """A job with company_name and skills. NotFound if missing."""
    row = conn.execute(
        "SELECT j.*, c.name AS company_name FROM jobs j"
        " JOIN companies c ON c.id = j.company_id WHERE j.id = ?",
        (job_id,),
    ).fetchone()
    if row is None:
        raise NotFound()
    job = dict(row)
    job["skills"] = [
        r["name"] for r in conn.execute(
            "SELECT s.name FROM job_skills js JOIN skills s ON s.id = js.skill_id"
            " WHERE js.job_id = ? ORDER BY s.name",
            (job_id,),
        )
    ]
    return job


def _attach_skills(job_rows: list, skill_rows: list) -> list[dict]:
    """Group skill_rows (job_id, name) onto job rows. No SQL here — fixed query count."""
    jobs = [dict(r) for r in job_rows]
    skills_by_job: dict[int, list[str]] = {j["id"]: [] for j in jobs}
    for r in skill_rows:
        if r["job_id"] in skills_by_job:
            skills_by_job[r["job_id"]].append(r["name"])
    for j in jobs:
        j["skills"] = skills_by_job[j["id"]]
    return jobs


def list_jobs(conn: sqlite3.Connection) -> list[dict]:
    """Every job with company_name and skills (two queries, independent of job count)."""
    rows = conn.execute(
        "SELECT j.*, c.name AS company_name FROM jobs j"
        " JOIN companies c ON c.id = j.company_id ORDER BY j.created_at DESC, j.id DESC"
    ).fetchall()
    skill_rows = conn.execute(
        "SELECT js.job_id, s.name FROM job_skills js JOIN skills s ON s.id = js.skill_id"
        " ORDER BY s.name"
    ).fetchall()
    return _attach_skills(rows, skill_rows)


def list_jobs_for_employer(conn: sqlite3.Connection, employer_id: int) -> list[dict]:
    """The employer's own jobs with company_name and skills (two queries, bound by owner)."""
    rows = conn.execute(
        "SELECT j.*, c.name AS company_name FROM jobs j"
        " JOIN companies c ON c.id = j.company_id WHERE c.owner_id = ?"
        " ORDER BY j.created_at DESC, j.id DESC",
        (employer_id,),
    ).fetchall()
    skill_rows = conn.execute(
        "SELECT js.job_id, s.name FROM job_skills js JOIN skills s ON s.id = js.skill_id"
        " JOIN jobs j ON j.id = js.job_id JOIN companies c ON c.id = j.company_id"
        " WHERE c.owner_id = ? ORDER BY s.name",
        (employer_id,),
    ).fetchall()
    return _attach_skills(rows, skill_rows)
