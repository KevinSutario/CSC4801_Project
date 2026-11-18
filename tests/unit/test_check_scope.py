"""CLI regression tests for task ownership enforcement."""

import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest


SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "check_scope.py"


def git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, check=True)


@pytest.fixture
def scope_repo(tmp_path: Path) -> Path:
    (tmp_path / "scripts").mkdir()
    (tmp_path / "docs" / "tasks").mkdir(parents=True)
    shutil.copyfile(SCRIPT, tmp_path / "scripts" / "check_scope.py")
    (tmp_path / "docs" / "tasks" / "B2.md").write_text(
        "# Fixture task\n\n## Owns\n- `owned.txt`\n- `owned-new.txt`\n", encoding="utf-8",
    )
    for name in ("owned.txt", "unowned.txt"):
        (tmp_path / name).write_text("original\n", encoding="utf-8")
    git(tmp_path, "init", "--initial-branch=dev")
    git(tmp_path, "config", "user.name", "Scope test")
    git(tmp_path, "config", "user.email", "scope@example.invalid")
    git(tmp_path, "config", "diff.renames", "true")
    git(tmp_path, "add", ".")
    git(tmp_path, "commit", "-m", "Fixture baseline")
    git(tmp_path, "checkout", "-b", "task/B2")
    return tmp_path


def change_file(repo: Path, name: str, state: str) -> str:
    if state == "untracked":
        name = name.replace(".txt", "-new.txt")
    (repo / name).write_text("changed\n", encoding="utf-8")
    if state in ("staged", "committed"):
        git(repo, "add", name)
    if state == "committed":
        git(repo, "commit", "-m", "Change fixture file")
    return name


def run_scope(repo: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "scripts/check_scope.py", "B2"],
        cwd=repo, capture_output=True, text=True,
        env={**os.environ, "SCOPE_BASE": "dev"}, timeout=15,
    )


@pytest.mark.parametrize("state", ["unstaged", "staged", "committed", "untracked"])
def test_scope_accepts_owned_changes(scope_repo: Path, state: str) -> None:
    change_file(scope_repo, "owned.txt", state)
    result = run_scope(scope_repo)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "SCOPE OK for B2" in result.stdout


@pytest.mark.parametrize("state", ["unstaged", "staged", "committed", "untracked"])
def test_scope_rejects_unowned_changes(scope_repo: Path, state: str) -> None:
    name = change_file(scope_repo, "unowned.txt", state)
    result = run_scope(scope_repo)
    assert result.returncode != 0, result.stdout + result.stderr
    assert "SCOPE FAILED for B2" in result.stdout
    assert name in result.stdout
    assert "SCOPE OK" not in result.stdout


@pytest.mark.parametrize("state", ["unstaged", "staged", "committed"])
@pytest.mark.parametrize("source,destination,outside", [
    ("unowned.txt", "owned-new.txt", "unowned.txt"),
    ("owned.txt", "owned-new.txt", None),
    ("owned.txt", "unowned-new.txt", "unowned-new.txt"),
])
def test_scope_checks_both_rename_paths(
    scope_repo: Path, state: str, source: str, destination: str, outside: str | None,
) -> None:
    if state == "unstaged":
        (scope_repo / source).rename(scope_repo / destination)
        git(scope_repo, "add", "--intent-to-add", destination)
    else:
        git(scope_repo, "mv", source, destination)
        if state == "committed":
            git(scope_repo, "commit", "-m", "Rename fixture file")
    diff_args = {"committed": ["dev...HEAD"], "staged": ["--cached"], "unstaged": []}[state]
    diff = subprocess.run(
        ["git", "diff", "--name-status", *diff_args], cwd=scope_repo,
        capture_output=True, text=True, check=True,
    )
    assert f"R100\t{source}\t{destination}" in diff.stdout
    result = run_scope(scope_repo)
    if outside is None:
        assert result.returncode == 0, result.stdout + result.stderr
        assert "SCOPE OK for B2" in result.stdout
    else:
        assert result.returncode != 0, result.stdout + result.stderr
        assert "SCOPE FAILED for B2" in result.stdout
        assert outside in result.stdout
        assert "SCOPE OK" not in result.stdout
