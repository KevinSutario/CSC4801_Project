"""Auth service: register, authenticate, get_user. Owned by T05 (T06 may extend).

All writes run inside a single transaction(). Passwords are hashed with Werkzeug
and never returned or logged. Rule limits are DEFAULT (not in brief), see T05 card.
"""

import re
import sqlite3

from werkzeug.security import check_password_hash, generate_password_hash

from app import audit
from app.db import now_iso, transaction
from app.errors import ValidationError

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_ROLES = ("candidate", "employer")
_EMAIL_MAX = 254
_PW_MIN, _PW_MAX = 8, 128
_NAME_MIN, _NAME_MAX = 1, 80


def _validate(email: str, password: str, role: str, display_name: str) -> tuple[str, str, dict]:
    """Return (clean_email, clean_name, errors). errors is empty when all valid."""
    errors: dict[str, str] = {}

    clean_email = (email or "").strip().lower()
    if not clean_email:
        errors["email"] = "Enter your email."
    elif len(clean_email) > _EMAIL_MAX or not _EMAIL_RE.match(clean_email):
        errors["email"] = "Enter a valid email."

    if not password or not (_PW_MIN <= len(password) <= _PW_MAX):
        errors["password"] = f"Password must be {_PW_MIN} to {_PW_MAX} characters."

    clean_name = (display_name or "").strip()
    if not (_NAME_MIN <= len(clean_name) <= _NAME_MAX):
        errors["display_name"] = f"Name must be {_NAME_MIN} to {_NAME_MAX} characters."

    if role not in _ROLES:
        errors["role"] = "Choose a role."

    return clean_email, clean_name, errors


def register(conn: sqlite3.Connection, email: str, password: str, role: str,
             display_name: str) -> int:
    """Create a user (and a candidate profile for candidates). Returns the user id.

    Raises ValidationError (with a field->message dict) for any invalid field or a
    duplicate email. Everything runs in one transaction.
    """
    clean_email, clean_name, errors = _validate(email, password, role, display_name)
    if errors:
        raise ValidationError(errors)

    try:
        with transaction(conn):
            cursor = conn.execute(
                "INSERT INTO users (email, password_hash, role, display_name, created_at)"
                " VALUES (?, ?, ?, ?, ?)",
                (clean_email, generate_password_hash(password), role, clean_name, now_iso()),
            )
            user_id = cursor.lastrowid
            if role == "candidate":
                conn.execute(
                    "INSERT INTO candidate_profiles (user_id, timezone, updated_at)"
                    " VALUES (?, 'UTC', ?)",
                    (user_id, now_iso()),
                )
            audit.log_event(conn, user_id, "user.register", "user", user_id)
    except sqlite3.IntegrityError as exc:
        # Unique email (case-insensitive). Generic message: do not reveal existence.
        raise ValidationError({"email": "That email cannot be used."}) from exc
    return user_id


def authenticate(conn: sqlite3.Connection, email: str, password: str) -> dict | None:
    """Return the user dict (without password_hash) for valid credentials, else None."""
    clean_email = (email or "").strip().lower()
    row = conn.execute(
        "SELECT id, email, password_hash, role, display_name FROM users WHERE email = ?",
        (clean_email,),
    ).fetchone()
    if row is None or not check_password_hash(row["password_hash"], password or ""):
        return None
    user = dict(row)
    user.pop("password_hash", None)
    return user


def get_user(conn: sqlite3.Connection, user_id: int) -> dict | None:
    """Return the user dict (without password_hash) by id, or None."""
    row = conn.execute(
        "SELECT id, email, role, display_name FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    return dict(row) if row else None
