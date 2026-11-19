"""Shared pytest fixtures. Owned by T01; T04 adds the factory and login fixtures."""

import pytest

from app import create_app
from app.db import get_db


@pytest.fixture()
def app(tmp_path):
    """A fresh app with its own database and upload dir under tmp_path."""
    return create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test",
            "DATABASE": str(tmp_path / "test.sqlite3"),
            "UPLOAD_DIR": str(tmp_path / "uploads"),
        }
    )


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def conn(app):
    with app.app_context():
        yield get_db()
