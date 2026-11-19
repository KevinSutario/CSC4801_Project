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
  timeutil.py            pure: local_to_utc(), utc_to_local(), format_local(), validate_tz()
  skills.py              pure: normalise_skill(), parse_skill_list(), get_or_create_skill_ids()
  auth/        routes.py service.py
  candidates/  profile_service.py routes_profile.py resume_service.py routes_resume.py
  employers/   routes.py service.py        company profile
  jobs/        routes.py service.py        job CRUD, job skills
  matching/    engine.py                   pure scoring + ranking (no db)
               service.py routes.py        loads data, calls engine
  applications/ statuses.py service.py routes_candidate.py review_service.py routes_employer.py
  scheduling/  slots.py booking.py routes_employer.py routes_candidate.py
  activity/    routes.py                   own-events activity log
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
profile form -> candidates.service.save_profile -> upsert candidate_profiles + users.display_name
skills field "Python, SQL"  -> normalise_skill() each -> replace candidate_skills rows
resume form (textarea) -> candidates.service.save_resume -> upsert resumes (owner_id, body)
resume view GET /candidates/<id>/resume -> get_resume_for_viewer(viewer_id, candidate_id)
  -> owner sees their text (escaped); anyone else 403
```
The resume is raw text, one per candidate, owner-only. No file is ever written to disk.

### Jobs and company (FP-EMP-1, FP-EMP-2)
```
company form -> employers.service.save_company -> upsert companies (one per employer)
job form -> jobs.service.create_job / update_job -> validate -> INSERT jobs + job_skills
delete POST -> jobs.service.delete_job -> ownership -> 409 if any application (D12)
```

### Recommendations (FP-CAN-2, FP-MATCH-1)
```
GET /candidate/recommendations
  -> matching.service.recommend_for(conn, candidate_id)
       -> load candidate skills (normalised) and ALL jobs (no closed state, D18) with their skills
       -> matching.engine.rank(candidate_skills, jobs)   pure function, rules from BRIEF
       -> return every job with its score and its fields unchanged
  -> template lists them in ranked order
```

### Applying and applicants (FP-CAN-3, FP-EMP-3)
```
confirm page (shows exactly what will be sent) -> POST apply
  -> applications.service.apply -> apply-once check (any existing = Conflict) -> INSERT applications
employer applicants page -> applications.review_service.list_applicants(conn, employer_id, job_id)
  -> ownership -> ordered per brief -> fields per brief
status change POST -> applications.review_service.set_status -> any status but the current one -> audit
```

### Slots and booking (FP-SCHED)
```
employer slot form (local date, time, timezone) -> timeutil.local_to_utc inside scheduling.slots.create_slot
  (employer-owned slot, exactly 30 minutes, in the future, D13)
candidate booking POST -> scheduling.booking.book_slot
  -> BEGIN IMMEDIATE (one writer at a time)
  -> five conditions (own interviewing application, no existing booking, slot is this employer's,
     future, unbooked) -> INSERT bookings (UNIQUE slot_id, UNIQUE application_id)
  -> COMMIT, or on IntegrityError: Conflict("Slot already booked"), 409 (D14)
display -> timeutil.utc_to_local(utc, viewer_tz)
```

## Configuration

| Env var | Default | Meaning |
|---|---|---|
| `SECRET_KEY` | random per start (sessions end on restart) | session signing key |
| `DATABASE` | `instance/keystone.sqlite3` | SQLite file path |
| `UPLOAD_DIR` | `instance/uploads` | unused since CC01 (resumes are raw text); kept so the Dockerfile and `.env.example` do not change |
| `MAX_UPLOAD_MB` | value from brief, else 2 | upload size cap |
| `PORT` | 8080 | waitress port in Docker |

Tests use `create_app({"TESTING": True, "DATABASE": tmp_path, "UPLOAD_DIR": tmp_path, "SECRET_KEY": "test"})`.
