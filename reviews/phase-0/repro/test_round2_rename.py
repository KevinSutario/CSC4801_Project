"""Round-two reproduction: a rename must check both owned paths."""

import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest


SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "check_scope.py"


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=repo, capture_output=True, text=True, check=True,
    ).stdout


@pytest.mark.parametrize("committed", [False, True], ids=["staged", "committed"])
def test_rename_from_unowned_source_is_rejected(tmp_path: Path, committed: bool) -> None:
    (tmp_path / "scripts").mkdir()
    (tmp_path / "docs" / "tasks").mkdir(parents=True)
    shutil.copyfile(SCRIPT, tmp_path / "scripts" / "check_scope.py")
    (tmp_path / "docs" / "tasks" / "B3.md").write_text(
        "# Fixture task\n\n## Owns\n- `owned-new.txt`\n", encoding="utf-8",
    )
    (tmp_path / "unowned.txt").write_text("original content\n", encoding="utf-8")
    git(tmp_path, "init", "--initial-branch=dev")
    git(tmp_path, "config", "user.name", "Judge rename fixture")
    git(tmp_path, "config", "user.email", "judge@example.invalid")
    git(tmp_path, "config", "diff.renames", "true")
    git(tmp_path, "add", ".")
    git(tmp_path, "commit", "-m", "Baseline")
    git(tmp_path, "checkout", "-b", "task/B3")
    git(tmp_path, "mv", "unowned.txt", "owned-new.txt")
    if committed:
        git(tmp_path, "commit", "-m", "Rename unowned source")
    result = subprocess.run(
        [sys.executable, "scripts/check_scope.py", "B3"],
        cwd=tmp_path, capture_output=True, text=True,
        env={**os.environ, "SCOPE_BASE": "dev"},
    )
    assert result.returncode != 0, result.stdout + result.stderr
    assert "unowned.txt" in result.stdout
