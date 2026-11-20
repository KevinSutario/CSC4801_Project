"""Candidate application confirmation and listing routes."""

from flask import flash, g, redirect, render_template, request

from app.db import get_db
from app.errors import Conflict, ValidationError
from app.jobs.service import get_job
from app.security import role_required

from . import bp, service
from .statuses import LABELS

_BADGE_TONES = {
    "pending": "pending",
    "interviewing": "info",
    "rejected": "danger",
    "accepted": "success",
}


@bp.get("/jobs/<int:job_id>/apply")
@role_required("candidate")
def confirm(job_id: int):
    conn = get_db()
    job = get_job(conn, job_id)
    return render_template(
        "applications/confirm.html", job=job, cover_note="", message=None, error=None
    )


@bp.post("/jobs/<int:job_id>/apply")
@role_required("candidate")
def submit(job_id: int):
    conn = get_db()
    job = get_job(conn, job_id)
    cover_note = request.form.get("cover_note", "")
    try:
        service.apply(conn, g.user["id"], job_id, cover_note)
    except Conflict as exc:
        return render_template(
            "applications/confirm.html", job=job, cover_note=cover_note,
            message=exc.message, error=None,
        ), 409
    except ValidationError as exc:
        error = exc.errors.get("cover_note")
        return render_template(
            "applications/confirm.html", job=job, cover_note=cover_note,
            message=None, error=error,
        ), 400
    flash(f"Application sent to {job['company_name']}", "success")
    return redirect("/candidate/applications")


@bp.get("/candidate/applications")
@role_required("candidate")
def mine():
    applications = service.list_for_candidate(get_db(), g.user["id"])
    return render_template(
        "applications/mine.html", applications=applications, labels=LABELS,
        badge_tones=_BADGE_TONES,
    )
