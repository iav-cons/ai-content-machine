# brief — stage contract (the execution contract for one page)

Method: MIRENA Operating Rules §1–§3 govern the brief's craft. This contract
fixes inputs, boundaries, and acceptance.

Input truth: the page record (owns / must_not_own is law), the approved
query-triage artifact for this page (its include/mention verdicts are the
page's coverage OBLIGATIONS; its link_elsewhere verdicts are routing
obligations), the approved entity research, the SERP/data files inlined, the
audience file, and voice-tone.

Output: one markdown artifact with the packet's frontmatter, containing every
element the Operating Rules §3 require (page type → document usage check),
with these engine additions:
- The "Selected PAAs and fan-outs" section MUST account for every include /
  mention / answer_with_correction row of the triage artifact — none dropped,
  none added from outside it.
- answer_with_correction rows: the brief states the correct fact to write and
  cites the claims-compliance rule it protects.
- Internal link plan may target only page IDs that exist in the approved URL
  map, honoring link_elsewhere verdicts.
- Section plan stays inside `owns`; anything from `must_not_own` appears only
  as a routed mention.
- For location pages: a "Local differentiation" section listing the confirmed
  local facts this page is built on ([REQUIRES CONFIRMATION] if absent — the
  brief then stops and says the page is not ready).

Acceptance: MIRENA Operating Rules acceptance check + every triage obligation
mapped to a section or FAQ + zero claims-compliance conflicts + Document Usage
Check honest.

## Project-tested additions (optional)
