# Installation Guide

## Prerequisites and Versions

- Python 3.12. The container is based on `python:3.12.11-slim-bookworm`.
- Docker Engine with the Docker CLI for container use.
- `pip` for Python package installation.

The runtime versions are pinned in [`requirements.lock`](requirements.lock), including Flask 3.1.2, pytest 8.4.2, waitress 3.0.2, Werkzeug 3.1.8, and tzdata 2026.5. The Dockerfile installs the locked dependency list through `requirements.txt`.

## Dependency Installation

From the repository root, create and activate a virtual environment, then install runtime dependencies:

```bash
python -m venv .venv
```

On macOS or Linux:

```bash
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

To run the lint and unit-test gate, install the development dependency set as well:

```bash
python -m pip install -r requirements-dev.txt
```

## Environment Variables

The app reads environment variables directly; it does not automatically load `.env.example` or a `.env` file. All settings are optional.

| Variable | Default | Purpose |
|---|---|---|
| `SECRET_KEY` | A randomly generated key per process start | Flask session signing. Set a stable secret for sessions that should survive a restart. |
| `DATABASE` | `<instance folder>/keystone.sqlite3` | SQLite database file path. |
| `UPLOAD_DIR` | `<instance folder>/uploads` | Compatibility configuration; résumé content is plain text and this directory is not used for résumé uploads. |
| `MAX_UPLOAD_MB` | `2` | Flask request body size limit in MiB. |
| `SESSION_COOKIE_SECURE` | Disabled unless set to `1` | Enable the Secure cookie attribute when served over HTTPS. |
| `PORT` | `8080` for `wsgi.py` | Waitress listening port in the container/WSGI entry point. Flask’s local development server uses its own default unless `--port` is passed. |

For example, in PowerShell set a local database path with `$env:DATABASE = "C:\keystone\demo.sqlite3"`. In Docker, `DATABASE` defaults to `/app/data/keystone.sqlite3` and `UPLOAD_DIR` to `/app/data/uploads`.

## Database Setup and Migrations

There is no separate migration system. The schema is created by `flask --app app init-db`; the application factory also initializes the schema when the configured database file is missing. Run the explicit setup command from the repository root:

```bash
python -m flask --app app init-db
```

The command is safe to run again on an already initialized database. The default local database is stored under Flask’s `instance/` directory. To use a different location, set `DATABASE` before running Flask or the seed script.

## Demo Data and Reset Command

Seed or reset the configured local database with:

```bash
python scripts/seed.py --reset
```

This deletes the configured SQLite database file, recreates its schema, and inserts fictional demo data: five accounts, three jobs, applications in all four statuses, match-score examples, and future unbooked slots. All demo accounts use `DemoPassw0rd!`; the credentials are local/demo-only and must not be reused for real accounts. See [README.md](README.md#demo-accounts) for account roles and profiles.

Running `python scripts/seed.py` without `--reset` adds demo data only to an empty database and refuses to duplicate existing data.

## Docker Build

Build the image from the repository root:

```bash
docker build -t keystone .
```

The image uses Python 3.12.11 slim Bookworm, installs the pinned runtime dependencies, and runs as an unprivileged `student` user. It exposes port 8080 and stores its database under `/app/data`.

## Docker Startup

Run the container and open the application at <http://localhost:8080/>:

```bash
docker run --rm -p 8080:8080 keystone
```

On first start, `wsgi.py` creates the database and schema, seeds demo accounts if the database has no users, and starts Waitress on `0.0.0.0:8080`. The command above removes the container and its database when it exits. To retain container data between runs, use a named volume and container:

```bash
docker run --name keystone -p 8080:8080 -v keystone-data:/app/data keystone
```

With that named volume, reset and reseed the container’s database with `docker exec keystone python scripts/seed.py --reset`. Stop the persistent container with `docker stop keystone`; remove it with `docker rm keystone` when no longer needed.

## Local Development

After installing the dependencies, initialize the local database, seed demo records, and start Flask’s development server:

```bash
python -m flask --app app init-db
python scripts/seed.py --reset
python -m flask --app app run --debug
```

Open <http://127.0.0.1:5000/>. The debug server is for local development only; the Docker image starts Waitress with debug disabled.

## Running Unit Tests

Install development dependencies with `python -m pip install -r requirements-dev.txt`, then run the project gate:

```bash
python scripts/check.py
```

This runs Ruff, the complete `tests/unit` suite, and the contract check. To run just the unit tests, use `python -m pytest tests/unit -q`. To list discovered tests, use `python -m pytest --collect-only -q`.

## Troubleshooting

- **Port 8080 or 5000 is already in use:** stop the process using that port, or map the Docker app to another host port, such as `docker run --rm -p 8081:8080 keystone`, then open <http://localhost:8081/>. For Flask, pass `--port 5001` to the `run` command.
- **Time-zone database errors, especially on Windows:** ensure dependencies were installed from `requirements.txt`; it pins `tzdata`, which supplies the IANA time-zone database on platforms without a system copy.
- **A Flask session becomes invalid after restarting:** set `SECRET_KEY` to a stable local secret before starting the app. When omitted, the application generates a new secret at startup.
- **The seed command refuses to run:** it found users in the configured database. Use `python scripts/seed.py --reset` only when you intend to delete and recreate that database.
- **Docker changes are missing from the running app:** rebuild the image with `docker build -t keystone .` and recreate the container.
