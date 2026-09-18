---
status: "unverified"
scope: public knowledge-tree example
source: "tools/kt dictionary integration tests; owner stop-word and numeric filtering request, 2026-09-18"
review_when: Recheck when leaf path rules, root access, kt dict, or live discovery behavior changes.
updated_at: "2026-09-18T12:14:46+10:00"
---

A knowledge-tree dictionary is the sorted set of useful unique segments in the final two positions of Markdown leaf paths across selected accessible roots. `kt dict` removes `.md`, preserves meaningful hyphenated and mixed-alphanumeric identifiers, deduplicates globally, and prints one comma-separated line. It reads no leaf bodies and exposes no complete paths.

Dictionary filtering is intentionally stronger than lookup filtering. It omits segments of two characters or fewer, segments consisting only of digits, grammatical and navigation words, relational glue such as `about` and `from`, generic action/state words, and knowledge-tree container vocabulary such as `knowledge`, `tree`, `leaf`, `root`, `file`, and `directory`. Normal question lookup keeps its own smaller grammatical set so dictionary compression cannot reduce search recall.

With no arguments, `kt dict` includes every currently accessible root. Root labels or configured canonical paths restrict it, for example `kt dict local global`. Normal access and force-private rules apply, including registered restricted subtrees.

`kt init` prints the dictionary after the canonical procedure and exact local orientation. Membership only signals that a potentially informative segment occurs somewhere; it does not reveal a path, prove a leaf exists, or replace lookup, full reads, evidence review, and proof checks.

On the accessible roots measured when the stronger filter was added, output fell from 281 to 185 segments and from 2,811 to 1,991 bytes, a 34.2% segment reduction. Corpus-dependent counts can change as roots and leaf paths change.
