"""Candidate home and profile routes."""

from zoneinfo import available_timezones

from flask import flash, g, redirect, render_template, request

from app.db import get_db
from app.errors import ValidationError
from app.security import login_required, role_required

from . import bp
from . import profile_service


@bp.get("/candidate/")
@login_required
@role_required("candidate")
def today():
    profile = profile_service.get_profile(get_db(), g.user["id"])
    return render_template("candidates/today.html", profile=profile)


@bp.route("/candidate/profile", methods=["GET", "POST"])
@login_required
@role_required("candidate")
def profile():
    conn = get_db()
    current = profile_service.get_profile(conn, g.user["id"])
    errors = {}
    values = dict(current)
    if request.method == "POST":
        values = {
            "display_name": request.form.get("display_name", ""),
            "headline": request.form.get("headline", ""),
            "location": request.form.get("location", ""),
            "timezone": request.form.get("timezone", "UTC"),
            "summary": request.form.get("summary", ""),
            "skills_text": request.form.get("skills_text", ""),
            "skills": current["skills"],
        }
        try:
            profile_service.save_profile(
                conn,
                g.user["id"],
                values["display_name"],
                values["headline"],
                values["location"],
                values["timezone"],
                values["summary"],
                values["skills_text"],
            )
        except ValidationError as exc:
            errors = exc.errors
        else:
            flash("Profile saved", "success")
            return redirect("/candidate/profile")
    else:
        values["skills_text"] = ", ".join(current["skills"])
    return render_template(
        "candidates/profile.html",
        profile=values,
        errors=errors,
        timezones=[(zone, zone) for zone in sorted(available_timezones())],
    ), (400 if errors else 200)
