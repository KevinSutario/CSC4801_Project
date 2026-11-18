"""Offline regression tests for phase review packet baselines."""

from pathlib import Path
import shutil
import subprocess
import sys

import pytest


SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "make_packet.py"
EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=repo, capture_output=True, text=True, check=True
    ).stdout


@pytest.fixture
def packet_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    (repo / "scripts").mkdir(parents=True)
    shutil.copyfile(SCRIPT, repo / "scripts" / "make_packet.py")
    git(repo, "init", "--initial-branch=dev")
    git(repo, "config", "user.name", "Packet test")
    git(repo, "config", "user.email", "packet@example.invalid")
    (repo / "README.md").write_text("Initial repository content\n", encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-m", "Initial repository")
    return repo


def run_phase(repo: Path, phase: int) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "scripts/make_packet.py", "phase", str(phase)],
        cwd=repo, capture_output=True, text=True,
    )


def test_phase_zero_without_tags_includes_whole_repository(packet_repo: Path) -> None:
    assert git(packet_repo, "tag") == ""
    result = run_phase(packet_repo, 0)
    assert result.returncode == 0, result.stderr
    packets = sorted((packet_repo / "reviews" / "phase-0").glob("packet-*.md"))
    assert packets
    text = "\n".join(packet.read_text(encoding="utf-8") for packet in packets)
    assert f"Compare: {EMPTY_TREE}..dev" in text
    assert "diff --git a/README.md b/README.md" in text
    assert "+Initial repository content" in text
    assert "diff --git a/scripts/make_packet.py b/scripts/make_packet.py" in text
    assert "new file mode" in text
    assert f"PACKET: {packets[0]}" in result.stdout
    assert f"WORKTREE: {packet_repo}" in result.stdout


def test_phase_one_compares_against_phase_zero_tag(packet_repo: Path) -> None:
    git(packet_repo, "tag", "phase-0")
    (packet_repo / "phase-one.txt").write_text("Phase one content\n", encoding="utf-8")
    git(packet_repo, "add", "phase-one.txt")
    git(packet_repo, "commit", "-m", "Phase one")
    result = run_phase(packet_repo, 1)
    assert result.returncode == 0, result.stderr
    packet = packet_repo / "reviews" / "phase-1" / "packet-1.md"
    text = packet.read_text(encoding="utf-8")
    assert "Compare: phase-0..dev" in text
    assert "+Phase one content" in text
    assert "diff --git a/README.md" not in text
    assert "diff --git a/scripts/make_packet.py" not in text


def test_phase_one_requires_phase_zero_tag(packet_repo: Path) -> None:
    result = run_phase(packet_repo, 1)
    assert result.returncode != 0
    assert "git diff phase-0..dev failed:" in result.stderr
    assert "unknown revision or path not in the working tree" in result.stderr
    assert not (packet_repo / "reviews" / "phase-1").exists()
