"""Demo data seeding. Owned by T19.

Creates the mandatory demo minimum from docs/plan/12-DEPLOY.md (FP-DOC-3)
through the real services, so demo data always obeys the rules. Exposed as
``seed(app)`` for wsgi.py (seed a brand-new database on first start) and as
``python scripts/seed.py [--reset]`` for a one-command demo reset.

``--reset`` deletes the database file (path from the app config, never
hard-coded) and recreates the schema. Without it, seeding refuses when the
database already has users.

All people and companies are fictional. The demo password is for demo accounts
only, documented in INSTALL.md, and must not be reused anywhere.
"""

from __future__ import annotations

import argparse
import os
import sqlite3
import sys
from datetime import datetime, timedelta, timezone

# Make "python scripts/seed.py" work from the project root: the interpreter
# puts scripts/ (not the project root) on sys.path.
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

# Demo-only password for all five demo accounts (documented in INSTALL.md).
DEMO_PASSWORD = "DemoPassw0rd!"


def seed(app) -> None:
    """Create the demo data on an empty database through the real services.

    Refuses (RuntimeError) when the database already has users; callers that
    own a reset (the --reset CLI below) delete and recreate the database first.
    """
    # Push our own app context: some seeded services need current_app (T25's
    # save_resume_file reads UPLOAD_DIR and MAX_UPLOAD_MB from it), and callers
    # such as wsgi.py's first-start seeding run outside any app context.
    with app.app_context():
        conn = sqlite3.connect(
            app.config["DATABASE"], isolation_level=None, detect_types=0
        )
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        try:
            _seed_with_connection(conn)
        finally:
            conn.close()


def _seed_with_connection(conn: sqlite3.Connection) -> None:
    # Imports stay inside the function: this module is imported by tests and
    # potentially by the app itself, so it must not import app.* at module
    # import time.
    from werkzeug.datastructures import FileStorage

    from app.applications.review_service import set_status
    from app.applications.service import apply
    from app.auth.service import register
    from app.candidates.profile_service import save_profile
    from app.candidates.resume_service import save_resume, save_resume_file
    from app.employers.service import save_company
    from app.jobs.service import create_job
    from app.scheduling.slots import create_slot

    has_users = conn.execute("SELECT 1 FROM users LIMIT 1").fetchone()
    if has_users is not None:
        raise RuntimeError(
            "The database already has users; pass --reset to delete it first."
        )

    # --- Candidates -------------------------------------------------------
    meilin = register(conn, "meilin@demo.keystone", DEMO_PASSWORD, "candidate",
                      "Mei Lin Tan")
    arjun = register(conn, "arjun@demo.keystone", DEMO_PASSWORD, "candidate",
                     "Arjun Patel")
    sofia = register(conn, "sofia@demo.keystone", DEMO_PASSWORD, "candidate",
                     "Sofia Novak")
    save_profile(conn, meilin, "Mei Lin Tan",
                 "Data analyst with Python and SQL", "Hong Kong",
                 "Asia/Hong_Kong",
                 "Fictional demo candidate who enjoys turning data into decisions.",
                 "Python, SQL")
    save_profile(conn, arjun, "Arjun Patel", "Python developer", "Singapore",
                 "Asia/Singapore", "Fictional demo candidate who builds tools.",
                 "Python")
    save_profile(conn, sofia, "Sofia Novak", "Systems programmer", "Berlin",
                 "Europe/Berlin", "Fictional demo candidate who loves Rust.", "Rust")
    save_resume(conn, meilin, "Demo resume. Fictional person.")

    # Mei Lin also gets a demo CV file through the real T23 upload service
    # (validation, UPLOAD_DIR storage, audit event), so the CV upload feature
    # and the employer view are demonstrable on fresh demo data. The other
    # candidates stay file-less on purpose (the "no CV" path).
    fixture = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "fixtures", "demo_cv.pdf"
    )
    with open(fixture, "rb") as f:
        save_resume_file(conn, meilin, FileStorage(
            stream=f, filename="demo_cv.pdf", content_type="application/pdf"
        ))

    # --- Employers, companies and jobs ------------------------------------
    daniel = register(conn, "daniel@demo.keystone", DEMO_PASSWORD, "employer",
                      "Daniel Wong")
    priya = register(conn, "priya@demo.keystone", DEMO_PASSWORD, "employer",
                     "Priya Sharma")
    save_company(conn, daniel, "Harbourline Logistics", "Logistics",
                 "Hong Kong", "https://harbourline.example.com",
                 "Fictional demo company moving freight across the Pearl River Delta.")
    save_company(conn, priya, "Tidewater Freight", "Shipping",
                 "London", "https://tidewater.example.com",
                 "Fictional demo company shipping cargo along the Thames.")

    analyst = create_job(conn, daniel, "Data Analyst",
                         "Fictional demo role: analyse shipment data and build reports.",
                         "Hong Kong", "full-time", "25000", "35000", "Python, SQL")
    create_job(conn, priya, "Logistics Coordinator",
               "Fictional demo role: coordinate container schedules and rates.",
               "London", "full-time", "28000", "36000", "SQL, Excel")
    trainee = create_job(conn, priya, "Graduate Trainee",
                         "Fictional demo role: rotate through three teams in a year.",
                         "London", "internship", "", "", "")

    # --- Applications ------------------------------------------------------
    # apply() creates them pending; the employers then set the demo statuses.
    ml_analyst = apply(conn, meilin, analyst, "I would love to analyse your data.")
    aj_analyst = apply(conn, arjun, analyst, "Python is my strongest tool.")
    apply(conn, sofia, analyst, "Curious about a switch to data.")
    ml_trainee = apply(conn, meilin, trainee, "Happy to learn a new domain.")
    sf_trainee = apply(conn, sofia, trainee, "Interested in logistics.")
    set_status(conn, daniel, ml_analyst, "interviewing")
    set_status(conn, daniel, aj_analyst, "interviewing")
    set_status(conn, priya, ml_trainee, "accepted")
    set_status(conn, priya, sf_trainee, "rejected")
    # Sofia on Data Analyst stays pending on purpose: the fourth status.

    # --- Interview slots ---------------------------------------------------
    # One future, unbooked 30-minute slot each, in the employer's own zone.
    # About a month out, so the demo stays valid indefinitely; 10:00 local is
    # never inside a DST gap.
    date_str = (datetime.now(timezone.utc) + timedelta(days=30)).strftime("%Y-%m-%d")
    create_slot(conn, daniel, date_str, "10:00", "10:30", "Asia/Hong_Kong")
    create_slot(conn, priya, date_str, "10:00", "10:30", "Europe/London")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Reset the app to the known demo state (fictional people only)."
    )
    parser.add_argument(
        "--reset", action="store_true",
        help="delete the database file first (the configured DATABASE, never a "
             "hard-coded path), then recreate the schema and add the demo data",
    )
    args = parser.parse_args(argv)

    # Import the app only after argument parsing: --help works without it.
    from app import create_app

    app = create_app()
    db_path = os.path.abspath(app.config["DATABASE"])

    if args.reset:
        print(f"Deleting {db_path}")
        if os.path.exists(db_path):
            os.remove(db_path)
        # create_app() ran init_db() only when the file was missing, so the
        # schema must be (re)created explicitly after the delete.
        with app.app_context():
            from app.db import init_db

            init_db()
        print("Recreated the schema.")

    with app.app_context():
        try:
            seed(app)
        except RuntimeError as exc:
            print(f"Refused: {exc}", file=sys.stderr)
            return 1
    print(f"Demo data ready. Sign in with any demo account and the password"
          f" {DEMO_PASSWORD!r} (demo-only).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
