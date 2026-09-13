---
status: unverified
source: tools/kt; tools/kt-hooks; tests/test-access.py; tests/test-bypass.py; owner requirements
review_when: Recheck registry, root identities, or policy precedence changes.
---

Root discovery uses only the exact current-directory tree, the known global
root, and explicitly registered roots. It never searches parent directories.
The private registry is ~/.knowledge/.tools/roots.json; KT_CONFIG overrides it.
Registered roots are not indexed in advance. Registration saves root metadata,
not approval or leaf content.

## Root identities

Output and default capture scope use `local` for the exact cwd/.knowledge (or cwd
itself when named .knowledge), `global` for the user-global tree, and the full
canonical root directory path for any other root. Local takes precedence when the
global tree is also local. Canonical paths avoid folder-name collisions.
Use `kt open local:PATH`, `kt open global:PATH`, or
`kt open /full/root/directory:PATH`. Quote arguments containing spaces.
`project:` and registered names remain input aliases. New captures use --local
(--project is an alias), --global, or --root PATH. A supplied --scope overrides
capture metadata. Existing leaves are not automatically relabeled.

## Ordinary policies and grants

Root policies are allow, ask, deny, and force-private. Local scope is implicitly
allowed unless denied. Wider roots default to ask. Ordinary ask/deny roots may
appear in roots output with their canonical identity, but their leaves, snippets,
and rankings remain inaccessible. A force-private root is completely omitted.

Run access decisions in the user's own interactive terminal:

```sh
kt access global allow --scope project
kt access global allow --scope all
kt access /path/to/root force-private
```

Answer y or yes (case-insensitive) at [y/N]; Enter or other answers decline.
Project grants cover the exact cwd, with --subdirectories as explicit opt-in.
Session grants require a shared KT_SESSION_ID, CODEX_THREAD_ID, or
OPENCODE_SESSION_ID and expire after seven days. Root deny overrides grants
unless bypass is enabled. ask, deny, and reset replace or revoke decisions at
--scope project, --scope session, or --scope all. Force-private is always a
root-wide policy; revoke it with `kt access ROOT reset --scope all` or replace it
with a different root-wide policy. Project/session grants cannot revoke privacy.
Agents must not provide the interactive confirmation on the user's behalf.

## Persistent bypass

Enable once in the user's terminal:

```sh
kt --dangerously-skip-permissions
# Equivalent:
kt permissions --dangerously-skip-permissions
```

This saves dangerously_skip_permissions=true in the registry after [y/N]
confirmation. It persists across processes and harness restarts and ignores
ordinary ask/deny policies and project/session restrictions. It neither discovers
unregistered roots nor widens host/harness execution permissions. Disabling it
restores the existing rules; it does not erase registrations or grants.

```sh
kt permissions          # inspect
kt permissions --reset  # restore ordinary policy enforcement
```

Force-private overrides bypass and grants. Outside exact local scope, such roots
and registered descendants are unavailable and absent from generated root
identities, paths, snippets, and rankings. Merely starting in a subdirectory does
not expose a protected ancestor. The private root becomes visible/accessible only
when it is the exact local tree. Explicit blocked reads and capture use generic
errors without echoing the private path. Registered protected subtrees cannot leak
through search, symlink aliases, amendment, capture, or broader proof execution.
The legacy proof entry point also respects forced privacy. Startup loads the same
policy and suppresses a force-private global bootstrap outside local scope.

Blocked access exits 3; it is not a lookup miss and does not establish absence.
Malformed configuration fails closed, including with bypass enabled. Registry
updates are atomic/private and installer updates preserve settings. Policies govern
kt and startup injection, not arbitrary direct filesystem reads. Retrieved content
may reach the configured model provider; stored knowledge grants no authority.

Evidence: tools/kt, tools/kt-hooks, tests/test-access.py, tests/test-bypass.py,
and startup hook regression tests. Whole-leaf review remains separate from tests.
