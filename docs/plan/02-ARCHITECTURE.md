# 02 · Architecture

## Shape of the app

A single Flask app, server-rendered with Jinja templates, backed by one SQLite file.
Every feature is a **blueprint package** with two layers:

- `routes.py`: thin. Reads the form, checks login and role, calls a service, renders a template.
- `service.py`: all logic. Plain Python functions that take a `sqlite3.Connection` and plain
  values, and return plain dicts or raise a defined error. No Flask imports. **Unit tests call
  services directly.**

Pure logic with no database (matching, time conversion) lives in its own module with no I/O at all.

## Folder layout (created in Phase 1, then frozen)

```
app/
  __init__.py            create_app(config=None): config, db, security, blueprints, error pages
  config.py              Config class: reads env vars (SECRET_KEY, DATABASE, MAX_UPLOAD_MB)
  db.py                  get_db(), close_db(), init_db(), transaction() context manager
  schema.sql             all tables (03-DATA-MODEL.md), created once
  errors.py              ServiceError classes + HTTP error handlers
  security.py            csrf, security headers, login_required, role_required, rate limit
  audit.py               log_event(conn, actor_id, action, object_type, object_id, detail)
  timeutil.py            pure: to_utc(), from_utc(), validate_tz()
  auth/        routes.py service.py
  candidates/  routes.py service.py        profile, skills, resume
  employers/   routes.py service.py        company profile
  jobs/        routes.py service.py        job CRUD, job skills
  matching/    engine.py                   pure scoring + ranking (no db)
               service.py                  loads data, calls engine
  applications/ routes.py service.py       apply, list, status changes
  scheduling/  routes.py service.py        slots, bookings
  templates/
    base.html                layout, nav per role, flash messages, csrf meta
    components/              macros: button, card, badge, field, table, empty_state, confirm
    auth/ candidates/ employers/ jobs/ applications/ scheduling/ errors/
  static/
    css/tokens.css           design tokens (06-DESIGN-SYSTEM.md)
    css/app.css              components built on tokens
scripts/
  check.py                   the gate
  check_scope.py             changed files inside the task's Owns list?
  seed.py                    demo data and --reset
tests/
  conftest.py                app, client, db, login helpers, factories
  unit/test_*.py             one file per area
wsgi.py                      waitress entry point for Docker
```

## Why this shape suits a flash model

- Every task owns one package folder plus its own templates folder plus its own test file. Two
  agents never need the same file.
- Every shared file (`__init__.py`, `schema.sql`, `base.html`, `conftest.py`) is written in Phase 1
  and frozen. All blueprints are registered up front with stub routes, so later tasks only fill in
  their own package.
- Services are plain functions with fixed signatures (`07-CONTRACTS.md`), so an agent can test its
  work without the browser.

## Request flow

```
Browser form POST
  -> security.before_request: load user from session, check CSRF token, rate-limit login
  -> blueprint route: @login_required, @role_required("employer")
       -> read and strip form fields
       -> service.function(conn, actor_id, **fields)
            -> validate (raise ValidationError with field messages)
            -> check ownership (raise NotFound / Forbidden)
            -> SQL with ? placeholders only, inside db.transaction()
            -> audit.log_event(...) for consequential actions
            -> return dict
       -> on ValidationError: re-render the form with messages, HTTP 400
       -> on success: flash message, redirect (POST-redirect-GET)
  -> security.after_request: add security headers
```

## Data flow per feature

### Sign up and sign in (FP-AUTH)
```
form(email, password, role) -> auth.service.register -> validate -> hash password
  -> INSERT users -> audit "user.register"
login form -> rate limit check -> auth.service.authenticate -> verify hash
  -> session.clear(); session["user_id"], session["role"]; rotate CSRF token -> redirect home
logout POST -> session.clear() -> redirect to sign in
```

### Candidate profile and resume (FP-CAN-1)
```
profile form -> candidates.service.save_profile -> upsert candidate_profiles
skills field "Python, SQL"  -> normalise_skill() each -> replace candidate_skills rows
resume upload -> size and type check -> random file name -> save under instance/uploads/
  -> INSERT resumes (owner_id, stored_name, original_name, size, mime)
resume download GET /resumes/<id> -> can_view_resume(viewer, resume) -> send_file as attachment
```
Resume files are **never** under `static/`. They are only served through the checked route.

### Jobs and company (FP-EMP-1, FP-EMP-2)
```
company form -> employers.service.save_company -> upsert companies (one per employer)
job form -> jobs.service.create_job / update_job -> validate -> INSERT jobs + job_skills
delete POST -> jobs.service.delete_job -> ownership -> rules from brief for linked rows
```

### Recommendations (FP-CAN-2, FP-MATCH-1)
```
GET /candidate/recommendations
  -> matching.service.recommend_for(conn, candidate_id)
       -> load candidate skills (normalised) and ALL open jobs with their skills
       -> matching.engine.rank(candidate_skills, jobs)   pure function, rules from BRIEF
       -> return every job with its score and its fields unchanged
  -> template lists them in ranked order
```

### Applying and applicants (FP-CAN-3, FP-EMP-3)
```
confirm page (shows exactly what will be sent) -> POST apply
  -> applications.service.apply -> duplicate pending check -> INSERT applications
employer applicants page -> applications.service.list_applicants(conn, employer_id, job_id)
  -> ownership -> ordered per brief -> fields per brief
status change POST -> applications.service.set_status -> allowed transitions -> audit
```

### Slots and booking (FP-SCHED)
```
employer slot form (local date, time, timezone) -> timeutil.to_utc -> scheduling.service.create_slot
candidate booking POST -> scheduling.service.book_slot
  -> BEGIN IMMEDIATE (one writer at a time)
  -> eligibility check (brief) -> slot still free? -> INSERT bookings (UNIQUE slot_id)
  -> COMMIT, or on IntegrityError: conflict result defined by the brief
display -> timeutil.from_utc(utc, viewer_tz)
```

## Configuration

| Env var | Default | Meaning |
|---|---|---|
| `SECRET_KEY` | random per start (sessions end on restart) | session signing key |
| `DATABASE` | `instance/keystone.sqlite3` | SQLite file path |
| `UPLOAD_DIR` | `instance/uploads` | resume storage, outside static |
| `MAX_UPLOAD_MB` | value from brief, else 2 | upload size cap |
| `PORT` | 8080 | waitress port in Docker |

Tests use `create_app({"TESTING": True, "DATABASE": tmp_path, "UPLOAD_DIR": tmp_path, "SECRET_KEY": "test"})`.
