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
