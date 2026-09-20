---
status: green
revised_at: "2026-09-20T10:52:38+10:00"
---

Install failure-triggered lookup/capture reminders and one-shot task-end capture
reviews with the knowledge-tree installer. For an existing root, use
`./install --hooks-only --force` to update infrastructure while preserving leaves
and hardlinked skills. Preview first with `--dry-run`.

The shared Python handler lives at `~/.knowledge/.tools/kt-hooks`. Claude Code definitions
merge into `~/.claude/settings.json` (other settings and hooks are preserved, and the
file's mode is kept); Codex definitions
merge into `~/.codex/hooks.json`; OpenCode loads
`~/.config/opencode/plugins/knowledgetrees.js`; Copilot CLI loads the dedicated
`~/.copilot/hooks/knowledgetrees.json`. Unrelated hooks remain intact, and differing
managed adapter files require explicit replacement permission via `--force`.

Successful proof timestamp refreshes alone do not conflict on reinstall; their
installed stamps are preserved until rechecked. Edited content, falsified markers,
and sticky `status: brown` remain protected differences.

The shared installed handler is executable at `~/.knowledge/.tools/kt-hooks`.

Proof: (verified at 2026-09-18T13:49:02+10:00)

```sh
test -x "$HOME/.knowledge/.tools/kt-hooks"
```

## When reminders run

Detected tool failure -> check `kt` for a known explanation/fix; inspect relevant
knowledge and eligible proofs; diagnose within authority; then capture the reusable
answer or rewrite its existing owner. Expected negative tests do not require invented
discoveries. A search miss requires alternate terms and scoped inspection before
declaring absence. Unresolved knowledge needs its blocker and next check.

Task end -> request a capture review after a failure or at least 10 completed tool
calls in the work cycle. The review may capture missing answers, rewrite owners, or
conclude that there is nothing new. It also reminds agents to ensure rewritten
knowledge is accurate and no still-valid knowledge was lost. Rewrite success and no-ops
are silent, so batching rewrites does not repeat that reminder.
This does not certify that capture happened.
One review is requested per cycle; review-generated prompts do not rearm it.
The next ordinary user prompt starts a fresh activity cycle. Set
`KT_HOOK_MIN_CALLS` to a positive integer in the harness environment to tune the
activity threshold. Tool count approximates substantial work, not semantic value.

Counters and hashed receipts persist in an SQLite database under
`${XDG_STATE_HOME:-~/.local/state}/knowledgetrees`, overridable with
`KT_HOOK_STATE_DIR`. Harness/session keys isolate concurrent sessions; duplicate
terminal event receipts do not increment counts again. Entries expire after seven
days. Raw commands, inputs, outputs, errors, and knowledge are not stored. The
handler performs no model calls and never runs or writes leaf bodies.

## Harness contracts and activation

To establish a harness's real hook payloads, do not rely on a summarized docs fetch: on 2026-09-20 one gave wrong Claude Code field names (`session_start_reason`, `user_prompt`, a `permissionDecision` Stop output) and a second fetch was truncated. Instead run the harness non-interactively with a throwaway settings file whose hooks append their stdin to a scratch log (for Claude Code: `claude -p PROMPT --settings FILE --allowedTools Read`, with one tool call that fails and one that succeeds), then read the captured JSON. Use `--allowedTools`, redirect stdin from `/dev/null`, and set a timeout.

Claude Code's `SessionStart` hook (matcher `startup|resume|clear|compact`) returns the same
boot output as `hookSpecificOutput.additionalContext`. Claude payloads carry `source`, `prompt`,
`session_id`, and `stop_hook_active`. Tool failures arrive as a separate `PostToolUseFailure`
event (with `error` and `is_interrupt`); `PostToolUse` fires only on success and carries no exit
status, so the adapter applies no text heuristics there. Interrupted calls do not count as
failures. `Stop` continues via top-level `decision: block` and `reason`. Review new definitions
with `/hooks` and restart Claude Code to test. Verified against a live session: it received the
complete boot output and listed all five skills. The boot output was about 9.8 KB; if it
grows much beyond 10 KB, confirm the harness does not truncate injected hook context.

Codex's native `SessionStart` hook runs `kt boot` and injects its complete output,
including the canonical procedure, exact local orientation, dictionary, and final
local proof summary. It matches startup, resume, clear, and compact, not ordinary
user prompts. A failed boot is shown as a diagnostic and must be repaired before
relying on the tree. Review/trust the new definition in `/hooks` and start a fresh
session to test it. Protocol tests cover all four lifecycle sources.

Codex Bash PostToolUse can supply stdout alone without an exit code. The adapter
prefers structured failure statuses when available and otherwise uses diagnostic-line
heuristics. Successful explicit exit status suppresses heuristic matches. It never
rewrites commands or requests permission decisions. Silent nonzero exits can be
missed; quoted diagnostic output can produce false positives. The installer retires
its former managed PreToolUse bridge while preserving unrelated hooks.

The handler adds `hookSpecificOutput.additionalContext` without suppressing the original
result. `Stop` can request a continuation with `decision: block` and `reason`;
this is not guaranteed pre-display gating. Use `/hooks` to review and trust new
definitions: installation does not bypass that requirement.
[Official Codex hooks](https://learn.chatgpt.com/docs/hooks).

OpenCode's plugin supplies the same complete `kt boot` output in assembled model
system context. It remains available after compaction; the compaction hook asks the
summary to preserve checked evidence and open captures. Focused skills still apply
when triggered. Restart after editing the adapter. Adapter tests cover injection,
duplicate prevention, request/session availability, and compaction context.

Source: tools/kt-hooks, install, tests/test-hooks.py, tests/test-install.py;
current Codex live stdout-only payload shape and the documented heuristic tradeoff.

## Startup initialization

Claude Code and Codex SessionStart, OpenCode system-context startup, and Copilot CLI sessionStart run `kt boot` in the exact working directory and inject its complete output: canonical global procedure,
exact local orientation, dictionary, and local proof result. A missing local tree is not a failed boot: `kt boot` falls back to the global root. A genuinely failed boot (unreachable procedure, access needing approval, brown proofs) is reported in context, and the hook still injects it. OpenCode and Copilot CLI require restart after installed hook changes. The handler protocol tests cover Copilot startup output; live Copilot model reception has not been observed. [GitHub Copilot hook reference](https://docs.github.com/en/copilot/reference/hooks-reference).

The harnesses share diagnostic failure detection and Stop/idle bookkeeping.
Startup uses the exact current-directory local root for orientation and normal
access policy for the dictionary; it never searches parent directories. The
injected contents follow that same scope and access boundary.

## Review before commit or push

A tool-before event can detect a pending shell command, but detection does not
establish that a model reviewed knowledge before the command executes.
Codex PreToolUse exposes tool_input and supports additionalContext without
blocking, or permissionDecision=deny to reject the call. OpenCode's
tool.execute.before exposes input/output.args; its documented rejection mechanism
is throwing an error. It does not document a model-context return field for this
before event. Queuing context through the existing system transform reaches a
later model request and cannot guarantee review before the pending command.
A guaranteed before-command review needs call rejection and an agent retry after
review. The installer does not install a boundary-blocking mechanism.
These are API capabilities and timing limits, not demonstrated model compliance.
Sources: [Codex hooks](https://learn.chatgpt.com/docs/hooks#pretooluse) and
[OpenCode plugins](https://opencode.ai/docs/plugins/).

Restart an OpenCode backend after updating its startup plugin/handler so newly
resumed sessions receive the compact initialization instruction.
