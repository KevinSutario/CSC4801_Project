# 03 · Data model

This is the full schema. Task T01 writes it to `app/schema.sql` exactly. After Phase 1 it is
**frozen**: a change needs a contract change request (see `09-AGENT-WORKFLOW.md`).

Columns marked **(brief)** have limits or allowed values that come from `docs/BRIEF.md`. T01 uses
the safe default shown; the task that owns the feature tightens validation in its service, not in
the schema.

## Conventions

- `id INTEGER PRIMARY KEY` on every table.
- Times: `TEXT` holding UTC ISO-8601 with a `Z`, for example `2026-11-30T02:00:00Z`.
- Booleans: `INTEGER` 0 or 1 with a CHECK.
- Every foreign key states `ON DELETE` explicitly. `PRAGMA foreign_keys = ON` is set on every
  connection in `db.get_db()`.
- Skills are stored **normalised** (the normalise rule is FP-MATCH-1, from the brief).

## Tables

```sql
PRAGMA foreign_keys = ON;

CREATE TABLE users (
  id            INTEGER PRIMARY KEY,
  email         TEXT NOT NULL UNIQUE COLLATE NOCASE,
  password_hash TEXT NOT NULL,
  role          TEXT NOT NULL CHECK (role IN ('candidate', 'employer')),
  display_name  TEXT NOT NULL,
  created_at    TEXT NOT NULL
);

CREATE TABLE candidate_profiles (
  user_id     INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
  headline    TEXT NOT NULL DEFAULT '',
  location    TEXT NOT NULL DEFAULT '',
  timezone    TEXT NOT NULL DEFAULT 'UTC',
  summary     TEXT NOT NULL DEFAULT '',
  updated_at  TEXT NOT NULL
);

CREATE TABLE skills (
  id    INTEGER PRIMARY KEY,
  name  TEXT NOT NULL UNIQUE          -- normalised form
);

CREATE TABLE candidate_skills (
  candidate_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  skill_id     INTEGER NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
  PRIMARY KEY (candidate_id, skill_id)
);

CREATE TABLE resumes (
  owner_id    INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
  body        TEXT NOT NULL,
  updated_at  TEXT NOT NULL
);

CREATE TABLE resume_files (
  owner_id      INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
  stored_name   TEXT NOT NULL,
  original_name TEXT NOT NULL,
  content_type  TEXT NOT NULL,
  size_bytes    INTEGER NOT NULL,
  updated_at    TEXT NOT NULL
);

CREATE TABLE companies (
  id           INTEGER PRIMARY KEY,
  owner_id     INTEGER NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
  name         TEXT NOT NULL,
  industry     TEXT NOT NULL DEFAULT '',
  location     TEXT NOT NULL DEFAULT '',
  website      TEXT NOT NULL DEFAULT '',
  description  TEXT NOT NULL DEFAULT '',
  updated_at   TEXT NOT NULL
);

CREATE TABLE jobs (
  id           INTEGER PRIMARY KEY,
  company_id   INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
  title        TEXT NOT NULL,                       -- (brief) length limits
  description  TEXT NOT NULL,
  location     TEXT NOT NULL DEFAULT '',
  employment_type TEXT NOT NULL DEFAULT '',          -- (brief) allowed values
  salary_min   INTEGER,                              -- (brief) required or optional
  salary_max   INTEGER,
  created_at   TEXT NOT NULL,
  updated_at   TEXT NOT NULL,
  CHECK (salary_min IS NULL OR salary_max IS NULL OR salary_min <= salary_max)
);

CREATE TABLE job_skills (
  job_id    INTEGER NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
  skill_id  INTEGER NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
  PRIMARY KEY (job_id, skill_id)
);

CREATE TABLE applications (
  id            INTEGER PRIMARY KEY,
  job_id        INTEGER NOT NULL REFERENCES jobs(id) ON DELETE RESTRICT,   -- (brief) delete refused in service first (409); constraint is the backstop
  candidate_id  INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  status        TEXT NOT NULL DEFAULT 'pending'
                CHECK (status IN ('pending', 'interviewing', 'rejected', 'accepted')),
  cover_note    TEXT NOT NULL DEFAULT '',
  created_at    TEXT NOT NULL,
  updated_at    TEXT NOT NULL
);
-- one application per candidate per job, ever (FP-CAN-3)
CREATE UNIQUE INDEX uq_application ON applications (job_id, candidate_id);

CREATE TABLE interview_slots (
  id           INTEGER PRIMARY KEY,
  employer_id  INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  starts_at    TEXT NOT NULL,      -- UTC
  ends_at      TEXT NOT NULL,      -- UTC
  created_tz   TEXT NOT NULL,      -- the IANA zone the employer entered it in
  created_at   TEXT NOT NULL,
  CHECK (ends_at > starts_at)
);

CREATE TABLE bookings (
  id              INTEGER PRIMARY KEY,
  slot_id         INTEGER NOT NULL UNIQUE REFERENCES interview_slots(id) ON DELETE CASCADE,
  application_id  INTEGER NOT NULL REFERENCES applications(id) ON DELETE CASCADE,
  booked_at       TEXT NOT NULL
);
-- one booking per application (FP-SCHED-2)
CREATE UNIQUE INDEX uq_booking_application ON bookings (application_id);

CREATE TABLE audit_log (
  id           INTEGER PRIMARY KEY,
  actor_id     INTEGER REFERENCES users(id) ON DELETE SET NULL,
  action       TEXT NOT NULL,      -- for example 'application.submit'
  object_type  TEXT NOT NULL,
  object_id    INTEGER,
  detail       TEXT NOT NULL DEFAULT '',   -- short, never contains passwords or file contents
  created_at   TEXT NOT NULL
);

CREATE INDEX ix_jobs_company ON jobs (company_id);
CREATE INDEX ix_applications_job ON applications (job_id);
CREATE INDEX ix_applications_candidate ON applications (candidate_id);
CREATE INDEX ix_slots_employer ON interview_slots (employer_id, starts_at);
CREATE INDEX ix_audit_actor ON audit_log (actor_id, created_at);
```

## Relationships

```
users (candidate) 1 ─ 1 candidate_profiles
users (candidate) 1 ─ * candidate_skills * ─ 1 skills
users (candidate) 1 ─ 0..1 resumes
users (candidate) 1 ─ 0..1 resume_files
users (employer)  1 ─ 1 companies 1 ─ * jobs 1 ─ * job_skills * ─ 1 skills
jobs 1 ─ * applications * ─ 1 users (candidate)
users (employer) 1 ─ * interview_slots 1 ─ 0..1 bookings 1 ─ 1 applications
users 1 ─ * audit_log
```

## Why these constraints

- `uq_application` makes the apply-once rule (FP-CAN-3) hold even if two requests race, for any
  status. The service still checks first, to give a friendly message.
- `bookings.slot_id UNIQUE` makes double booking impossible at the database level (FP-SCHED-3).
  The service uses `BEGIN IMMEDIATE` and turns the `IntegrityError` into the brief's conflict result.
- `uq_booking_application` holds the one-booking-per-application rule (FP-SCHED-2) at the database
  level.
- `applications.job_id ON DELETE RESTRICT` is the backstop for the brief's 409-on-delete rule
  (FP-EMP-2): the service refuses first, the constraint stops a cascade if it somehow slips through.

## Audit actions (fixed list)

`user.register`, `user.login`, `user.login_failed`, `profile.update`, `resume.update`,
`company.update`, `job.create`, `job.update`, `job.delete`, `application.submit`,
`application.status`, `slot.create`, `slot.delete`, `booking.create`, `booking.conflict`.
