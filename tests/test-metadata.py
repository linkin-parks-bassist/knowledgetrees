#!/usr/bin/env python3
"""Checks for the current flat metadata schema and manual review time."""

import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile

KT = Path(__file__).resolve().parents[1] / "tools/kt"


def run(project, *arguments, expected=0):
    result = subprocess.run([sys.executable, str(KT), *arguments], cwd=project,
                            capture_output=True, text=True)
    assert result.returncode == expected, (arguments, result.stdout, result.stderr)
    return result


with tempfile.TemporaryDirectory() as directory:
    project = Path(directory)
    tree = project / ".knowledge"
    tree.mkdir()
    leaf = tree / "answer.md"
    leaf.write_text(
        "---\nstatus: green\nrevised_at: '2026-09-01T00:00:00+00:00'\n"
        "expires_every: '200 weeks'\n---\n\n"
        "Answer.\n\nProof: (verified at _)\n\n```bash\ntrue\n```\n"
    )
    run(project, "prove", "--local")
    revision = hashlib.sha256(leaf.read_bytes()).hexdigest()
    run(project, "rewrite", "local:answer.md", revision,
        leaf.read_text().replace("Answer.", "Revised answer."))
    assert 'status: "yellow"' in leaf.read_text()
    assert "checked_at:" not in leaf.read_text()
    revision = hashlib.sha256(leaf.read_bytes()).hexdigest()
    run(project, "check", "local:answer.md", revision)
    checked_line = next(line for line in leaf.read_text().splitlines()
                        if line.startswith("checked_at:"))
    run(project, "prove", "--local")
    assert checked_line in leaf.read_text(), "proof runs must not advance manual check time"

    flagged = tree / "flagged.md"
    flagged.write_text(
        "---\nstatus: yellow\nrevised_at: '2026-09-01T00:00:00+00:00'\n"
        "verifiable: true\n---\n\n"
        "A proved claim.\n\nProof: (verified at _)\n\n```bash\ntrue\n```\n"
    )
    revision = hashlib.sha256(flagged.read_bytes()).hexdigest()
    run(project, "rewrite", "local:flagged.md", revision,
        flagged.read_text().replace("claim.", "claim revised."))
    assert "verifiable: true" in flagged.read_text()
    run(project, "prove", "--local")
    assert "status: green" in flagged.read_text()

    invalid = tree / "invalid.md"
    invalid.write_text("---\nstatus: green\nobsolete: true\n---\n\nNeeds repair.\n")
    result = run(project, "prove", "--local", "invalid", expected=1)
    assert "brown=1" in result.stdout
    assert "status: brown" in invalid.read_text()
    revision = hashlib.sha256(invalid.read_bytes()).hexdigest()
    run(project, "rewrite", "local:invalid.md", revision, invalid.read_text(), expected=0)
    run(project, "rewrite", "local:invalid.md", revision,
        invalid.read_text().replace("Needs repair.", "Changed but still invalid."), expected=2)
    assert "obsolete: true" in invalid.read_text()

    invalid.write_text("---\nstatus: green\nchecked_at: 2026-09-19\n---\n\nUnknown check time.\n")
    result = run(project, "prove", "--local", "invalid", expected=1)
    assert "brown=1" in result.stdout

print("metadata checks passed")
