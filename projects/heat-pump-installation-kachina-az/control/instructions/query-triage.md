# query_triage — stage contract (PAA + fan-out assessment)

Purpose: turn raw collected queries (PAA scrapes = observed demand; ChatGPT /
Gemini fan-outs = synthetic expansion) into per-page coverage obligations —
BEFORE the brief. Assess every query against this page's intent, its owns /
must_not_own territory, and the whole-site ownership ledger.

Input: the page record, the raw query files inlined in the packet, the
approved entity research, and the ownership ledger (if present).

Output: one markdown artifact with the packet's frontmatter containing exactly
one table, one row per unique collected query:

| query | source | verdict | destination/note |
|---|---|---|---|

- source: paa | fanout-chatgpt | fanout-gemini | serp | related-search | manual
- verdict: include_in_section | include_in_faq | mention_briefly |
  link_elsewhere | exclude | separate_page_idea | answer_with_correction
- destination/note: for link_elsewhere = the owning PAGE ID from the approved
  URL map; for separate_page_idea = one-line page idea; for
  answer_with_correction = the correct fact to state (use for queries whose
  naive answer would violate claims-compliance, e.g. expired incentives);
  otherwise the section/FAQ placement.

Rules: weight PAA (observed) above fan-outs (synthetic) when they conflict;
kill noise rows (truncation artifacts, off-market, wrong-location) as exclude
with the reason; a query owned by another page per the ledger is ALWAYS
link_elsewhere; duplicates collapse to one row. After the table: a short
"Ledger updates" list (query → this page) for every include verdict.

Acceptance: every unique input query has exactly one row; no verdict outside
the set; no include verdict for a query the ledger assigns elsewhere.

## Project-tested additions (optional)
