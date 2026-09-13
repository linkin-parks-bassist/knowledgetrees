---
status: unverified
updated_at: '2026-09-12T12:34:09+00:00'
verified_at: '2026-09-12T12:21:21+00:00'
verified_by: codex /root
scope: public knowledge-tree example
source: repository handler and installer; official Codex hooks, OpenCode plugins, and GitHub Copilot hooks documentation
verification: Tested diagnostic heuristics, explicit status precedence, failure bookkeeping, one-shot review, and retirement of the managed pre-tool wrapper. Live unwrapped diagnostic output delivered failure guidance; other harness model adoption remains unconfirmed.
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
plugin. After fully quitting OpenCode, relaunch with `opencode --continue` (last
session) or `opencode --session SESSION_ID` (a specific session). The installed
plugin applies to resumed sessions even if they predate installation: its hooks
handle subsequent activity and its bootstrap is added to the next model request.
It does not replay historical tool calls. If the TUI attaches to a separate
`opencode serve` or `opencode web` process, restart that backend too; reconnecting
the terminal alone does not reload its plugins. This follows the documented
startup loading and CLI resume/attach behavior plus the adapter's per-request
injection; a live pre-installation-session resume test remains unverified.
[Official OpenCode CLI](https://opencode.ai/docs/cli/).
Requests can fail if the session is unavailable or the model cannot run;
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

## Unwrapped failure detection

Use unwrapped PostToolUse with structured-status precedence and diagnostic-line
heuristics, plus existing Stop bookkeeping. No pre-tool command rewriting remains;
legacy `codex before` calls are inert. The installer removes only its managed
pre-tool definition and preserves unrelated hooks, including mixed hook groups.

Explicit exit status wins, including zero even when expected error text appears.
Otherwise inspect diagnostic shapes: error/fatal prefixes, compiler error locations,
Python traceback and exception lines, shell command/syntax/path failures, npm,
make/CMake/ninja failures, build-failure markers, and common network/file diagnostics.
Strip ANSI formatting and bound heuristic input to 256 KiB. Plain mentions of
errors, ordinary warnings, and zero-error summaries do not trigger reminders.
This is best-effort detection: silent nonzero Bash exits remain undetectable from
stdout-only transport, and printed or quoted diagnostic examples can false-trigger.

Completed calls and detected failures still update session counters and hashed
receipts. Repeated callbacks are deduplicated; detected failures arm the one-shot
Stop review. Ordinary prompts rearm the cycle; review prompts do not loop.
No raw commands, outputs, or diagnostic bodies are stored. Test coverage includes
positive/negative diagnostics, success precedence, failure deduplication, stop
arming, silent-output limits, and preservation/removal during installer migration.
Source: tools/kt-hooks, install, tests/test-hooks.py, tests/test-install.py;
current Codex live stdout-only payload shape and the documented heuristic tradeoff.

## Project orientation at startup

Codex SessionStart and OpenCode system-context bootstrap share the Python startup
loader. It resolves the supplied cwd and reads only that directory’s
.knowledge; it never searches parent directories. It appends where/am/i.md verbatim after the canonical procedure,
labeling the source and retaining the obligation to verify evidence/proofs.
It never substitutes a parent or global orientation when the local file is missing;
missing or oversized (over 64 KiB) orientation reports a diagnostic and retains
the canonical bootstrap. No root means no injected project orientation.
Codex startup/resume/clear/compact events use the same loader; OpenCode loads it
at plugin startup and retains a single block in rebuilt system context.
OpenCode still requires restart after installed plugin/context changes.

Both harnesses share diagnostic failure detection and Stop/idle bookkeeping.
OpenCode tests cover metadata-free diagnostics through tool.execute.after and
terminal tool-part events, explicit exit-zero precedence, and existing one-shot
review/session isolation. No command wrapping or uncertainty scanner is added.
Source: tools/kt-hooks; tools/kt-opencode.mjs; tests/test-hooks.py;
tests/test-opencode-hooks.mjs. Relevant integration checks passed.

Privacy boundary: automatic orientation injection is restricted to the supplied
session directory. Parent/home orientations are never searched or used as fallback.
The canonical global procedure remains loaded; this does not inject global orientation.
