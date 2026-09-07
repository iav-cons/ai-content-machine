# Setup & daily use — the button version

After a one-time install, you never open the Actions tab, never edit YAML,
never create files. You type short commands as comments on GitHub issues.

## One-time install (already done for ai-content-engine: skip to "Upgrade")
1. Create a private repo → upload `content-engine.zip` (the zip file itself).
2. Green **Code** → **Codespaces** → **Create codespace on main** → in its
   terminal paste:
   `unzip -o content-engine.zip && cp -a content-engine/. . && rm -rf content-engine content-engine.zip && bash engine/scripts/setup_codespace.sh`
3. Browser: Settings → Secrets and variables → Actions → `ANTHROPIC_API_KEY`.
4. Delete the codespace.

## Upgrade an existing install
Upload the new zip → open a codespace → paste the same line → delete codespace.

## Commands (type as the first line of an issue comment)
| Command | What happens |
|---|---|
| `/bootstrap` | posts the project-chat bootstrap in parts |
| `/packet <stage>` | posts a slim job packet for the issue's page |
| `/ingest` + pasted artifact | places the file, opens the PR, runs Hard QC + Claude review, posts the verdict (or a revision packet) |
| `/approve` | bookkeeping, merge, SYNC message, and the next packet — automatically |
| `/pages P0` (P1, all) | one issue per not-started page of that priority |
| `/factor` | derives the whole control stack from the docs in `sources/` (intake issue) |
| `/sync <path>` | SYNC message for any file |

## New project from your documents
Issues → New issue → **New project (intake)** → submit → upload your four docs
(questionnaire, entity analysis, ICP, master prompt) into `projects/<id>/sources/`
→ comment `/factor` → read the PR → merge → comment `/bootstrap`.

## Business facts
Issues → New issue → **Truth update** → fill what you know → submit.
It lands in source-context (and the ROC number in claims wording) and merges itself.

## Per page
`/packet query_triage` → paste into MIRENA → `/ingest` her answer → read verdict
→ `/approve` → (brief packet appears) → paste → `/ingest` → `/approve`
→ (content packet appears) → paste → `/ingest` → `/approve` → page complete.
