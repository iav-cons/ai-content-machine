---
project_id: "heat-pump-installation-kachina-az"
stage: query_triage
page_id: TRUST-002
version: 1
status: approved
niche: "Heat Pump Installation"
location: "Kachina Village, AZ"
created: 2026-09-07
job_id: JOB-20260907-130219-query_triage
attempt: 3
---

# Query Triage — TRUST-002

Current stage: query_triage  
Previous completed stage: URL/content map (with entity research and content cluster approved)  
Next allowed stage after approval: page brief  
Request status: allowed by revision packet, attempt 3

| query | source | verdict | destination/note |
|---|---|---|---|
| 800 feet? | fanout-chatgpt | exclude | Truncation artifact; no recoverable intent. Duplicate also appeared in fanout-gemini. |
| How do heat pumps perform at 6 | fanout-chatgpt | exclude | Truncation artifact; incomplete altitude-performance query and not usable as collected. Duplicate also appeared in fanout-gemini. |
| Can I get a load calculation for my home? | fanout-chatgpt | link_elsewhere | TECH-004 |
| What are the benefits of heat pumps in high altitudes? | fanout-chatgpt | link_elsewhere | TECH-001 |
| How do I find a licensed contractor in Coconino County? | fanout-chatgpt | link_elsewhere | TRUST-001 |
| What should I expect in terms of installation costs for a heat pump? | fanout-chatgpt | link_elsewhere | COST-001 |
| What permits are required for installing a heat pump in Coconino County? | fanout-chatgpt | include_in_section | Core section: which Coconino County permit/inspection path applies to residential heat pump installation in Kachina Village. Keep licensing separate. Confirm current permit details against Coconino County before publication. Duplicate also appeared in fanout-gemini. |
| What are the common issues with heat pumps in cold climates? | fanout-chatgpt | link_elsewhere | FAQ-004 |
| How do I compare propane heating costs to electric heating costs? | fanout-chatgpt | link_elsewhere | COST-003 |
| Are there incentives for switching to a heat pump in Arizona? | fanout-chatgpt | link_elsewhere | COST-004 |
| What should I know about upgrading my electrical panel for a heat pump installation? | fanout-chatgpt | link_elsewhere | COST-006 |

## Ledger updates

- What permits are required for installing a heat pump in Coconino County? → TRUST-002
