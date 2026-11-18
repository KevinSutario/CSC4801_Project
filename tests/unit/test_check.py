"""CLI regression tests for the development gate."""

from pathlib import Path
import shutil
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def gate_repo(tmp_path: Path) -> Path:
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    shutil.copyfile(ROOT / "scripts" / "check.py", scripts / "check.py")
    shutil.copyfile(ROOT / "ruff.toml", tmp_path / "ruff.toml")
    (tmp_path / "tests" / "unit").mkdir(parents=True)
    return tmp_path


def run_gate(repo: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(repo / "scripts" / "check.py")],
        cwd=repo, capture_output=True, text=True, timeout=15,
    )


def write_test(repo: Path, assertion: str) -> None:
    (repo / "tests" / "unit" / "test_example.py").write_text(
        f"def test_example():\n    assert {assertion}\n", encoding="utf-8",
    )


def test_gate_fails_when_no_tests_are_collected(gate_repo: Path) -> None:
    result = run_gate(gate_repo)
    output = result.stdout + result.stderr
    assert "no tests ran" in output, output
    assert result.returncode != 0, output
    assert "CHECK FAILED: tests" in output, output
    assert "CHECK PASSED" not in output, output


def test_gate_passes_with_clean_lint_and_passing_test(gate_repo: Path) -> None:
    write_test(gate_repo, "True")
    result = run_gate(gate_repo)
    output = result.stdout + result.stderr
    assert result.returncode == 0, output
    assert "All checks passed!" in output, output
    assert "1 passed" in output, output
    assert "CHECK PASSED" in output, output


def test_gate_fails_when_lint_fails(gate_repo: Path) -> None:
    write_test(gate_repo, "True")
    (gate_repo / "bad_lint.py").write_text("import os\n", encoding="utf-8")
    result = run_gate(gate_repo)
    output = result.stdout + result.stderr
    assert result.returncode != 0, output
    assert "F401" in output, output
    assert "1 passed" in output, output
    assert "CHECK FAILED: lint" in output, output
    assert "CHECK PASSED" not in output, output


def test_gate_fails_when_a_test_fails(gate_repo: Path) -> None:
    write_test(gate_repo, "1 == 2")
    result = run_gate(gate_repo)
    output = result.stdout + result.stderr
    assert result.returncode != 0, output
    assert "All checks passed!" in output, output
    assert "1 failed" in output, output
    assert "CHECK FAILED: tests" in output, output
    assert "CHECK PASSED" not in output, output
