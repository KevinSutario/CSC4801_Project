# 12 · Deploy and run

The audit builds `main` from the `Dockerfile` (see the issue template). That build must work from a
fresh clone with no extra steps.

## Runtime

- `wsgi.py` creates the app and serves it with waitress on `0.0.0.0:$PORT` (default 8080).
- On start: create `instance/`, run `init_db()` if the database file does not exist, then seed demo
  data if the database is new (so auditors can sign in at once). Resumes are raw text, so there is no
  uploads folder to seed.
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

`python scripts/seed.py --reset` deletes the database, recreates the schema, and adds the mandatory
minimum below (quoting FP-DOC-3; T19 may add more jobs after these):

| Account | Password | Role | Notes |
|---|---|---|---|
| `meilin@demo.keystone` | one demo password (INSTALL.md) | candidate | skills Python, SQL; a raw-text resume |
| `arjun@demo.keystone` | same demo password | candidate | skills Python |
| `sofia@demo.keystone` | same demo password | candidate | skills Rust |
| `daniel@demo.keystone` | same demo password | employer | Harbourline Logistics |
| `priya@demo.keystone` | same demo password | employer | Tidewater Freight |

Jobs: Harbourline "Data Analyst" requires Python, SQL; Tidewater "Logistics Coordinator" requires
SQL, Excel (so "two jobs with required skills" holds on any reading); Tidewater "Graduate Trainee"
requires no skills. These give the four FP-MATCH-1 examples: Mei Lin 100 and Arjun 50 and Sofia 0 on
Data Analyst, everyone 100 on Graduate Trainee.

Applications: Mei Lin and Arjun on Data Analyst, both `interviewing` (the two candidates eligible to
race for one slot); Sofia on Data Analyst `pending`; Mei Lin on Graduate Trainee `accepted`; Sofia on
Graduate Trainee `rejected`. Slots: Daniel has one future 30-minute unbooked slot created in
`Asia/Hong_Kong`; Priya has one in `Europe/London`.

Demo passwords are documented in INSTALL.md and README "Demo Accounts" because the template asks for
them. They are demo-only and must not be reused anywhere. All people and companies are fictional.

## Release checklist (phase 4 gate)

1. `python scripts/check.py --release` passes (no skipped tests).
2. Fresh clone in a new folder, then `docker build` and `docker run`, then sign in as each demo account.
3. README, SPEC.md and INSTALL.md have no empty sections.
4. `git status` clean on `main`; tag `release-1`.
