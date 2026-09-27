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
    handler_api = runpy.run_path(str(HANDLER))
    assert "knowledgetrees-maintenance skill" in handler_api["MAINTAIN"]
    assert "never append logs" in handler_api["MAINTAIN"]
    handle = handler_api["handle"]
    with tempfile.TemporaryDirectory(prefix="kt info hook test ") as temporary:
        root = Path(temporary)
        global_root = root / "global"
        (global_root / "how/to/use").mkdir(parents=True)
        (global_root / "how/to/use/knowledgetrees.md").write_text("Canonical procedure fixture.\n")
        (root / "config.json").write_text(json.dumps({"roots": {"global": {"path": str(global_root), "access": "allow"}}}))
        project = root / "project"
        (project / ".knowledge/where/am").mkdir(parents=True)
        (project / ".knowledge/where/am/i.md").write_text("Project orientation fixture.\n")
        with patch.dict(os.environ, {"KT_INFO_CLI": str(REPOSITORY / "tools/kt"),
                                  "KT_GLOBAL_ROOT": str(global_root),
                                  "KT_CONFIG": str(root / "config.json")}):
            for harness in ("codex", "opencode", "copilot", "claude"):
                sources = ("startup", "resume", "new") if harness == "copilot" else ("startup", "resume", "clear", "compact")
                for source in sources:
                    result, code = handle(harness, "start", {"source": source, "cwd": str(project)})
                    assert code == 0
                    context = (result["hookSpecificOutput"]["additionalContext"]
                               if harness in ("codex", "claude") else result["additionalContext"])
                    assert "Canonical procedure fixture." in context
                    assert "Project orientation fixture." in context
                    assert context.rstrip().endswith("0 failed · SUCCESS") and "0 brown" in context
            # Claude Code drops hook context past ~10,000 characters, so oversized `kt info` output is
            # replaced by an instruction to run it directly; other harnesses keep the full text.
            with patch.dict(os.environ, {"KT_HOOK_CONTEXT_LIMIT": "200"}):
                big, _ = handle("claude", "start", {"source": "startup", "cwd": str(project)})
                text = big["hookSpecificOutput"]["additionalContext"]
                assert "Call the kt_info tool" in text and "Canonical procedure fixture." not in text
                assert len(text) < 700
                whole, _ = handle("codex", "start", {"source": "startup", "cwd": str(project)})
                assert "Canonical procedure fixture." in whole["hookSpecificOutput"]["additionalContext"]
            small, _ = handle("claude", "start", {"source": "startup", "cwd": str(project)})
            assert "Canonical procedure fixture." in small["hookSpecificOutput"]["additionalContext"]
            # Without a local root, `kt info` falls back to the global root instead of failing.
            fallback, _ = handle("claude", "start", {"source": "startup", "cwd": str(root)})
            context = fallback["hookSpecificOutput"]["additionalContext"]
            assert "kt info failed" not in context and "Canonical procedure fixture." in context
            assert "no ./.knowledge" in context and context.rstrip().endswith("0 failed · SUCCESS") and "0 brown" in context
            # A genuinely unusable `kt info` run (no global procedure) is still reported, not hidden.
            (global_root / "how/to/use/knowledgetrees.md").unlink()
            failed_info, _ = handle("codex", "start", {"source": "startup", "cwd": str(project)})
            assert "kt info failed" in failed_info["hookSpecificOutput"]["additionalContext"]
    assert handle("codex", "start", {"source": "unexpected"}) == ({}, 0)
    assert handle("copilot", "start", {"source": "unexpected"}) == ({}, 0)
    assert handle("claude", "start", {"source": "unexpected"}) == ({}, 0)
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
        env = {**os.environ, "KT_HOOK_STATE_DIR": str(state)}

        def run(harness, event, payload, expected=0):
            result = subprocess.run([sys.executable, str(HANDLER), harness, event],
                                    input=json.dumps(payload), text=True, capture_output=True, env=env)
            assert result.returncode == expected, (result.stdout, result.stderr)
            return json.loads(result.stdout)

        # Dormant failure reminders still deduplicate receipts per session.
        for harness in ("codex", "copilot", "opencode"):
            def event(kind, **kwargs):
                return run(harness, kind, {"session_id": "session-one", **kwargs},
                           expected=2 if harness == "copilot" and kind == "failed" else 0)
            assert event("prompt", prompt="ordinary task") == {}
            response = event("after", tool_use_id="failed-shell", tool_response={"exit_code": 4})
            message = response.get("additionalContext", response.get("hookSpecificOutput", {}).get("additionalContext"))
            assert "check kt" in message and "kt_add" in message
            assert event("after", tool_use_id="failed-shell", tool_response={"exit_code": 4}) == {}
            errors = run(harness, "failed", {"sessionID": "error-session", "callID": "error-one"},
                         expected=2 if harness == "copilot" else 0)
            assert errors
        broken = run("claude", "failed", {"session_id": "claude-one", "tool_use_id": "bad-1", "error": "Exit code 1", "is_interrupt": False})
        assert broken["hookSpecificOutput"]["hookEventName"] == "PostToolUseFailure"
        assert run("claude", "failed", {"session_id": "claude-one", "tool_use_id": "stopped", "is_interrupt": True}) == {}
        # Reminders are rate-limited per session; the default interval is five minutes.
        first = run("claude", "stop", {"session_id": "claude-rate", "stop_hook_active": False})
        assert first["decision"] == "block" and "knowledgetrees-maintenance" in first["reason"]
        assert run("claude", "stop", {"session_id": "claude-rate", "stop_hook_active": True}) == {}
        assert run("claude", "stop", {"session_id": "claude-rate", "stop_hook_active": False}) == {}, "within the interval"
        assert run("claude", "stop", {"session_id": "claude-other", "stop_hook_active": False})["decision"] == "block"
        env["KT_HOOK_MAINTENANCE_INTERVAL"] = "0"
        for harness in ("claude", "codex"):
            for _ in range(2):
                assert run(harness, "stop", {"session_id": f"{harness}-turns", "stop_hook_active": False})["decision"] == "block"
                assert run(harness, "stop", {"session_id": f"{harness}-turns", "stop_hook_active": True}) == {}
        # Without a continuation flag, stops alternate per session: turn, maintenance, turn.
        for harness in ("copilot", "opencode"):
            for session in ("alpha", "beta"):
                assert run(harness, "stop", {"sessionId": session})["decision"] == "block"
            assert run(harness, "stop", {"sessionId": "alpha"}) == {}, "maintenance must not trigger itself"
            assert run(harness, "stop", {"sessionId": "alpha"})["decision"] == "block"
            assert run(harness, "stop", {"sessionId": "beta"}) == {}
        assert run("copilot", "stop", {}) == {}, "missing ids fail open instead of looping"
        # A turn that already wrote the tree after its last code edit needs no reminder.
        transcript = Path(temporary) / "transcript.jsonl"

        def claude_turn(*names):
            entries = [{"type": "user", "message": {"role": "user", "content": "earlier task"}},
                       {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "mcp__knowledgetrees__kt_add", "input": {}}]}},
                       {"type": "user", "message": {"role": "user", "content": "current task"}}]
            for name in names:
                entries.append({"type": "assistant", "message": {"content": [{"type": "tool_use", "name": name, "input": {"command": "kt rewrite local:x.md HASH body" if name == "Bash" else ""}}]}})
                entries.append({"type": "user", "message": {"role": "user", "content": [{"type": "tool_result", "content": "ok"}]}})
            transcript.write_text("\n".join(map(json.dumps, entries)) + "\n")
            return run("claude", "stop", {"session_id": "claude-transcript", "stop_hook_active": False, "transcript_path": str(transcript)})
        assert claude_turn("Edit", "mcp__knowledgetrees__kt_rewrite") == {}
        assert claude_turn("Edit", "Bash", "Read") == {}, "shell kt writes count and reads do not undo them"
        assert claude_turn("mcp__knowledgetrees__kt_edit", "Write")["decision"] == "block", "code edits after the tree write"
        assert claude_turn()["decision"] == "block", "direction-only turns still get a reminder"
        assert run("claude", "stop", {"session_id": "claude-transcript", "stop_hook_active": False,
                                      "transcript_path": str(Path(temporary) / "missing.jsonl")})["decision"] == "block"

        def codex_turn(*inputs):
            entries = [{"type": "event_msg", "payload": {"type": "task_started"}}]
            entries += [{"type": "response_item", "payload": {"type": "custom_tool_call", "name": "exec", "input": text}} for text in inputs]
            transcript.write_text("\n".join(map(json.dumps, entries)) + "\n")
            return run("codex", "stop", {"session_id": "codex-transcript", "stop_hook_active": False, "transcript_path": str(transcript)})
        assert codex_turn("*** Begin Patch", '{"method":"tools/call","params":{"name":"kt_edit"}}') == {}
        assert codex_turn('{"name":"kt_edit"}', "apply_patch <<EOF")["decision"] == "block"
        assert codex_turn("ls kt_editor_notes")["decision"] == "block", "only exact kt tool names count"
        assert run("opencode", "stop", {"sessionID": "oc-tools", "tools": [{"name": "edit"}, {"name": "knowledgetrees_kt_rewrite"}]}) == {}
        del env["KT_HOOK_MAINTENANCE_INTERVAL"]
        assert run("codex", "after", {"session_id": "silent", "tool_response": ""}) == {}
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
