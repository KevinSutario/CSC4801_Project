# Review packet T00 (1 of 1)

Worktree: /Users/mac/ks-T00

Files in this packet: (no changes)

## Review type: task

## Task card

# T00 · Tooling and gate

| Phase | Lane | Depends on | Joins lanes | Status |
|---|---|---|---|---|
| 0 | tooling | none | no | DONE in setup: verify and commit |

## Goal
`python scripts/check.py` works on Windows and in Docker and passes on the template repo.

## Owns
- `scripts/*`
- `pytest.ini`
- `ruff.toml`
- `requirements-dev.txt`
- `requirements.lock`
- `.gitignore`

## May read
- `CLAUDE.md`, `docs/plan/09-AGENT-WORKFLOW.md`, `docs/plan/10-REVIEW-PROTOCOL.md`

## Steps (already done in setup; the agent only verifies)
1. `requirements.lock` contains `tzdata==2026.5`.
2. `.gitignore` contains `instance/`, `tests/repro/`, `reviews/*/repro/`.
3. `python -m pip install -r requirements-dev.txt`
4. `python scripts/check.py` prints CHECK PASSED.
5. `python scripts/check_scope.py --overlap T07 T09 T12` prints OK.

## Done when
- Steps 3 to 5 pass. Kevin commits on `dev` and tags `phase-0`.


## Changed files

```

```

## Check output (in the worktree)

```
=== lint: /Users/mac/ks-T00/.venv/bin/python -m ruff check .
All checks passed!

=== tests: /Users/mac/ks-T00/.venv/bin/python -m pytest tests/unit -q -rs -p no:cacheprovider
.................                                                        [100%]
17 passed in 0.01s

=== contracts: skipped (no app/ folder yet)

============================================================
CHECK PASSED
```

## Scope check

```
SCOPE OK for T00
```

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



## Diff

```diff

```
