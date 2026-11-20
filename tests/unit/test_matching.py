"""Matching engine tests (FP-MATCH-1). Rules and examples quoted from the brief,
section "5. Matching contract", FP-MATCH-1 "Score definition"."""

import copy
import random

import pytest

from app.matching.engine import rank, score


def _job(job_id: int, title: str, skills: list[str], **extra) -> dict:
    """A dict shaped like jobs.service.list_jobs output (07-CONTRACTS.md: id,
    title, skills as a list of normalised names, created_at, and more)."""
    job = {
        "id": job_id,
        "title": title,
        "skills": list(skills),
        "company_name": "Harbourline Logistics",
        "created_at": "2026-11-01T00:00:00Z",
    }
    job.update(extra)
    return job


@pytest.mark.parametrize(
    ("candidate_text", "required_text", "expected_score", "expected_matched",
     "expected_missing"),
    [
        # brief: "5. Matching contract", FP-MATCH-1 example table, row 1
        ("Python, SQL", "Python, SQL", 100, ["python", "sql"], []),
        # brief: "5. Matching contract", FP-MATCH-1 example table, row 2
        ("Python", "Python, SQL", 50, ["python"], ["sql"]),
        # brief: "5. Matching contract", FP-MATCH-1 example table, row 3
        ("Rust", "Python, SQL", 0, [], ["python", "sql"]),
        # brief: "5. Matching contract", FP-MATCH-1 example table, row 4
        # ("any skills", "empty list")
        ("Python, Rust", "", 100, [], []),
    ],
)
def test_fp_match_1_examples_normalization_and_floor(
    candidate_text, required_text, expected_score, expected_matched, expected_missing
):
    # The brief's comma-separated lists, split without normalising first, so
    # score() has to do the normalisation itself.
    result = score(set(candidate_text.split(",")), set(required_text.split(",")))
    assert result == {
        "score": expected_score,
        "matched": expected_matched,
        "missing": expected_missing,
    }
    assert isinstance(result["score"], int)

    # Normalisation (brief FP-MATCH-1): trim surrounding whitespace, convert to
    # lowercase, remove empty values, remove duplicates. Nothing else.
    assert score({"  PYTHON  ", "Python", "python", "", "   "}, {"python"}) == {
        "score": 100,
        "matched": ["python"],
        "missing": [],
    }
    assert score({"python"}, {" PYTHON ", "Python", ""}) == {
        "score": 100,
        "matched": ["python"],
        "missing": [],
    }
    # Required skills that are all empty values: |R| = 0 after normalisation.
    assert score({"python"}, {"", "   "})["score"] == 100

    # Floor (brief FP-MATCH-1): at, just under and just over an integer boundary.
    assert score({"python"}, {"python", "sql"})["score"] == 50  # exactly 50
    # 100 * 2 / 3 = 66.67 -> 66
    assert score({"python", "sql"}, {"python", "sql", "rust"})["score"] == 66
    # 100 * 1 / 3 = 33.33 -> 33
    assert score({"python"}, {"python", "sql", "rust"})["score"] == 33


def test_fp_match_1_both_tie_breakers():
    # Tie-breaker 1 (brief FP-MATCH-1): equal scores are split by
    # case-insensitive job title, before job id.
    jobs = [
        _job(1, "Zebra Developer", ["python"]),
        _job(2, "alpha developer", ["python"]),
    ]
    snapshot = copy.deepcopy(jobs)
    assert [j["id"] for j in rank({"python"}, jobs)] == [2, 1]
    # Reversing the input order gives the same result.
    assert [j["id"] for j in rank({"python"}, list(reversed(jobs)))] == [2, 1]
    # The input is not mutated.
    assert jobs == snapshot

    # Tie-breaker 2 (brief FP-MATCH-1): equal score and equal case-insensitive
    # title are split by ascending job id.
    jobs = [
        _job(9, "Data Analyst", ["python", "sql"]),
        _job(4, "DATA ANALYST", ["python", "sql"]),
    ]
    snapshot = copy.deepcopy(jobs)
    ranked = rank({"python"}, jobs)
    assert [j["id"] for j in ranked] == [4, 9]
    assert [j["id"] for j in rank({"python"}, list(reversed(jobs)))] == [4, 9]
    assert jobs == snapshot
    # New dicts: original fields kept, match result added.
    assert set(ranked[0]) == {
        "id", "title", "skills", "company_name", "created_at",
        "score", "matched", "missing",
    }
    assert ranked[0]["title"] == "DATA ANALYST"
    assert ranked[0]["score"] == 50
    assert ranked[0]["matched"] == ["python"]
    assert ranked[0]["missing"] == ["sql"]


def test_score_candidate_with_no_skills():
    # |C| = 0, so |C intersection R| = 0 and the score is 0 (brief FP-MATCH-1).
    assert score(set(), {"python", "sql"}) == {
        "score": 0,
        "matched": [],
        "missing": ["python", "sql"],
    }


def test_rank_job_with_no_required_skills():
    # |R| = 0, so the score is 100 (brief FP-MATCH-1).
    ranked = rank({"python"}, [_job(1, "Dev", [])])
    assert len(ranked) == 1
    assert ranked[0]["score"] == 100
    assert ranked[0]["matched"] == []
    assert ranked[0]["missing"] == []


def test_rank_empty_job_list():
    assert rank({"python"}, []) == []


def test_rank_property_fixed_seed():
    """Task card: random.Random(1234), 200 rounds."""
    rng = random.Random(1234)
    skill_pool = ["python", "sql", "rust", "go", "excel", "tableau"]
    titles = [
        "Data Analyst",
        "Backend Engineer",
        "QA Engineer",
        "data analyst",
        "Go Developer",
    ]
    for _ in range(200):
        n = rng.randint(0, 6)
        ids = rng.sample(range(1, 100), n)
        jobs = [
            _job(
                ids[i],
                rng.choice(titles),
                rng.sample(skill_pool, rng.randint(0, len(skill_pool))),
            )
            for i in range(n)
        ]
        candidate = set(rng.sample(skill_pool, rng.randint(0, len(skill_pool))))
        snapshot = copy.deepcopy(jobs)

        ranked = rank(candidate, jobs)

        # Every job appears exactly once.
        assert sorted(j["id"] for j in ranked) == sorted(j["id"] for j in jobs)
        # The input list and dicts are unchanged, and the output dicts are new.
        assert jobs == snapshot
        assert all(out is not orig for out in ranked for orig in jobs)
        # Original fields are kept and the match result is added.
        by_id = {j["id"]: j for j in jobs}
        for out in ranked:
            for key, value in by_id[out["id"]].items():
                assert out[key] == value
            assert {"score", "matched", "missing"} <= set(out)
        # Brief order: score descending, then title.lower(), then id.
        keys = [(-j["score"], j["title"].lower(), j["id"]) for j in ranked]
        assert keys == sorted(keys)
        # Running rank again gives the same order.
        again = rank(candidate, jobs)
        assert [j["id"] for j in again] == [j["id"] for j in ranked]
