---
status: green
revised_at: "2026-09-20T15:15:54+10:00"
---

## Success output policy

Under normal operation, silence = success and success = silence, following kt
prove. Successful create/rewrite/remove/move/combine/register operations and
identical no-ops emit no stdout or stderr; check exit 0. Access/permissions changes
retain required consent prompts and disclosures, without post-save receipts.
Reads, searches, help, policy inspection, dry-run previews and explicitly verbose
proof checks return the requested information. Failures retain diagnostics and
nonzero exit statuses; silence alone is not sufficient without checking status.
Accuracy/preservation reminders belong in the one-shot review hook.

## Command and address quick reference

- Create: `kt init [ORIENTATION]` creates `.knowledge/` in the current directory with empty canonical branches, `where/am/i.md`, and empty spec, plan, state, and next leaves. The argument, if given, is written literally. Existing trees are preserved.

- Initialize: `kt info` prints the canonical global procedure and exact local
  orientation, then the accessible dictionary, then the
  `kt prove --local` result. With no `./.knowledge` or no local `where/am/i.md` it
  falls back to the global orientation and `kt prove --global`. It fails only when the global
  procedure is unreachable, access needs approval, or the final proof check is brown. Run it directly and consume all output;
  never pipe it through `head`, `tail`, a pager, a filter, or any command that
  truncates or partially captures it. Initialization is incomplete unless the final
  proof summary is displayed.
- Dictionary: `kt dict` prints every useful segment occurring in the final two positions of leaf paths across all
  accessible roots on one sorted, comma-separated line. It reads path names, not
  leaf bodies, and never prints complete paths. Repeated segments appear once;
  segments of at most two characters, purely numeric segments, and broad
  grammatical/relational/generic/container stop words are omitted. `kt dict local global`
  restricts output to the named configured roots; canonical configured root paths
  are also accepted. Restricted and force-private material remains excluded.
- Lookup: `kt how to rewrite a knowledge leaf` or `kt find "rewrite knowledge leaf"`.
  Both search permitted active roots; neither accepts `--root`. Use `--limit 5`
  to bound search output without piping away the command exit status.
- Read: copy a returned address exactly into `kt open ADDRESS`. `local:PATH`
  selects only the current project; `global:PATH` selects only global knowledge.
  A qualified read never falls back to another root. General kt procedures normally
  live globally: `kt open global:how/to/rewrite/a/knowledge/leaf.md`.
  An external `ROOT:PATH` uses a configured canonical root identity from `kt roots`;
  it cannot substitute for registration/access. An absolute leaf filename has no colon.
- Proofs and leaf state: bare `kt prove` checks every accessible root. `kt prove --local` checks
  only the exact current-directory `.knowledge`; `kt prove --global` checks only
  global knowledge; `--root ROOT` selects another exact accessible tree. Exit 0
  means no selected leaf is brown; `--verbose` supplies diagnostics. Optional filters are separate
  semantic components, e.g. `kt prove --root .knowledge --no-stamp how to use`;
  every run reports green/yellow/brown totals and prints brown addresses only.
  Normal evaluation writes `status` in front matter; `kt check` writes `checked_at`;
  `--no-stamp` preserves bytes.
  Non-expiring leaves evaluate green unless a proof fails or brown falsification
  remains. Expired leaves evaluate yellow and need manual review; brown fails the
  command and requires diagnosis and repair.
  slash-containing leaf paths are not filters. Multiple tokens are disjunctive.
- Create: `kt add "what is the result" "Checked answer" --local`.
  Creation supports `--local`, `--global`, or `--root ROOT`; it refuses existing leaves.
  Add `--expires-at`, `--expires-every`, or `--verifiable` when justified.
- Rewrite inline: `kt rewrite ADDRESS HASH "Complete answer body"`.
  Use `--expires-at`, `--expires-every`, `--no-expiry`, `--verifiable`, or
  `--no-verifiable` to change optional metadata. Omitted options preserve it.
  HASH is a required positional revision supplied automatically on stderr by full
  leaf reads. No --expect option. --dry-run previews the diff. Successful writes
  produce no stdout or stderr (exit 0), without echoing either body. No-ops are
  also silent; dry-run shows the diff and failures report diagnostics. Accuracy and
  preservation reminders belong to the one-shot task-end capture-review hook.
- Manual check: `kt check ADDRESS HASH` records `checked_at` for the complete
  answer read at HASH. It does not run proofs; follow it with `kt prove`.
- Help: `kt COMMAND --help` describes options for that command. Options do not
  automatically transfer between commands. `kt open` takes an address, not `--root`.

Preserve exit status when diagnosing failures: use `--limit` for searches instead
of `| head`; a pipeline normally returns the final command's status. In a batch,
check each kt command rather than letting a later successful command hide failure.

Use `kt where is vivado` or `kt how to make a plan` for branch-directed lookup.
Words are consumed as directories one at a time. At the first unmatched word,
the remaining words are ranked only among leaves beneath the matched prefix.
If no candidate meets the default 60% meaningful-keyword coverage threshold,
search widens to the parent,
one level at a time. This transparent lexical-coverage heuristic is not confidence
or semantic similarity. `kt where is _` lists location leaves without a query.
Exact question-path hits return full contents on stdout and their SHA-256 revision
on stderr, frontmatter included; they do not
run proofs or establish correctness. Use `kt open` to read fallback list results.

Conventions: `does/` and `is/` answer yes/no questions; `where/is/` answers locations, `how/to/` procedures, `when/to/`
decision triggers, `what/is/` definitions/state, and `why/does/` or `why/is/`
rationale. Other complete question prefixes can be navigated under these starters.

Use `kt find leaves` for deliberately broad lookup, or pass a quoted question:
`kt find "how to add knowledge leaves"`. Words are matched case-insensitively;
question-shaped paths receive higher scores than body matches. This is lexical
retrieval, not a semantic model, and scores are not probabilities of correctness.
A no-match result exits 1 but does not establish that knowledge is absent.
When `kt` fails to find needed information, you MUST determine whether a leaf
exists: retry distinctive terms/synonyms and inspect plausible paths in the applicable
roots. If it exists, read or rewrite it; if absent, investigate and add the scoped
leaf. Preserve the established answer before the next unrelated tool call or
completion. Add a truthful unresolved record if blocked; forbidden writes require
a scoped handoff. Do not silently move on or create a duplicate from a lexical miss.

`kt roots` labels the exact current-directory tree local, the user-global tree global,
and other roots by full canonical root directory path. It lists the local/global trees
and registered roots without duplicates. Wider roots default to private; use
`kt access` for user-approved sharing. `KT_GLOBAL_ROOT` can override the global
root. Root discovery never walks parent directories. Ordinary restricted roots expose
no leaf paths/snippets; force-private roots expose no generated root identity either.

`kt open global:how/to/add/knowledge/leaves.md` selects a global leaf explicitly;
`local:` selects the exact local tree; `project:` is a compatibility alias. An unqualified relative path tries project
then global. Absolute Markdown leaf paths also work. Content and frontmatter are
returned verbatim on stdout; full reads also print Revision: HASH on stderr. Relative paths cannot escape the selected root.

`kt prove --no-stamp leaves` checks exact semantic-component tokens across all
accessible roots. Narrow with `--local`, `--global`, or `--root ROOT`; explicit
ROOT is the exact knowledge-tree directory from `kt roots`. Default proof checks may stamp
outcomes; lookup and open do not verify or stamp proofs.

Default output is compact plain text for agents. Non-exact searches print one
summary (`matches=shown/total`, adequate count, selected branch where applicable,
and `coverage=lexical`), then one tab-separated line per result: root-qualified
leaf address, keyword coverage with `weak` when below threshold, current leaf status, and an excerpt bounded to 160 characters. Rank order is
unchanged; coverage is not confidence. Excerpts help select a leaf and are not
complete answers. Open the chosen leaf before relying on it.

Use `kt --pretty find leaves`, `kt find leaves --pretty`, or
`kt where is vivado --pretty` for the expanded human layout. Pretty mode retains
scores, longer excerpts, spacing, reminders, and terminal-only colors; `NO_COLOR`
disables colors. Default output never emits ANSI colors, including in a terminal.
Both modes preserve exact question hits and `kt open` byte-for-byte, including
frontmatter. Search modes share ordering, limits, access checks, and exit statuses.
Empty or weak-only keyword matches exit 1; blocked root access exits 3.
Results show the current leaf status. Manual check time is distinct from proof
verification time. Check relevant proofs before reliance.
The installer puts the script in the global `.tools/kt` and links `~/.local/bin/kt`.

## MCP tools

When a harness has the knowledgetrees MCP server (installed by `./install`), the workflow is also available as tools with the same semantics: `kt_lookup` (`kt how to ...`), `kt_find`, `kt_read` (`kt open`, returning the revision), `kt_edit`, `kt_rewrite`, `kt_add`, `kt_dict`, `kt_roots`, and `kt_prove` (read-only unless `stamp` is set). Prefer `kt_edit` for small changes: it replaces exact text that must occur once in the answer body, against the revision from your read, and returns a diff. A miss or brown result comes back as data marked `(exit 1)`; only exit 2 or higher is a tool error. `info`, `init`, `check`, `rm`, `mv`, `combine`, `register`, `access`, and `permissions` remain CLI-only. Design and limits: `how/to/expose/structured/knowledge-tree/edits/across/local/agent/harnesses.md`.

## Persistent access settings

`kt --dangerously-skip-permissions` (or `kt permissions --dangerously-skip-permissions`)
saves a persistent bypass after user-terminal [y/N] confirmation. Inspect with
`kt permissions`; disable with `kt permissions --reset`. Bypass ignores ordinary
ask/deny and grants, but not force-private. Set a root-wide private exception with
`kt access /path/to/root force-private`; it is hidden/unavailable outside exact local
scope. See [root access](../control/knowledge/root/access.md) for precedence and aliases.

Lookup loads root access once and lazily reuses leaf text only within that lookup.
No persistent cache/index is created, and private roots are never indexed. Every
new invocation sees current configuration and filesystem changes.

## Remove, move, and coalesce leaves

Read a source revision with `kt open local:what/is/old.md`.
Use the hash printed on stderr for destructive single-leaf changes:

```sh
kt rm local:what/is/old.md --expect HASH --dry-run
kt mv local:what/is/old.md local:what/is/new.md --expect HASH
kt combine local:what/is/first.md local:what/is/second.md -o local:what/is/cohesive.md
```

Combine coalesces destructively: Markdown bodies are concatenated in input order
under one destination header, then source names are removed only after a successful
save. If output is an existing leaf, supply its --expect revision. An input that is
the destination is retained; other inputs are removed. `--dry-run` writes/removes
nothing. Sources are revision/inode checked before saving and removal; detected
concurrent changes are retained. Cleanup across multiple files is not transactional:
interruption or a conflict can leave sources beside the saved destination. Inspect
that state before retrying so content is not duplicated. Source answer bodies, including unresolved blockers and next checks, survive.
A brown source keeps the combined leaf brown. Manual check time and inherited
proof stamps are reset for review.

Move refuses an existing destination and preserves bytes. Same-filesystem moves
preserve hardlink identity; cross-filesystem moves copy exclusively before removing
the source. Removing a name leaves other hardlinks intact. No command prunes empty
canonical branches or updates links automatically. Review scope, links,
orientation, current-state projections, and affected proofs after maintenance.
All operations enforce source/destination access and force-private boundaries.
