#!/usr/bin/env python3
"""Integration checks for per-proof verification timestamps."""

from datetime import datetime
import os
from pathlib import Path
import subprocess
import tempfile

TOOLS = Path(__file__).resolve().parents[1] / "tools"
COMMAND = [str(TOOLS / "kt"), "prove"]


def run(root, *arguments, expected=0):
    result = subprocess.run([*COMMAND, "--root", str(root), *arguments],
                            capture_output=True, text=True, cwd=root.parent,
                            env={**os.environ, "KT_CONFIG": str(root.parent / "access.json")})
    assert result.returncode == expected, (result.stdout, result.stderr)


with tempfile.TemporaryDirectory(prefix="proof-stamp-test-") as temporary:
    root = Path(temporary) / ".knowledge"
    root.mkdir()
    leaf = root / "fact.md"
    original = ("---\nverified_at: '2000-01-01T00:00:00+00:00'\n---\n\n"
                "A passing assertion.\n\nProof:\n\n```bash\ntest 1 -eq 1\n```\n\n"
                "A failing assertion.\n\nProof: (verified at _)\n\n```bash\nfalse\n```\n")
    leaf.write_text(original)
    linked = Path(temporary) / "SKILL.md"
    os.link(leaf, linked)
    run(root, "--no-stamp", expected=1)
    assert leaf.read_text() == original
    run(root, expected=1)
    updated = leaf.read_text()
    marker = next(line for line in updated.splitlines() if line.startswith("Proof:"))
    timestamp = marker.removeprefix("Proof: (verified at ").removesuffix(")")
    assert datetime.fromisoformat(timestamp).utcoffset() is not None
    assert "verified_at: '2000-01-01T00:00:00+00:00'" in updated
    assert "Proof: (falsified at " in updated
    assert "falsified_at: '" in updated
    assert linked.read_text() == updated and linked.samefile(leaf)
    leaf.write_text(updated.replace("false", "test 2 -eq 2"))
    run(root, expected=1)
    assert "Proof: (verified at _)" not in leaf.read_text()
    assert "Proof: (falsified at " not in leaf.read_text()
    assert "falsified_at: '" in leaf.read_text(), "passing proofs cannot validate a leaf"
    run(root, "--no-stamp", expected=1)
    leaf.write_text("\n".join(line for line in leaf.read_text().splitlines()
                              if not line.startswith("falsified_at:")) + "\n")
    run(root)
    leaf.write_text("Malformed.\n\nProof: (verified at yesterday)\n\n```bash\ntrue\n```\n")
    malformed = leaf.read_text()
    run(root, expected=1)
    assert "falsified_at:" in leaf.read_text()
    assert "Proof: (verified at yesterday)" in leaf.read_text()
    leaf.write_text("Instructions only.\n\n```bash\ntrue\n```\n")
    unproved = leaf.read_text()
    run(root)
    assert leaf.read_text() == unproved
    leaf.write_text("---\nname: test\nmetadata:\n  verified_at: '2000-01-01T00:00:00+00:00'\n---\n\nBad.\n\nProof: (falsified at _)\n\n```bash\nfalse\n```\n")
    run(root, expected=1)
    assert "metadata:\n  falsified_at:" in leaf.read_text()
    assert "  verified_at: '2000-01-01T00:00:00+00:00'" in leaf.read_text()
    leaf.write_text("Bad.\n\nProof:\n\n```bash\nfalse\n```\n")
    run(root, expected=1)
    assert leaf.read_text().startswith("---\nfalsified_at:")

print("proof timestamp integration checks passed")
