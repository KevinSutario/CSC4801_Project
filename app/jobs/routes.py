"""Jobs routes. Owned by T10.

Employer routes require the employer role and operate only on the employer's own
jobs (ownership enforced in the service). jobs.detail is login-only and shows any
job (no closed state, D18). Every POST form carries csrf_field().
"""

from flask import abort, flash, g, redirect, render_template, request

from app.db import get_db
from app.errors import Conflict, Forbidden, NotFound, ValidationError
from app.security import login_required, role_required

from . import bp
from . import service


def _form_values() -> dict:
    f = request.form
    return {
        "title": f.get("title", ""),
        "description": f.get("description", ""),
        "location": f.get("location", ""),
        "employment_type": f.get("employment_type", ""),
        "salary_min": f.get("salary_min", ""),
        "salary_max": f.get("salary_max", ""),
        "skills_text": f.get("skills", ""),
    }


@bp.get("/employer/jobs")
@role_required("employer")
def my_jobs():
    jobs = service.list_jobs_for_employer(get_db(), g.user["id"])
    return render_template("jobs/list.html", jobs=jobs)


@bp.route("/employer/jobs/new", methods=["GET", "POST"])
@role_required("employer")
def new():
    conn = get_db()
    if request.method == "POST":
        values = _form_values()
        try:
            job_id = service.create_job(conn, g.user["id"], **values)
        except ValidationError as exc:
            return render_template("jobs/form.html", errors=exc.errors, job=values,
                                   mode="new"), 400
        flash("Job posted", "success")
        return redirect(f"/jobs/{job_id}")
    return render_template("jobs/form.html", errors={}, job={}, mode="new")


@bp.route("/employer/jobs/<int:job_id>/edit", methods=["GET", "POST"])
@role_required("employer")
def edit(job_id: int):
    conn = get_db()
    try:
        service.get_owned_job(conn, g.user["id"], job_id)  # ownership check
    except NotFound:
        abort(404)
    except Forbidden:
        abort(403)
    if request.method == "POST":
        values = _form_values()
        try:
            service.update_job(conn, g.user["id"], job_id, **values)
        except ValidationError as exc:
            values["id"] = job_id
            return render_template("jobs/form.html", errors=exc.errors, job=values,
                                   mode="edit"), 400
        flash("Job updated", "success")
        return redirect(f"/jobs/{job_id}")
    # GET: prefill from the stored job plus its skills
    full = service.get_job(conn, job_id)
    full["skills_text"] = ", ".join(full["skills"])
    return render_template("jobs/form.html", errors={}, job=full, mode="edit")


@bp.get("/employer/jobs/<int:job_id>/delete")
@role_required("employer")
def confirm_delete(job_id: int):
    conn = get_db()
    try:
        service.get_owned_job(conn, g.user["id"], job_id)
    except NotFound:
        abort(404)
    except Forbidden:
        abort(403)
    job = service.get_job(conn, job_id)
    dependants = service.count_dependants(conn, job_id)
    return render_template("jobs/confirm_delete.html", job=job, dependants=dependants)


@bp.post("/employer/jobs/<int:job_id>/delete")
@role_required("employer")
def delete(job_id: int):
    conn = get_db()
    try:
        service.delete_job(conn, g.user["id"], job_id)
    except NotFound:
        abort(404)
    except Forbidden:
        abort(403)
    except Conflict as exc:
        raise exc  # handled by the 409 error handler
    flash("Job deleted", "success")
    return redirect("/employer/jobs")


@bp.get("/jobs/<int:job_id>")
@login_required
def detail(job_id: int):
    try:
        job = service.get_job(get_db(), job_id)
    except NotFound:
        abort(404)
    return render_template("jobs/detail.html", job=job)
