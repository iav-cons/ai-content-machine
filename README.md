# AI Content Production Engine

This repository runs the controlled content workflow defined in
[`docs/workflow-spec.md`](docs/workflow-spec.md) — **unchanged**. The tooling here
only puts that workflow on rails: state lives in files and labels, approval gates
are physically enforced, QC is automated, and every artifact is versioned and
attributable. The spec is the constitution; when in doubt, the spec wins.

## Tool assignment (spec role → implementation)

| Spec role | Implemented by |
|---|---|
| Files + versions (§21) | This repo. `projects/<id>/` with the §21 folder tree. |
| Approved canonical vs latest (§15, §16) | `main` = canonical. Open PR = proposed. Branch protection makes approved files immutable. |
| Human approval gates (§14) | **Merging a PR is the approval.** Nothing else counts. |
| State + queue (§8, §19, §20) | `projects/<id>/project.yml` (stage state machine) + one GitHub Issue per page with `status:*` labels. |
| Hard QC (§12) | `engine/scripts/hard_qc.py`, run by Actions on every PR. Required check → QC failure blocks merge. |
| Qualitative QC (§12) | Claude reviews the PR against `control/quality-checklist.md` when you add the `needs-qualitative-qc` label. It reports PASS/FAIL — it never approves (§14). |
| Job packets (§10) | `engine/scripts/make_packet.py` — always built from canonical `main`, never by hand (§23.8). Also runnable from the Actions tab. |
| Manual worker bridge (§11) | Packet posted to the page/stage issue → you run it through the Custom GPT → paste the result back as a branch + PR. |
| Revision loop (§13) | QC failure list + previous output feed a revision packet. Max 3 attempts, then `human_review_required`. |
| Change log (§17) | `control/change-log.md`, append-only — hard QC blocks any edit to existing lines. |
| Notifications (optional) | Make/n8n as thin glue on GitHub webhooks (PR opened, label added). No logic lives there (§22). |

## Repo map

```
docs/workflow-spec.md          the canonical spec (verbatim)
engine/qc-config.yml           editable hard-QC rules (headings, intents, max attempts)
engine/scripts/
  new_project.py               §2  project initialization
  make_packet.py               §10 packet generator + §19 state-machine gate
  hard_qc.py                   §12 deterministic QC (CI + local)
  labels.sh                    creates the §8/§11/§13 labels
  status_report.py             STATUS BOARD generator (spec §20)
  publish_notify.py            canonical-content → publish payloads
  canary_diff.py               worker drift detector
engine/templates/project/      control-file templates copied into each new project
benchmarks/                    frozen canary packet + monthly worker outputs
.github/workflows/             hard-qc, qualitative-qc, packet-gen, status-report,
                               publish-notify
projects/<project-id>/         control/ sources/ research/ cluster/ url-map/
                               briefs/ content/ pages/ qc/ jobs/   (§21)
```

## One-time setup

1. Create a **private** GitHub repo and push this scaffold to `main`.
2. Branch protection on `main`: require a pull request before merging, require the
   **Hard QC** status check, disallow force pushes and deletions. (This is what
   makes §14/§15 physically enforceable.)
3. Run `sh engine/scripts/labels.sh <owner/repo>` (needs GitHub CLI) to create the
   status labels.
4. For qualitative QC: install the Claude GitHub app on the repo and add the
   `ANTHROPIC_API_KEY` repository secret
   (setup reference: https://code.claude.com/docs/en/github-actions). Until then,
   do qualitative QC yourself against `control/quality-checklist.md` — the gate
   still works, it's just human-only.
5. Paste your **tested prompts** into `engine/templates/project/control/instructions/`
   (one file per stage). They're placeholders on purpose — the packet generator
   refuses to issue a job while a placeholder is still in place. Your workflow's
   substance lives in these files and only you edit them.
6. Secrets policy (§23.11): keys exist only as GitHub Secrets / worker-side config.
   Hard QC scans every PR for leaked keys.

Local use is optional — everything (packets, QC, review, approval) can be operated
from the GitHub website and the Actions tab.

## Phase 1 — operating loop (per stage: entity research → cluster → URL map)

1. **Initialize** (once):
   `python engine/scripts/new_project.py --id my-next-project --name "My Next Project" --domain example.com --niche "Niche" --location "City, ST"`
   Add source documents to `sources/`, complete the §3 checklist in
   `control/source-context.md`, fill `contamination_terms` in `project.yml`,
   commit on a branch, open the initialization PR, merge it.
2. **Packet**: Actions → *Generate job packet* → project + stage (+ issue number to
   post it to). Or locally: `python engine/scripts/make_packet.py --project <id> --stage entity_research`.
   The generator refuses anything the state machine forbids (§19) and refuses to
   run while source validation is incomplete (§3).
3. **Worker**: run the packet through the assigned worker (Claude / ChatGPT API /
   Custom GPT via the manual bridge below).
4. **Return**: put the single output file at the path named in the packet, on a new
   branch, open a PR (GitHub web UI: *Add file → Create new file → commit to a new
   branch* works fine). Hard QC runs automatically.
5. **QC**: hard QC must be green. Add label `needs-qualitative-qc` for the AI
   review; it posts `QUALITATIVE QC: PASS/FAIL` with an exact failure list.
6. **Fail → revision** (§13): re-run the packet generator with
   `--revision-of <previous output> --failures <failure report> --attempt 2`.
   Attempt 4 does not exist — the generator stops with `human_review_required`.
7. **Approve** (§14): when QC passes and you're satisfied, turn the PR into an
   **approval PR** (see shape below) and merge it. Merging *is* the approval.
   The next stage is now unlocked.

### The approval PR shape

An approval PR contains, together:
- the artifact with frontmatter `status: approved`;
- `project.yml`: the stage status set to `approved` **and** `canonical:` pointing
  at the artifact's path;
- a new line at the end of `control/change-log.md`
  (`YYYY-MM-DD | Stage | User | Approved <artifact> vN — <reason>`).

Hard QC enforces this shape and blocks: approved status without a canonical entry,
approvals without a change-log entry, any later modification of a canonical file
(§15), and any downstream artifact whose prerequisite isn't approved on `main`
(§19). To change an approved decision later, propose `vN+1` in a new PR with the
**Reason for change** section filled — `vN` stays canonical until you merge (§16).

## Manual worker bridge (subscribed Custom GPT — §11)

**Session model: one dedicated chat per project** — bootstrap once, slim
packets per job, SYNC messages on approvals, rotation when the chat ages out.
Full procedure: `docs/mirena-session-protocol.md`; day-to-day loop:
`docs/operator-runbook.md`. The steps below remain the per-message mechanics.

0. **Verification, at the start of every chat:** each job runs in a fresh
   chat, so verify first, every time — send the payment email alone, wait for
   the "subscription is verified" reply, then paste the packet as the next
   message. Always in that fixed order, so the pre-packet context is identical
   across runs. The email is a credential: it never goes into packets, issues,
   or the repo. When copying results back, always start at the artifact's
   opening `---` frontmatter so the verification exchange is never committed.
1. Generate the packet with the issue number filled in → the packet lands as a
   comment on that issue, and the issue gets you a single copy source.
   Label the issue `awaiting_manual_worker`.
2. Open a **fresh chat** with the Custom GPT (no prior context; ChatGPT Memory off
   or a temporary chat — §18/§23.8 project isolation), paste the whole packet.
3. Copy the worker's single output file back: GitHub web UI → *Add file* at the
   exact path named in the packet → *Commit to a new branch* → open PR.
4. From here it's the normal loop: hard QC → qualitative QC → approve by merging.
   Remove `awaiting_manual_worker`.
   The packet is fully self-contained on purpose — the GPT needs nothing outside it.

## Phase 2 — per-page production (§8, §9)

1. After the URL map is approved, create **one issue per page** with the *Page
   production* template (Page ID, URL, priority). Track the queue on a GitHub
   Projects board; work P0 → P3.
2. Page statuses (§8) live as `status:*` labels on the page's issue — move the
   label as the page advances (`researching` → `brief_qc` → `drafting` → …).
3. Per page, the loop is the same as Phase 1, with stages
   `serp_research` → `brief` → `content`:
   - SERP/PAA/fan-out outputs go under `projects/<id>/pages/<PAGE_ID>/` and are
     inlined into the brief packet automatically.
   - The **brief** requires the approved URL map; the brief's approval PR adds
     `canonical["brief:<PAGE_ID>"]`.
   - **content** refuses to start without that approved brief (§14, §23.12).
4. Final content approved + merged → label `status:complete`, close the issue.

## Consistency levers (why output stays stable)

- Packets are always script-generated from canonical `main` — identical inputs
  every time; nothing depends on chat history (§23.8).
- All prompts/instructions are versioned files — any quality shift is traceable to
  a specific diff.
- API workers: **pin dated model versions** in whatever calls them, so provider
  updates can't silently change output.
- Manual worker: same packet template, fresh chat, Memory off — every time.
- `engine/qc-config.yml`: once your tested outputs have a stable structure, add
  their headings to `required_headings` and hard QC will hold that structure
  forever.

## Guardrail coverage (spec §23 → enforcement)

1–2, 12: `make_packet.py` gates + `hard_qc.py` stage-order checks + protected
`main`. 3–4: canonical map + immutability check + PRs. 5: folder/frontmatter
project-id match + contamination scan. 6: §3 checklist gate + contamination terms.
7: only merged PRs change state; workers only ever produce one file. 8: packets
are self-contained and generated from `main`. 9: attempt cap in generator + QC.
10: append-only change-log check. 11: secret scan + Secrets-only policy.
13: revision packets fix only listed failures. 14–15: frontmatter (project, stage,
version, status, job, attempt) + PR history + change log.

## Extensions (bolt-ons — the core workflow above is untouched)

**Performance feedback loop (`page_review` stage).** After a page is live, drop
GSC/analytics exports into `pages/<PAGE_ID>/performance/` and generate a
`page_review` packet (gated: requires that page's approved canonical content).
The review's numbered findings feed a normal content revision:
`make_packet.py --stage content --revision-of <canonical content> --failures <review file>`
— same machinery, now driven by real performance data. Paste your review prompt
into `control/instructions/page-review.md`.

**Publish pipeline.** Merging canonical content to `main` fires
`publish-notify.yml`: a WordPress-ready payload (markdown + HTML) is POSTed to
your Make webhook and the publish event is commented on the page's issue. Make
does only the WordPress call — recipe in `docs/make-publish.md`. Secret:
`MAKE_PUBLISH_WEBHOOK_URL`. Only canonical content can ever publish (§16).

**Golden examples.** Put your single best approved output per stage in
`control/golden/` (filenames in its README) and every future packet for that
stage inlines it as "match this structure and quality." The strongest
consistency lever after fixed inputs.

**Worker canary.** `benchmarks/canary-packet.md` is a frozen benchmark job: paste
your real prompt once, then run it through MIRENA monthly, save outputs as
`benchmarks/mirena/YYYY-MM.md`, and `canary_diff.py` flags structural drift —
your alarm that the vendor shipped an update. Procedure: `benchmarks/README.md`.

**Staleness guard.** `staleness_max_age_days` in `engine/qc-config.yml`
(defaults: SERP research 45d, briefs 120d). The packet generator refuses to build
content on decayed research; `--allow-stale` overrides consciously and stamps the
acceptance into the packet.

**STATUS BOARD.** A daily action maintains one issue titled "STATUS BOARD":
every project's stage statuses, the page queue by label, and stalls (manual work
waiting ≥7 days, anything in `human_review_required`). Stalls can ping Make for
a notification — secret: `MAKE_STATUS_WEBHOOK_URL`. Run on demand from the
Actions tab any time.

Optional secrets summary: `ANTHROPIC_API_KEY` (qualitative QC),
`MAKE_PUBLISH_WEBHOOK_URL` (publish), `MAKE_STATUS_WEBHOOK_URL` (stall alerts).
Everything degrades gracefully when a secret is absent.
