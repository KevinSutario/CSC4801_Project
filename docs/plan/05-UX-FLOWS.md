# 05 · UX flows and screens

Screens follow the Keystone design canvas (web-only cut). The canvas ID in brackets, such as
[C11], is the screen to look at for layout ideas. Routes and template names are frozen in
`07-CONTRACTS.md`.

## Principles (from the canvas)

1. **The system proposes, a person decides.** Any action that sends data to someone else (apply,
   change an applicant's status, delete a job, book a slot) goes through a **confirm screen**
   showing exactly what will happen, to whom, and what will be shared.
2. **Explain every score.** A match score always shows which skills matched and which did not.
3. **Private by default.** Say plainly who can see what ("Only you and employers you apply to can
   open this resume").
4. **Plain, short words.** Sentence case. Verb-first buttons: "Save profile", "Apply to this job".
5. **Every list has an empty state** that tells the user what to do next.

## Roles and their home

| Role | Home after sign-in | Nav items |
|---|---|---|
| Visitor | `/` landing [P01] | Sign in, Create account |
| Candidate | `/candidate/` Today [C06] | Today, Recommendations, Applications, Profile, Activity |
| Employer | `/employer/` Home [R01] | Home, Company, Jobs, Activity |

## Journey: candidate

```
Landing [P01] -> Create account [P02] (role = candidate)
  -> Profile [C22/C03]: headline, location, timezone, summary, skills (comma separated)
  -> Upload resume [C01] (PDF, private)
  -> Today [C06]: profile completeness, top 3 recommendations, application statuses
  -> Recommendations [C07]: every open job, ranked, each with score + matched / missing skills
  -> Job detail [C08]: full job, company card, "Apply to this job"
  -> Confirm application [C11]: shows job, resume to be shared, cover note -> Submit
  -> Applications [C12]: list with status badges
  -> Application detail: status; if eligible, list of open slots in her timezone
  -> Confirm booking -> Booked (or conflict message per brief)
```

## Journey: employer

```
Landing -> Create account (role = employer)
  -> Company [R03 area]: name, industry, location, website, description
  -> Jobs [R03]: list, "Post a job"
  -> New job [R05]: title, description, location, type, salary range, skills
  -> Job applicants [R06/R10]: applicants in the brief's order, each with match score, skills,
     resume link, status; actions per allowed status change
  -> Confirm status change -> Updated
  -> Interview slots [R13]: add slot (date, start, end, timezone), list, delete unbooked slot
```

## Screen list

| Screen | Route | Template | Task | Canvas |
|---|---|---|---|---|
| Landing | `GET /` | `index.html` | T03 | P01 |
| Create account | `GET/POST /auth/register` | `auth/register.html` | T05 | P02 |
| Sign in | `GET/POST /auth/login` | `auth/login.html` | T05 | P02 |
| Candidate Today | `GET /candidate/` | `candidates/today.html` | T07 | C06 |
| Candidate profile | `GET/POST /candidate/profile` | `candidates/profile.html` | T07 | C22 |
| Resume upload and list | `GET/POST /candidate/resume` | `candidates/resume.html` | T08 | C01 |
| Recommendations | `GET /candidate/recommendations` | `matching/recommendations.html` | T13 | C07 |
| Job detail | `GET /jobs/<id>` | `jobs/detail.html` | T10 | C08 |
| Confirm application | `GET /jobs/<id>/apply` | `applications/confirm.html` | T14 | C11 |
| My applications | `GET /candidate/applications` | `applications/mine.html` | T14 | C12 |
| Application detail and booking | `GET /candidate/applications/<id>` | `scheduling/book.html` | T16 | C12 |
| Employer home | `GET /employer/` | `employers/home.html` | T09 | R01 |
| Company profile | `GET/POST /employer/company` | `employers/company.html` | T09 | R03 |
| My jobs | `GET /employer/jobs` | `jobs/list.html` | T10 | R03 |
| New or edit job | `GET/POST /employer/jobs/new`, `/employer/jobs/<id>/edit` | `jobs/form.html` | T10 | R05 |
| Confirm job delete | `GET /employer/jobs/<id>/delete` | `jobs/confirm_delete.html` | T10 | none |
| Applicants | `GET /employer/jobs/<id>/applicants` | `applications/applicants.html` | T15 | R06, R10 |
| Interview slots | `GET/POST /employer/jobs/<id>/slots` | `scheduling/slots.html` | T12 | R13 |
| Activity log | `GET /activity` | `activity/list.html` | T18 | A02 |
| Errors | 400, 403, 404, 405, 409, 413, 500 | `errors/<code>.html` | T03 | none |

## Screen content rules

**Recommendations card** (FP-CAN-2): job title, company name, location, employment type, salary
range (or "Not stated"), score shown as a number plus a 5-segment bar, "Matched: Python, SQL",
"Missing: dbt". Every open job appears, including weak matches, unless the brief says otherwise.
Ranking and tie-breaks come from the brief only.

**Applicants table** (FP-EMP-3): candidate name, headline, match score, matched skills, applied
date (shown in the employer's timezone), status badge, resume link, actions. Columns and order
from the brief.

**Confirm application** (Keystone approval pattern): a box titled "This will be sent to
<company>", listing the resume file name, the cover note, and "Not shared: your other
applications, your email address" (adjust to the brief's privacy rules). Buttons: primary
"Submit application", secondary "Back to job".

**Slot times**: always show the timezone label, for example "Mon 30 Nov, 10:00 to 10:45 (Asia/Hong_Kong)".

## Forms

- Labels above fields, field errors directly under the field in danger color, a summary at the top
  when there are errors ("2 fields need fixing").
- Required fields marked "Required" in muted text, not with an asterisk only.
- After a successful POST: redirect, then a success flash ("Profile saved").
- Every POST form includes `{{ csrf_field() }}`.

## Empty states (text is fixed, so tests can find it)

| Where | Text | Action |
|---|---|---|
| Recommendations, no skills | "Add your skills to see how jobs match you." | Edit profile |
| Recommendations, no open jobs | "No open jobs right now. Check back soon." | none |
| My applications | "You have not applied to any jobs yet." | See recommendations |
| My jobs | "You have not posted a job yet." | Post a job |
| Applicants | "No one has applied to this job yet." | none |
| Slots | "No interview slots yet. Add one so applicants can book." | Add slot |
| Activity | "Nothing here yet. Actions you take will show up here." | none |
