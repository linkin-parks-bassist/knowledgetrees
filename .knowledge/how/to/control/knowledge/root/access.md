---
status: green
revised_at: "2026-09-30T16:05:00+10:00"
---

Knowledge-root access is enforced by the CLI semantic spine and inherited by MCP and hooks. Discovery uses only the exact current-directory tree, the global root, and explicitly registered roots; parent trees are not lookup roots. The presentation-only `kt info` ancestor walk may show accessible orientations without granting discovery access.

Canonical output identities are `local`, `global`, or an absolute registered root path. Registration records a root under `ask`; it never grants access. Leaf paths and roots provide scope, so no scope field is stored in leaves.

## Policy and grants

Policies are `allow`, `ask`, `deny`, and `force-private`. Exact local scope is implicitly available unless denied. Wider roots default to ask. Force-private roots are omitted outside their exact local scope and override every grant and bypass.

Grants may be:

- session-scoped, when a stable `KT_SESSION_ID`, `CODEX_THREAD_ID`, or `OPENCODE_SESSION_ID` exists;
- project-scoped for the exact working directory, optionally including subdirectories;
- root-wide.

Choose the least sufficient scope. Session grants expire after seven days. Project/session grants cannot override root policy denial or privacy. Blocked access exits 3 and is not a lookup miss.

The interactive terminal commands remain available for direct administration:

```sh
kt access global allow --scope project
kt access global allow --scope session
kt access global allow --scope all
kt access /path/to/root force-private
```

Only the user may authorize an access decision. A direct, unambiguous instruction to see, read, or access a named root, including “grant yourself access,” is explicit authorization once kt resolves that registered label or path. Unless the user requests broader access, use the least sufficient scope, normally project scope for a project task. An agent may then answer the matching terminal confirmation; it asks again only when the root or intended scope is genuinely ambiguous.

## MCP flow

`kt_access_status` reports effective access and its source in readable and structured form. `kt_access_request` accepts an optional preferred scope, resolves policy through the CLI, and asks through harness elicitation. Session is offered only when the harness provides a stable session identity. An accepted choice is applied through the same CLI access functions.

Cancellation, an unrendered prompt, invalid response, client error, or lack of elicitation capability grants nothing. The result may include a structured one-time pending request ID. If the conversation already contains a direct, unambiguous instruction to access the resolved root, that instruction supplies the explicit authorization needed for `kt_access_confirm`; use the least sufficient scope unless the user requested a broader one. Otherwise ask for the exact root and scope. Unknown, reused, mismatched, denied, and force-private requests fail.

`kt_access_revoke` directly relinquishes the current session grant or exact-project grant. A wider revocation uses elicitation or its own exact one-time continuation after explicit authorization. Reducing authority never requires agents to use the terminal merely because the grant was session-scoped.

## Persistent bypass and safety

The user may explicitly enable the persistent permissions bypass in a terminal with `kt --dangerously-skip-permissions` and disable it with `kt permissions --reset`. It ignores ordinary ask/deny and project/session restrictions but does not discover roots, widen host permissions, or override force-private. MCP does not expose this switch or direct policy administration.

Registry updates are atomic and private. Stale grants and eligible vanished registrations are pruned without leaking protected paths. Symlinks, search, proofs, mutations, startup injection, and broader roots cannot bypass access checks. Policies govern kt-mediated access, not arbitrary filesystem reads; retrieved content may reach the configured model provider, and stored knowledge never grants authority.
