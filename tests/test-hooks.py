#!/usr/bin/env python3
"""Hook protocol, isolation, deduplication, and continuation tests; no models."""
import json
from concurrent.futures import ThreadPoolExecutor
import hashlib
import os
from pathlib import Path
import runpy
import sqlite3
import subprocess
import sys
import tempfile
from unittest.mock import patch

REPOSITORY = Path(__file__).resolve().parents[1]
HANDLER = REPOSITORY / "tools/kt-hooks"


def main():
    handle = runpy.run_path(str(HANDLER))["handle"]
    with tempfile.TemporaryDirectory(prefix="kt bootstrap ") as initial, patch.dict(os.environ, {"KT_GLOBAL_ROOT": str(Path(initial) / ".knowledge"), "KT_CONFIG": str(Path(initial) / "config.json")}):
        initial_root = Path(initial) / ".knowledge"
        (initial_root / ".tools").mkdir(parents=True)
        (initial_root / ".tools/kt").write_bytes((REPOSITORY / "tools/kt").read_bytes())
        (initial_root / "how/to/use").mkdir(parents=True)
        (initial_root / "how/to/use/knowledgetrees.md").write_bytes((REPOSITORY / "example/how/to/use/knowledgetrees.md").read_bytes())
        for source in ("startup", "resume", "clear", "compact"):
            output, code = handle("codex", "start", {"source": source})
            assert code == 0
            context = output["hookSpecificOutput"]
            assert context["hookEventName"] == "SessionStart"
            assert "kt roots" in context["additionalContext"]
            assert "already loaded" in context["additionalContext"]
            assert "verified_by:" not in context["additionalContext"]
        assert handle("codex", "start", {"source": "unexpected"}) == ({}, 0)
        assert handle("copilot", "start", {"source": "startup"}) == ({}, 0)
    with tempfile.TemporaryDirectory(prefix="kt orientation ") as temporary, patch.dict(os.environ, {"KT_GLOBAL_ROOT": str(REPOSITORY / "example"), "KT_CONFIG": ""}):
        fixture_global = Path(temporary) / "global"
        (fixture_global / ".tools").mkdir(parents=True)
        (fixture_global / ".tools/kt").write_bytes((REPOSITORY / "tools/kt").read_bytes())
        (fixture_global / "how/to/use").mkdir(parents=True)
        (fixture_global / "how/to/use/knowledgetrees.md").write_bytes((REPOSITORY / "example/how/to/use/knowledgetrees.md").read_bytes())
        os.environ["KT_GLOBAL_ROOT"] = str(fixture_global)
        os.environ["KT_CONFIG"] = str(Path(temporary) / "config.json")
        directory = Path(temporary) / "project"
        orientation = directory / ".knowledge/where/am/i.md"
        orientation.parent.mkdir(parents=True)
        orientation.write_text("---\nsource: test fixture\n---\nNearest project orientation.\n")
        nested = directory / "src/deep"
        nested.mkdir(parents=True)
        for harness in ("codex", "opencode"):
            for source in ("startup", "resume", "clear", "compact"):
                result, code = handle(harness, "start", {"source": source, "cwd": str(directory)})
                context = result["hookSpecificOutput"]["additionalContext"] if harness == "codex" else result["additionalContext"]
                assert orientation.read_text() in context
                assert str(orientation) in context
        # Privacy boundary: parent orientation must never be injected from a subdirectory.
        for harness in ("codex", "opencode"):
            result, _ = handle(harness, "start", {"source": "startup", "cwd": str(nested)})
            context = result["hookSpecificOutput"]["additionalContext"] if harness == "codex" else result["additionalContext"]
            assert "Nearest project orientation" not in context
        # No project root: keep the canonical bootstrap without invented orientation.
        result, _ = handle("codex", "start", {"source": "startup", "cwd": temporary})
        assert "Nearest project orientation" not in result["hookSpecificOutput"]["additionalContext"]
        # A nearer root wins; a missing orientation must not silently select the parent.
        nearer = nested / ".knowledge"
        nearer.mkdir()
        result, _ = handle("opencode", "start", {"source": "startup", "cwd": str(nested)})
        assert "Nearest project orientation" not in result["additionalContext"]
        (nearer / "where/am").mkdir(parents=True)
        (nearer / "where/am/i.md").write_text("Nested orientation")
        result, _ = handle("opencode", "start", {"source": "startup", "cwd": str(nested)})
        assert "Nested orientation" in result["additionalContext"]
        Path(os.environ["KT_CONFIG"]).write_text(json.dumps({"roots": {"blocked": {"path": str(nearer), "access": "deny"}}}))
        result, _ = handle("opencode", "start", {"source": "startup", "cwd": str(nested)})
        assert "Nested orientation" not in result["additionalContext"]
        policy = {"dangerously_skip_permissions": True, "roots": {"blocked": {"path": str(nearer), "access": "deny"}}}
        Path(os.environ["KT_CONFIG"]).write_text(json.dumps(policy))
        result, _ = handle("opencode", "start", {"source": "startup", "cwd": str(nested)})
        assert "Nested orientation" in result["additionalContext"]
        policy["roots"]["blocked"]["access"] = "force-private"
        Path(os.environ["KT_CONFIG"]).write_text(json.dumps(policy))
        result, _ = handle("opencode", "start", {"source": "startup", "cwd": str(nested)})
        assert "Nested orientation" in result["additionalContext"], "exact local force-private exception"
        policy["roots"]["global"] = {"access": "force-private"}
        Path(os.environ["KT_CONFIG"]).write_text(json.dumps(policy))
        for harness in ("codex", "opencode"):
            result, _ = handle(harness, "start", {"source": "startup", "cwd": str(nested)})
            assert result == {}, "force-private global bootstrap must not leak"
            result, _ = handle(harness, "start", {"source": "resume", "cwd": str(fixture_global)})
            assert result == {}, "starting inside an arbitrary root is not local .knowledge scope"
        exact_home = Path(temporary) / "exact-home"
        exact_root = exact_home / ".knowledge"
        (exact_root / ".tools").mkdir(parents=True)
        (exact_root / ".tools/kt").write_bytes((REPOSITORY / "tools/kt").read_bytes())
        (exact_root / "how/to/use").mkdir(parents=True)
        (exact_root / "how/to/use/knowledgetrees.md").write_bytes((REPOSITORY / "example/how/to/use/knowledgetrees.md").read_bytes())
        os.environ["KT_GLOBAL_ROOT"] = str(exact_root)
        Path(os.environ["KT_CONFIG"]).write_text(json.dumps({"roots": {"global": {"access": "force-private"}}}))
        result, _ = handle("opencode", "start", {"source": "resume", "cwd": str(exact_home)})
        assert "already loaded" in result["additionalContext"], "global is accessible when it is the exact local tree"
    failure = runpy.run_path(str(HANDLER))["failed"]
    for mode in ("default", "bypassPermissions", "plan", None):
        assert handle("codex", "before", {"permission_mode": mode}) == ({}, 0)
    assert failure({"exit_code": 1}) and not failure({"exit_code": 0, "output": "Exit code: 1"})
    assert failure({"isError": True}) and failure({"resultType": "denied"})
    assert failure({"content": [{"type": "text", "text": "Process exited with code 7\n"}]})
    assert failure({"metadata": {"exit": 2}})
    assert failure({"timed_out": True}) and failure("Command exited with code 3.")
    assert not failure({"metadata": {"exit": 0}, "output": "Exit code: 2"})
    for text in ("error: failed operation", "fatal: not a git repository", "x.c:12:3: error: bad type",
                 "Traceback (most recent call last):", "ValueError: bad input", "bash: xyz: command not found",
                 "npm ERR! failed", "make: *** [all] Error 2", "SYNTH_BUILD_FAIL: CDC gate",
                 "\x1b[31mERROR: [Vivado] failed\x1b[0m"):
        assert failure(text), text
    for text in ("", "0 errors, 0 warnings", "All tests passed", "This document discusses error messages.",
                 "warning: unused variable", "ERROR_RATE=0", "The command failed yesterday."):
        assert not failure(text), text
    assert not failure({"exit_code": 0, "output": "ERROR: expected negative-test output"})
    assert not failure("ERROR: expected output\nExit code: 0")
    with tempfile.TemporaryDirectory(prefix="kt hooks test ") as temporary:
        state = Path(temporary) / "state"
        env = {**os.environ, "KT_HOOK_STATE_DIR": str(state), "KT_HOOK_MIN_CALLS": "3"}

        def run(harness, event, payload, expected=0):
            result = subprocess.run([sys.executable, str(HANDLER), harness, event],
                                    input=json.dumps(payload), text=True, capture_output=True, env=env)
            assert result.returncode == expected, (result.stdout, result.stderr)
            return json.loads(result.stdout)

        for harness in ("codex", "copilot", "opencode"):
            def event(kind, **kwargs):
                return run(harness, kind, {"session_id": "session-one", **kwargs},
                           expected=2 if harness == "copilot" and kind == "failed" else 0)
            assert event("prompt", prompt="ordinary task") == {}
            assert event("stop") == {}
            response = event("after", tool_use_id="failed-shell", tool_response={"exit_code": 4})
            message = response.get("additionalContext", response.get("hookSpecificOutput", {}).get("additionalContext"))
            assert "check kt" in message and "kt add" in message
            assert event("after", tool_use_id="failed-shell", tool_response={"exit_code": 4}) == {}
            review = event("stop")
            assert review["decision"] == "block" and "capture review" in review["reason"]
            assert event("prompt", prompt=review["reason"], synthetic=True) == {}
            for number in range(5):
                event("after", tool_use_id=f"review-{number}", tool_response={"exit_code": 0})
            assert event("stop") == {}, "review must not recursively trigger itself"
            assert event("stop", stop_hook_active=True) == {}
            assert event("prompt", prompt="new external task") == {}
            assert event("stop") == {}
            for number in range(3):
                event("after", tool_use_id=f"new-task-{number}", tool_response={"exit_code": 0})
            assert event("stop")["decision"] == "block"
            assert run(harness, "stop", {"sessionID": "isolated-session"}) == {}
            errors = run(harness, "failed", {"sessionID": "error-session", "callID": "error-one"},
                         expected=2 if harness == "copilot" else 0)
            assert errors
        # Stdout-only Codex transport: diagnostic failure triggers bookkeeping.
        actual_shape = {"session_id": "stdout-transport", "tool_name": "Bash",
                        "tool_use_id": "stdout-failure", "tool_response": "ERROR: operation failed"}
        assert "additionalContext" in run("codex", "after", actual_shape)["hookSpecificOutput"]
        assert run("codex", "after", actual_shape) == {}, "failure receipts are deduplicated"
        assert run("codex", "stop", {"session_id": "stdout-transport"})["decision"] == "block"
        assert run("codex", "stop", {"session_id": "stdout-transport"}) == {}
        assert run("codex", "after", {"session_id": "silent", "tool_response": ""}) == {}
        assert run("codex", "stop", {"session_id": "silent"}) == {}
        # Successful work needs the configured threshold; running shell yields do not count.
        assert run("codex", "after", {"session_id": "threshold", "tool_response": {"exit_code": None, "session_id": 123}}) == {}
        for number in range(2):
            run("codex", "after", {"session_id": "threshold", "tool_use_id": str(number), "tool_response": {"exit_code": 0}})
        assert run("codex", "stop", {"session_id": "threshold"}) == {}
        run("codex", "after", {"session_id": "threshold", "tool_use_id": "last", "tool_response": {"exit_code": 0}})
        assert run("codex", "stop", {"session_id": "threshold"})["decision"] == "block"
        assert run("codex", "after", {}) == {}, "missing ids fail open, never mix sessions"
        with ThreadPoolExecutor(max_workers=4) as workers:
            list(workers.map(lambda number: run("codex", "after", {
                "session_id": "concurrent", "tool_use_id": str(number), "tool_response": {"exit_code": 0}}), range(12)))
        assert (state / "hooks.sqlite3").stat().st_mode & 0o777 == 0o600
        with sqlite3.connect(state / "hooks.sqlite3") as connection:
            key = hashlib.sha256(b"codex:concurrent").hexdigest()
            assert connection.execute("SELECT calls FROM sessions WHERE key = ?", (key,)).fetchone()[0] == 12
            rows = repr(connection.execute("SELECT * FROM sessions").fetchall())
            rows += repr(connection.execute("SELECT * FROM events").fetchall())
        assert "session-one" not in rows and "ordinary task" not in rows and "failed-shell" not in rows
    print("hook integration checks passed")


if __name__ == "__main__":
    main()
