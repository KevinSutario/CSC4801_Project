"""Copy the Keystone agent and skill definitions into .claude/ (run once, by Kevin).

Usage: python scripts/install_claude_setup.py

Copies claude-setup/agents/*.md to .claude/agents/ and claude-setup/skills/*/SKILL.md to
.claude/skills/. Existing files with the same name are replaced; nothing else in .claude/ is touched
(your settings.local.json stays as it is).
"""

from __future__ import annotations

import os
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main() -> int:
    src_root = os.path.join(ROOT, "claude-setup")
    copied = 0
    for kind in ("agents", "skills"):
        src = os.path.join(src_root, kind)
        for dirpath, _dirs, files in os.walk(src):
            for name in files:
                rel = os.path.relpath(os.path.join(dirpath, name), src)
                dest = os.path.join(ROOT, ".claude", kind, rel)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                shutil.copyfile(os.path.join(dirpath, name), dest)
                print(f"  .claude/{kind}/{rel.replace(os.sep, '/')}")
                copied += 1
    print(f"Copied {copied} files. Restart Claude Code so it loads the new agents and skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
