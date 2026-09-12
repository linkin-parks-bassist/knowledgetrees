---
status: unverified
updated_at: '2026-09-12T12:34:09+00:00'
verified_at: '2026-09-12T12:21:21+00:00'
verified_by: codex /root
scope: public knowledge-tree example
source: repository handler and installer; official Codex hooks, OpenCode plugins, and GitHub Copilot hooks documentation
verification: Reviewed protocols and tested the observed Codex stdout-only shape; live wrapped false delivered developer-context guidance without changing stdout or exit status. Automatic wrapping awaits new hook trust; OpenCode/Copilot model behavior remains untested.
review_when: Recheck after harness hook-schema or lifecycle changes.
---

Install failure-triggered lookup/capture reminders and one-shot task-end capture
reviews with the knowledge-tree installer. For an existing root, use
`./install --hooks-only --force` to update infrastructure while preserving leaves
and hardlinked skills. Preview first with `--dry-run`.

The shared Python handler lives at `~/.knowledge/.tools/kt-hooks`. Codex definitions
merge into `~/.codex/hooks.json`; OpenCode loads
`~/.config/opencode/plugins/knowledgetrees.js`; Copilot CLI loads the dedicated
`~/.copilot/hooks/knowledgetrees.json`. Unrelated hooks remain intact, and differing
managed adapter files require explicit replacement permission via `--force`.

Successful proof timestamp refreshes alone do not conflict on reinstall; their
installed stamps are preserved until rechecked. Edited content, falsified markers,
and sticky leaf falsification flags remain protected differences.

The shared installed handler is executable at `~/.knowledge/.tools/kt-hooks`.

Proof: (verified at 2026-09-12T22:05:28+10:00)

```sh
test -x "$HOME/.knowledge/.tools/kt-hooks"
```

## When reminders run

Detected tool failure -> check `kt` for a known explanation/fix; inspect relevant
knowledge and eligible proofs; diagnose within authority; then capture the reusable
answer or amend its existing owner. Expected negative tests do not require invented
discoveries. A search miss requires alternate terms and scoped inspection before
declaring absence. Unresolved knowledge needs its blocker and next check.

Task end -> request a capture review after a failure or at least 10 completed tool
calls in the work cycle. The review may capture missing answers, amend owners, or
conclude that there is nothing new. This does not certify that capture happened.
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

Codex's native `SessionStart` hook reads the canonical bootstrap procedure and
returns its body as `hookSpecificOutput.additionalContext` developer context.
It matches startup, resume, clear, and compact, not ordinary user prompts.
The procedure is already loaded; no bootstrap skill invocation is needed.
On resume/compaction, preserve completed initialization and restore only lost
context or changed scope. Review/trust the new definition in `/hooks` and start
a fresh session to test it. Protocol tests cover all four lifecycle sources;
live startup compliance remains unconfirmed. Missing/invalid procedure files
fail open with a diagnostic; they do not grant permissions or run proofs.

The observed Codex Bash `PostToolUse` payload contains stdout text, not an exit
code; a silent failure therefore cannot be detected from that response alone.
Its `PreToolUse` adapter runs the command once in a Bash subshell, records the exit
status in a private hashed receipt, preserves stdout, and exits with the original
status. The post-tool handler joins that receipt to detect silent failures.
Quotes, syntax errors, `exit`, `exec`, and `set -e` have regression coverage.
Because Codex requires `permissionDecision: allow` for `updatedInput`, wrapping
runs only in sessions already reporting `bypassPermissions`. Approval-based
sessions are never auto-approved; native structured failure detection remains
available when provided. Do not weaken permissions just to enable the bridge.

The handler adds `hookSpecificOutput.additionalContext` without suppressing the original
result. `Stop` can request a continuation with `decision: block` and `reason`;
this is not guaranteed pre-display gating. Use `/hooks` to review and trust new
definitions: installation does not bypass that requirement.
[Official Codex hooks](https://learn.chatgpt.com/docs/hooks).

OpenCode's plugin reads the canonical `how/to/use/knowledgetrees.md` at startup
and includes its procedure body once in each assembled model system context.
This is harness-owned context, not repeated skill invocation or new conversation
messages. It is also available after compaction; the compaction hook asks the
summary to preserve completed initialization, checked evidence, and open captures.
Startup work remains once per fresh session, not per turn. Focused skills still
apply when triggered. Restart after editing the canonical procedure. Only the
procedure is loaded, not the entire tree; it may be sent to the configured provider.
Missing or empty procedure files report a diagnostic and leave other hooks active.
Adapter tests cover injection, duplicate prevention, request/session availability,
and compaction context; model compliance still requires an uncoached live test.

OpenCode's adapter inspects shell result metadata and terminal tool-part events,
queues failed-tool guidance into subsequent model context, and requests a synthetic
capture-review prompt on `session.idle`. It preserves the selected agent/model
when available and guards its follow-up cycle. Restart the harness to load the local
plugin. Requests can fail if the session is unavailable or the model cannot run;
errors are reported, not retried in a loop.
[Official OpenCode plugins](https://opencode.ai/docs/plugins/).

Copilot CLI uses `postToolUse` for completed results, `postToolUseFailure` for tool
errors, and `agentStop` for completion review. Command failure hooks return recovery
context with exit `2`; normal results use `additionalContext`. Start a new CLI
session to load hooks. User-level hooks can be disabled by the harness's own policy
or `disableAllHooks`; the installer does not weaken such controls.
[Official Copilot hooks](https://docs.github.com/en/copilot/reference/hooks-reference).

Only supported tool paths and detectable failure statuses can trigger reminders.
Missing session ids or broken storage fail open with diagnostics, never by sharing
state between sessions. This is a local reliability mechanism, not an adversarial
enforcement boundary. It does not authorize access, edits, escalation, publication,
or automatic proof execution. Local Copilot CLI installation does not configure
VS Code or ephemeral Copilot cloud jobs.
