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
KT = REPOSITORY / "tools/kt"


def main():
    with tempfile.TemporaryDirectory(prefix="kt mcp test ") as temporary:
        root = Path(temporary)
        global_root = root / "global"
        global_root.mkdir()
        (root / "config.json").write_text(json.dumps({"roots": {"global": {"path": str(global_root), "access": "allow"}}}))
        project = root / "project"
        (project / ".knowledge").mkdir(parents=True)
        env = {**os.environ, "KT_GLOBAL_ROOT": str(global_root), "KT_CONFIG": str(root / "config.json"),
               "KT_MCP_CLI": str(KT)}
        subprocess.run([sys.executable, str(KT), "add", "what is the fixture", "Alpha line.\nBeta line.\nBeta line.\n"],
                       cwd=project, env=env, check=True, capture_output=True)
        address = "local:what/is/the/fixture.md"

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
        assert names == {"kt_read", "kt_edit", "kt_rewrite"}
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
        assert not response["isError"] and "Whole new body." in response["content"][0]["text"]
        remote.stdin.close()
        assert remote.wait(timeout=10) == 0
    print("mcp server checks passed")


if __name__ == "__main__":
    main()
