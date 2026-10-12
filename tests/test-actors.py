#!/usr/bin/env python3
"""Actor authority follows a trusted launcher, never the containing project."""
import argparse
import io
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
from unittest.mock import patch

CLI = Path(__file__).resolve().parents[1] / 'tools/kt'
SERVER = CLI.with_name('kt-mcp')


def main():
    with tempfile.TemporaryDirectory(prefix='kt-actors-') as temporary:
        base = Path(temporary)
        projects = [base / 'one', base / 'two']
        vault = base / 'vault'
        for path in projects:
            (path / '.knowledge').mkdir(parents=True)
        vault.mkdir()
        (vault / 'answer.md').write_text('Actor fixture knowledge.\n')
        config = base / 'roots.json'
        original = {'roots': {'vault': {'path': str(vault), 'access': 'ask'}}, 'projects': {}}
        config.write_text(json.dumps(original))
        env = {**os.environ, 'KT_CONFIG': str(config), 'KT_GLOBAL_ROOT': str(base / 'global'),
               'KT_MCP_CLI': str(CLI), 'KT_ACCESS_STATE_DIR': str(base / 'state')}
        env.pop('KT_ACTOR', None)

        def command(*args, actor=None, cwd=projects[0], expected=0):
            selected = {**env, **({'KT_ACTOR': actor} if actor is not None else {})}
            result = subprocess.run([sys.executable, str(CLI), *args], cwd=cwd, env=selected,
                                    text=True, capture_output=True, timeout=10)
            assert result.returncode == expected, (args, result.stdout, result.stderr)
            return result.stdout + result.stderr

        command('open', 'vault:answer.md', expected=3)
        command('actor', 'coin', 'allow', expected=3)
        assert json.loads(config.read_text()) == original
        api = runpy.run_path(str(CLI))
        with patch.dict(os.environ, env, clear=True), patch('sys.stdin.isatty', return_value=True), \
                patch('builtins.input', return_value='y'), patch('sys.stdout', new=io.StringIO()):
            assert api['actor_command'](argparse.Namespace(name='coin', decision='allow')) == 0
        granted = json.loads(config.read_text())
        assert granted['projects'] == original['projects'] and granted['roots'] == original['roots']
        for project in projects:
            assert 'Actor fixture' in command('open', 'vault:answer.md', actor='coin', cwd=project)
            assert 'actor grant (coin)' in command('grants', actor='coin', cwd=project)
            command('open', 'vault:answer.md', cwd=project, expected=3)
            command('open', 'vault:answer.md', actor='another-bot', cwd=project, expected=3)
        # New registrations automatically participate, without rewriting the actor grant.
        fresh = base / 'fresh'; fresh.mkdir(); (fresh / 'answer.md').write_text('Fresh actor fixture.\n')
        current = json.loads(config.read_text()); current['roots']['fresh'] = {'path': str(fresh), 'access': 'ask'}
        config.write_text(json.dumps(current))
        assert 'Fresh actor' in command('open', 'fresh:answer.md', actor='coin')
        command('open', 'fresh:answer.md', expected=3)
        # Ordinary root denial and forced privacy remain stronger than actor authority.
        for policy in ('deny', 'force-private'):
            current['roots']['vault']['access'] = policy; config.write_text(json.dumps(current))
            output = command('open', 'vault:answer.md', actor='coin', expected=3)
            assert 'Actor fixture knowledge' not in output
        current['roots']['vault']['access'] = 'ask'; config.write_text(json.dumps(current))
        # The actual MCP subprocess inherits identity; its claimed client name grants nothing.
        def mcp(actor):
            selected = {**env, **({'KT_ACTOR': actor} if actor else {})}
            with subprocess.Popen([sys.executable, str(SERVER)], cwd=projects[0], env=selected,
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True) as server:
                def rpc(ident, method, params):
                    server.stdin.write(json.dumps({'jsonrpc': '2.0', 'id': ident, 'method': method, 'params': params})+'\n'); server.stdin.flush()
                    return json.loads(server.stdout.readline())
                rpc(1, 'initialize', {'clientInfo': {'name': 'coin', 'version': '1'}, 'capabilities': {}})
                result = rpc(2, 'tools/call', {'name': 'kt_read', 'arguments': {'address': 'vault:answer.md'}})
                server.stdin.close(); server.wait(timeout=10)
                return json.dumps(result)
        assert 'Actor fixture knowledge' in mcp('coin')
        assert 'Actor fixture knowledge' not in mcp(None)
        command('open', 'vault:answer.md', actor='bad actor', expected=2)
        current['actors'] = {'coin': ['allow']}; config.write_text(json.dumps(current))
        command('open', 'vault:answer.md', actor='coin', expected=2)
        current['actors'] = {}; config.write_text(json.dumps(current))
        command('open', 'vault:answer.md', actor='coin', expected=3)
    print('actor identity and MCP isolation checks passed')


if __name__ == '__main__':
    main()
