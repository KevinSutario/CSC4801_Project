"""Auth routes: register, login, logout. Owned by T05.

Sign-in clears the session first (anti-fixation), rotates the CSRF token, and
only redirects to a `next` that passes is_safe_next. Passwords never reach a
template context, a log, or the audit detail.
"""

from flask import flash, g, redirect, render_template, request, session

from app import audit
from app.db import get_db, transaction
from app.errors import ValidationError
from app.security import (
    is_login_blocked,
    is_safe_next,
    login_key,
    record_failed_login,
    reset_login_failures,
    rotate_csrf,
)

from . import bp
from . import service

_LOCKED_MSG = "Too many attempts. Try again in 10 minutes."
_BAD_CREDS_MSG = "Email or password is wrong."


def _sign_in(user: dict) -> None:
    """Start a fresh signed-in session for the given user dict."""
    session.clear()
    session["user_id"] = user["id"]
    session["role"] = user["role"]
    session.permanent = True
    rotate_csrf()


@bp.route("/register", methods=["GET", "POST"])
def register():
    if g.get("user"):
        return redirect("/")
    if request.method == "POST":
        conn = get_db()
        email = request.form.get("email", "")
        role = request.form.get("role", "")
        display_name = request.form.get("display_name", "")
        try:
            user_id = service.register(
                conn, email, request.form.get("password", ""), role, display_name
            )
        except ValidationError as exc:
            return (
                render_template(
                    "auth/register.html",
                    errors=exc.errors,
                    email=email,
                    role=role,
                    display_name=display_name,
                ),
                400,
            )
        _sign_in({"id": user_id, "role": role})
        flash("Welcome to Keystone", "success")
        return redirect("/")
    return render_template("auth/register.html", errors={}, email="", role="candidate",
                           display_name="")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if g.get("user"):
        return redirect("/")
    next_target = request.args.get("next", "")
    if request.method == "POST":
        conn = get_db()
        email = request.form.get("email", "")
        password = request.form.get("password", "")
        # Two independent limits (04-AUTH-SECURITY: "per email AND per IP"): one keyed on the
        # email alone, one on the IP alone, so rotating the IP cannot bypass the per-email cap.
        email_key = login_key(email, "")
        ip_key = login_key("", request.remote_addr or "")
        if is_login_blocked(email_key) or is_login_blocked(ip_key):
            return render_template("auth/login.html", error=_LOCKED_MSG, email=email), 429
        user = service.authenticate(conn, email, password)
        if user is None:
            record_failed_login(email_key)
            record_failed_login(ip_key)
            with transaction(conn):
                audit.log_event(conn, None, "user.login_failed", "user", None)
            return render_template("auth/login.html", error=_BAD_CREDS_MSG, email=email), 400
        reset_login_failures(email_key)
        reset_login_failures(ip_key)
        _sign_in(user)
        with transaction(conn):
            audit.log_event(conn, user["id"], "user.login", "user", user["id"])
        if next_target and is_safe_next(next_target):
            return redirect(next_target)
        return redirect("/")
    return render_template("auth/login.html", error=None, email="")


@bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Signed out", "success")
    return redirect("/auth/login")
