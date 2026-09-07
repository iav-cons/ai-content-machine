# Entity Analysis: "Heat Pump Services, Kachina, AZ"

## Overview

- **Input**: heat pump services, Kachina, AZ
- **Resolved location**: Kachina Village, Coconino County, Arizona (CDP, ZIP 86005, elev. 6,798 ft)
- **Central Entity**: Heat pump
- **Total entities extracted**: 52
- **Validation coverage**: 42% high confidence · 37% medium · 21% low
- **Analysis date**: July 23, 2026

> ### ⚠ Read this first: two findings that change the whole build
>
> **1. "Kachina" alone is a disambiguation trap.** The dominant entity for the bare string *kachina* is the Hopi/Puebloan **katsina** — a spirit being and carved doll, with a Wikipedia article, Knowledge Panel, and museum/retail SERP. Your place entity is **Kachina Village, Arizona** (GNIS 2408458). Writing "Kachina, AZ" forces search engines to resolve an ambiguous string against a much stronger cultural entity. **Always write the full form "Kachina Village."**
>
> **2. This is a heating market, not a cooling market.** Kachina Village sits at 6,798 ft in Ponderosa pine forest ~10 miles south of Flagstaff. January mean low is 18.4°F; July mean high is 83.4°F. Nearly every piece of Arizona heat pump content on the web is written for Phoenix (Zone 2B, hot-dry). Applying that template here is the single biggest failure mode — and the single biggest opportunity. In Kachina Village, a heat pump is bought as a **furnace replacement**, not an AC upgrade.

---

## Central Entity

**Entity**: Heat pump
**Type**: Product / HVAC equipment (technology)
**Definition**: An electrically driven vapor-compression system that moves heat between outdoor air and a building's interior, reversing direction seasonally via a reversing valve to provide both heating and cooling from one appliance.
**Salience**: 1.0
**Validation**: **High** — Wikipedia article, Knowledge Panel, extensive "People Also Ask" coverage, rich autocomplete with attribute-level suggestions (cost, how it works, vs furnace, in cold weather).

### Why "heat pump" and not the alternatives

| Candidate | Test result |
|---|---|
| **Heat pump** ✅ | Passes all four. Every other entity is a type of, part of, problem with, or action performed on a heat pump. |
| "Heat pump services" ❌ | "Services" is a **predicate wrapper** (install, repair, maintain, replace), not an entity. It has no independent meaning and no Knowledge Graph presence. |
| "Kachina Village" ❌ as central | Fails the Coverage Test — the location doesn't appear in every technical section. But see below: it is unusually high-salience for a modifier. |

### The geographic anchor is doing real work here

Normally a city name is a low-salience qualifier. Not in this case. **Kachina Village carries salience 0.9** because the location is *causally determinative* of the technical content — elevation and climate zone decide which sub-entities are relevant and which are noise:

| Location forces IN | Location forces OUT |
|---|---|
| Cold-climate heat pump (ccASHP) | SEER2 as the headline metric |
| Backup / auxiliary heat, balance point | Monsoon dust and desert coil fouling |
| Defrost cycle, snow clearance, elevated mounting | Evaporative cooling comparisons |
| Propane furnace comparison, dual-fuel | "Beat the summer heat" framing |
| Altitude derating at ~6,800 ft | 5-ton oversizing habits from the Valley |

Treat this as a **bound entity pair — Heat pump × Kachina Village** — rather than a topic plus a city tag.

---

## Entity Classification

### Primary Entities (0.8 – 1.0)

| Entity | Type | Salience | Validation | Placement |
|---|---|---|---|---|
| Heat pump | Product | 1.0 | High | H1, title, meta, first 100 words, schema, throughout |
| Kachina Village, Arizona | Location | 0.9 | High | H1, title, meta, first sentence, `areaServed` schema |
| Cold-climate heat pump (ccASHP) | Product subtype | 0.85 | Medium | H2, first 200 words, repeated |
| Heat pump installation | Service / Process | 0.85 | High | H2, service schema, CTA |
| Heat pump repair | Service / Process | 0.85 | High | H2, service schema, emergency CTA |
| Air-source heat pump | Product subtype | 0.80 | High | Define on first use; distinguish from geothermal |

### Secondary Entities (0.5 – 0.7)

| Entity | Type | Salience | Validation | Relationship to Central |
|---|---|---|---|---|
| Auxiliary / backup heat (electric strip) | Component | 0.70 | High | Supplements heat pump below balance point |
| Flagstaff, Arizona | Location | 0.70 | High | Parent metro; service-area anchor 10 mi north |
| Snow | Condition | 0.68 | High | Environmental constraint on outdoor unit |
| Manual J load calculation | Process | 0.68 | High | Determines correct heat pump sizing |
| Propane / LP furnace | Product / Substance | 0.65 | High | Incumbent heat source being replaced or paired |
| Dual-fuel (hybrid) system | System type | 0.65 | Medium | Heat pump + fossil backup configuration |
| Elevated mounting / snow stand | Component | 0.62 | Medium | Required install detail in snow country |
| Balance point | Concept / Metric | 0.60 | Medium | Temperature where heat pump output = building load |
| Defrost cycle | Process | 0.60 | High | Removes coil frost during heating |
| HSPF2 | Metric | 0.60 | High | Heating efficiency rating — the metric that matters here |
| Ductless mini-split | Product subtype | 0.60 | High | Common retrofit path for cabins/additions |
| Heat pump replacement | Service | 0.60 | Medium | Commercial intent variant |
| Efficiency Arizona (HEAR) | Program | 0.60 | Medium | Active incentive pathway in 2026 |
| Coconino County | Location | 0.58 | High | Permitting jurisdiction (unincorporated) |
| Heat pump maintenance / tune-up | Service | 0.58 | Medium | Recurring revenue service |
| Emergency heat mode | Concept | 0.55 | Medium | Thermostat setting homeowners misuse |
| Altitude derating (~6,800 ft) | Concept | 0.55 | **Low** | Airflow/CFM and capacity correction — see opportunity note |
| IECC Climate Zone 5B | Classification | 0.55 | Medium | Code/design context for equipment selection |
| Arizona ROC license (R-39R / CR-39) | Credential | 0.55 | Medium | Trust signal; legally required over $1,000 |
| SEER2 | Metric | 0.50 | High | Cooling efficiency — **deliberately demoted** |

### Supporting Entities (0.2 – 0.4)

| Entity | Type | Salience | Validation | Role |
|---|---|---|---|---|
| Frozen / iced outdoor coil | Condition | 0.42 | Medium | Top winter symptom query |
| Air handler | Component | 0.40 | High | Indoor half of the system |
| Ductwork / duct sealing | Component | 0.40 | High | Capacity killer in older Kachina homes |
| Weatherization, insulation, air sealing | Process | 0.40 | High | Prerequisite for heat pump success |
| Coefficient of Performance (COP) | Metric | 0.40 | High | Efficiency at a given outdoor temp |
| APS (Arizona Public Service) | Organization | 0.40 | High | Electric utility for Kachina Village |
| Emergency / 24-hour service | Concept | 0.40 | Low | Conversion driver in winter |
| City of Flagstaff Energy Rebate | Program | 0.38 | Medium | **Eligibility caveat — see incentives section** |
| Refrigerant leak | Condition | 0.36 | High | Common repair cause |
| Wood stove / fireplace | Product | 0.35 | High | Near-universal secondary heat locally |
| R-454B / A2L refrigerant | Substance | 0.35 | Medium | 2025 refrigerant transition |
| Mechanical permit | Process | 0.35 | Medium | Coconino County Community Development |
| Smart thermostat | Product | 0.35 | High | Dual-fuel and aux-heat control |
| Short cycling | Condition | 0.32 | Medium | Oversizing symptom |
| Reversing valve | Component | 0.30 | High | Defines heat pump vs AC |
| Geothermal / ground-source | Product subtype | 0.30 | High | Alternative; contrast only |
| Ponderosa pine / Coconino NF | Location / Nature | 0.30 | High | Needle debris in coils; wildfire smoke |
| 25C tax credit (expired) | Program | 0.28 | High | **Must be corrected, not promoted** |
| Munds Park, Mountainaire, Forest Highlands | Locations | 0.25 | High | Adjacent service-area entities |
| Heat pump water heater | Product | 0.24 | High | Cross-sell, separate incentive |
| Capacitor failure | Condition | 0.22 | Medium | Common repair cause |

### Contextual Entities (0.1 – 0.2)

NEEP ccASHP Product List (0.20) · AHRI-matched system (0.20) · ENERGY STAR (0.20) · Manual S / Manual D (0.20) · MERV filtration & wildfire smoke (0.20) · EPA Section 608 certification (0.15) · Kachina Village Improvement District (0.15) · ACCA (0.12) · ASHRAE (0.10)

---

## Attribute Analysis

### Root Attributes — cover all of these

| Attribute | Why It's Essential | Content Requirement |
|---|---|---|
| Heating capacity (BTU/h) | Defines whether the unit can hold the house | State capacity **at 47°F and at 17°F/5°F**, not just nominal tons |
| Cooling capacity / tonnage | Sizing baseline | Cover briefly; secondary in this climate |
| HSPF2 rating | Seasonal heating efficiency | Lead metric — explain what the number means on a January bill |
| SEER2 rating | Seasonal cooling efficiency | Mention and move on; do not headline |
| Refrigerant type and charge | Determines serviceability and future parts | Address R-454B/A2L transition plainly |
| Outdoor unit + indoor coil/air handler | System architecture | Diagram or plain-language walkthrough |
| Reversing valve | The thing that makes it a heat pump | Define on first mention |
| Defrost cycle | Universal winter behavior; source of panic calls | Explain steam clouds are normal |
| Electrical requirements | Breaker, disconnect, possible panel upgrade | Flag panel capacity as a real cost line |
| Warranty terms | Purchase decision factor | Separate parts / labor / compressor |
| Expected lifespan | Purchase decision factor | Give a range with local caveats |
| Air filter | Maintenance baseline | Tie to pine debris and wildfire smoke |

### Rare Attributes — cover these to differentiate

| Attribute | Differentiating Value | When to Include |
|---|---|---|
| **Rated capacity at 5°F** | The decisive spec at 6,798 ft. Most units lose 40–60% of nameplate capacity by 5°F; true ccASHPs hold far more | Every installation and sizing page — non-negotiable |
| Variable-speed inverter compressor | Enables capacity retention in cold and low-load modulation | Installation, equipment comparison |
| Low-ambient operating limit | The temperature below which the unit stops | Sizing, dual-fuel, "will it work here" pages |
| Integrated dual-fuel control | Switches to propane below the balance point | Dual-fuel and propane-comparison pages |
| Base pan heater | Prevents ice accumulation in the drain pan | Snow-country install detail |
| Ducted vs ductless configuration | Determines retrofit feasibility in older cabins | Installation, mini-split pages |
| Manufacturer snow-stand height spec | Install-manual requirement that voids warranty if ignored | Installation quality / "how to vet a contractor" |
| NEEP ccASHP list inclusion | Third-party verification of cold performance | Equipment selection |

### Unique Attributes — highest relevance, use sparingly

| Attribute | Unique To | Relevance Boost |
|---|---|---|
| Rated heating output down to −13°F | Specific hyper-heat inverter product lines | Directly answers the "does a heat pump work in Flagstaff winter" objection with a number |
| Manufacturer altitude-correction tables for 6,000–7,000 ft | Individual manufacturers' engineering data | **Highest-value differentiator on the page** — almost no competitor content addresses air density at elevation |
| ≥100% capacity retention at 5°F | A small set of premium models | Converts skeptics; strong linkable-asset hook |
| City of Flagstaff "Primary Source" designation (heat pump sized to carry ≥80% of heating) | A local program term of art | Signals genuine local knowledge to both readers and search engines |

---

## Entity Relationships (EAV Triples)

| Entity | Attribute (Predicate) | Value |
|---|---|---|
| Heat pump | is a | HVAC system |
| Heat pump | provides | heating and cooling |
| Heat pump | contains | reversing valve |
| Heat pump | performs | defrost cycle |
| Heat pump | measured by | HSPF2, SEER2, COP |
| Heat pump | requires | Manual J load calculation |
| Cold-climate heat pump | is a type of | heat pump |
| Cold-climate heat pump | retains capacity at | 5°F and below |
| Cold-climate heat pump | recommended for | IECC Climate Zone 5B |
| Kachina Village | located in | Coconino County, Arizona |
| Kachina Village | has elevation | 6,798 ft |
| Kachina Village | located near | Flagstaff, Arizona (~10 mi) |
| Kachina Village | receives | electric service from APS |
| Kachina Village | is | unincorporated (not in Flagstaff city limits) |
| Elevation | reduces | air density and heat pump airflow capacity |
| Snow | blocks | outdoor unit airflow |
| Snow | requires | elevated mounting above peak snow depth |
| Defrost meltwater | must | drain away and not refreeze |
| Auxiliary heat | engages below | the balance point |
| Balance point | determined by | building heat loss and equipment capacity curve |
| Dual-fuel system | combines | heat pump and propane furnace |
| Propane furnace | serves as | backup heat below balance point |
| Emergency heat mode | bypasses | the heat pump entirely |
| Emergency heat mode | increases | electricity cost |
| Efficiency Arizona HEAR | provides | up to $8,000 for income-qualified households |
| Section 25C credit | expired on | December 31, 2025 |
| Arizona ROC | issues | R-39R and CR-39 licenses |
| HVAC work over $1,000 | requires | a licensed contractor in Arizona |

### Key Predicates

`installs` · `repairs` · `replaces` · `services` · `sizes` · `retains capacity at` · `switches to` · `engages below` · `defrosts` · `elevates above` · `drains` · `derates for` · `qualifies for` · `requires` · `is located in` · `serves`

Use these verbs in headings and body copy. Prefer `heat pump installation in Kachina Village` over `Kachina Village HVAC solutions` — the first expresses a triple, the second expresses nothing.

---

## Co-Occurrence Map

### High priority — same sentence or paragraph

- **Heat pump + Kachina Village** — the query pair; must appear together early and repeatedly
- **Heat pump + cold weather / winter** — the core objection this content exists to answer
- **Cold-climate heat pump + capacity at 5°F** — defining characteristic
- **Kachina Village + elevation 6,798 ft** — establishes the local technical premise
- **Snow + elevated mounting + defrost drainage** — one causal chain, keep it intact
- **Balance point + auxiliary heat** — meaningless apart
- **Manual J + correct sizing** — definitional pairing
- **Emergency heat + higher electric bill** — corrects the most common homeowner error

### Medium priority — same section

- Heat pump + propane furnace + dual-fuel
- Kachina Village + Flagstaff + Coconino County
- HSPF2 + SEER2 + COP
- Ductless mini-split + retrofit + older cabin
- HEAR rebate + income qualification + Efficiency Arizona
- Insulation + air sealing + heat pump performance
- ROC license + permit + warranty

### Document level

- Heat pump + wood stove (secondary heat reality)
- Heat pump + wildfire smoke + filtration
- Heat pump + heat pump water heater (cross-sell)
- Heat pump + geothermal (contrast only)
- Kachina Village + Munds Park / Mountainaire / Forest Highlands (service-area silo)

---

## Validation Summary

### High confidence — use freely

**Heat pump** (Wikipedia, Knowledge Panel, dense PAA) · **Kachina Village, Arizona** (Wikipedia, GNIS feature ID 2408458, Census CDP, coordinates and elevation published) · **Flagstaff, Arizona** · **Coconino County** · **APS / Arizona Public Service** · **SEER2** and **HSPF2** (DOE standards) · **Manual J** (ACCA) · **Propane** · **Defrost cycle** · **Ductless mini-split** · **Geothermal heat pump** · **ENERGY STAR**

### Medium confidence — define on first use

- **Cold-climate heat pump / ccASHP** — recognized as a product class via DOE and the NEEP product list, but no discrete Knowledge Panel. Define it explicitly the first time.
- **Balance point** — a real HVAC term with thin consumer-facing coverage. Define in one sentence.
- **IECC Climate Zone 5B** — the zone itself is well documented, but sources **conflict on Coconino County's assignment**: some place Flagstaff-elevation locations in 4B, while DOE Zero Energy Ready Home documentation for a Flagstaff project lists 5B. Verify with Coconino County Community Development before publishing a specific zone number.
- **Efficiency Arizona / HEAR** — launched 2025, administered by the Arizona Governor's Office of Resiliency. Real but recent; link the official source.
- **Arizona ROC R-39R / CR-39** — confirmed on roc.az.gov. Note that several third-party HVAC sites publish **incorrect** class codes (e.g. "CR-41," "CR-42"). Cite the ROC directly.

### Low confidence — define comprehensively, or avoid

- **"Kachina, AZ"** — ⚠ The highest-risk string in this project. Bare "Kachina" resolves to the Hopi/Puebloan katsina spirit and doll, a strong established entity. Never use the short form. Always **"Kachina Village"**, and reinforce with county, ZIP 86005, and nearby-landmark co-occurrence.
- **"Heat pump services"** — a generic commercial wrapper with no entity status. Decompose it into the actual service entities: installation, repair, replacement, maintenance.
- **Altitude derating at 6,798 ft** — the underlying engineering is real (air density at ~6,800 ft is roughly 78% of sea level, affecting CFM and delivered capacity), but consumer-facing content on it is nearly nonexistent. **This is the strongest content-gap opportunity in the entire analysis.** You would be teaching the topic rather than repeating it.
- **"24-hour emergency heat pump repair Kachina Village"** — a commercially valuable phrase with no entity backing. It earns relevance only through genuine local proof: response-time claims, service-area maps, real reviews.

---

## Incentive Landscape — accuracy warnings

This section changes fast and most competing pages are wrong. Verify everything before publishing.

| Program | Status as of July 2026 | Content implication |
|---|---|---|
| **Federal 25C tax credit** | **Expired.** Terminated by the One Big Beautiful Bill Act (P.L. 119-21, signed July 4, 2025) for property placed in service after Dec 31, 2025. No grandfathering. | Do **not** promote it. Publishing a "get $2,000 back" claim in 2026 is factually wrong and an E-E-A-T liability. Consider a short corrective section instead — competitors still have stale claims live. |
| **Federal 25D** (geothermal) | Expired on the same date | Same treatment |
| **Efficiency Arizona (HEAR)** | Active; up to $8,000 per heat pump for households under 150% AMI, running through Sept 30, 2031 or until funds are exhausted | The main live incentive. Lead with it, with the income qualification stated plainly. |
| **APS rebates** | Heat pump and AC rebates **discontinued** | Kachina Village is APS territory — do not promise APS rebate money. |
| **City of Flagstaff Home Weatherization & Energy Rebate** | Active, sliding income scale, up to ~$3,000 for a "Primary Source" heat pump | ⚠ **Explicitly limited to City of Flagstaff residents in existing homes.** Kachina Village is unincorporated Coconino County and residents are very likely **ineligible**. Confirm with the City's Sustainability Office and say so clearly. Getting this right is a strong differentiator — most regional content blurs "Flagstaff" into "Flagstaff area." |

---

## Content Recommendations

### Title / H1 must include

- **Heat pump** (central entity)
- **Kachina Village, AZ** (full place name — never "Kachina")
- A specific service predicate: *installation*, *repair*, or *replacement*

Suggested H1: **Heat Pump Repair & Installation in Kachina Village, AZ**
Suggested title tag: **Heat Pump Repair & Installation — Kachina Village, AZ | [Brand]**

### H2 topics, derived from secondary entities

1. **Do heat pumps actually work at 6,800 feet?** — the primary objection; answer with capacity-at-5°F numbers
2. **Sizing a heat pump for Kachina Village winters** — Manual J, balance point, altitude derating
3. **Cold-climate heat pumps vs. standard models** — the ccASHP distinction
4. **Heat pump or propane furnace? Dual-fuel explained** — the local incumbent comparison
5. **Snow, ice, and your outdoor unit** — elevated mounting, defrost drainage, what homeowners should clear
6. **Common heat pump repairs we see in Kachina Village** — frozen coils, refrigerant leaks, capacitors, aux-heat lockouts
7. **What "emergency heat" actually does to your APS bill**
8. **Heat pump rebates in Coconino County: what's still available in 2026**
9. **Our Kachina Village service area** — with Mountainaire, Munds Park, Forest Highlands, Flagstaff

### Entities to define on first mention

| Entity | Definition approach |
|---|---|
| Cold-climate heat pump | One sentence tying it to a measurable spec, not a marketing adjective: a heat pump engineered to hold most of its rated heating capacity at 5°F |
| Balance point | The outdoor temperature at which the heat pump's output exactly equals the home's heat loss — below it, backup heat starts |
| Auxiliary vs. emergency heat | Aux supplements the heat pump automatically; emergency shuts it off entirely and runs backup alone at much higher cost |
| HSPF2 | The heating-season efficiency score — the number that matters more than SEER2 at this elevation |
| Altitude derating | Thinner air at 6,800 ft carries less heat per cubic foot, so airflow and capacity must be corrected from sea-level ratings |

### Relationships to emphasize

| From | Predicate | To | How to express it |
|---|---|---|---|
| Kachina Village | sits at | 6,798 ft in IECC Zone 5B | Open with it — establishes local authority in the first 100 words |
| Cold-climate heat pump | retains capacity at | 5°F | Give a real number from a real model, not "works great in cold" |
| Snow | requires | elevated mounting | Frame as an install-quality tell readers can inspect themselves |
| Balance point | triggers | auxiliary heat | Connect directly to the APS bill — this is the reader's real question |
| Heat pump | replaces or supplements | propane furnace | Run the cost comparison honestly, including the case where dual-fuel wins |

### Schema recommendations

- `HVACBusiness` (subtype of `LocalBusiness`) with `areaServed` listing Kachina Village, Mountainaire, Munds Park, Forest Highlands, and Flagstaff
- `Service` entities for installation, repair, replacement, and maintenance, each with `serviceType` and `provider`
- `FAQPage` targeting the cold-weather objections above
- `GeoCoordinates` 35.0950, −111.6925 to reinforce place disambiguation

---

## Strategic Note

Kachina Village has roughly 3,300 residents. A standalone "heat pump services" money page here will never carry meaningful standalone search volume. Build this as a **service-area page inside a Flagstaff-region silo**, where it does three jobs: captures genuine long-tail local intent, feeds internal links to the stronger Flagstaff heat pump hub, and — most valuably — anchors topical authority around cold-climate, high-elevation heat pump content that Phoenix-oriented competitors cannot credibly produce.

The altitude and cold-climate angle is the moat. The city name is the door.

---

*Analysis generated by The SEO Pub Entity Extraction Tool*

---

**For more great AI SEO tools and tips visit The SEO Pub. Looking to hire an SEO consultant? Visit ClickedConsulting.com.**
