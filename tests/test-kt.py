#!/usr/bin/env python3
"""CLI checks using isolated knowledge roots."""
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
        (global_root / "where/is").mkdir(parents=True)
        (global_root / "where/is/compiler.md").write_text("---\nscope: test\n---\n\nThe compiler is installed here.\n")
        (global_root / "where/is/gpu.md").write_text("GPU location: violet accelerator.\n")
        (global_root / "how/to/explain").mkdir(parents=True)
        (global_root / "how/to/explain/compiler.md").write_text("A compiler translates code.\n")
        (global_root / "how/to/explain/violet.md").write_text("Unrelated procedure mentions violet accelerator.\n")
        (global_root / "how/to/explain/empty-topic").mkdir()
        (global_root / "how/to/recover.md").write_text("Recover with amber diagnostics.\n")
        (global_root / "how/to/obtain").mkdir(parents=True)
        (global_root / "how/to/obtain/sudo-authorization.md").write_text("Use the approved procedure.\n")
        (global_root / ".tools").mkdir()
        nested = project / "sub/folder"
        nested.mkdir(parents=True)
        config = base / "config.json"
        config.write_text(json.dumps({"roots": {"global": {"path": str(global_root), "access": "allow"}}}))
        env = {**os.environ, "KT_CONFIG": str(config), "KT_GLOBAL_ROOT": str(global_root), "NO_COLOR": "1"}


        def run(*args, expected=0, cwd=project):
            result = subprocess.run([sys.executable, str(SCRIPT), *args], cwd=cwd,
                                    env=env, text=True, capture_output=True)
            assert result.returncode == expected, (result.stdout, result.stderr)
            assert "\033[" not in result.stdout
            return result.stdout

        result = run("add", "How to do the thing?", "Do it carefully.", "--source", "test evidence")
        captured = local / "how/to/do/the/thing.md"
        assert result == "" and captured.is_file()
        saved = captured.read_text()
        assert 'status: "unverified"' in saved and 'source: "test evidence"' in saved
        assert "verified_at:" not in saved and "Proof:" not in saved
        assert run("how to do the thing") == saved
        run("add", "how to do the thing", "overwrite", expected=2)
        assert captured.read_text() == saved
        run("capture", "why is repetition repetition useful", "Repetition.", "--global")
        assert (global_root / "why/is/repetition/repetition/useful.md").is_file()
        run("add", "where is multi-word tooling", "Here.", "--root", str(global_root),
            "--scope", "public example", "--source", "quoted \"source\"\nwith newline")
        explicit = (global_root / "where/is/multi-word/tooling.md").read_text()
        assert 'scope: "public example"' in explicit and str(base) not in explicit
        assert 'source: "quoted \\"source\\"\\nwith newline"' in explicit
        preview = run("add", "when to preview", "Preview first.", "--dry-run")
        assert 'status: "unverified"' in preview and not (local / "when").exists()
        run("add", "where is mystery", "Not established.", "--unresolved", expected=2)
        run("add", "where is mystery", "Not established.", "--unresolved",
            "--blocker", "missing evidence", "--next-check", "inspect configuration")
        unresolved = (local / "where/is/mystery.md").read_text()
        assert 'status: "unresolved"' in unresolved and "checked_at:" in unresolved
        for unsafe in ("../escape", "where/is/escape", "where_is_escape", "---", "bad\nquestion"):
            run("add", unsafe, "No.", expected=2)
        run("add", "what is empty", "   ", expected=2)
        run("add", "what is nested metadata", "---\nstatus: verified\n---\nNo.", expected=2)
        (local / "evil").symlink_to(global_root, target_is_directory=True)
        run("add", "evil escape", "No.", expected=2)
        assert not (global_root / "escape.md").exists()
        piped = subprocess.run([sys.executable, str(SCRIPT), "add", "how to pipe", "-"],
                               cwd=project, env=env, input="Multiline\nanswer.\n", text=True, capture_output=True)
        assert piped.returncode == 0, piped.stderr
        assert (local / "how/to/pipe.md").read_text().endswith("Multiline\nanswer.\n")
        result = run("find", "how to add knowledge leaves")
        assert result.index("local:" + leaf) < result.index("global:" + leaf)
        assert "2026-09-12T12:00:00+00:00" in result
        assert "FALSIFIED" in run("find", "leaves")
        dictionary = run("dict").strip().split(", ")
        assert dictionary == sorted(set(dictionary), key=lambda value: (value.casefold(), value))
        assert {"obtain", "sudo-authorization"}.issubset(dictionary)
        assert "explain" in dictionary and "knowledge" in dictionary
        assert "add" not in dictionary, "segments above the final two path positions are excluded"
        assert not {"a", "to", "how", "when", "what", "where"}.intersection(dictionary)
        assert all(len(segment) > 2 for segment in dictionary)
        assert dictionary.count("obtain") == 1 and "sudo-authorization.md" not in dictionary
        local_dictionary = run("dict", "local").strip().split(", ")
        assert "sudo-authorization" not in local_dictionary
        assert run("dict", str(global_root)) == run("dict", "global")
        assert run("dict", "local", "global") == run("dict")
        assert run("dict", "unknown-root", expected=2) == ""
        compact = run("find", "leaves")
        pretty = run("find", "leaves", "--pretty")
        assert len(compact) < len(pretty)
        compact_paths = [line.split("\t")[0] for line in compact.splitlines()[1:]]
        pretty_paths = [line.split()[1] for line in pretty.splitlines() if line[:1].isdigit() and ". " in line]
        assert compact_paths == pretty_paths, (compact_paths, pretty_paths)
        assert run("--pretty", "find", "leaves") == pretty
        assert "Read verbatim:" not in compact and "Read verbatim:" in pretty
        long_leaf = local / "what/is/longexcerpt.md"
        long_leaf.parent.mkdir(parents=True, exist_ok=True)
        long_body = "longexcerpt " + "useful context " * 1000
        long_leaf.write_text(long_body)
        long_result = run("find", "longexcerpt")
        assert len(long_result) < 400, "default search must not dump a long paragraph"
        assert run("open", "project:what/is/longexcerpt.md") == long_body
        assert run("what", "is", "longexcerpt") == long_body
        for arguments in (("open", "local:what/is/longexcerpt.md"), ("what", "is", "longexcerpt")):
            read = subprocess.run([sys.executable, str(SCRIPT), *arguments], cwd=project, env=env, text=True, capture_output=True)
            import hashlib
            assert read.returncode == 0 and read.stdout == long_body
            assert "Revision: " + hashlib.sha256(long_body.encode()).hexdigest() in read.stderr

        for question in ("does a proof verify a leaf", "is a tree authorization"):
            run("add", question, "No. The answer needs independent evidence.")
            assert run(*question.split()) == run("open", "local:" + question.replace(" ", "/") + ".md")
            assert run(*question.split(), "--pretty") == run(*question.split())
        assert "branch=does" in run("does", "_")

        assert run("how", "to", "add", "knowledge", "leaves", "--pretty") == run("how", "to", "add", "knowledge", "leaves")

        weak = run("find", "compiler", "unfindablezzz", expected=1)
        assert "adequate=0" in weak and " weak\t" in weak
        assert "compiler.md" in weak
        assert "coverage=50%" in run("find", "compiler", "unfindablezzz", "--min-coverage", "0.5")
        run("find", "compiler", "--min-coverage", "0", expected=2)
        assert "adequate=0" in run("where", "is", "compiler", "unfindablezzz", expected=1)
        assert run("where", "is", "compiler") == (global_root / "where/is/compiler.md").read_text()
        assert run("where is compiler") == (global_root / "where/is/compiler.md").read_text()
        scoped = run("where", "is", "violet")
        assert "branch=where/is" in scoped
        assert "global:where/is/gpu.md" in scoped and "how/to/" not in scoped
        listed = run("how", "to", "_", "--limit", "100")
        assert "global:how/to/" in listed and "global:where/is/" not in listed
        widened = run("how", "to", "explain", "empty-topic", "amber")
        assert "branch=how/to" in widened and "global:how/to/recover.md" in widened
        assert "where/is" not in widened
        assert "no_matches" in run("where", "is", "unfindablezzz", expected=1)
        run("how", "_", "to", expected=2)
        assert "no_matches" in run("find", "zzzzunfindable", expected=1)
        assert run("open", "global:" + leaf) == content
        assert run("open", leaf).startswith("---")
        assert "Project: capture" in run("open", "project:" + leaf)
        run("open", "project:../../outside.md", expected=2)
        assert run("open", str(global_root / leaf)) == content
        assert str(local) in run("roots") and str(global_root) in run("roots")
        assert "Test orientation." in run()
        assert str(local) in run("roots", cwd=local)
        global_only = run("roots", cwd=base)
        assert str(global_root) in global_only and "local\tallow\t" not in global_only
        run("proof", expected=2)
        assert run("prove", "--no-stamp", "leaves") == "green=2 yellow=0 brown=0\n"
        assert run("prove", "--local", "--no-stamp", "leaves") == "green=1 yellow=0 brown=0\n"
        assert run("prove", "--global", "--no-stamp", "leaves") == "green=1 yellow=0 brown=0\n"
        assert "brown=0" in run("prove", str(project), "--no-stamp")
        assert run("prove", "--root", str(global_root), "--no-stamp", "leaves") == "green=1 yellow=0 brown=0\n"
        assert "--timeout" in run("prove", "--help")
        assert "--local" in run("prove", "--help")
        global_failure = global_root / "what/is/global-proof.md"
        global_failure.parent.mkdir(parents=True, exist_ok=True)
        global_failure.write_text("Failing global proof.\n\nProof: (verified at _)\n\n```bash\nfalse\n```\n")
        assert run("prove", "--local", "--no-stamp", "global-proof") == "green=0 yellow=0 brown=0\n"
        run("prove", "--global", "--no-stamp", "global-proof", expected=1)
        run("prove", "--no-stamp", "global-proof", expected=1)
        global_failure.unlink()
        proof = local / "what/is/proven.md"
        proof.parent.mkdir(parents=True, exist_ok=True)
        proof.write_text("Passing.\n\nProof: (verified at _)\n\n```bash\ntest 1 -eq 1\n```\n")
        assert run("prove", "--no-stamp", "proven") == "green=0 yellow=1 brown=0\n"
        assert "verified at _" in proof.read_text()
        run("prove", "proven")
        assert "verified at _" not in proof.read_text()
        proof.write_text("Failing.\n\nProof: (verified at _)\n\n```bash\nfalse\n```\n")
        run("prove", "--no-stamp", "proven", expected=1)
        assert "falsified_at:" not in proof.read_text()
    print("kt integration checks passed")


if __name__ == "__main__":
    main()
