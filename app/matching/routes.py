"""Candidate recommendation page."""

from flask import g, render_template

from app.candidates.profile_service import get_profile
from app.db import get_db
from app.security import role_required

from . import bp, service


@bp.get("/candidate/recommendations")
@role_required("candidate")
def recommendations():
    conn = get_db()
    profile = get_profile(conn, g.user["id"])
    jobs = service.recommend_for(conn, g.user["id"])
    return render_template(
        "matching/recommendations.html",
        jobs=jobs,
        has_skills=bool(profile["skills"]),
    )
