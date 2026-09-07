# page_review — stage contract (performance feedback loop)

Input: the approved live content, its brief, the page record, and every file
in pages/<PAGE_ID>/performance/ (GSC exports, ranking data).

Task: diagnose the gap between what the page was built to own and what it is
actually winning. Compare query-level performance against the triage
obligations and the brief's targets.

Output: one markdown artifact with the packet's frontmatter:
1. Performance summary (impressions/clicks/position by query group)
2. Diagnosis (coverage gap / intent mismatch / cannibalization / SERP-feature
   loss / freshness — with evidence)
3. Numbered revision requirements — exact, minimal, each tied to evidence
   (these become the failure list for a content revision job, spec §13)
4. Keep-list: what must NOT change
5. Ledger/triage updates if new queries surfaced in GSC

Acceptance: every requirement is actionable and evidence-backed; no rewrite-
everything recommendations; nothing that violates owns/must_not_own.

## Project-tested additions (optional)
