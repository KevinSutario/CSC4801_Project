# 12 · Deploy and run

The audit builds `main` from the `Dockerfile` (see the issue template). That build must work from a
fresh clone with no extra steps.

## Runtime

- `wsgi.py` creates the app and serves it with waitress on `0.0.0.0:$PORT` (default 8080).
- On start: create `instance/` and `UPLOAD_DIR`, run `init_db()` if the database file does not
  exist, then seed demo data if the database is new (so auditors can sign in at once).
- `debug` is never on in Docker.

## Dockerfile (T20 fills in the template's TODOs)

- Keep the base image and the unprivileged `student` user from the template.
- Data folder: `/app/data` owned by `student`; `DATABASE=/app/data/keystone.sqlite3`,
  `UPLOAD_DIR=/app/data/uploads`.
- `EXPOSE 8080`
- `CMD ["python", "wsgi.py"]`
- `tzdata` is pinned in `requirements.lock`, so time zones work in the slim image and on Windows.

Commands (also in INSTALL.md):
```
docker build -t keystone .
docker run --rm -p 8080:8080 keystone
# then open http://localhost:8080
```

## Demo data (T19)

`python scripts/seed.py --reset` deletes the database and uploads, recreates the schema, and adds:

| Account | Password | Role | Notes |
|---|---|---|---|
| `meilin@demo.keystone` | from INSTALL.md | candidate | full profile, Python, SQL, dbt, Tableau, one resume |
| `arjun@demo.keystone` | from INSTALL.md | candidate | few skills, no resume |
| `daniel@demo.keystone` | from INSTALL.md | employer | Harbourline Logistics, 3 jobs, slots |
| `priya@demo.keystone` | from INSTALL.md | employer | Tidewater Freight, 2 jobs |

Demo passwords are documented in INSTALL.md and README "Demo Accounts" because the template asks for
them. They are demo-only and must not be reused anywhere. All people and companies are fictional.

## Release checklist (phase 4 gate)

1. `python scripts/check.py --release` passes (no skipped tests).
2. Fresh clone in a new folder, then `docker build` and `docker run`, then sign in as each demo account.
3. README, SPEC.md and INSTALL.md have no empty sections.
4. `git status` clean on `main`; tag `release-1`.
