"""Private raw-text and PDF candidate resume persistence."""

import secrets
import sqlite3
from pathlib import Path

from flask import current_app

from app import audit
from app.config import Config
from app.db import now_iso, transaction
from app.errors import Forbidden, NotFound, ValidationError

RESUME_MAX_CHARS = 20000
RESUME_FILE_MAX_MB: int = Config.MAX_UPLOAD_MB


def get_resume(conn: sqlite3.Connection, owner_id: int) -> dict | None:
    """Return the owner's resume row, or None when no resume has been saved."""
    row = conn.execute(
        "SELECT owner_id, body, updated_at FROM resumes WHERE owner_id = ?",
        (owner_id,),
    ).fetchone()
    return dict(row) if row else None


def save_resume(conn: sqlite3.Connection, owner_id: int, body: str) -> None:
    """Replace the owner's raw-text resume and record the update atomically."""
    body = body.strip()
    if not body or len(body) > RESUME_MAX_CHARS:
        raise ValidationError({"body": f"Enter a resume of 1 to {RESUME_MAX_CHARS} characters."})
    with transaction(conn):
        conn.execute(
            "INSERT INTO resumes (owner_id, body, updated_at) VALUES (?, ?, ?)"
            " ON CONFLICT(owner_id) DO UPDATE SET body = excluded.body,"
            " updated_at = excluded.updated_at",
            (owner_id, body, now_iso()),
        )
        audit.log_event(conn, owner_id, "resume.update", "resume", owner_id)


def get_resume_for_viewer(
    conn: sqlite3.Connection, viewer_id: int, candidate_id: int
) -> dict:
    """Return a resume only to its owner, distinguishing private and missing cases."""
    if viewer_id != candidate_id:
        raise Forbidden()
    resume = get_resume(conn, candidate_id)
    if resume is None:
        raise NotFound()
    return resume


def _resume_file_path(stored_name: str) -> Path:
    """Build an absolute upload path from a server-generated name only."""
    upload_dir = Path(current_app.config["UPLOAD_DIR"]).resolve()
    path = (upload_dir / stored_name).resolve()
    if path.parent != upload_dir or path.name != stored_name:
        raise NotFound()
    return path


def get_resume_file(conn: sqlite3.Connection, owner_id: int) -> dict | None:
    """Return the owner's PDF metadata, or None if no file is saved."""
    row = conn.execute(
        "SELECT owner_id, stored_name, original_name, content_type, size_bytes, updated_at"
        " FROM resume_files WHERE owner_id = ?",
        (owner_id,),
    ).fetchone()
    return dict(row) if row else None


def save_resume_file(
    conn: sqlite3.Connection, owner_id: int, file_storage
) -> None:
    """Validate and replace the owner's private PDF, recording one audit event."""
    if file_storage is None:
        raise ValidationError({"file": "Choose a PDF file to upload."})

    original_name = getattr(file_storage, "filename", None)
    if not isinstance(original_name, str) or not original_name.strip():
        raise ValidationError({"file": "Choose a PDF file to upload."})
    if Path(original_name).suffix.lower() != ".pdf":
        raise ValidationError({"file": "Choose a file with the .pdf extension."})
    if getattr(file_storage, "content_type", None) != "application/pdf":
        raise ValidationError({"file": "The uploaded file must be a PDF."})

    max_bytes = int(current_app.config["MAX_UPLOAD_MB"]) * 1024 * 1024
    stream = file_storage.stream
    stream.seek(0)
    content = stream.read(max_bytes + 1)
    if not content:
        raise ValidationError({"file": "The PDF file is empty."})
    if len(content) > max_bytes:
        raise ValidationError({"file": "The PDF file is too large."})
    if not content.startswith(b"%PDF-"):
        raise ValidationError({"file": "The uploaded file is not a valid PDF."})

    previous = get_resume_file(conn, owner_id)
    stored_name = f"{secrets.token_hex(16)}.pdf"
    new_path = _resume_file_path(stored_name)
    stream.seek(0)
    try:
        file_storage.save(new_path)
        with transaction(conn):
            conn.execute(
                "INSERT INTO resume_files"
                " (owner_id, stored_name, original_name, content_type, size_bytes, updated_at)"
                " VALUES (?, ?, ?, ?, ?, ?)"
                " ON CONFLICT(owner_id) DO UPDATE SET"
                " stored_name = excluded.stored_name,"
                " original_name = excluded.original_name,"
                " content_type = excluded.content_type,"
                " size_bytes = excluded.size_bytes,"
                " updated_at = excluded.updated_at",
                (
                    owner_id,
                    stored_name,
                    original_name,
                    "application/pdf",
                    len(content),
                    now_iso(),
                ),
            )
            audit.log_event(
                conn,
                owner_id,
                "resume.update",
                "resume",
                owner_id,
                detail=f"file added: {original_name}",
            )
    except BaseException:
        new_path.unlink(missing_ok=True)
        raise

    if previous is not None:
        _resume_file_path(previous["stored_name"]).unlink(missing_ok=True)


def delete_resume_file(conn: sqlite3.Connection, owner_id: int) -> None:
    """Remove the owner's PDF metadata and disk file, safely if already absent."""
    current = get_resume_file(conn, owner_id)
    if current is None:
        return

    with transaction(conn):
        conn.execute("DELETE FROM resume_files WHERE owner_id = ?", (owner_id,))
        audit.log_event(
            conn,
            owner_id,
            "resume.update",
            "resume",
            owner_id,
            detail="file removed",
        )

    _resume_file_path(current["stored_name"]).unlink(missing_ok=True)


def _with_resume_file_path(resume_file: dict) -> dict:
    result = dict(resume_file)
    result["path"] = str(_resume_file_path(result["stored_name"]))
    return result


def get_resume_file_for_viewer(
    conn: sqlite3.Connection, viewer_id: int, candidate_id: int
) -> dict:
    """Return a PDF only to its owner; check privacy before file existence."""
    if viewer_id != candidate_id:
        raise Forbidden()
    resume_file = get_resume_file(conn, candidate_id)
    if resume_file is None:
        raise NotFound()
    return _with_resume_file_path(resume_file)


def resolve_resume_file(conn: sqlite3.Connection, candidate_id: int) -> dict | None:
    """Resolve a candidate PDF for a trusted caller that checks access separately."""
    resume_file = get_resume_file(conn, candidate_id)
    if resume_file is None:
        return None
    return _with_resume_file_path(resume_file)
