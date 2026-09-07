# Entity Research + Content Cluster Ruleset

## Purpose

Use this ruleset before individual page briefs or final content.

Goal: define the niche, validate entities, create the content map, prevent cannibalization, and establish internal linking architecture.

---

## Workflow

Source context + voice/tone + buyer persona, if available  
→ niche diagnosis  
→ SERP / PAA / fan-out review  
→ entity research  
→ intent clustering  
→ proposed content map  
→ internal linking architecture  
→ user confirmation  
→ individual page briefs using MIRENA Operating Rules

If inputs are missing, state what is missing and proceed only with labeled assumptions.

Do not begin page-level briefs or final content until the content map is approved.

---

## Required Inputs

Check for:

- Source context
- Voice/tone file
- Buyer persona file, if available
- Existing URL map/sitemap, if available
- Main niche, keyword, service, product, or topic
- Target location, language, or market, if relevant
- Business goals or priority offers, if available

If no URL map exists because the project is new, create a proposed content map.

---

## Source Context Rules

Use source context to define:

- What the brand does and sells
- Who it serves and does not serve
- What topics are in scope or out of scope
- What claims are allowed or forbidden
- Which services/products/offers matter most
- What makes the brand meaningfully different

Do not create clusters that contradict source context.

---

## Entity Research Rules

Identify:

- Core entities
- Supporting entities
- Buyer/problem entities
- Commercial entities
- Location entities, if relevant
- Trust/authority entities
- Entities to avoid

Validate important facts, claims, definitions, statistics, local details, product claims, legal/medical/financial claims, and technical claims.

Only turn an entity into a page opportunity if it has search intent, business relevance, and a clear role in the site structure.

---

## Intent and Cluster Rules

Group topics by intent and user journey, not just keyword similarity.

For each cluster, define:

- Cluster purpose
- Search intent
- Funnel stage
- Page opportunities
- Priority
- Internal link role

Use cluster types only when relevant:

- Core commercial pages
- Service/product/category pages
- Location pages
- Comparison pages
- Problem/solution pages
- Educational guides
- FAQ/support pages
- Trust pages
- Blog support articles

---

## Cannibalization Rules

Before proposing pages, define ownership.

Each proposed page must include:

- What it owns
- What it must not own
- Parent/child/sibling relationship
- Topics to mention briefly and route elsewhere

If two pages have the same primary intent, merge them or clearly separate them.

---

## Required Output 1: Entity Research Summary

Include:

- Niche definition
- Core entities
- Supporting entities
- Buyer/problem entities
- Commercial entities
- Trust/authority entities
- Entities to avoid
- Strategic interpretation

---

## Required Output 2: Cluster Map

| Cluster | Purpose | Page opportunities | Intent | Priority |
|---|---|---|---|---|

---

## Required Output 3: Proposed Content Map

| Page name | URL | Page type | Primary intent | Secondary intent | Core entities | Owns | Must not own | Parent/child relationship | Priority |
|---|---|---|---|---|---|---|---|---|---|

---

## Required Output 4: Internal Link Architecture

| Source page | Target page | Link role | Purpose |
|---|---|---|---|

Define hub, spoke, sibling, support, and conversion paths.

---

## Required Output 5: Content Exclusions

List topics that should not be targeted because they are:

- Outside scope
- Poor-fit traffic
- Risky
- Better suited to another page/site/brand
- Likely to confuse topical authority

---

## Required Output 6: Next-Step Recommendation

End with:

- Which cluster to build first
- Which page to brief first
- Which pages need SERP data before briefing
- Which missing inputs would improve accuracy
- Which risks need confirmation

---

## Document Usage Check

| Document | Used? | What it controlled |
|---|---:|---|
| Source context | Yes/No | Facts, offers, claims, exclusions, topical boundaries |
| Voice/tone file | Yes/No | Style implications for future content |
| Buyer persona file | Yes/No | Audience, objections, pain points, decision triggers |
| Existing URL map / sitemap | Yes/No | Internal linking, cannibalization, existing page ownership |
| SERP data + PAAs + fan-outs | Yes/No | Intent, clusters, page opportunities, query coverage |

Do not claim a document was used unless it visibly influenced the research or content map.

---

## Acceptance Check

The output must pass:

- Niche is clearly defined
- Source context is followed
- Core entities are covered
- Clusters are intent-based
- Proposed pages have clear ownership
- Cannibalization is controlled
- Internal linking architecture is included
- Priority pages support business goals
- No unsupported or risky claims are introduced
- Next step is clear

---

## Engine session hooks (added for the engine — the rules above are unchanged)

- One dedicated chat per project. Approvals arrive only as SYNC messages;
  treat repo canonical state as authoritative over chat memory. QC-rejected or
  premature outputs are VOID DRAFTS — never reference or build on them.
- Every artifact you produce starts with the exact frontmatter block given in
  the job packet (project_id, stage, version, status: proposed, niche,
  location, created, job_id, attempt) and is delivered as ONE artifact in ONE
  code block with nothing after it.
- Revision packets list exact numbered failures: fix only those, change
  nothing else, maximum three attempts.
