"""T13 · candidate recommendations."""

import pytest

from app.candidates.profile_service import get_profile
from app.errors import NotFound
from app.jobs.service import list_jobs
from app.matching import engine, service


def test_fp_can_2_recommendations_preserve_fields_and_rank_all_jobs(
    conn, make_candidate, make_employer, make_job
):
    candidate_id = make_candidate(skills=("python", "sql"))
    employer_id = make_employer()
    make_job(employer_id, title="Zero overlap", skills=("go",))
    make_job(employer_id, title="No required skills", skills=())
    make_job(employer_id, title="A great fit", skills=("python", "sql"))
    make_job(employer_id, title="Some overlap", skills=("python", "go"))

    original = list_jobs(conn)
    expected = engine.rank(set(get_profile(conn, candidate_id)["skills"]), original)
    recommendations = service.recommend_for(conn, candidate_id)

    assert len(recommendations) == len(original)
    assert recommendations == expected
    for job in original:
        actual = next(item for item in recommendations if item["id"] == job["id"])
        assert {key: actual[key] for key in job} == job
    no_skills_job = next(job for job in recommendations if job["title"] == "No required skills")
    zero_overlap_job = next(job for job in recommendations if job["title"] == "Zero overlap")
    assert no_skills_job["score"] == 100
    assert zero_overlap_job["score"] == 0
    assert service.score_candidate_for_job(conn, candidate_id, next(
        job["id"] for job in original if job["title"] == "Zero overlap"
    ))["score"] == 0
    with pytest.raises(NotFound):
        service.score_candidate_for_job(conn, candidate_id, 99999)


def test_recommendations_page_ranks_all_jobs_and_shows_match_explanation(
    client, make_candidate, make_employer, make_job, login_as
):
    candidate_id = make_candidate(skills=("python", "sql"))
    employer_id = make_employer()
    make_job(employer_id, title="Zero overlap", skills=("go",))
    make_job(employer_id, title="No required skills", skills=())
    make_job(employer_id, title="A great fit", skills=("python", "sql"))
    login_as(client, candidate_id, "candidate")

    response = client.get("/candidate/recommendations")
    body = response.get_data(as_text=True)
    assert response.status_code == 200
    titles = ("A great fit", "No required skills", "Zero overlap")
    positions = [body.index(title) for title in titles]
    assert positions == sorted(positions)
    assert "Matched:" in body
    assert "Missing:" in body
    assert 'href="/jobs/' in body


def test_candidate_without_skills_sees_hint_and_full_recommendations(
    client, make_candidate, make_employer, make_job, login_as
):
    candidate_id = make_candidate(skills=())
    employer_id = make_employer()
    make_job(employer_id, title="A job", skills=("python",))
    login_as(client, candidate_id, "candidate")
    response = client.get("/candidate/recommendations")
    body = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "Add your skills to see how jobs match you." in body
    assert "A job" in body
    assert body.index("Add your skills to see how jobs match you.") < body.index("A job")


def test_employer_cannot_open_candidate_recommendations(client, make_employer, login_as):
    employer_id = make_employer()
    login_as(client, employer_id, "employer")
    assert client.get("/candidate/recommendations").status_code == 403


def test_recommendations_page_empty_state(client, make_candidate, login_as):
    candidate_id = make_candidate(skills=())
    login_as(client, candidate_id, "candidate")
    response = client.get("/candidate/recommendations")
    body = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "No jobs right now. Check back soon." in body
