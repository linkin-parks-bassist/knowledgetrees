#!/usr/bin/env python3
"""Standalone revision-checked rewrite, hardlinks, review/proof invalidation."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

SCRIPT = Path(__file__).resolve().parents[1] / "tools/kt"


def body(text):
    match = re.match(r"\A---\n.*?\n---\n", text, re.S)
    return text[match.end():].lstrip("\n") if match else text


def main():
    with tempfile.TemporaryDirectory(prefix="kt rewrite ") as temporary:
        base = Path(temporary)
        root = base / ".knowledge"
        (root / "where/am").mkdir(parents=True)
        (root / "where/am/i.md").write_text("Standalone tree, no Git repository.")
        path = root / "how/to/test.md"
        original = '''---
status: brown
revised_at: '2026-09-12T12:00:00+00:00'
name: test-skill
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

        opened = run("open", "project:how/to/test.md")
        token = opened.stderr.strip().removeprefix("Revision: ")
        assert token == hashlib.sha256(path.read_bytes()).hexdigest()
        assert opened.stdout == original
        revised = body(original).replace("The second assertion is true.", "The second assertion is different.")
        preview = run("rewrite", "project:how/to/test.md", token, revised, "--dry-run")
        assert "second assertion is different" in preview.stdout
        assert path.read_text() == original and path.stat().st_ino == inode
        run("rewrite", "project:how/to/test.md", token, revised)
        updated = path.read_text()
        assert "status: \"brown\"" in updated and "revised_at:" in updated
        assert updated.count("Proof: (verified at 2026-09-12T12:00:00+00:00)") == 1
        assert updated.count("Proof: (verified at _)") == 1
        assert alias.read_text() == updated and path.stat().st_ino == inode
        run("rewrite", "project:how/to/test.md", token, "stale replacement", expected=4)
        assert path.read_text() == updated
        token = run("open", "project:how/to/test.md").stderr.strip().removeprefix("Revision: ")
        no_op = run("rewrite", "project:how/to/test.md", token, body(updated))
        assert no_op.stdout == "" and no_op.stderr == "" and path.read_text() == updated
        # Changed predicate cannot retain an old proof stamp, even if submitted as verified.
        revised = body(updated).replace("```bash\ntrue\n```", "```bash\nfalse\n```", 1)
        run("rewrite", "project:how/to/test.md", token, revised)
        assert "Proof: (verified at 2026-09-12" not in path.read_text()
        # Newly inserted orphan proof markers must not carry caller-invented verification.
        token = hashlib.sha256(path.read_bytes()).hexdigest()
        run("rewrite", "project:how/to/test.md", token,
            body(path.read_text()) + "\nProof: (verified at 2030-01-01T00:00:00+00:00)\n")
        assert "2030-01-01" not in path.read_text()
        # Body-only input gets current metadata on rewrite.
        bare = root / "bare.md"
        bare.write_text("Old body")
        token = run("open", "project:bare.md").stderr.strip().removeprefix("Revision: ")
        run("rewrite", "project:bare.md", token, "New body\n")
        assert 'status: "green"' in bare.read_text()
        assert "New body" in bare.read_text()
        fresh = hashlib.sha256(bare.read_bytes()).hexdigest()
        for invalid in ("", "---\nunclosed"):
            run("rewrite", "project:bare.md", fresh, invalid, expected=2)
        run("rewrite", "project:bare.md", "bad", "body", expected=2)
        # Ordinary reads automatically carry the revision; rewrite requires it positionally.
        opened = run("open", "project:how/to/test.md")
        token = opened.stderr.strip().removeprefix("Revision: ")
        before = path.read_text()
        assert token == hashlib.sha256(before.encode()).hexdigest()
        run("rewrite", "project:how/to/test.md", "answer", expected=2)
        run("rewrite", "project:how/to/test.md", "bad", "answer", expected=2)
        run("rewrite", "project:how/to/test.md", token, "Inline answer\nwith multiple lines", "--dry-run")
        assert path.read_text() == before
        rewritten = run("rewrite", "project:how/to/test.md", token, "Inline answer\nwith multiple lines")
        assert rewritten.stdout == ""
        assert rewritten.stderr == ""
        assert path.stat().st_ino == inode and alias.read_text() == path.read_text()
        assert "Inline answer\nwith multiple lines" in path.read_text()
        assert 'status: "brown"' in path.read_text() and "revised_at:" in path.read_text()
        run("rewrite", "project:how/to/test.md", token, "stale", expected=4)
        current = path.read_text()
        token = hashlib.sha256(current.encode()).hexdigest()
        no_op = run("rewrite", "project:how/to/test.md", token, body(current))
        assert no_op.stdout == "" and no_op.stderr == ""
        for invalid in ("", "---\nunclosed"):
            run("rewrite", "project:how/to/test.md", token, invalid, expected=2)
        run("rewrite", "project:missing.md", token, "answer", expected=2)
        # Symlink aliases cannot be used for mutation; denied roots stay denied.
        (root / "alias.md").symlink_to(bare)
        run("rewrite", "project:alias.md", fresh, "body", expected=2)
        config = {"roots": {"blocked": {"path": str(root), "access": "deny"}}}
        Path(env["KT_CONFIG"]).write_text(json.dumps(config))
        run("open", "project:bare.md", expected=3)
        run("rewrite", "project:bare.md", fresh, "body", expected=3)
        assert "New body" in bare.read_text()
    print("rewrite integration checks passed")


if __name__ == "__main__":
    main()
