# url_map — stage contract

Input truth: the approved canonical content cluster. Ownership is decided HERE.

Produce url-map-vN.yml as ONE yaml document, exactly this schema (hard QC
validates it):

```yaml
meta:
  project_id: <id>
  stage: url_map
  version: <N>
  status: proposed
  niche: <niche>
  location: <location>
  created: YYYY-MM-DD
pages:
  - id: COM-001            # stable, unique, CLUSTER-PREFIXED
    cluster: Core Commercial
    name: Heat Pump Installation
    url: /heat-pump-installation   # leading slash, lowercase-hyphen segments
    type: service          # homepage|service|commercial|conversion|location|
                           # support|educational|comparison|informational|trust|faq
    primary_intent: Installation service
    secondary_intent: Contractor selection
    core_entities: [heat pump installation, Manual J]
    owns: Installation process, assessment, proposal
    must_not_own: Cost, rebates, replacement urgency
    parent: HOME-001       # existing id, or null for root
    priority: P1           # P0|P1|P2|P3
    status: not_started
```

Rules: every important entity/intent has exactly ONE owning page; `owns` and
`must_not_own` are mandatory and specific; location pages only where genuinely
local content is possible (no name-swap pages); hierarchy is hub-and-spoke
with parents that exist; no cycles.

Acceptance: no duplicate ids/urls; no two pages with the same primary_intent +
owns territory; every cluster from the approved cluster artifact is either
represented or explicitly excluded with a reason in a trailing comment block.

## Project-tested additions (optional)
