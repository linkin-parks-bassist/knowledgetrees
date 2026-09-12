#!/usr/bin/env python3
"""Integration checks for the knowledge-tree installer."""

from pathlib import Path
import os
import subprocess
import sys
import tempfile


REPOSITORY = Path(__file__).resolve().parents[1]
INSTALLER = REPOSITORY / "install"


def run(*arguments: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        [str(INSTALLER), *arguments],
        cwd=REPOSITORY,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert completed.returncode == expected, (completed.stdout, completed.stderr)
    return completed


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="knowledgetrees-install-test-") as temporary:
        target_home = Path(temporary) / "user"
        home_arguments = ("--home", str(target_home))

        dry_home = Path(temporary) / "dry-run-user"
        dry_run = run("--home", str(dry_home), "--dry-run")
        assert "Would hard-link" in dry_run.stdout
        assert not dry_home.exists()

        codex_skill = target_home / ".codex" / "skills" / "knowledgetrees" / "SKILL.md"
        codex_config = target_home / ".codex" / "config.toml"
        codex_config.parent.mkdir(parents=True)
        codex_config.write_text(
            'model = "example-model"\n\n'
            "[[skills.config]]\n"
            f'path = "{codex_skill}"\n'
            "enabled = false\n"
        )
        instructions = target_home / "user-instructions.md"
        instructions.write_text("# Existing user instructions\n")
        agents_path = target_home / "AGENTS.md"
        agents_path.symlink_to(instructions.name)

        run(*home_arguments)
        knowledge = target_home / ".knowledge"
        canonical = knowledge / "how" / "to" / "use" / "knowledgetrees.md"
        shared_skill = target_home / ".agents" / "skills" / "knowledgetrees" / "SKILL.md"
        orientation = knowledge / "where" / "am" / "i.md"
        verifier = knowledge / ".tools" / "verify-knowledgetree-proofs"

        assert orientation.read_bytes() == b""
        assert canonical.is_file()
        assert "scope: personal global" in canonical.read_text()
        for leaf in knowledge.rglob("*.md"):
            assert "scope: public knowledge-tree example" not in leaf.read_text()
        assert not (knowledge / "what" / "is" / "the" / "spec.md").exists()
        assert os.access(verifier, os.X_OK)
        assert not canonical.is_symlink()
        assert not shared_skill.is_symlink()
        assert not codex_skill.is_symlink()
        assert canonical.stat().st_dev == shared_skill.stat().st_dev == codex_skill.stat().st_dev
        assert canonical.stat().st_ino == shared_skill.stat().st_ino == codex_skill.stat().st_ino
        assert "fresh agent session" in canonical.read_text()
        assert "first move of every task" not in canonical.read_text()
        assert len(list(knowledge.rglob("verify-knowledgetree-proofs"))) == 1

        assert agents_path.is_symlink()
        agents = agents_path.read_text()
        assert "Existing user instructions" in agents
        assert agents.count("BEGIN KNOWLEDGETREES BOOTSTRAP") == 1
        assert "fresh agent session" in agents
        assert "first move of every task" not in agents
        config = codex_config.read_text()
        assert 'model = "example-model"' in config
        assert config.count(str(codex_skill)) == 1
        assert "enabled = true" in config

        orientation.write_text("Local environment orientation.\n")
        run(*home_arguments)
        assert orientation.read_text() == "Local environment orientation.\n"
        assert agents_path.read_text().count(
            "BEGIN KNOWLEDGETREES BOOTSTRAP"
        ) == 1
        assert codex_config.read_text().count(str(codex_skill)) == 1

        changed_leaf = knowledge / "what" / "is" / "a" / "knowledge" / "tree.md"
        changed_leaf.write_text("Customized content.\n")
        conflict = run(*home_arguments, expected=2)
        assert "Refusing to overwrite" in conflict.stderr
        run(*home_arguments, "--force")
        assert "Customized content" not in changed_leaf.read_text()
        assert canonical.stat().st_ino == shared_skill.stat().st_ino == codex_skill.stat().st_ino

        verifier_environment = os.environ.copy()
        verifier_environment["HOME"] = str(target_home)
        subprocess.run(
            [str(verifier), "--root", str(knowledge)],
            cwd=target_home,
            env=verifier_environment,
            check=True,
        )

    print("installer integration checks passed")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as error:
        print(f"installer integration check failed: {error}", file=sys.stderr)
        raise
