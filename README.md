# Keystone

## Project Overview

Keystone is a locally runnable recruiting platform for candidates and employers. Candidates manage a profile and private plain-text résumé, receive skill-based job recommendations, apply, and book interview slots. Employers manage a company profile and job postings, review applicants, and offer interview availability. The matching score supports decisions; people make them.

## Team Members

- Kevin Sutario

## Architecture Summary

Keystone is a single Flask 3.1 application with server-rendered Jinja templates and a SQLite relational database. Feature packages use thin Flask routes for HTTP, login and role checks, and rendering; service functions own validation, authorization, and database operations. Matching and time conversion are pure Python modules. Flask’s application factory registers the blueprints and shared security and error handling. Waitress serves the production container.

## Quick Start

For the complete installation, environment, database, Docker, and troubleshooting instructions, see [INSTALL.md](INSTALL.md).

```bash
python -m pip install -r requirements.txt
python -m flask --app app init-db
python scripts/seed.py --reset
python -m flask --app app run --debug
```

Open <http://127.0.0.1:5000/>. The seed command resets the configured local database and loads fictional demo data.

## Demo Accounts

These fictional accounts are for local demonstration only. They all use the demo-only password `DemoPassw0rd!`.

| Email | Role | Demo profile |
|---|---|---|
| `meilin@demo.keystone` | Candidate | Python and SQL; résumé included |
| `arjun@demo.keystone` | Candidate | Python |
| `sofia@demo.keystone` | Candidate | Rust |
| `daniel@demo.keystone` | Employer | Harbourline Logistics |
| `priya@demo.keystone` | Employer | Tidewater Freight |

Never reuse the demo password for a real account.

## Running Unit Tests

Install development tools with `python -m pip install -r requirements-dev.txt`, then run the complete suite and project checks:

```bash
python scripts/check.py
```

To run tests directly, use `python -m pytest tests/unit -q`. To verify test names for the requirement mapping, use `python -m pytest --collect-only -q`.

## Requirement–Test Mapping

The test names below were checked against `python -m pytest --collect-only -q`. The brief’s functional requirements map to named unit tests of the application behavior; supporting requirements cite the relevant tests and/or concrete verification evidence.

| Requirement ID | Behavior to verify | Implementation file(s) | Unit test(s) / verification evidence |
|---|---|---|---|
| FP-ARCH-1 | Browser UI, server-side behavior, persistent relational database, clean-checkout run | `app/__init__.py`, `app/db.py`, `app/templates/`, `Dockerfile`, `wsgi.py` | `tests/unit/test_db.py::test_all_tables_exist`; `tests/unit/test_wsgi.py::test_import_wsgi_creates_a_seeded_database`; clean Docker build and startup per [INSTALL.md](INSTALL.md) |
| FP-AUTH-1 | Registration, login, logout, unique accounts, session lifecycle | `app/auth/service.py`, `app/auth/routes.py`, `app/security.py` | `tests/unit/test_auth.py::test_fp_auth_1_registration_and_session_lifecycle`; `tests/unit/test_auth.py::test_fp_auth_1_invalid_registration`; `tests/unit/test_auth.py::test_fp_auth_1_invalid_registration_duplicate_email` |
| FP-AUTH-2 | Salted password hashing and verification; no credential rendering | `app/auth/service.py`, `app/auth/routes.py` | `tests/unit/test_auth.py::test_fp_auth_2_salted_hash_and_password_verification` |
| FP-AUTH-3 | Unauthenticated, forbidden, and missing-object responses; server-side role and ownership checks | `app/security.py`, `app/errors.py`, feature service and route modules | `tests/unit/test_auth.py::test_fp_auth_3_authorization_and_missing_object`; `tests/unit/test_authz_sweep.py::test_fp_sec_1_object_access_boundaries` (parameterized across representative routes) |
| FP-CAN-1 | Own profile, skills, private raw-text résumé, replace and view | `app/candidates/profile_service.py`, `app/candidates/resume_service.py`, `app/candidates/routes_profile.py`, `app/candidates/routes_resume.py` | `tests/unit/test_can_resume.py::test_fp_can_1_profile_and_private_resume_rules`; `tests/unit/test_can_profile.py::test_candidate_profile_routes_roles_and_post` |
| FP-CAN-2 | All current jobs ranked with score, title, company, skills, and description link | `app/matching/engine.py`, `app/matching/service.py`, `app/matching/routes.py`, `app/templates/matching/recommendations.html` | `tests/unit/test_can_recommend.py::test_fp_can_2_recommendations_preserve_fields_and_rank_all_jobs` |
| FP-CAN-3 | Apply once with Pending status; see own applications and booking; protect other applications | `app/applications/service.py`, `app/applications/routes_candidate.py`, `app/applications/statuses.py` | `tests/unit/test_can_apply.py::test_fp_can_3_pending_duplicate_and_application_owner` |
| FP-EMP-1 | View and edit the employer’s company profile | `app/employers/service.py`, `app/employers/routes.py` | `tests/unit/test_emp_company.py::test_fp_emp_1_company_profile` |
| FP-EMP-2 | Create, view, edit, and delete own jobs; dependent-job deletion returns conflict | `app/jobs/service.py`, `app/jobs/routes.py` | `tests/unit/test_emp_jobs.py::test_fp_emp_2_job_validation_and_deletion`; `tests/unit/test_emp_jobs.py::test_delete_job_with_application_is_409_and_changes_nothing` |
| FP-EMP-3 | View ranked applicants and set the allowed statuses for an owned job | `app/applications/review_service.py`, `app/applications/routes_employer.py`, `app/applications/statuses.py` | `tests/unit/test_emp_applicants.py::test_fp_emp_3_applicant_fields_order_status_and_role` |
| FP-MATCH-1 | Required skill normalization, score examples, integer floor, and tie-breakers | `app/skills.py`, `app/matching/engine.py` | `tests/unit/test_matching.py::test_fp_match_1_examples_normalization_and_floor`; `tests/unit/test_matching.py::test_fp_match_1_both_tie_breakers` |
| FP-MATCH-2 | Optional AI explanation or secondary recommendation | Not implemented | N/A; the deterministic required score and ordering do not use an LLM. |
| FP-SCHED-1 | Create and delete future 30-minute slots with explicit time zones; reject invalid slots and booked-slot deletion | `app/timeutil.py`, `app/scheduling/slots.py`, `app/scheduling/routes_employer.py` | `tests/unit/test_sched_slots.py::test_fp_sched_1_slot_creation_timezones_and_deletion`; `tests/unit/test_sched_slots.py::test_fp_sched_1_invalid_slots` |
| FP-SCHED-2 | Enforce application, owner, status, time, and uniqueness conditions for booking | `app/scheduling/booking.py`, `app/scheduling/routes_candidate.py`, `app/schema.sql` | `tests/unit/test_sched_booking.py::test_fp_sched_2_eligible_booking`; `tests/unit/test_sched_booking.py::test_fp_sched_2_ineligible_booking` (parameterized across refusal cases) |
| FP-SCHED-3 | Atomic booking conflict response and exactly one booking row | `app/scheduling/booking.py`, `app/db.py`, `app/schema.sql` | `tests/unit/test_sched_booking.py::test_fp_sched_3_conflict_contract`; `tests/unit/test_sched_booking.py::test_fp_sched_3_conflict_from_second_connection` |
| FP-SEC-1 | Prevent cross-user access to resumes, applications, jobs, applicants, and bookings | `app/security.py`, `app/candidates/resume_service.py`, `app/applications/`, `app/jobs/`, `app/scheduling/` | `tests/unit/test_authz_sweep.py::test_fp_sec_1_object_access_boundaries`; additional named boundary tests in `tests/unit/test_authz_sweep.py` |
| FP-SEC-2 | Bind user-controlled SQL values as parameters | Feature service modules using SQLite queries | `tests/unit/test_auth.py::test_fp_sec_2_sql_metacharacters_stay_bound` |
| FP-SEC-3 | Escape user-controlled text in rendered HTML | Jinja templates under `app/templates/` | `tests/unit/test_emp_company.py::test_fp_sec_3_script_tag_is_escaped` |
| FP-SEC-4 | Isolated test database and placeholder-only environment example | `tests/conftest.py`, `app/config.py`, `.env.example` | `tests/unit/test_db.py::test_fp_sec_4_tests_use_isolated_database`; `.env.example` contains placeholder values only. |
| FP-PROC-1 | Specification describes the submitted architecture, data, routes, workflows, matching, scheduling, and security | `SPEC.md`, `docs/plan/` | Review each SPEC section against its linked plan and implementation; requirement mapping is in this README. |
| FP-DOC-1 | Installation steps, exact commands, versions, environment variables, Docker, and troubleshooting | `INSTALL.md`, `Dockerfile`, `wsgi.py`, `requirements.lock` | Follow INSTALL from a clean checkout; `tests/unit/test_wsgi.py::test_import_wsgi_creates_a_seeded_database` verifies first-start initialization. |
| FP-DOC-2 | README overview, architecture, demo credentials, test command, complete mapping, index, limitations | `README.md` | Review this document; all listed test names were verified using `pytest --collect-only`. |
| FP-DOC-3 | Repeatable local reset and minimum fictional demo dataset | `scripts/seed.py`, `docs/plan/12-DEPLOY.md` | `tests/unit/test_seed.py::test_seed_creates_the_demo_minimum`; `tests/unit/test_seed.py::test_seed_matches_the_four_fp_match_1_scores`; `tests/unit/test_seed.py::test_seed_twice_without_reset_refuses_and_changes_nothing` |
| FP-TEST-1 | Unit coverage for each functional requirement and a non-interactive full-suite command | `tests/unit/`, `scripts/check.py`, `README.md` | `python scripts/check.py`; collected test names are available with `python -m pytest --collect-only -q`; this table maps every functional requirement to its named tests. |
| FP-SUB-1 | Permanent main-branch commit URL and runnable environment built from the repository Dockerfile | `Dockerfile`, `wsgi.py`, `scripts/seed.py`, `INSTALL.md` | Build and run commands in INSTALL; `tests/unit/test_wsgi.py::test_import_wsgi_creates_a_seeded_database`; GitHub commit URL and public main-branch availability are release-submission checks. |

## Document Index

- [Specification](SPEC.md)
- [Installation Guide](INSTALL.md)
- [Product requirements](docs/BRIEF.md)
- [Architecture plan](docs/plan/02-ARCHITECTURE.md)
- [Data model](docs/plan/03-DATA-MODEL.md)
- [Authentication and security](docs/plan/04-AUTH-SECURITY.md)
- [UX flows](docs/plan/05-UX-FLOWS.md)
- [Design system](docs/plan/06-DESIGN-SYSTEM.md)
- [Frozen contracts](docs/plan/07-CONTRACTS.md)
- [Deployment plan](docs/plan/12-DEPLOY.md)
- [Project decisions](docs/state/DECISIONS.md)

## Known Limitations

- Login rate limiting is held in process memory, so separate application processes do not share its counters.
- If `SECRET_KEY` is omitted, the app generates a key at startup; signed-in sessions therefore stop working after a restart.
- Résumés are plain text and private to their owning candidate; file upload and PDF extraction are not implemented.
- Optional AI recommendations or explanations are not implemented.
- The Docker example stores its SQLite database inside the container. Use a mounted data directory if data must persist after removing the container.
