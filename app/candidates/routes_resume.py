"""Candidate resume entry and owner-only viewing routes."""

from flask import flash, g, redirect, render_template, request

from app.db import get_db
from app.errors import ValidationError
from app.security import login_required, role_required

from . import bp
from . import resume_service


@bp.route("/candidate/resume", methods=["GET", "POST"])
@login_required
@role_required("candidate")
def resume():
    conn = get_db()
    current = resume_service.get_resume(conn, g.user["id"])
    body = current["body"] if current else ""
    error = None
    if request.method == "POST":
        body = request.form.get("body", "")
        try:
            resume_service.save_resume(conn, g.user["id"], body)
        except ValidationError as exc:
            error = exc.errors.get("body")
        else:
            flash("Resume saved", "success")
            return redirect("/candidate/resume")
    response = render_template("candidates/resume.html", body=body, error=error)
    return response, (400 if error else 200)


@bp.get("/candidates/<int:candidate_id>/resume")
@login_required
def resume_view(candidate_id: int):
    resume = resume_service.get_resume_for_viewer(
        get_db(), g.user["id"], candidate_id
    )
    return render_template(
        "candidates/resume.html", body=resume["body"], error=None, read_only=True
    )
