# Project Specification

## Product Scope

Keystone is a browser-based recruiting and candidate-matching application for two roles: Candidate and Employer. Candidates manage their own profile, skills, and private plain-text résumé; view and apply to current jobs; track application status; and book an eligible interview slot. Employers manage a company profile and their job postings; review applicants for their own jobs; change application status; and create interview slots.

The product follows the requirements in [docs/BRIEF.md](docs/BRIEF.md). It does not include phone-specific screens, job search, email, file résumé upload or PDF extraction, or optional AI recommendations. Every existing job is current and listable; there is no job open/closed state (D18, D21).

## Architecture

The system is a single Flask 3.1 application using server-rendered Jinja templates and a SQLite database. `app/__init__.py:create_app` configures the app and registers the `core`, `auth`, `candidates`, `employers`, `jobs`, `matching`, `applications`, and `scheduling` blueprints. Feature route modules handle HTTP requests, access decorators, form data, and template rendering. Feature services validate inputs, check object ownership, and perform database work using parameterized SQL and the shared transaction helper. Pure matching and time-zone conversion logic live in separate modules.

The request flow is: browser request → Flask security hooks (load user, enforce CSRF, attach security headers) → route with role checks → service → SQLite transaction → redirect or rendered response. Unit tests use isolated SQLite databases and call the real application logic.

## Data Model and Relationships

`app/schema.sql` defines these relational records:

- `users` stores unique case-insensitive email, password hash, role, display name, and creation time.
- A candidate has one `candidate_profiles` row, zero or more `candidate_skills` linked to normalized `skills`, and at most one `resumes` row.
- An employer has one `companies` row and may own many `jobs`; job requirements use `job_skills` linked to `skills`.
- `applications` link a candidate to a job, store status and cover note, and have a unique `(job_id, candidate_id)` index to enforce one application per candidate per job.
- Employers own `interview_slots`; `bookings` associate a slot with an application. Unique indexes on `slot_id` and `application_id` prevent double booking and multiple bookings for one application.
- `audit_log` stores consequential event metadata without passwords, tokens, or résumé contents.

Foreign keys express ownership and deletion behavior. Job deletion is refused by the service with a conflict when applications depend on it; the database `ON DELETE RESTRICT` constraint is a backstop. See [the data model plan](docs/plan/03-DATA-MODEL.md) for the schema and relationships.

## Authentication and Authorization

Accounts use an email, password, and one of the two roles (`candidate` or `employer`). Passwords are stored using Werkzeug’s salted password-hashing functions. Flask’s signed session holds the user identity and role; signing in clears the prior session and rotates the CSRF token. The cookie is HTTP-only and SameSite=Lax, with the secure flag configurable for HTTPS. Failed-login throttling is in process memory.

Protected routes use `login_required` and/or `role_required`. Services receive the acting user’s ID and enforce ownership on every object operation. A missing object returns 404 when the caller could otherwise access it; an existing object owned by another user returns 403. The résumé-view rule deliberately returns 403 for any candidate ID other than the viewer’s own, including a nonexistent ID, as recorded in D10. See [the authentication and security plan](docs/plan/04-AUTH-SECURITY.md).

## API Routes or Server Actions

Keystone exposes server-rendered HTML routes rather than a JSON API. The registered endpoints are:

| Endpoint | Methods and path | Access |
|---|---|---|
| `core.index` | GET `/` | Public; signed-in users are redirected to their role home. |
| `auth.register` | GET, POST `/auth/register` | Public. |
| `auth.login` | GET, POST `/auth/login` | Public. |
| `auth.logout` | POST `/auth/logout` | CSRF-protected; clears the session. |
| `candidates.today` | GET `/candidate/` | Candidate. |
| `candidates.profile` | GET, POST `/candidate/profile` | Candidate; own profile. |
| `candidates.resume` | GET, POST `/candidate/resume` | Candidate; own résumé. |
| `candidates.resume_view` | GET `/candidates/<int:candidate_id>/resume` | Signed-in; owner only. |
| `employers.home` | GET `/employer/` | Employer. |
| `employers.company` | GET, POST `/employer/company` | Employer; own company. |
| `jobs.my_jobs` | GET `/employer/jobs` | Employer; own jobs. |
| `jobs.new` | GET, POST `/employer/jobs/new` | Employer. |
| `jobs.edit` | GET, POST `/employer/jobs/<int:job_id>/edit` | Employer; job owner. |
| `jobs.confirm_delete` | GET `/employer/jobs/<int:job_id>/delete` | Employer; job owner. |
| `jobs.delete` | POST `/employer/jobs/<int:job_id>/delete` | Employer; job owner; CSRF-protected. |
| `jobs.detail` | GET `/jobs/<int:job_id>` | Signed-in. |
| `matching.recommendations` | GET `/candidate/recommendations` | Candidate. |
| `applications.confirm` | GET `/jobs/<int:job_id>/apply` | Candidate. |
| `applications.submit` | POST `/jobs/<int:job_id>/apply` | Candidate; CSRF-protected. |
| `applications.mine` | GET `/candidate/applications` | Candidate; own applications. |
| `applications.applicants` | GET `/employer/jobs/<int:job_id>/applicants` | Employer; owner of job. |
| `applications.confirm_status` | GET `/employer/applications/<int:application_id>/status` | Employer; owner of job. |
| `applications.set_status` | POST `/employer/applications/<int:application_id>/status` | Employer; owner of job; CSRF-protected. |
| `scheduling.slots` | GET, POST `/employer/slots` | Employer; own slots; POST is CSRF-protected. |
| `scheduling.delete_slot` | POST `/employer/slots/<int:slot_id>/delete` | Employer; slot owner; CSRF-protected. |
| `scheduling.application_detail` | GET `/candidate/applications/<int:application_id>` | Candidate; application owner. |
| `scheduling.confirm_booking` | GET `/candidate/applications/<int:application_id>/book/<int:slot_id>` | Candidate; application owner. |
| `scheduling.book` | POST `/candidate/applications/<int:application_id>/book/<int:slot_id>` | Candidate; application owner; CSRF-protected. |

Route names and signatures follow [the frozen contracts](docs/plan/07-CONTRACTS.md). There are no separate client-side server actions.

## User Interface and Workflows

The application uses Jinja templates, shared layout and UI/form macros, and local CSS. Visitors see the landing page and account links. Candidates can visit their home, edit their profile, replace their private résumé, review all jobs in ranked recommendations, open job details, confirm an application, track applications, and view or confirm a booking. Employers can edit a company profile, create and manage jobs, review ranked applicants, confirm status changes, and manage interview slots.

Consequential actions have a confirmation step where specified by the workflow. Every POST form includes the CSRF macro. Lists provide a next-step empty state; match scores show matched and missing skills. Jinja autoescaping is used for user-provided text. See [the UX flow plan](docs/plan/05-UX-FLOWS.md) and the frozen route and template contracts.

## Matching Algorithm and Skill Storage

Candidate skills and job-required skills are stored in normalized form in `skills` and linked through `candidate_skills` and `job_skills`. Normalization trims surrounding whitespace and lowercases; empty entries are removed and duplicates are removed while preserving the specified order during parsing. Matching does not read résumé text.

For candidate skill set `C` and required skill set `R`, the score is 100 if `R` is empty; otherwise it is `floor(100 × |C ∩ R| / |R|)`. Scores are integers from 0 to 100. Candidate job lists sort by descending score, then case-insensitive title, then job ID. Employer applicant lists sort by descending score, then case-insensitive candidate display name, then candidate ID. The shared implementation is `app/matching/engine.py` (`score` and `rank`), and the database service is `app/matching/service.py` (D15).

## Interview Scheduling and Booking Transaction

Employers create future availability with a start, end, and IANA time-zone name. The scheduling service validates local times, converts them to UTC ISO-8601 values, and requires a 30-minute duration. The entered zone is stored with the slot so its time basis is explicit. Candidates see available times in their profile time zone. Slots are owned by employers rather than jobs (D13).

A candidate may book only when they own the application, its status is `interviewing`, it has no booking, the slot belongs to the employer for the job, and the slot is future and unbooked. `app/scheduling/booking.py:book_slot` checks these conditions and inserts within `BEGIN IMMEDIATE`. Unique database indexes on slot and application are the final guard against conflicting writes. A losing booking attempt rolls back and becomes `Conflict("Slot already booked")`, displayed with HTTP 409; a conflict audit event is written after rollback (D14). A status change away from interviewing does not remove an existing booking. Résumés remain raw text and owner-only (D10); job/application/status decisions follow D11 and D12; slot ownership and duration follow D13.

## Security Controls

- `@login_required`, `@role_required`, and service-level ownership checks protect server routes and objects.
- Session cookies are HTTP-only and SameSite=Lax; the secure cookie flag can be enabled for HTTPS. Login clears the session and rotates CSRF state.
- A `before_request` hook checks CSRF tokens on POST requests. User values in SQL are bound parameters.
- Jinja autoescaping is retained; user text is not marked safe. The application does not accept résumé files or store their contents on disk.
- Response headers include a content security policy, frame protection, content-type sniffing protection, and a same-origin referrer policy.
- The login `next` target is checked to prevent external redirects. Errors are rendered through shared error pages without exception traces.
- Audit records exclude passwords, tokens, and résumé contents. Demo records are fictional and `.env.example` contains placeholders.

These controls follow [the security plan](docs/plan/04-AUTH-SECURITY.md). The rate limiter is process-local.

## Optional AI Features and Data Flow

Not implemented. No user data is sent to an LLM. The required matching score and ranking are deterministic and do not use AI.

## Design Decisions and Limitations

- D10: the résumé is raw text, one per candidate, and readable only by its owner; file upload is not used.
- D11: applications can move to any different one of the four allowed statuses; a candidate may apply once per job ever.
- D12: deleting a job with an application returns conflict and changes nothing; an empty required-skills list is allowed.
- D13: interview slots belong to employers, last exactly 30 minutes, and must be in the future.
- D14: slot booking uses `BEGIN IMMEDIATE`, a unique slot constraint, and the exact conflict message `Slot already booked`.
- D15: matching scores and tie-breakers follow FP-MATCH-1.
- D18: no job open/closed flag or optional job-search workflow is included; limits and other unstated product defaults are documented in the decisions file.
- D21 and D22: scope is limited to the brief; the activity-log viewer and dashboard widgets are descoped, while audit logging remains.

Known operational limitations include process-local login throttling and generated session keys when `SECRET_KEY` is unset. See [docs/state/DECISIONS.md](docs/state/DECISIONS.md) for the complete decision record.
