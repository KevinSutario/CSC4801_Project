# Final Project Product Requirements

This is the normative specification for the project. Every team builds the recruiting and candidate matching system below.

> **MUST** and **MUST NOT** requirements are graded. **SHOULD** items are recommended but not graded unless they are required by another **MUST**. **MAY** items are optional.

## 1. Product boundary

### FP-ARCH-1: Full-stack boundary

The submission **MUST** be a locally runnable full-stack application with:


- **a browser-based user interface;**
- **a backend server or API enforcing business rules and authorization; and**
- **a persistent relational database.**

The application **MUST** work from a clean checkout by following `INSTALL.md`. Using a hosted service is optional and **MUST NOT** be necessary for grading. If the application uses an external LLM, the core system and automated tests **MUST** still run without paid credentials, using a deterministic fake or a non-LLM fallback.

## 2. Roles and authentication

### FP-AUTH-1: Accounts

The system **MUST** support exactly two application roles: `Candidate` and `Employer`. A user **MUST** be able to register, log in, and log out. Email or username identifiers **MUST** be unique.

### FP-AUTH-2: Credential storage

Passwords **MUST** be stored with an established password-hashing function. Plain text, reversible encryption, and a general-purpose fast hash such as unsalted SHA-256 do not satisfy this requirement. Authentication secrets **MUST NOT** be returned by an API or rendered in the UI.

### FP-AUTH-3: Server-side authorization

Every protected operation **MUST** enforce role and ownership on the server; hiding a button in the UI is not sufficient. The observable response contract is:

- unauthenticated request: `401 Unauthorized` or redirect to login;
- authenticated user with the wrong role or owner: `403 Forbidden`; and
- missing object that the caller would otherwise be allowed to access: `404 Not Found`.

For non-HTTP frameworks, the UI and service layer **MUST** provide equivalent, clearly distinguishable outcomes.

## 3. Candidate workflow

### FP-CAN-1: Candidate profile and resume

A candidate **MUST** be able to view and edit only their own profile, including a display name and a list of technical skills. Skills **MUST** be saved and available to the matching function.

A candidate **MUST** be able to enter a raw-text resume. The application **MUST** persist the text and allow the owner to view and replace it. PDF upload and extraction are optional. Resume contents are private: only the owning candidate may read or modify them. Any other candidate or employer **MUST** receive `403` through a direct URL/API request.

### FP-CAN-2: Recommendations

A candidate dashboard **MUST** list all current (not deleted) jobs with a visible match score and sort them from highest to lowest score. The dashboard **MUST** include the job title, employer/company, required skills, and a way to view the description.

### FP-CAN-3: Applications

A candidate **MUST** be able to apply to a job once. A new application **MUST** have status `Pending`. A duplicate application by the same candidate to the same job **MUST** be rejected without creating another row. A candidate **MUST** be able to view the job, employer, current status, and interview booking (if any) for each of their own applications.

A candidate **MUST NOT** be able to view another candidate's applications or change an application status.

## 4. Employer workflow

### FP-EMP-1: Company profile

An employer **MUST** be able to view and edit a company profile containing at least a company name and description.

### FP-EMP-2: Job postings

An employer **MUST** be able to create, view, edit, and delete their own job postings. Each posting **MUST** contain a non-empty title and description plus a required-skills list; the list may be empty. An employer **MUST** receive `403` when attempting to edit, delete, or manage applicants for another employer's posting.

A job with no applications or interview slots **MUST** be deletable. If either kind of dependent record exists, deletion **MUST** fail with `409 Conflict` (or a clearly documented equivalent) and leave the job and dependent records unchanged.

### FP-EMP-3: Applicant management

For each owned job, an employer **MUST** be able to view its applicants sorted by match score from highest to lowest. Each row **MUST** show candidate identity, skills, match score, application status, and interview booking (if any).

The employer who owns the job **MUST** be able to set an application to one of exactly these statuses: `Pending`, `Interviewing`, `Rejected`, or `Accepted`. Other employers and candidates **MUST NOT** be able to change the status.

## 5. Matching contract

### FP-MATCH-1: Score definition

The required match score is a deterministic skill-overlap score. Resume text is not an input. Normalize candidate and required skills by trimming surrounding whitespace, converting to lowercase, removing empty values, and removing duplicates. Let `C` and `R` be the resulting candidate-skill and required-skill sets:

```text
score = 100                                      when |R| = 0
score = floor(100 * |C intersection R| / |R|)   otherwise
```

The result **MUST** be an integer from 0 through 100. Candidate and employer views **MUST** call the same implementation. Sort by descending score. Break candidate dashboard ties by case-insensitive job title and then stable job ID; break employer applicant ties by case-insensitive candidate display name and then stable candidate ID.

The seed data and unit tests **MUST** include these examples:

| Candidate skills | Required skills | Expected score |
|---|---|---:|
| `Python, SQL` | `Python, SQL` | 100 |
| `Python` | `Python, SQL` | 50 |
| `Rust` | `Python, SQL` | 0 |
| any skills | empty list | 100 |

`SPEC.md` **MUST** identify the matching implementation and describe how skills are stored. It may cite this formula rather than inventing another scoring oracle.

### FP-MATCH-2: Optional AI enhancement

Teams **MAY** add an LLM-generated explanation or secondary recommendation, but it earns no substitute credit and **MUST NOT** alter the required score or ordering. If user-controlled text is sent to an LLM, it **MUST** be treated as untrusted data, **MUST NOT** reveal prompts or secrets, and the data flow **MUST** be documented in `SPEC.md`. An optional AI enhancement is part of the peer-audit scope.

## 6. Applications and interview scheduling

### FP-SCHED-1: Availability

An employer **MUST** be able to create and delete future, 30-minute availability slots. Each slot **MUST** have one owner and an exact start and end time with an unambiguous, documented timezone. The system **MUST** reject invalid durations, end-before-start values, and deletion of a booked slot. Booked slots **MUST NOT** be shown as available.

### FP-SCHED-2: Booking eligibility

The system **MUST** allow a candidate to book a slot if and only if all of the following are true:

- the candidate owns the application;
- the slot belongs to the employer for the candidate's application;
- the application status is `Interviewing`;
- the slot is in the future and is not already booked; and
- the application has no existing booking.

A successful booking **MUST** link the candidate's application to the slot and be visible to both that candidate and the owning employer. Ineligible bookings **MUST** fail without partially changing either record. If a booked application later leaves `Interviewing`, its booking **MUST** remain associated with the application and the slot **MUST** remain unavailable.

### FP-SCHED-3: Atomic concurrency

Booking **MUST** be atomic at the database layer. Use a transaction plus row locking, optimistic concurrency, a uniqueness constraint, or an equivalent database mechanism. An in-process check alone is insufficient.

When two eligible candidates concurrently attempt to book the same slot, exactly one attempt **MUST** succeed, the other **MUST** fail with conflict status (HTTP `409` or a clearly documented equivalent) and the message `Slot already booked`, and the database **MUST** contain exactly one booking afterward. Students **MUST** write unit tests for the booking conflict-handling logic. Database atomicity is verified through implementation review and the running system; students are not required to provide a synchronized multi-client test.

## 7. Security requirements

### FP-SEC-1: Object access

Changing an object ID in a request **MUST NOT** bypass FP-AUTH-3. Unit tests of the authorization logic **MUST** cover these representative boundaries:

1. one candidate cannot read or modify another candidate's resume or application;
2. one employer cannot modify another employer's job or read its applicant list;
3. a candidate cannot book a slot using another candidate's application.

Unit tests for each functional requirement are additionally required by FP-TEST-1; code review and demonstration supplement that evidence.

### FP-SEC-2: SQL injection

All database access involving user-controlled values **MUST** use parameterized queries, a correctly used ORM, or an equivalent safe API. Concatenating raw user input into a query is prohibited. At least one unit test **MUST** pass SQL metacharacters to the query-building or data-access logic and verify that the input remains a bound value rather than executable SQL. Code review and the running system verify the use of safe database APIs.

### FP-SEC-3: Cross-site scripting

User-controlled profile, resume, company, job, and search text **MUST** be escaped when rendered as HTML. If the design intentionally supports formatted HTML, it **MUST** use an allow-list sanitizer. At least one unit test **MUST** pass `<script>alert(1)</script>` to the rendering or sanitization logic and verify that it is not emitted as executable markup.

### FP-SEC-4: Secrets and test isolation

The repository **MUST** contain no real secrets or personal data. Unit tests **MUST** use isolated fixtures or test doubles and **MUST NOT** call real third-party services. Any test that uses a database **MUST** use an isolated test database. `.env.example` **MUST** contain placeholders only.

## 8. Spec-driven and AI-assisted engineering

### FP-PROC-1: Living specification

`SPEC.md` **MUST** describe the architecture, data model and relationships, authentication/authorization design, API routes or server actions, major UI screens, matching contract, booking transaction, and security controls. The requirement–test mapping **MUST** be written in `README.md` as specified in FP-DOC-2, rather than in `SPEC.md`.

The specification **MUST** match the graded commit. A large generated document that does not match the submitted system receives no credit for accuracy.

Every team member **MUST** be able to explain and safely modify the submitted code, regardless of which portions were AI-generated.

## 9. Documentation, data, tests, and CI

### FP-DOC-1: Installation

`INSTALL.md` **MUST** list prerequisite versions, exact install commands, environment variables, database setup/migrations, seed command, run command, test command, `Dockerfile` build and start commands, and troubleshooting for any non-obvious dependency. A grader with a clean checkout who builds the repository's `Dockerfile` **MUST** not need an undocumented command or secret.

### FP-DOC-2: Repository README

`README.md` **MUST** give a short product overview, architecture summary, quick-start link to `INSTALL.md`, demo account credentials for seeded non-production users, unit-test command, document index, and known limitations. It **MUST** include a requirement–test mapping table covering every requirement ID in this document, with implementation file(s) and named student-written unit tests for each functional requirement. Non-functional requirements may cite the appropriate verification evidence. An optional enhancement that is not implemented may be marked `N/A`.

### FP-DOC-3: Deterministic demo data

One documented command **MUST** reset and seed a local database. Seed data **MUST** include at least:

- two candidates and two employers;
- two jobs with required skills;
- the four matching examples required by FP-MATCH-1;
- applications covering all four statuses; and
- two `Interviewing` candidates eligible to race for the same available slot.

Seed credentials **MUST** be clearly marked as local/demo credentials.

### FP-TEST-1: Automated verification

Students **MUST** write their own unit tests for every functional requirement: FP-AUTH-1 through FP-AUTH-3, FP-CAN-1 through FP-CAN-3, FP-EMP-1 through FP-EMP-3, FP-MATCH-1, and FP-SCHED-1 through FP-SCHED-3 (plus FP-MATCH-2 if implemented). Tests **MUST** exercise the team's actual business logic, cover successful behavior and applicable validation, permission, and conflict cases, and assert observable outcomes. Each functional requirement **MUST** map to named unit tests in the `README.md` table; copied example tests or `pass` placeholders do not satisfy this obligation. Students remain responsible for writing, reviewing, and explaining their tests when using AI assistance.

Only unit tests are required from students. One documented command **MUST** run the complete unit-test suite non-interactively and return a nonzero exit status on failure. The unit tests **MUST** cover:

- the unauthenticated, forbidden, and missing-object outcomes in FP-AUTH-3;
- the four skill-overlap examples and both tie-breaking rules;
- the representative authorization boundaries in FP-SEC-1;
- the SQL-injection case in FP-SEC-2;
- the XSS case in FP-SEC-3; and
- the booking conflict-handling logic in FP-SCHED-3.

Demonstrations **MUST NOT** replace the required unit tests. Product requirements, including database atomicity and server-side security, remain mandatory and may also be checked through code review and the running system. Unit tests with test doubles do not by themselves prove database concurrency behavior.

## 10. Submission protocol

### FP-SUB-1: Submission protocol

Each team **MUST** submit a permanent GitHub commit URL on `main`, and the repository at that commit **MUST** build and run entirely from its own `Dockerfile`. Both conditions **MUST** hold at the same graded commit. Failing either fails the submission-format check below.

#### Git submission

The team **MUST** submit one permanent GitHub commit URL through the course-site submission link, using the form `https://github.com/<owner>/<repository>/commit/<40-character-sha>`. This URL identifies both the repository and the exact graded commit. A moving branch URL such as `/tree/main` **MUST NOT** be used. The linked commit **MUST** be pushed to the repository's `main` branch by the deadline, and the repository **MUST** be public so the instructor and other teams can access it.


#### Dockerfile

The repository **MUST** contain a `Dockerfile` that builds the complete runnable environment from the graded commit, so that graders and auditors can rebuild it after every commit or bug fix. There is **no image tar to upload** — see [`DOCKER.md`](DOCKER.md). The build **MUST**:

- succeed from a clean checkout of the graded commit with no undocumented command or secret;
- include every application and standard dependency image (databases, caches, message brokers) needed to run and test the environment;
- work **without pulling or downloading any undocumented container image** at run time; and
- contain no real credential, API key, personal data, or production database.

The `Dockerfile`, entrypoint scripts, migrations, and seed scripts **MUST** remain in the Git repository. Docker images do not preserve database volumes, so the documented seed command **MUST** initialize the grading data after startup. The image does not replace source submission, CI, migrations, or deterministic seed data.

Before the deadline, the team **SHOULD** verify the build on a clean machine:

1. clone the repository and check out the graded commit;
2. build the environment (`docker build`);
3. start the complete environment using the documented command;
4. run migrations and deterministic seed data;
5. run the required automated test command; and
6. open the browser UI and complete a documented smoke test.

#### Submission-format check and second submission

The first submission passes the format check only if the permanent commit URL is present and resolves to an accessible graded commit on a public repository, required CI checks pass, the repository's `Dockerfile` builds from that commit, and the documented start/seed/test flow works without downloading any undocumented container image.

- If the first submission passes this check, there is no submission-format deduction.
- If the first submission fails this check, the team will make one corrective second submission by the instructor's published deadline. If the second submission passes, **5 points are deducted from the 50-point preliminary total before ranking**. The reduced preliminary total is used to determine the team's rank.
- If the second submission is not made by the deadline or still fails the check, **the final project score is 0**, and the team is not included in the normal rank conversion.


# Cross-Team Peer Review

Read this document before inspecting another team's project. A finding is eligible for points only if it follows this process and the safety boundary. 

> **MUST** and **MUST NOT** requirements are graded. **SHOULD** items are recommended but not graded unless they are required by another **MUST**. **MAY** items are optional.

## 0. Safety boundary

Audit only the target team's source code at the latest commit on its `main` branch, built from the repository's `Dockerfile`, on your own machine or in your own CI. Fixes are pushed to `main`, so always work against the newest commit rather than an older one. You **MAY**:

- read source code and documentation;
- build the environment from the repository's `Dockerfile` and run the project's documented test suite and local server from it;
- write and run a minimal regression test against the local checkout; and
- run static analysis, linters, dependency scanners, and secret scanners against that checkout.

You **MUST NOT**:

- test any deployed URL, shared staging system, real third-party account, or resource the target team did not explicitly provide as local test data;
- perform load testing, denial of service, resource exhaustion, destructive testing, social engineering, or secret exfiltration;
- modify the target team's branches, pull requests, CI, repository settings, or any issue other than the finding you file;
- publish a secret value or personal data; report only its redacted location; or
- scan anything outside the local checkout.

These restrictions apply even if a technique might reveal a valid bug. A safety violation is an academic-integrity issue, not merely an invalid report.

## 1. Audit target

1. Clone the assigned repository and check out the latest commit on its `main` branch.
2. Build the environment from the repository's `Dockerfile` (see [`DOCKER.md`](DOCKER.md)). You **MUST NOT** modify the target source to make the build work.
3. Follow the target team's `INSTALL.md` to start, migrate, seed, test, and smoke-test the environment. You **MUST NOT** modify the target source or repair its setup on a branch or pull request.
4. Use the checked-out source for code inspection and the running Docker environment for runtime review.
5. Record the exact commit SHA where you observed the bug in every report.
6. File findings only during the published audit window.

A finding that omits the exact commit SHA where the bug was observed is not reproducible and is invalid. If the repository's `Dockerfile` fails to build or run, report that environmental problem (it is itself a valid finding) rather than modifying the target source. When the target team pushes a fix to `main`, retest against the latest commit on `main`.

## 2. Valid finding standard

A valid finding **MUST** satisfy every condition below:

- **In scope:** it violates a **MUST** requirement in the course [`REQUIREMENTS.md`](REQUIREMENTS.md), the target team's precise `SPEC.md`, or a documented behavior exposed to users.
- **Present:** it occurs in the environment built from the target repository's `Dockerfile` at the latest `main` commit, without changing the target source.
- **Reproducible:** the report gives exact setup and execution commands plus the smallest practical input or test needed to observe it.
- **Observable:** expected and actual results differ in a concrete way. A style preference, hypothetical concern with no reachable path, or unsupported scanner warning is not a bug.
- **Independent:** it is not a duplicate symptom of an already reported root cause. Search open and closed issues before filing.
- **Safe:** it was found within the boundary in Section 0.

File every finding through the GitHub Issue Form at [`templates/github/ISSUE_TEMPLATE/audit_bug_report.yml`](templates/github/ISSUE_TEMPLATE/audit_bug_report.yml); every team **MUST** enable it in their repository. Missing a required field or reproduction makes the report invalid. One issue **SHOULD** describe one root cause; split only unrelated findings.

### Report types

Every report **MUST** use `audit:report` and `status:needs-triage`, plus exactly one type label. Apply exactly one type label:

| Label | Use when |
|---|---|
| `type:functional` | A required workflow, specification rule, or required test/CI behavior is missing, incorrect, crashes, or cannot be completed. |
| `type:security` | Authentication, authorization, privacy, injection, XSS, prompt safety, secret handling, or test isolation is violated. |
| `type:performance` | A documented performance expectation fails on a small, safe fixture; load or resource-exhaustion testing is never allowed. |

Choose the type that best represents the root cause. `type:security` takes precedence when more than one type could apply.

Every team imports all audit labels (`audit:*`, `type:*`, and `status:*`) into their repository from [`templates/github/labels.yml`](templates/github/labels.yml) so that every repository uses the same label set.

## 3. Reproduction quality

A reader with no prior context should be able to reproduce the result. Include:

- OS and Docker versions and the exact commit SHA you built and observed the bug at, plus any deviation from `INSTALL.md`;
- exact reset and seed commands;
- exact request, UI sequence, or minimal failing test;
- relevant response, exception, assertion, or database count;
- expected behavior with the requirement ID or `SPEC.md` section; and
- actual behavior with secrets and personal data redacted.

Screenshots **MAY** supplement commands but **MUST NOT** replace them. For a concurrency finding, use a synchronization barrier or another repeatable method; sequential requests do not establish a concurrency bug. For a scanner finding, trace the warning to a reachable code path and provide a harmless local proof.

## 4. Triage and resolution

Every new report begins with `status:needs-triage`. The target team or instructor changes it to one of:

- `status:confirmed`: reproducible, in scope, safe, and not a duplicate;
- `status:rejected`: fails any condition in Section 2;
- `status:duplicate`: has the same root cause as an earlier issue, which **MUST** be linked; or
- `status:fixed`: the fix and regression evidence pass at the linked fix commit.

The reporter **MUST NOT** mark their own report confirmed or fixed. For a confirmed issue, the target team **MUST** add a regression test, repair the issue through its normal review process, and open a pull request that links back to the bug report issue and documents the root cause, fix, and verification. The reporter **MAY** build the fixed environment from the linked commit, retest locally, and comment with the result.

All reports and fixes **MUST** meet the published deadlines.

If teams disagree, each side **SHOULD** post one concise, evidence-based comment and ask the instructor or TA to decide. Do not repeatedly change labels or argue about intent. The instructor's final status controls scoring.

## 5. Academic integrity and anti-gaming

- **MUST NOT** split one root cause into several reports to receive extra points.
- **MUST NOT** move, reuse, or backdate commits or claim evidence from a different commit.
- **MUST NOT** fabricate evidence, coordinate duplicate findings, or hide information needed to reproduce a result.
- **MUST NOT** violate the safety boundary to find or demonstrate a bug.

Fabricated evidence, collusion, commit manipulation, and safety violations are academic-integrity matters and earn no audit points.


# Using Docker for the Final Project

Each team repository **MUST** contain a `Dockerfile` so that anyone can build and
run the complete environment from any commit on `main`. Images are rebuilt from
source: there is **no image tar to upload**. Graders and auditors build from the
repository directly, including after every bug fix.

## What your repository must provide

- A `Dockerfile` at the location documented in `INSTALL.md`.
- Entrypoint scripts, migrations, and seed scripts committed to the repository.
- Exact build, start, migrate, seed, and unit-test commands in `INSTALL.md`.
- Documented images, configuration, and startup commands for any dependencies.

The build **MUST** succeed from a clean checkout without an undocumented command
or secret. The running environment **MUST** reproduce the deterministic seed data.

## Build and run

Example commands (replace the image name, port, and application commands with
those documented by the team):

```bash
docker build -t team-example .
docker run -d --name team-example -p 127.0.0.1:8080:8080 team-example
docker exec team-example <migration-command>
docker exec team-example <seed-command>
docker exec team-example <unit-test-command>
```

`INSTALL.md` must also document how to start any required dependencies and how
to persist or reset local data. Graders must be able to follow that document
without guessing a command, image, or secret.

## Auditing another team

Auditors build from the **latest commit on the target team's `main` branch**.
All developers on the target team publish their changes and fixes to `main`.
Auditors only find and report bugs; the target team is responsible for fixing them.
Always update to the newest commit before auditing to avoid reporting stale bugs:

```bash
git clone <target-repo>
cd <target-repo>
git checkout main
git pull
docker build -t audit-target .
```

Then follow the team's `INSTALL.md` to start, migrate, seed, and run unit tests.
Record the exact commit SHA in each report. Do not modify the target team's
source or repository; see [`PEER_REVIEW.md`](PEER_REVIEW.md) for the safety boundary.

# CSC4801 Final Project: Recruiting and Candidate Matching

Teams will build **a full-stack recruiting platform** with AI coding agents and a spec-driven workflow. The product is fixed: a two-sided marketplace in which candidates find and apply to jobs, employers manage applicants, and candidates book interview slots safely under concurrent use.

The framework, language, database, hosting model, and optional enhancements are your team's choice. The required matching baseline and other observable behavior are fixed in [`REQUIREMENTS.md`](REQUIREMENTS.md); requirements are mandatory unless explicitly marked optional.

## Read these documents

| Document | Purpose |
|---|---|
| [`REQUIREMENTS.md`](REQUIREMENTS.md) | Normative product requirements and acceptance criteria |
| [`PEER_REVIEW.md`](PEER_REVIEW.md) | Required cross-team audit procedure, valid-finding standard, and safety rules |
| [`DOCKER.md`](DOCKER.md) | How to build and run the environment from the repository's `Dockerfile` |
| [`templates/github/ISSUE_TEMPLATE/audit_bug_report.yml`](templates/github/ISSUE_TEMPLATE/audit_bug_report.yml) | GitHub Issue Form for audit findings; every team enables it |
| [`templates/github/labels.yml`](templates/github/labels.yml) | Audit labels every team imports into its repository |


## Grading

The final project is **50% of the overall course grade**. A preliminary 50-point team total is used to rank the expected ten teams:

| Component | Preliminary points |
|---|---:|
| Requirements fulfillment (100 raw points scaled to 10) | 10 |
| Cross-team audit and repair | 30 |
| Presentation | 10 |
| **Total used for ranking** | **50** |


### 1. Requirements fulfillment

Students **MUST** write their own unit tests for every functional requirement in `REQUIREMENTS.md` and map them in `README.md`. Only unit tests are required, including the security and booking conflict logic specified in FP-TEST-1. Grading is based on the number of requirements fulfilled. Students are responsible for ensuring that their tests are correct and complete.

### 2. Cross-team audit and repair

Every team starts at **0 audit points**. Valid findings and evidence-backed repairs add to the audit points. Every report and audit action must follow [`PEER_REVIEW.md`](PEER_REVIEW.md). The [`leadboard`](https://sra-research.github.io/CSC4801/project.html) shows the real-time audit points for each team. The final grade is based on the team ranking, not the absolute number of audit points.

#### Finding points

| Outcome | Points |
|---|---:|
| Security bug | +2 |
| Functional or performance bug | +1 |
| Environmental issue (e.g., the repository's `Dockerfile` fails to build or run) | +0.5 |
| Invalid bug report | -0.5 |
| Duplicate bug report | 0 |

One root cause counts as one finding even if it produces several symptoms.

#### Repair points

| Outcome | Points |
|---|---:|
| Valid fix record, permanent fix commit URL, and regression evidence submitted by the repair deadline | +2 |
| Incorrect fix or regression-test claim | -0.5 |


#### Repository availability

The repository must remain publicly readable during the published audit window. Deduct `0.2` audit points per unavailable audit-window hour, capped at 10 points. Instructor-confirmed GitHub-wide outages do not count.


### 3. Presentation
Each team will present its system to the class and answer questions about its implementation. The presentation is graded on clarity, completeness, and correctness of the system's implementation, as well as the team's ability to answer questions about its design and implementation. The presentation is also an opportunity to demonstrate any optional enhancements implemented by the team.

## Milestones

| Week | Required milestone |
|---|---|
| 1-2 | Form a team of three and create a private repository. |
| 3 | Final project and requirements announced. |
| 3-10 | Build the system, tests, documentation, and seed data. |
| 11 | Feature freeze. tests must pass on the `main` branch. |
| 12 | Make the repository public before the audit window. Other teams build the environment from your repository's `Dockerfile` at the latest commit on `main` and conduct peer audits. After feature freeze, make only bug fixes and documentation corrections on `main`. |
| End of Week 12 | Complete repairs and documentation. Submit the permanent URL for the exact graded commit on `main`; its repository `Dockerfile` must build the complete environment. |
| 13-14 | Present the running system and answer implementation questions. |

Exact calendar dates are published on the course site.

## Audit window

The audit window is **08:00-20:00, Monday-Friday of Week 12** in the course timezone. The repository must remain publicly readable throughout that window. Late or interrupted access will result in a penalty.

All auditing is performed against another team's source at the latest commit on its `main` branch, built from the repository's `Dockerfile`, on the auditor's own machine. This is code review and local testing, not penetration testing of a live service. Every auditor must follow [`PEER_REVIEW.md`](PEER_REVIEW.md).

