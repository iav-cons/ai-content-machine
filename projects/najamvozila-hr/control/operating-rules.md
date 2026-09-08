---
project_id: "najamvozila-hr"
stage: control
niche: "Najam Vozila"
location: "Hrvatska"
---
# Operating Rules — Najam Vozila

Every worker job inherits these rules (spec §4, §10, §23). They are included in
every job packet. Add project-specific rules below the core set.

## Core guardrails (spec §23 — do not remove)

1. Never skip required stages.
2. Never treat AI output as approved automatically.
3. Never overwrite an approved artifact silently.
4. Never use newest when approved canonical is required.
5. Never mix projects. This job belongs to project_id najamvozila-hr only.
6. Never ignore a material source mismatch — stop and report it.
7. Never control workflow state — perform the one job in the packet, nothing else.
8. Never rely on conversation memory — the packet contains everything needed.
9. Never loop revisions beyond what the packet instructs.
10. Never delete change-log history.
11. Never include API keys or secrets in any output.
12. Never build on unapproved strategic inputs — use only the inputs in the packet.
13. Never regenerate work the packet did not ask for.
14. Always produce the single output file named in the packet, in the required format.
15. Always keep niche = Najam Vozila and location = Hrvatska — if any input
    contradicts this, STOP and report the mismatch instead of improvising.

16. Never invent business facts, claims, credentials, offers, locations,
    pricing, guarantees, or results. Missing information becomes a clearly
    labeled assumption, never a stated fact.
17. Use the truth ladder explicitly: confirmed fact (stated plainly) →
    [ASSUMPTION] (labeled inline) → [REQUIRES CONFIRMATION] (unresolved).
    Nothing carrying an unresolved marker can be approved — hard QC blocks it.
18. Never claim a source document was used unless it visibly influenced the
    output. If required information was missing, say so.
19. Layer hierarchy: sources = truth, research = understanding, architecture =
    allocation, brief = specification, persona/NLP/style = expression only.
    Expression never manufactures truth; SEO value never overrides facts,
    topical relevance, or compliance.
20. Competitors are evidence, not authority: benchmark → evaluate →
    retain/reject/improve. Never copy architecture or claims because a
    competitor ranks. Matching the SERP is baseline; the page must add
    justified value beyond it.
21. "Continue", "next", "go ahead" or similar is never permission to advance
    stages — only a job packet authorizes work.
22. On conflicting instructions: follow the AUTHORITY ORDER stated in the
    packet (global rules → project truth → approved canonicals → stage
    instructions), flag the conflict explicitly, and involve the human when a
    real project decision is needed.

## Project-specific rules

