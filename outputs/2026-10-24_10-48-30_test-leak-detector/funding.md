# Funding report: self-calibrating acoustic leak detection for district heating pipes

*Prepared by Aalto Innovation funding advisory, 24 October 2026. The disclosure is confidential. All searches used only general terms such as "district heating leak detection" and "acoustic leak detection".*

---

## ⚠️ Act on this first: the patent filing, before any money

- **The conference paper is the biggest risk.** It was submitted on 15 Sept 2026 and the decision is due in December 2026. Europe and Finland have no grace period. If the paper or a preprint becomes public before a patent application is filed, the invention can no longer be patented. Most funders on this list (R2B, EIC, investors) will expect protectable IP.
  - File a priority application (Finnish PRH or EP) before acceptance and camera-ready, and in any case before anything is published.
  - Check now whether the conference makes submissions public (some review systems are open) and whether a preprint exists.
- **Do a patent search before filing.** The team has not done one, and my quick searches found closely related documents:
  - A US patent titled *"Method for acoustic leak detection in a district heat conduction network"* ([USPTO](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12687263))
  - A Kamstrup application on monitoring district heating pipe condition, EP4760155A1 ([listing](https://eureka.patsnap.com/patent/EP4760155A1))
  - An EU-funded "Passive **and Active** Acoustic Leak Detection" project from 2018 (PAALD, section 4)

  The novelty claimed (active pulses that measure sound speed and damping per pipe section) has to be tested against these.
- **Clear up who owns the IP.** Results come from a Research Council of Finland project, and the energy company gave access to its network. Check the terms of that access agreement. R2B requires that Aalto can transfer the rights to whoever commercialises them.

---

## 1. Where the invention stands and what the next step needs

**Maturity: about TRL 5, approaching 6.** The method works on a lab rig (DN100, 40 m, 0.5 l/min leaks, under 1 m error). It has also had one field trial in a relevant environment: 2.3 km, 6 sensors, 4 months, 3 known leaks found, 2.1 m mean error against 9.4 m for a manual correlator, 2 false alarms. The hardware is a prototype built from off-the-shelf parts (about €120 in parts per sensor), and battery life is estimated, not measured.

**Gaps to close before this is a product or a company:**

| Gap | What's needed |
|---|---|
| Validation at scale | A pilot of roughly 20–50 km with 50–150 sensors, covering a full year (heating and summer seasons, since water temperature changes sound speed), several pipe sizes and ages, and ideally 2 or more operators |
| Robustness | Fewer false alarms (pump stations and other noise sources), measured battery life, data transmission from underground valve chambers, a ruggedised enclosure for wet and hot conditions |
| IP | Patent search, priority filing, then a PCT application within 12 months |
| Market | Customer discovery with 10–20 district heating operators in Finland and the Nordics; pricing model (hardware plus monitoring service); position against alarm-wire systems such as LOGSTOR Detect, drones and water-leak logger vendors |
| Team | Nobody has business experience. A commercial lead or co-founder is needed. The doctoral researcher (PhD expected 2027) is the likely founder, and the staff scientist would advise |

**What the next step needs:**
- **Money:** about €600–800k for an 18–24 month commercialisation project. That breaks down roughly as:
  - 2–3 person-years of engineering and research
  - a commercialisation lead
  - €60–100k for sensors and installation
  - IP, market work and travel
- **Partners:** the host energy company (in-kind support such as network access, installation staff and leak verification, and ideally a letter of intent) plus a second operator.
- **Time:** about 2 years to a spin-off that is ready to invest in (late 2028).

---

## 2. Best-fitting funding now

| # | Funder / programme | Typical size | Deadline | Eligibility | Fit | Link |
|---|---|---|---|---|---|---|
| **1** | **Business Finland – Research to Business (R2B)** | Total project cost about €400–800k; grant covers 80% (Aalto pays 20%); 1.5–2 years | Autumn 2/2026 call closed 16 Sept 2026. **Next call expected spring 2027.** The 1/2026 call ran 1 Dec 2025 to 4 Mar 2026, so 1/2027 may open around Dec 2026 with a deadline around Mar 2027. *Not confirmed, check with BF* | Research organisations only, alone or in a consortium. At least 40% of costs must go to commercialisation preparation. The applicant must be able to transfer rights to the party that commercialises | **Excellent.** Built for exactly this stage: TRL 5–6, an operator pilot, spin-off preparation, and money for a business lead | [Call 1/2026](https://www.businessfinland.fi/en/services/funding/calls/2026/research-to-business--funding-call-12026/) · [Call 2/2026](https://www.businessfinland.fi/en/services/funding/calls/2026/r2b-funding-call-2-2026/) · [R2B overview](https://www.businessfinland.fi/en/services/funding/funding-services/cooperation-between-companies-and-research-organisations/research-to-business/) · [R2B Clinic](https://www.businessfinland.fi/en/whats-new/Events/2026/research-to-business-clinic2/) |
| **2** | **Pilot co-funding from the host energy company** (bilateral research and pilot agreement) | In-kind (network, staff, leak verification) plus possibly cash for sensors | Talks now; pilot planned for 2027 | No formal eligibility | **High.** The company asked for a larger pilot itself. Its in-kind support and a letter of intent make the R2B application much stronger. Agree IP terms before the pilot starts | n/a (contract handled by Aalto Innovation / Research Services) |
| **3** | **Business Finland – research organisations and SMEs call** (as reported in search results) | Research-organisation project. Size not confirmed | **18 Dec 2026** (from search results, **verify**) | Only research organisations apply; the aim is to bring SMEs into research cooperation | **Medium.** Only useful if a Finnish SME partner can be found quickly (for example a sensor, IoT or service company). The large energy company probably doesn't count as an SME. The deadline is tight | [BF company–research cooperation](https://www.businessfinland.fi/en/services/funding/funding-services/cooperation-between-companies-and-research-organisations/) |
| **4** | **Fortum and Neste Foundation** (doctoral grant) | Up to about €27k/year plus about €3k for costs (amount needs checking) | Spring 2027 round (opens in April, decision in June). *Check* | Full-time doctoral researcher supervised at a Finnish institution; energy-sector topics | **Good, as a bridge** to fund the founder-to-be through PhD completion in 2027 | [research.fi call](https://research.fi/en/results/funding-call/13959) · [guide](https://www.european-funding-guide.eu/fi-en/scholarship/fortum-neste-foundation) |
| **5** | **Tekniikan edistämissäätiö (TES)** | Up to about €26.6k for 12 months, or about €2.2k/month (third-party source) | Usually opens in January and closes early February. *2027 dates not confirmed* | Doctoral students at Finnish universities in technology | **Good, as a bridge.** Same purpose as option 4 | [Guide page](https://www.european-funding-guide.eu/fi/node/74544) · tekniikanedistamissaatio.fi |
| **6** | **EIC Accelerator** (later, for the spin-off) | Grant up to about €2.5M plus equity | Short proposals can be sent at any time. A secondary source gives 3 Feb 2027 as the first 2027 full-proposal cut-off (*verify in the EIC Work Programme 2027*) | An SME, or people who intend to found one. Requires at least TRL 5 completed | **Not yet.** Needs a company, a team and investor interest. Realistic target is 2028–29 | [Topic HORIZON-EIC-2026-ACCELERATOR-01](https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/opportunities/topic-details/horizon-eic-2026-accelerator-01) |

**Checked and ruled out (or poor fit):**
- **Research Council of Finland Proof of Concept.** The 2026 call closed on 6 May 2026, and **there will be no call in 2027**. It is also only open to PIs whose RCF funding ended 2025–2026, while this project runs to 2027. ([call page](https://www.aka.fi/en/research-funding/apply-for-funding/calls-for-applications/apply-now2/2026-rcf-proof-of-concept-funding/), [press release](https://www.aka.fi/en/about-the-rcf/whats-new/press-releases/2026/research-council-of-finland-gearing-spring-2026-proof-of-concept-call-towards-national-strategic-choices/))
- **EIC Transition.** The usual deadline is around September, and grants go up to €2.5M. Applicants must build on results from eligible EU projects (EIC Pathfinder, ERC Proof of Concept and similar), so a national RCF project most likely doesn't qualify. *Confirm with the EIC national contact point.* ([EIC news](https://eic.ec.europa.eu/news/record-number-proposals-submitted-eic-transition-call-2025-09-29_en))
- **HORIZON-BRIDGING-2027-01-12**, AI-driven digital platforms for the energy system. One €15M project, electricity flexibility, 6+ countries, deadline 16 Feb 2027. Wrong focus and wrong scale. ([link](https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/opportunities/topic-details/horizon-bridging-2027-01-12))
- **EIC Pre-accelerator (Widening).** Finland is not a Widening country.
- **No open EU call targets district heating network monitoring.** The 2027 Cluster 5 building and heat calls (opening May 2027) cover waste heat and renovation, not network leak detection.

---

## 3. Upcoming options to prepare for

| When | Option | Note / link |
|---|---|---|
| 19 Nov 2026 | EIC 2027 Work Programme info day | Learn the 2027 Accelerator and Transition rules ([source](https://ufukavrupa.org.tr/en/node/6624)) |
| 18 Dec 2026 | BF research organisations and SMEs call | Only if an SME partner is found (*verify*) |
| ~Dec 2026 to ~Mar 2027 (expected) | **Business Finland R2B 1/2027** | Main target. Dates not yet announced; watch the [BF calls page](https://www.businessfinland.fi/en/services/funding/) |
| Jan–Feb 2027 (expected) | Tekniikan edistämissäätiö grants | For the doctoral researcher |
| Apr 2027 (expected) | Fortum and Neste Foundation | For the doctoral researcher |
| 2027 (cut-offs every 2–3 months) | EIC Accelerator | Only after the company exists ([topic](https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/opportunities/topic-details/horizon-eic-2026-accelerator-01)) |
| Continuous, since 1 Sept 2026 | **Business Finland Sprint** (small companies aiming at rapid international growth) | For the spin-off after founding. Startups under 5 years old without earlier BF funding. Amount not confirmed. Book a meeting with BF before applying ([call](https://www.businessfinland.fi/en/services/funding/calls/2026/ongoing-sprint-grant-funding/), [news](https://www.businessfinland.fi/en/whats-new/news/2026/sprint-funding-to-encourage-ambitious-rd-continues/)). The older Tempo programme has closed ([BF](https://www.businessfinland.fi/en/services/funding/funding-services/tempo-funding/)) |
| Rolling | EIT InnoEnergy Highway (acceleration support in exchange for equity) | For an energy start-up after founding. Current terms not confirmed ([IEA summary](https://www.iea.org/policies/15240-eit-innoenergy-highway)) |
| Rolling | Aalto Startup Center (Research-to-Business track, Business Generator) | Coaching and investor contacts for the founder ([services](https://startupcenter.aalto.fi/our-services)) |
| After founding | Pre-seed and seed investors | Finnish deep-tech and energy-tech investors. Approach once the patent is filed and the pilot has run |

---

## 4. Who has been funded for similar work

**Closest to this invention (possible competitors, and prior art to check):**

| Project | Funder | Period | Amount | Relevance | Link |
|---|---|---|---|---|---|
| **Jensen Predictive Maintenance (JPM)**: online monitoring and fault location for district heating pipes | EC (SME Instrument Phase 1) | 2015–2016 | €50,000 | **Direct competitor or possible partner.** Appears to be the Swedish acoustic-listening consultancy that is developing a permanent monitoring system ([B&K article](https://www.bksv.com/de/knowledge/blog/perspectives/savings-in-the-pipeline)) | [CORDIS search](https://cordis.europa.eu/search?q=%27Jensen%20Predictive%20Maintenance%27) |
| **PAALD**: Passive and Active Acoustic Leak Detection (oil and liquid pipelines, US company) | EC | 2018 | €50,000 | **Prior art for the "active" idea.** Must be covered in the patent search | [CORDIS search](https://cordis.europa.eu/search?q=PAALD%20acoustic%20leak) |
| **PIPESCANNER**: condition assessment of metal pipes in district heating and drinking water networks | EC (SME Instrument) | 2020 | €50,000 | Adjacent competitor (pipe condition, not leak position) | [CORDIS search](https://cordis.europa.eu/search?q=PIPESCANNER) |
| **WATER-LDL**: advanced acoustic leak detection and localisation in ageing water networks | EC | 2025–2027 | €276,188 | Academic peer in water networks; possible collaborator for a later EU consortium | [CORDIS search](https://cordis.europa.eu/search?q=WATER-LDL) |
| **RAINDROP**: acoustic sensing for leaks in water mains (EP/V028111/1) | UKRI | 2021–2024 | £702,767 | Leading UK academic group; possible partner | [UKRI GtR](https://gtr.ukri.org/projects?ref=EP%2FV028111%2F1) |
| **L-BAS** (259190) and 206972: active acoustic leak detection, subsea | Research Council of Norway | 2011–2021 | n/a | More prior art on active acoustics | [RCN project bank](https://prosjektbanken.forskningsradet.no/en/project/FORISS/259190) |
| Acoustic sensing on gas and oil pipelines (2108480) | UKRI | 2018–2022 | n/a | Adjacent | [UKRI GtR](https://gtr.ukri.org/search/project?term=2108480) |

**District heating digitalisation (possible partners and channels):**

| Project | Funder | Amount | Note | Link |
|---|---|---|---|---|
| AI-DTDH: AI digital twin and GIS for district heating (IP-2025-02-6488) | Croatian Science Foundation | €199,790 (2025–2028) | Predictive maintenance using sensor data. Possible data or research partner | [HRZZ](https://hrzz.hr/en/) |
| DHC Academy (101186097): skills for smart district heating and cooling | EC | €1,498,720 | Network for reaching European operators | [CORDIS](https://cordis.europa.eu/project/id/101186097) (*check: this may be an Erasmus+ project*) |
| THERMO-S ARE (Ngenic and Jämtkraft), digital district heating | Swedish Energy Agency | SEK 1.36M | Swedish operator open to digital pilots | [Energimyndigheten project database](https://www.energimyndigheten.se/forskning-och-innovation/projektdatabas/) |
| Service life of district heating pipes, phases 1–2; carbon-fibre relining (SEK 3.3M) | Swedish Energy Agency | SEK 0.25–3.3M | Swedish pipe-ageing research groups | same database |
| Aarhus University self-powered sensors in district heating pipes | Innovation Fund Denmark | n/a | **Watch closely**: a close neighbour (low-power sensors for district heating) and a possible partner | [AU news](https://ingenioer.au.dk/en/current/news/view/artikel/smart-sensors-to-provide-real-time-data-for-optimized-operation-of-the-district-heating-grid) |
| KICT (Korea): acoustic emission sensors with machine learning on a pilot district heating line | Korean public funding | n/a | Still needed field validation, which this team already has (an advantage) | [TechXplore](https://techxplore.com/news/2022-12-diagnosis-technology-leaks-district-pipes.amp) |

**Commercial landscape:**
- **LOGSTOR Detect** monitors alarm wires around the clock. It is the incumbent the invention would complement, especially where wires are broken or missing ([LOGSTOR](https://www.logstor.com/products/detect)).
- **Kamstrup** has a patent application on monitoring pipe condition using heat-meter data ([EP4760155A1](https://eureka.patsnap.com/patent/EP4760155A1)).
- **Copenhagen utility HOFOR** combines acoustics, drones and alarm wires ([article](https://doi.dk/en/innovation/artikel/hofor-bruger-ny-teknologi-til-at-opdage-utaetheder-i-fjernvarmeroer)). It is a possible second pilot customer.

**Finnish picture:** a search of Research Council of Finland projects found no projects on district heating leak detection. There seems to be little direct competition in Finnish public research, which supports a "Finnish first mover" story in R2B.

---

## 5. Recommended funding path

**Before Christmas 2026 (must be in place first):**
1. **Invention assignment to Aalto, IP clearance, and a patent search followed by a priority filing**, all before the conference paper becomes public. Owner: Aalto Innovation with the inventors.
2. **A letter of intent and pilot term sheet with the host energy company**: network size for the 2027 pilot, in-kind contribution, how leaks are verified, and IP terms.
3. **About 10 interviews with other operators** (Finland, Sweden, Denmark) to show demand beyond one customer. A second operator willing to join the pilot would be ideal.
4. **Name a commercialisation lead**: an experienced business person (contact through Aalto Startup Center or an entrepreneur-in-residence), budgeted inside R2B.
5. Check whether the current RCF project can cover a small extension of the field trial during 2027 within its scope. This would fill the gap until R2B money arrives.

**Optional, mid-December 2026:** apply to the BF research organisations and SMEs call (18 Dec, *verify*), but only if a suitable SME partner appears.

**Jan–Apr 2027:**
- **Submit to Business Finland R2B 1/2027.** Budget about €600–750k for 24 months, with BF paying 80% and Aalto 20%. Use the R2B Clinic and talk to BF before the call opens.
- **The doctoral researcher applies to TES (Jan–Feb) and the Fortum and Neste Foundation (April)** to fund finishing the PhD in 2027.

**Mid-2027:** expected R2B decision. If funded, start around Aug–Sept 2027 so the large pilot covers the 2027–28 heating season and summer 2028. If R2B isn't funded, revise and resubmit in the autumn 2027 call. Meanwhile run a smaller pilot funded by the energy company.

**2027–2028 (R2B project):** a multi-season pilot with 1–2 operators, an industrial-grade sensor, measured battery life, lower false-alarm rate, PCT filing, business model and pricing, founding team, and talks with investors.

**Late 2028 to 2029 (spin-off):** found the company with a licence or assignment from Aalto. Then:
- Business Finland **Sprint** (continuous call)
- **Pre-seed round** (Finnish deep-tech and energy investors), and possibly **EIT InnoEnergy**
- The first paid deployments
- **EIC Accelerator** short proposal → full proposal once there is investor interest and paying pilots (2029)

**Points to confirm with funders:**
- R2B 1/2027 dates and budget
- The BF 18 Dec 2026 call: name, scope, and whether an SME partner is required
- The EIC 2027 cut-offs (Work Programme 2027)
- Sprint grant size
- 2027 dates for TES and Fortum & Neste
- That EIC Transition is not open to results from an RCF project

---

### Sources
- [EIC Accelerator 2026 topic](https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/opportunities/topic-details/horizon-eic-2026-accelerator-01) · [HORIZON-BRIDGING-2027-01-12](https://ec.europa.eu/info/funding-tenders/opportunities/portal/screen/opportunities/topic-details/horizon-bridging-2027-01-12)
- [BF R2B 1/2026](https://www.businessfinland.fi/en/services/funding/calls/2026/research-to-business--funding-call-12026/) · [BF R2B 2/2026](https://www.businessfinland.fi/en/services/funding/calls/2026/r2b-funding-call-2-2026/) · [R2B overview](https://www.businessfinland.fi/en/services/funding/funding-services/cooperation-between-companies-and-research-organisations/research-to-business/) · [R2B Clinic](https://www.businessfinland.fi/en/whats-new/Events/2026/research-to-business-clinic2/) · [BF funding services 2026](https://www.businessfinland.fi/en/whats-new/news/2026/what-do-business-finlands-funding-services-look-like-at-the-beginning-of-2026/) · [BF cooperation services](https://www.businessfinland.fi/en/services/funding/funding-services/cooperation-between-companies-and-research-organisations/)
- [BF Sprint call](https://www.businessfinland.fi/en/services/funding/calls/2026/ongoing-sprint-grant-funding/) · [Sprint continues](https://www.businessfinland.fi/en/whats-new/news/2026/sprint-funding-to-encourage-ambitious-rd-continues/) · [Tempo closed](https://www.businessfinland.fi/en/services/funding/funding-services/tempo-funding/)
- [RCF PoC 2026](https://www.aka.fi/en/research-funding/apply-for-funding/calls-for-applications/apply-now2/2026-rcf-proof-of-concept-funding/) · [RCF PoC press release](https://www.aka.fi/en/about-the-rcf/whats-new/press-releases/2026/research-council-of-finland-gearing-spring-2026-proof-of-concept-call-towards-national-strategic-choices/)
- [EIC Accelerator 2027 (Deloitte)](https://www.deloitte.com/mt/en/services/tax/perspectives/gi3/eic-accelerator-2027-call.html) · [EIC Accelerator FAQ](https://eic.ec.europa.eu/eic-frequently-asked-questions/faqs-eic-accelerator_en) · [EIC Transition news](https://eic.ec.europa.eu/news/record-number-proposals-submitted-eic-transition-call-2025-09-29_en) · [EIC 2027 draft WP (TR)](https://ufukavrupa.org.tr/tr/haberler/eic-2027-taslak-calisma-programi-yayinlandi)
- [EIT InnoEnergy Highway (IEA)](https://www.iea.org/policies/15240-eit-innoenergy-highway) · [Aalto Startup Center](https://startupcenter.aalto.fi/our-services)
- [Fortum and Neste Foundation (research.fi)](https://research.fi/en/results/funding-call/13959) · [Fortum and Neste guide](https://www.european-funding-guide.eu/fi-en/scholarship/fortum-neste-foundation) · [TES guide](https://www.european-funding-guide.eu/fi/node/74544)
- [USPTO patent on acoustic leak detection in district heating](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12687263) · [Kamstrup EP4760155A1](https://eureka.patsnap.com/patent/EP4760155A1) · [LOGSTOR Detect](https://www.logstor.com/products/detect)
- [TechXplore KICT](https://techxplore.com/news/2022-12-diagnosis-technology-leaks-district-pipes.amp) · [B&K article](https://www.bksv.com/de/knowledge/blog/perspectives/savings-in-the-pipeline) · [HOFOR](https://doi.dk/en/innovation/artikel/hofor-bruger-ny-teknologi-til-at-opdage-utaetheder-i-fjernvarmeroer) · [Aarhus University](https://ingenioer.au.dk/en/current/news/view/artikel/smart-sensors-to-provide-real-time-data-for-optimized-operation-of-the-district-heating-grid)
- Project data: OpenAIRE via the research_projects tool. EC, UKRI, Research Council of Norway, Swedish Energy Agency, Vinnova and Croatian Science Foundation records as linked above.