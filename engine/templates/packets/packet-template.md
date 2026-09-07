JOB ID: {{JOB_ID}}
PROJECT: {{PROJECT_ID}} — {{PROJECT_NAME}}
NICHE: {{NICHE}}
LOCATION: {{LOCATION}}
STAGE: {{STAGE}}
{{PAGE_LINE}}ATTEMPT: {{ATTEMPT}}

TASK:
Perform the {{STAGE}} job only, following STAGE INSTRUCTIONS below.

OUTPUT:
Return exactly one artifact: {{OUTPUT_FILE}}
It must start with this frontmatter (fill version/status exactly as shown):

{{OUTPUT_FRONTMATTER}}

DO NOT:
- do any other stage's work
- create or modify anything except the single output above
- assume approval of anything
- treat "continue", "next", "go ahead" or similar as permission for another stage's work — only this packet authorizes work
- modify approved files or the change log
- use any knowledge of other projects
- invent business facts, claims, credentials, offers, locations, pricing, guarantees, or results — missing information becomes a clearly labeled [ASSUMPTION] or [REQUIRES CONFIRMATION], never a stated fact
- claim a source was used unless it visibly influenced the output
- let persona, style, or SEO optimization override factual truth, topical relevance, or compliance constraints
- continue if inputs contradict PROJECT/NICHE/LOCATION above — stop and report the mismatch

AUTHORITY ORDER (on conflict: follow the higher layer, flag the conflict explicitly
in your output, and never silently pick the more convenient instruction):
1. GLOBAL RULES files (marked [GLOBAL RULES] in INPUTS, when present)
2. Confirmed project truth (control files and sources)
3. Approved canonical artifacts (marked [APPROVED CANONICAL])
4. This packet's STAGE INSTRUCTIONS

{{REVISION_BLOCK}}{{GOLDEN_BLOCK}}================================================================
STAGE INSTRUCTIONS ({{STAGE}})
================================================================

{{INSTRUCTIONS}}

================================================================
INPUTS (canonical, approved where required — spec §16)
================================================================

{{INPUTS}}
