#!/usr/bin/env python3
"""kt grep, kt status, and the reusable access-grant function; no models."""
import json
import os
import re
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
from unittest.mock import patch

REPOSITORY = Path(__file__).resolve().parents[1]
KT = REPOSITORY / "tools/kt"


def main():
    with tempfile.TemporaryDirectory(prefix="kt grep status test ") as temporary:
        base = Path(temporary)
        global_root = base / "global"
        global_root.mkdir()
        private = base / "private-tree"
        (private / "how/to").mkdir(parents=True)
        (private / "how/to/hide.md").write_text("---\nstatus: green\n---\n\nSECRETWORD lives here.\n")
        config_path = base / "config.json"
        config_path.write_text(json.dumps({"roots": {
            "global": {"path": str(global_root), "access": "allow"},
            "vault": {"path": str(private), "access": "ask"}}, "projects": {}}))
        project = base / "project"
        (project / ".knowledge").mkdir(parents=True)
        env = {**os.environ, "KT_GLOBAL_ROOT": str(global_root), "KT_CONFIG": str(config_path),
               "KT_ACCESS_STATE_DIR": str(base / "state")}

        def kt(*arguments, expected=0, cwd=project):
            result = subprocess.run([sys.executable, str(KT), *arguments], cwd=cwd, env=env, text=True,
                                    capture_output=True)
            assert result.returncode == expected, (arguments, result.returncode, result.stdout, result.stderr)
            return result.stdout

        kt("add", "how to bake bread", "Mix a.b flour.\nProof the dough.\nBake at 220C.\nCool. A.B done.\n")
        kt("add", "what is the sauce", "Tomato.\n", "--global")

        # grep: fixed string by default; regex metacharacters are literal.
        found = kt("grep", "a.b")
        assert "local:how/to/bake/bread.md:" in found and "Mix a.b flour." in found
        assert "A.B done." not in found, "case-sensitive by default"
        insensitive = kt("grep", "-i", "A.B")
        assert "Mix a.b flour." in insensitive and "A.B done." in insensitive
        assert kt("grep", "a.b", "-l").strip() == "local:how/to/bake/bread.md"
        assert "Mix a.b flour." in kt("grep", "-E", "Mix a.b"), "regex dot also matches the literal dot"
        regex = kt("grep", "-E", r"Bake at \d+C")
        assert "Bake at 220C." in regex
        assert "no_matches" in kt("grep", r"Bake at \d+C", expected=1), "fixed-string mode must not treat \\d as a class"
        assert kt("grep", "-E", "^Proof the").count("\n") == 1
        with_context = kt("grep", "-C", "1", "Proof the dough")
        assert re.search(r"bread\.md:\d+- Mix a\.b flour\.", with_context), with_context
        assert re.search(r"bread\.md:\d+: Proof the dough\.", with_context), with_context
        assert re.search(r"bread\.md:\d+- Bake at 220C\.", with_context), with_context
        assert "global:what/is/the/sauce.md:" in kt("grep", "Tomato")
        limited = kt("grep", "-E", ".", "--limit", "2")
        assert limited.count("\n") == 3 and "showing 2 of" in limited
        assert "no_matches" in kt("grep", "zzznope", expected=1)
        assert "invalid regular expression" in subprocess.run(
            [sys.executable, str(KT), "grep", "-E", "("], cwd=project, env=env, text=True, capture_output=True).stderr
        kt("grep", "-E", "(", expected=2)
        kt("grep", "--limit", "0", "x", expected=2)
        assert "no_matches" in kt("grep", "--", "-flag", expected=1), "a leading dash needs -- and is otherwise a usage error"

        # Policy: an "ask" root is invisible to grep and status until approved.
        assert "SECRETWORD" not in kt("grep", "SECRETWORD", expected=1)
        assert "vault" not in kt("status") and "hide" not in kt("status")

        # status: everything proved is green; expired, brown, and unproved leaves are listed with reasons.
        kt("prove", "--local")
        kt("prove", "--global")
        assert kt("status").strip().splitlines()[-1].endswith("yellow=0 brown=0"), kt("status")
        kt("add", "what is fresh", "Brand new answer.\n")
        marked = project / ".knowledge/what/is/marked.md"
        marked.write_text("---\nstatus: yellow\nrevised_at: '2026-09-12T12:00:00+00:00'\n---\n\nAwaiting review.\n")
        kt("add", "what is stale", "Old answer.\n", "--expires-at", "2000-01-01T00:00:00+00:00")
        bad = project / ".knowledge/what/is/broken.md"
        bad.parent.mkdir(parents=True, exist_ok=True)
        bad.write_text("---\nstatus: brown\nrevised_at: '2026-09-12T12:00:00+00:00'\n---\n\nFalsified.\n")
        report = kt("status", "--local").splitlines()
        assert report[0].startswith("brown\tlocal:what/is/broken.md\t"), "brown sorts first"
        assert "priority-one incident" in report[0] and "report it to the user" in report[0]
        rows = {line.split("\t")[1]: line.split("\t") for line in report if "\t" in line}
        assert "local:what/is/fresh.md" not in rows, "a new leaf starts green"
        assert rows["local:what/is/marked.md"][0] == "yellow" and "marked yellow for re-verification" in rows["local:what/is/marked.md"][2]
        assert rows["local:what/is/stale.md"][0] == "yellow" and "expires_at=2000-01-01" in rows["local:what/is/stale.md"][2]
        assert report[-1].endswith("brown=1") and "yellow=2" in report[-1]
        assert "local:" not in kt("status", "--global")
        assert "global:" not in kt("status", "--local")
        kt("status", "--local", "--global", expected=2)
        before = {p: p.read_bytes() for p in (project / ".knowledge").rglob("*.md")}
        kt("status")
        assert before == {p: p.read_bytes() for p in (project / ".knowledge").rglob("*.md")}, "status is read-only"

        # The grant function persists a confirmed decision without prompting; the CLI still needs a TTY.
        kt("access", str(private), "allow", "--scope", "project", expected=3)
        with patch.dict(os.environ, {"KT_GLOBAL_ROOT": str(global_root), "KT_CONFIG": str(config_path),
                                     "KT_ACCESS_STATE_DIR": str(base / "state")}):
            namespace = runpy.run_path(str(KT))
            previous = Path.cwd()
            os.chdir(project)
            try:
                config = namespace["access_config"]()
                root, label, available = namespace["resolve_access_root"](config, str(private))
                assert namespace["root_access"](root, label) == "ask"
                namespace["apply_access_decision"](config, root, label, available, "allow", "project", str(project))
                assert namespace["root_access"](root, label) == "allow"
            finally:
                os.chdir(previous)
        assert "SECRETWORD lives here." in kt("grep", "SECRETWORD"), "an approved root becomes searchable"
        assert "no_matches" in kt("grep", "SECRETWORD", cwd=base, expected=1), "the grant is scoped to the project directory"
    print("grep/status checks passed")


if __name__ == "__main__":
    main()
