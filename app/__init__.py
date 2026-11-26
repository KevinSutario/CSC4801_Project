"""Application factory. Owned by T01 (frozen afterwards)."""

import os

import click
from flask import Flask

from . import errors, security
from .config import Config
from .db import close_db, get_db, init_db, missing_tables, upgrade_interview_slot_notes, user_tables


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)
    if test_config is not None:
        app.config.from_mapping(test_config)

    # Fill in the path defaults that depend on the instance folder.
    if not app.config.get("DATABASE"):
        app.config["DATABASE"] = os.path.join(app.instance_path, "keystone.sqlite3")
    if not app.config.get("UPLOAD_DIR"):
        app.config["UPLOAD_DIR"] = os.path.join(app.instance_path, "uploads")

    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config["UPLOAD_DIR"], exist_ok=True)

    app.teardown_appcontext(close_db)

    @app.cli.command("init-db")
    def init_db_command() -> None:
        """Create the database tables from schema.sql.

        - no user-created table at all (empty or brand-new database; sqlite_*
          internal tables are ignored) -> run schema.sql;
        - all required tables present -> already initialised, nothing to do;
        - any user-created table exists but required tables are missing ->
          partly-built or unknown database: report the missing tables and
          refuse, without touching the data (schema.sql cannot be applied on
          top of existing tables).
        """
        db = get_db()
        if user_tables(db):
            missing = missing_tables(db)
            if missing:
                raise click.ClickException(
                    "database is missing tables: " + ", ".join(missing)
                    + " (refusing to run schema.sql on a partly-built database;"
                    " inspect it manually)"
                )
            click.echo("Database already initialised.")
            return
        init_db()
        click.echo("Initialised the database.")

    errors.init_app(app)
    security.init_app(app)

    from . import applications, auth, candidates, core, employers, jobs, matching, scheduling

    app.register_blueprint(core.bp)
    app.register_blueprint(auth.bp, url_prefix="/auth")
    app.register_blueprint(candidates.bp)
    app.register_blueprint(employers.bp)
    app.register_blueprint(jobs.bp)
    app.register_blueprint(matching.bp)
    app.register_blueprint(applications.bp)
    app.register_blueprint(scheduling.bp)

    with app.app_context():
        if not os.path.exists(app.config["DATABASE"]):
            init_db()
        else:
            upgrade_interview_slot_notes()

    return app
