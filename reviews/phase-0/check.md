# Phase 0 gate checks

Reviewed snapshot: `697a485` on `dev` (T00 and B1 MERGED).
Environment: Python 3.12, `/private/tmp/keystone-phase0-venv`; pinned dependencies installed from `requirements-dev.txt`.
Ruff cache redirected to `/private/tmp/keystone-phase0-ruff` for sandbox compatibility.

```text
=== lint: /private/tmp/keystone-phase0-venv/bin/python -m ruff check .
All checks passed!

=== tests: /private/tmp/keystone-phase0-venv/bin/python -m pytest tests/unit -q -rs -p no:cacheprovider
....................                                                     [100%]
20 passed in 0.31s

=== contracts: skipped (no app/ folder yet)

============================================================
CHECK PASSED
CONTRACTS: nothing to check yet
```

The first phase packet attempt exposed B1: nonexistent `phase--1`. B1 was repaired test-first, independently checked, reviewed by three reviewers and a judge, and merged after a separate merge review. Phase 0 now compares against Git's empty tree; later phases retain predecessor tags.

`python scripts/make_packet.py phase 0` generated 20 packets successfully.
Phase review and mutation checks are pending. No Phase 0 tag or merge to `main` has been made.
