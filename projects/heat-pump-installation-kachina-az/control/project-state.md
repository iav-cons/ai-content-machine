---
project_id: "heat-pump-installation-kachina-az"
stage: control
niche: "Heat Pump Installation"
location: "Kachina Village, AZ"
---
# Project State — Kachina Village Heat Pump Installation (continuity dashboard)

Inlined into every packet; page 30 must not forget page 3. Machine state in
project.yml; decisions and notes here. Update in every approval PR.

## Current position (2026-08-12)
Phase 1 COMPLETE (entity research, cluster, URL map all approved — ingested
pre-engine work). Phase 2 not started: 67 pages, all not_started. Next: pilot
page TRUST-002 (Coconino County Permits) — its QueryFan data is already in
pages/TRUST-002/.

## Active decisions
- Ownership system: owns/must_not_own per page in the URL map is law.
- Cost lives only in COST-001..006; every service page links to it.
- One mini-split page (COM-004); ducted ≠ ductless; installation ≠ replacement.
- Location pages require confirmed local facts before briefing (see
  quality-checklist location rules); Flagstaff routes Kachina/Mountainaire
  intent back to their pages.
- Free assessment (COM-009) is the single conversion target every spoke
  points at.

## Internal-linking notes
Hub-and-spoke per url-map-v1.yml hierarchy; spokes link up to hub + COM-009;
location pages link to services, never to each other in bulk.

## Cannibalization notes
Guardrails ingested from the approved map: Installation≠Replacement,
Ducted≠Ductless, DualFuel≠PropaneComparison, Assessment≠Contact,
ColdClimate≠AltitudeEducation, Cost≠OperatingCost, ManualJ≠Sizing,
Permits≠ROCLicensing, Commissioning≠InstallationProcess,
QuoteComparison≠Assessment. Ledger: control/query-ownership.md (empty — fills
as triage artifacts are approved).

## Open questions
All Operations-truth items in source-context marked [REQUIRES CONFIRMATION]
(partner ROC, brands installed, certifications, NAP/phone, GBP, cost ranges,
financing lender, emergency staffing). Content depending on any of them is
blocked until confirmed.

## Next step
Bootstrap the MIRENA project chat → run query_triage for TRUST-002 → brief →
content (the pilot page).
- setup test line (safe to remove later)
