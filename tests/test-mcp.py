#!/usr/bin/env python3
"""MCP server protocol and structured-edit tests; no models."""
import json
import os
from pathlib import Path
import re
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

        def tool(tool_name, **arguments):
            result = rpc("tools/call", {"name": tool_name, "arguments": arguments})["result"]
            return result["isError"], result["content"][0]["text"]

        initialized = rpc("initialize", {"protocolVersion": "2025-03-26", "capabilities": {}})
        assert initialized["result"]["protocolVersion"] == "2025-03-26"
        assert "tools" in initialized["result"]["capabilities"]
        assert rpc("notifications/initialized", notify=True) is None
        assert rpc("ping")["result"] == {}
        names = {t["name"] for t in rpc("tools/list")["result"]["tools"]}
        assert names == {"kt_info", "kt_lookup", "kt_find", "kt_grep", "kt_read", "kt_rewrite", "kt_edit", "kt_undo",
                         "kt_add", "kt_rm", "kt_mv", "kt_combine", "kt_init", "kt_renew", "kt_dict", "kt_roots",
                         "kt_register", "kt_prove", "kt_status", "kt_access_status", "kt_access_request",
                         "kt_access_confirm", "kt_access_revoke"}
        listed = {t["name"]: t for t in rpc("tools/list")["result"]["tools"]}
        for name, definition in listed.items():
            hints = definition["annotations"]
            assert set(hints) >= {"readOnlyHint", "destructiveHint", "idempotentHint", "openWorldHint"} and not hints["openWorldHint"], name
        for name in ("kt_lookup", "kt_find", "kt_grep", "kt_read", "kt_dict", "kt_roots", "kt_status", "kt_access_status"):
            assert listed[name]["annotations"]["readOnlyHint"] and not listed[name]["annotations"]["destructiveHint"], name
        for name in ("kt_rewrite", "kt_edit", "kt_undo", "kt_rm", "kt_mv", "kt_combine"):
            assert not listed[name]["annotations"]["readOnlyHint"] and listed[name]["annotations"]["destructiveHint"], name
        assert not listed["kt_renew"]["annotations"]["destructiveHint"] and not listed["kt_renew"]["annotations"]["readOnlyHint"]
        assert not listed["kt_add"]["annotations"]["destructiveHint"] and not listed["kt_add"]["annotations"]["readOnlyHint"]
        assert not listed["kt_init"]["annotations"]["destructiveHint"] and not listed["kt_init"]["annotations"]["readOnlyHint"]
        assert set(listed["kt_init"]["inputSchema"]["properties"]) == {"orientation", "project"}
        assert not listed["kt_register"]["annotations"]["destructiveHint"] and not listed["kt_register"]["annotations"]["readOnlyHint"]
        assert set(listed["kt_read"]["inputSchema"]["properties"]) == {"address"}, "whole reads have no range or paging parameters"
        assert "instructions" in initialized["result"] and "kt_access_request" in initialized["result"]["instructions"]
        assert "kt_renew" in initialized["result"]["instructions"] and "shell" in initialized["result"]["instructions"]
        assert "priority-one incident" in initialized["result"]["instructions"]
        assert "startup with no user task" in initialized["result"]["instructions"]
        assert "explicitly permits ignoring that specific status" in initialized["result"]["instructions"]
        assert not [n for n, t in listed.items() if len(json.dumps(t)) > 1800], "tool schemas must stay compact"
        assert rpc("nope")["error"]["code"] == -32601
        server.stdin.write("{broken\n")
        server.stdin.flush()
        assert json.loads(server.stdout.readline())["error"]["code"] == -32700

        error, text = tool("kt_edit", address=address, old_text="Alpha", new_text="x")
        assert error and "read this leaf first" in text, "an edit needs a read in this session"
        error, text = tool("kt_read", address=address)
        assert not error and "Alpha line." in text and "status:" not in text and "revised_at" not in text
        revision = re.search(r"^Revision: ([a-f0-9]{64})$", text, re.M).group(1)
        assert text.count("Revision:") == 1
        leaf = project / ".knowledge/what/is/the/fixture.md"
        inode = leaf.stat().st_ino

        error, text = tool("kt_rewrite", address=address, revision=revision,
                           answer="Alpha line.\nBeta line.\nBeta line.\n", dry_run=True)
        assert not error and text == "No change." and "revised_at" not in text
        error, text = tool("kt_rewrite", address=address, revision="bad", answer="No.")
        assert error and "64-character" in text

        error, text = tool("kt_edit", address=address, old_text="Beta line.", new_text="Gamma line.")
        assert error and "2 matches" in text and "Gamma" not in leaf.read_text()
        error, text = tool("kt_edit", address=address, old_text="missing", new_text="x")
        assert error and "0 matches" in text
        error, text = tool("kt_edit", address=address, old_text="status:", new_text="x")
        assert error and "0 matches" in text, "front matter is not part of the answer"
        error, text = tool("kt_edit", address=address, old_text="", new_text="x")
        assert error
        error, text = tool("kt_edit", address=address, old_text="Alpha line.", new_text="Omega line.", dry_run=True)
        assert not error and "+Omega line." in text and "Omega" not in leaf.read_text() and "revised_at" not in text

        error, text = tool("kt_edit", address=address, old_text="Alpha line.", new_text="Omega line.")
        assert not error and "+Omega line." in text and "revised_at" not in text
        assert "Omega line.\nBeta line." in leaf.read_text() and leaf.stat().st_ino == inode
        assert 'status: "green"' in leaf.read_text(), "an edit keeps the leaf's status"
        error, text = tool("kt_rewrite", address=address, revision=revision, answer="Stale overwrite.")
        assert error and "stale" in text and "Stale overwrite" not in leaf.read_text()
        error, text = tool("kt_edit", address=address, old_text="Omega line.", new_text="Alpha again.")
        assert not error, "an edit updates what this session has seen, so edits chain without a re-read"

        def external_edit(new_body):
            """A change made outside this server (another agent, the shell)."""
            digest = subprocess.run([sys.executable, str(KT), "open", address], cwd=project, env=env, capture_output=True,
                                    text=True).stderr.split()[-1]
            subprocess.run([sys.executable, str(KT), "rewrite", address, digest, new_body], cwd=project, env=env, check=True)
        external_edit("External body.\nBeta line.\nBeta line.\n")
        error, text = tool("kt_edit", address=address, old_text="Beta", new_text="x")
        assert error and "changed since you read it" in text and "External body." in leaf.read_text()
        error, text = tool("kt_read", address=address)
        assert not error and "External body." in text

        error, text = tool("kt_edit", address=address, edits=[
            {"old_text": "External body.\nBeta line.\nBeta line.", "new_text": "Whole new body."}])
        assert not error and "Whole new body." in leaf.read_text() and "External" not in leaf.read_text()
        assert leaf.read_text().startswith("---\n"), "front matter survives"
        error, text = tool("kt_read", address="local:no/such/leaf.md")
        assert error
        error, text = tool("kt_init")
        assert error and "exists" in text.lower(), "init refuses an existing tree"
        error, text = tool("kt_add", question="what is movable", answer="Move me.", scope="local")
        assert not error
        error, text = tool("kt_read", address="local:what/is/movable.md")
        move_revision = re.search(r"^Revision: ([a-f0-9]{64})$", text, re.M).group(1)
        error, text = tool("kt_mv", source="local:what/is/movable.md", destination="local:what/is/moved.md",
                           revision=move_revision, dry_run=True)
        assert not error and (project / ".knowledge/what/is/movable.md").exists()
        error, text = tool("kt_mv", source="local:what/is/movable.md", destination="local:what/is/moved.md",
                           revision=move_revision)
        assert not error and (project / ".knowledge/what/is/moved.md").exists()
        error, text = tool("kt_read", address="local:what/is/moved.md")
        remove_revision = re.search(r"^Revision: ([a-f0-9]{64})$", text, re.M).group(1)
        error, text = tool("kt_rm", address="local:what/is/moved.md", revision=remove_revision, dry_run=True)
        assert not error and (project / ".knowledge/what/is/moved.md").exists()
        error, text = tool("kt_rm", address="local:what/is/moved.md", revision=remove_revision)
        assert not error and not (project / ".knowledge/what/is/moved.md").exists()

        for question, answer in (("what is combine one", "First answer."), ("what is combine two", "Second answer.")):
            error, text = tool("kt_add", question=question, answer=answer)
            assert not error, text
        combined_sources = []
        for source in ("local:what/is/combine/one.md", "local:what/is/combine/two.md"):
            error, text = tool("kt_read", address=source)
            assert not error, text
            combined_sources.append({"address": source, "revision": re.search(r"^Revision: ([a-f0-9]{64})$", text, re.M).group(1)})
        combined_path = project / ".knowledge/what/is/combined.md"
        error, text = tool("kt_combine", sources=combined_sources, destination="local:what/is/combined.md", dry_run=True)
        assert not error and "First answer." in text and not combined_path.exists()
        aliased_sources = [combined_sources[0], {"address": "project:what/is/combine/one.md",
                                                "revision": combined_sources[0]["revision"]}]
        error, text = tool("kt_combine", sources=aliased_sources, destination="local:what/is/combined.md", dry_run=True)
        assert error and "duplicates" in text, "aliases of one source must not be combined twice"
        error, text = tool("kt_combine", sources=combined_sources,
                           destination="project:what/is/combine/one.md", dry_run=True)
        assert not error and "First answer." in text, "a destination alias of a source reuses its read revision"
        stale_sources = [dict(item) for item in combined_sources]
        stale_sources[0]["revision"] = "0" * 64
        error, text = tool("kt_combine", sources=stale_sources, destination="local:what/is/combined.md")
        assert error and "stale" in text and not combined_path.exists()
        error, text = tool("kt_combine", sources=combined_sources, destination="local:what/is/combined.md")
        assert not error and combined_path.exists() and "First answer.\n\nSecond answer." in combined_path.read_text()
        assert not (project / ".knowledge/what/is/combine/one.md").exists()

        registered = root / "registered"
        (registered / "where/am").mkdir(parents=True)
        (registered / "where/am/i.md").write_text("Registered fixture.\n")
        error, text = tool("kt_register", name="registered", path=str(registered))
        assert not error and "ask policy" in text
        assert json.loads((root / "config.json").read_text())["roots"]["registered"]["access"] == "ask"
        error, text = tool("kt_register", name="relative", path="relative/path")
        assert error and "absolute" in text
        error, text = tool("kt_add", question="what is the global mcp fixture", answer="Global MCP fixture.",
                           root=str(global_root))
        assert not error and (global_root / "what/is/the/global/mcp/fixture.md").exists()
        error, text = tool("kt_add", question="what is invalid scope", answer="No.", scope="local",
                           root=str(global_root))
        assert error and "either scope or root" in text
        error, text = tool("kt_prove", root=str(global_root))
        assert not error and "0 brown" in text
        error, text = tool("kt_status", root=str(global_root))
        assert not error and "0 brown" in text
        error, text = tool("kt_prove", scope="global", root=str(global_root))
        assert error and "either scope or root" in text
        assert rpc("tools/call", {"name": "kt_delete", "arguments": {}})["result"]["isError"]

        # Retrieval, creation, and inspection tools wrap the same CLI semantics.
        error, text = tool("kt_lookup", question="what is the fixture")
        assert not error and "Whole new body." in text and text.startswith(f"[{address}]") and "revised_at" not in text
        assert "kt: exact" not in text and re.search(r"^Revision: [a-f0-9]{64}$", text, re.M)
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
        assert not error and "0 brown" in text and "0 failed · SUCCESS" in text and created.read_text() == before, "default prove must not stamp"
        error, text = tool("kt_prove", scope="galaxy")
        assert error

        # ---- kt_info, kt_grep, kt_status, ranged reads, multi-edit, undo, JSON find, access status
        bake = "local:how/to/bake/the/fixture.md"
        error, text = tool("kt_read", address=bake)
        assert not error and text.startswith("- Preheat."), "a new leaf reads without any notice"
        error, text = tool("kt_status", scope="local")
        assert not error and bake not in text
        error, text = tool("kt_status", scope="nowhere")
        assert error
        stale = project / ".knowledge/what/is/stale.md"
        stale.write_text("---\nstatus: green\nrevised_at: '2026-01-01T00:00:00+00:00'\n"
                         "expires_at: '2026-02-01T00:00:00+00:00'\n---\n\nA dated claim.\n")
        stale_address = "local:what/is/stale.md"
        error, text = tool("kt_renew", address=stale_address)
        assert error and "read this leaf first" in text, "renewing attests a read"
        error, text = tool("kt_read", address=stale_address)
        assert not error and text.startswith(f"kt: yellow leaf {stale_address}") and "kt_renew" in text and "A dated claim." in text
        assert "status:" not in text and "revised_at" not in text
        error, text = tool("kt_find", terms="dated claim")
        assert not error and f"{stale_address}\t" in text and "\tyellow\t" in text, "find names only non-green statuses"
        stale.write_text(stale.read_text() + "\nA hand tweak.\n")
        error, text = tool("kt_renew", address=stale_address)
        assert error and "changed since you read it" in text, "renewal is refused when the leaf changed after your read"
        error, text = tool("kt_read", address=stale_address)
        assert not error and "A hand tweak." in text
        error, text = tool("kt_renew", address=stale_address)
        assert not error and "Renewed" in text and "checked_at:" in stale.read_text()
        error, text = tool("kt_read", address=stale_address)
        assert not error and text.startswith("A dated claim."), "a renewed leaf reads without any notice"
        error, text = tool("kt_status", scope="local")
        assert stale_address not in text
        error, text = tool("kt_find", terms="dated claim")
        assert "yellow" not in text and "green" not in text
        error, text = tool("kt_info")
        assert not error and "Canonical procedure fixture." in text and "=== kt prove --local ===" in text
        error, text = tool("kt_status", scope="local")
        assert "local:how/to/bake/the/fixture.md" not in text
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

        error, text = tool("kt_read", address=address)
        assert not error and "status:" not in text and "Whole new body." in text

        external_edit("Line one.\nLine two.\nLine three.\n")
        error, text = tool("kt_read", address=address)
        original = leaf.read_text()
        error, text = tool("kt_edit", address=address, edits=[
            {"old_text": "Line one.", "new_text": "First."}, {"old_text": "Line missing.", "new_text": "x"}])
        assert error and "edit 2:" in text and "0 matches" in text and leaf.read_text() == original, "multi-edit is atomic"
        error, text = tool("kt_edit", address=address, edits=[], old_text="a", new_text="b")
        assert error
        error, text = tool("kt_edit", address=address, old_text="Line one.", new_text="X", edits=[
            {"old_text": "Line two.", "new_text": "Y"}])
        assert error and "either" in text
        error, text = tool("kt_edit", address=address, edits=[
            {"old_text": "Line one.", "new_text": "First."}, {"old_text": "First.", "new_text": "Primary."},
            {"old_text": "Line three.", "new_text": "Third."}])
        assert not error, text
        assert "Primary.\nLine two.\nThird." in leaf.read_text(), "edits apply in order against the running body"

        error, text = tool("kt_undo", address=address, dry_run=True)
        assert not error and "+Line one." in text and "Primary." in leaf.read_text()
        error, text = tool("kt_undo", address=address)
        assert not error and "Line one.\nLine two.\nLine three." in leaf.read_text() and "Primary." not in leaf.read_text()
        error, text = tool("kt_edit", address=address, old_text="Line two.", new_text="Second.")
        assert not error
        error, text = tool("kt_prove", scope="local", stamp=True)
        assert not error
        error, text = tool("kt_undo", address=address)
        assert not error and "Line two." in leaf.read_text(), "a status stamp is not a change to the answer, so undo still works"
        error, text = tool("kt_edit", address=address, old_text="Line two.", new_text="Second.")
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
        assert not error and "cannot show confirmation prompts" in text and "request_id kt-access-" in text
        error, text = tool("kt_access_revoke", root="global")
        assert not error and "cannot show confirmation prompts" in text, "revoking the global root always needs the user"
        assert json.loads((root / "config.json").read_text())["roots"]["vault"]["access"] == "ask", "no change without the user"
        error, text = tool("kt_access_status", root="relative/path")
        assert error

        # Without a client that can prompt, a request returns a one-time MCP continuation and grants nothing.
        error, text = tool("kt_access_request", root=str(vaults["vault"]), reason="need the vault")
        assert not error and "kt_access_confirm" in text and "cannot show approval prompts" in text
        pending_id = re.search(r"request_id: (kt-access-[A-Za-z0-9_-]+)", text).group(1)
        assert json.loads((root / "config.json").read_text())["projects"] == {}, "request alone never grants"
        error, text = tool("kt_access_confirm", request_id="unknown", scope="project")
        assert error and "unknown" in text
        error, text = tool("kt_access_confirm", request_id=pending_id, scope="project")
        assert not error and "explicit authorization" in text
        assert str(vaults["vault"].resolve()) in json.loads((root / "config.json").read_text())["projects"][str(project.resolve())]
        error, text = tool("kt_access_confirm", request_id=pending_id, scope="project")
        assert error and "already been used" in text
        error, text = tool("kt_access_revoke", root=str(vaults["vault"]))
        assert not error
        error, text = tool("kt_access_request", root=str(vaults["locked"]), reason="please")
        assert error and "denied" in text and "Do not work around" in text
        error, text = tool("kt_access_request", root=str(vaults["hidden"]), reason="please")
        assert error and "unavailable" in text and "hidden" not in text
        error, text = tool("kt_access_request", root="global", reason="already open")
        assert not error and "already readable" in text
        error, text = tool("kt_access_request", root="-x", reason="x")
        assert error
        assert json.loads((root / "config.json").read_text()).get("projects", {}) == {}, "revocation removed the test grant"

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
        assert deferred["id"] == 99 and len(deferred["result"]["tools"]) == 23, "a request that arrived mid-prompt is still served"
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
            assert not error and "did not confirm" in text and grants() == before, "anything but a confirmed accept changes nothing"
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
        assert "did not confirm" in text and grants()["roots"]["global"]["access"] == "allow"

        # Denied and force-private roots never reach the user.
        for refused in ("locked", "hidden"):
            identifier = ask(vaults[refused])
            reply = receive()
            assert reply["id"] == identifier and reply["result"]["isError"], "no prompt may be sent for " + refused
        client.stdin.close()
        assert client.wait(timeout=10) == 0

        # Decline, cancel, client errors, and invalid answers are reported without inventing a user refusal.
        for answer in ({"action": "decline"}, {"action": "cancel"}):
            client, send, receive = start_client({"elicitation": {}})
            before = grants()
            identifier = ask(base_extra)
            prompt = receive()
            send({"jsonrpc": "2.0", "id": prompt["id"], "result": answer})
            reply = receive()
            text = reply["result"]["content"][0]["text"]
            assert "MCP client" in text and "kt_access_confirm" in text and "user declined" not in text.lower() and grants() == before
            identifier = ask(base_extra)
            prompt = receive()
            assert prompt["method"] == "elicitation/create", "an unshown client decline must not suppress a later request"
            send({"jsonrpc": "2.0", "id": prompt["id"], "result": {"action": "cancel"}})
            assert receive()["id"] == identifier
            client.stdin.close()
            assert client.wait(timeout=10) == 0
        client, send, receive = start_client({"elicitation": {}})
        before = grants()
        identifier = ask(base_extra)
        prompt = receive()
        send({"jsonrpc": "2.0", "id": prompt["id"], "error": {"code": -32603, "message": "prompt unavailable"}})
        reply = receive()
        text = reply["result"]["content"][0]["text"]
        assert "prompt unavailable" in text and "kt_access_confirm" in text and grants() == before
        client.stdin.close()
        assert client.wait(timeout=10) == 0
        client, send, receive = start_client({"elicitation": {}})
        before = grants()
        identifier = ask(base_extra)
        prompt = receive()
        send({"jsonrpc": "2.0", "id": prompt["id"], "result": {"action": "accept", "content": {"decision": "everything"}}})
        reply = receive()
        invalid_text = reply["result"]["content"][0]["text"]
        assert not reply["result"]["isError"] and "invalid approval response" in invalid_text
        assert "kt_access_confirm" in invalid_text and grants() == before
        client.stdin.close()
        assert client.wait(timeout=10) == 0

        # A client without elicitation gets an MCP-native pending continuation instead of a shell command.
        client, send, receive = start_client({})
        identifier = ask(base_extra)
        reply = receive()
        fallback = reply["result"]["content"][0]["text"]
        assert reply["id"] == identifier and "kt_access_confirm" in fallback and "kt access" not in fallback
        pending_id = re.search(r"request_id: (kt-access-[A-Za-z0-9_-]+)", fallback).group(1)
        identifier = next(request_id)
        send({"jsonrpc": "2.0", "id": identifier, "method": "tools/call",
              "params": {"name": "kt_access_confirm", "arguments": {"request_id": pending_id, "scope": "project"}}})
        reply = receive()
        assert reply["id"] == identifier and not reply["result"]["isError"]
        assert grants()["projects"][str(project.resolve())][str(base_extra.resolve())] == "allow"
        identifier = next(request_id)
        send({"jsonrpc": "2.0", "id": identifier, "method": "tools/call",
              "params": {"name": "kt_access_revoke", "arguments": {"root": str(base_extra), "scope": "all"}}})
        reply = receive()
        revoke_fallback = reply["result"]["content"][0]["text"]
        revoke_id = re.search(r"request_id (kt-access-[A-Za-z0-9_-]+)", revoke_fallback).group(1)
        assert "cannot show confirmation prompts" in revoke_fallback and grants()["roots"]["extra"]["access"] == "ask"
        identifier = next(request_id)
        send({"jsonrpc": "2.0", "id": identifier, "method": "tools/call",
              "params": {"name": "kt_access_revoke", "arguments": {
                  "root": str(base_extra), "scope": "all", "request_id": revoke_id}}})
        reply = receive()
        assert not reply["result"]["isError"] and "explicit authorization" in reply["result"]["content"][0]["text"]
        assert str(base_extra.resolve()) not in grants()["projects"].get(str(project.resolve()), {})
        client.stdin.close()
        assert client.wait(timeout=10) == 0
    print("mcp server checks passed")


if __name__ == "__main__":
    main()
