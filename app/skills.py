"""Skill normalisation. Provisional version written by T01; T11 owns it afterwards."""

from __future__ import annotations

import sqlite3


def normalise_skill(raw: str) -> str:
    """FP-MATCH-1: strip surrounding whitespace and lower-case. Nothing else."""
    return raw.strip().lower()


def parse_skill_list(text: str) -> list[str]:
    """Split on commas, normalise, drop empties, dedupe keeping order."""
    names: list[str] = []
    for part in text.split(","):
        name = normalise_skill(part)
        if name and name not in names:
            names.append(name)
    return names


def get_or_create_skill_ids(conn: sqlite3.Connection, names: list[str]) -> list[int]:
    """Return skill ids for already-normalised names, inserting missing rows.

    Call inside the caller's transaction (the connection is in autocommit mode).
    """
    ids: list[int] = []
    for name in names:
        row = conn.execute("SELECT id FROM skills WHERE name = ?", (name,)).fetchone()
        if row is None:
            cursor = conn.execute("INSERT INTO skills (name) VALUES (?)", (name,))
            ids.append(cursor.lastrowid)
        else:
            ids.append(row["id"])
    return ids
