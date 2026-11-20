"""Employer company requirement tests (FP-EMP-1, FP-SEC-3). Owned by T09."""

import pytest

from app.employers import service
from app.errors import ValidationError


def _count_companies(conn) -> int:
    return conn.execute("SELECT COUNT(*) AS n FROM companies").fetchone()["n"]


def test_fp_emp_1_company_profile(conn, make_employer):
    emp = make_employer()
    # create
    cid = service.save_company(conn, emp, "Harbourline Logistics", "Logistics",
                               "Singapore", "https://harbourline.example", "We move things.")
    assert isinstance(cid, int)
    got = service.get_company(conn, emp)
    assert got["name"] == "Harbourline Logistics"
    assert got["description"] == "We move things."

    # update returns the SAME id (one company per employer, upsert on owner_id)
    cid2 = service.save_company(conn, emp, "Harbourline Pte", "Logistics", "Singapore",
                                "https://harbourline.example", "Updated.")
    assert cid2 == cid
    assert service.get_company(conn, emp)["name"] == "Harbourline Pte"
    assert _count_companies(conn) == 1

    # get_company_by_id
    assert service.get_company_by_id(conn, cid)["name"] == "Harbourline Pte"
    assert service.get_company_by_id(conn, 999999) is None


@pytest.mark.parametrize(
    "name,website,bad_field",
    [
        ("", "https://ok.example", "name"),
        ("   ", "https://ok.example", "name"),
        ("x" * 121, "https://ok.example", "name"),
        ("Ok Co", "javascript:alert(1)", "website"),
        ("Ok Co", "ftp://nope.example", "website"),
        ("Ok Co", "x" * 201, "website"),
    ],
)
def test_company_validation_errors(conn, make_employer, name, website, bad_field):
    emp = make_employer()
    before = _count_companies(conn)
    with pytest.raises(ValidationError) as exc:
        service.save_company(conn, emp, name, "Industry", "Loc", website, "Desc")
    assert bad_field in exc.value.errors
    assert _count_companies(conn) == before  # nothing written


def test_website_optional_when_empty(conn, make_employer):
    emp = make_employer()
    cid = service.save_company(conn, emp, "No Site Co", "", "", "", "")
    assert service.get_company_by_id(conn, cid)["website"] == ""


def test_candidate_cannot_open_company_page(client, make_candidate, login_as):
    uid = make_candidate()
    login_as(client, uid, "candidate")
    assert client.get("/employer/company").status_code == 403


def test_company_form_post_redirects_with_flash(client, make_employer, login_as, csrf_post):
    emp = make_employer()
    login_as(client, emp, "employer")
    resp = csrf_post(client, "/employer/company", {
        "name": "Formful Co", "industry": "Tech", "location": "Remote",
        "website": "https://formful.example", "description": "Hello",
    })
    assert resp.status_code == 302
    # follow and confirm a success flash is shown
    resp2 = client.get("/employer/", follow_redirects=True)
    assert b"Formful Co" in resp2.data


def test_fp_sec_3_script_tag_is_escaped(client, conn, make_employer, login_as, csrf_post):
    emp = make_employer()
    login_as(client, emp, "employer")
    payload = "<script>alert(1)</script>"
    csrf_post(client, "/employer/company", {
        "name": payload, "industry": "", "location": "",
        "website": "", "description": payload,
    })
    resp = client.get("/employer/company")
    body = resp.get_data(as_text=True)
    assert "<script>alert(1)</script>" not in body
    assert "&lt;script&gt;" in body
