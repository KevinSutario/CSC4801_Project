"""Reproduction for the phase-0 gate accepting an empty test suite."""

from pathlib import Path
import shutil
import subprocess
import sys


def test_gate_fails_when_no_tests_are_collected(tmp_path: Path) -> None:
    """A present tests/unit directory with no tests must fail the gate."""
    source_root = Path(__file__).resolve().parents[2]
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    shutil.copyfile(source_root / "scripts" / "check.py", scripts / "check.py")
    shutil.copyfile(source_root / "ruff.toml", tmp_path / "ruff.toml")
    (tmp_path / "tests" / "unit").mkdir(parents=True)
    (tmp_path / "tests" / "unit" / "__init__.py").write_text("", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(scripts / "check.py")],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    output = result.stdout + result.stderr
    assert "no tests ran" in output, output
    assert result.returncode != 0, output
