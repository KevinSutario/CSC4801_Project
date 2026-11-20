"""Employer routes: home and company profile. Owned by T09.

Both require the employer role. Company text is rendered escaped by Jinja
autoescape (FP-SEC-3); the website is shown as plain text, never an unescaped link.
"""

from flask import flash, g, redirect, render_template, request

from app.db import get_db
from app.errors import ValidationError
from app.security import role_required

from . import bp
from . import service


@bp.get("/employer/")
@role_required("employer")
def home():
    company = service.get_company(get_db(), g.user["id"])
    return render_template("employers/home.html", company=company)


@bp.route("/employer/company", methods=["GET", "POST"])
@role_required("employer")
def company():
    conn = get_db()
    if request.method == "POST":
        values = {
            "name": request.form.get("name", ""),
            "industry": request.form.get("industry", ""),
            "location": request.form.get("location", ""),
            "website": request.form.get("website", ""),
            "description": request.form.get("description", ""),
        }
        try:
            service.save_company(conn, g.user["id"], **values)
        except ValidationError as exc:
            return render_template("employers/company.html", errors=exc.errors, company=values), 400
        flash("Company profile saved", "success")
        return redirect("/employer/")
    company = service.get_company(conn, g.user["id"])
    return render_template("employers/company.html", errors={}, company=company or {})
