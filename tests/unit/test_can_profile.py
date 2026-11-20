"""T07 · candidate profile and skills."""

import pytest

from app.candidates import profile_service
from app.errors import ValidationError


def test_save_then_get_normalises_and_sorts_skills(conn, make_candidate):
    candidate_id = make_candidate(skills=())
    profile_service.save_profile(
        conn, candidate_id, "  Mei Lin  ", " Analyst ", " Hong Kong ",
        "Asia/Hong_Kong", " Summary ", "SQL, python, SQL, ,Python",
    )
    profile = profile_service.get_profile(conn, candidate_id)
    assert profile == {
        "display_name": "Mei Lin",
        "headline": "Analyst",
        "location": "Hong Kong",
        "timezone": "Asia/Hong_Kong",
        "summary": "Summary",
        "skills": ["python", "sql"],
        "updated_at": profile["updated_at"],
    }
    assert profile["updated_at"]


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("display_name", "x" * 81),
        ("headline", "x" * 121),
        ("location", "x" * 81),
        ("summary", "x" * 2001),
        ("skills_text", ",".join(f"s{i}" for i in range(31))),
    ],
)
def test_profile_limits_reject_without_saving(conn, make_candidate, field, value):
    candidate_id = make_candidate(skills=())
    before = profile_service.get_profile(conn, candidate_id)
    values = {
        "display_name": "Mei", "headline": "", "location": "",
        "timezone": "UTC", "summary": "", "skills_text": "python",
    }
    values[field] = value
    with pytest.raises(ValidationError) as error:
        profile_service.save_profile(conn, candidate_id, **values)
    assert field in error.value.errors
    assert profile_service.get_profile(conn, candidate_id) == before


@pytest.mark.parametrize("display_name", ["", " " , "x" * 81])
def test_display_name_invalid(conn, make_candidate, display_name):
    candidate_id = make_candidate()
    with pytest.raises(ValidationError) as error:
        profile_service.save_profile(
            conn, candidate_id, display_name, "", "", "UTC", "", "python"
        )
    assert "display_name" in error.value.errors


def test_invalid_timezone_rejected(conn, make_candidate):
    candidate_id = make_candidate()
    with pytest.raises(ValidationError) as error:
        profile_service.save_profile(
            conn, candidate_id, "Mei", "", "", "Mars/Base", "", "python"
        )
    assert "timezone" in error.value.errors


def test_saving_again_replaces_skills(conn, make_candidate):
    candidate_id = make_candidate(skills=())
    profile_service.save_profile(conn, candidate_id, "Mei", "", "", "UTC", "", "python,sql")
    profile_service.save_profile(conn, candidate_id, "Mei", "", "", "UTC", "", "Go")
    assert profile_service.get_profile(conn, candidate_id)["skills"] == ["go"]


def test_candidate_profile_routes_roles_and_post(
    client, make_candidate, make_employer, login_as, csrf_post
):
    candidate_id = make_candidate(skills=())
    employer_id = make_employer()
    response = client.get("/candidate/profile")
    assert response.status_code == 302
    assert response.headers["Location"].startswith("/auth/login")
    login_as(client, employer_id, "employer")
    assert client.get("/candidate/profile").status_code == 403
    login_as(client, candidate_id, "candidate")
    response = csrf_post(client, "/candidate/profile", {
        "display_name": "Mei Updated", "headline": "Analyst", "location": "HK",
        "timezone": "UTC", "summary": "Summary", "skills_text": "Python, sql",
    })
    assert response.status_code == 302
    assert response.headers["Location"] == "/candidate/profile"
    assert "Profile saved" in client.get("/candidate/profile").get_data(as_text=True)


def test_candidate_home_welcomes_and_links(client, make_candidate, login_as):
    candidate_id = make_candidate(name="Mei")
    login_as(client, candidate_id, "candidate")
    response = client.get("/candidate/")
    body = response.get_data(as_text=True)
    assert response.status_code == 200
    targets = (
        "/candidate/recommendations", "/candidate/applications",
        "/candidate/profile", "/candidate/resume",
    )
    for target in targets:
        assert target in body
    assert "Mei" in body
