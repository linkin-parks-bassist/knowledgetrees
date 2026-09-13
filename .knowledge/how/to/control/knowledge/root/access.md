---
status: unverified
source: tools/kt; tools/kt-hooks; tests/test-access.py; current owner requirements
review_when: Recheck registry schema, grant scope, or root discovery changes.
---

Root discovery uses the explicit current-directory tree, the known global tree,
and a private user-global registry at `~/.knowledge/.tools/roots.json` (KT_CONFIG
overrides the registry path). It never walks parent directories. Configured roots
are not indexed in advance; queries read only permitted roots. Registration saves
only a root name, canonical path and policy. An unfamiliar capture target is
registered with access=ask; registration does not grant wider access or write the
requested leaf until approved. Register deliberately with `kt register NAME PATH`.

Policies are allow, ask and deny. Only the tree in the explicit cwd (or cwd itself when named .knowledge) is local
scope and implicitly permitted unless denied; wider/global/cross-repo roots
need approval by default. An allow root policy opens it to all projects; deny wins.
Private roots can have pairwise project-to-root approvals saved persistently.
Project approvals apply to the exact directory by default. `--subdirectories`
explicitly opts in to descendants; granting from a home directory without that
option cannot authorize all repositories below it.

Use `kt access ROOT` to inspect policy. In the user's own terminal,
`kt access ROOT allow --scope project` saves pairwise trust; --scope all saves
open access; --scope session saves a session decision in private SQLite state.
Session scope needs the same KT_SESSION_ID (or CODEX_THREAD_ID/OPENCODE_SESSION_ID)
in the user's terminal and agent environment. Grants expire after seven days;
distinct session identifiers isolate them. `deny`, `ask`, or `reset` replace or
revoke decisions at the chosen scope. Mutation requires an interactive `[y/N]` confirmation: `y` or `yes` (case-insensitive)
approves; Enter or any other response declines. Noninteractive agent lookups never
save approvals automatically. Agents must not
supply that confirmation themselves. Retrieval can send content to the configured
model provider. Policies govern kt and startup injection, not direct filesystem reads.

Search, exact questions, relative and absolute open, capture and proof respect
access. Restricted roots expose no leaf paths/snippets/rankings; roots reports
restricted paths as hidden. Registered restricted subtrees cannot leak through
an allowed ancestor; proof rejects scopes containing restricted registered trees.
Blocked access exits 3, is not an answer lookup miss, and does not imply absence.
Malformed configuration fails closed. Registry writes are atomic and private;
installer updates preserve the user registry. Both harnesses share policy loading
and startup suppression for denied local orientations.

Evidence: tests/test-access.py checks no content leakage, persistent/new-process
approvals, cross-project isolation, exact/opt-in descendant behavior, session
isolation, revoke/deny/open override, private capture registration, absolute paths,
and nested restricted roots. Existing CLI, hook, OpenCode adapter and installer
suites pass with explicit access fixtures. Fixture adjustments reflect the new
privacy defaults; old globally-open discovery is intentionally superseded.
