"""Employer applicant routes (FP-EMP-3). Owned by T15.

The employer views applicants for their own job and moves an application between
the four statuses via a confirm screen. Ownership is enforced in the service.
"""

from flask import abort, flash, g, redirect, render_template, request

from app.db import get_db
from app.errors import Forbidden, NotFound, ValidationError
from app.security import role_required

from . import bp, review_service
from .statuses import LABELS, STATUSES

_BADGE_TONES = {
    "pending": "pending",
    "interviewing": "info",
    "rejected": "danger",
    "accepted": "success",
}


@bp.get("/employer/jobs/<int:job_id>/applicants")
@role_required("employer")
def applicants(job_id: int):
    conn = get_db()
    try:
        rows = review_service.list_applicants(conn, g.user["id"], job_id)
    except NotFound:
        abort(404)
    except Forbidden:
        abort(403)
    return render_template(
        "applications/applicants.html", job_id=job_id, applicants=rows,
        labels=LABELS, badge_tones=_BADGE_TONES, statuses=STATUSES,
    )


def _load_application_for_owner(conn, application_id: int) -> dict:
    row = conn.execute(
        "SELECT a.id, a.status, a.candidate_id, a.job_id, u.display_name AS candidate_name,"
        " c.owner_id AS owner_id FROM applications a"
        " JOIN jobs j ON j.id = a.job_id JOIN companies c ON c.id = j.company_id"
        " JOIN users u ON u.id = a.candidate_id WHERE a.id = ?",
        (application_id,),
    ).fetchone()
    if row is None:
        abort(404)
    if row["owner_id"] != g.user["id"]:
        abort(403)
    return dict(row)


@bp.get("/employer/applications/<int:application_id>/status")
@role_required("employer")
def confirm_status(application_id: int):
    conn = get_db()
    app_row = _load_application_for_owner(conn, application_id)
    to = request.args.get("to", "")
    if to not in STATUSES or to == app_row["status"]:
        abort(400)
    return render_template(
        "applications/confirm_status.html", application=app_row, to=to, labels=LABELS,
    )


@bp.post("/employer/applications/<int:application_id>/status")
@role_required("employer")
def set_status(application_id: int):
    conn = get_db()
    app_row = _load_application_for_owner(conn, application_id)
    to = request.form.get("to", "")
    try:
        review_service.set_status(conn, g.user["id"], application_id, to)
    except Forbidden:
        abort(403)
    except NotFound:
        abort(404)
    except ValidationError:
        abort(400)
    flash(f"Status changed to {LABELS.get(to, to)}", "success")
    return redirect(f"/employer/jobs/{app_row['job_id']}/applicants")
