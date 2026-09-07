# AI Content Production Engine — System Overview v2

Date: 2026-08-12. Supersedes the v1 overview (kept verbatim in `docs/workflow-spec.md`).
This version incorporates: the tool assignment as actually built (GitHub-based), the
MIRENA global-rules integration, the query-intelligence (PAA / fan-out) layer, the
location-differentiation guardrail, the automation roadmap, and implementation status.
The goal is unchanged: stable, reliable, consistently high-quality content — with a
human approving every strategic decision.

---

## 1. What we're building

A controlled AI Content Production Engine. Not an article generator — a persistent
system that runs the tested multi-step workflow with enforced gates.

```
                    ┌────────────────────────┐
                    │         HUMAN          │
                    │  approvals = PR merges │
                    │  exceptions, decisions │
                    └───────────┬────────────┘
                                │
                                ▼
        ┌─────────────────────────────────────────────┐
        │                GITHUB REPO                  │
        │  files + versions (canonical on main)       │
        │  state: project.yml, issues + status labels │
        │  global rules, control files, artifacts     │
        └───────────┬─────────────────────┬───────────┘
                    │                     │
                    ▼                     ▼
        ┌───────────────────┐   ┌──────────────────────┐
        │  GITHUB ACTIONS   │   │     MAKE (thin glue) │
        │  hard QC, packets │   │  notifications,      │
        │  status board,    │   │  WordPress publish   │
        │  publish payloads │   │  (no logic lives     │
        │  qualitative QC   │   │   here)              │
        └────────┬──────────┘   └──────────────────────┘
                 │
                 ▼
        ┌─────────────────────────────────────────────┐
        │                 WORKERS                     │
        │  MIRENA via manual bridge — ALL production  │
        │  stages: entity research, cluster, URL map, │
        │  briefs, content (fresh chat, Memory off)   │
        │  CLAUDE — qualitative QC reviewer           │
        │  HUMAN — niche research, source context,    │
        │  SERP research, PAA + fan-out data          │
        └─────────────────────────────────────────────┘
```

GitHub stores and versions everything and holds the state. Actions run the
deterministic machinery. Make is notification and publish glue only. Workers —
MIRENA, Claude, or the human — perform single jobs: AI workers receive packets,
human-performed steps enter as dated, provenance-labeled files via PR, subject
to the same QC. The human approves by merging.

**Worker assignment (confirmed):**

| Step | Performed by |
|---|---|
| Initial niche research + source context | Human, manually, before the workflow starts |
| Project setup / control files | Human (persona system: Persona → ICP → Rulebook → Humanization) |
| Entity research | MIRENA (manual bridge) |
| Content cluster | MIRENA (manual bridge) |
| URL map | MIRENA (manual bridge) |
| SERP research / brief intelligence | Human — provided as a file |
| PAA scraping + fan-out queries | Human — provided as files (QueryFan export etc.) |
| Page brief | MIRENA (manual bridge) |
| Content generation + revisions | MIRENA (manual bridge) |
| Hard QC | Engine scripts via Actions |
| Qualitative QC | Claude review workflow + human |
| Approvals | Human only (PR merges) |
| Publish | Actions → Make → WordPress |
| Performance page review | To assign (Claude or MIRENA) |

Session model: every MIRENA stage runs inside the project's one dedicated
chat (bootstrap → slim packets → SYNC on approvals — §13 and
docs/mirena-session-protocol.md). Day-to-day operation:
docs/operator-runbook.md.

---

## 2. Phase 1 — Project Strategy & Setup

PROJECT INITIALIZATION → SOURCE VALIDATION → CONTROL FILES → ENTITY RESEARCH → QC
→ HUMAN APPROVAL → CONTENT CLUSTER → QC → HUMAN APPROVAL → URL MAP → QC
→ HUMAN APPROVAL → PHASE 1 COMPLETE

Stages cannot be skipped or merged. "Continue / next / go ahead" is never
permission — only a job packet authorizes work, and only a merge advances state.
Anything generated too early is a non-approved draft; the workflow returns to the
proper stage.

---

## 3. Source validation

Before any AI strategy work: correct project, niche, location, domain; required
files present; no contradictory instructions; no remnants from another project
(contamination terms are scanned on every PR); no obvious factual conflicts.
The checklist in `control/source-context.md` physically blocks packet generation
until completed.

---

## 4. Control files and authority

Two layers.

**Global rules (highest authority, all projects):**
`engine/rules/entity-content-cluster-ruleset.md` and
`engine/rules/mirena-operating-rules.md` — inlined first into every packet,
changed only via PR, never overridden by project files or chat instructions.

**Per-project control files:** project-brief, source-context, operating-rules
(core guardrails + truth ladder), quality-checklist, change-log (append-only),
persona/ICP + voice-tone, claims-compliance (never-claim list, verify-always
list), project-state.md (continuity dashboard: active decisions, internal-linking
notes, cannibalization notes, open questions — inlined into every packet so page
30 inherits page 3).

**Authority order, stated in every packet:** global rules → confirmed project
truth → approved canonical artifacts → stage instructions. Conflicts are flagged,
never silently resolved.

**Truth ladder:** confirmed fact → `[ASSUMPTION]` (labeled) →
`[REQUIRES CONFIRMATION]` (unresolved). Nothing carrying an unresolved marker can
be approved — hard QC blocks it. No invented business facts, claims, credentials,
offers, locations, pricing, guarantees, or results. Ever.

---

## 5. Entity research

Packet = global rules + project truth + entity-research instructions →
entity-research artifact (central entity, primary/secondary/supporting entities,
attributes, relationships, adjacencies, entities to avoid). Hard QC → qualitative
QC → human approval → canonical.

Entities determine coverage. Relationships determine structure. Salience
determines prominence. This layer decides what deserves to exist before anything
is written.

---

## 6. Content cluster

Only approved entity research feeds this stage. Clusters are grouped by intent
and user journey, not keyword similarity. Every proposed page needs a justified
semantic role (method / diagnostic / problem / symptom / escalation / geographic /
audience adjacency). Search volume alone is never topical permission.
QC → approval → canonical.

---

## 7. URL map

Approved cluster in → structured page records out: ID, name, URL, page type,
primary query/intent, secondary intent, core entities, **owns / must not own**,
parent, priority, status. Ownership is defined here: every important entity and
intent gets exactly one owning page, with supporting pages routed to it.
Hard QC validates the schema: duplicate URLs/IDs, malformed slugs, broken
hierarchy, orphans, duplicate primary intents (cannibalization). Human approval
completes Phase 1 and becomes the production plan.

---

## 8. Query intelligence layer (PAA / fan-out assessment)

Collected queries — Google PAA scrapes (observed demand) and Gemini/ChatGPT
fan-outs (synthetic expansion) — are inputs, not content. They pass through a
controlled triage before any brief uses them:

1. **Data drops with provenance.** Every scrape lands in the page's data folder
   labeled with source and date. Unlabeled or undated data is not accepted into
   briefs; staleness limits apply (SERP-class data decays fastest).
2. **Triage artifact.** A dedicated structured artifact assigns every query
   exactly one verdict against the page's intent and goal:
   include in section / include in FAQ / mention briefly / internally link
   elsewhere / exclude / separate page idea.
3. **Deterministic checks.** Every collected query has exactly one verdict;
   every "link elsewhere" target exists in the approved URL map; "separate page
   idea" verdicts land in a backlog file instead of evaporating.
4. **Query ownership ledger.** A project-level ledger enforces one question, one
   owner — the same PAA cannot be answered on two pages (FAQ-level
   cannibalization is caught, not just primary-query overlap).
5. Judgment (is the verdict right?) stays with qualitative QC and the human;
   completeness and ownership are machine-enforced.

---

## 9. Location differentiation (sibling-page guardrail)

Two location pages — "bravar Zagreb" and "bravar Karlovac" — must differ in
substance, not just the place name. Enforced at three layers:

1. **Input gate — no local facts, no page.** A location page cannot be briefed
   until location-specific truth exists for it: confirmed local facts (housing
   stock, districts, access, pricing context, regulations), its own PAA/SERP
   data, and its own "owns" definition. Differentiation must come from confirmed
   local truth — never from invented local color, which would violate the
   no-invented-facts rule and is worse than duplication.
2. **Deterministic check — masked similarity.** On every location-page PR, the
   location tokens are masked in the new page and its approved siblings and the
   bodies are compared. Above-threshold similarity fails hard QC with the
   overlapping sections named: a literal "same except the city" detector.
   Applies within a project, and — as a deliberate exception to project
   isolation — as an opt-in check across same-niche projects, because
   near-duplicate sites in one niche are both a quality failure and a doorway
   risk.
3. **Generation-time lever.** Location-page packets inline the approved sibling
   pages (or their owns-lists) as negative examples: here is what already
   exists; differ from it. Qualitative QC answers directly: meaningful
   difference, or a city swap?

Consequence, accepted deliberately: location pages have an entry requirement and
are slower per page — which is exactly why they rank instead of getting filtered.

---

## 10. Phase 2 — Production queue

The approved URL map becomes the plan. One GitHub issue per page; status labels
carry the spec statuses (not_started → researching → research_complete →
brief_pending → brief_qc → awaiting_approval → approved → drafting → draft_qc →
revision → complete); priorities P0–P3 ordered on a Projects board. Workflow
state exists entirely outside any chat.

---

## 11. Page production workflow

PAGE SELECTED → ENTITY CONTEXT → SERP RESEARCH (human-provided file)
→ PAA / FAN-OUT TRIAGE (§8 — data human-provided)
→ COMPETITOR / INTENT ANALYSIS → CONTENT BRIEF (execution contract; for location
pages: differentiation inputs per §9) → QC → APPROVAL → CONTENT GENERATION
(inside persona / voice / compliance rails) → QC → REVISION IF NEEDED
→ FINAL CONTENT → SAVE + VERSION → QA + PROJECT-STATE UPDATE

The brief defines the page's semantic territory; drafting may not expand beyond
it. Competitor data is evidence (benchmark → evaluate → retain/reject/improve),
never authority. Internal links follow semantic relationships, not keyword
overlap.

---

## 12. AI is a worker, not the controller

Every job is a self-contained packet generated by script from canonical `main` —
never assembled by hand, never from chat memory. The packet carries: job ID,
project identity, stage, attempt, task, authority order, DO-NOT list, golden
example when present, full inlined inputs. One job in, one artifact out.
The system decides what happens next; the worker never does.

---

## 13. Manual worker bridge + canary

The subscribed Custom GPT has no API, and it performs every production stage
(entity research → content), so this bridge is the system's critical path and
throughput ceiling. **Session model — one chat per project:** each project
gets one dedicated MIRENA chat for its whole life (Memory off). The chat is
bootstrapped once with the session rules, both global rulesets, all control
files, and current canonical state; jobs then arrive as slim packets; every
approval or correction is announced into the chat as a SYNC message; the repo
wins any disagreement, and QC-rejected or premature outputs are void drafts.
When a long project outgrows the context window, a fresh bootstrap generated
from current main starts a new chat with nothing lost (rotation). Full
procedure: docs/mirena-session-protocol.md. **Verification preamble (every
chat, including rotations):**
each job runs in a fresh chat, so each chat starts by verifying the
subscription — the operator sends the payment email alone, waits for the
"subscription is verified" confirmation, then pastes the packet as the next
message. Done manually, always in that fixed order, so the pre-packet context
is identical across every run. The email is a credential: it never enters
packets, issues, the repo, or the canary file, and result-copying starts at the
artifact's opening frontmatter so the verification exchange is never committed.
The bridge per job: slim packet posted to the page's issue →
`awaiting_manual_worker` → paste into the project chat → result returned as a
branch + PR → normal QC → SYNC on approval. A frozen monthly canary packet plus
a structural diff script detects silent vendor updates — the one variance source
that cannot be pinned is made visible instead.

---

## 14. Hard QC vs qualitative QC

**Hard QC (deterministic, every PR, merge-blocking):** required files and
frontmatter; project/niche/location identity; versioned filenames; URL-map
schema (duplicates, slugs, hierarchy, orphans, intents); required headings per
stage; contamination scan (other projects' terms); protected canonical files
immutable; change log append-only; stage-order gates; approval-PR coherence;
attempt cap; secrets scan; staleness of research inputs; unresolved
`[REQUIRES CONFIRMATION]` markers block approval; **never-claim and
banned-phrase scanning from claims-compliance and voice files; masked
location-similarity (§9); query-triage completeness and ownership (§8).**

**Qualitative QC (judgment):** Claude reviews the PR against the project's
quality checklist — intent correctness, entity coverage, redundancy,
cannibalization risk, brief adherence, truthfulness of differentiation, actual
usefulness — and posts PASS/FAIL with an exact numbered failure list. It never
approves and never edits. The human is the only approval.

---

## 15. Revision loop

Failure ≠ rewrite. Revision packet = original instructions + previous output +
exact numbered failures + fix-only-these correction rule. Maximum 3 attempts,
then `human_review_required` and the system stops. Failure lists are
machine-readable so revision packets can be generated automatically.

---

## 16. Approval gates are absolute

QC pass is never approval. An approval is one atomic PR merge containing: the
artifact marked approved + the canonical pointer + the status flip + the
change-log line — a shape hard QC enforces. Nothing downstream reads anything
that isn't canonical on `main`.

---

## 17. Approved files are protected

Canonical files are immutable. Change = proposed vN+1 with a stated reason →
QC → human approval. vN stays authoritative until the merge.

## 18. Canonical vs latest

Newest never means authoritative. Downstream work consumes only the approved
canonical version — enforced by the packet generator, which reads only the
canonical map.

## 19. Change log

Append-only, per project. Every approval and material decision gets a line.
Hard QC blocks any edit to existing lines. AI may add history; it may never
erase it.

## 20. Project isolation

Every artifact, job, page, QC run, approval, and change belongs to one
project_id, checked throughout: folder/frontmatter identity, cross-project
contamination scanning, self-contained packets. One deliberate, opt-in
exception: same-niche cross-project similarity comparison (§9), because
isolation must not hide near-duplicate sites.

## 21. State machine guardrail

Recorded state controls progression. Entity research not approved → no cluster.
Cluster not approved → no URL map. URL map not approved → no page production.
No approved brief → no content. No approved content → no page review. The packet
generator refuses forbidden jobs; hard QC fails artifacts whose prerequisites
aren't approved on `main`.

---

## 22. State layer

`project.yml` per project (stage statuses + canonical map — machine truth),
GitHub issues + labels (page queue), `control/project-state.md` (human truth:
decisions, linking notes, cannibalization notes, open questions), the
append-only change log, and a daily STATUS BOARD issue: every project's stages,
the queue by status, and stalls (manual work waiting ≥ 7 days, anything in human
review). The system answers: what exists, what's approved, what's waiting, what
failed, what's next — months later, with zero chat dependency.

## 23. File layer

```
engine/rules/                    global rulesets (highest authority)
engine/qc-config.yml             editable QC rules (headings, limits, staleness)
engine/scripts/                  packets, hard QC, status, publish, canary
engine/templates/                project + packet templates
benchmarks/                      frozen canary packet + monthly worker outputs
projects/<project-id>/
  control/  (instructions/, golden/)  sources/  research/  cluster/  url-map/
  briefs/<PAGE>/  content/<PAGE>/  pages/<PAGE>/ (+ performance/)  qc/  jobs/
```

---

## 24. Orchestration and automation

**Running now (GitHub Actions):** hard QC on every PR; qualitative QC on label;
packet generation from the Actions tab (posted to issues for the manual bridge);
daily status board; publish payloads on canonical-content merges. Make: stall
notifications and the WordPress publish call. No logic lives in Make.

**Automation roadmap (planned, in build order):**
1. Claims / banned-phrase / never-claim scanning wired into hard QC.
2. Query triage artifact + ownership ledger (§8) with completeness checks.
3. Required headings encoded from the tested rulesets; golden examples seeded;
   URL-map schema aligned to the real map format (owns / must-not-own columns).
4. Bridge ergonomics — since MIRENA performs all production stages, automation
   centers on the bridge rather than replacing it: packet-to-issue on one click
   (built), auto-generated revision packets on QC failure posted to the issue,
   stall alerts. An API worker-runner stays on the shelf for any stage later
   reassigned to Claude/ChatGPT — and becomes the instant unlock if the vendor
   ever licenses API access.
5. Auto-revision packets: QC failure → the exact-failure revision packet is
   generated and posted automatically; API-run jobs could run attempts 2–3
   unattended, MIRENA jobs await the paste.
6. Auto-creation of page issues on URL-map approval.
7. One pilot page end-to-end before volume, so recurring failures get encoded
   into config first.

Human approvals are never automated. That is the design, not a limitation.

---

## 25. Post-publication loop

Publishing is a stage, not an exit. Merged canonical content → publish payload →
WordPress (draft first) → publish event recorded on the page's issue → live URL
logged. Monthly performance exports (GSC etc.) drop into the page's performance
folder → `page_review` packet (gated on approved live content) → numbered
findings → normal content revision through the same machinery. Underperformance
becomes a data-driven revision job with full traceability from SERP data to
brief version to published change.

---

## 26. Consistency levers

Identical inputs: packets always script-generated from canonical `main`.
Pinned dated models for API workers; fresh chat + Memory off protocol for the
manual worker; monthly canary against drift. Golden examples inlined per stage.
Required headings enforced once tested structures stabilize. Staleness limits on
research data. Every prompt and rule versioned — any quality shift is traceable
to a specific diff, and every fix compounds forward.

---

## 27. Core guardrails

1. Never skip required stages.
2. Never treat AI output as approved automatically.
3. Never overwrite an approved artifact silently.
4. Never use newest when approved canonical is required.
5. Never mix projects.
6. Never ignore a material source mismatch.
7. Never let AI control workflow state directly.
8. Never let conversation memory become project state.
9. Never allow infinite revision loops.
10. Never delete change-log history.
11. Never expose API keys/secrets in blueprints or GitHub.
12. Never make downstream work from unapproved strategic inputs.
13. Never regenerate unaffected work unnecessarily.
14. Every important artifact is versioned and attributable.
15. Every important workflow transition is recorded.
16. Never invent business facts, claims, credentials, offers, locations,
    pricing, guarantees, or results — the truth ladder is mandatory and
    unresolved markers block approval.
17. Never publish sibling/location pages that differ only by the place name —
    masked-content similarity is checked within a project and, opt-in, across
    same-niche projects.
18. Never brief a location page before confirmed location-specific truth exists
    for it — and never substitute invented local color for real differentiation.
19. Every collected query (PAA / fan-out) receives exactly one triage verdict
    and exactly one owning page.
20. Never feed unlabeled or undated research data into a brief — provenance and
    freshness are enforced.
21. Never state what the compliance file forbids — the never-claim and
    banned-phrase lists are machine-scanned on every artifact.
22. SEO value never overrides factual truth, topical relevance, or compliance.

---

## 28. Implementation status

**Built and smoke-tested:** repo scaffold; state machine + packet generator with
gates, staleness, goldens, revisions; hard QC (identity, schema, canonical
protection, append-only log, stage gates, secrets, markers, contamination);
qualitative QC workflow; approval-PR shape; manual bridge; page_review stage;
publish pipeline; status board; canary tooling; global-rules layer and
project-state/claims-compliance templates (integration applied, final re-test
and repackage pending).

**Next build (ordered):** claims/banned-phrase scanning → query triage +
ownership ledger → headings/goldens/URL-map schema alignment → bridge automation +
auto revision packets + auto page issues → Kachina Village loaded as the first real
project → one pilot page end-to-end.

---

## End goal

Open the system months later and see exactly what exists, what was approved, why
something changed, what stage every project and page is at, and what the
automation should do next — with output quality that is stable because every
input is identical, every rule is versioned, every failure becomes a permanent
check, and no page ships that is a city-swap, an invented claim, or an answer to
a question another page already owns.
