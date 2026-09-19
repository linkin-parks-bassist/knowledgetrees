---
status: green
revised_at: "2026-09-18T13:14:39+10:00"
---

A knowledge tree is an authoritative, semantically structured knowledge substrate.
Directory choices progressively narrow natural-language questions; Markdown leaves
directly answer them. It is persistent memory and the primary agent retrieval
interface for its scope, not a catalog or link farm over human-oriented monoliths.

Knowledge trees must hold knowledge at every scale. There is no minimum level of
abstraction or importance: very fine-grained implementation knowledge belongs in
the tree just as much as architecture, design decisions, plans, and specifications.
This includes what function `f` does and why, its inputs, outputs, ownership,
side effects and invariants; what file `z` contains; where typedef `y` is declared;
include order and dependency constraints; repository folders and their roles;
and information normally expressed in code comments. Capture these direct answers
in the owning project or subsystem tree. Do not omit them because they are small,
obvious, discoverable in source, or below the level of a design document.

Source code remains primary evidence for implemented behavior. A leaf contains the
checked answer and rationale, with source locations and review conditions for drift;
a filename or instruction to read the code alone does not capture the knowledge.
Existing comments need not be deleted to establish this coverage. The same tree
also holds broad architecture shape and cohesive specs; retrieval chooses the scale
needed by the question.

Context is working memory, not storage. Retrieve the smallest answer that resolves
the current question, then stop. Any directory can have a local root; nearest scope
filters irrelevant knowledge before semantic descent narrows the question. Broader
roots supply shared facts while local roots own refinements. Governing instructions
remain authoritative; knowledge of policy cannot silently weaken them.

Leaves are semantically focused, not uniformly tiny. Cohesive answers may be long
when their parts are normally needed together. Boundaries require judgment about
relation, discovery paths, joint use, ownership, lifecycle, volatility, and retrieval
cost. Many short and fewer long answers are expected, but sizing and file count are
heuristics, not quotas or automatic splitting/consolidation triggers. Orientation
and repository spines deliberately aggregate coordinated truths.

The hard obligations are direct answers, incremental semantic retrieval, clear
canonical scope ownership, sentence-derived paths with hyphens rather than
underscores in multi-word components, immediate reusable capture, truthful
provenance, portable project knowledge, and verified coverage before authorized
retirement of redundant sources. Documents and task bundles may be external
authorities, primary evidence, temporary ingestion sources, or presentations; they
are not competing internal knowledge stores.

Executable proofs connect eligible atomic factual claims to reality. Their passing
timestamps do not verify unproved prose. Any failed proof falsifies its leaf; all
proofs passing is necessary but not sufficient unless a reviewed `verifiable: true`
declaration asserts that every claim is covered. Independent review and explicit
repair remain agent responsibilities for unflagged leaves and proof coverage.

Every leaf is green, yellow, or brown. Green is the default, including for specs,
plans, procedures, opinions, and other content that is not actually verifiable;
it also requires no active falsification or failing proof. Yellow is explicitly
marked or has passed an optional `expires_at` or
`expires_every` boundary and cannot be used until re-verification. Brown is actually
falsified or proof-failing; it makes the tree busted and must be diagnosed and repaired.
Agents should optionally add expiries to factual knowledge liable to change.

The installed skill-shaped entry point is compatibility bootstrap into this
substrate, not a precedent for proliferating separately maintained skill documents.
