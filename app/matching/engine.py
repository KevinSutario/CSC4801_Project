"""Pure matching engine (FP-MATCH-1).

Rules from docs/BRIEF.md, section "5. Matching contract", FP-MATCH-1
"Score definition" (quoted on the task card docs/tasks/T11.md):

> Normalize candidate and required skills by trimming surrounding whitespace,
> converting to lowercase, removing empty values, and removing duplicates.
>
> score = 100                                      when |R| = 0
> score = floor(100 * |C intersection R| / |R|)   otherwise

Resume text is not an input. No synonyms, punctuation handling or
inner-space collapsing: none are in the brief. This module is pure: it imports
only app.skills and the standard library, touches no database.
"""

from __future__ import annotations

from app.skills import normalise_skill


def _normalised(raw_skills: set[str]) -> set[str]:
    """The brief's normalisation: strip, lower-case, drop empty values, dedupe."""
    return {name for raw in raw_skills if (name := normalise_skill(raw))}


def score(candidate_skills: set[str], job_skills: set[str]) -> dict:
    """Score a candidate against one job's required skills.

    Returns {"score": int, "matched": sorted list, "missing": sorted list}.
    """
    candidate = _normalised(candidate_skills)
    required = _normalised(job_skills)

    if not required:
        return {"score": 100, "matched": [], "missing": []}

    matched = candidate & required
    missing = required - candidate
    # floor(100 * |C intersection R| / |R|) with integer arithmetic.
    return {
        "score": 100 * len(matched) // len(required),
        "matched": sorted(matched),
        "missing": sorted(missing),
    }


def rank(candidate_skills: set[str], jobs: list[dict]) -> list[dict]:
    """Rank jobs for a candidate.

    Returns new dicts (every original key unchanged, plus score, matched,
    missing), sorted by score descending, then case-insensitive job title,
    then job id. Never mutates the input list or its dicts.
    """
    ranked: list[dict] = []
    for job in jobs:
        result = score(candidate_skills, set(job.get("skills", [])))
        ranked.append(dict(job) | result)
    ranked.sort(key=lambda job: (-job["score"], job["title"].lower(), job["id"]))
    return ranked
