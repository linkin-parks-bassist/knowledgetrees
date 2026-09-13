#!/usr/bin/env python3
"""Root privacy, persistent grants, session isolation, and capture registration."""
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

SCRIPT = Path(__file__).resolve().parents[1] / "tools/kt"


def main():
    api = runpy.run_path(str(SCRIPT))
    with tempfile.TemporaryDirectory(prefix="kt privacy ") as temporary:
        base = Path(temporary)
        project = base / "project-a"
        other = base / "project-b"
        global_root = base / "global"
        shared = base / "shared"
        for directory in (project, other):
            (directory / ".knowledge/where/am").mkdir(parents=True)
            (directory / ".knowledge/where/am/i.md").write_text("Local orientation")
        for root in (global_root, shared):
            (root / "where/is").mkdir(parents=True)
            (root / "where/is/private.md").write_text("secretneedle confidential payload")
        (project / ".knowledge/what/is").mkdir(parents=True)
        (project / ".knowledge/what/is/local.md").write_text("Public local answer")
        config = base / "roots.json"
        environment = {"KT_CONFIG": str(config), "KT_GLOBAL_ROOT": str(global_root),
                       "KT_ACCESS_STATE_DIR": str(base / "state"), "KT_SESSION_ID": "session-one"}
        previous = Path.cwd()
        try:
            os.chdir(project)
            with patch.dict(os.environ, environment):
                def run(*arguments, cwd=project, expected=0):
                    result = subprocess.run([sys.executable, str(SCRIPT), *arguments], cwd=cwd,
                                            text=True, capture_output=True)
                    assert result.returncode == expected, (arguments, result.stdout, result.stderr)
                    return result.stdout + result.stderr

                def decision(root, value, scope="project", response="yes", subdirectories=False):
                    with patch("sys.stdin.isatty", return_value=True), patch("builtins.input", return_value=response) as confirmation, patch("sys.stdout", new=io.StringIO()):
                        result = api["access_command"](argparse.Namespace(root=root, decision=value, scope=scope, subdirectories=subdirectories))
                        confirmation.assert_called_once_with(f"Save {value!r} decision? [y/N] ")
                        return result

                assert "Public local answer" in run("what is local")
                assert "confidential payload" not in run("find", "secretneedle", expected=1)
                assert str(global_root / "where") not in run("roots")
                for arguments in (("open", "global:where/is/private.md"),
                                  ("open", str(global_root / "where/is/private.md")),
                                  ("prove", "--root", str(global_root))):
                    output = run(*arguments, expected=3)
                    assert "confidential payload" not in output
                before = config.read_bytes() if config.exists() else None
                run("access", "global", "allow", expected=3)
                assert (config.read_bytes() if config.exists() else None) == before
                # Persistent project grant survives new processes and narrows to descendants.
                for response in ("", "n", "N", "no", "es"):
                    assert decision("global", "allow", response=response) == 1
                    assert (config.read_bytes() if config.exists() else None) == before
                    run("open", "global:where/is/private.md", expected=3)
                assert decision("global", "allow", response="y") == 0
                assert "confidential payload" in run("open", "global:where/is/private.md")
                assert decision("global", "allow", response=" Y ") == 0
                assert "confidential payload" not in run("find", "secretneedle", cwd=other, expected=1)
                nested = project / "src"
                nested.mkdir()
                run("open", "global:where/is/private.md", cwd=nested, expected=3)
                decision("global", "allow", subdirectories=True)
                assert "confidential payload" in run("open", "global:where/is/private.md", cwd=nested)
                decision("global", "reset")
                run("open", "global:where/is/private.md", expected=3)
                # Session-only grant cannot leak to another session or another project.
                decision("global", "allow", "session")
                run("open", "global:where/is/private.md")
                with patch.dict(os.environ, {"KT_SESSION_ID": "session-two"}):
                    run("open", "global:where/is/private.md", expected=3)
                run("open", "global:where/is/private.md", cwd=other, expected=3)
                decision("global", "reset", "session")
                # Always-allow and root-level deny persist independently of project/session grants.
                decision("global", "allow", "all")
                run("open", "global:where/is/private.md", cwd=other)
                decision("global", "deny", "all")
                run("open", "global:where/is/private.md", expected=3)
                decision("global", "reset", "all")
                run("open", "global:where/is/private.md", expected=3)
                # Merely being inside a registered private tree cannot grant its entire ancestor scope.
                child_directory = global_root / "subdir"
                child_directory.mkdir()
                run("open", "global:where/is/private.md", cwd=child_directory, expected=3)
                # Capture into an unfamiliar wider tree registers it as private, without writing a leaf.
                run("add", "what is capture", "New content", "--root", str(shared), expected=3)
                registry = json.loads(config.read_text())
                label = next(name for name, spec in registry["roots"].items() if spec.get("path") == str(shared))
                assert registry["roots"][label]["access"] == "ask"
                assert not (shared / "what/is/capture.md").exists()
                assert "confidential payload" not in config.read_text()
                assert "confidential payload" not in run("find", "secretneedle", expected=1)
                decision(label, "allow")
                run("add", "what is capture", "New content", "--root", str(shared))
                assert "New content" in run("open", label + ":what/is/capture.md")
                run("open", label + ":what/is/capture.md", cwd=other, expected=3)
                # No implicit parent discovery, even with a parent orientation on disk.
                run("open", "project:what/is/local.md", cwd=nested, expected=2)
                # A restricted registered subtree cannot leak through an allowed ancestor tree.
                child = project / ".knowledge/private"
                child.mkdir()
                (child / "hidden.md").write_text("nestedsecret must not leak")
                run("register", "restricted-child", str(child))
                assert "must not leak" not in run("find", "nestedsecret", expected=1)
                run("open", "project:private/hidden.md", expected=3)
                run("open", str(child / "hidden.md"), expected=3)
                # Denying an ancestor root also denies registered children.
                decision("restricted-child", "allow", "all")
                decision(str(project / ".knowledge"), "deny", "all")
                run("open", str(child / "hidden.md"), expected=3)
                # Malformed policy fails closed and never emits knowledge.
                config.write_text('{"roots":{"global":{"access":"oops"}}}')
                assert "confidential payload" not in run("find", "secretneedle", expected=2)
        finally:
            os.chdir(previous)
    print("root access integration checks passed")


if __name__ == "__main__":
    main()
