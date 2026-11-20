"""Recommendation queries built on the shared matching engine."""

import sqlite3

from app.candidates.profile_service import get_profile
from app.jobs.service import get_job, list_jobs

from .engine import rank, score


def recommend_for(conn: sqlite3.Connection, candidate_id: int) -> list[dict]:
    """Return every job ranked using the candidate's saved skills."""
    candidate_skills = set(get_profile(conn, candidate_id)["skills"])
    return rank(candidate_skills, list_jobs(conn))


def score_candidate_for_job(conn: sqlite3.Connection, candidate_id: int, job_id: int) -> dict:
    """Score one candidate against one existing job using the shared engine."""
    job = get_job(conn, job_id)
    candidate_skills = set(get_profile(conn, candidate_id)["skills"])
    return score(candidate_skills, set(job["skills"]))
