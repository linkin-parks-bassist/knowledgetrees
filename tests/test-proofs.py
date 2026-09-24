#!/usr/bin/env python3
"""Integration checks for timeless proof markers and leaf lifecycle status."""

import hashlib
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
    return result


with tempfile.TemporaryDirectory(prefix="proof-marker-test-") as temporary:
    root = Path(temporary) / ".knowledge"
    root.mkdir()
    leaf = root / "fact.md"
    original = ("---\nstatus: green\nrevised_at: '2026-09-12T12:00:00+00:00'\n"
                "checked_at: '2000-01-01T00:00:00+00:00'\n"
                "expires_at: '2099-01-01T00:00:00+00:00'\n---\n\n"
                "A passing assertion.\n\nProof:\n\n```bash\ntest 1 -eq 1\n```\n\n"
                "A failing assertion.\n\nProof:\n\n```bash\nfalse\n```\n")
    leaf.write_text(original)
    linked = Path(temporary) / "SKILL.md"
    os.link(leaf, linked)

    run(root, "--no-stamp", expected=1)
    assert leaf.read_text() == original
    run(root, expected=1)
    updated = leaf.read_text()
    assert updated.count("\nProof:\n") == 2
    assert "checked_at: '2000-01-01T00:00:00+00:00'" in updated
    assert "status: brown" in updated
    assert linked.read_text() == updated and linked.samefile(leaf)
    stable_mtime = leaf.stat().st_mtime_ns
    run(root, expected=1)
    assert leaf.read_text() == updated and leaf.stat().st_mtime_ns == stable_mtime

    legacy = ("Legacy assertions.\n\nProof: (verified at _)\n\n```bash\ntrue\n```\n\n"
              "Another legacy assertion.\n\n"
              "Proof: (verified at 2026-09-12T12:00:00+00:00)\n\n"
              "```bash\ntrue\n```\n\nA formerly failing legacy assertion.\n\n"
              "Proof: (falsified at 2026-09-12T12:00:00+00:00)\n\n"
              "```bash\ntrue\n```\n")
    leaf.write_text(legacy)
    run(root, "--no-stamp")
    assert leaf.read_text() == legacy, "read-only proving must not migrate legacy markers"
    run(root)
    migrated = leaf.read_text()
    assert migrated.count("\nProof:\n") == 3
    assert "verified at" not in migrated and "falsified at" not in migrated

    leaf.write_text(updated.replace("false", "test 2 -eq 2"))
    run(root, expected=1)
    assert leaf.read_text().count("\nProof:\n") == 2
    assert "status: brown" in leaf.read_text(), "passing proofs cannot validate an unflagged leaf"
    reviewed = subprocess.run([str(TOOLS / "kt"), "renew", str(leaf),
                              hashlib.sha256(leaf.read_bytes()).hexdigest()],
                             capture_output=True, text=True, cwd=root.parent)
    assert reviewed.returncode == 0, reviewed.stderr
    run(root)
    assert "status: green" in leaf.read_text()

    leaf.write_text("Malformed.\n\nProof: decorated\n\n```bash\ntrue\n```\n")
    run(root, expected=1)
    assert "status: brown" in leaf.read_text()
    assert "Proof: decorated" in leaf.read_text()

    leaf.write_text("Instructions only.\n\n```bash\ntrue\n```\n")
    unproved = leaf.read_text()
    run(root)
    assert "status: green" in leaf.read_text() and unproved in leaf.read_text()

    leaf.write_text("---\nstatus: green\nrevised_at: '2026-09-12T12:00:00+00:00'\nname: test\n---\n\nBad.\n\nProof:\n\n```bash\nfalse\n```\n")
    run(root, expected=1)
    assert "status: brown" in leaf.read_text()

    leaf.write_text(
        "---\nstatus: brown\nrevised_at: '2026-09-12T12:00:00+00:00'\nverifiable: true\n---\n\n"
        "A fully proved concrete fact.\n\nProof:\n\n```bash\ntest 3 -eq 3\n```\n")
    run(root)
    verified = leaf.read_text()
    assert "checked_at:" not in verified
    assert verified.count("\nProof:\n") == 1
    assert "status: green" in verified
    stable = leaf.read_text()
    stable_mtime = leaf.stat().st_mtime_ns
    run(root)
    assert leaf.read_text() == stable
    assert leaf.stat().st_mtime_ns == stable_mtime, "unchanged evaluation must not write"

    leaf.write_text(
        "---\nverifiable: true\nstatus: yellow\n"
        "expires_at: '2000-01-01T00:00:00+00:00'\n---\n\n"
        "The complete claim is proved.\n\nProof:\n\n```bash\ntest 4 -eq 4\n```\n")
    run(root)
    assert "status: green" in leaf.read_text() and "checked_at:" not in leaf.read_text()
    leaf.write_text(leaf.read_text().replace("test 4 -eq 4", "false"))
    run(root, expected=1)
    assert "status: brown" in leaf.read_text()
    leaf.write_text(leaf.read_text().replace("false", "test 4 -eq 4"))
    run(root)
    assert "status: green" in leaf.read_text()

    leaf.write_text("---\nverifiable: true\n---\n\nClaim without a proof.\n")
    run(root, expected=1)
    assert "status: brown" in leaf.read_text()

    leaf.write_text("---\nverifiable: perhaps\n---\n\nClaim.\n\nProof:\n\n```bash\ntrue\n```\n")
    run(root, expected=1)
    assert "status: brown" in leaf.read_text()

with tempfile.TemporaryDirectory(prefix="leaf-state-test-") as temporary:
    root = Path(temporary) / ".knowledge"
    root.mkdir()
    (root / "green.md").write_text(
        "---\nstatus: green\nrevised_at: '2026-09-17T00:00:00+10:00'\nchecked_at: '2026-09-17T00:00:00+10:00'\nexpires_every: '2 weeks'\n---\n\nCurrent.\n")
    (root / "expired.md").write_text(
        "---\nstatus: green\nrevised_at: '2026-08-01T00:00:00+10:00'\nchecked_at: '2026-08-01T00:00:00+10:00'\nexpires_every: 'two weeks'\n---\n\nOld.\n")
    (root / "default-green.md").write_text("A non-verifiable plan is green by default.\n")
    (root / "explicit-yellow.md").write_text("---\nstatus: yellow\nexpires_every: '2 weeks'\n---\n\nNeeds review.\n")
    result = run(root, "--no-stamp")
    assert result.stdout == ("Leaves: 4 total · 2 green · 2 yellow · 0 brown\n"
                             "Proofs: 0 total · 0 valid · 0 failed · SUCCESS\n")
    assert "yellow local:" not in result.stderr
    run(root)
    assert "status: green" in (root / "green.md").read_text()
    assert (root / "default-green.md").read_text().startswith("---\nstatus: green")
    assert "status: yellow" in (root / "expired.md").read_text()
    assert "status: yellow" in (root / "explicit-yellow.md").read_text()

    expired = root / "expired.md"
    reviewed = subprocess.run([str(TOOLS / "kt"), "renew", str(expired),
                              hashlib.sha256(expired.read_bytes()).hexdigest()],
                             capture_output=True, text=True, cwd=root.parent)
    assert reviewed.returncode == 0, reviewed.stderr
    run(root)
    assert "status: green" in expired.read_text()

    fixed = root / "fixed-deadline.md"
    fixed.write_text("---\nexpires_at: '2000-01-01T00:00:00+00:00'\n---\n\nOne-time review.\n")
    result = run(root)
    assert "2 yellow" in result.stdout and "yellow local:" not in result.stderr
    reviewed = subprocess.run([str(TOOLS / "kt"), "renew", str(fixed),
                              hashlib.sha256(fixed.read_bytes()).hexdigest()],
                             capture_output=True, text=True, cwd=root.parent)
    assert reviewed.returncode == 0, reviewed.stderr
    run(root)
    assert "status: green" in fixed.read_text()

    (root / "brown.md").write_text("Broken.\n\nProof:\n\n```bash\nfalse\n```\n")
    result = run(root, "--no-stamp", expected=1)
    assert result.stdout == ("Leaves: 6 total · 4 green · 1 yellow · 1 brown\n"
                             "Proofs: 1 total · 0 valid · 1 failed · FAIL\n")
    assert "brown local:brown.md" in result.stderr

print("proof marker and lifecycle integration checks passed")
