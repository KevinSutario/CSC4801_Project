"""Employer company service. Owned by T09.

One company per employer (companies.owner_id is UNIQUE); save_company upserts.
All limits are DEFAULT (not in brief) per the T09 card. Writes run in one
transaction and are audited as company.update.
"""

import sqlite3

from app import audit
from app.db import now_iso, transaction
from app.errors import ValidationError

_NAME_MAX = 120
_INDUSTRY_MAX = 80
_LOCATION_MAX = 80
_WEBSITE_MAX = 200
_DESCRIPTION_MAX = 4000


def _validate(name, industry, location, website, description) -> tuple[dict, dict]:
    """Return (clean_fields, errors). errors empty when valid."""
    errors: dict[str, str] = {}
    clean = {
        "name": (name or "").strip(),
        "industry": (industry or "").strip(),
        "location": (location or "").strip(),
        "website": (website or "").strip(),
        "description": (description or "").strip(),
    }
    if not (1 <= len(clean["name"]) <= _NAME_MAX):
        errors["name"] = f"Company name is required (1 to {_NAME_MAX} characters)."
    if len(clean["industry"]) > _INDUSTRY_MAX:
        errors["industry"] = f"Industry must be at most {_INDUSTRY_MAX} characters."
    if len(clean["location"]) > _LOCATION_MAX:
        errors["location"] = f"Location must be at most {_LOCATION_MAX} characters."
    if clean["website"]:
        if len(clean["website"]) > _WEBSITE_MAX:
            errors["website"] = f"Website must be at most {_WEBSITE_MAX} characters."
        elif not (clean["website"].startswith("https://")
                  or clean["website"].startswith("http://")):
            errors["website"] = "Website must start with https:// or http://."
    if len(clean["description"]) > _DESCRIPTION_MAX:
        errors["description"] = f"Description must be at most {_DESCRIPTION_MAX} characters."
    return clean, errors


def _row_to_dict(row) -> dict | None:
    return dict(row) if row else None


def get_company(conn: sqlite3.Connection, employer_id: int) -> dict | None:
    """The employer's company, or None."""
    return _row_to_dict(
        conn.execute(
            "SELECT id, owner_id, name, industry, location, website, description, updated_at"
            " FROM companies WHERE owner_id = ?",
            (employer_id,),
        ).fetchone()
    )


def get_company_by_id(conn: sqlite3.Connection, company_id: int) -> dict | None:
    """A company by its id, or None."""
    return _row_to_dict(
        conn.execute(
            "SELECT id, owner_id, name, industry, location, website, description, updated_at"
            " FROM companies WHERE id = ?",
            (company_id,),
        ).fetchone()
    )


def save_company(conn: sqlite3.Connection, employer_id: int, name: str, industry: str,
                 location: str, website: str, description: str) -> int:
    """Create or update the employer's single company. Returns the company id.

    Raises ValidationError with a field->message dict for any invalid field.
    """
    clean, errors = _validate(name, industry, location, website, description)
    if errors:
        raise ValidationError(errors)
    with transaction(conn):
        conn.execute(
            "INSERT INTO companies (owner_id, name, industry, location, website,"
            " description, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)"
            " ON CONFLICT(owner_id) DO UPDATE SET"
            " name=excluded.name, industry=excluded.industry, location=excluded.location,"
            " website=excluded.website, description=excluded.description,"
            " updated_at=excluded.updated_at",
            (employer_id, clean["name"], clean["industry"], clean["location"],
             clean["website"], clean["description"], now_iso()),
        )
        row = conn.execute(
            "SELECT id FROM companies WHERE owner_id = ?", (employer_id,)
        ).fetchone()
        company_id = row["id"]
        audit.log_event(conn, employer_id, "company.update", "company", company_id)
    return company_id
