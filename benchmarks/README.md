# Worker canary (drift alarm)

The one variance source the engine cannot pin is a worker changing underneath you
— the Custom GPT vendor shipping an update, or an unpinned model changing. The
canary makes that visible within a month instead of after degraded deliverables.

## Procedure

1. **Freeze the packet once.** Open `canary-packet.md`, paste your real
   entity-research prompt into the marked slot, commit — and never edit it again.
   Same input forever is the whole point.
2. **Monthly run.** Fresh chat with the worker (Memory off), paste the entire
   frozen packet, save the output verbatim as `benchmarks/mirena/YYYY-MM.md`
   (via PR — benchmarks are outside `projects/`, so hard QC leaves them alone).
   Same idea for API workers after any model change: `benchmarks/claude/…`.
3. **Diff.**
   `python engine/scripts/canary_diff.py benchmarks/mirena/2026-08.md benchmarks/mirena/2026-09.md`
   Wording variance = normal. **Structural drift** (headings changed, sections
   appearing/vanishing, length shifting hard) = the worker changed → re-validate
   quality on the next few real jobs and tighten `required_headings` in
   `engine/qc-config.yml` if needed.
