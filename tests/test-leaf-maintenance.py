#!/usr/bin/env python3
"""Leaf maintenance behavior without Git or an interactive editor."""
import argparse
import errno
import hashlib
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]
CLI = REPO / "tools/kt"
api = runpy.run_path(str(CLI))

with tempfile.TemporaryDirectory(prefix="kt-maintenance-") as temporary:
    base = Path(temporary)
    root = base / ".knowledge"
    root.mkdir()
    outside = base / "elsewhere/.knowledge"
    outside.mkdir(parents=True)
    private = base / "hidden/.knowledge"
    private.mkdir(parents=True)
    secret = private / "fact.md"
    secret.write_text("private payload")
    config = base / "access.json"
    config.write_text(json.dumps({"dangerously_skip_permissions": True, "roots": {
        "outside": {"path": str(outside), "access": "ask"},
        "hidden": {"path": str(private), "access": "force-private"}}}))
    env = {**os.environ, "KT_CONFIG": str(config), "KT_GLOBAL_ROOT": str(base / "global")}
    def run(*args, expected=0):
        result = subprocess.run([sys.executable, str(CLI), *args], cwd=base, env=env,
                                capture_output=True, text=True)
        assert result.returncode == expected, (args, result.stdout, result.stderr)
        if expected == 0 and "--dry-run" not in args:
            assert result.stdout == "" and result.stderr == "", (args, result.stdout, result.stderr)
        return result.stdout + result.stderr
    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    source = root / "what/is/first.md"
    source.parent.mkdir(parents=True)
    first = "---\nverified_at: yesterday\n---\n\nFirst answer.\n\nA true assertion.\n\nProof: (verified at yesterday)\n\n```bash\ntest 1 -eq 1\n```\n"
    source.write_text(first)
    alias = base / "alias.md"
    os.link(source, alias)
    original_inode = source.stat().st_ino
    destination = root / "what/is/moved.md"
    run("mv", "local:what/is/first.md", "local:what/is/moved.md", "--expect", "0" * 64, expected=4)
    assert source.exists() and not destination.exists()
    run("mv", "local:what/is/first.md", "local:what/is/moved.md", "--expect", digest(source), "--dry-run")
    assert source.exists() and not destination.exists()
    destination.write_text("existing")
    run("mv", "local:what/is/first.md", "local:what/is/moved.md", "--expect", digest(source), expected=2)
    assert source.read_text() == first and destination.read_text() == "existing"
    destination.unlink()
    run("mv", "local:what/is/first.md", "local:what/is/moved.md", "--expect", digest(source))
    assert not source.exists() and destination.read_text() == first
    assert destination.samefile(alias) and destination.stat().st_ino == original_inode
    # Across-filesystem fallback preserves bytes and only removes source after copy.
    previous = Path.cwd()
    try:
        os.chdir(base)
        with patch.dict(os.environ, env), patch("os.link", side_effect=OSError(errno.EXDEV, "cross device")):
            target = outside / "what/is/moved.md"
            api["relocate_leaf"](argparse.Namespace(command="mv", path="local:what/is/moved.md",
                destination=str(target), expect=digest(destination), dry_run=False))
        assert target.read_text() == first and not destination.exists()
        assert alias.read_text() == first
    finally:
        os.chdir(previous)
    run("rm", str(target), "--expect", "0" * 64, expected=4)
    run("rm", str(target), "--expect", digest(target), "--dry-run")
    assert target.exists()
    run("rm", str(target), "--expect", digest(target))
    assert not target.exists() and alias.read_text() == first
    assert root.is_dir() and (outside / "what/is").is_dir()

    source.write_text(first)
    second = root / "what/is/second.md"
    second_body = "---\nfalsified_at: yesterday\nstatus: unresolved\nblocker: pending evidence\nnext_check: inspect source\n---\n\nSecond answer.\n"
    second.write_text(second_body)
    output = root / "what/is/combined.md"
    args = ("combine", "local:what/is/first.md", "local:what/is/second.md", "-o", "local:what/is/combined.md")
    run(*args, "--dry-run")
    assert not output.exists()
    run(*args)
    text = output.read_text()
    assert text.count("---\n") == 2 and text.index("First answer") < text.index("Second answer")
    assert "verified_at:" not in text and "verified at yesterday" not in text
    assert "Proof: (verified at _)" in text and 'falsified_at: "yesterday"' in text
    assert 'status: "unresolved"' in text
    assert "source:" in text and "revision=" in text
    assert not source.exists() and not second.exists()
    assert "pending evidence" in text and "inspect source" in text
    source.write_text(first)
    second.write_text(second_body)
    run(*args, expected=2)
    assert source.read_text() == first and second.read_text() == second_body
    run(*args, "--expect", "0" * 64, expected=4)
    combined_alias = base / "combined-alias.md"
    os.link(output, combined_alias)
    # Replacement preserves destination hardlinks and invalidates even unchanged proofs.
    output.write_text(text.replace("verified at _", "verified at caller-invented-date"))
    run(*args, "--expect", digest(output))
    assert output.samefile(combined_alias)
    assert "caller-invented-date" not in output.read_text()
    assert not source.exists() and not second.exists()
    source.write_text(first)
    second.write_text(second_body)
    reverse = root / "what/is/reversed.md"
    run("combine", "local:what/is/second.md", "local:what/is/first.md", "-o", str(reverse))
    assert reverse.read_text().index("Second answer") < reverse.read_text().index("First answer")
    assert not source.exists() and not second.exists()
    source.write_text(first)
    second.write_text(second_body)
    input_alias = root / "what/is/input-alias.md"
    os.link(source, input_alias)
    run("combine", str(source), str(second), str(input_alias), "-o", str(source), "--expect", digest(source))
    assert source.exists() and not second.exists() and not input_alias.exists()
    assert source.read_text().index("First answer") < source.read_text().index("Second answer")
    # A failed output write never removes inputs.
    saved_source = source.read_bytes()
    original_open = Path.open
    failed_output = root / "what/is/failed.md"
    def fail_output(path, *arguments, **kwargs):
        if path == failed_output:
            raise OSError("simulated write failure")
        return original_open(path, *arguments, **kwargs)
    try:
        os.chdir(base)
        with patch.dict(os.environ, env), patch.object(Path, "open", fail_output):
            try:
                api["combine_leaves"](argparse.Namespace(paths=[str(source)], output=str(failed_output), expect=None, dry_run=False))
                raise AssertionError("write failure should propagate")
            except OSError:
                pass
        assert source.read_bytes() == saved_source and not failed_output.exists()
        # Concurrent source changes after destination save are retained.
        changed_output = root / "what/is/changed.md"
        with patch.dict(os.environ, env), patch("os.fsync", side_effect=lambda fd: source.write_text("concurrent update")):
            try:
                api["combine_leaves"](argparse.Namespace(paths=[str(source)], output=str(changed_output), expect=None, dry_run=False))
                raise AssertionError("changed input must be retained")
            except api["RevisionConflict"]:
                pass
        assert source.read_text() == "concurrent update" and changed_output.exists()
    finally:
        os.chdir(previous)
    for command in (("rm", str(secret), "--expect", digest(secret)),
                    ("mv", str(secret), str(root / "fact.md"), "--expect", digest(secret)),
                    ("mv", str(source), str(private / "new.md"), "--expect", digest(source)),
                    ("combine", str(secret), "-o", str(root / "new.md")),
                    ("combine", str(source), "-o", str(private / "new.md"))):
        result = run(*command, expected=3)
        assert str(private) not in result and "private payload" not in result
    assert secret.read_text() == "private payload" and source.exists()
    # Escape/symlink destinations cannot be used to relocate a leaf.
    (root / "symlink").symlink_to(outside, target_is_directory=True)
    run("mv", str(source), "local:../escape.md", "--expect", digest(source), expected=2)
    run("mv", str(source), "local:symlink/fact.md", "--expect", digest(source), expected=2)
print("leaf maintenance integration checks passed")
