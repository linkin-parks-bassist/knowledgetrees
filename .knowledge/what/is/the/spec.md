---
verified_at: '2026-09-12T20:16:19+10:00'
verified_by: codex /root
scope: knowledgetrees repository
source: user request in the active Codex session
verification: Reconciled all requested deliverables, installer-only skill creation, session-boundary bootstrap constraint, public-safety boundary, and publication gate.
review_when: Recheck when the requested contents or publication workflow changes.
---

The repository must be a local Git repository connected to its intended public
GitHub repository. It must contain:

- `README.md`, adapting `~/Downloads/knowledge_trees_pitch.html` into readable
  Markdown;
- the canonical `knowledgetrees` procedure in the visible example corpus;
- a distributable copy of the knowledge-tree proof verifier outside `.knowledge`;
- its own canonical `.knowledge` root;
- a visible `example/` corpus containing all global knowledge that pertains directly
  and only to knowledge trees, with an empty `example/where/am/i.md` that adopters
  are prompted to personalize; and
- useful leaves distilled from the Superpowers methodology, including how to make
  a plan, write a spec, update a spec, and when to ask for clarification.

The repository must provide a knowledge-first installer. It merges reusable leaves
without installing the example spine, preserves an existing orientation, installs
one verifier under the global knowledge root, asserts the bootstrap in the user's
`AGENTS.md`, and creates shared-harness and Codex `SKILL.md` entry points as hard
links to the installed `how/to/use/knowledgetrees.md`. The compatibility skill is a
bootstrap created by the installer for current harnesses, not a parallel knowledge
authority.
The compact bootstrap must carry the kt-first and miss-resolution mandate inline and link detailed
retrieval, capture, maintenance, and ingestion procedures. The installer must create hardlinked skills for those four
procedures, enabled in both Codex and OpenCode. A kt miss requires determining
whether a leaf exists; existing owners are read or amended, absent leaves are
investigated and added (or recorded unresolved). Established answers are captured
before the next unrelated tool call or completion. The bootstrap remains once per
fresh session; procedure skills are used when their task triggers apply. Real root orientations
must name branch purposes and actual entry routes. Installer OpenCode grants require
an informed `[n/Y]` gate before any writes, disclose reads and knowledge-tree writes,
and preserve unrelated configuration and the empty example orientation.
It is invoked once when a fresh agent session bootstraps, not once per user message,
turn, or task; a loaded session continues applying the procedure without rebooting.

The two trees have separate ownership. `.knowledge/` is the real operational root
for this repository. `example/` is the visible, distributable public specimen and
must not become a mirror of repository-specific plan or state.

The verifier timestamps individual proof outcomes using `Proof: (verified at …)`
or `Proof: (falsified at …)`. A failed proof falsifies the whole leaf via sticky
`falsified_at` metadata; only independent agent review may clear it. Passing all
proofs never changes leaf `verified_at` or establishes whole-leaf validation.
Keep legacy markers compatible, support read-only checking, preserve hardlinks,
and leave agentic knowledge repair outside the verifier's scope.

Every repository leaf must be suitable for public release: it must not name the
repository owner as an individual, expose home-directory identifiers, or include
personal or private knowledge. Imported global knowledge must therefore be curated
and sanitized rather than copied mechanically.

No first push may occur until the repository owner has reviewed the prepared contents and asks for
the push.
