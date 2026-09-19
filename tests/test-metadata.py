#!/usr/bin/env python3
"""Regression checks for manual review timestamps and old metadata."""

import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile

KT = Path(__file__).resolve().parents[1] / "tools/kt"


with tempfile.TemporaryDirectory() as directory:
    project = Path(directory)
    tree = project / ".knowledge"
    tree.mkdir()
    leaf = tree / "legacy.md"
    leaf.write_text(
        "---\nmetadata:\n  status: unverified\n"
        "  verified_at: '2026-09-01T00:00:00+00:00'\n"
        "  expires_every: '200 weeks'\n---\nStatus: Green\n\n"
        "Old answer.\n\nProof: (verified at _)\n\n```bash\ntrue\n```\n"
    )
    result = subprocess.run([sys.executable, str(KT), "prove", "--local"],
                            cwd=project, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert "status: green" in leaf.read_text()
    assert "checked_at:" not in leaf.read_text()

    revision = hashlib.sha256(leaf.read_bytes()).hexdigest()
    revised = leaf.read_text().replace("Old answer.", "Revised answer.")
    subprocess.run([sys.executable, str(KT), "rewrite", "local:legacy.md",
                    revision, revised], cwd=project, check=True, capture_output=True)
    assert 'status: "yellow"' in leaf.read_text()
    assert "checked_at:" not in leaf.read_text()
    review_revision = hashlib.sha256(leaf.read_bytes()).hexdigest()
    subprocess.run([sys.executable, str(KT), "check", "local:legacy.md",
                    review_revision], cwd=project, check=True, capture_output=True)
    checked_line = next(line for line in leaf.read_text().splitlines()
                        if line.startswith("checked_at:"))
    subprocess.run([sys.executable, str(KT), "prove", "--local"],
                   cwd=project, check=True, capture_output=True)
    assert checked_line in leaf.read_text(), "proofs must not advance manual check time"

    flagged = tree / "flagged.md"
    flagged.write_text(
        "---\nverifiable: true\n---\n\n"
        "A fully proved claim.\n\nProof: (verified at _)\n\n```bash\ntrue\n```\n"
    )
    revision = hashlib.sha256(flagged.read_bytes()).hexdigest()
    subprocess.run([sys.executable, str(KT), "rewrite", "local:flagged.md",
                    revision, flagged.read_text().replace("claim.", "claim revised.")],
                   cwd=project, check=True, capture_output=True)
    assert "verifiable: true" in flagged.read_text()
    result = subprocess.run([sys.executable, str(KT), "prove", "--local"],
                            cwd=project, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert "status: green" in flagged.read_text()

with tempfile.TemporaryDirectory() as directory:
    project = Path(directory)
    tree = project / ".knowledge"
    tree.mkdir()
    leaf = tree / "legacy-date.md"
    leaf.write_text("---\nchecked_at: 2026-09-19\n---\n\nUnresolved questions remain.\n")
    result = subprocess.run([sys.executable, str(KT), "prove", "--local"],
                            cwd=project, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert "green=1 yellow=0 brown=0" in result.stdout
    assert "falsified_at:" not in leaf.read_text()
    leaf.write_text("---\nchecked_at: 2026-09-19\nexpires_every: 999 weeks\n---\n\nOld date.\n")
    result = subprocess.run([sys.executable, str(KT), "prove", "--local"],
                            cwd=project, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert "brown=0" in result.stdout and "falsified_at:" not in leaf.read_text()
    leaf.write_text("---\nchecked_at: unknown\nexpires_every: 2 weeks\n---\n\nNeeds review.\n")
    result = subprocess.run([sys.executable, str(KT), "prove", "--local"],
                            cwd=project, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert result.stdout == "green=0 yellow=1 brown=0\n"
    assert "falsified_at:" not in leaf.read_text()

print("metadata checks passed")
