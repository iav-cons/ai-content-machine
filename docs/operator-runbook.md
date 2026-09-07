# Operator Runbook — the minimum-human loop

Everything NOT listed here is the system's job. Your work is: strategy,
research data collection, verify-paste-return on the bridge, and approvals.

## Once per project
1. `new_project.py` (or copy an existing project as template) → fill control
   files → tick source validation → set contamination_terms → initialization
   PR → merge.
2. Fill Operations truth in source-context (or leave [REQUIRES CONFIRMATION] —
   dependent claims stay blocked, everything else proceeds).
3. Open the MIRENA project chat: verify → paste bootstrap (multi-part on
   large projects: paste each part, wait for "READY x/y", act only after the
   final part) → log chat start (docs/mirena-session-protocol.md).
4. After URL-map approval: create page issues (template: "Page production"),
   priority labels P0→P3.

## Per page (the production loop — ~4 pastes of your time)
1. **Data drops (you, manual):** put your files in `pages/<PAGE_ID>/` via
   web UI → "Add file", commit to a branch, PR, merge. Naming (date = when
   collected; staleness limits enforce freshness):
   - `serp--<page-id>--YYYY-MM-DD.md`
   - `paa--<page-id>--YYYY-MM-DD.(md|csv)`
   - `fanout--<tool>--YYYY-MM-DD.(xlsx|csv|md)`
   - later: `performance/gsc--YYYY-MM.csv`
2. **Query triage:** Actions → Generate job packet (stage `query_triage`,
   page id, issue number, `--slim` is automatic for session projects) → paste
   packet into the project chat → commit MIRENA's triage artifact → PR → QC →
   merge → paste SYNC. Ledger rows from the artifact go into
   `control/query-ownership.md` in the same PR.
3. **Brief:** same loop, stage `brief`. The generator refuses a brief
   without an approved triage for the page (`--skip-triage` overrides,
   consciously). Triage approval PRs set `canonical["query_triage:<PAGE_ID>"]`.
   Brief approval PRs set `canonical["brief:<PAGE_ID>"]` + change-log line +
   state update → SYNC.
4. **Content:** same loop, stage `content`. Output format is simple HTML
   (frontmatter carries slug/title/meta) — passes to WordPress untouched. Hard QC machine-scans never-claim
   patterns and banned phrases; qualitative QC checks the brief contract.
   Approval PR sets `canonical["content:<PAGE_ID>"]` → SYNC → label
   `status:complete` → publish fires automatically (if Make is wired).
5. **Failures:** hard QC prints numbered failures → regenerate with
   `--revision-of <artifact> --failures <report> --attempt N` → paste → return.
   Attempt 4 doesn't exist; the system stops with human_review_required.

## Recurring
- Monthly: canary run + `canary_diff.py` (worker drift alarm).
- Monthly: GSC export into `pages/<id>/performance/` for live pages →
  `page_review` jobs for underperformers → findings feed content revisions.
- Daily: STATUS BOARD issue updates itself; stall alerts ping Make if wired.
- Quarterly: verify volatile incentive facts in source-context; update
  verified-on dates via PR + SYNC.

## Every manual touch, enumerated
Collect SERP/PAA/fan-out data · upload data files · fill/confirm truth gaps ·
verify + paste bootstrap/packets/SYNCs into the chat · commit MIRENA's outputs
· add the qualitative-QC label when ready · merge approvals · set page labels
· monthly canary + GSC export. Everything else — packet assembly, QC, state
gates, immutability, publish payloads, status — is automated.
