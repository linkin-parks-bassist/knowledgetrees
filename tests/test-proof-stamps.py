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
    original = ("---\nverified_at: '2000-01-01T00:00:00+00:00'\n"
                "expires_at: '2099-01-01T00:00:00+00:00'\n---\n\n"
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
    assert "\nStatus: Brown\n\n" in updated
    assert linked.read_text() == updated and linked.samefile(leaf)
    first_falsified = next(line for line in updated.splitlines()
                            if line.startswith("falsified_at:"))
    run(root, expected=1)
    assert first_falsified in leaf.read_text(), "sticky falsification time must not churn"
    leaf.write_text(updated.replace("false", "test 2 -eq 2"))
    run(root, expected=1)
    assert "Proof: (verified at _)" not in leaf.read_text()
    assert "Proof: (falsified at " not in leaf.read_text()
    assert "falsified_at: '" in leaf.read_text(), "passing proofs cannot validate a leaf"
    run(root, "--no-stamp", expected=1)
    leaf.write_text("\n".join(line for line in leaf.read_text().splitlines()
                              if not line.startswith("falsified_at:")) + "\n")
    run(root)
    assert "\nStatus: Green\n\n" in leaf.read_text()
    leaf.write_text("Malformed.\n\nProof: (verified at yesterday)\n\n```bash\ntrue\n```\n")
    malformed = leaf.read_text()
    run(root, expected=1)
    assert "falsified_at:" in leaf.read_text()
    assert "Proof: (verified at yesterday)" in leaf.read_text()
    leaf.write_text("Instructions only.\n\n```bash\ntrue\n```\n")
    unproved = leaf.read_text()
    run(root)
    assert leaf.read_text() == "Status: Green\n\n" + unproved
    leaf.write_text("---\nname: test\nmetadata:\n  verified_at: '2000-01-01T00:00:00+00:00'\n---\n\nBad.\n\nProof: (falsified at _)\n\n```bash\nfalse\n```\n")
    run(root, expected=1)
    assert "metadata:\n  falsified_at:" in leaf.read_text()
    assert "  verified_at: '2000-01-01T00:00:00+00:00'" in leaf.read_text()
    assert "\nStatus: Brown\n\n" in leaf.read_text()
    leaf.write_text("Bad.\n\nProof:\n\n```bash\nfalse\n```\n")
    run(root, expected=1)
    assert leaf.read_text().startswith("---\nfalsified_at:")

    leaf.write_text(
        "---\nverifiable: true\nfalsified_at: '2000-01-01T00:00:00+00:00'\n---\n\n"
        "A fully proved concrete fact.\n\nProof: (falsified at _)\n\n"
        "```bash\ntest 3 -eq 3\n```\n")
    run(root)
    verified = leaf.read_text()
    assert "falsified_at:" not in verified
    assert "verified_at: '" in verified
    assert "Proof: (verified at " in verified
    assert "\nStatus: Green\n\n" in verified
    stable = leaf.read_text()
    stable_mtime = leaf.stat().st_mtime_ns
    run(root)
    assert leaf.read_text() == stable, "non-expiring verified leaves must not churn timestamps"
    assert leaf.stat().st_mtime_ns == stable_mtime, "unchanged evaluation must not write"

    leaf.write_text("---\nverifiable: true\n---\n\nClaim without a proof.\n")
    run(root, expected=1)
    assert "falsified_at:" in leaf.read_text()

    leaf.write_text(
        "---\nname: stable\n---\nStatus: Green\n\nStable.\n\n"
        "Proof: (verified at 2020-01-01T00:00:00+00:00)\n\n"
        "```bash\ntrue\n```\n")
    stable = leaf.read_text()
    stable_mtime = leaf.stat().st_mtime_ns
    run(root)
    assert leaf.read_text() == stable, "passing non-expiring proof timestamps stay untouched"
    assert leaf.stat().st_mtime_ns == stable_mtime, "stable status and proof markers must not write"

    leaf.write_text(
        "---\nverifiable: perhaps\n---\n\nClaim.\n\nProof:\n\n```bash\ntrue\n```\n")
    run(root, expected=1)
    assert "falsified_at:" in leaf.read_text()

with tempfile.TemporaryDirectory(prefix="leaf-state-test-") as temporary:
    root = Path(temporary) / ".knowledge"
    root.mkdir()
    (root / "green.md").write_text(
        "---\nverified_at: '2026-09-17T00:00:00+10:00'\nexpires_every: '2 weeks'\n---\n\nCurrent.\n")
    (root / "expired.md").write_text(
        "---\nverified_at: '2026-08-01T00:00:00+10:00'\nexpires_every: 'two weeks'\n---\n\nOld.\n")
    (root / "default-green.md").write_text("A non-verifiable plan is green by default.\n")
    (root / "explicit-yellow.md").write_text("---\nstate: yellow\n---\n\nNeeds review.\n")
    result = run(root, "--no-stamp")
    assert result.stdout == "green=2 yellow=2 brown=0\n"
    assert "yellow local:expired.md" in result.stderr
    assert "yellow local:explicit-yellow.md" in result.stderr
    assert "default-green.md" not in result.stderr
    run(root)
    assert "\nStatus: Green\n\n" in (root / "green.md").read_text()
    assert (root / "default-green.md").read_text().startswith("Status: Green\n\n")
    assert "\nStatus: Yellow\n\n" in (root / "expired.md").read_text()
    assert "\nStatus: Yellow\n\n" in (root / "explicit-yellow.md").read_text()

    (root / "brown.md").write_text(
        "Broken.\n\nProof: (verified at _)\n\n```bash\nfalse\n```\n")
    result = run(root, "--no-stamp", expected=1)
    assert result.stdout == "green=2 yellow=2 brown=1\n"
    assert "brown local:brown.md" in result.stderr

print("proof timestamp integration checks passed")
