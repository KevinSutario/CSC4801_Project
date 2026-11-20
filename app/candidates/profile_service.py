"""Candidate profile and skill persistence."""

import sqlite3
from zoneinfo import available_timezones

from app import audit
from app.db import now_iso, transaction
from app.errors import ValidationError
from app.skills import get_or_create_skill_ids, parse_skill_list


def get_profile(conn: sqlite3.Connection, candidate_id: int) -> dict:
    """Return a candidate's profile with safe defaults when it is not saved yet."""
    user = conn.execute(
        "SELECT display_name FROM users WHERE id = ? AND role = 'candidate'",
        (candidate_id,),
    ).fetchone()
    if user is None:
        return {
            "display_name": "", "headline": "", "location": "", "timezone": "UTC",
            "summary": "", "skills": [], "updated_at": None,
        }
    profile = conn.execute(
        "SELECT headline, location, timezone, summary, updated_at"
        " FROM candidate_profiles WHERE user_id = ?",
        (candidate_id,),
    ).fetchone()
    skills = conn.execute(
        "SELECT s.name FROM skills AS s"
        " JOIN candidate_skills AS cs ON cs.skill_id = s.id"
        " WHERE cs.candidate_id = ? ORDER BY s.name",
        (candidate_id,),
    ).fetchall()
    return {
        "display_name": user["display_name"],
        "headline": profile["headline"] if profile else "",
        "location": profile["location"] if profile else "",
        "timezone": profile["timezone"] if profile else "UTC",
        "summary": profile["summary"] if profile else "",
        "skills": [row["name"] for row in skills],
        "updated_at": profile["updated_at"] if profile else None,
    }


def save_profile(
    conn: sqlite3.Connection,
    candidate_id: int,
    display_name: str,
    headline: str,
    location: str,
    timezone: str,
    summary: str,
    skills_text: str,
) -> None:
    """Validate and replace a candidate's profile and skills atomically."""
    display_name = display_name.strip()
    headline = headline.strip()
    location = location.strip()
    timezone = timezone.strip()
    summary = summary.strip()
    skills = parse_skill_list(skills_text)

    errors = {}
    if not 1 <= len(display_name) <= 80:
        errors["display_name"] = "Enter a display name between 1 and 80 characters."
    if len(headline) > 120:
        errors["headline"] = "Headline must be 120 characters or fewer."
    if len(location) > 80:
        errors["location"] = "Location must be 80 characters or fewer."
    if len(summary) > 2000:
        errors["summary"] = "Summary must be 2000 characters or fewer."
    if timezone not in available_timezones():
        errors["timezone"] = "Choose a valid time zone."
    if len(skills) > 30 or any(not 1 <= len(skill) <= 40 for skill in skills):
        errors["skills_text"] = "Enter up to 30 skills, each 1 to 40 characters."
    if errors:
        raise ValidationError(errors)

    with transaction(conn):
        conn.execute("UPDATE users SET display_name = ? WHERE id = ?", (display_name, candidate_id))
        conn.execute(
            "INSERT INTO candidate_profiles"
            " (user_id, headline, location, timezone, summary, updated_at)"
            " VALUES (?, ?, ?, ?, ?, ?)"
            " ON CONFLICT(user_id) DO UPDATE SET headline = excluded.headline,"
            " location = excluded.location, timezone = excluded.timezone,"
            " summary = excluded.summary, updated_at = excluded.updated_at",
            (candidate_id, headline, location, timezone, summary, now_iso()),
        )
        conn.execute("DELETE FROM candidate_skills WHERE candidate_id = ?", (candidate_id,))
        skill_ids = get_or_create_skill_ids(conn, skills)
        conn.executemany(
            "INSERT INTO candidate_skills (candidate_id, skill_id) VALUES (?, ?)",
            [(candidate_id, skill_id) for skill_id in skill_ids],
        )
        audit.log_event(conn, candidate_id, "profile.update", "user", candidate_id)
