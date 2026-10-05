---
status: green
revised_at: "2026-09-30T16:03:25+10:00"
---

Root discovery uses only the exact current-directory tree, the known global
root, and explicitly registered roots. `kt init` registers the tree it creates
under `ask` without granting access elsewhere. Lookup and mutation never search
parent directories. The presentation-only `kt info` walk is the exception: it
checks `.knowledge/where/am/i.md` from `~` down to the working directory and prints
only ancestor orientations whose roots are accessible from that working directory;
it does not add those roots to discovery.
The private registry is ~/.knowledge/.tools/roots.json; KT_CONFIG overrides it.
Registered roots are not indexed in advance. Registration saves root metadata,
not approval or leaf content.

## Root identities

Output and default add scope use `local` for the exact cwd/.knowledge (or cwd
itself when named .knowledge), `global` for the user-global tree, and the full
canonical root directory path for any other root. Local takes precedence when the
global tree is also local. Canonical paths avoid folder-name collisions.
Use `kt_read` (shell: `kt open`) with `local:PATH`, `global:PATH`, or
`/full/root/directory:PATH`. Quote arguments containing spaces.
`project:` and registered names remain input aliases. New answers use --local
(--project is an alias), --global, or --root PATH. A supplied --scope overrides
the target root. Existing leaves are not automatically relabeled.

## Ordinary policies and grants

Root policies are allow, ask, deny, and force-private. Local scope is implicitly
allowed unless denied. Wider roots default to ask. Ordinary ask/deny roots may
appear in roots output with their canonical identity, but their leaves, snippets,
and rankings remain inaccessible. A force-private root is completely omitted.

Run access decisions in an interactive terminal:

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
Only the user may authorize access. A direct, unambiguous instruction to see,
read, or access a named root, including “grant yourself access,” is explicit
authorization once kt resolves that registered label or path. Unless the user
requests broader access, use the least sufficient scope, normally project scope
for a project task. An agent may then answer the matching CLI confirmation; this
carries out the user's decision rather than inventing one. Ask only when the root
or intended scope is genuinely ambiguous. Inspect the displayed resolved root and
scope before answering, and never substitute the persistent global bypass.

Seeing and revoking grants: `kt grants [ROOT]` lists each root's effective access and its source (local tree, project grant and where it was made, allowed everywhere, session grant, permissions bypass, denied, or none) and marks roots whose tree is gone. `kt access ROOT revoke [--scope project|all]` narrows access already granted: project scope makes the root require approval again for this directory (overriding an everywhere-allow for this project only), and `all` does so everywhere and drops every project grant for it, or removes the registration of a missing root. Like other changes it needs interactive confirmation, either from the user or from an agent carrying out explicit authorization for that exact change. The local tree, a permissions bypass, and session grants cannot be revoked this way.

Stale approvals: grants are keyed by path, so on every run `kt` drops project grants whose project directory or root no longer exists, registered roots allowed everywhere whose tree is gone, and auto-named `root-<hash>` ask registrations whose tree is gone, printing a one-line notice on stderr; a tree recreated at that path then needs a fresh approval. Deny and force-private entries and user-named ask registrations are kept because they protect or name a tree that may only be unmounted. A tree deleted and recreated between two `kt` runs is not detected.

Asking through the harness: an agent calls `kt_access_request(root, reason, preferred_scope)` with the least scope that satisfies the task. The user still chooses. When the harness supplies `KT_SESSION_ID`, `CODEX_THREAD_ID`, or `OPENCODE_SESSION_ID`, temporary session access is offered alongside project, project-with-subdirectories, and everywhere. Only an accepted response saves a grant. Decline, cancellation, invalid replies, client errors, and clients without elicitation change nothing and return a structured one-time pending request. If the conversation already contains a direct, unambiguous instruction to access the resolved root, that instruction supplies the explicit authorization needed for `kt_access_confirm`; choose the least sufficient scope unless the user requested a broader one. Otherwise ask for the exact root and scope. `kt_access_status` returns readable text plus structured root/source data. `kt_access_revoke` removes session access directly, narrows this project directly, and asks before wider changes; failed confirmation returns a matching structured continuation. Direct policy administration and the persistent permissions bypass remain terminal-only.

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
when it is the exact local tree. Explicit blocked reads and add use generic
errors without echoing the private path. Registered protected subtrees cannot leak
through search, symlink aliases, rewrite, add, or broader proof execution.
Startup loads the same
policy and suppresses a force-private global bootstrap outside local scope.

Blocked access exits 3; it is not a lookup miss and does not establish absence.
Malformed configuration fails closed, including with bypass enabled. Registry
updates are atomic/private and installer updates preserve settings. Policies govern
kt and startup injection, not arbitrary direct filesystem reads. Retrieved content
may reach the configured model provider; stored knowledge grants no authority.

Evidence: tools/kt, tools/kt-hooks, tests/test-access.py, tests/test-bypass.py,
and startup hook regression tests. Whole-leaf review remains separate from tests.
