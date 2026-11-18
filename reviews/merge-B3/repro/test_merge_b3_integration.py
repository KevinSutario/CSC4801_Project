"""Exercise B1 packets with B3 scope while the B2 gate remains passing."""

import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[2]


def command(repo: Path, *args: str, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=repo, env=env, text=True, capture_output=True, timeout=45)


def git(repo: Path, *args: str, env: dict[str, str]) -> str:
    result = command(repo, "git", *args, env=env)
    assert result.returncode == 0, result.stdout + result.stderr
    return result.stdout


@pytest.mark.parametrize("source,accepted", [("owned.txt", True), ("unowned.txt", False)])
def test_b1_packets_include_b3_rename_scope_and_passing_b2_gate(
    tmp_path: Path, source: str, accepted: bool,
) -> None:
    repo = tmp_path / "repo"
    (repo / "scripts").mkdir(parents=True)
    (repo / "docs" / "tasks").mkdir(parents=True)
    (repo / "docs" / "plan").mkdir(parents=True)
    for script in ("make_packet.py", "check_scope.py", "check.py"):
        shutil.copyfile(ROOT / "scripts" / script, repo / "scripts" / script)
    shutil.copytree(ROOT / "tests" / "unit", repo / "tests" / "unit")
    for name in ("pytest.ini", "ruff.toml", ".gitignore"):
        shutil.copyfile(ROOT / name, repo / name)
    shutil.copyfile(
        ROOT / "docs" / "plan" / "04-AUTH-SECURITY.md",
        repo / "docs" / "plan" / "04-AUTH-SECURITY.md",
    )
    (repo / "docs" / "tasks" / "B3.md").write_text(
        "# Integration fixture\n\n## Owns\n- `owned.txt`\n- `owned-new.txt`\n",
        encoding="utf-8",
    )
    for name in ("owned.txt", "unowned.txt"):
        (repo / name).write_text("original\n", encoding="utf-8")
    env = {**os.environ, "SCOPE_BASE": "dev", "TMPDIR": str(tmp_path)}
    git(repo, "init", "--initial-branch=dev", env=env)
    git(repo, "config", "user.name", "Merge judge", env=env)
    git(repo, "config", "user.email", "judge@example.invalid", env=env)
    git(repo, "config", "diff.renames", "true", env=env)
    git(repo, "add", ".", env=env)
    git(repo, "commit", "-m", "Fixture baseline", env=env)
    assert git(repo, "tag", env=env) == ""
    phase = command(repo, sys.executable, "scripts/make_packet.py", "phase", "0", env=env)
    assert phase.returncode == 0, phase.stdout + phase.stderr
    phase_text = "\n".join(
        packet.read_text(encoding="utf-8")
        for packet in (repo / "reviews" / "phase-0").glob("packet-*.md")
    )
    assert "Compare: 4b825dc642cb6eb9a060e54bf8d69288fbee4904..dev" in phase_text
    assert "diff --git a/scripts/check_scope.py b/scripts/check_scope.py" in phase_text

    worktree = tmp_path / "ks-int"
    git(repo, "worktree", "add", "-b", "int/B3", str(worktree), "dev", env=env)
    git(worktree, "mv", source, "owned-new.txt", env=env)
    git(worktree, "commit", "-m", "Rename fixture source", env=env)
    rename = git(worktree, "diff", "--name-status", "dev...HEAD", env=env)
    assert f"R100\t{source}\towned-new.txt" in rename
    merged = command(repo, sys.executable, "scripts/make_packet.py", "merge", "B3", env=env)
    assert merged.returncode == 0, merged.stdout + merged.stderr
    packet = (repo / "reviews" / "merge-B3" / "packet-1.md").read_text(encoding="utf-8")
    assert "All checks passed!" in packet
    assert "41 passed" in packet
    assert "CHECK PASSED" in packet
    assert "rename to owned-new.txt" in packet
    if accepted:
        assert "SCOPE OK for B3" in packet
        assert "SCOPE FAILED" not in packet
    else:
        scope_section = packet.split("## Scope check", 1)[1].split("## Security", 1)[0]
        assert "SCOPE FAILED for B3" in scope_section
        assert "  unowned.txt" in scope_section
        assert "SCOPE OK" not in scope_section
