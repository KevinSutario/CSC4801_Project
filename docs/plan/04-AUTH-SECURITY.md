# 04 · Authentication and security

Other teams will attack this app in the Week 12 audit, and every confirmed security bug costs
marks. This file is the spec, and it doubles as the checklist every reviewer uses.

## Authentication

| Item | Design |
|---|---|
| Accounts | email + password + role (`candidate` or `employer`), chosen at sign-up |
| Password hashing | `werkzeug.security.generate_password_hash(password)` (salted, scrypt by default). Verify with `check_password_hash`. Never store or log the password. |
| Password rules | from the brief; default minimum 8 characters, maximum 128 |
| Email | stripped and lower-cased; basic format check; unique (case-insensitive) |
| Sign-up errors | field messages, HTTP 400, form refilled except password |
| Duplicate email | same generic message as other errors where the brief allows, to limit account probing |
| Session | Flask signed cookie. Holds only `user_id`, `role`, `csrf`. |
| Sign in | `session.clear()` first (stops session fixation), then set values and a new CSRF token |
| Sign out | POST only, with CSRF. `session.clear()`. |
| Cookie flags | `SESSION_COOKIE_HTTPONLY=True`, `SESSION_COOKIE_SAMESITE="Lax"`, `SESSION_COOKIE_SECURE` on when served over HTTPS |
| Session lifetime | from the brief; default `PERMANENT_SESSION_LIFETIME` 8 hours |
| Brute force | per email and per IP: 5 failed logins in 10 minutes blocks the next try for 10 minutes (in-memory dict, fine for one process). Message does not say whether the email exists. |
| Current user | `security.load_user` runs before every request: reads `session["user_id"]`, loads the row, puts it on `g.user`. A deleted user means the session is cleared. |

## Authorization

- `@login_required`: no user, redirect to sign-in (GET) or 401 (POST).
- `@role_required("employer")` or `("candidate")`: wrong role gives 403.
- **Object ownership is checked in the service, every time**, with the actor id passed in.
  Never trust an id from the form or URL on its own.
- Missing object gives 404. Another user's object gives 403 or 404, as the brief says
  (FP-AUTH-3). Until the brief says otherwise, use **404** for both, so ids cannot be probed.
- Ownership helpers (in services): `get_owned_job(conn, employer_id, job_id)`,
  `get_owned_slot(...)`, `get_own_application(...)`, `can_view_resume(conn, viewer, resume_id)`.

## Request security

| Threat | Control |
|---|---|
| CSRF | Every POST form has `<input type="hidden" name="csrf_token">` from the `csrf_field()` macro. `before_request` rejects a POST with a missing or wrong token (403), compared with `hmac.compare_digest`. No exceptions, logout included. |
| SQL injection | Only `?` placeholders. No f-strings or `%` or `+` in SQL. Column and sort names, if dynamic, come from a fixed allowlist dict. |
| XSS | Jinja autoescape stays on. Never use `|safe` or `Markup()` on user data. No inline event handlers. |
| Open redirect | `next` parameter is accepted only if it starts with `/` and not `//`. |
| Clickjacking | `X-Frame-Options: DENY` and CSP `frame-ancestors 'none'` |
| Content sniffing | `X-Content-Type-Options: nosniff` on every response |
| CSP | `default-src 'self'; style-src 'self' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; form-action 'self'; base-uri 'none'; frame-ancestors 'none'` |
| Referrer | `Referrer-Policy: same-origin` |
| Debug leaks | `debug` off in Docker. Error handlers render plain pages for 400, 403, 404, 413, 500 without tracebacks. |
| Secrets | `SECRET_KEY` from env only. Never committed. `.env` stays gitignored. |
| Mass assignment | Services take named fields only. Never `**request.form`. `role` is never editable after sign-up. |
| Integer ids | Route converters `<int:job_id>`, so non-numbers give 404. |

## File uploads (resumes)

- `MAX_CONTENT_LENGTH` set from `MAX_UPLOAD_MB`; larger uploads give 413 with a friendly page.
- Allowed types from the brief; default PDF only. Check the extension **and** the first bytes
  (`%PDF-`).
- Stored as `secrets.token_hex(16) + ".pdf"` under `UPLOAD_DIR`, outside `static/`.
- `original_name` is for display only. It passes through `werkzeug.utils.secure_filename` and is
  never used as a path.
- Download route checks `can_view_resume`, then `send_file(path, as_attachment=True,
  download_name=original_name, mimetype="application/pdf")`.
- Deleting a resume removes the row and the file.

## Data privacy

- A resume is private to its owner, plus anyone the brief allows (likely the employer of a job
  the candidate applied to).
- Employers see applicants only for their own jobs.
- The audit log never stores passwords, tokens or file contents.
- Demo data uses fake people and companies only.

## Security review checklist (reviewers tick every line)

1. Every new route has `@login_required` and the right `@role_required`, or a written reason why not.
2. Every POST form includes `csrf_field()`. No route skips the CSRF check.
3. Every service that loads an object by id also checks the actor owns it or may see it.
4. Missing and not-yours both give the agreed status code. Try an id that belongs to another user.
5. All SQL uses `?` placeholders. Search the diff for `f"`, `.format(`, `%` and `+` near `execute`.
6. No `|safe`, `Markup(` or `autoescape false` on anything a user typed.
7. Uploads: size cap, type check by content, random stored name, served only via the checked route.
8. Redirects use `url_for`, or a `next` value that passes the safe-redirect check.
9. No secret, password, token or traceback appears in logs, flash messages, audit detail or HTML.
10. Error responses use the error templates, with the right status code.
11. Sign-in clears the session first. Sign-out is POST with CSRF.
12. Role cannot be changed through any form field.
