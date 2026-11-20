"""Tests for the T04 fixtures in tests/conftest.py: factories, login_as, csrf_post."""

from werkzeug.security import check_password_hash


def test_make_candidate_twice(conn, make_candidate):
    first = make_candidate()
    second = make_candidate()
    assert first != second

    rows = {
        r["id"]: r
        for r in conn.execute("SELECT * FROM users WHERE id IN (?, ?)", (first, second))
    }
    assert sorted(rows) == sorted((first, second))
    assert len({rows[first]["email"], rows[second]["email"]}) == 2  # no UNIQUE clash
    for user_id in (first, second):
        row = rows[user_id]
        assert row["role"] == "candidate"
        assert row["display_name"] == "Mei Lin Tan"
        assert row["password_hash"] != "Passw0rd!"  # stored hashed, not plaintext
        assert check_password_hash(row["password_hash"], "Passw0rd!")

        profile = conn.execute(
            "SELECT * FROM candidate_profiles WHERE user_id = ?", (user_id,)
        ).fetchone()
        assert profile is not None
        assert profile["timezone"] == "UTC"

        skill_names = [
            r["name"]
            for r in conn.execute(
                "SELECT s.name FROM skills s"
                " JOIN candidate_skills cs ON cs.skill_id = s.id"
                " WHERE cs.candidate_id = ? ORDER BY s.name",
                (user_id,),
            )
        ]
        assert skill_names == ["python", "sql"]


def test_make_employer_twice(conn, make_employer):
    first = make_employer()
    second = make_employer()
    assert first != second

    rows = {
        r["id"]: r
        for r in conn.execute("SELECT * FROM users WHERE id IN (?, ?)", (first, second))
    }
    assert len({rows[first]["email"], rows[second]["email"]}) == 2
    for user_id in (first, second):
        assert rows[user_id]["role"] == "employer"
        assert rows[user_id]["display_name"] == "Daniel Wong"
        assert check_password_hash(rows[user_id]["password_hash"], "Passw0rd!")


def test_make_company_twice(conn, make_employer, make_company):
    emp_a = make_employer()
    emp_b = make_employer()
    company_a = make_company(emp_a)
    company_b = make_company(emp_b, name="Nimbus Freight")
    assert company_a != company_b

    row = conn.execute("SELECT * FROM companies WHERE id = ?", (company_a,)).fetchone()
    assert row["owner_id"] == emp_a
    assert row["name"] == "Harbourline Logistics"
    row = conn.execute("SELECT * FROM companies WHERE id = ?", (company_b,)).fetchone()
    assert row["owner_id"] == emp_b
    assert row["name"] == "Nimbus Freight"


def test_make_job_twice(conn, make_employer, make_company, make_job):
    emp = make_employer()
    first = make_job(emp, skills=("python", "sql"))
    second = make_job(emp, title="Warehouse Lead", skills=())
    assert first != second

    # Both jobs hang off the company auto-created for the employer.
    companies = conn.execute(
        "SELECT id FROM companies WHERE owner_id = ?", (emp,)
    ).fetchall()
    assert len(companies) == 1
    for job_id, expected_title in ((first, "Data Analyst"), (second, "Warehouse Lead")):
        row = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
        assert row["company_id"] == companies[0]["id"]
        assert row["title"] == expected_title

    skill_names = [
        r["name"]
        for r in conn.execute(
            "SELECT s.name FROM skills s JOIN job_skills js ON js.skill_id = s.id"
            " WHERE js.job_id = ? ORDER BY s.name",
            (first,),
        )
    ]
    assert skill_names == ["python", "sql"]
    n_skills = conn.execute(
        "SELECT COUNT(*) FROM job_skills WHERE job_id = ?", (second,)
    ).fetchone()[0]
    assert n_skills == 0

    # An existing company is reused, not duplicated.
    emp2 = make_employer()
    make_company(emp2, name="Anchor Terminals")
    job = make_job(emp2)
    row = conn.execute("SELECT * FROM jobs WHERE id = ?", (job,)).fetchone()
    owner_row = conn.execute(
        "SELECT id, name FROM companies WHERE owner_id = ?", (emp2,)
    ).fetchone()
    assert row["company_id"] == owner_row["id"]
    assert owner_row["name"] == "Anchor Terminals"


def test_make_application_twice(conn, make_candidate, make_job, make_employer, make_application):
    emp = make_employer()
    job = make_job(emp)
    cand_a = make_candidate()
    cand_b = make_candidate()
    first = make_application(cand_a, job)
    second = make_application(cand_b, job, status="interviewing")
    assert first != second

    for app_id, cand_id, status in (
        (first, cand_a, "pending"),
        (second, cand_b, "interviewing"),
    ):
        row = conn.execute("SELECT * FROM applications WHERE id = ?", (app_id,)).fetchone()
        assert row["job_id"] == job
        assert row["candidate_id"] == cand_id
        assert row["status"] == status


def test_make_slot_twice(conn, make_employer, make_slot):
    emp = make_employer()
    first = make_slot(emp)
    second = make_slot(emp, starts_at="2030-02-10T04:00:00Z", ends_at="2030-02-10T04:30:00Z")
    assert first != second

    for slot_id, starts_at in ((first, "2030-01-07T02:00:00Z"), (second, "2030-02-10T04:00:00Z")):
        row = conn.execute(
            "SELECT * FROM interview_slots WHERE id = ?", (slot_id,)
        ).fetchone()
        assert row["employer_id"] == emp
        assert row["starts_at"] == starts_at
        assert row["ends_at"] > row["starts_at"]
        assert row["created_tz"] == "UTC"


def test_make_booking_twice(conn, make_candidate, make_employer, make_job, make_application,
                            make_slot, make_booking):
    emp = make_employer()
    job = make_job(emp)
    cand_a = make_candidate()
    cand_b = make_candidate()
    app_a = make_application(cand_a, job, status="interviewing")
    app_b = make_application(cand_b, job, status="interviewing")
    slot_a = make_slot(emp)
    slot_b = make_slot(emp, starts_at="2030-02-10T04:00:00Z", ends_at="2030-02-10T04:30:00Z")

    first = make_booking(app_a, slot_a)
    second = make_booking(app_b, slot_b)
    assert first != second

    for booking_id, app_id, slot_id in ((first, app_a, slot_a), (second, app_b, slot_b)):
        row = conn.execute("SELECT * FROM bookings WHERE id = ?", (booking_id,)).fetchone()
        assert row["application_id"] == app_id
        assert row["slot_id"] == slot_id


def test_login_as_redirects_by_role(client, make_candidate, make_employer, login_as):
    cand = make_candidate()
    login_as(client, cand, "candidate")
    resp = client.get("/")
    assert resp.status_code == 302
    assert resp.headers["Location"] == "/candidate/"

    emp = make_employer()
    login_as(client, emp, "employer")
    resp = client.get("/")
    assert resp.status_code == 302
    assert resp.headers["Location"] == "/employer/"


def test_csrf_post_to_nowhere_is_404_not_403(client, csrf_post):
    resp = csrf_post(client, "/nowhere", {"x": "1"})
    assert resp.status_code == 404
