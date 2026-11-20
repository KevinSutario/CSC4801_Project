"""Interview slot requirement tests (FP-SCHED-1). Owned by T12.

Rule (brief section 6, FP-SCHED-1 "Availability"): employers create and delete
future, 30-minute slots; invalid durations, end-before-start and deletion of a
booked slot are rejected; booked slots are never shown as available.
"""

import pytest

from app.errors import Conflict, Forbidden, NotFound, ValidationError
from app.scheduling import slots as service


def _count_slots(conn) -> int:
    return conn.execute("SELECT COUNT(*) AS n FROM interview_slots").fetchone()["n"]


def test_fp_sched_1_slot_creation_timezones_and_deletion(conn, make_employer, make_company,
                                                         make_candidate):
    emp = make_employer()
    # Create 2030-01-07 10:00-10:30 Hong Kong time -> 02:00-02:30 UTC, stored UTC.
    slot_id = service.create_slot(conn, emp, "2030-01-07", "10:00", "10:30",
                                  "Asia/Hong_Kong")
    row = conn.execute("SELECT * FROM interview_slots WHERE id = ?", (slot_id,)).fetchone()
    assert row["starts_at"] == "2030-01-07T02:00:00Z"
    assert row["ends_at"] == "2030-01-07T02:30:00Z"
    assert row["created_tz"] == "Asia/Hong_Kong"

    listed = service.list_slots_for_employer(conn, emp)
    assert len(listed) == 1
    assert listed[0]["id"] == slot_id
    assert listed[0]["booked"] is False

    # Delete works on an unbooked slot.
    service.delete_slot(conn, emp, slot_id)
    assert _count_slots(conn) == 0
    with pytest.raises(NotFound):
        service.delete_slot(conn, emp, slot_id)  # now missing

    # A booked slot cannot be deleted (Conflict).
    slot2 = service.create_slot(conn, emp, "2030-02-01", "09:00", "09:30",
                                "Asia/Hong_Kong")
    cand = make_candidate()
    company_id = make_company(emp)
    with conn:  # direct SQL, as the card says: insert a booking with SQL
        job = conn.execute(
            "INSERT INTO jobs (company_id, title, description, created_at, updated_at)"
            " VALUES (?, 'J', 'D', '2030-01-01T00:00:00Z', '2030-01-01T00:00:00Z')",
            (company_id,),
        ).lastrowid
        app_id = conn.execute(
            "INSERT INTO applications (job_id, candidate_id, status, created_at, updated_at)"
            " VALUES (?, ?, 'interviewing', '2030-01-01T00:00:00Z', '2030-01-01T00:00:00Z')",
            (job, cand),
        ).lastrowid
        conn.execute(
            "INSERT INTO bookings (slot_id, application_id, booked_at)"
            " VALUES (?, ?, '2030-01-01T00:00:00Z')",
            (slot2, app_id),
        )
    with pytest.raises(Conflict):
        service.delete_slot(conn, emp, slot2)
    # and the slot is listed as booked, not available
    listed = service.list_slots_for_employer(conn, emp)
    assert listed[0]["booked"] is True

    # Another employer's slot cannot be deleted (Forbidden, D9).
    emp_b = make_employer(email="emp-b@example.com")
    slot_b = service.create_slot(conn, emp_b, "2030-03-01", "09:00", "09:30",
                                 "Asia/Hong_Kong")
    with pytest.raises(Forbidden):
        service.delete_slot(conn, emp, slot_b)
    assert conn.execute("SELECT COUNT(*) AS n FROM interview_slots WHERE id = ?",
                        (slot_b,)).fetchone()["n"] == 1


@pytest.mark.parametrize(
    "date,start,end,tz,field",
    [
        ("2030-13-01", "10:00", "10:30", "UTC", "date"),          # bad date
        ("2030-01-07", "25:00", "25:30", "UTC", "start"),         # bad time
        ("2030-01-07", "10:30", "10:00", "UTC", "end"),           # end before start
        ("2030-01-07", "10:00", "10:29", "UTC", "end"),           # 29 minutes
        ("2030-01-07", "10:00", "10:31", "UTC", "end"),           # 31 minutes
        ("2020-01-07", "10:00", "10:30", "UTC", "start"),         # in the past
        ("2030-01-07", "10:00", "10:30", "Mars/Base", "timezone"),  # unknown zone
    ],
)
def test_fp_sched_1_invalid_slots(conn, make_employer, date, start, end, tz, field):
    emp = make_employer()
    before = _count_slots(conn)
    with pytest.raises(ValidationError) as exc:
        service.create_slot(conn, emp, date, start, end, tz)
    assert field in exc.value.errors
    assert _count_slots(conn) == before


def test_invalid_slot_overlapping_own_slot(conn, make_employer):
    emp = make_employer()
    service.create_slot(conn, emp, "2030-01-07", "10:00", "10:30", "UTC")
    before = _count_slots(conn)
    with pytest.raises(ValidationError) as exc:
        service.create_slot(conn, emp, "2030-01-07", "10:15", "10:45", "UTC")
    assert "start" in exc.value.errors or "end" in exc.value.errors
    assert _count_slots(conn) == before


def test_overlap_with_other_employer_is_fine(conn, make_employer):
    emp_a = make_employer()
    emp_b = make_employer(email="emp-b@example.com")
    service.create_slot(conn, emp_a, "2030-01-07", "10:00", "10:30", "UTC")
    service.create_slot(conn, emp_b, "2030-01-07", "10:00", "10:30", "UTC")
    assert _count_slots(conn) == 2


def test_candidate_post_to_slots_page_is_403(client, make_candidate, login_as, csrf_post):
    cand = make_candidate()
    login_as(client, cand, "candidate")
    resp = csrf_post(client, "/employer/slots", {
        "date": "2030-01-07", "start": "10:00", "end": "10:30", "timezone": "UTC",
    })
    assert resp.status_code == 403


def test_employer_can_see_slots_page(client, conn, make_employer, login_as):
    emp = make_employer()
    service.create_slot(conn, emp, "2030-01-07", "10:00", "10:30", "Asia/Hong_Kong")
    login_as(client, emp, "employer")
    resp = client.get("/employer/slots")
    assert resp.status_code == 200
    assert b"2030-01-07T02:00:00Z" not in resp.data  # list is shown in the chosen zone
    assert "10:00".encode() in resp.data


def test_bad_date_error_shown_under_date_field(client, conn, make_employer, login_as,
                                               csrf_post):
    """An invalid date reports on the date field and renders under the date box,
    not under the start-time box."""
    emp = make_employer()
    login_as(client, emp, "employer")
    resp = csrf_post(client, "/employer/slots", {
        "date": "2030-13-01", "start": "10:00", "end": "10:30", "timezone": "UTC",
    })
    assert resp.status_code == 400
    body = resp.data.decode()
    assert 'id="date-error"' in body          # the date box has an error
    assert 'id="start-error"' not in body     # the start box does not


def test_employer_post_valid_slot_creates_and_stores_utc(client, conn, make_employer,
                                                         login_as, csrf_post):
    """The success path: a real employer POST creates the slot (302 back to the
    page) and it is stored owned by that employer in UTC."""
    emp = make_employer()
    login_as(client, emp, "employer")
    resp = csrf_post(client, "/employer/slots", {
        "date": "2030-01-07", "start": "10:00", "end": "10:30",
        "timezone": "Asia/Hong_Kong",
    })
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/employer/slots")
    row = conn.execute("SELECT * FROM interview_slots").fetchone()
    assert row is not None                    # exactly one slot was created
    assert row["employer_id"] == emp
    assert row["starts_at"] == "2030-01-07T02:00:00Z"   # 10:00 HK = 02:00 UTC
    assert row["ends_at"] == "2030-01-07T02:30:00Z"     # 10:30 HK = 02:30 UTC
    assert row["created_tz"] == "Asia/Hong_Kong"
