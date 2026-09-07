# MIRENA Session Protocol (one chat per project)

The chat is the workspace; the repo is the truth. MIRENA's session
intelligence — accumulated project context across jobs — is part of what the
subscription buys, and this protocol uses it while keeping canonical state in
the repo where it cannot drift or be lost.

## Chat lifecycle
1. **Open** one new, dedicated chat per project. ChatGPT Memory OFF
   (account-level memory would leak across projects; the dedicated chat itself
   is the persistence).
2. **Verify** — send the payment email ALONE, wait for "subscription is
   verified." The email is a credential: never in packets, issues, or the repo.
3. **Bootstrap** — generate with
   `python engine/scripts/make_session.py bootstrap --project <id>`
   (or the Actions tab). Large bootstraps are auto-split into parts under
   the paste limit: paste part 1, wait for the exact reply "READY 1/n",
   continue part by part; MIRENA acts only after the final part. It carries
   the session rules, both global rulesets, all control files, and the current
   canonical state. MIRENA confirms stage + next allowed step and stops.
4. Record the chat start: change-log line + `session.chat_started` in
   project.yml (via the same PR as any bootstrap-day approvals).

## Job loop (inside the chat)
- Every job = a **slim packet** (`make_packet.py --slim …`): job header, stage
  contract, canonical-state block, page record, and any human data files —
  no re-pasted rulesets or control files.
- MIRENA returns exactly one artifact in one code block. You commit it on a
  new branch at the packet's output path → PR → hard QC → (label) qualitative
  QC → you merge to approve.
- **SYNC after every approval or correction:**
  `make_session.py sync --project <id> --artifact <path>` → paste into the
  chat. The sync states: this exact text is now canonical; in-chat variants
  are void. QC-rejected or premature outputs are VOID DRAFTS — the revision
  packet (with exact failures) supersedes them.
- Control-file changes (rules, compliance, state) merged to main also get a
  sync so the chat never works from stale rules.

## Chat rotation (when the context window ages out)
Signs: MIRENA forgets synced state, re-asks settled questions, or quality
drifts. Then: generate a FRESH bootstrap from current main (it embeds the
latest control files, statuses, and canonical list), open a new chat, verify,
paste, log the rotation in the change log, archive the old chat unused.
Nothing is lost — the repo held the truth the whole time. Rotate proactively
at major milestones on large projects (e.g., after Phase 1, every ~15–20
pages).

## Hygiene
- Copy results starting at the artifact's opening frontmatter — the
  verification exchange and any chat preamble never enter the repo.
- Never discuss another project in the chat, ever (spec §18).
- The monthly canary (benchmarks/) still runs in a separate fresh chat — it
  measures the worker, not the project.
