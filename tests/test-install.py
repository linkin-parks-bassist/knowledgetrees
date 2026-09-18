#!/usr/bin/env python3
"""Integration checks for the knowledge-tree installer."""

from pathlib import Path
import json
import os
import runpy
import subprocess
import sys
import tempfile
import tomllib


REPOSITORY = Path(__file__).resolve().parents[1]
INSTALLER = REPOSITORY / "install"


def run(*arguments: str, expected: int = 0, answer: str = "Y\n") -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        [str(INSTALLER), *arguments],
        cwd=REPOSITORY,
        text=True,
        input=answer,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert completed.returncode == expected, (completed.stdout, completed.stderr)
    return completed


def main() -> None:
    merge = runpy.run_path(str(INSTALLER))["opencode_config_text"]
    hypothetical_home = Path("/example-user")
    scoped = "/example-user/.knowledge/**"
    reordered = merge(json.dumps({"permission": {"read": {scoped: "allow", "*": "deny"}}}), hypothetical_home)
    assert list(json.loads(reordered)["permission"]["read"]).index(scoped) > 0
    assert merge(reordered, hypothetical_home) == reordered

    with tempfile.TemporaryDirectory(prefix="knowledgetrees-install-test-") as temporary:
        target_home = Path(temporary) / "user"
        home_arguments = ("--home", str(target_home))

        dry_home = Path(temporary) / "dry-run-user"
        dry_run = run("--home", str(dry_home), "--dry-run")
        assert "Would hard-link" in dry_run.stdout
        assert not dry_home.exists()
        assert "[n/Y]" in dry_run.stdout

        for reply in ("n\n", ""):
            denied_home = Path(temporary) / ("denied-user" if reply else "eof-user")
            denied = run("--home", str(denied_home), expected=2, answer=reply)
            assert "cancelled" in denied.stdout
            assert not denied_home.exists(), "consent must precede every write"

        accepted_home = Path(temporary) / "default-consent-user"
        run("--home", str(accepted_home), answer="\n")
        assert (accepted_home / ".knowledge").is_dir()

        malformed_home = Path(temporary) / "malformed-config-user"
        malformed_config = malformed_home / ".config/opencode/opencode.json"
        malformed_config.parent.mkdir(parents=True)
        malformed_config.write_text("{broken")
        run("--home", str(malformed_home), expected=2)
        assert malformed_config.read_text() == "{broken"
        assert not (malformed_home / ".knowledge").exists()

        broken_hooks_home = Path(temporary) / "broken-hooks-user"
        broken_hooks = broken_hooks_home / ".codex/hooks.json"
        broken_hooks.parent.mkdir(parents=True)
        broken_hooks.write_text('{"hooks": {"Stop": "not an array"}}')
        run("--home", str(broken_hooks_home), expected=2)
        assert not (broken_hooks_home / ".knowledge").exists()
        assert "not an array" in broken_hooks.read_text()

        codex_skill = target_home / ".codex" / "skills" / "knowledgetrees" / "SKILL.md"
        codex_config = target_home / ".codex" / "config.toml"
        codex_config.parent.mkdir(parents=True)
        codex_config.write_text(
            'model = "example-model"\n\n'
            "[[skills.config]]\n"
            f'path = "{codex_skill}"\n'
            "enabled = false\n"
            "[desktop]\n"
            "followUpQueueMode = \"steer\"\n"
        )
        codex_hooks = target_home / ".codex/hooks.json"
        unrelated_hook = {"hooks": [{"type": "command", "command": "existing-review-command"}]}
        codex_hooks.write_text(json.dumps({"description": "existing hooks", "hooks": {"Stop": [unrelated_hook], "PreToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": f"python3 {target_home}/.knowledge/.tools/kt-hooks codex before"}, {"type": "command", "command": "unrelated-pre-check"}]}]}}))
        instructions = target_home / "user-instructions.md"
        instructions.write_text("# Existing user instructions\n")
        agents_path = target_home / "AGENTS.md"
        agents_path.symlink_to(instructions.name)

        opencode_config = target_home / ".config" / "opencode" / "opencode.json"
        opencode_config.parent.mkdir(parents=True)
        opencode_config.write_text(json.dumps({"model": "example/local-model", "permission": {
            "skill": {"*": "deny"}, "read": {"*": "ask"}, "edit": {"*": "deny"}
        }}))

        installation = run(*home_arguments)
        assert "WARNING" in installation.stdout and "WRITE" in installation.stdout
        knowledge = target_home / ".knowledge"
        hooks = json.loads(codex_hooks.read_text())
        assert hooks["description"] == "existing hooks" and hooks["hooks"]["Stop"][0] == unrelated_hook
        assert len(hooks["hooks"]["Stop"]) == 2
        assert hooks["hooks"]["PreToolUse"][0]["matcher"] == "Bash"
        assert hooks["hooks"]["PreToolUse"][0]["hooks"] == [{"type": "command", "command": "unrelated-pre-check"}]
        assert hooks["hooks"]["SessionStart"][0]["matcher"] == "^(startup|resume|clear|compact)$"
        assert hooks["hooks"]["SessionStart"][0]["hooks"][0]["command"].endswith("codex start")
        assert (knowledge / ".tools/kt-hooks").is_file()
        assert os.access(knowledge / ".tools/kt-hooks", os.X_OK)
        assert (target_home / ".config/opencode/plugins/knowledgetrees.js").read_bytes() == (REPOSITORY / "tools/kt-opencode.mjs").read_bytes()
        copilot_hooks = json.loads((target_home / ".copilot/hooks/knowledgetrees.json").read_text())
        assert set(copilot_hooks["hooks"]) == {"userPromptSubmitted", "postToolUse", "postToolUseFailure", "agentStop"}
        assert copilot_hooks["hooks"]["agentStop"][0]["args"][-2:] == ["copilot", "stop"]
        canonical = knowledge / "how" / "to" / "use" / "knowledgetrees.md"
        shared_skill = target_home / ".agents" / "skills" / "knowledgetrees" / "SKILL.md"
        orientation = knowledge / "where" / "am" / "i.md"

        assert "How to navigate this tree" in orientation.read_text()
        for branch in ("how/", "what/", "where/", "why/", "does/", "is/"):
            assert branch in orientation.read_text()
        assert canonical.is_file()
        assert "scope: personal global" in canonical.read_text()
        for leaf in knowledge.rglob("*.md"):
            assert "scope: public knowledge-tree example" not in leaf.read_text()
        assert not (knowledge / "what" / "is" / "the" / "spec.md").exists()
        assert os.access(knowledge / ".tools/kt", os.X_OK)
        assert (target_home / ".local/bin/kt").is_symlink()
        assert (target_home / ".local/bin/kt").samefile(knowledge / ".tools/kt")
        assert not canonical.is_symlink()
        assert not shared_skill.is_symlink()
        assert not codex_skill.is_symlink()
        assert canonical.stat().st_dev == shared_skill.stat().st_dev == codex_skill.stat().st_dev
        assert canonical.stat().st_ino == shared_skill.stat().st_ino == codex_skill.stat().st_ino
        assert "fresh agent session" in canonical.read_text()
        assert "first move of every task" not in canonical.read_text()
        assert "For every new question, use kt first" in canonical.read_text()
        assert "A miss is not proof of absence" in canonical.read_text()
        assert "before the next unrelated tool call or completion" in canonical.read_text()
        for name in ("how/to/add/knowledge/leaves.md", "how/to/maintain/a/knowledge/tree.md",
                     "how/should/an/agent/traverse/a/knowledge/tree.md"):
            assert (knowledge / name).is_file()
        assert {p.name for p in (knowledge / ".tools").iterdir()} == {"kt", "kt-hooks"}

        assert agents_path.is_symlink()
        agents = agents_path.read_text()
        assert "Existing user instructions" in agents
        assert agents.count("BEGIN KNOWLEDGETREES BOOTSTRAP") == 1
        assert "fresh agent session" in agents
        assert "New question -> `kt` first" in agents
        assert "determine whether a leaf exists" in agents
        assert "first move of every task" not in agents
        config = codex_config.read_text()
        assert 'model = "example-model"' in config
        assert config.count(str(codex_skill)) == 1
        assert "enabled = true\n[desktop]" in config or "enabled = true\n\n[desktop]" in config
        parsed_config = tomllib.loads(config)
        assert parsed_config["desktop"]["followUpQueueMode"] == "steer"
        installed_skills = runpy.run_path(str(INSTALLER))["SKILL_LEAVES"]
        for name, relative in installed_skills.items():
            owner = knowledge / relative
            assert f"name: {name}" in owner.read_text()
            assert "metadata:\n" in owner.read_text()
            assert "  ---" not in owner.read_text(), "frontmatter delimiter must not be nested"
            assert owner.read_text().count("\n---\n") == 1
            assert "kt" in owner.read_text()
            assert "unrelated tool call" in owner.read_text()
            for harness in (".agents", ".codex"):
                entry = target_home / harness / "skills" / name / "SKILL.md"
                assert not entry.is_symlink()
                assert entry.samefile(owner)
                if harness == ".codex":
                    assert config.count(str(entry)) == 1
        opencode = json.loads(opencode_config.read_text())
        assert opencode["model"] == "example/local-model"
        permissions = opencode["permission"]
        assert permissions["read"]["*"] == "ask"
        assert permissions["edit"]["*"] == "deny"
        assert permissions["skill"]["*"] == "deny"
        assert permissions["skill"]["knowledgetrees"] == "allow"
        for name in installed_skills:
            assert permissions["skill"][name] == "allow"
        for name in (".knowledge", ".agents"):
            pattern = str(target_home / name) + "/**"
            assert permissions["read"][pattern] == "allow"
            assert permissions["external_directory"][pattern] == "allow"
        assert permissions["edit"][str(knowledge) + "/**"] == "allow"
        assert permissions["edit"][str(target_home / ".agents") + "/**"] == "ask"

        orientation.write_text("Local environment orientation.\n")
        rerun = run(*home_arguments, answer="")
        assert len(json.loads(codex_hooks.read_text())["hooks"]["Stop"]) == 2
        assert "[n/Y]" not in rerun.stdout
        assert orientation.read_text() == "Local environment orientation.\n"
        assert agents_path.read_text().count(
            "BEGIN KNOWLEDGETREES BOOTSTRAP"
        ) == 1
        assert codex_config.read_text().count(str(codex_skill)) == 1
        for name, relative in installed_skills.items():
            assert (target_home / ".agents/skills" / name / "SKILL.md").samefile(knowledge / relative)

        capture_owner = knowledge / installed_skills["knowledgetrees-capture"]
        proof_owner = knowledge / "how/to/use/knowledgetree/hooks.md"
        proof_content = proof_owner.read_text()
        assert "Proof: (verified at " in proof_content
        proof_owner.write_text(proof_content.replace("Proof: (verified at ", "Proof: (falsified at "))
        run(*home_arguments, expected=2)
        assert "Proof: (falsified at " in proof_owner.read_text()
        proof_owner.write_text(proof_content.replace("---\n", "---\nfalsified_at: test-failure\n", 1))
        run(*home_arguments, expected=2)
        assert "falsified_at: test-failure" in proof_owner.read_text()
        proof_owner.write_text(proof_content)
        capture_owner.write_text(capture_owner.read_text() + "\nLocal customization.\n")
        customized = capture_owner.read_bytes()
        inode = capture_owner.stat().st_ino
        opencode_before = opencode_config.read_bytes()
        registry = knowledge / ".tools/roots.json"
        registry.write_text('{"roots":{"private":{"path":"/example/private","access":"ask"}},"projects":{}}')
        registered = registry.read_bytes()
        run(*home_arguments, "--hooks-only", answer="")
        assert registry.read_bytes() == registered
        assert capture_owner.read_bytes() == customized and capture_owner.stat().st_ino == inode
        assert opencode_config.read_bytes() == opencode_before
        assert (target_home / ".agents/skills/knowledgetrees-capture/SKILL.md").samefile(capture_owner)
        run(*home_arguments, expected=2)
        assert "Local customization" in capture_owner.read_text()
        run(*home_arguments, "--force")
        assert "Local customization" not in capture_owner.read_text()
        for name, relative in installed_skills.items():
            for harness in (".agents", ".codex"):
                assert (target_home / harness / "skills" / name / "SKILL.md").samefile(knowledge / relative)

        changed_leaf = knowledge / "what" / "is" / "a" / "knowledge" / "tree.md"
        changed_leaf.write_text("Customized content.\n")
        conflict = run(*home_arguments, expected=2)
        assert "Refusing to overwrite" in conflict.stderr
        run(*home_arguments, "--force")
        assert "Customized content" not in changed_leaf.read_text()
        assert canonical.stat().st_ino == shared_skill.stat().st_ino == codex_skill.stat().st_ino

        proof_environment = os.environ.copy()
        proof_environment["HOME"] = str(target_home)
        subprocess.run(
            [str(knowledge / ".tools/kt"), "prove", "--root", str(knowledge)],
            cwd=target_home,
            env=proof_environment,
            check=True,
        )

    print("installer integration checks passed")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as error:
        print(f"installer integration check failed: {error}", file=sys.stderr)
        raise
