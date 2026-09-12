#!/usr/bin/env python3
"""Read-only CLI checks using isolated knowledge roots."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

SCRIPT = Path(__file__).resolve().parents[1] / "tools/kt"


def main():
    with tempfile.TemporaryDirectory(prefix="kt test ") as directory:
        base = Path(directory)
        project = base / "project space"
        local = project / ".knowledge"
        global_root = base / "global space"
        for root in (local, global_root):
            (root / "where/am").mkdir(parents=True)
            (root / "where/am/i.md").write_text("---\nscope: test\n---\n\nTest orientation.\n")
            (root / "how/to/add/knowledge").mkdir(parents=True)
        leaf = "how/to/add/knowledge/leaves.md"
        content = "---\nmetadata:\n  verified_at: '2026-09-12T12:00:00+00:00'\n---\n\nCapture leaves immediately.\n"
        (global_root / leaf).write_text(content)
        (local / leaf).write_text(content.replace("Capture", "Project: capture"))
        (global_root / "bad.md").write_text("---\nfalsified_at: yesterday\n---\n\nLeaves are bad.\n")
        (global_root / ".tools").mkdir()
        verifier = global_root / ".tools/verify-knowledgetree-proofs"
        verifier.write_text("#!/usr/bin/env python3\nimport json,sys\nprint(json.dumps(sys.argv[1:]))\n")
        verifier.chmod(0o755)
        nested = project / "sub/folder"
        nested.mkdir(parents=True)
        env = {**os.environ, "KT_GLOBAL_ROOT": str(global_root), "NO_COLOR": "1"}

        def run(*args, expected=0, cwd=nested):
            result = subprocess.run([sys.executable, str(SCRIPT), *args], cwd=cwd,
                                    env=env, text=True, capture_output=True)
            assert result.returncode == expected, (result.stdout, result.stderr)
            assert "\033[" not in result.stdout
            return result.stdout

        result = run("find", "how to add knowledge leaves")
        assert result.index("project:" + leaf) < result.index("global:" + leaf)
        assert "2026-09-12T12:00:00+00:00" in result
        assert "FALSIFIED" in run("find", "leaves")
        assert "No matches" in run("find", "zzzzunfindable", expected=1)
        assert run("open", "global:" + leaf) == content
        assert run("open", leaf).startswith("---")
        assert "Project: capture" in run("open", "project:" + leaf)
        run("open", "project:../../outside.md", expected=2)
        assert run("open", str(global_root / leaf)) == content
        assert str(local) in run("roots") and str(global_root) in run("roots")
        assert "Test orientation." in run()
        assert str(local) in run("roots", cwd=local)
        global_only = run("roots", cwd=base)
        assert len(global_only.splitlines()) == 1 and str(global_root) in global_only
        assert json.loads(run("proof", "--no-stamp", "leaves")) == ["--root", str(local), "--no-stamp", "leaves"]
        assert json.loads(run("proof", str(project), "--no-stamp")) == ["--root", str(local), "--no-stamp"]
        assert json.loads(run("proof", "--root", str(global_root), "--no-stamp")) == ["--root", str(global_root), "--no-stamp"]
    print("kt integration checks passed")


if __name__ == "__main__":
    main()
