# 07 · Contracts (frozen)

This file is the single source of truth for **names**. If a name is not here, it does not exist.
Do not rename anything. Do not add a public function to a module you do not own.

To change this file, the orchestrator follows "Contract change request" in `09-AGENT-WORKFLOW.md`.

Type notes: `Conn` means `sqlite3.Connection` with `row_factory = sqlite3.Row`. Services return
plain `dict` (convert rows with `dict(row)`) or `list[dict]`, never `sqlite3.Row`.

---

## Shared modules (written in Phase 1)

### `app/__init__.py` (T01)
```python
def create_app(test_config: dict | None = None) -> Flask
```
Registers blueprints in this order: `core`, `auth`, `candidates`, `employers`, `jobs`, `matching`,
`applications`, `scheduling`, `activity`. Calls `security.init_app(app)` and `errors.init_app(app)`.
Creates `instance/` and `UPLOAD_DIR` if missing.

### `app/config.py` (T01)
```python
class Config:
    SECRET_KEY: str           # env SECRET_KEY or secrets.token_hex(32)
    DATABASE: str             # env DATABASE or <instance>/keystone.sqlite3
    UPLOAD_DIR: str           # env UPLOAD_DIR or <instance>/uploads
    MAX_UPLOAD_MB: int        # env MAX_UPLOAD_MB or 2
    MAX_CONTENT_LENGTH: int   # MAX_UPLOAD_MB * 1024 * 1024
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE: bool   # env SESSION_COOKIE_SECURE == "1"
    PERMANENT_SESSION_LIFETIME: timedelta   # 8 hours unless the brief says otherwise
```

### `app/db.py` (T01)
```python
def get_db() -> Conn            # one per request on flask.g; isolation_level=None; foreign_keys ON
def close_db(e: BaseException | None = None) -> None
def init_db() -> None            # runs schema.sql on the configured database
def transaction(conn: Conn, immediate: bool = False) -> ContextManager[Conn]
    # BEGIN (or BEGIN IMMEDIATE); COMMIT on success; ROLLBACK and re-raise on error
def now_iso() -> str             # UTC now as "YYYY-MM-DDTHH:MM:SSZ"
```
CLI: `flask --app app init-db` (registered in `create_app`).
**Every write must happen inside `with transaction(conn):`.** Connections are in autocommit mode
(`isolation_level=None`), so a write outside a transaction commits immediately.

### `app/errors.py` (T01)
```python
class ServiceError(Exception): ...
class ValidationError(ServiceError):
    def __init__(self, errors: dict[str, str]) -> None   # field name -> message
    errors: dict[str, str]
class NotFound(ServiceError): ...
class Forbidden(ServiceError): ...
class Conflict(ServiceError):
    def __init__(self, message: str) -> None
    message: str
def init_app(app: Flask) -> None
    # NotFound -> 404 errors/404.html; Forbidden -> 403 errors/403.html
    # Conflict -> 409 errors/409.html (unless the route handles it)
    # also handles HTTP 400, 403, 404, 405, 413, 500 with errors/<code>.html
```
Routes catch `ValidationError` themselves and re-render the form with status 400.

### `app/security.py` (T02)
```python
def init_app(app: Flask) -> None     # before_request: load_user, csrf_protect; after_request: headers
def login_required(view)              # decorator
def role_required(role: str)          # decorator factory: "candidate" | "employer"
def csrf_token() -> str               # creates session["csrf"] if missing
def rotate_csrf() -> None             # new token (call after login)
def is_safe_next(target: str | None) -> bool
def login_key(email: str, ip: str) -> str
def is_login_blocked(key: str) -> bool
def record_failed_login(key: str) -> None
def reset_login_failures(key: str) -> None
```
`g.user` is `dict | None` with keys `id, email, role, display_name`.
Jinja globals: `csrf_token()`, `current_user` (same as `g.user`).

### `app/audit.py` (T02)
```python
def log_event(conn: Conn, actor_id: int | None, action: str, object_type: str,
              object_id: int | None, detail: str = "") -> None   # call inside the caller's transaction
def list_events(conn: Conn, actor_id: int, limit: int = 100) -> list[dict]   # newest first
ACTIONS: frozenset[str]   # the fixed list in 03-DATA-MODEL.md; log_event raises ValueError otherwise
```

### `app/skills.py` (T01 writes a PROVISIONAL version, T11 owns it afterwards)
```python
def normalise_skill(raw: str) -> str          # PROVISIONAL: strip, lower-case, collapse spaces
def parse_skill_list(text: str) -> list[str]  # split on commas, normalise, drop empties, dedupe keeping order
def get_or_create_skill_ids(conn: Conn, names: list[str]) -> list[int]   # names already normalised
```

### Templates and static (T03)
```
templates/base.html               blocks: title, content. Shows nav for current_user.role.
templates/index.html              landing page
templates/components/ui.html      button, link_button, badge, card, empty_state, score_bar,
                                  confirm_box, flash_messages
templates/components/forms.html   field, textarea_field, select_field, csrf_field
templates/errors/400.html 403.html 404.html 405.html 409.html 413.html 500.html
static/css/tokens.css  static/css/app.css
```
Macro signatures are in `06-DESIGN-SYSTEM.md`. Import with
`{% from "components/ui.html" import button, badge %}`.

### `app/core/routes.py` (T03)
| Endpoint | Method and path | Who |
|---|---|---|
| `core.index` | GET `/` | anyone. Signed in: redirect to `candidates.today` or `employers.home`. |

### `tests/conftest.py` (T01 writes app, client, conn; T04 adds the rest)
Fixtures: `app`, `client`, `conn`, `make_candidate`, `make_employer`, `make_company`, `make_job`,
`make_application`, `make_slot`, `login`, `login_as`, `csrf_post`. Signatures:
```python
make_candidate(email="cand@example.com", password="Passw0rd!", name="Mei Lin Tan",
               skills=("python", "sql")) -> int          # user id
make_employer(email="emp@example.com", password="Passw0rd!", name="Daniel Wong") -> int
make_company(employer_id: int, name="Harbourline Logistics") -> int
make_job(employer_id: int, title="Data Analyst", skills=("python",), is_open=1, **cols) -> int
make_application(candidate_id: int, job_id: int, status="pending") -> int
make_slot(employer_id: int, job_id: int, starts_at="2030-01-07T02:00:00Z",
          ends_at="2030-01-07T02:45:00Z", created_tz="UTC") -> int
login(client, email, password) -> Response           # through /auth/login (works after T05)
login_as(client, user_id: int, role: str) -> None     # sets the session directly, plus a csrf token
csrf_post(client, url, data: dict, **kwargs) -> Response   # adds the session CSRF token
```
Factories insert with SQL directly (not through services), so lanes do not depend on each other.

---

## Feature modules

Each row lists the owning task. Only that task (or a later bug task) edits the file.

### auth (T05, T06)
`app/auth/service.py`
```python
def register(conn: Conn, email: str, password: str, role: str, display_name: str) -> int
def authenticate(conn: Conn, email: str, password: str) -> dict | None
def get_user(conn: Conn, user_id: int) -> dict | None
```
`app/auth/routes.py`
| Endpoint | Path | Methods |
|---|---|---|
| `auth.register` | `/auth/register` | GET, POST |
| `auth.login` | `/auth/login` | GET, POST |
| `auth.logout` | `/auth/logout` | POST |

### candidates: profile (T07)
`app/candidates/profile_service.py`
```python
def get_profile(conn: Conn, candidate_id: int) -> dict
    # keys: headline, location, timezone, summary, skills (list[str]), updated_at (or None)
def save_profile(conn: Conn, candidate_id: int, headline: str, location: str,
                 timezone: str, summary: str, skills_text: str) -> None
```
`app/candidates/routes_profile.py`: `candidates.today` GET `/candidate/`;
`candidates.profile` GET, POST `/candidate/profile`

### candidates: resume (T08)
`app/candidates/resume_service.py`
```python
def save_resume(conn: Conn, upload_dir: str, owner_id: int, file) -> int   # file: werkzeug FileStorage
def list_resumes(conn: Conn, owner_id: int) -> list[dict]
def delete_resume(conn: Conn, upload_dir: str, owner_id: int, resume_id: int) -> None
def can_view_resume(conn: Conn, viewer_id: int, viewer_role: str, resume_id: int) -> bool
def get_resume_for_download(conn: Conn, viewer_id: int, viewer_role: str, resume_id: int) -> dict
    # raises NotFound if missing or not allowed
```
`app/candidates/routes_resume.py`: `candidates.resume` GET, POST `/candidate/resume`;
`candidates.resume_delete` POST `/candidate/resume/<int:resume_id>/delete`;
`candidates.resume_download` GET `/resumes/<int:resume_id>`

### employers (T09)
`app/employers/service.py`
```python
def get_company(conn: Conn, employer_id: int) -> dict | None
def get_company_by_id(conn: Conn, company_id: int) -> dict | None
def save_company(conn: Conn, employer_id: int, name: str, industry: str, location: str,
                 website: str, description: str) -> int
```
`app/employers/routes.py`: `employers.home` GET `/employer/`;
`employers.company` GET, POST `/employer/company`

### jobs (T10)
`app/jobs/service.py`
```python
def create_job(conn: Conn, employer_id: int, title: str, description: str, location: str,
               employment_type: str, salary_min: str, salary_max: str, skills_text: str) -> int
def update_job(conn: Conn, employer_id: int, job_id: int, title: str, description: str,
               location: str, employment_type: str, salary_min: str, salary_max: str,
               skills_text: str, is_open: bool) -> None
def delete_job(conn: Conn, employer_id: int, job_id: int) -> None
def get_owned_job(conn: Conn, employer_id: int, job_id: int) -> dict    # NotFound if not theirs
def get_job(conn: Conn, job_id: int) -> dict    # with company_name, skills; NotFound if missing
def list_jobs_for_employer(conn: Conn, employer_id: int) -> list[dict]
def list_open_jobs(conn: Conn) -> list[dict]    # every open job with company_name and skills
EMPLOYMENT_TYPES: tuple[str, ...]               # from the brief
```
Salary fields arrive as form strings; the service parses them (empty means None).
`app/jobs/routes.py`: `jobs.my_jobs` GET `/employer/jobs`; `jobs.new` GET, POST `/employer/jobs/new`;
`jobs.edit` GET, POST `/employer/jobs/<int:job_id>/edit`; `jobs.confirm_delete` GET and
`jobs.delete` POST `/employer/jobs/<int:job_id>/delete`; `jobs.detail` GET `/jobs/<int:job_id>`

### matching (T11 engine, T13 service and routes)
`app/matching/engine.py` (pure: no imports from `app` except `app.skills`)
```python
def score(candidate_skills: set[str], job_skills: set[str]) -> dict
    # {"score": <number per brief>, "matched": sorted list, "missing": sorted list}
def rank(candidate_skills: set[str], jobs: list[dict]) -> list[dict]
    # returns NEW dicts: each job's fields unchanged plus score, matched, missing;
    # sorted by the brief's rule and both tie-breakers; never mutates the input
```
`app/matching/service.py` (T13)
```python
def recommend_for(conn: Conn, candidate_id: int) -> list[dict]
def score_candidate_for_job(conn: Conn, candidate_id: int, job_id: int) -> dict
```
`app/matching/routes.py` (T13): `matching.recommendations` GET `/candidate/recommendations`

### applications (T14 candidate side, T15 employer side)
`app/applications/statuses.py` (T14)
```python
STATUSES: tuple[str, ...]                      # from the brief, first is "pending"
TRANSITIONS: dict[str, tuple[str, ...]]        # allowed next statuses, from the brief
LABELS: dict[str, str]                         # status -> display text
```
`app/applications/service.py` (T14)
```python
def apply(conn: Conn, candidate_id: int, job_id: int, resume_id: int | None,
          cover_note: str) -> int
def list_for_candidate(conn: Conn, candidate_id: int) -> list[dict]
def get_own_application(conn: Conn, candidate_id: int, application_id: int) -> dict
```
`app/applications/review_service.py` (T15)
```python
def list_applicants(conn: Conn, employer_id: int, job_id: int) -> list[dict]
def set_status(conn: Conn, employer_id: int, application_id: int, new_status: str) -> None
```
`app/applications/routes_candidate.py` (T14): `applications.confirm` GET and
`applications.submit` POST `/jobs/<int:job_id>/apply`; `applications.mine` GET `/candidate/applications`
`app/applications/routes_employer.py` (T15): `applications.applicants` GET
`/employer/jobs/<int:job_id>/applicants`; `applications.confirm_status` GET and
`applications.set_status` POST `/employer/applications/<int:application_id>/status`

### scheduling (T12 slots, T16 and T17 booking)
`app/timeutil.py` (T12, pure)
```python
def validate_tz(name: str) -> str                   # ValueError if not an IANA zone
def local_to_utc(date_str: str, time_str: str, tz_name: str) -> str   # "YYYY-MM-DD","HH:MM" -> UTC iso
def utc_to_local(utc_iso: str, tz_name: str) -> datetime
def format_local(utc_iso: str, tz_name: str) -> str  # "Mon 30 Nov 2026, 10:00 (Asia/Hong_Kong)"
def parse_iso(utc_iso: str) -> datetime              # aware UTC
COMMON_TIMEZONES: tuple[str, ...]                    # for the select box
```
`local_to_utc` raises `ValueError` for a local time that does not exist (DST gap): it converts,
converts back, and compares.

`app/scheduling/slots.py` (T12)
```python
def create_slot(conn: Conn, employer_id: int, job_id: int, date_str: str, start_str: str,
                end_str: str, tz_name: str) -> int
def delete_slot(conn: Conn, employer_id: int, slot_id: int) -> None
def list_slots_for_job(conn: Conn, employer_id: int, job_id: int) -> list[dict]   # adds "booked": bool
```
`app/scheduling/booking.py` (T16, then T17)
```python
def is_eligible(conn: Conn, candidate_id: int, application_id: int) -> bool
def list_bookable_slots(conn: Conn, candidate_id: int, application_id: int) -> list[dict]
def book_slot(conn: Conn, candidate_id: int, application_id: int, slot_id: int) -> int
    # Forbidden if not eligible; NotFound if missing or not theirs; Conflict per brief
```
`app/scheduling/routes_employer.py` (T12): `scheduling.slots` GET, POST
`/employer/jobs/<int:job_id>/slots`; `scheduling.delete_slot` POST `/employer/slots/<int:slot_id>/delete`
`app/scheduling/routes_candidate.py` (T16): `scheduling.application_detail` GET
`/candidate/applications/<int:application_id>`; `scheduling.confirm_booking` GET and
`scheduling.book` POST `/candidate/applications/<int:application_id>/book/<int:slot_id>`

### activity (T18)
`app/activity/routes.py`: `activity.list` GET `/activity` (signed-in users; own events only)

---

## Blueprint objects

Each package `__init__.py` (written by T01, frozen) is exactly:
```python
from flask import Blueprint
bp = Blueprint("<name>", __name__)
from . import <route modules>  # noqa: E402,F401
```
Route modules start as stubs (T01): `from . import bp` and nothing else. The owning task fills them.

## Test files and owners

| File | Owner | Template test names it must contain |
|---|---|---|
| `tests/unit/test_db.py` | T01 | none (extra) |
| `tests/unit/test_security.py` | T02 | none (extra) |
| `tests/unit/test_audit.py` | T02 | none (extra) |
| `tests/unit/test_auth.py` | T04 (placeholders), T05, then T06 | `test_fp_auth_1_registration_and_session_lifecycle`, `test_fp_auth_1_invalid_registration`, `test_fp_auth_2_salted_hash_and_password_verification`, `test_fp_auth_3_authorization_and_missing_object` |
| `tests/unit/test_can_profile.py` | T07 | none (extra) |
| `tests/unit/test_can_resume.py` | T08 | `test_fp_can_1_profile_and_private_resume_rules` |
| `tests/unit/test_emp_company.py` | T09 | `test_fp_emp_1_company_profile` |
| `tests/unit/test_emp_jobs.py` | T10 | `test_fp_emp_2_job_validation_and_deletion` |
| `tests/unit/test_matching.py` | T11 | `test_fp_match_1_examples_normalization_and_floor`, `test_fp_match_1_both_tie_breakers` |
| `tests/unit/test_timeutil.py` | T12 | none (extra) |
| `tests/unit/test_sched_slots.py` | T12 | `test_fp_sched_1_slot_creation_timezones_and_deletion`, `test_fp_sched_1_invalid_slots` |
| `tests/unit/test_can_recommend.py` | T13 | `test_fp_can_2_recommendations_preserve_fields_and_rank_all_jobs` |
| `tests/unit/test_can_apply.py` | T14 | `test_fp_can_3_pending_duplicate_and_application_owner` |
| `tests/unit/test_emp_applicants.py` | T15 | `test_fp_emp_3_applicant_fields_order_status_and_role` |
| `tests/unit/test_sched_booking.py` | T16, then T17 | `test_fp_sched_2_eligible_booking`, `test_fp_sched_2_ineligible_booking`, `test_fp_sched_3_conflict_contract` |
| `tests/unit/test_activity.py` | T18 | none (extra) |
| `tests/unit/test_authz_sweep.py` | T06 | none (extra) |

T04 creates every file in this table that does not exist yet, holding the template test names as
`@pytest.mark.skip(reason="TODO Txx")` placeholders, and deletes the template's
`tests/unit/test_workflows.py` and `tests/unit/test_scheduling.py` (their tests move to the files above).
