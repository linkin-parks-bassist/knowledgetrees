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
    return result


with tempfile.TemporaryDirectory(prefix="proof-stamp-test-") as temporary:
    root = Path(temporary) / ".knowledge"
    root.mkdir()
    leaf = root / "fact.md"
    original = ("---\nstatus: green\nrevised_at: '2026-09-12T12:00:00+00:00'\n"
                "checked_at: '2000-01-01T00:00:00+00:00'\n"
                "expires_at: '2099-01-01T00:00:00+00:00'\n---\n\n"
                "A passing assertion.\n\nProof: (verified at _)\n\n```bash\ntest 1 -eq 1\n```\n\n"
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
    assert "checked_at: '2000-01-01T00:00:00+00:00'" in updated
    assert "Proof: (falsified at " in updated
    assert "status: brown" in updated
    assert linked.read_text() == updated and linked.samefile(leaf)
    first_falsified = next(line for line in updated.splitlines()
                            if line.startswith("Proof: (falsified at "))
    run(root, expected=1)
    assert first_falsified in leaf.read_text(), "proof failure time must not churn"
    leaf.write_text(updated.replace("false", "test 2 -eq 2"))
    run(root, expected=1)
    assert "Proof: (verified at _)" not in leaf.read_text()
    assert "Proof: (falsified at " not in leaf.read_text()
    assert "status: brown" in leaf.read_text(), "passing proofs cannot validate an unflagged leaf"
    run(root, "--no-stamp", expected=1)
    import hashlib
    reviewed = subprocess.run([str(TOOLS / "kt"), "renew", str(leaf),
                              hashlib.sha256(leaf.read_bytes()).hexdigest()],
                             capture_output=True, text=True, cwd=root.parent)
    assert reviewed.returncode == 0, reviewed.stderr
    run(root)
    assert "status: green" in leaf.read_text()
    leaf.write_text("Malformed.\n\nProof: (verified at yesterday)\n\n```bash\ntrue\n```\n")
    malformed = leaf.read_text()
    run(root, expected=1)
    assert "status: brown" in leaf.read_text()
    assert "Proof: (verified at yesterday)" in leaf.read_text()
    leaf.write_text("Instructions only.\n\n```bash\ntrue\n```\n")
    unproved = leaf.read_text()
    run(root)
    assert "status: green" in leaf.read_text() and unproved in leaf.read_text()
    leaf.write_text("---\nstatus: green\nrevised_at: '2026-09-12T12:00:00+00:00'\nname: test\n---\n\nBad.\n\nProof: (falsified at _)\n\n```bash\nfalse\n```\n")
    run(root, expected=1)
    assert "status: brown" in leaf.read_text()
    leaf.write_text("Bad.\n\nProof: (verified at _)\n\n```bash\nfalse\n```\n")
    run(root, expected=1)
    assert leaf.read_text().startswith("---\nstatus: brown")

    leaf.write_text(
        "---\nstatus: brown\nrevised_at: '2026-09-12T12:00:00+00:00'\nverifiable: true\n---\n\n"
        "A fully proved concrete fact.\n\nProof: (falsified at _)\n\n"
        "```bash\ntest 3 -eq 3\n```\n")
    run(root)
    verified = leaf.read_text()
    assert "checked_at:" not in verified
    assert "Proof: (verified at " in verified
    assert "status: green" in verified
    stable = leaf.read_text()
    stable_mtime = leaf.stat().st_mtime_ns
    run(root)
    assert leaf.read_text() == stable, "non-expiring verified leaves must not churn timestamps"
    assert leaf.stat().st_mtime_ns == stable_mtime, "unchanged evaluation must not write"

    leaf.write_text(
        "---\nverifiable: true\nstatus: yellow\n"
        "expires_at: '2000-01-01T00:00:00+00:00'\n---\n\n"
        "The complete claim is proved.\n\n"
        "Proof: (verified at _)\n\n```bash\ntest 4 -eq 4\n```\n")
    run(root)
    assert "status: green" in leaf.read_text()
    assert "checked_at:" not in leaf.read_text()
    leaf.write_text(leaf.read_text().replace("test 4 -eq 4", "false"))
    run(root, expected=1)
    assert "status: brown" in leaf.read_text()
    leaf.write_text(leaf.read_text().replace("false", "test 4 -eq 4"))
    run(root)
    assert "status: green" in leaf.read_text()
    assert "status: green" in leaf.read_text()

    leaf.write_text("---\nverifiable: true\n---\n\nClaim without a proof.\n")
    run(root, expected=1)
    assert "status: brown" in leaf.read_text()

    leaf.write_text(
        "---\nstatus: green\nrevised_at: '2026-09-12T12:00:00+00:00'\nname: stable\n---\n\nStable.\n\n"
        "Proof: (verified at 2020-01-01T00:00:00+00:00)\n\n"
        "```bash\ntrue\n```\n")
    stable = leaf.read_text()
    stable_mtime = leaf.stat().st_mtime_ns
    run(root)
    assert "Proof: (verified at 2020-01-01T00:00:00+00:00)" in leaf.read_text()
    assert "status: green" in leaf.read_text() and "checked_at:" not in leaf.read_text()

    leaf.write_text(
        "---\nverifiable: perhaps\n---\n\nClaim.\n\nProof: (verified at _)\n\n```bash\ntrue\n```\n")
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
    assert "default-green.md" not in result.stderr
    run(root)
    assert "status: green" in (root / "green.md").read_text()
    assert (root / "default-green.md").read_text().startswith("---\nstatus: green")
    assert "status: yellow" in (root / "expired.md").read_text()
    assert "status: yellow" in (root / "explicit-yellow.md").read_text()

    import hashlib
    expired = root / "expired.md"
    digest = hashlib.sha256(expired.read_bytes()).hexdigest()
    reviewed = subprocess.run([str(TOOLS / "kt"), "renew", str(expired), digest],
                              capture_output=True, text=True, cwd=root.parent)
    assert reviewed.returncode == 0, reviewed.stderr
    run(root)
    assert "status: green" in expired.read_text()

    fixed = root / "fixed-deadline.md"
    fixed.write_text("---\nexpires_at: '2000-01-01T00:00:00+00:00'\n---\n\nOne-time review.\n")
    result = run(root)
    assert "2 yellow" in result.stdout and "yellow local:" not in result.stderr
    digest = hashlib.sha256(fixed.read_bytes()).hexdigest()
    reviewed = subprocess.run([str(TOOLS / "kt"), "renew", str(fixed), digest],
                              capture_output=True, text=True, cwd=root.parent)
    assert reviewed.returncode == 0, reviewed.stderr
    run(root)
    assert "status: green" in fixed.read_text()

    (root / "brown.md").write_text(
        "Broken.\n\nProof: (verified at _)\n\n```bash\nfalse\n```\n")
    result = run(root, "--no-stamp", expected=1)
    assert result.stdout == ("Leaves: 6 total · 4 green · 1 yellow · 1 brown\n"
                             "Proofs: 1 total · 0 valid · 1 failed · FAIL\n")
    assert "brown local:brown.md" in result.stderr

print("proof timestamp integration checks passed")
