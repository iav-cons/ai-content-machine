# serp_research — human-provided stage (data drop, not an AI job)

SERP research is performed by the operator and enters the repo as files, not
through a worker packet. Drop files into pages/<PAGE_ID>/ named:
  serp--<page-id>--YYYY-MM-DD.md      (SERP anatomy, competitor scan, PAAs seen)
  paa--<page-id>--YYYY-MM-DD.(md|csv) (scraped PAA set)
  fanout--<tool>--YYYY-MM-DD.(xlsx|csv|md)
Every file carries its date in the name (staleness limits apply) and its
source is self-evident from the prefix. These files are auto-inlined into the
page's query-triage and brief packets. This instruction file exists so the
engine can, exceptionally, issue a serp_research packet to an AI worker — if
that ever happens, the output must follow the same naming and include a
Document Usage Check.
