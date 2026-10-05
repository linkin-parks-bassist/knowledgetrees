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

Proof:

```bash
true
```

The second assertion is true.

Proof:

```bash
true
```
'''
        path.parent.mkdir(parents=True)
        path.write_text(original)
        alias = base / "SKILL.md"
        os.link(path, alias)
        inode = path.stat().st_ino
        env = {**os.environ, "KT_GLOBAL_ROOT": str(base / "global"), "KT_CONFIG": str(base / "registry.json"),
               "KT_REWRITE_STATE_DIR": str(base / "state")}

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
        assert "status: brown" in updated and "revised_at:" in updated
        assert updated.count("Proof:") == 2
        assert alias.read_text() == updated and path.stat().st_ino == inode
        run("rewrite", "project:how/to/test.md", token, "stale replacement", expected=4)
        assert path.read_text() == updated
        token = run("open", "project:how/to/test.md").stderr.strip().removeprefix("Revision: ")
        no_op = run("rewrite", "project:how/to/test.md", token, body(updated))
        assert no_op.stdout == "" and no_op.stderr == "" and path.read_text() == updated
        # Proof markers are timeless; changing a predicate leaves the delimiter intact.
        revised = body(updated).replace("```bash\ntrue\n```", "```bash\nfalse\n```", 1)
        run("rewrite", "project:how/to/test.md", token, revised)
        assert path.read_text().count("Proof:") == 2
        # Rewriting does not execute or validate a newly inserted orphan marker.
        token = hashlib.sha256(path.read_bytes()).hexdigest()
        run("rewrite", "project:how/to/test.md", token,
            body(path.read_text()) + "\nProof:\n")
        assert path.read_text().count("Proof:") == 3
        # Body-only input gets current metadata on rewrite.
        bare = root / "bare.md"
        bare.write_text("Old body")
        token = run("open", "project:bare.md").stderr.strip().removeprefix("Revision: ")
        run("rewrite", "project:bare.md", token, "New body\n")
        assert 'status: green' in bare.read_text()
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
        assert 'status: brown' in path.read_text() and "revised_at:" in path.read_text()
        run("rewrite", "project:how/to/test.md", token, "stale", expected=4)
        current = path.read_text()
        token = hashlib.sha256(current.encode()).hexdigest()
        no_op = run("rewrite", "project:how/to/test.md", token, body(current))
        assert no_op.stdout == "" and no_op.stderr == ""
        reported = run("rewrite", "project:how/to/test.md", token, body(current), "--print-revision")
        assert reported.stdout == f"Revision: {token}\n" and not reported.stderr
        preview = run("rewrite", "project:how/to/test.md", token, "Preview", "--print-revision", "--dry-run")
        assert "Revision:" not in preview.stdout and path.read_text() == current
        reported = run("rewrite", "project:how/to/test.md", token, "Committed", "--print-revision")
        token = hashlib.sha256(path.read_bytes()).hexdigest()
        assert reported.stdout == f"Revision: {token}\n" and not reported.stderr
        for invalid in ("", "---\nunclosed"):
            run("rewrite", "project:how/to/test.md", token, invalid, expected=2)
        run("rewrite", "project:missing.md", token, "answer", expected=2)
        # Growth friction persists across CLI processes, but never changes a rejected leaf.
        long_leaf = root / "long.md"
        other_leaf = root / "other.md"
        def words(count, word="knowledge"):
            return " ".join([word] * count) + "\n"

        def seed(count):
            long_leaf.write_text(words(count))
            return hashlib.sha256(long_leaf.read_bytes()).hexdigest()

        def grow(token, count, expected=0, address="project:long.md", **options):
            return run("rewrite", address, token, words(count), expected=expected, **options)

        # The 500-word boundary is independent of the 1,000-word audit threshold.
        digest = seed(499)
        grow(digest, 500)
        digest = hashlib.sha256(long_leaf.read_bytes()).hexdigest()
        before = long_leaf.read_bytes()
        bounced = grow(digest, 501, expected=5)
        assert "1 of 1" in bounced.stderr and "at most 500 words" in bounced.stderr
        assert "Consider splitting independently useful content into separate leaves" in bounced.stderr
        assert "keep cohesive knowledge together" in bounced.stderr
        assert long_leaf.read_bytes() == before
        grow(digest, 501)
        digest = hashlib.sha256(long_leaf.read_bytes()).hexdigest()
        grow(digest, 502, expected=5)
        grow(digest, 500)
        digest = seed(1000)
        before = long_leaf.read_bytes()
        for _ in range(2):
            run("rewrite", "project:long.md", digest, words(1001), "--dry-run")
        bounced = grow(digest, 1001, expected=5)
        assert "1 of 2" in bounced.stderr and "frontier of knowledge" in bounced.stderr
        assert long_leaf.read_bytes() == before
        # Stale requests and unchanged no-ops do not consume the second rejection.
        grow("0" * 64, 1002, expected=4)
        grow(digest, 1000)
        assert long_leaf.read_bytes() == before
        # A hardlink alias shares the counter; another leaf does not.
        os.link(long_leaf, root / "long-alias.md")
        other_leaf.write_text(words(1000))
        other_digest = hashlib.sha256(other_leaf.read_bytes()).hexdigest()
        grow(other_digest, 1001, expected=5, address="project:other.md")
        bounced = grow(digest, 1002, expected=5, address="project:long-alias.md")
        assert "2 of 2" in bounced.stderr and long_leaf.read_bytes() == before
        grow(digest, 1002)
        assert len(body(long_leaf.read_text()).split()) == 1002
        digest = hashlib.sha256(long_leaf.read_bytes()).hexdigest()
        assert "1 of 2" in grow(digest, 1003, expected=5).stderr
        # A shorter body, still long, is accepted immediately and resets the cycle.
        grow(digest, 1001)
        digest = hashlib.sha256(long_leaf.read_bytes()).hexdigest()
        assert "1 of 2" in grow(digest, 1002, expected=5).stderr
        grow(digest, 999)
        # Changed but equal-length answers pass unless a bounce cycle is active.
        digest = seed(1500)
        run("rewrite", "project:long.md", digest, words(1500, "current"))
        digest = hashlib.sha256(long_leaf.read_bytes()).hexdigest()
        grow(digest, 1501, expected=5)
        assert "2 of 2" in grow(digest, 1500, expected=5).stderr
        grow(digest, 1500)
        # Very long proposals require three rejections; changing committed revision resets.
        digest = seed(2000)
        for attempt in range(1, 4):
            assert f"{attempt} of 3" in grow(digest, 2001, expected=5).stderr
        grow(digest, 2001)
        digest = hashlib.sha256(long_leaf.read_bytes()).hexdigest()
        grow(digest, 2002, expected=5)
        long_leaf.write_text(words(2001, "external"))
        digest = hashlib.sha256(long_leaf.read_bytes()).hexdigest()
        assert "1 of 3" in grow(digest, 2002, expected=5).stderr
        # Metadata-only changes bypass the guard and start a fresh revision.
        run("rewrite", "project:long.md", digest, words(2001, "external"), "--expires-every", "1d")
        digest = hashlib.sha256(long_leaf.read_bytes()).hexdigest()
        assert "1 of 3" in grow(digest, 2002, expected=5).stderr
        grow(digest, 1000)
        # --force copies a generated answer past the guard in one call and leaves later edits guarded.
        digest = seed(2000)
        run("rewrite", "project:long.md", digest, words(2500), "--force")
        assert len(body(long_leaf.read_text()).split()) == 2500
        digest = hashlib.sha256(long_leaf.read_bytes()).hexdigest()
        assert "1 of 3" in grow(digest, 2501, expected=5).stderr
        grow(digest, 1000)
        # Concurrent callers serialize their counters under the leaf lock.
        digest = seed(1000)
        callers = [subprocess.Popen([sys.executable, str(SCRIPT), "rewrite", "project:long.md",
                                     digest, words(1001)], cwd=base, env=env, text=True,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE) for _ in range(3)]
        results = [(caller.communicate(), caller.returncode) for caller in callers]
        assert sorted(code for _, code in results) == [0, 5, 5], results
        assert len(body(long_leaf.read_text()).split()) == 1001
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
