#!/usr/bin/env python3
"""Standalone revision-checked amendment, hardlinks, review/proof invalidation."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

SCRIPT = Path(__file__).resolve().parents[1] / "tools/kt"


def main():
    with tempfile.TemporaryDirectory(prefix="kt amend ") as temporary:
        base = Path(temporary)
        root = base / ".knowledge"
        (root / "where/am").mkdir(parents=True)
        (root / "where/am/i.md").write_text("Standalone tree, no Git repository.")
        path = root / "how/to/test.md"
        original = '''---
name: test-skill
metadata:
  verified_at: yesterday
  verified_by: fixture
  verification: |
    Checked all claims.
  scope: fixture
  source: original evidence
  falsified_at: older-failure
---

The first assertion is true.

Proof: (verified at 2026-09-12T12:00:00+00:00)

```bash
true
```

The second assertion is true.

Proof: (verified at 2026-09-12T12:00:00+00:00)

```bash
true
```
'''
        path.parent.mkdir(parents=True)
        path.write_text(original)
        alias = base / "SKILL.md"
        os.link(path, alias)
        inode = path.stat().st_ino
        env = {**os.environ, "KT_GLOBAL_ROOT": str(base / "global"), "KT_CONFIG": str(base / "registry.json")}

        def run(*args, expected=0, content=None):
            result = subprocess.run([sys.executable, str(SCRIPT), *args], cwd=base, env=env,
                                    input=content, text=True, capture_output=True)
            assert result.returncode == expected, (args, result.stdout, result.stderr)
            return result

        opened = run("open", "project:how/to/test.md", "--revision")
        token = opened.stderr.strip().removeprefix("Revision: ")
        assert token == hashlib.sha256(path.read_bytes()).hexdigest()
        assert opened.stdout == original
        revised = original.replace("The second assertion is true.", "The second assertion is different.")
        revised = revised.replace("  falsified_at: older-failure\n", "")
        replacement = base / "revised.md"
        replacement.write_text(revised)
        preview = run("amend", "project:how/to/test.md", "--expect", token, "--body-file", str(replacement), "--dry-run")
        assert "second assertion is different" in preview.stdout
        assert path.read_text() == original and path.stat().st_ino == inode
        run("amend", "project:how/to/test.md", "--expect", token, "--body-file", str(replacement), "--source", "new experimental evidence")
        updated = path.read_text()
        assert "verified_at:" not in updated and "verified_by:" not in updated and "verification:" not in updated
        assert "  status: \"unverified\"" in updated and "new experimental evidence" in updated
        assert "older-failure" in updated, "sticky falsification cannot be silently cleared"
        assert updated.count("Proof: (verified at 2026-09-12T12:00:00+00:00)") == 1
        assert updated.count("Proof: (verified at _)") == 1
        assert alias.read_text() == updated and path.stat().st_ino == inode
        run("amend", "project:how/to/test.md", "--expect", token, content="stale replacement", expected=4)
        assert path.read_text() == updated
        token = run("open", "project:how/to/test.md", "--revision").stderr.strip().removeprefix("Revision: ")
        no_op = run("amend", "project:how/to/test.md", "--expect", token, content=updated)
        assert "Unchanged" in no_op.stdout and path.read_text() == updated
        # Changed predicate cannot retain an old proof stamp, even if submitted as verified.
        revised = updated.replace("```bash\ntrue\n```", "```bash\nfalse\n```", 1)
        run("amend", "project:how/to/test.md", "--expect", token, content=revised)
        assert "Proof: (verified at 2026-09-12" not in path.read_text()
        # Newly inserted orphan proof markers must not carry caller-invented verification.
        token = hashlib.sha256(path.read_bytes()).hexdigest()
        run("amend", "project:how/to/test.md", "--expect", token,
            content=path.read_text() + "\nProof: (verified at 2030-01-01T00:00:00+00:00)\n")
        assert "2030-01-01" not in path.read_text()
        # Body-only standalone leaves get unverified metadata.
        bare = root / "bare.md"
        bare.write_text("Old body")
        token = run("open", "project:bare.md", "--revision").stderr.strip().removeprefix("Revision: ")
        run("amend", "project:bare.md", "--expect", token, content="New body\n")
        assert 'status: "unverified"' in bare.read_text()
        assert "New body" in bare.read_text()
        fresh = hashlib.sha256(bare.read_bytes()).hexdigest()
        for invalid in ("", "---\nunclosed", "invalid\x00body"):
            run("amend", "project:bare.md", "--expect", fresh, content=invalid, expected=2)
        run("amend", "project:bare.md", "--expect", "bad", content="body", expected=2)
        # Inline replacement needs neither a prior revision call nor stdin/file input.
        run("rewrite", "project:how/to/test.md", "Inline answer\nwith multiple lines", "--dry-run")
        before = path.read_text()
        rewritten = run("rewrite", "project:how/to/test.md", "Inline answer\nwith multiple lines", "--source", "inline evidence")
        assert before in rewritten.stdout
        assert "superseded contents; no longer current knowledge" in rewritten.stdout
        assert "rewrite again to add it back if so" in rewritten.stdout
        assert "Inline answer\nwith multiple lines" not in rewritten.stdout
        assert "Rewritten" in rewritten.stdout
        assert path.stat().st_ino == inode and alias.read_text() == path.read_text()
        assert "Inline answer\nwith multiple lines" in path.read_text()
        assert "older-failure" in path.read_text() and "inline evidence" in path.read_text()
        run("rewrite", "project:how/to/test.md", "stale", "--expect", hashlib.sha256(before.encode()).hexdigest(), expected=4)
        current = path.read_text()
        no_op = run("rewrite", "project:how/to/test.md", current)
        assert "Unchanged" in no_op.stdout and current in no_op.stdout
        assert "unchanged current contents" in no_op.stdout
        conflict = run("rewrite", "project:how/to/test.md", "stale", "--expect", "0" * 64, expected=4)
        assert "BEGIN ORIGINAL" not in conflict.stdout
        for invalid in ("", "---\nunclosed"):
            run("rewrite", "project:how/to/test.md", invalid, expected=2)
        run("rewrite", "project:missing.md", "answer", expected=2)
        # Symlink aliases cannot be used for mutation; denied roots stay denied.
        (root / "alias.md").symlink_to(bare)
        run("amend", "project:alias.md", "--expect", fresh, content="body", expected=2)
        run("rewrite", "project:alias.md", "body", expected=2)
        config = {"roots": {"blocked": {"path": str(root), "access": "deny"}}}
        Path(env["KT_CONFIG"]).write_text(json.dumps(config))
        run("open", "project:bare.md", "--revision", expected=3)
        run("amend", "project:bare.md", "--expect", fresh, content="body", expected=3)
        run("rewrite", "project:bare.md", "body", expected=3)
        assert "New body" in bare.read_text()
    print("amendment integration checks passed")


if __name__ == "__main__":
    main()
