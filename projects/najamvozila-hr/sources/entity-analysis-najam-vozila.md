# Entity Analysis: "najam vozila" (Croatian market · short-term rental)

## Overview
- **Input**: `najam vozila` — Croatian market, short-term (rent-a-car) rentals
- **Central Entity**: **Najam vozila** (kratkoročni najam / rent-a-car) — the service of renting a vehicle without a driver for a short period
- **Total Entities Extracted**: 78
- **Validation Coverage**: ~42% high confidence · ~38% medium · ~20% low (see Validation Summary)
- **Validation method**: Live SERP checks (Croatian-language results), Wikipedia/Wikidata presence, regulatory sources (zakon.hr, narodne-novine.nn.hr, mint.gov.hr, psc.hr), and provider T&C pages (Carwiz, Avia, HAK Rent a Car, Enterprise, Loop, Connitor, Maximum, Car-Rent.hr)

### ⚠️ Critical SERP finding: "najam vozila" is a mixed-intent query in Croatia
The live Croatian SERP for `najam vozila` returns three different service types side by side:

| SERP slice | Examples observed | Intent |
|---|---|---|
| **Short-term rent-a-car** | Sixt, Hertz, Carwiz, RentX (najam-vozila.hr), vozi.hr, najamvozila.com | Daily/weekly rental, tourist + local |
| **Long-term / business rental** | Auto Hrvatska Mobility, Moove On (Grand Automotive), Hertz "dugoročni najam", Enterprise Flexi | 12+ month operational rental / fleet |
| **Rental with driver** | Lutar "najam vozila s vozačem" | Chauffeur / transfer (legally a *different* activity) |

**Implication:** Because you are targeting short-term rentals, your content must *actively disambiguate*. Google currently treats "najam vozila" as ambiguous between rent-a-car and operational leasing. Co-occurrence with **"rent a car"**, **"dnevni najam"**, **"cijena po danu"**, **"preuzimanje / povrat"**, **"zračna luka"**, **"depozit / kaucija"** signals the short-term entity; an explicit contrast section ("Kratkoročni vs. dugoročni najam") tells Google which meaning you serve.

### Terminology cluster (all map to the same Central Entity)
| Variant | Register | Where it dominates |
|---|---|---|
| **najam vozila** | neutral / commercial | Provider H1s, category pages (RentX, Hertz.hr, Avia) |
| **rent a car / rent-a-car** | industry vernacular, brand naming | Almost every Croatian provider's brand name (HAK Rent a Car, Avia Rent a Car, Carwiz rent a car, Connitor rent a car) |
| **najam automobila** | neutral | Enterprise.hr, rentalcars.com/hr, guides (aviokarte.com.hr) |
| **najam auta** | colloquial | Carwiz copy ("Najam auta je odlično iskustvo"), RentX |
| **iznajmljivanje vozila / automobila** | legal / formal | *Zakon o pružanju usluga u turizmu* ("usluge iznajmljivanja vozila (rent-a-car)") |
| **unajmljivanje / unajmiti** | user-side verb | Consumer guides |
| **kratkoročni najam vozila** | disambiguator | Mobile4U, Carwiz, HAK ("kratkoročne najmove") |

> Use "najam vozila" as the H1 anchor, "rent a car" as the co-primary synonym (it is what Croatians actually say and what brands are named), and "iznajmljivanje vozila" when referencing the law.

---

## Central Entity

**Entity**: Najam vozila (kratkoročni najam / rent-a-car)
**Type**: Service (Product-type entity) — a regulated tourism service in Croatia
**Definition**: A service in which a registered rent-a-car provider (*najmodavac*) makes a vehicle available to a customer (*najmoprimac*) **without a driver**, for a fee calculated per day, for a short period (typically 1–30 days), under a written rental agreement (*ugovor o najmu vozila*) and general terms (*opći uvjeti najma*). In Croatia it is legally classified as a *tourism service in a special form of tourist offer* under the **Zakon o pružanju usluga u turizmu** (NN 130/17, 25/19, 98/19, 42/20, 70/21), Article 95, and requires notification to the Ministry of Tourism and Sport and entry in the *Središnji registar*. It is distinct from **dugoročni najam / operativni leasing** (12+ months, business-oriented) and from **iznajmljivanje vozila s vozačem** (chauffeured hire, regulated separately under the *Zakon o prijevozu u cestovnom prometu*).
**Validation**: **High** — "Car rental" has an English Wikipedia article and Knowledge Graph entry; a Serbian-language Wikipedia article ("Iznajmljivanje automobila / rent-a-car") exists for the regional term; the Croatian SERP shows rich local-business results (Google Business Profiles with hours/addresses for airport branches), aggregator listings (DiscoverCars, Skyscanner, Rentalcars.com), and legal-definition results. Major providers (Sixt, Hertz, Enterprise, Avis, Europcar) all have Wikipedia pages.

**Why this is the Central Entity (tests applied):**
- *Removal test*: remove "najam" and you have just "vozila" (vehicles) — the topic collapses. ✔
- *Relationship test*: every other entity (price, deposit, insurance, airport, driver's licence, brands) is an attribute, condition, location, or provider *of* the rental. ✔
- *Query test*: the searcher wants to rent a vehicle, not to learn about vehicles or leasing. ✔
- *Coverage test*: "najam" appears in every section of any rental page (uvjeti najma, cijena najma, trajanje najma, produženje najma). ✔
- *Common-mistake check*: "vozilo" is the object, not the subject; "Hrvatska"/"Zagreb" is the location filter, not the subject; "kratkoročni" is a modifier.

---

## Entity Classification

### Primary Entities (salience 0.8–1.0)
| Entity | Type | Salience | Validation | Placement |
|---|---|---|---|---|
| **Najam vozila** (Central) | Service | 1.00 | High | Title, H1, meta, URL slug, first sentence, every H2, schema `name`/`serviceType` |
| **Rent a car / rent-a-car** | Concept (synonym / industry term) | 0.90 | High | Title (secondary), H1 or subtitle, first 100 words, brand mentions, schema `alternateName` |
| **Kratkoročni najam** (short-term rental) | Concept (disambiguating modifier) | 0.85 | Medium | First paragraph, dedicated H2 contrasting with dugoročni najam |
| **Hrvatska** (Croatia) — and city/airport modifiers | Location | 0.85 | High | Title, H1 (e.g. "u Hrvatskoj" / "Zadar"), meta, schema `areaServed` |
| **Vozilo / osobni automobil (kategorija M1)** | Product (object of rental) | 0.80 | High | H2 "Vozila u ponudi", fleet section, schema `Car`/`Vehicle` |

### Secondary Entities (salience 0.5–0.7)
| Entity | Type | Salience | Validation | Relationship to Central |
|---|---|---|---|---|
| Cijena najma / dnevna cijena (price per day) | Metric | 0.70 | High | Root attribute — the primary decision variable |
| Ugovor o najmu vozila (rental agreement) | Concept / Document | 0.70 | High | Legal instrument that constitutes the rental |
| Osiguranje vozila u najmu — CDW, TP, SCDW, kasko | Concept / Product | 0.70 | High | Governs najmoprimac liability; #1 confusion point |
| Franšiza / odbitna franšiza / učešće u šteti (excess) | Metric | 0.65 | Medium | Amount the renter pays before insurance applies |
| Depozit / kaucija / polog (deposit) | Metric | 0.65 | High | Pre-authorised on credit card; released after return |
| Opći uvjeti najma (general terms) | Document | 0.65 | Medium | Legally required in HR and/or EN under čl. 95 |
| Zračna luka (Zagreb, Split, Dubrovnik, Zadar, Pula, Rijeka, Osijek) | Location | 0.65 | High | Dominant pick-up location; each has Knowledge Panel |
| Preuzimanje i povrat vozila (pick-up & return) | Process | 0.60 | Medium | Defines start/end of rental; check-in/out report |
| Kreditna kartica (na ime glavnog vozača) | Product | 0.60 | High | Mandatory instrument for deposit at most providers |
| Vozačka dozvola (driver's licence) | Document | 0.60 | High | Eligibility requirement; validity period (1–2 years) |
| Sezona / sezonalnost (predsezona, glavna sezona, posezona) | Event / Concept | 0.60 | Medium | Drives price (July up to ~60% above March/April) and availability |
| Kategorije vozila (ekonomska, kompakt, SUV, karavan, kombi, kabriolet, luksuzna) | Product taxonomy | 0.60 | High | Determines price, deposit, franšiza |
| Prelazak granice / naknada za prelazak granice (cross-border) | Process / Metric | 0.55 | Medium | Rare attribute with high Croatian search demand (BiH, Slovenija, Crna Gora, Srbija) |
| Online rezervacija / besplatno otkazivanje | Process | 0.55 | Medium | Booking flow; conversion driver |
| Dugoročni najam (long-term rental) | Concept (contrast) | 0.50 | Medium | Must appear as *contrast* to disambiguate the SERP |
| Gorivo / politika goriva (puno–puno) | Concept | 0.50 | Medium | Root condition of return |
| Kilometraža (neograničena / ograničena) | Metric | 0.50 | Medium | Root pricing condition |
| Dodatni vozač (additional driver) | Person / role | 0.50 | Medium | Must be named in contract; extra fee |
| Mladi vozač / naknada za mladog vozača (18–21 / under 25) | Condition / Metric | 0.50 | Medium | Eligibility + surcharge (e.g. 50–62,50 € per rental) |
| Automatski mjenjač (automatic transmission) | Product attribute | 0.50 | High | Scarce in peak season; frequent filter |
| Najmoprimac / Najmodavac (renter / lessor) | Person / Organization roles | 0.50 | Medium | Contract parties — use to align with legal language |

### Supporting Entities (salience 0.2–0.4)
| Entity | Type | Salience | Validation | Role |
|---|---|---|---|---|
| Rent-a-car brands — global: Sixt, Hertz, Avis, Europcar, Enterprise, Budget | Organization | 0.40 | High | Competitor context; comparison content |
| Rent-a-car brands — Croatian: Carwiz, HAK Rent a Car, Avia Rent a Car, Autowill, Lutar, Loop, Euro Media (rent.hr), Connitor, Car-Rent.hr | Organization | 0.40 | Medium (GBP/local, no Wikipedia) | Local competitor set; define/link |
| Aggregators: DiscoverCars, Rentalcars.com, Skyscanner, Kayak | Organization | 0.35 | High | Compete for the same query; price-comparison context |
| Minimalna dob i vozačko iskustvo (min age 18/21; 1–2 yrs licence) | Condition | 0.40 | Medium | Eligibility rules |
| Osobna iskaznica / putovnica | Document | 0.40 | High | ID requirement |
| Međunarodna vozačka dozvola (IDP) | Document | 0.30 | High | For non-EU licence holders |
| Najam kombija / dostavnog vozila / putnički kombi 9 sjedala | Product | 0.40 | Medium | High-demand sub-category (selidbe, grupe) |
| Otkup franšize / puno pokriće (SCDW / excess buy-out) | Product | 0.40 | Medium | Rare attribute; upsell |
| Osiguranje stakala, guma i svjetala | Product | 0.30 | Medium | Rare add-on |
| Senior vozač (70+/71+) naknada | Condition / Metric | 0.30 | Low | Rare eligibility surcharge |
| Jednosmjerni najam (one-way rental) | Process | 0.35 | Medium | Rare attribute; fee |
| Dostava vozila na adresu / Meet & Greet | Process | 0.30 | Low | Service differentiator |
| Trajekt / otoci (ferry & island declaration) | Process / Location | 0.35 | High (Jadrolinija, islands) | Croatia-specific condition (must declare island use) |
| Asistencija na cesti 24/7 (HAK asistencija) | Service | 0.35 | High (HAK) | Included / optional add-on |
| Policijski zapisnik / prijava štete | Process / Document | 0.35 | Medium | Mandatory for any damage claim |
| Prometne kazne i naknada za obradu | Metric | 0.30 | Medium | Renter liability |
| Kašnjenje / grace period / penali za kašnjenje | Metric | 0.30 | Low | Return conditions |
| Produženje najma (extension) | Process | 0.30 | Low | Must be requested ≥24h ahead |
| Zamjensko vozilo (replacement vehicle) | Product | 0.30 | Medium | Provided on breakdown; also an insurance-claim sub-intent |
| Dječja sjedalica, GPS, lanci, zimske gume (dodatna oprema) | Product | 0.30 | High | Add-ons (child seat ~8–12 €/day) |
| Cestarina / ENC / HAC (tolls) | Concept / Organization | 0.30 | High | Driving-in-Croatia context |
| Zimska oprema (15.11.–15.4.) | Condition | 0.25 | High | Seasonal legal requirement |
| Naknada za čišćenje / zabrana pušenja | Metric | 0.25 | Low | Return conditions |
| Gubitak ključa / dokumenata vozila | Metric | 0.20 | Low | Penalty clause |
| PDV 25 % | Metric | 0.30 | High | Price display ("PDV uključen") |
| Debitna kartica / najam bez kreditne kartice / polog u gotovini | Product / Condition | 0.30 | Medium | Rare attribute; strong niche search intent |
| Najam vozila s vozačem (chauffeured) | Service (contrast) | 0.30 | High (legal definition) | Contrast entity — different legal activity |
| Car sharing (Spin City, Avant2Go) | Service (alternative) | 0.30 | Medium | Alternative for minute/hour rentals in Zagreb |
| Električno vozilo / hibrid u najmu | Product | 0.25 | High | Emerging fleet attribute |
| Kamper / najam kampera | Product | 0.20 | High | Adjacent rental category |
| Poslovnica / radno vrijeme (branch, opening hours) | Location attribute | 0.30 | High | Local-SEO signal; čl. 95 requires ≥1 poslovni prostor |

### Contextual Entities (salience 0.1–0.2)
| Entity | Type | Salience | Validation | Role |
|---|---|---|---|---|
| Zakon o pružanju usluga u turizmu (čl. 95) | Concept / Law | 0.20 | High | Governing statute — trust signal |
| Ministarstvo turizma i sporta / Središnji registar | Organization | 0.15 | High | Regulator & registry |
| Zakon o prijevozu u cestovnom prometu | Law | 0.15 | High | Defines chauffeured hire (contrast) |
| Zakon o obveznim odnosima (ugovor o najmu) | Law | 0.15 | High | General contract law basis |
| Zakon o sigurnosti prometa na cestama | Law | 0.15 | High | Driver/vehicle rules |
| Turistička inspekcija | Organization | 0.10 | Medium | Enforcement |
| Europski centar za potrošače Hrvatska (ECC) | Organization | 0.15 | High | Consumer-rights source for rental disputes |
| Zelena karta / Sustav zelene karte | Document / Concept | 0.20 | High | Cross-border insurance context (BiH in multilateral agreement) |
| HGK (Hrvatska gospodarska komora) | Organization | 0.10 | High | Industry body; rent-a-car fleets drive new-car sales |
| Osiguravatelji (Croatia osiguranje, Triglav, Laqo) | Organization | 0.10 | High | Insurance ecosystem |
| Turizam u Hrvatskoj / turistička sezona | Concept | 0.20 | High | Demand driver |
| Operativni leasing | Concept | 0.20 | High | Adjacent (long-term) category |
| NKD 77.11 (iznajmljivanje automobila) | Concept | 0.10 | Medium | Statistical classification |
| Uber / taksi / javni prijevoz (alternatives) | Service | 0.15 | High | Alternatives comparison |
| GDPR / zaštita osobnih podataka | Concept | 0.10 | High | Contract clause context |
| Rent a scooter / rent a boat | Service | 0.10 | Medium | Sibling tourism services in the same law |

---

## Attribute Analysis

### Root Attributes (present in EVERY short-term rental — cover all of these)
| Attribute | Why It's Essential | Content Requirement |
|---|---|---|
| **Cijena po danu** (daily rate) & dependence on duration/season | The primary decision variable; SERP shows "od X €/dan" everywhere | Show price ranges by category and season; state "PDV uključen"; explain that per-day price falls with longer rentals |
| **Trajanje najma** (rental period: 1 dan = 24 h, grace period, min/max) | Defines the service; grace period disputes are common | State day definition, grace period, late-return penalties (e.g. 50 €/day + daily rate) |
| **Kategorija / model vozila** | Determines price, deposit, franšiza | Fleet table by category (ekonomska → luksuzna), transmission, seats, fuel |
| **Mjesto preuzimanja i povrata** (pick-up/return location) | Airport vs. city vs. delivery; drives local intent | List branches with address, hours, airport code (ZAG, SPU, DBV, ZAD, PUY, RJK) |
| **Uvjeti za vozača** (min age, licence validity, experience) | Hard eligibility gate | State min age (18/21), licence held ≥1–2 yrs, IDP for non-EU |
| **Potrebni dokumenti** (osobna/putovnica, vozačka, kartica) | Every provider lists them | Checklist block |
| **Depozit / kaucija** (amount, card type, release time) | Blocks funds; biggest complaint source | Amount by category; credit card in main driver's name; release up to 30 working days |
| **Osiguranje i franšiza** (basic cover + excess) | Determines renter liability | Explain CDW/TP with franšiza, what is *excluded* (podvozje, gume, stakla, interijer, kvačilo, krivo gorivo) |
| **Politika goriva** (puno–puno) | Return condition | State policy and refuelling service fee |
| **Kilometraža** (limited/unlimited) | Pricing condition | State km included and per-km overage (e.g. 0,15 €/km) |
| **Ugovor o najmu + opći uvjeti** | Legal basis; required in HR/EN | Link to full T&C; summarise key clauses |
| **Odgovornost najmoprimca** (damage, fines, misuse) | Defines risk | Explain police-report requirement, fines processing fee, prohibited uses (taxi, off-road, towing) |

### Rare Attributes (present in SOME rentals — cover to differentiate and capture long-tail)
| Attribute | Differentiating Value | When to Include |
|---|---|---|
| Otkup franšize / SCDW / puno pokriće | Removes or reduces excess; key upsell | Insurance section; pricing table |
| Osiguranje stakala, guma, svjetala | Covers what basic CDW excludes | Insurance section |
| Naknada za mladog vozača (18–21) / senior (70+) | Eligibility surcharge; niche queries | Conditions section; FAQ |
| Dodatni vozač | Extra fee; must be on contract | Conditions section |
| Prelazak granice (EU vs. non-EU fee; forbidden countries) | Very high demand from Croatia (BiH, SLO, MNE, SRB); penalties for unauthorised crossing (e.g. 500 €) | Dedicated H2 + FAQ |
| Prijava korištenja trajekta / otoci | Croatia-specific; must inform provider | Conditions + island-travel guide |
| Jednosmjerni najam (one-way) | Fee-based; airport-to-airport routes | Locations section |
| Dostava vozila na adresu / Meet & Greet | Service differentiator at airports | Locations / service section |
| Automatski mjenjač | Scarce in peak season; strong filter | Fleet filters; early-booking advice |
| Kombi 9 sjedala / dostavni kombi | Distinct sub-category; scarce in season | Separate fleet page |
| Najam bez kreditne kartice / polog u gotovini / debitna kartica | Niche but strong intent; some providers only accept cash deposit | FAQ + conditions |
| Besplatno otkazivanje (e.g. ≥48 h / ≥3 days) | Conversion driver | Booking section |
| Dodatna oprema (dječja sjedalica, GPS, lanci, zimske gume, krovni nosač) | Add-on revenue | Extras table with per-day prices |
| Asistencija 24/7 & zamjensko vozilo | Trust signal | Service section |
| Električno / hibridno vozilo | Emerging differentiator | Fleet |
| Vozilo s kukom za vuču | Rare (HAK) | Fleet |
| Neograničena kilometraža | Marketed differentiator | Pricing |

### Unique Attributes (specific to ONE provider — cover for highest relevance in comparison content)
| Attribute | Unique To | Relevance Boost |
|---|---|---|
| Only-new-vehicle fleet + tow-hook vehicles + HAK 24/7 asistencija + vehicles tracked via HT telematics | HAK Rent a Car | Trust/authority association with Hrvatski autoklub |
| Cross-border fee 80 € (EU) / 100 € (non-EU); 500 € penalty for unauthorised crossing; airport branches 7–21 h; 100 € different-return-location fee | Carwiz | Concrete numbers for "prelazak granice" queries |
| Young-driver fee 62,50 €; replacement vehicle within 3 days of damage report; 100 € smoking fine | Avia Rent a Car | Concrete conditions for FAQ content |
| Debit cards accepted (except Maestro/Electron/prepaid); credit card only for 4×4/premium; full refund if cancelled ≥3 days ahead; Flexi 1–12-month rental | Enterprise Hrvatska | "bez kreditne kartice" and flexible-booking queries |
| 0,15 €/km overage; flat 45 € abroad fee; 30 % advance payment | Loop rent-a-car | Transparent-pricing angle |
| Cash deposit 300 €, no cards accepted, min age 21, licence ≥1 yr | Car-Rent.hr (Velika Gorica) | Sole "gotovinski polog" positioning |
| Young (18–21) and senior (71+) fee 50 € each; police report mandatory regardless of insurance | Connitor (Zadar/Zemunik) | Local Zadar relevance |
| Per-minute/hour electric car sharing at Zagreb Airport (13 dedicated bays) | Avant2Go | "najam po satu" alternative |

---

## Entity Relationships (EAV Triples)

| Entity | Attribute | Value |
|---|---|---|
| Najam vozila | is a | usluga u turizmu (posebni oblik turističke ponude) |
| Najam vozila | is also known as | rent a car / rent-a-car / najam automobila / najam auta |
| Najam vozila | regulated by | Zakon o pružanju usluga u turizmu, članak 95 |
| Najam vozila | requires provider to have | najmanje jedan poslovni prostor |
| Najam vozila | requires provider to publish | opći uvjeti najma na hrvatskom i/ili engleskom jeziku |
| Najam vozila | requires provider to notify | Ministarstvo turizma i sporta (upis u Središnji registar) |
| Najam vozila | is distinct from | dugoročni najam / operativni leasing |
| Najam vozila | is distinct from | iznajmljivanje vozila s vozačem (Zakon o prijevozu u cestovnom prometu) |
| Najam vozila | is formalised by | ugovor o najmu vozila |
| Najam vozila | has parties | najmodavac, najmoprimac |
| Najam vozila | priced per | dan (24 sata) |
| Najam vozila | price depends on | kategorija vozila, trajanje, sezona, lokacija, osiguranje |
| Najam vozila | requires | vozačka dozvola, osobna iskaznica/putovnica, kreditna kartica |
| Najam vozila | requires | depozit / kaucija (predautorizacija na kartici glavnog vozača) |
| Najam vozila | includes | obvezno osiguranje od odgovornosti prema trećim osobama |
| Najam vozila | typically includes | CDW s franšizom, TP |
| Najam vozila | may be upgraded with | otkup franšize (SCDW), osiguranje stakala i guma |
| Najam vozila | typically uses fuel policy | puno–puno |
| Najam vozila | typically starts at | zračna luka ili gradska poslovnica |
| Najam vozila | can be extended by | produženje najma (najava ≥24 h) |
| Najam vozila | may be limited by | kilometraža |
| Najam vozila | may incur | naknada za prelazak granice, naknada za mladog vozača, naknada za dodatnog vozača, jednosmjerna naknada |
| Najam vozila | prohibits | taksi prijevoz, off-road, vuča, auto-moto sport, vožnja pod utjecajem alkohola |
| Najam vozila | peaks in | glavna sezona (srpanj–kolovoz) |
| Kratkoročni najam | duration | 1 dan – ~30 dana |
| Dugoročni najam | duration | 12+ mjeseci; primarily pravne osobe |
| Franšiza | is | iznos štete koji plaća najmoprimac prije nego osiguranje preuzme ostatak |
| Franšiza | depends on | grupa / kategorija vozila |
| Franšiza | can be removed by | otkup franšize / puno pokriće |
| Depozit | held on | kreditna kartica na ime glavnog vozača |
| Depozit | released within | do 30 radnih dana (ovisno o banci) |
| CDW | covers | štetu na karoseriji do visine franšize |
| CDW | excludes | podvozje, gume, stakla, interijer, kvačilo, motor (krivo gorivo/manjak ulja) |
| TP | covers | krađu vozila |
| Mladi vozač | age range | 18–21 (some providers: under 25) |
| Mladi vozač | pays | naknada (e.g. 50–62,50 € per rental) |
| Prelazak granice | requires | prethodno odobrenje najmodavca + naknada |
| Prelazak granice | forbidden to | Kosovo, Ukrajina, Rusija, Moldavija (typical exclusions) |
| Trajekt / otoci | requires | prijava najmodavcu prilikom potpisivanja ugovora |
| Šteta na vozilu | requires | policijski zapisnik (bez obzira na osiguranje) |
| Zračna luka Zagreb (ZAG) | hosts | rent-a-car poslovnice + Avant2Go car sharing |
| Zračna luka Split (SPU) | located in | Kaštel Štafilić |
| Zračna luka Dubrovnik (DBV) | located in | Čilipi |
| Zračna luka Zadar (ZAD) | located in | Zemunik |
| Rent-a-car flota | drives | prodaja novih vozila u Hrvatskoj (HGK) |
| Car sharing (Spin City, Avant2Go) | priced per | minuta / sat / dan |

### Key Predicates
`unajmiti` · `iznajmiti` · `rezervirati` · `preuzeti` · `vratiti` · `produžiti` · `otkazati` · `platiti` · `položiti (depozit)` · `blokirati (sredstva)` · `pokriva` · `isključuje` · `zahtijeva` · `naplaćuje` · `dopušta` · `zabranjuje` · `uključuje` · `ovisi o` · `prijaviti (štetu / trajekt / prelazak granice)` · `prelaziti (granicu)` · `odgovara za` · `regulira`

Use these verbs in H2/H3 headings and FAQ questions ("Što uključuje cijena najma?", "Što osiguranje ne pokriva?", "Mogu li prijeći granicu unajmljenim vozilom?", "Kako se vraća depozit?").

---

## Co-Occurrence Map

### High Priority (same sentence / paragraph)
- **Najam vozila + rent a car** — synonym pairing; anchors the short-term meaning
- **Najam vozila + Hrvatska / [grad] / zračna luka** — location intent (query-driven)
- **Najam vozila + cijena po danu / od X €/dan** — price is the defining attribute
- **Najam vozila + kratkoročni + dugoročni** — disambiguation pair (must co-occur once, early)
- **Depozit / kaucija + kreditna kartica + glavni vozač** — definitional cluster
- **Osiguranje + franšiza + CDW / TP** — definitional cluster
- **Otkup franšize + puno pokriće / SCDW** — definitional
- **Mladi vozač + 18–21 + naknada** — definitional
- **Prelazak granice + naknada + odobrenje** — relational
- **Preuzimanje + povrat + gorivo (puno–puno)** — process cluster
- **Ugovor o najmu + najmoprimac + najmodavac** — legal cluster
- **Šteta + policijski zapisnik** — mandatory relationship

### Medium Priority (same section)
- Kategorije vozila + automatski mjenjač + broj sjedala + kombi 9 sjedala
- Zračna luka Zagreb + Split + Dubrovnik + Zadar + Pula + Rijeka (location set)
- Sezona + srpanj/kolovoz + rana rezervacija + dostupnost
- Vozačka dozvola + osobna iskaznica / putovnica + međunarodna vozačka dozvola + minimalna dob
- Dodatni vozač + naknada + upis u ugovor
- Trajekt + otoci + Jadrolinija + prijava
- Kilometraža + neograničena + 0,15 €/km
- Kašnjenje + grace period + penali + produženje najma
- Dodatna oprema: dječja sjedalica + GPS + lanci + zimske gume
- Brands: Sixt + Hertz + Avis + Europcar + Enterprise + Carwiz + HAK Rent a Car + Avia (comparison section)
- Aggregators: DiscoverCars + Rentalcars.com + Skyscanner (comparison section)

### Document Level
- Najam vozila + Zakon o pružanju usluga u turizmu + Ministarstvo turizma i sporta + Središnji registar (regulatory trust block)
- Najam vozila + najam s vozačem + Zakon o prijevozu u cestovnom prometu (contrast)
- Najam vozila + car sharing (Spin City, Avant2Go) + Uber + javni prijevoz (alternatives)
- Najam vozila + cestarina / ENC / HAC + zimska oprema (driving-in-Croatia context)
- Najam vozila + zelena karta + BiH / Crna Gora / Srbija (cross-border context)
- Najam vozila + Europski centar za potrošače (consumer rights)
- Najam vozila + PDV 25 % (price display)
- Najam vozila + turizam + turistička sezona + HGK (market context)

---

## Validation Summary

### High Confidence Entities (use freely; reference known attributes)
- **Najam vozila / rent a car / car rental** — English Wikipedia "Car rental"; regional Wikipedia (sr) "Iznajmljivanje automobila"; rich local SERP with Google Business Profiles, aggregators, and legal definitions
- **Zračna luka Zagreb (Franjo Tuđman), Split, Dubrovnik, Zadar (Zemunik), Pula, Rijeka (Krk), Osijek** — Knowledge Panels, IATA codes, Wikipedia
- **Sixt, Hertz, Avis, Europcar, Enterprise Rent-A-Car, Budget** — Wikipedia + Knowledge Panels
- **DiscoverCars, Rentalcars.com, Skyscanner, Kayak** — Wikipedia / brand panels
- **Zakon o pružanju usluga u turizmu; Zakon o prijevozu u cestovnom prometu; Zakon o obveznim odnosima; Zakon o sigurnosti prometa na cestama** — zakon.hr + Narodne novine (primary legal sources)
- **Ministarstvo turizma i sporta; HGK; HAK (Hrvatski autoklub); Europski centar za potrošače Hrvatska; Croatia osiguranje; Triglav** — Wikipedia / official domains / Knowledge Panels
- **Kreditna kartica, vozačka dozvola, međunarodna vozačka dozvola, putovnica, osobna iskaznica, PDV** — universal entities
- **Automatski mjenjač, SUV, kombi, kabriolet, električno vozilo, kamper** — product entities with Wikipedia articles
- **Zelena karta (Sustav zelene karte), cestarina / ENC / HAC, Jadrolinija, zimska oprema** — Wikipedia / official sources
- **Hrvatska + all cities (Zagreb, Split, Dubrovnik, Zadar, Pula, Rijeka, Šibenik, Rovinj, Poreč, Makarska, Umag, Opatija, Osijek, Brač)** — Knowledge Panels

### Medium Confidence Entities (use; define clearly on first mention)
- **Kratkoročni najam / dugoročni najam** — widely used commercial terms; no dedicated Wikipedia; SERP shows category pages (Mobile4U, Carwiz, Hertz, Enterprise Flexi)
- **Franšiza / odbitna franšiza / učešće u šteti** — insurance term with Croatian coverage (Triglav guide, provider T&Cs); ambiguous with "franchise" (business) — define on first use
- **CDW, TP, SCDW, otkup franšize, puno pokriće** — industry acronyms; present in Croatian guides (aviokarte.com.hr, Triglav) — expand acronyms
- **Depozit / kaucija / polog** — synonyms used interchangeably by providers — pick one and gloss the others
- **Opći uvjeti najma; ugovor o najmu vozila; najmoprimac / najmodavac** — legal terms present in every T&C and in čl. 95 — define once
- **Sezona / predsezona / posezona** — tourism concept, no dedicated entity page for rental pricing
- **Prelazak granice / naknada za prelazak granice** — clear provider coverage, no encyclopedic entity
- **Mladi vozač, dodatni vozač, minimalna dob, vozačko iskustvo** — consistent across T&Cs, no encyclopedic entity
- **Croatian providers: Carwiz, HAK Rent a Car, Avia Rent a Car, Autowill, Lutar, Loop, Euro Media/rent.hr, Connitor, Car-Rent.hr** — strong local presence (GBP, own domains), no Wikipedia; treat as local organisations with `LocalBusiness`/`AutoRental` schema
- **Spin City, Avant2Go** — active Croatian car-sharing services (Zagreb Airport page confirms Avant2Go); no Wikipedia
- **Najam kombija / kombi 9 sjedala, jednosmjerni najam, zamjensko vozilo, policijski zapisnik, prometne kazne** — commercially established, define in context
- **Središnji registar za ugostiteljsku djelatnost i usluge u turizmu; turistička inspekcija; NKD 77.11** — official but niche

### Low Confidence Entities (define comprehensively; you are teaching Google)
- **Naknada za senior vozača (70+/71+)** — provider-specific, inconsistent thresholds
- **Grace period / penali za kašnjenje / produženje najma** — provider-specific clauses
- **Dostava vozila na adresu / Meet & Greet** — service names, not entities
- **Naknada za čišćenje, zabrana pušenja, gubitak ključa / dokumenata** — clause-level terms
- **Najam bez kreditne kartice / polog u gotovini** — real search intent but no entity recognition; build a dedicated definitional section/FAQ
- **Vozilo s kukom za vuču** — provider-specific
- **Otkup franšize** (as a standalone phrase) — define alongside SCDW

**Action items:**
- Expand every acronym on first use: *CDW (Collision Damage Waiver – osiguranje od štete na vozilu s franšizom)*, *TP (Theft Protection – osiguranje od krađe)*, *SCDW (Super CDW – otkup franšize)*.
- Define "franšiza" immediately as an insurance excess to avoid the business-franchise meaning.
- Always pair "najam vozila" with "rent a car" and either "kratkoročni" or "po danu" in the first 100 words so the page is not classified as leasing content.
- Give Croatian providers full names + city in the first mention (e.g. "Carwiz rent a car (Zagreb, Split, Dubrovnik, Rijeka, Pula)").

---

## Content Recommendations

### Search intent & SERP shape (for planning)
- **Intent**: predominantly **commercial/transactional with strong local modifier**; a secondary informational layer exists (guides on insurance, conditions, driving in Croatia).
- **SERP composition observed**: provider sites (global + Croatian), aggregators, long-term rental/leasing pages (noise for you), one chauffeur page, and consumer guides (aviokarte.com.hr, Triglav).
- **Local dominance**: city and airport pages ("najam vozila Zagreb", "rent a car Zračna luka Split") are the practical ranking unit — plan a **city/airport silo** under a national hub.
- **Bilingual reality**: providers publish HR + EN (the law requires terms in HR and/or EN); use `hreflang` for hr/en and keep entity names consistent across both.

### Title / H1 Must Include
- **Najam vozila** (Central Entity)
- **Rent a car** (co-primary synonym — in title or H1 subtitle)
- **Hrvatska** or the specific **city / zračna luka** (location modifier)
- A short-term signal: **po danu**, **kratkoročni**, or **od X €/dan**

Example H1s:
- *Najam vozila Zadar – Rent a car već od 29 €/dan (zračna luka Zemunik i centar)*
- *Rent a car Hrvatska | Kratkoročni najam vozila bez skrivenih troškova*

### H2 Topics (based on Secondary entities)
1. **Cijene najma vozila po danu** — po kategoriji i sezoni, PDV uključen, što je uključeno u cijenu
2. **Vozila u ponudi** — ekonomska, kompakt, SUV, karavan, kombi (9 sjedala), kabriolet, automatski mjenjač, električna
3. **Uvjeti najma** — minimalna dob, vozačka dozvola, dokumenti, mladi i dodatni vozač
4. **Depozit (kaucija) i kreditna kartica** — iznos po kategoriji, predautorizacija, povrat depozita
5. **Osiguranje i franšiza** — CDW, TP, otkup franšize (SCDW), što nije pokriveno, policijski zapisnik
6. **Preuzimanje i povrat vozila** — zračne luke (ZAG, SPU, DBV, ZAD, PUY, RJK), poslovnice, radno vrijeme, dostava, meet & greet, gorivo puno–puno
7. **Prelazak granice unajmljenim vozilom** — BiH, Slovenija, Crna Gora, Srbija; naknada; zabranjene zemlje; zelena karta
8. **Otoci i trajekti** — prijava korištenja trajekta, Jadrolinija
9. **Kratkoročni vs. dugoročni najam** — kada se isplati rent a car, a kada dugoročni najam / leasing (explicit disambiguation)
10. **Rezervacija i otkazivanje** — online rezervacija, besplatno otkazivanje, rana rezervacija u sezoni
11. **Dodatna oprema** — dječje sjedalice, GPS, lanci, zimske gume
12. **Vožnja u Hrvatskoj** — cestarina/ENC, zimska oprema, prometne kazne
13. **Alternative** — car sharing (Spin City, Avant2Go), najam s vozačem, taksi/Uber
14. **Često postavljana pitanja (FAQ)** — schema-marked

### Entities to Define (first mention)
- **Najam vozila (rent a car)**: "usluga iznajmljivanja vozila bez vozača na dnevnoj osnovi, regulirana Zakonom o pružanju usluga u turizmu" — establishes legal identity and short-term meaning.
- **Franšiza (odbitna franšiza / učešće u šteti)**: "iznos štete koji najmoprimac snosi sam prije nego osiguranje pokrije ostatak" — pre-empts confusion with business franchising.
- **CDW / TP / SCDW**: expand each acronym in Croatian on first use.
- **Depozit (kaucija)**: "iznos privremeno blokiran na kreditnoj kartici glavnog vozača kao jamstvo".
- **Kratkoročni najam**: "najam od jednog dana do oko mjesec dana, naplaćen po danu" vs. **dugoročni najam**: "12 i više mjeseci, uglavnom za tvrtke".
- **Mladi vozač**: state the age band your provider uses (18–21 or <25) — thresholds vary.
- **Prelazak granice**: "korištenje vozila izvan Hrvatske uz prethodno odobrenje i naknadu".

### Relationships to Emphasize
- **Najam vozila → priced per → dan**: "Cijena najma vozila obračunava se po danu (24 sata) i ovisi o kategoriji, trajanju i sezoni."
- **Najam vozila → requires → kreditna kartica + depozit**: "Za najam vozila potrebna je kreditna kartica na ime glavnog vozača na kojoj se blokira depozit."
- **Osiguranje → includes → franšiza; otkup franšize → removes → franšiza**: "Osnovno osiguranje (CDW) uključuje franšizu, koju možete ukloniti otkupom franšize."
- **Najam vozila → is distinct from → dugoročni najam**: "Za razliku od dugoročnog najma, rent a car je namijenjen kratkim razdobljima od jednog dana."
- **Prelazak granice → requires → odobrenje + naknada**: "Unajmljenim vozilom možete prijeći granicu uz prethodnu najavu i plaćanje naknade."
- **Šteta → requires → policijski zapisnik**: "Svaku štetu na vozilu potrebno je prijaviti policiji, inače osiguranje ne vrijedi."
- **Najam vozila → regulated by → Zakon o pružanju usluga u turizmu (čl. 95)**: use as a trust block near the footer / "O nama".
- **Zračna luka → is pick-up location of → najam vozila**: one page per airport with address, hours, and code.

### Schema & technical hints
- Use `AutoRental` (subtype of `LocalBusiness`) for each poslovnica with `address`, `openingHoursSpecification`, `areaServed`, `priceRange`; `Service` with `serviceType: "najam vozila"` and `alternateName: "rent a car"`; `Product`/`Car` for fleet items; `FAQPage` for uvjeti; `Offer` with `priceCurrency: EUR`.
- Keep entity names identical in HR and EN versions (`hreflang`), e.g. "Zračna luka Split (SPU)" ↔ "Split Airport (SPU)".
- Internal-link the disambiguation section to (or from) any long-term/leasing page so Google sees both meanings served on separate URLs.

---

*Analysis generated by The SEO Pub Entity Extraction Tool — 2026-09-08*

---

**For more great AI SEO tools and tips visit The SEO Pub. Looking to hire an SEO consultant? Visit ClickedConsulting.com.**
