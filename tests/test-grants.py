#!/usr/bin/env python3
"""Access grant lifecycle: why a root is readable, revocation, and stale-approval pruning; no models."""
import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile
from unittest.mock import patch

REPOSITORY = Path(__file__).resolve().parents[1]
KT = REPOSITORY / "tools/kt"


def main():
    with tempfile.TemporaryDirectory(prefix="kt grants test ") as temporary:
        base = Path(temporary)
        global_root = base / "global"
        (global_root / "how").mkdir(parents=True)
        project = base / "project"
        (project / ".knowledge").mkdir(parents=True)
        sub = project / "sub"
        sub.mkdir()
        trees = {}
        for name in ("vault", "everywhere", "locked", "hidden", "temp", "unmounted"):
            trees[name] = base / name
            (trees[name] / "how").mkdir(parents=True)
            (trees[name] / "how" / "x.md").write_text(f"---\nstatus: green\n---\n\nTOKEN-{name}\n")
        config_path = base / "config.json"

        def write_config(projects=None, **extra):
            config_path.write_text(json.dumps({"roots": {
                "global": {"path": str(global_root), "access": "allow"},
                "vault": {"path": str(trees["vault"]), "access": "ask"},
                "everywhere": {"path": str(trees["everywhere"]), "access": "allow"},
                "locked": {"path": str(trees["locked"]), "access": "deny"},
                "hidden": {"path": str(trees["hidden"]), "access": "force-private"},
                "temp": {"path": str(trees["temp"]), "access": "allow"},
                "unmounted": {"path": str(trees["unmounted"]), "access": "ask"},
                **extra.get("roots", {})}, "projects": projects or {}}))

        def config():
            return json.loads(config_path.read_text())

        env = {**os.environ, "KT_GLOBAL_ROOT": str(global_root), "KT_CONFIG": str(config_path),
               "KT_ACCESS_STATE_DIR": str(base / "state")}
        env.pop("KT_SESSION_ID", None)
        env.pop("CODEX_THREAD_ID", None)
        env.pop("OPENCODE_SESSION_ID", None)

        def kt(*arguments, expected=0, cwd=project):
            result = subprocess.run([sys.executable, str(KT), *arguments], cwd=cwd, env=env, text=True,
                                    capture_output=True)
            assert result.returncode == expected, (arguments, result.returncode, result.stdout, result.stderr)
            return result

        # ---- kt grants explains why each root is (not) readable
        write_config({str(project): {str(trees["vault"]): "allow"}})
        rows = {line.split("\t")[0]: line.split("\t") for line in kt("grants").stdout.splitlines()}
        assert rows["local"][1:3] == ["allow", "local tree"]
        assert rows["global"][2] == "allowed everywhere"
        assert rows[str(trees["vault"])][1:3] == ["allow", "project grant"]
        assert rows[str(trees["locked"])][1] == "deny" and rows[str(trees["locked"])][3] == "(restricted)"
        assert rows[str(trees["unmounted"])][1] == "ask"
        assert str(trees["hidden"]) not in kt("grants").stdout, "force-private roots are not listed"
        assert kt("grants", str(trees["hidden"])).stdout.strip() == "force-private"
        assert rows[str(trees["vault"])][3] == str(trees["vault"]), "an allowed root shows its path"
        kt("grants", "relative/path", expected=2)

        # Subdirectory inheritance is explained, not hidden.
        write_config({str(project): {str(trees["vault"]): {"access": "allow", "subdirectories": True}}})
        inherited = kt("grants", str(trees["vault"]), cwd=sub).stdout
        assert "project grant including subdirectories" in inherited and f"granted for {project}" in inherited
        assert kt("grants", str(trees["vault"]), cwd=base).stdout.split("\t")[1] == "ask", "a grant does not leak outside the project"

        # ---- revocation: CLI needs the user's terminal, the function does not prompt
        kt("access", str(trees["vault"]), "revoke", expected=3)
        with patch.dict(os.environ, env):
            ns = runpy.run_path(str(KT))
            previous = Path.cwd()
            os.chdir(project)
            try:
                def revoke(name, scope="project", cwd=project, save=True):
                    cfg = ns["access_config"]()
                    root, label, available = ns["resolve_access_root"](cfg, str(trees[name]))
                    return ns["apply_revocation"](cfg, root, label, available, scope, str(cwd), save=save), cfg

                def policy(name, cwd=project):
                    cfg = ns["access_config"]()
                    root, label, _ = ns["resolve_access_root"](cfg, str(trees[name]))
                    return ns["resolve_root_access"](root, label, cwd, cfg)

                # exact-directory grant is removed
                write_config({str(project): {str(trees["vault"]): "allow"}})
                assert policy("vault")[:2] == ("allow", "project grant")
                message, _ = revoke("vault")
                assert "requires approval again in this project" in message
                assert policy("vault")[0] == "ask" and str(project) not in config()["projects"]
                # a preview edits only the given copy
                write_config({str(project): {str(trees["vault"]): "allow"}})
                _, preview = revoke("vault", save=False)
                assert str(project) not in preview["projects"] and str(trees["vault"]) in config()["projects"][str(project)]
                # "allowed everywhere" is overridden for this project only
                write_config()
                assert policy("everywhere")[:2] == ("allow", "allowed everywhere")
                revoke("everywhere")
                assert config()["projects"][str(project)][str(trees["everywhere"])] == "ask"
                assert policy("everywhere")[0] == "ask" and policy("everywhere", cwd=base)[0] == "allow"
                assert ns["resolve_root_access"](trees["everywhere"], None, project, ns["access_config"]())[1] == "project grant"
                # everywhere: policy back to ask, and every project grant for the root is dropped
                write_config({str(project): {str(trees["vault"]): "allow"}, str(sub): {str(trees["vault"]): "allow"}})
                message, _ = revoke("vault", scope="all")
                assert "every project" in message and config()["projects"] == {}
                assert config()["roots"]["vault"]["access"] == "ask"
                write_config()
                message, _ = revoke("everywhere", scope="all")
                assert config()["roots"]["everywhere"]["access"] == "ask"
                # inherited grants are revoked at the project that made them
                write_config({str(project): {str(trees["vault"]): {"access": "allow", "subdirectories": True}}})
                message, _ = revoke("vault", cwd=sub)
                assert f"the grant was made for {project} and its subdirectories" in message and policy("vault", cwd=sub)[0] == "ask"
                # not currently readable: nothing to do
                write_config()
                assert "nothing to revoke" in revoke("unmounted")[0]
                # refusals
                for name, expected in (("hidden", "unavailable"),):
                    try:
                        revoke(name)
                    except ValueError as error:
                        assert expected in str(error)
                    else:
                        raise AssertionError(name)
                cfg = ns["access_config"]()
                local, label, available = ns["resolve_access_root"](cfg, "local")
                try:
                    ns["apply_revocation"](cfg, local, label, available, "project", str(project))
                except ValueError as error:
                    assert "local tree" in str(error)
                else:
                    raise AssertionError("the local tree must not be revocable")
                bypass = ns["access_config"]()
                bypass["dangerously_skip_permissions"] = True
                root, label, available = ns["resolve_access_root"](bypass, str(trees["vault"]))
                try:
                    ns["apply_revocation"](bypass, root, label, available, "project", str(project))
                except ValueError as error:
                    assert "permissions --reset" in str(error)
                else:
                    raise AssertionError("bypass must be turned off by the user, not revoked")
            finally:
                os.chdir(previous)

        # ---- stale approvals never follow a recreated tree
        write_config({str(project): {str(trees["vault"]): "allow"},
                      str(base / "gone-project"): {str(trees["vault"]): "allow"}})
        (base / "gone-project").mkdir()
        result = kt("roots")
        assert "stale access approval" not in result.stderr, "nothing is stale while the trees exist"
        shutil.rmtree(base / "gone-project")
        result = kt("roots")
        assert "removed 1 stale access approval" in result.stderr
        assert list(config()["projects"]) == [str(project)]
        shutil.rmtree(trees["vault"])
        result = kt("roots")
        assert "removed 1 stale access approval" in result.stderr and config()["projects"] == {}
        (trees["vault"] / "how").mkdir(parents=True)
        (trees["vault"] / "how" / "x.md").write_text("---\nstatus: green\n---\n\nRECREATED-DIFFERENT-TREE\n")
        assert "RECREATED-DIFFERENT-TREE" not in kt("grep", "RECREATED-DIFFERENT-TREE", expected=1).stdout, \
            "a recreated tree needs a fresh approval"
        assert kt("roots").stderr == "", "pruning is quiet when there is nothing to prune"

        # a registered root that was allowed everywhere is dropped when its tree disappears
        shutil.rmtree(trees["temp"])
        assert "removed 1 stale access approval" in kt("roots").stderr
        assert "temp" not in config()["roots"]
        (trees["temp"] / "how").mkdir(parents=True)
        (trees["temp"] / "how" / "x.md").write_text("---\nstatus: green\n---\n\nRECREATED-TEMP\n")
        kt("grep", "RECREATED-TEMP", expected=1)

        # auto-named (root-<hash>) ask registrations name nothing but a dead path, so they go; user-named ones stay
        ghost = base / "ghost"
        (ghost / "how").mkdir(parents=True)
        cfg = config()
        cfg["roots"]["root-0123456789ab"] = {"path": str(ghost), "access": "ask"}
        config_path.write_text(json.dumps(cfg))
        assert kt("roots").stderr == "", "nothing is pruned while the tree exists"
        shutil.rmtree(ghost)
        assert "removed 1 stale access approval" in kt("roots").stderr
        assert "root-0123456789ab" not in config()["roots"] and "unmounted" in config()["roots"]

        # deny, ask, force-private registrations and the global entry survive a missing tree
        shutil.rmtree(trees["locked"])
        shutil.rmtree(trees["hidden"])
        shutil.rmtree(trees["unmounted"])
        assert kt("roots").stderr == ""
        assert {"locked", "hidden", "unmounted", "global"} <= set(config()["roots"])
        listing = kt("grants").stdout
        assert "TREE MISSING" in listing and str(trees["locked"]) in listing
        (trees["hidden"] / "how").mkdir(parents=True)
        assert str(trees["hidden"]) not in kt("grants").stdout, "a recreated force-private tree stays private"

        # a missing registered root can be removed by naming its label or its old path
        with patch.dict(os.environ, env):
            ns = runpy.run_path(str(KT))
            cfg = ns["access_config"]()
            root, label, available = ns["resolve_access_root"](cfg, str(trees["locked"]))
            assert not root.is_dir()
            assert "Removed the registration" in ns["apply_revocation"](cfg, root, label, available, "all", str(project))
        assert "locked" not in config()["roots"]
        # an unrelated missing path is still an error
        kt("grants", str(base / "never-existed"), expected=2)
        kt("access", str(base / "never-existed"), expected=2)

        # A corrupt access file is a clean error (no traceback, nothing pruned or rewritten); help still works.
        config_path.write_text("{broken")
        broken = kt("roots", expected=2)
        assert "Traceback" not in broken.stderr and config_path.read_text() == "{broken"
        assert "usage" in kt("--help").stdout.lower()
    print("access grant lifecycle checks passed")


if __name__ == "__main__":
    main()
