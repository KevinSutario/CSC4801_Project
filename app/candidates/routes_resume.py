"""Candidate resume entry and owner-only viewing routes."""

from flask import flash, g, redirect, render_template, request, send_file

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
    current_file = resume_service.get_resume_file(conn, g.user["id"])
    body = current["body"] if current else ""
    error = None
    file_error = None
    if request.method == "POST":
        body = request.form.get("body", "")
        try:
            resume_service.save_resume(conn, g.user["id"], body)
        except ValidationError as exc:
            error = exc.errors.get("body")
        else:
            flash("Resume saved", "success")
            return redirect("/candidate/resume")
    response = render_template(
        "candidates/resume.html",
        body=body,
        error=error,
        resume_file=current_file,
        file_error=file_error,
    )
    return response, (400 if error else 200)


@bp.post("/candidate/resume/file")
@login_required
@role_required("candidate")
def resume_file():
    conn = get_db()
    try:
        resume_service.save_resume_file(
            conn, g.user["id"], request.files.get("file")
        )
    except ValidationError as exc:
        current = resume_service.get_resume(conn, g.user["id"])
        current_file = resume_service.get_resume_file(conn, g.user["id"])
        response = render_template(
            "candidates/resume.html",
            body=current["body"] if current else "",
            error=None,
            resume_file=current_file,
            file_error=exc.errors.get("file"),
        )
        return response, 400
    flash("CV file uploaded", "success")
    return redirect("/candidate/resume")


@bp.post("/candidate/resume/file/delete")
@login_required
@role_required("candidate")
def resume_file_delete():
    resume_service.delete_resume_file(get_db(), g.user["id"])
    flash("CV file removed", "success")
    return redirect("/candidate/resume")


@bp.get("/candidates/<int:candidate_id>/resume/file")
@login_required
def resume_file_view(candidate_id: int):
    resume_file = resume_service.get_resume_file_for_viewer(
        get_db(), g.user["id"], candidate_id
    )
    return send_file(
        resume_file["path"],
        mimetype=resume_file["content_type"],
        as_attachment=False,
        download_name=resume_file["original_name"],
    )


@bp.get("/candidates/<int:candidate_id>/resume")
@login_required
def resume_view(candidate_id: int):
    resume = resume_service.get_resume_for_viewer(
        get_db(), g.user["id"], candidate_id
    )
    return render_template(
        "candidates/resume.html", body=resume["body"], error=None, read_only=True
    )
