"""Check that the names in docs/plan/07-CONTRACTS.md really exist.

Reads scripts/contracts.json. Checks the tasks marked MERGED in docs/state/STATUS.md, plus the
task of the current branch if it is task/<id>. For each: every module:name can be imported, and
every endpoint exists in the Flask app with the right path and methods.

Usage: python scripts/check_contracts.py
"""

from __future__ import annotations

import importlib
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)


def merged_tasks() -> set[str]:
    path = os.path.join(ROOT, "docs", "state", "STATUS.md")
    done: set[str] = set()
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                m = re.match(r"\|\s*(T\d+\w*)\s*\|[^|]*\|\s*(MERGED|DONE)\s*\|", line)
                if m:
                    done.add(m.group(1))
    branch = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT,
                            capture_output=True, text=True).stdout.strip()
    m = re.match(r"(?:task|int)/(T\d+\w*)$", branch)
    if m:
        done.add(m.group(1))
    return done


def main() -> int:
    with open(os.path.join(ROOT, "scripts", "contracts.json"), encoding="utf-8") as fh:
        contracts = json.load(fh)
    tasks = sorted(t for t in merged_tasks() if t in contracts)
    if not tasks:
        print("CONTRACTS: nothing to check yet")
        return 0

    problems: list[str] = []
    for task in tasks:
        for ref in contracts[task]["names"]:
            module_name, _, attr = ref.partition(":")
            try:
                module = importlib.import_module(module_name)
            except Exception as exc:  # noqa: BLE001 - report any import failure
                problems.append(f"{task}: cannot import {module_name}: {exc}")
                continue
            if not hasattr(module, attr):
                problems.append(f"{task}: {module_name} has no {attr}")

    wanted = [(t, e) for t in tasks for e in contracts[t]["endpoints"]]
    if wanted:
        try:
            from app import create_app

            tmp = tempfile.mkdtemp()
            app = create_app({"TESTING": True, "SECRET_KEY": "contracts",
                              "DATABASE": os.path.join(tmp, "c.sqlite3"),
                              "UPLOAD_DIR": os.path.join(tmp, "uploads")})
            rules = {}
            for rule in app.url_map.iter_rules():
                rules.setdefault(rule.endpoint, []).append(rule)
            for task, (endpoint, methods, path) in wanted:
                found = rules.get(endpoint, [])
                if not found:
                    problems.append(f"{task}: endpoint {endpoint} missing")
                    continue
                need = set(methods.split())
                ok = any(r.rule == path and need <= set(r.methods or ()) for r in found)
                if not ok:
                    have = [(r.rule, sorted((r.methods or set()) - {"HEAD", "OPTIONS"}))
                            for r in found]
                    problems.append(f"{task}: {endpoint} should be {methods} {path}, found {have}")
        except Exception as exc:  # noqa: BLE001
            problems.append(f"could not build the app to check endpoints: {exc}")

    if problems:
        print("CONTRACTS FAILED:")
        for p in problems:
            print(f"  {p}")
        return 1
    print("CONTRACTS OK for " + ", ".join(tasks))
    return 0


if __name__ == "__main__":
    sys.exit(main())
