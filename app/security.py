"""Security spine. Owned by T02 (frozen afterwards).

Installs the per-request user loader, CSRF protection and security headers, and
provides the login_required / role_required decorators, the safe-redirect check
and the in-memory login rate limiter. See docs/plan/04-AUTH-SECURITY.md.
"""

import functools
import hmac
import secrets
import time

from flask import (
    Flask,
    abort,
    current_app,
    g,
    redirect,
    request,
    session,
    url_for,
)

from .db import get_db

# ---- Security headers (docs/plan/04-AUTH-SECURITY.md, exact list) -----------
_CSP = (
    "default-src 'self'; style-src 'self' https://fonts.googleapis.com; "
    "font-src https://fonts.gstatic.com; img-src 'self' data:; "
    "form-action 'self'; base-uri 'none'; frame-ancestors 'none'"
)
_SECURITY_HEADERS = {
    "X-Frame-Options": "DENY",
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "same-origin",
    "Content-Security-Policy": _CSP,
}

# POST-like methods that must carry a valid CSRF token.
_CSRF_METHODS = frozenset({"POST", "PUT", "PATCH", "DELETE"})

# Rate limit: 5 failures within the window blocks for the window from the last one.
_MAX_FAILURES = 5
_WINDOW_SECONDS = 600

def login_required(view):
    """Require a signed-in user. GET redirects to sign-in; other methods 401."""

    @functools.wraps(view)
    def wrapped(*args, **kwargs):
        if g.get("user") is None:
            if request.method == "GET":
                return redirect(url_for("auth.login", next=request.path))
            abort(401)
        return view(*args, **kwargs)

    return wrapped


def role_required(role: str):
    """Require a signed-in user with the given role ('candidate' | 'employer')."""

    def decorator(view):
        @functools.wraps(view)
        def wrapped(*args, **kwargs):
            if g.get("user") is None:
                if request.method == "GET":
                    return redirect(url_for("auth.login", next=request.path))
                abort(401)
            if g.user["role"] != role:
                abort(403)
            return view(*args, **kwargs)

        return wrapped

    return decorator


# ---- Login rate limiter -----------------------------------------------------
# Stored per app at app.extensions["login_limiter"], so each test app is fresh.


def _limiter() -> dict[str, list[float]]:
    return current_app.extensions["login_limiter"]


def login_key(email: str, ip: str) -> str:
    """Normalise an email+ip into a single limiter key."""
    return f"{email.strip().lower()}|{ip}"


def _recent_failures(key: str) -> list[float]:
    """Failure timestamps for this key within the window (prunes old ones)."""
    now = time.monotonic()
    kept = [t for t in _limiter().get(key, []) if now - t < _WINDOW_SECONDS]
    if kept:
        _limiter()[key] = kept
    else:
        _limiter().pop(key, None)
    return kept


def is_login_blocked(key: str) -> bool:
    """True once there are at least 5 failures inside the window."""
    return len(_recent_failures(key)) >= _MAX_FAILURES


def record_failed_login(key: str) -> None:
    """Record one failed attempt at the current time."""
    _limiter().setdefault(key, []).append(time.monotonic())


def reset_login_failures(key: str) -> None:
    """Clear the failure history for a key (call after a successful sign-in)."""
    _limiter().pop(key, None)


def init_app(app: Flask) -> None:
    """Register hooks, Jinja globals and the per-app login limiter."""
    app.extensions["login_limiter"] = {}

    app.before_request(load_user)
    app.before_request(csrf_protect)
    app.after_request(add_security_headers)

    app.jinja_env.globals["csrf_token"] = csrf_token

    @app.context_processor
    def inject_current_user() -> dict:
        return {"current_user": g.get("user")}


def load_user() -> None:
    """before_request: put the current user dict on g.user, or None.

    Clears the session if the stored user_id no longer maps to a row.
    """
    g.user = None
    user_id = session.get("user_id")
    if user_id is None:
        return
    row = get_db().execute(
        "SELECT id, email, role, display_name FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    if row is None:
        session.clear()
        return
    g.user = dict(row)


def csrf_token() -> str:
    """Return the session CSRF token, creating it on first use."""
    if "csrf" not in session:
        session["csrf"] = secrets.token_urlsafe(32)
    return session["csrf"]


def rotate_csrf() -> None:
    """Replace the CSRF token (call right after a successful sign-in)."""
    session["csrf"] = secrets.token_urlsafe(32)


def csrf_protect() -> None:
    """before_request: reject an unsafe-method request with a bad CSRF token."""
    if request.method in _CSRF_METHODS:
        sent = request.form.get("csrf_token") or ""
        expected = session.get("csrf") or ""
        if not expected or not hmac.compare_digest(sent, expected):
            abort(403)


def add_security_headers(response):
    """after_request: attach the fixed security headers to every response."""
    for name, value in _SECURITY_HEADERS.items():
        response.headers[name] = value
    return response


def is_safe_next(target: str | None) -> bool:
    """True only for a local path: starts with a single '/', no backslash, no scheme."""
    if not target or not isinstance(target, str):
        return False
    if not target.startswith("/") or target.startswith("//"):
        return False
    if "\\" in target:
        return False
    return True
