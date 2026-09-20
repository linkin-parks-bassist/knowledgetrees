#!/usr/bin/env python3
"""MCP server protocol and structured-edit tests; no models."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

REPOSITORY = Path(__file__).resolve().parents[1]
SERVER = REPOSITORY / "tools/kt-mcp"
PROTOCOL = "2025-06-18"
KT = REPOSITORY / "tools/kt"


def main():
    with tempfile.TemporaryDirectory(prefix="kt mcp test ") as temporary:
        root = Path(temporary)
        global_root = root / "global"
        global_root.mkdir()
        (global_root / "how/to/use").mkdir(parents=True)
        (global_root / "how/to/use/knowledgetrees.md").write_text("Canonical procedure fixture.\n")
        vaults = {}
        for name in ("vault", "vault2", "vault3", "locked", "hidden", "extra"):
            vaults[name] = root / name
            (vaults[name] / "how/to").mkdir(parents=True)
            (vaults[name] / "how/to/read.md").write_text(f"---\nstatus: green\n---\n\nSECRET-{name} lives here.\n")
        policies = {"vault": "ask", "vault2": "ask", "vault3": "ask", "locked": "deny", "hidden": "force-private", "extra": "ask"}
        (root / "config.json").write_text(json.dumps({"roots": {
            "global": {"path": str(global_root), "access": "allow"},
            **{name: {"path": str(vaults[name]), "access": access} for name, access in policies.items()}}, "projects": {}}))
        project = root / "project"
        (project / ".knowledge").mkdir(parents=True)
        env = {**os.environ, "KT_GLOBAL_ROOT": str(global_root), "KT_CONFIG": str(root / "config.json"),
               "KT_MCP_CLI": str(KT)}
        subprocess.run([sys.executable, str(KT), "add", "what is the fixture", "Alpha line.\nBeta line.\nBeta line.\n"],
                       cwd=project, env=env, check=True, capture_output=True)
        address = "local:what/is/the/fixture.md"
        base_extra = vaults["extra"]

        server = subprocess.Popen([sys.executable, str(SERVER)], cwd=project, env=env, text=True,
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        counter = iter(range(1, 1000))

        def rpc(method, params=None, notify=False):
            message = {"jsonrpc": "2.0", "method": method, **({"params": params} if params is not None else {})}
            if not notify:
                message["id"] = next(counter)
            server.stdin.write(json.dumps(message) + "\n")
            server.stdin.flush()
            return None if notify else json.loads(server.stdout.readline())

        def tool(name, **arguments):
            result = rpc("tools/call", {"name": name, "arguments": arguments})["result"]
            return result["isError"], result["content"][0]["text"]

        initialized = rpc("initialize", {"protocolVersion": "2025-03-26", "capabilities": {}})
        assert initialized["result"]["protocolVersion"] == "2025-03-26"
        assert "tools" in initialized["result"]["capabilities"]
        assert rpc("notifications/initialized", notify=True) is None
        assert rpc("ping")["result"] == {}
        names = {t["name"] for t in rpc("tools/list")["result"]["tools"]}
        assert names == {"kt_info", "kt_lookup", "kt_find", "kt_grep", "kt_read", "kt_edit", "kt_rewrite", "kt_undo",
                         "kt_add", "kt_dict", "kt_roots", "kt_prove", "kt_status", "kt_access_status", "kt_access_request",
                         "kt_access_revoke"}
        listed = {t["name"]: t for t in rpc("tools/list")["result"]["tools"]}
        for name, definition in listed.items():
            hints = definition["annotations"]
            assert set(hints) >= {"readOnlyHint", "destructiveHint", "idempotentHint", "openWorldHint"} and not hints["openWorldHint"], name
        for name in ("kt_lookup", "kt_find", "kt_grep", "kt_read", "kt_dict", "kt_roots", "kt_status", "kt_access_status"):
            assert listed[name]["annotations"]["readOnlyHint"] and not listed[name]["annotations"]["destructiveHint"], name
        for name in ("kt_edit", "kt_rewrite", "kt_undo"):
            assert not listed[name]["annotations"]["readOnlyHint"] and listed[name]["annotations"]["destructiveHint"], name
        assert not listed["kt_add"]["annotations"]["destructiveHint"] and not listed["kt_add"]["annotations"]["readOnlyHint"]
        assert "instructions" in initialized["result"] and "kt_access_request" in initialized["result"]["instructions"]
        assert not [n for n, t in listed.items() if len(json.dumps(t)) > 1800], "tool schemas must stay compact"
        assert rpc("nope")["error"]["code"] == -32601
        server.stdin.write("{broken\n")
        server.stdin.flush()
        assert json.loads(server.stdout.readline())["error"]["code"] == -32700

        error, text = tool("kt_read", address=address)
        assert not error and "Alpha line." in text
        revision = text.splitlines()[0].split()[1]
        leaf = project / ".knowledge/what/is/the/fixture.md"
        inode = leaf.stat().st_ino

        error, text = tool("kt_edit", address=address, revision=revision, old_text="Beta line.", new_text="Gamma line.")
        assert error and "2 matches" in text and "Gamma" not in leaf.read_text()
        error, text = tool("kt_edit", address=address, revision=revision, old_text="missing", new_text="x")
        assert error and "0 matches" in text
        error, text = tool("kt_edit", address=address, revision=revision, old_text="status:", new_text="x")
        assert error and "front matter" in text
        error, text = tool("kt_edit", address=address, revision=revision, old_text="", new_text="x")
        assert error
        error, text = tool("kt_edit", address=address, revision="0" * 64, old_text="Alpha", new_text="x")
        assert error and "changed" in text
        error, text = tool("kt_edit", address=address, revision=revision, old_text="Alpha line.", new_text="Omega line.",
                           dry_run=True)
        assert not error and "Omega" in text and "Omega" not in leaf.read_text()

        error, text = tool("kt_edit", address=address, revision=revision, old_text="Alpha line.", new_text="Omega line.")
        assert not error and "+Omega line." in text
        assert "Omega line.\nBeta line." in leaf.read_text() and leaf.stat().st_ino == inode
        new_revision = text.splitlines()[0].split()[1]
        assert new_revision != revision
        error, text = tool("kt_edit", address=address, revision=revision, old_text="Omega", new_text="Stale")
        assert error and "changed" in text, "the pre-edit revision is stale"
        assert "Stale" not in leaf.read_text()

        error, text = tool("kt_rewrite", address=address, revision=new_revision, body="Whole new body.\n")
        assert not error and "Whole new body." in leaf.read_text() and "Omega" not in leaf.read_text()
        assert leaf.read_text().startswith("---\n"), "front matter survives"
        error, text = tool("kt_rewrite", address=address, revision=new_revision, body="stale rewrite\n")
        assert error
        error, text = tool("kt_read", address="local:no/such/leaf.md")
        assert error
        assert rpc("tools/call", {"name": "kt_delete", "arguments": {}})["result"]["isError"]

        # Retrieval, creation, and inspection tools wrap the same CLI semantics.
        error, text = tool("kt_lookup", question="what is the fixture")
        assert not error and "Whole new body." in text
        error, text = tool("kt_lookup", question="-h what is")
        assert error and "must not start" in text
        error, text = tool("kt_find", terms="Whole body", limit=2)
        assert not error and "local:what/is/the/fixture.md" in text
        error, text = tool("kt_find", terms="zzzunfindablezzz")
        assert not error and "no_matches" in text and "(exit 1)" in text, "a miss is data, not a tool error"
        error, text = tool("kt_find", terms="--help")
        assert error
        error, text = tool("kt_add", question="how to bake the fixture", answer="- Preheat.\n- Bake.\n", dry_run=True)
        assert not error and "Preheat." in text
        assert not (project / ".knowledge/how/to/bake/the/fixture.md").exists(), "dry run must not write"
        error, text = tool("kt_add", question="how to bake the fixture", answer="- Preheat.\n- Bake.\n")
        created = project / ".knowledge/how/to/bake/the/fixture.md"
        assert not error and created.is_file() and "- Preheat." in created.read_text()
        error, text = tool("kt_add", question="how to bake the fixture", answer="Duplicate.\n")
        assert error, "an existing owner must not be overwritten"
        assert "Preheat" in created.read_text() and "Duplicate" not in created.read_text()
        error, text = tool("kt_add", question="-x how to", answer="a")
        assert error
        error, text = tool("kt_add", question="how to be global", answer="Global answer.\n", scope="global")
        assert not error and (global_root / "how/to/be/global.md").is_file()
        error, text = tool("kt_add", question="how to be sloppy", answer="-")
        assert error
        error, text = tool("kt_add", question="how to nowhere", answer="x", scope="elsewhere")
        assert error
        error, text = tool("kt_dict")
        assert not error and "fixture" in text
        error, text = tool("kt_dict", roots=["local"])
        assert not error and "fixture" in text
        error, text = tool("kt_roots")
        assert not error and str(project / ".knowledge") in text
        before = created.read_text()
        error, text = tool("kt_prove", scope="local")
        assert not error and "brown=0" in text and created.read_text() == before, "default prove must not stamp"
        error, text = tool("kt_prove", scope="galaxy")
        assert error

        # ---- kt_info, kt_grep, kt_status, ranged reads, multi-edit, undo, JSON find, access status
        error, text = tool("kt_status", scope="local")
        assert not error and "local:how/to/bake/the/fixture.md" in text and "created or rewritten" in text
        error, text = tool("kt_status", scope="nowhere")
        assert error
        error, text = tool("kt_info")
        assert not error and "Canonical procedure fixture." in text and "=== kt prove --local ===" in text
        error, text = tool("kt_status", scope="local")
        assert "local:how/to/bake/the/fixture.md" not in text, "kt_info's proof pass stamped the leaves green"
        error, text = tool("kt_grep", pattern="Whole new body")
        assert not error and "local:what/is/the/fixture.md:" in text and "Whole new body." in text
        error, text = tool("kt_grep", pattern=r"Whole \w+ body", regex=True, files_only=True)
        assert not error and text.strip() == "local:what/is/the/fixture.md"
        error, text = tool("kt_grep", pattern="whole NEW body", ignore_case=True, context=1, limit=5)
        assert not error and "Whole new body." in text
        error, text = tool("kt_grep", pattern="zzznope")
        assert not error and "no_matches" in text and "(exit 1)" in text
        error, text = tool("kt_grep", pattern="-x-dash")
        assert not error and "no_matches" in text, "a leading dash is data, not an option"
        error, text = tool("kt_grep", pattern="(", regex=True)
        assert error and "invalid regular expression" in text
        error, text = tool("kt_grep", pattern="")
        assert error
        error, text = tool("kt_grep", pattern="x", limit=0)
        assert error

        error, text = tool("kt_read", address=address, body_only=True)
        assert not error and "status:" not in text and "Whole new body." in text
        error, text = tool("kt_read", address=address, offset=2, limit=5)
        assert not error and "characters 2-7 of" in text
        error, text = tool("kt_read", address=address, limit=0)
        assert error
        error, text = tool("kt_read", address=address, offset=True)
        assert error, "booleans are not integers"

        error, text = tool("kt_read", address=address)
        revision = text.splitlines()[0].split()[1]
        error, text = tool("kt_rewrite", address=address, revision=revision, body="Line one.\nLine two.\nLine three.\n")
        assert not error
        revision = text.splitlines()[0].split()[1]
        original = leaf.read_text()
        error, text = tool("kt_edit", address=address, revision=revision, edits=[
            {"old_text": "Line one.", "new_text": "First."}, {"old_text": "Line missing.", "new_text": "x"}])
        assert error and "edit 2:" in text and "0 matches" in text and leaf.read_text() == original, "multi-edit is atomic"
        error, text = tool("kt_edit", address=address, revision=revision, edits=[], old_text="a", new_text="b")
        assert error
        error, text = tool("kt_edit", address=address, revision=revision, old_text="Line one.", new_text="X", edits=[
            {"old_text": "Line two.", "new_text": "Y"}])
        assert error and "either" in text
        error, text = tool("kt_edit", address=address, revision=revision, edits=[
            {"old_text": "Line one.", "new_text": "First."}, {"old_text": "First.", "new_text": "Primary."},
            {"old_text": "Line three.", "new_text": "Third."}])
        assert not error, text
        assert "Primary.\nLine two.\nThird." in leaf.read_text(), "edits apply in order against the running body"
        edited_revision = text.splitlines()[0].split()[1]

        error, text = tool("kt_undo", address=address, dry_run=True)
        assert not error and "Line one." in text and "Primary." in leaf.read_text()
        error, text = tool("kt_undo", address=address)
        assert not error and "Line one.\nLine two.\nLine three." in leaf.read_text() and "Primary." not in leaf.read_text()
        error, text = tool("kt_read", address=address)
        revision = text.splitlines()[0].split()[1]
        error, text = tool("kt_edit", address=address, revision=revision, old_text="Line two.", new_text="Second.")
        assert not error
        leaf.write_text(leaf.read_text() + "\nHand edit.\n")
        error, text = tool("kt_undo", address=address)
        assert error and "changed after the recorded edit" in text and "Hand edit." in leaf.read_text(), "undo never clobbers later work"
        error, text = tool("kt_undo", address="local:no/such/leaf.md")
        assert error

        result = rpc("tools/call", {"name": "kt_find", "arguments": {"terms": "Line", "json": True, "limit": 3}})["result"]
        assert not result["isError"] and result["structuredContent"]["exit"] in (0, 1)
        assert json.loads(result["content"][0]["text"]) == result["structuredContent"]
        found_items = result["structuredContent"]["results"]
        assert any(item["address"] == "local:what/is/the/fixture.md" and item["status"] in ("green", "yellow", "brown")
                   and isinstance(item["coverage"], int) for item in found_items), found_items
        plain = rpc("tools/call", {"name": "kt_find", "arguments": {"terms": "Line"}})["result"]
        assert "structuredContent" not in plain

        error, text = tool("kt_access_status")
        assert not error and "kt_access_request" in text and str(vaults["vault"]) in text
        error, text = tool("kt_access_status", root=str(vaults["vault"]))
        assert not error and "ask" in text and "kt_access_request" in text
        error, text = tool("kt_access_status", root=str(vaults["hidden"]))
        assert not error and "unavailable" in text
        error, text = tool("kt_access_status", root="-x")
        assert error
        error, text = tool("kt_access_status")
        assert "local tree" in text and "allowed everywhere" in text and "Give back access" in text, text
        error, text = tool("kt_access_revoke", root="local")
        assert error and "local tree" in text
        error, text = tool("kt_access_revoke", root=str(vaults["hidden"]))
        assert error and "unavailable" in text and "hidden" not in text
        error, text = tool("kt_access_revoke", root="-x")
        assert error
        error, text = tool("kt_access_revoke", root=str(vaults["vault"]), scope="galaxy")
        assert error
        error, text = tool("kt_access_revoke", root=str(vaults["vault"]))
        assert not error and "nothing to revoke" in text, "an already-restricted root has nothing to revoke"
        error, text = tool("kt_access_revoke", root=str(vaults["vault"]), scope="all")
        assert not error and "cannot show confirmation prompts" in text and f"kt access {vaults['vault']} revoke --scope all" in text
        error, text = tool("kt_access_revoke", root="global")
        assert not error and "cannot show confirmation prompts" in text, "revoking the global root always needs the user"
        assert json.loads((root / "config.json").read_text())["roots"]["vault"]["access"] == "ask", "no change without the user"
        error, text = tool("kt_access_status", root="relative/path")
        assert error

        # Without a client that can prompt, a request returns the terminal command and grants nothing.
        error, text = tool("kt_access_request", root=str(vaults["vault"]), reason="need the vault")
        assert not error and f"kt access {vaults['vault']} allow --scope project" in text and "cannot show approval prompts" in text
        error, text = tool("kt_access_request", root=str(vaults["locked"]), reason="please")
        assert error and "denied" in text and "Do not work around" in text
        error, text = tool("kt_access_request", root=str(vaults["hidden"]), reason="please")
        assert error and "unavailable" in text and "hidden" not in text
        error, text = tool("kt_access_request", root="global", reason="already open")
        assert not error and "already readable" in text
        error, text = tool("kt_access_request", root="-x", reason="x")
        assert error
        assert '"projects": {}' in (root / "config.json").read_text().replace("\n", "").replace("  ", "") or \
            json.loads((root / "config.json").read_text())["projects"] == {}, "no grant without the user"

        listed_prompts = {p["name"]: p for p in rpc("prompts/list")["result"]["prompts"]}
        assert set(listed_prompts) == {"capture_review", "garden", "verify_leaf", "revoke_access"}
        got = rpc("prompts/get", {"name": "capture_review"})["result"]["messages"][0]["content"]["text"]
        assert "Knowledge-tree capture review" in got
        got = rpc("prompts/get", {"name": "verify_leaf", "arguments": {"address": address}})["result"]["messages"][0]["content"]["text"]
        assert address in got and "kt_grep" in got
        assert rpc("prompts/get", {"name": "verify_leaf"})["error"]["code"] == -32602
        assert rpc("prompts/get", {"name": "nope"})["error"]["code"] == -32602
        server.stdin.close()
        assert server.wait(timeout=10) == 0

        # A user-scoped Claude server may start outside the project. Its
        # project environment must select the local tree before any tool call.
        remote = subprocess.Popen([sys.executable, str(SERVER)], cwd=root,
                                  env={**env, "CLAUDE_PROJECT_DIR": str(project)}, text=True,
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        request = {"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                   "params": {"name": "kt_read", "arguments": {"address": address}}}
        remote.stdin.write(json.dumps(request) + "\n")
        remote.stdin.flush()
        response = json.loads(remote.stdout.readline())["result"]
        assert not response["isError"] and "Hand edit." in response["content"][0]["text"]
        remote.stdin.close()
        assert remote.wait(timeout=10) == 0

        # ---- elicitation: the user, not the model, answers approval prompts through the harness
        def start_client(capabilities, extra_env=None):
            process = subprocess.Popen([sys.executable, str(SERVER)], cwd=project, env={**env, **(extra_env or {})}, text=True,
                                       stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            def send(message):
                process.stdin.write(json.dumps(message) + "\n")
                process.stdin.flush()

            def receive():
                return json.loads(process.stdout.readline())
            send({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": PROTOCOL, "capabilities": capabilities}})
            assert receive()["id"] == 1
            send({"jsonrpc": "2.0", "method": "notifications/initialized"})
            return process, send, receive

        client, send, receive = start_client({"elicitation": {}})
        request_id = iter(range(100, 1000))

        def ask(root_path, reason="need it"):
            identifier = next(request_id)
            send({"jsonrpc": "2.0", "id": identifier, "method": "tools/call",
                  "params": {"name": "kt_access_request", "arguments": {"root": str(root_path), "reason": reason}}})
            return identifier

        def grants():
            return json.loads((root / "config.json").read_text())

        # Accept for this directory only.
        identifier = ask(vaults["vault"], "line1\nline2\x07" + "x" * 400)
        prompt = receive()
        assert prompt["method"] == "elicitation/create" and prompt["id"].startswith("kt-elicit-")
        assert str(vaults["vault"]) in prompt["params"]["message"] and str(project.resolve()) in prompt["params"]["message"]
        reason_line = next(line for line in prompt["params"]["message"].splitlines() if line.startswith("Reason (from the agent):"))
        assert "line1 line2 xxx" in reason_line and "\x07" not in prompt["params"]["message"] and len(reason_line) < 400
        schema = prompt["params"]["requestedSchema"]["properties"]["decision"]
        assert schema["enum"] == ["project", "project_and_subdirectories", "all"] and len(schema["enumNames"]) == 3
        assert "SECRET-vault" not in json.dumps(prompt), "the prompt never leaks the root's contents"
        send({"jsonrpc": "2.0", "id": "ping-1", "method": "ping"})
        assert receive() == {"jsonrpc": "2.0", "id": "ping-1", "result": {}}, "pings are answered mid-prompt"
        send({"jsonrpc": "2.0", "id": 99, "method": "tools/list"})  # arrives while the user is deciding
        assert grants()["projects"] == {}, "nothing is granted before the user answers"
        send({"jsonrpc": "2.0", "id": prompt["id"], "result": {"action": "accept", "content": {"decision": "project"}}})
        outcome = receive()
        assert outcome["id"] == identifier and not outcome["result"]["isError"] and "approved" in outcome["result"]["content"][0]["text"]
        deferred = receive()
        assert deferred["id"] == 99 and len(deferred["result"]["tools"]) == 16, "a request that arrived mid-prompt is still served"
        assert grants()["projects"][str(project.resolve())][str(vaults["vault"].resolve())] == "allow"
        identifier = next(request_id)
        send({"jsonrpc": "2.0", "id": identifier, "method": "tools/call",
              "params": {"name": "kt_grep", "arguments": {"pattern": "SECRET-vault"}}})
        assert "SECRET-vault lives here." in receive()["result"]["content"][0]["text"], "the approved root is now searchable"
        identifier = ask(vaults["vault"])
        assert receive()["id"] == identifier, "an already-approved root needs no prompt"

        # Accept with subdirectories, and everywhere.
        identifier = ask(vaults["vault2"])
        prompt = receive()
        send({"jsonrpc": "2.0", "id": prompt["id"], "result": {"action": "accept", "content": {"decision": "project_and_subdirectories"}}})
        assert receive()["id"] == identifier
        assert grants()["projects"][str(project.resolve())][str(vaults["vault2"].resolve())] == {"access": "allow", "subdirectories": True}
        identifier = ask(vaults["vault3"])
        prompt = receive()
        send({"jsonrpc": "2.0", "id": prompt["id"], "result": {"action": "accept", "content": {"decision": "all"}}})
        assert receive()["id"] == identifier
        assert grants()["roots"]["vault3"]["access"] == "allow"

        # ---- revocation: narrowing this directory is direct; anything wider needs the user
        def call(name, **arguments):
            identifier = next(request_id)
            send({"jsonrpc": "2.0", "id": identifier, "method": "tools/call", "params": {"name": name, "arguments": arguments}})
            return identifier

        def outcome(identifier):
            reply = receive()
            assert reply["id"] == identifier, reply
            return reply["result"]["isError"], reply["result"]["content"][0]["text"]
        here = str(project.resolve())
        identifier = call("kt_access_status", root=str(vaults["vault"]))
        error, text = outcome(identifier)
        assert not error and "project grant" in text and "kt_access_revoke" in text
        identifier = call("kt_access_revoke", root=str(vaults["vault"]))
        error, text = outcome(identifier)  # no prompt was sent: the reply arrives directly
        assert not error and "requires approval again in this project" in text and "prompt the user" in text
        assert str(vaults["vault"].resolve()) not in grants()["projects"].get(here, {})
        identifier = call("kt_grep", pattern="SECRET-vault lives")
        error, text = outcome(identifier)
        assert "no_matches" in text, "revoked access takes effect immediately"
        identifier = call("kt_access_revoke", root=str(vaults["vault2"]))  # made "and subdirectories" for this directory
        error, text = outcome(identifier)
        assert not error and "requires approval again" in text
        assert str(vaults["vault2"].resolve()) not in grants()["projects"].get(here, {})
        identifier = call("kt_access_revoke", root=str(vaults["vault3"]))  # allowed everywhere: overridden here only
        error, text = outcome(identifier)
        assert not error and grants()["projects"][here][str(vaults["vault3"].resolve())] == "ask"
        assert grants()["roots"]["vault3"]["access"] == "allow", "other projects are unaffected"
        for answer in ({"action": "decline"}, {"action": "accept", "content": {"confirm": False}}, {"action": "cancel"}):
            before = grants()
            identifier = call("kt_access_revoke", root=str(vaults["vault3"]), scope="all")
            prompt = receive()
            assert prompt["method"] == "elicitation/create" and "Effect:" in prompt["params"]["message"]
            assert prompt["params"]["requestedSchema"]["properties"]["confirm"]["type"] == "boolean"
            send({"jsonrpc": "2.0", "id": prompt["id"], "result": answer})
            error, text = outcome(identifier)
            assert not error and "declined" in text and grants() == before, "anything but a confirmed accept changes nothing"
        identifier = call("kt_access_revoke", root=str(vaults["vault3"]), scope="all")
        prompt = receive()
        send({"jsonrpc": "2.0", "id": prompt["id"], "result": {"action": "accept", "content": {"confirm": True}}})
        error, text = outcome(identifier)
        assert not error and "in every project" in text
        assert grants()["roots"]["vault3"]["access"] == "ask" and here not in grants()["projects"]
        identifier = call("kt_access_revoke", root="global")  # the global root needs the user even for one project
        prompt = receive()
        assert prompt["method"] == "elicitation/create"
        send({"jsonrpc": "2.0", "id": prompt["id"], "result": {"action": "decline"}})
        error, text = outcome(identifier)
        assert "declined" in text and grants()["roots"]["global"]["access"] == "allow"

        # Denied and force-private roots never reach the user.
        for refused in ("locked", "hidden"):
            identifier = ask(vaults[refused])
            reply = receive()
            assert reply["id"] == identifier and reply["result"]["isError"], "no prompt may be sent for " + refused
        client.stdin.close()
        assert client.wait(timeout=10) == 0

        # Decline, cancel, invalid answers, and refusal to nag.
        for answer in ({"action": "decline"}, {"action": "cancel"}):
            client, send, receive = start_client({"elicitation": {}})
            before = grants()
            identifier = ask(base_extra)
            prompt = receive()
            send({"jsonrpc": "2.0", "id": prompt["id"], "result": answer})
            reply = receive()
            assert "declined" in reply["result"]["content"][0]["text"] and grants() == before
            identifier = ask(base_extra)
            reply = receive()
            assert reply["id"] == identifier and "earlier in this session" in reply["result"]["content"][0]["text"], \
                "a declined root is not asked about again"
            client.stdin.close()
            assert client.wait(timeout=10) == 0
        client, send, receive = start_client({"elicitation": {}})
        before = grants()
        identifier = ask(base_extra)
        prompt = receive()
        send({"jsonrpc": "2.0", "id": prompt["id"], "result": {"action": "accept", "content": {"decision": "everything"}}})
        reply = receive()
        assert reply["result"]["isError"] and "nothing was granted" in reply["result"]["content"][0]["text"] and grants() == before
        client.stdin.close()
        assert client.wait(timeout=10) == 0

        # A client without the elicitation capability gets the terminal command instead of a prompt.
        client, send, receive = start_client({})
        identifier = ask(base_extra)
        reply = receive()
        assert reply["id"] == identifier and "kt access" in reply["result"]["content"][0]["text"]
        client.stdin.close()
        assert client.wait(timeout=10) == 0
    print("mcp server checks passed")


if __name__ == "__main__":
    main()
