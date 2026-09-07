---
project_id: "{{PROJECT_ID}}"
stage: control
niche: "{{NICHE}}"
location: "{{LOCATION}}"
---
# Quality Checklist — {{PROJECT_NAME}}

Used by qualitative QC (AI reviewer and/or human — spec §12). The reviewer answers
each question with PASS/FAIL + a one-line reason. Any FAIL puts the artifact into
the revision loop (spec §13). Extend this list with your own tested criteria.

## All artifacts
- Correct project, niche ({{NICHE}}), and location ({{LOCATION}}) throughout?
- Consistent with project-brief.md and operating-rules.md?
- No contradictions with the approved canonical inputs listed in the packet?

## Truth & provenance (all artifacts)
- Any business facts, claims, credentials, offers, pricing, guarantees, or
  results that are NOT supported by the sources? (invented facts = FAIL)
- Any assumptions presented as facts instead of labeled [ASSUMPTION]?
- Any sources claimed as used without visibly influencing the output?
- Any architecture or claims copied from competitors without evaluation?
- Anything that violates control/claims-compliance.md (when present)?

## Entity research
- Is entity coverage sufficient for the niche?
- Is the central entity correctly identified?
- Are attributes/relationships plausible and useful for planning?

## Content cluster
- Is search intent correct for each proposed page?
- Any duplicate or redundant pages?
- Could any pages cannibalize each other?
- Any missing pages an expert would expect? Any unsupported pages?
- Are page-vs-section decisions right? Commercial/informational balance right? Hierarchy sound?
- Does every proposed page have a justified semantic role (method / diagnostic /
  problem / symptom / escalation / geographic / audience adjacency)?
- Any page justified only by search volume, without a legitimate relationship to
  the central entity, a real offer, and the buyer's decision process?
- Does every important entity/query have exactly ONE owning page (primary entity
  → primary intent → owning URL → supporting URLs)?

## Content brief
- Is the brief strategically good — would a skilled writer produce the right page from it?
- Does it target the primary query and intent from the approved URL map record?
- Does it respect sibling pages (no overlap with their primary queries)?

## Content
- Is the content actually useful to the target customer?
- Does it follow the approved brief — staying inside its semantic territory,
  without reintroducing entities or intents the architecture excluded?
- Correct intent, no drift into sibling pages' territory?
- Do internal links follow semantic relationships (parent→child, service→method,
  problem→solution, symptom→diagnosis, service→cost/location) rather than
  keyword overlap?
