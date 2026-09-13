#!/usr/bin/env python3
"""Persistent bypass, forced privacy, and canonical root address regressions."""
import argparse
import io
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

with tempfile.TemporaryDirectory(prefix="kt-bypass-") as temporary:
    base = Path(temporary)
    project = base / "project"
    local = project / ".knowledge"
    global_root = base / "global"
    shared = base / "one/common/.knowledge"
    private = base / "two/common/.knowledge"
    colon_root = base / "root:colon/.knowledge"
    nested = local / "private"
    for root in (local, global_root, shared, private, colon_root, nested):
        (root / "where/is").mkdir(parents=True)
        (root / "where/is/answer.md").write_text(f"answerneedle {root.name}\n")
    (private / "where/is/answer.md").write_text("classifiedneedle private payload")
    (nested / "hidden.md").write_text("nestedclassified private payload")
    (local / "alias.md").symlink_to(private / "where/is/answer.md")
    registry = base / "roots.json"
    config = {"roots": {
        "global": {"path": str(global_root), "access": "deny"},
        "one": {"path": str(shared), "access": "ask"},
        "secret-alias": {"path": str(private), "access": "force-private"},
        "colon": {"path": str(colon_root), "access": "deny"},
        "nested-secret": {"path": str(nested), "access": "force-private"}},
        "projects": {str(project): {str(private): "allow"}}}
    registry.write_text(json.dumps(config))
    environment = {"KT_CONFIG": str(registry), "KT_GLOBAL_ROOT": str(global_root)}
    previous = Path.cwd()
    try:
        os.chdir(project)
        with patch.dict(os.environ, environment):
            def run(*args, expected=0, cwd=project):
                result = subprocess.run([sys.executable, str(CLI), *args], cwd=cwd,
                                        capture_output=True, text=True)
                assert result.returncode == expected, (args, result.stdout, result.stderr)
                return result.stdout + result.stderr

            before = registry.read_bytes()
            run("permissions", "--dangerously-skip-permissions", expected=3)
            run("--dangerously-skip-permissions", expected=3)
            assert registry.read_bytes() == before
            for response, expected in (("", 1), ("n", 1), ("y", 0)):
                with patch("sys.stdin.isatty", return_value=True), patch("builtins.input", return_value=response) as prompt, patch("sys.stdout", new=io.StringIO()):
                    code = api["permissions_command"](argparse.Namespace(dangerously_skip_permissions=True, reset=False))
                    assert code == expected
                    prompt.assert_called_once_with("Save permission setting? [y/N] ")
                if expected:
                    assert registry.read_bytes() == before
            assert json.loads(registry.read_text())["dangerously_skip_permissions"] is True
            assert "true" in run("permissions")
            listing = run("roots")
            assert "local\tallow" in listing and "global\tallow" in listing
            assert str(shared) in listing and str(colon_root) in listing
            assert str(private) not in listing and "secret-alias" not in listing
            assert str(nested) not in listing and "nested-secret" not in listing
            assert "answerneedle" in run("open", "global:where/is/answer.md")
            assert "answerneedle" in run("open", f"{shared}:where/is/answer.md")
            assert "answerneedle" in run("open", f"{colon_root}:where/is/answer.md")
            assert run("open", "local:where/is/answer.md") == run("open", "project:where/is/answer.md")
            matches = run("find", "answerneedle")
            assert f"{shared}:where/is/answer.md" in matches
            assert f"{colon_root}:where/is/answer.md" in matches
            for pretty in ((), ("--pretty",)):
                for args in (("roots",), ("find", "classifiedneedle"), ("where", "is", "answer")):
                    expected = 1 if args[0] == "find" else 0
                    output = run(*args, *pretty, expected=expected)
                    assert str(private) not in output and "private payload" not in output
                    assert str(nested) not in output
            for args in (("open", f"{private}:where/is/answer.md"),
                         ("open", str(private / "where/is/missing.md")),
                         ("open", "secret-alias:where/is/answer.md"),
                         ("open", "local:alias.md"),
                         ("open", "local:private/missing.md"),
                         ("add", "what is hidden", "new", "--root", str(private)),
                         ("add", "private hidden", "new"),
                         ("amend", str(private / "where/is/answer.md"), "--expect", "0" * 64),
                         ("prove", "--root", str(private), "--no-stamp"),
                         ("prove", "--root", str(local), "--no-stamp")):
                output = run(*args, expected=3)
                assert str(private) not in output and str(nested) not in output, output
            assert not (private / "what/is/hidden.md").exists()
            assert not (nested / "hidden/new.md").exists()
            assert str(private) not in run("access", "secret-alias")
            # Only exact local scope exposes the private tree; descendants do not.
            assert "classifiedneedle" in run("open", "local:where/is/answer.md", cwd=private)
            assert "local\tallow" in run("roots", cwd=private)
            child = private / "subdir"
            child.mkdir()
            assert str(private) not in run("roots", cwd=child)
            run("add", "what is external", "captured", "--root", str(shared))
            assert f'scope: "{shared}"' in (shared / "what/is/external.md").read_text()
            run("add", "what is local", "captured", "--local")
            assert 'scope: "local"' in (local / "what/is/local.md").read_text()
            # Restoring checks keeps force-private and existing root policies intact.
            with patch("sys.stdin.isatty", return_value=True), patch("builtins.input", return_value="yes"), patch("sys.stdout", new=io.StringIO()):
                assert api["permissions_command"](argparse.Namespace(dangerously_skip_permissions=False, reset=True)) == 0
            run("open", "global:where/is/answer.md", expected=3)
            assert api["root_access"](private) == "force-private"
            cfg = json.loads(registry.read_text())
            cfg["dangerously_skip_permissions"] = "yes"
            registry.write_text(json.dumps(cfg))
            run("roots", expected=2)
    finally:
        os.chdir(previous)
print("bypass/privacy/root identity integration checks passed")
