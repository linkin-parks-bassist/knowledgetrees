---
status: unverified
source: tools/kt-hooks; install; integration tests; owner request
review_when: Recheck diagnostic patterns or hook payload changes.
---
Status: Green

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
current Codex live stdout-only payload shape and owner-authorized heuristic tradeoff.

Local deployment verified: an unwrapped SYNTH_BUILD_FAIL diagnostic delivered
the failure reminder and retained exit 1. Hook and installer integration tests passed.
