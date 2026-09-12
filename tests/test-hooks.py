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

REPOSITORY = Path(__file__).resolve().parents[1]
HANDLER = REPOSITORY / "tools/kt-hooks"


def main():
    failure = runpy.run_path(str(HANDLER))["failed"]
    assert failure({"exit_code": 1}) and not failure({"exit_code": 0, "output": "Exit code: 1"})
    assert failure({"isError": True}) and failure({"resultType": "denied"})
    assert failure({"content": [{"type": "text", "text": "Process exited with code 7\n"}]})
    assert failure({"metadata": {"exit": 2}})
    assert failure({"timed_out": True}) and failure("Command exited with code 3.")
    assert not failure({"metadata": {"exit": 0}, "output": "Exit code: 2"})
    assert not failure({"output": "error: expected in negative test"})
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
