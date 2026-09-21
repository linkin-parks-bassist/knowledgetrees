---
status: green
revised_at: "2026-09-21T14:30:55+10:00"
name: "knowledgetrees-capture"
description: "Use after kt misses or reusable discoveries: establish leaf existence, update or add scoped knowledge, and capture before the next unrelated tool call; include truthful provenance and eligible proofs."
---

Capture an established reusable answer before the next unrelated tool call or
completion; necessary verification and capture calls are part of resolving it.
Use `kt_find` and `kt_read` (shell: `kt find`, `kt open`) to check for an existing owner before writing.
Prefer a question-prefix query when the answer category is known: `where is`
for locations, `how to` for procedures, `when to` for triggers, `what is` for
definitions/state, and `why does` or `why is` for rationale. Place the full
sentence-derived leaf under that branch so queries exclude unrelated answer kinds.
If `kt` fails to find information, determine whether the leaf exists through
alternate keywords and scoped semantic inspection. If it exists, use or rewrite it;
if it does not, add it at the correct scope. A lexical miss never establishes absence.
A checked hit needs no duplicate capture. If unresolved, record the blocker and
next check in the answer.
Do not resume surrounding work with an outstanding capture obligation. The agent's
own uncertainty remains an additional capture signal, not the only trigger.

## Capture every scale of knowledge

Capture fine-grained implementation answers as readily as architecture and specs.
Do not reject a discovered fact because it is "just a code comment", a single
function, typedef, include-order constraint, file, or folder. Record what a function
does and why, contracts and invariants, what a file contains, where a type lives,
and dependency/layout details at their owning project or subsystem scope. There is
no minimum abstraction, complexity, or answer-length threshold for capture.

Examples of complete question routes include `what does f do`, `why does f check
its input`, `what does file z contain`, `where is typedef y declared`, `what is the
required include order`, and `how is the repository structured`. These are example
questions, not claims that such leaves already exist. Preserve literal identifiers
when needed to locate the answer. Answer in the leaf body and attribute checked
source evidence; keep review conditions tied to the code or structure that can change.

## Choose the owner and path

Put host/personal tooling in `~/.knowledge` and project/subsystem facts in the
nearest applicable local root. Never promote professional, customer, partner, or
restricted material into the global tree; sanitize anything intended for publication.
Keep an existing owner in context before editing. Full reads return the complete
answer and its revision hash; there are no partial reads. Use `kt_rewrite` as the
standard editing method with that hash. Use `kt_edit` only for economy on a tiny
surgical exact replacement.
Preserve still-valid knowledge and reread/merge if the leaf changed.
Use `kt_read` (shell: `kt open ROOT:PATH`) for that read and `kt_prove` (shell: `kt prove --root ROOT TOKEN`) after
changing eligible proofs. Create a new leaf in one call with `kt_add`; the shell equivalent is:

```sh
kt add "how to prepare the demo" "Run the project's documented demo command."
```

`capture` is an alias for `add`. The exact current-directory local root is the default, falling
back to global; choose `--global`, `--local` (`--project` is an alias), or `--root example` explicitly when
scope matters. `--dry-run` previews without
writing. Pass `-` as the answer to read multiline Markdown from stdin.
If the question or answer might begin with `-` (for example `-foo`; a Markdown list item like `- step` is fine), put `--` before them, as in `kt add --local -- "how to x" "-foo"`, or the parser reports a missing answer. `-` alone as the answer reads stdin.

The command preserves repeated words and hyphenated components, creates metadata,
and refuses existing owners rather than overwriting them. It records new answers
with `status: green` (starting the `checked_at` clock only when `--expires-every` is given), never invents a proof, and never executes
the supplied body. Pass only answer Markdown; `kt` generates the front matter.
Use `--expires-at TIMESTAMP` or `--expires-every DURATION` when a fact has a real
time-based freshness boundary. Use `--verifiable` only after checking that every
claim is covered by eligible proofs. Review the answer before recording `checked_at`;
inspect and run eligible proofs separately. For an unresolved question, supply
`--unresolved --blocker "missing evidence" --next-check "specific next investigation"`.

Write the full natural-language question first. Lowercase it, remove only punctuation
not belonging to a literal identifier, replace spaces with `/`, and add `.md` to
the last word. Keep grammatical words such as `to`, `is`, `the`, `of`, and `for`.
The slash-expanded path must read as the complete question. Hyphenate genuinely
multi-word components; never use underscores or implementation-shaped category
buckets. For example, "how to check knowledgetree proofs" becomes
`how/to/check/knowledgetree/proofs.md`.

Write the answer first, then the context, preconditions, limits, eligible proofs, and
links needed to use it. Leaves directly answer their paths rather than outsourcing
the answer to internal monolithic documents. Link alternate routes to a canonical
answer instead of copying it; record the conclusion and the distinction that made
it non-obvious. A leaf is a current answer, never a log: do not append task chronology,
session notes, progress updates, tool transcripts, or stream of consciousness.
Log-shaped leaves are tree poisoning because stale events become indistinguishable
from current truth and retrieval sends later agents down contradictory paths. Rewrite
the current answer in place. Retain history only when it explains a present constraint
or decision; use Git or a purpose-built external log for chronology.

## Size and provenance

Semantic atomicity is guidance, not a word-count cap or automatic partitioning rule.
Consider relation, likely queries, joint use, ownership, lifecycle, volatility,
fan-out, retrieval cost, and drift. A cohesive answer may be substantial. Expect
many short leaves and fewer long ones, but never impose a distribution or file quota.
Splitting and consolidation both require judgment, not mechanical optimization.
Orientation and repository spine leaves deliberately aggregate coordinated truths;
do not thin them into catalogs or inflate them with unrelated archive material.

A new leaf gets `status: green` and `revised_at` automatically. `kt prove` records
the evaluated status and only lowers it; `kt_renew` (shell: `kt renew ADDRESS HASH`) records `checked_at` after manual review and is the way back up. Put substantive evidence and origin in the
answer body when they help establish the claim; the path supplies scope and a full
read supplies the revision hash. See `what/is/knowledge/leaf/metadata.md`.
Manual `checked_at` requires independent review of everything in the leaf.
When a leaf contains exclusively concrete facts and eligible proofs cover every
claim, mark it `verifiable: true` after reviewing that coverage.
If every declared proof runs and passes, `kt prove` clears
sticky falsification, and auto-greens the leaf. A missing, malformed, skipped, or
failing proof makes it brown. The flag asserts complete coverage; proof execution
cannot detect uncovered prose. An unresolved reusable question retains a blocker
and next check in its answer until the question is resolved. A green proof result
does not resolve an unanswered question.

Freshness may additionally use either `--expires-at` (ISO 8601 with timezone) or
`--expires-every` (for example `14d`, `2 weeks`, or `two weeks`, measured from
manual `checked_at`). An elapsed expiry makes the leaf yellow and unusable until
re-verification. Use expiry only when a real time-based freshness boundary exists.
Proof-free specifications, plans, procedures, opinions, and other content
that is not mechanically verifiable can be green. Prefer
expiries for factual answers liable to change.

## Narrowly eligible executable proofs

Add a proof for a single concrete true/false assertion whose truth a tiny local
read-only predicate can check immediately. Do not add proofs to commands,
requirements, policy, plans, history, opinions, bundled assertions, or non-trivial
conclusions. Split independent assertions only when that makes semantic sense;
otherwise use truthful provenance. The cadence is:

    The single mechanically verifiable assertion.

    Proof: (verified at _)

    ```bash
    the_read_only_predicate
    ```

The marker is a standalone paragraph between assertion and supported executable
fence. Bash, sh, Python, and Python3 are supported. An unmarked code block is an
instruction or example, not a proof. Predicates must be bounded, self-contained,
small enough to inspect at a glance, and return 0 exactly when the preceding
assertion is true. They must not write files, install, mutate services, launch
persistent processes, or have other externally visible side effects. Never use
`true` as a placeholder; prefer quiet `test` queries or a few direct assertions.

Inspect and run the predicate before relying on its assertion. An eligible
assertion without a marked proof, or a marker whose predicate is unsafe or tests
a different assertion, is a defect to repair within current authority before
reliance. A passing run
refreshes only its `Proof: (verified at …)` marker. A failing run changes it to
`Proof: (falsified at …)` and sets `status: brown`. The verifier cannot
decide semantic eligibility, faithful coverage, or whether all prose is proved;
the agent remains responsible. Read maintenance before repairing a falsified leaf.

For an existing owner, use `kt_rewrite` (or surgical `kt_edit`; shell: kt rewrite ADDRESS HASH BODY) as
described in
`how/to/rewrite/a/knowledge/leaf.md`; creation still refuses overwriting existing leaves.

Use canonical `does/` and `is/` branches for yes/no answers. The leaf path and
selected root supply scope; no scope field is written to front matter.
