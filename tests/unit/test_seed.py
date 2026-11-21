"""Demo data seeding (T19).

seed(app) builds the mandatory minimum from docs/plan/12-DEPLOY.md through the
real services, refuses to run twice without a reset, and leaves two
``interviewing`` candidates eligible to race for Daniel's slot.
"""

import sqlite3

import pytest

from app.db import get_db, now_iso
from app.matching.engine import score
from app.scheduling.booking import is_eligible
from scripts.seed import DEMO_PASSWORD, seed


_COUNTS = {
    "users": "SELECT COUNT(*) AS n FROM users",
    "jobs": "SELECT COUNT(*) AS n FROM jobs",
    "applications": "SELECT COUNT(*) AS n FROM applications",
    "interview_slots": "SELECT COUNT(*) AS n FROM interview_slots",
}


def _count(conn: sqlite3.Connection, table: str) -> int:
    return conn.execute(_COUNTS[table]).fetchone()["n"]


def _seeded(app) -> dict:
    """Run seed(app) and return the id lookup tables for assertions."""
    with app.app_context():
        seed(app)
        conn = get_db()
        users = {
            row["email"]: row["id"]
            for row in conn.execute("SELECT id, email FROM users")
        }
        jobs = {
            row["title"]: row["id"]
            for row in conn.execute("SELECT id, title FROM jobs")
        }
        return {"users": users, "jobs": jobs}


def _skills(conn: sqlite3.Connection, candidate_id: int) -> set[str]:
    return {
        row["name"]
        for row in conn.execute(
            "SELECT s.name FROM skills s JOIN candidate_skills cs"
            " ON cs.skill_id = s.id WHERE cs.candidate_id = ?",
            (candidate_id,),
        )
    }


def _job_skills(conn: sqlite3.Connection, job_id: int) -> set[str]:
    return {
        row["name"]
        for row in conn.execute(
            "SELECT s.name FROM skills s JOIN job_skills js"
            " ON js.skill_id = s.id WHERE js.job_id = ?",
            (job_id,),
        )
    }


def _application(conn: sqlite3.Connection, candidate_id: int, job_id: int) -> dict:
    row = conn.execute(
        "SELECT id, status FROM applications WHERE candidate_id = ? AND job_id = ?",
        (candidate_id, job_id),
    ).fetchone()
    assert row is not None
    return dict(row)


def test_seed_creates_the_demo_minimum(app):
    ids = _seeded(app)
    assert set(ids["users"]) == {
        "meilin@demo.keystone", "arjun@demo.keystone", "sofia@demo.keystone",
        "daniel@demo.keystone", "priya@demo.keystone",
    }
    assert set(ids["jobs"]) == {"Data Analyst", "Logistics Coordinator",
                                "Graduate Trainee"}

    with app.app_context():
        conn = get_db()
        meilin = ids["users"]["meilin@demo.keystone"]
        arjun = ids["users"]["arjun@demo.keystone"]
        sofia = ids["users"]["sofia@demo.keystone"]
        daniel = ids["users"]["daniel@demo.keystone"]
        priya = ids["users"]["priya@demo.keystone"]

        # Skills on candidates and jobs.
        assert _skills(conn, meilin) == {"python", "sql"}
        assert _skills(conn, arjun) == {"python"}
        assert _skills(conn, sofia) == {"rust"}
        analyst = ids["jobs"]["Data Analyst"]
        coordinator = ids["jobs"]["Logistics Coordinator"]
        trainee = ids["jobs"]["Graduate Trainee"]
        assert _job_skills(conn, analyst) == {"python", "sql"}
        assert _job_skills(conn, coordinator) == {"excel", "sql"}
        assert _job_skills(conn, trainee) == set()

        # Companies.
        names = {
            row["owner_id"]: row["name"]
            for row in conn.execute("SELECT owner_id, name FROM companies")
        }
        assert names == {daniel: "Harbourline Logistics",
                         priya: "Tidewater Freight"}

        # Mei Lin's raw-text resume.
        assert conn.execute(
            "SELECT body FROM resumes WHERE owner_id = ?", (meilin,)
        ).fetchone()["body"] == "Demo resume. Fictional person."

        # Applications cover all four statuses (five applications, per the card).
        assert conn.execute("SELECT COUNT(*) FROM applications").fetchone()[0] == 5
        expected = {
            (meilin, analyst): "interviewing",
            (arjun, analyst): "interviewing",
            (sofia, analyst): "pending",
            (meilin, trainee): "accepted",
            (sofia, trainee): "rejected",
        }
        for (cand, job), status in expected.items():
            assert _application(conn, cand, job)["status"] == status

        # Two interviewing candidates are eligible for Daniel's slot.
        ml_da = _application(conn, meilin, analyst)
        aj_da = _application(conn, arjun, analyst)
        assert ml_da["status"] == "interviewing"
        assert aj_da["status"] == "interviewing"
        assert is_eligible(conn, meilin, ml_da["id"]) is True
        assert is_eligible(conn, arjun, aj_da["id"]) is True

        # One future, unbooked 30-minute slot each for Daniel and Priya.
        slots = conn.execute(
            "SELECT employer_id, starts_at, ends_at, created_tz,"
            " (SELECT COUNT(*) FROM bookings b WHERE b.slot_id = s.id) AS bookings"
            " FROM interview_slots s"
        ).fetchall()
        assert len(slots) == 2
        for row in slots:
            assert row["starts_at"] > now_iso()
            assert row["bookings"] == 0
        zones = {row["employer_id"]: row["created_tz"] for row in slots}
        assert zones[daniel] == "Asia/Hong_Kong"
        assert zones[priya] == "Europe/London"
        starts = sorted(row["starts_at"] for row in slots)
        assert starts[1] != starts[0]  # different employer slots are distinct


def test_seed_matches_the_four_fp_match_1_scores(app):
    ids = _seeded(app)
    with app.app_context():
        conn = get_db()
        analyst = ids["jobs"]["Data Analyst"]
        trainee = ids["jobs"]["Graduate Trainee"]
        meilin = ids["users"]["meilin@demo.keystone"]
        arjun = ids["users"]["arjun@demo.keystone"]
        sofia = ids["users"]["sofia@demo.keystone"]

        assert score(_skills(conn, meilin), _job_skills(conn, analyst))["score"] == 100
        assert score(_skills(conn, arjun), _job_skills(conn, analyst))["score"] == 50
        assert score(_skills(conn, sofia), _job_skills(conn, analyst))["score"] == 0
        for candidate in (meilin, arjun, sofia):
            assert score(_skills(conn, candidate),
                         _job_skills(conn, trainee))["score"] == 100


def test_seed_twice_without_reset_refuses_and_changes_nothing(app):
    _seeded(app)
    with app.app_context():
        conn = get_db()
        before = {t: _count(conn, t)
                  for t in ("users", "jobs", "applications", "interview_slots")}
        before_max_user = conn.execute("SELECT MAX(id) FROM users").fetchone()[0]

    # The second call refuses.
    with app.app_context():
        with pytest.raises(RuntimeError, match="already has users"):
            seed(app)

    # And nothing changed.
    with app.app_context():
        conn = get_db()
        after = {t: _count(conn, t)
                 for t in ("users", "jobs", "applications", "interview_slots")}
        assert after == before
        # No registration attempt wrote a new user row.
        assert conn.execute("SELECT MAX(id) FROM users").fetchone()[0] == before_max_user
        assert conn.execute("SELECT COUNT(*) FROM users WHERE email = ?",
                            ("meilin@demo.keystone",)).fetchone()[0] == 1


def test_demo_password_meets_the_auth_rules(app):
    """The demo password must be able to sign every demo account in."""
    ids = _seeded(app)
    from app.auth.service import authenticate

    with app.app_context():
        conn = get_db()
        for email in ids["users"]:
            user = authenticate(conn, email, DEMO_PASSWORD)
            assert user is not None and user["email"] == email
