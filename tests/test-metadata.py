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
        "Answer.\n\nProof:\n\n```bash\ntrue\n```\n"
    )
    run(project, "prove", "--local")
    revision = hashlib.sha256(leaf.read_bytes()).hexdigest()
    run(project, "rewrite", "local:answer.md", revision,
        "Revised answer.\n\nProof:\n\n```bash\ntrue\n```\n")
    assert 'revised_at: "20' in leaf.read_text() and 'status: "yellow"' in leaf.read_text(), "a rewrite keeps the status it had (unanchored expiry made this yellow)"
    assert "checked_at:" not in leaf.read_text()
    revision = hashlib.sha256(leaf.read_bytes()).hexdigest()
    run(project, "renew", "local:answer.md", revision)
    checked_line = next(line for line in leaf.read_text().splitlines()
                        if line.startswith("checked_at:"))
    run(project, "prove", "--local")
    assert checked_line in leaf.read_text(), "proof runs must not advance manual check time"
    revision = hashlib.sha256(leaf.read_bytes()).hexdigest()
    run(project, "rewrite", "local:answer.md", revision,
        "Revised answer.\n\nProof:\n\n```bash\ntrue\n```\n",
        "--expires-every", "3 weeks")
    assert "checked_at:" in leaf.read_text(), "setting a freshness window starts its clock"
    assert 'expires_every: "3 weeks"' in leaf.read_text()

    flagged = tree / "flagged.md"
    flagged.write_text(
        "---\nstatus: yellow\nrevised_at: '2026-09-01T00:00:00+00:00'\n"
        "verifiable: true\n---\n\n"
        "A proved claim.\n\nProof:\n\n```bash\ntrue\n```\n"
    )
    revision = hashlib.sha256(flagged.read_bytes()).hexdigest()
    run(project, "rewrite", "local:flagged.md", revision,
        "A proved claim revised.\n\nProof:\n\n```bash\ntrue\n```\n")
    assert 'verifiable: "true"' in flagged.read_text()
    run(project, "prove", "--local")
    assert "status: green" in flagged.read_text()

    invalid = tree / "invalid.md"
    invalid.write_text("---\nstatus: green\nobsolete: true\n---\n\nNeeds repair.\n")
    result = run(project, "prove", "--local", "invalid", expected=1)
    assert "1 brown" in result.stdout
    assert "status: brown" in invalid.read_text()
    revision = hashlib.sha256(invalid.read_bytes()).hexdigest()
    run(project, "rewrite", "local:invalid.md", revision,
        "Changed but still invalid.", expected=2)
    assert "obsolete: true" in invalid.read_text()

    run(project, "add", "what is expiry example", "A changing answer.",
        "--local", "--expires-every", "2 weeks")
    expiry = tree / "what/is/expiry/example.md"
    assert "expires_every: \"2 weeks\"" in expiry.read_text()
    revision = hashlib.sha256(expiry.read_bytes()).hexdigest()
    run(project, "rewrite", "local:what/is/expiry/example.md", revision,
        "A changing answer.", "--expires-at", "2026-12-01T12:00:00+11:00")
    assert "expires_at:" in expiry.read_text() and "expires_every:" not in expiry.read_text()
    revision = hashlib.sha256(expiry.read_bytes()).hexdigest()
    run(project, "rewrite", "local:what/is/expiry/example.md", revision,
        "A changing answer.", "--no-expiry")
    assert "expires_at:" not in expiry.read_text()
    run(project, "add", "what is proof covered example",
        "A checked fact.\n\nProof:\n\n```bash\ntrue\n```",
        "--local", "--verifiable")
    covered = tree / "what/is/proof/covered/example.md"
    assert "verifiable: \"true\"" in covered.read_text()
    run(project, "prove", "--local", "covered")
    assert "status: green" in covered.read_text()
    revision = hashlib.sha256(covered.read_bytes()).hexdigest()
    run(project, "rewrite", "local:what/is/proof/covered/example.md", revision,
        "A checked fact.\n\nProof:\n\n```bash\ntrue\n```", "--no-verifiable")
    assert "verifiable:" not in covered.read_text()
    run(project, "add", "what is invalid expiry", "Body.", "--local",
        "--expires-at", "2026-09-19", expected=2)
    run(project, "add", "what is unproved", "No proof.", "--local",
        "--verifiable", expected=2)

    invalid.write_text("---\nstatus: green\nchecked_at: 2026-09-19\n---\n\nUnknown check time.\n")
    result = run(project, "prove", "--local", "invalid", expected=1)
    assert "1 brown" in result.stdout

print("metadata checks passed")

# Lean output hides bookkeeping and flags only non-green leaves; renew confirms and re-greens at once.
with tempfile.TemporaryDirectory() as directory:
    project = Path(directory)
    tree = project / ".knowledge/what/is"
    tree.mkdir(parents=True)
    stale = tree / "stale.md"
    stale.write_text("---\nstatus: green\nrevised_at: '2026-01-01T00:00:00+00:00'\n"
                     "expires_at: '2026-02-01T00:00:00+00:00'\n---\n\nA fact.\n")
    (tree / "fresh.md").write_text("A fresh fact.\n")
    lean = run(project, "--lean", "open", "local:what/is/stale.md")
    assert lean.stdout.startswith("kt: yellow leaf local:what/is/stale.md is due for re-verification")
    assert "kt_renew" in lean.stdout and lean.stdout.endswith("\n\nA fact.\n") and "revised_at" not in lean.stdout
    assert run(project, "--lean", "open", "local:what/is/fresh.md").stdout == "A fresh fact.\n"
    assert run(project, "open", "local:what/is/stale.md").stdout.startswith("---\nstatus: green")
    exact = run(project, "--lean", "what", "is", "fresh")
    assert exact.stdout == "A fresh fact.\n" and "kt: exact local:what/is/fresh.md\n" in exact.stderr
    assert "check relevant proofs" not in exact.stderr
    found = run(project, "--lean", "find", "fact").stdout
    assert "local:what/is/stale.md\tcoverage=" in found and "\tyellow\t" in found and "green" not in found
    revision = hashlib.sha256(stale.read_bytes()).hexdigest()
    run(project, "renew", "local:what/is/stale.md", "0" * 64, expected=4)
    run(project, "renew", "local:what/is/stale.md", revision)
    assert "checked_at:" in stale.read_text() and "status: green" in stale.read_text()
    assert run(project, "--lean", "open", "local:what/is/stale.md").stdout == "A fact.\n"
    assert "yellow=0" in run(project, "status").stdout

    broken = tree / "broken.md"
    broken.write_text("Claim.\n\nProof:\n\n```bash\nfalse\n```\n")
    revision = hashlib.sha256(broken.read_bytes()).hexdigest()
    result = run(project, "renew", "local:what/is/broken.md", revision, expected=1)
    assert "still brown" in result.stderr and "status: brown" in broken.read_text()
    brown_notice = run(project, "--lean", "open", "local:what/is/broken.md").stdout
    assert brown_notice.startswith("kt: BROWN leaf")
    assert "STOP: report it to the user" in brown_notice and "before other work" in brown_notice

print("lean output and renew checks passed")

# Status moves down by itself (expiry, failed proofs) and up only by hand, except for verifiable leaves.
with tempfile.TemporaryDirectory() as directory:
    project = Path(directory)
    tree = project / ".knowledge/what/is"
    tree.mkdir(parents=True)
    run(project, "add", "what is new", "A new answer.", "--local")
    new = tree / "new.md"
    assert 'status: "green"' in new.read_text() and "checked_at" not in new.read_text(), "a new leaf starts green"
    run(project, "add", "what is timed", "A timed answer.", "--local", "--expires-every", "2 weeks")
    timed = tree / "timed.md"
    assert 'status: "green"' in timed.read_text() and "checked_at:" in timed.read_text(), "a recurring window starts its clock"

    revision = hashlib.sha256(new.read_bytes()).hexdigest()
    run(project, "rewrite", "local:what/is/new.md", revision, "A revised answer.")
    assert 'status: "green"' in new.read_text() and "A revised answer." in new.read_text(), "an edit keeps the status"

    marked = tree / "marked.md"
    marked.write_text("---\nstatus: yellow\nrevised_at: '2026-09-01T00:00:00+00:00'\n---\n\nAwaiting review.\n")
    run(project, "prove", "--local")
    assert "status: yellow" in marked.read_text(), "prove never raises a status"
    revision = hashlib.sha256(marked.read_bytes()).hexdigest()
    run(project, "rewrite", "local:what/is/marked.md", revision, "Still awaiting review.")
    assert 'status: "yellow"' in marked.read_text(), "an edit does not clear a yellow mark either"
    run(project, "prove", "--local")
    assert "status: yellow" in marked.read_text()
    revision = hashlib.sha256(marked.read_bytes()).hexdigest()
    run(project, "renew", "local:what/is/marked.md", revision)
    assert "status: green" in marked.read_text() and "checked_at:" in marked.read_text(), "renew is the manual way up"

    brown = tree / "brown.md"
    brown.write_text("---\nstatus: brown\nrevised_at: '2026-09-01T00:00:00+00:00'\n---\n\nFalsified.\n")
    revision = hashlib.sha256(brown.read_bytes()).hexdigest()
    run(project, "rewrite", "local:what/is/brown.md", revision, "Repaired but unreviewed.")
    run(project, "prove", "--local", expected=1)
    assert 'status: "brown"' in brown.read_text() or "status: brown" in brown.read_text(), "only review clears brown"

    proved = tree / "proved.md"
    proved.write_text("---\nstatus: yellow\nrevised_at: '2026-09-01T00:00:00+00:00'\nverifiable: true\n---\n\n"
                      "A proved claim.\n\nProof:\n\n```bash\ntrue\n```\n")
    run(project, "prove", "--local", expected=1)  # brown.md is still brown
    assert "status: green" in proved.read_text(), "a verifiable leaf whose proofs all pass is raised by prove"

    first = tree / "first.md"
    second = tree / "second.md"
    first.write_text("---\nstatus: green\nrevised_at: '2026-09-01T00:00:00+00:00'\n---\n\nOne.\n")
    second.write_text("---\nstatus: yellow\nrevised_at: '2026-09-01T00:00:00+00:00'\n---\n\nTwo.\n")
    run(project, "combine", "local:what/is/first.md", "local:what/is/second.md", "-o", "local:what/is/both.md")
    assert 'status: "yellow"' in (tree / "both.md").read_text(), "a combined leaf is as unverified as its worst source"

print("lifecycle checks passed")
