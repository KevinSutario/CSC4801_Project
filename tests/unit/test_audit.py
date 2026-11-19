"""T02 · audit log: action validation, truncation, per-actor newest-first listing."""

import pytest

from app import audit
from app.db import transaction


def _make_user(db, email, role="candidate", name="X"):
    with transaction(db):
        db.execute(
            "INSERT INTO users (email, password_hash, role, display_name, created_at)"
            " VALUES (?, ?, ?, ?, ?)",
            (email, "x", role, name, "2030-01-01T00:00:00Z"),
        )
    return db.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()["id"]


def test_unknown_action_raises_valueerror(conn):
    actor = _make_user(conn, "a@example.com")
    with pytest.raises(ValueError):
        with transaction(conn):
            audit.log_event(conn, actor, "not.a.real.action", "user", actor)


def test_known_actions_are_accepted(conn):
    actor = _make_user(conn, "a@example.com")
    with transaction(conn):
        for action in audit.ACTIONS:
            audit.log_event(conn, actor, action, "user", actor, detail="ok")
    rows = audit.list_events(conn, actor)
    assert len(rows) == len(audit.ACTIONS)


def test_detail_truncated_to_500_chars(conn):
    actor = _make_user(conn, "a@example.com")
    with transaction(conn):
        audit.log_event(conn, actor, "user.login", "user", actor, detail="z" * 600)
    rows = audit.list_events(conn, actor)
    assert len(rows[0]["detail"]) == 500


def test_events_newest_first_and_only_for_actor(conn):
    a = _make_user(conn, "a@example.com")
    b = _make_user(conn, "b@example.com")
    with transaction(conn):
        audit.log_event(conn, a, "user.login", "user", a, detail="a1")
        audit.log_event(conn, a, "profile.update", "user", a, detail="a2")
        audit.log_event(conn, b, "user.login", "user", b, detail="b1")
    rows = audit.list_events(conn, a)
    assert [r["detail"] for r in rows] == ["a2", "a1"]  # newest first
    assert all(r["actor_id"] == a for r in rows)  # b's event excluded


def test_log_event_records_action_and_object(conn):
    actor = _make_user(conn, "a@example.com")
    with transaction(conn):
        audit.log_event(conn, actor, "job.create", "job", 42, detail="posted")
    row = audit.list_events(conn, actor)[0]
    assert row["action"] == "job.create"
    assert row["object_type"] == "job"
    assert row["object_id"] == 42
    assert row["created_at"].endswith("Z")


def test_actions_matches_data_model_fixed_list(conn):
    expected = {
        "user.register", "user.login", "user.login_failed", "profile.update",
        "resume.update", "company.update", "job.create", "job.update", "job.delete",
        "application.submit", "application.status", "slot.create", "slot.delete",
        "booking.create", "booking.conflict",
    }
    assert set(audit.ACTIONS) == expected
