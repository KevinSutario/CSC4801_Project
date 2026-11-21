"""WSGI entry point. Owned by T20.

`create_app()` builds the app and runs init_db() when the database file is
missing. On first start we also seed the demo data (so an auditor who runs
`docker run` can sign in immediately); seeding is skipped once the database has
users. Served with waitress on 0.0.0.0:$PORT (default 8080); debug is never on.
"""

import os

from app import create_app

app = create_app()


def _seed_if_empty(flask_app) -> None:
    """Seed demo data when the database has no users yet.

    Reads through the app's own connection (get_db inside an app context) rather
    than a bare sqlite3 handle, matching the rest of the app. seed() is imported
    lazily so importing wsgi never hard-requires the seed module.
    """
    from app.db import get_db

    with flask_app.app_context():
        has_users = get_db().execute("SELECT 1 FROM users LIMIT 1").fetchone() is not None
    if not has_users:
        from scripts.seed import seed

        seed(flask_app)


_seed_if_empty(app)


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
