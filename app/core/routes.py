"""Core landing page routes."""

from flask import g, redirect, render_template

from . import bp


@bp.get("/")
def index():
    if g.get("user"):
        if g.user["role"] == "candidate":
            return redirect("/candidate/")
        if g.user["role"] == "employer":
            return redirect("/employer/")
    return render_template("index.html")
