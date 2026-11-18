"""Exercise B1 packet generation with B2's real gate.

Reviewed CLI entry points: make_packet.main() -> int and check.main() -> int.
There is no tests/conftest.py in this tooling-only repository.
"""

from pathlib import Path
import shutil
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[2]
EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"


def run(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=repo, capture_output=True, text=True, timeout=20)


def git(repo: Path, *args: str) -> str:
    result = run(repo, "git", *args)
    assert result.returncode == 0, result.stdout + result.stderr
    return result.stdout


@pytest.mark.parametrize(
    ("state", "expected", "exit_code"),
    [
        ("empty", "CHECK FAILED: tests", 1),
        ("passing", "CHECK PASSED", 0),
        ("failing", "CHECK FAILED: tests", 1),
        ("lint", "CHECK FAILED: lint", 1),
    ],
)
def test_b1_phase_zero_and_merge_packets_preserve_b2_gate_results(
    tmp_path: Path, state: str, expected: str, exit_code: int,
) -> None:
    # The real merge CLI resolves its integration worktree as sibling ks-int.
    repo = tmp_path / "ks-int"
    (repo / "scripts").mkdir(parents=True)
    (repo / "tests" / "unit").mkdir(parents=True)
    (repo / "docs" / "tasks").mkdir(parents=True)
    for name in ("make_packet.py", "check.py", "check_scope.py"):
        shutil.copyfile(ROOT / "scripts" / name, repo / "scripts" / name)
    shutil.copyfile(ROOT / "ruff.toml", repo / "ruff.toml")
    (repo / ".gitignore").write_text("reviews/\n", encoding="utf-8")
    (repo / "docs" / "tasks" / "B2.md").write_text(
        "# B2 fixture\n\n## Owns\n- `owned.txt`\n", encoding="utf-8",
    )
    (repo / "owned.txt").write_text("before\n", encoding="utf-8")
    if state != "empty":
        assertion = "1 == 2" if state == "failing" else "True"
        (repo / "tests" / "unit" / "test_example.py").write_text(
            f"def test_example():\n    assert {assertion}\n", encoding="utf-8",
        )
    if state == "lint":
        (repo / "bad_lint.py").write_text("import os\n", encoding="utf-8")
    git(repo, "init", "--initial-branch=dev")
    git(repo, "config", "user.name", "Integration judge")
    git(repo, "config", "user.email", "judge@example.invalid")
    git(repo, "add", ".")
    git(repo, "commit", "-m", "Tooling baseline")
    git(repo, "checkout", "-b", "int/B2")
    (repo / "owned.txt").write_text("after\n", encoding="utf-8")
    git(repo, "add", "owned.txt")
    git(repo, "commit", "-m", "Owned integration change")

    assert git(repo, "tag") == ""
    phase = run(repo, sys.executable, "scripts/make_packet.py", "phase", "0")
    assert phase.returncode == 0, phase.stdout + phase.stderr
    phase_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((repo / "reviews" / "phase-0").glob("packet-*.md"))
    )
    assert f"Compare: {EMPTY_TREE}..dev" in phase_text
    assert "diff --git a/scripts/check.py b/scripts/check.py" in phase_text
    assert "+    if code != 0:" in phase_text
    assert "if code not in (0, 5)" not in phase_text

    gate = run(repo, sys.executable, "scripts/check.py")
    assert gate.returncode == exit_code, gate.stdout + gate.stderr
    assert expected in gate.stdout
    merge = run(repo, sys.executable, "scripts/make_packet.py", "merge", "B2")
    assert merge.returncode == 0, merge.stdout + merge.stderr
    packet = (repo / "reviews" / "merge-B2" / "packet-1.md").read_text(
        encoding="utf-8",
    )
    assert "## Check output (in the worktree)" in packet
    assert expected in packet
    assert "SCOPE OK for B2" in packet
    assert "diff --git a/owned.txt b/owned.txt" in packet
    if state == "empty":
        assert "no tests ran" in packet
    if exit_code:
        assert "CHECK PASSED" not in packet
