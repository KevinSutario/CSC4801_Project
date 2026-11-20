"""Booking requirement tests (FP-SCHED-2, FP-SCHED-3). Owned by T16, then T17.

Rule (brief section 6, FP-SCHED-2 "Booking eligibility"): a candidate may book a
slot if and only if they own the application, the slot belongs to the employer
of the application's job, the application status is interviewing, the slot is
in the future and unbooked, and the application has no booking yet. A failed
booking writes nothing. A booking survives the application later leaving
interviewing, and the slot stays unavailable.

Rule (brief section 6, FP-SCHED-3 "Atomic concurrency"): when two eligible
candidates attempt the same slot, exactly one booking exists afterward and the
loser gets HTTP 409 with the exact message "Slot already booked" plus a
booking.conflict audit row. A synchronized multi-client test is not required.
"""

import sqlite3

import pytest

from app.db import now_iso
from app.errors import Conflict, Forbidden, NotFound
from app.scheduling import booking as service


def _count_bookings(conn) -> int:
    return conn.execute("SELECT COUNT(*) AS n FROM bookings").fetchone()["n"]


@pytest.fixture()
def world(conn, make_candidate, make_employer, make_job, make_application, make_slot):
    """A small scheduling world: two employers, two candidates, jobs and slots."""
    cand_a = make_candidate()
    cand_b = make_candidate(email="cand-b@example.com")
    emp_a = make_employer()
    emp_b = make_employer(email="emp-b@example.com")
    job_a = make_job(emp_a, title="Data Analyst")
    job_a2 = make_job(emp_a, title="Backend Engineer")
    return {
        "cand_a": cand_a,
        "cand_b": cand_b,
        "emp_a": emp_a,
        "emp_b": emp_b,
        "app_a": make_application(cand_a, job_a, status="interviewing"),
        "app_a_pending": make_application(cand_a, job_a2, status="pending"),
        "app_b": make_application(cand_b, job_a, status="interviewing"),
        "slot_a": make_slot(emp_a, "2030-01-07T02:00:00Z", "2030-01-07T02:30:00Z",
                            created_tz="UTC"),
        "slot_c": make_slot(emp_a, "2030-01-08T02:00:00Z", "2030-01-08T02:30:00Z",
                            created_tz="UTC"),
        "slot_other": make_slot(emp_b, "2030-01-07T06:00:00Z", "2030-01-07T06:30:00Z",
                                created_tz="UTC"),
        "slot_past": make_slot(emp_a, "2020-01-07T02:00:00Z", "2020-01-07T02:30:00Z",
                               created_tz="UTC"),
    }


def test_fp_sched_2_eligible_booking(client, conn, world, login_as, csrf_post):
    w = world
    # The candidate's profile zone is Hong Kong; the slot was entered in UTC.
    conn.execute(
        "UPDATE candidate_profiles SET timezone = 'Asia/Hong_Kong' WHERE user_id = ?",
        (w["cand_a"],),
    )
    login_as(client, w["cand_a"], "candidate")

    # Detail page: the employer's open slots, in the candidate's zone.
    resp = client.get(f"/candidate/applications/{w['app_a']}")
    assert resp.status_code == 200
    body = resp.data.decode()
    assert "Asia/Hong_Kong" in body       # the zone name is shown
    assert "10:00" in body                # 02:00 UTC = 10:00 Asia/Hong_Kong

    # Confirm page: the range in the candidate's zone and the entry zone.
    resp = client.get(f"/candidate/applications/{w['app_a']}/book/{w['slot_a']}")
    assert resp.status_code == 200
    body = resp.data.decode()
    assert "10:00" in body and "Asia/Hong_Kong" in body
    assert "02:00" in body and "(UTC)" in body

    # POST books and redirects to the detail page.
    resp = csrf_post(client, f"/candidate/applications/{w['app_a']}/book/{w['slot_a']}", {})
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith(f"/candidate/applications/{w['app_a']}")

    row = conn.execute("SELECT * FROM bookings").fetchone()
    assert row["application_id"] == w["app_a"]
    assert row["slot_id"] == w["slot_a"]

    # The booking.create audit row exists (written in the same transaction).
    audited = conn.execute(
        "SELECT 1 FROM audit_log WHERE action = 'booking.create' AND actor_id = ?",
        (w["cand_a"],),
    ).fetchone()
    assert audited is not None

    # The booked slot is no longer bookable; the same employer's other slot is.
    bookable = service.list_bookable_slots(conn, w["cand_a"], w["app_a"])
    assert [s["id"] for s in bookable] == [w["slot_c"]]

    # Detail page shows the booked time in the candidate's zone.
    resp = client.get(f"/candidate/applications/{w['app_a']}")
    assert resp.status_code == 200
    body = resp.data.decode()
    assert "10:00" in body and "Asia/Hong_Kong" in body

    # Leaving interviewing keeps the booking and the slot unavailable.
    conn.execute("UPDATE applications SET status = 'accepted' WHERE id = ?", (w["app_a"],))
    row = conn.execute(
        "SELECT slot_id FROM bookings WHERE application_id = ?", (w["app_a"],)
    ).fetchone()
    assert row is not None and row["slot_id"] == w["slot_a"]
    bookable = service.list_bookable_slots(conn, w["cand_a"], w["app_a"])
    assert [s["id"] for s in bookable] == [w["slot_c"]]


@pytest.mark.parametrize(
    "application_key,slot_key,expected,pre_booking",
    [
        ("app_a_pending", "slot_a", Forbidden, None),        # status not interviewing
        ("app_b", "slot_a", Forbidden, None),                # another candidate's application
        ("app_a", "slot_other", Forbidden, None),            # slot of another employer
        ("app_a", "slot_a", Forbidden, ("app_a", "slot_c")),  # already booked (other slot)
        ("app_a", "slot_past", Forbidden, None),             # slot in the past
        ("app_a", "slot_a", Conflict, ("app_b", "slot_a")),  # slot already booked
        ("app_a", "missing", NotFound, None),                # missing slot
        ("missing", "slot_a", NotFound, None),               # missing application
    ],
)
def test_fp_sched_2_ineligible_booking(conn, world, make_booking, application_key, slot_key,
                                       expected, pre_booking):
    w = world
    if pre_booking is not None:
        make_booking(w[pre_booking[0]], w[pre_booking[1]])
    application_id = w.get(application_key, 999999)
    slot_id = w.get(slot_key, 999999)
    before = _count_bookings(conn)
    with pytest.raises(expected):
        service.book_slot(conn, w["cand_a"], application_id, slot_id)
    assert _count_bookings(conn) == before   # no new booking row on failure


def test_employer_get_application_detail_is_403(client, world, login_as):
    """The candidate detail page is candidate-only: an employer gets 403."""
    login_as(client, world["emp_a"], "employer")
    resp = client.get(f"/candidate/applications/{world['app_a']}")
    assert resp.status_code == 403


def test_other_candidate_get_application_detail_is_403(client, world, login_as):
    """Another candidate's application detail is Forbidden (get_own_application)."""
    login_as(client, world["cand_b"], "candidate")
    resp = client.get(f"/candidate/applications/{world['app_a']}")
    assert resp.status_code == 403


def test_missing_application_detail_is_404(client, world, login_as):
    login_as(client, world["cand_a"], "candidate")
    resp = client.get("/candidate/applications/999999")
    assert resp.status_code == 404


def test_fp_sched_3_conflict_contract(client, conn, world, login_as, csrf_post):
    """Two eligible candidates contend for one slot (brief FP-SCHED-3).

    A books slot_a successfully; B POSTs the same slot: HTTP 409 with the exact
    message "Slot already booked"; still exactly one booking row, still A's; a
    booking.conflict audit row exists for B's failed attempt.
    """
    w = world
    login_as(client, w["cand_a"], "candidate")
    resp = csrf_post(client, f"/candidate/applications/{w['app_a']}/book/{w['slot_a']}", {})
    assert resp.status_code == 302

    # B is also eligible for the same job's employer slots and has no booking.
    login_as(client, w["cand_b"], "candidate")
    resp = csrf_post(client, f"/candidate/applications/{w['app_b']}/book/{w['slot_a']}", {})
    assert resp.status_code == 409
    body = resp.data.decode()
    assert "Slot already booked" in body

    # Exactly one booking for the slot, still A's application; B has none.
    rows = conn.execute("SELECT * FROM bookings WHERE slot_id = ?", (w["slot_a"],)).fetchall()
    assert len(rows) == 1
    assert rows[0]["application_id"] == w["app_a"]
    assert conn.execute(
        "SELECT COUNT(*) AS n FROM bookings WHERE application_id = ?", (w["app_b"],)
    ).fetchone()["n"] == 0

    # The failed attempt left a booking.conflict audit row (after the rollback).
    conflict = conn.execute(
        "SELECT 1 FROM audit_log WHERE action = 'booking.conflict' AND actor_id = ?",
        (w["cand_b"],),
    ).fetchone()
    assert conflict is not None


def test_fp_sched_3_conflict_from_second_connection(app, world):
    """A booking committed by a second connection to the same file is seen by
    book_slot, which raises Conflict and does not double-book.

    Not a synchronized concurrency stress test (the brief does not require
    one): the second connection commits before book_slot runs.
    """
    w = world
    with app.app_context():
        from app.db import get_db

        conn = get_db()
        # A second connection to the same database file, per the task card.
        other = sqlite3.connect(app.config["DATABASE"], isolation_level=None)
        try:
            other.execute("BEGIN IMMEDIATE")
            other.execute(
                "INSERT INTO bookings (slot_id, application_id, booked_at) VALUES (?, ?, ?)",
                (w["slot_a"], w["app_a"], now_iso()),
            )
            other.execute("COMMIT")
        finally:
            other.close()

        # Now book_slot from the first connection sees the slot taken.
        with pytest.raises(Conflict):
            service.book_slot(conn, w["cand_b"], w["app_b"], w["slot_a"])

        n = conn.execute(
            "SELECT COUNT(*) AS n FROM bookings WHERE slot_id = ?", (w["slot_a"],)
        ).fetchone()["n"]
        assert n == 1   # no double booking
        assert conn.execute(
            "SELECT COUNT(*) AS n FROM bookings WHERE application_id = ?", (w["app_b"],)
        ).fetchone()["n"] == 0


@pytest.mark.parametrize("contended_slot", ["same_slot", "other_slot"])
def test_fp_sched_3_overlap_same_application_is_forbidden(app, monkeypatch, world,
                                                          contended_slot):
    """Regression (T17): a second overlapping request for the SAME application.

    The race: the eligibility checks read the application before BEGIN
    IMMEDIATE, so both requests see "no booking yet"; the other request commits
    its booking (on slot_a) after that read but before this one enters the
    transaction. Simulated by committing the other request's booking on a
    second connection right before the real BEGIN IMMEDIATE runs, inside a
    wrapper around booking.transaction. Whether this request aims at the same
    slot the other request took, or a different one, the result must be
    Forbidden (D14), never a 409 conflict, and never a booking.conflict audit.
    """
    w = world
    aimed_slot = w["slot_a"] if contended_slot == "same_slot" else w["slot_c"]

    real_transaction = service.transaction

    def racing_transaction(conn, immediate=False):
        # Runs when book_slot calls transaction(..., immediate=True): the
        # eligibility checks have already passed on a stale snapshot; the
        # other request commits here, just before BEGIN IMMEDIATE. Only that
        # call is intercepted; later transactions (e.g. a conflict audit)
        # pass through untouched.
        if immediate:
            other = sqlite3.connect(app.config["DATABASE"], isolation_level=None)
            try:
                other.execute("BEGIN IMMEDIATE")
                other.execute(
                    "INSERT INTO bookings (slot_id, application_id, booked_at)"
                    " VALUES (?, ?, ?)",
                    (w["slot_a"], w["app_a"], now_iso()),
                )
                other.execute("COMMIT")
            finally:
                other.close()
        return real_transaction(conn, immediate=immediate)

    with app.app_context():
        from app.db import get_db

        conn = get_db()
        monkeypatch.setattr(service, "transaction", racing_transaction)
        before = _count_bookings(conn)
        with pytest.raises(Forbidden):
            service.book_slot(conn, w["cand_a"], w["app_a"], aimed_slot)
        assert _count_bookings(conn) == before + 1   # only the other request's row
        assert conn.execute(
            "SELECT COUNT(*) AS n FROM bookings WHERE application_id = ?", (w["app_a"],)
        ).fetchone()["n"] == 1
        assert conn.execute(
            "SELECT COUNT(*) AS n FROM audit_log WHERE action = 'booking.conflict'"
        ).fetchone()["n"] == 0


def test_fp_sched_3_same_candidate_twice_is_forbidden_not_conflict(conn, world, make_booking):
    """The same application re-POSTing after booking is Forbidden (D14,
    FP-SCHED-2 no-existing-booking), not the FP-SCHED-3 conflict — even though
    the slot is also occupied. The original booking is unchanged and the
    refusal is not recorded as booking.conflict."""
    w = world
    make_booking(w["app_a"], w["slot_a"])   # this application already booked slot_a
    before = _count_bookings(conn)
    with pytest.raises(Forbidden):
        service.book_slot(conn, w["cand_a"], w["app_a"], w["slot_a"])
    assert _count_bookings(conn) == before
    row = conn.execute(
        "SELECT slot_id, application_id FROM bookings WHERE application_id = ?", (w["app_a"],)
    ).fetchone()
    assert row["slot_id"] == w["slot_a"]
    assert conn.execute(
        "SELECT COUNT(*) AS n FROM audit_log WHERE action = 'booking.conflict'"
    ).fetchone()["n"] == 0
