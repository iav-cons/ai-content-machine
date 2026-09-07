# Workflow Specification (canonical — 2026-08-12)

This document is the constitution of this repository. The tooling implements it 1:1.
Nothing in the tooling may contradict it.

---

## 1. What we're building

A controlled AI Content Production Engine that takes the multi-step workflow already used
with ChatGPT / Claude / the subscribed third-party Custom GPT and turns it into a persistent system.

Roles:
- Orchestration runs the workflow.
- State layer remembers exactly where every project/page/job is.
- GitHub stores and versions the important files.
- AI systems perform specific jobs.
- The human approves strategic decisions and resolves exceptions.

## 2. Phase 1 — Project Strategy & Setup

A new project starts with: Project name, Domain/website, Niche, Location, Source documents,
Project-specific instructions.

Stage sequence:

PROJECT INITIALIZATION → SOURCE VALIDATION → CONTROL FILES → ENTITY RESEARCH → QC → HUMAN APPROVAL
→ CONTENT CLUSTER → QC → HUMAN APPROVAL → URL MAP → QC → HUMAN APPROVAL → PHASE 1 COMPLETE

## 3. Source Validation

Before AI strategy work starts, the system checks the supplied project documents:
correct project, correct niche, correct location, correct domain, required files present,
no contradictory instructions, no remnants from another project/template, no obvious factual conflicts.

Failure mode designed against: Phoenix Drain Cleaning project → source file accidentally contains
Seawall Repair instructions. That must BLOCK the workflow.

## 4. Control Files

Persistent operating files per project: project-brief.md, operating-rules.md, quality-checklist.md,
change-log.md, project-state/config, source-context files, persona/ICP files.
Subsequent jobs inherit these. The AI never reconstructs project rules from conversation history.

## 5. Entity Research

Job = PROJECT + SOURCE CONTEXT + OPERATING RULES + ENTITY RESEARCH INSTRUCTIONS → entity-research.md
Then: Hard QC → Qualitative QC → Human approval. The approved version becomes canonical.

## 6. Content Cluster

Only approved entity research feeds this stage.
QC checks: search intent, entity coverage, duplicate pages, cannibalization, missing pages,
unsupported pages, page vs section decisions, commercial/informational balance, hierarchy.
PASS → Awaiting Approval. FAIL → Revision. Human approves the final cluster.

## 7. URL Map

Approved cluster is the input. Structured page records: Page ID, Page Name, URL, Page Type,
Primary Query, Intent, Parent, Priority, Status.
QC: duplicate URLs, duplicate IDs, malformed slugs, broken hierarchy, orphan pages,
intent overlap, cannibalization. Human approves. Phase 1 complete.

## 8. Phase 2 — Production Queue

Approved URL map = production plan. Priorities:
P0 homepage/core money pages, P1 major service/category pages, P2 supporting commercial pages,
P3 informational/supporting content.

Per-page statuses: not_started, researching, research_complete, brief_pending, brief_qc,
awaiting_approval, approved, drafting, draft_qc, revision, complete.

Workflow state exists independently of any chat.

## 9. Page Production Workflow

PAGE SELECTED → ENTITY CONTEXT → SERP RESEARCH → PAA / FAN-OUT DATA → COMPETITOR / INTENT ANALYSIS
→ CONTENT BRIEF → QC → APPROVAL → CONTENT GENERATION → QC → REVISION IF NEEDED → FINAL CONTENT
→ SAVE + VERSION

## 10. AI is a worker, not the controller

Workers receive a job packet (JOB ID, PROJECT, STAGE, ATTEMPT, TASK, INPUTS, OUTPUT, DO-NOT list).
AI performs one job. Orchestration determines what happens next.

## 11. Special handling for the subscribed Custom GPT

No API assumed. Manual bridge:
create job → complete job packet → status = awaiting_manual_worker → HUMAN runs packet through the
Custom GPT → returns result → system ingests → QC → workflow continues.
If the owner later provides an API, the bridge is replaced.

## 12. Hard QC vs qualitative QC

Hard QC (deterministic, automated): required file exists, required field exists, correct project,
correct location, correct niche, correct page, duplicate URL, duplicate page ID, required headings,
valid output format, protected artifact modified.

Qualitative QC (judgment, AI and/or human): search intent correct, entity coverage sufficient,
page redundancy, cannibalization risk, brief strategically good, content actually useful.

## 13. Revision loop

QC failure ≠ start over. Revision packet = original instructions + previous output + exact QC
failures + exact correction requirements. Maximum 3 automated revision attempts, then
human_review_required — the system stops.

## 14. Approval gates are absolute

QC PASS → AWAITING APPROVAL → STOP. QC pass is never interpreted as human approval.
Only human approval unlocks the next stage. Applies especially to: entity research, content cluster,
URL map, important content briefs, major strategic revisions.

## 15. Approved files are protected

An approved artifact is never overwritten. Changes arrive as PROPOSED vN+1 with DIFF + reason for
change → QC → human approval → only then does vN+1 become canonical.

## 16. Canonical vs latest is critical

latest ≠ approved canonical. Downstream production uses the approved canonical version until a
newer version is approved. Newest does not mean authoritative.

## 17. Change log

Important decisions become permanent history (date, stage, actor, description).
Append-only. AI may add entries. AI may never erase history.

## 18. Project isolation

Every artifact, job, page, QC run, approval, change belongs to a specific project_id.
Cross-project retrieval is forbidden. Project identity is checked throughout.

## 19. State machine guardrail

The workflow cannot jump around. Example: entity_research = awaiting_approval means Content Cluster
cannot start. content_cluster = approved + url_map = awaiting_approval means page production cannot
start. Recorded state controls progression.

## 20. State layer

Tracks: projects, stages, pages, artifacts, jobs, qc_runs, approvals, change_log.
Answers: what project is this, where are we, what is approved, what's waiting, what failed,
what needs revision, what should happen next.

## 21. File layer (GitHub)

/projects/<project-id>/ with control/, sources/, research/, cluster/, url-map/, briefs/, content/, qc/
Proper file history and recoverability.

## 22. Orchestration

Creates projects, initializes stages, creates jobs, moves statuses, calls available AI/API services,
generates job packets, waits for manual worker, receives outputs, runs QC, creates revisions,
requests approval, stores artifacts, updates state, commits files, writes change logs, advances the
workflow. Orchestration is not the long-term knowledge store.

## 23. Core guardrails

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

End goal: open the system months later and see exactly what exists, what was approved, why something
changed, what stage every project/page is at, and what the automation should do next — without
depending on any particular AI conversation.
