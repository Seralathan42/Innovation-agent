# Contactless sleep apnea screening with a bedside 60 GHz radar that separates obstructive from central apnea

**Summary:** A small bedside device with a 60 GHz radar chip measures chest and abdomen movement without any worn sensors. An on-device neural network reports AHI and the obstructive/central split.

*(Fictional demo disclosure dated 2026-11-02. Everything below comes from the disclosure unless marked as our own data or web.)*

## Need
- **Who:** Sleep apnea patients, and the sleep units and health systems that diagnose them. The disclosure says close to a billion people are affected and most are undiagnosed. Finnish waiting lists are often several months long.
- **Pain:** Polysomnography needs a night in a lab with a dozen sensors. Home tests need belts, a nasal tube and a finger clip, which many patients tolerate poorly. Telling obstructive from central apnea still needs chest and abdomen belts.
- **Importance:** High and clear. The type of apnea decides the treatment: CPAP for obstructive, a different therapy for central. Willingness to pay is not stated.

## Approach
- A radar at up to 2 m separates chest and abdomen motion. Obstructive events show the two moving against each other. In central events both stop. A small neural network on the device classifies each event, so no raw radar data leaves the bedroom.
- **Route to market (my view; the disclosure states none):** There are two options.
  - Licence or sell to an existing health-tech or sleep-device company. Two Finnish health-tech companies have already asked about the results.
  - A spin-off by the doctoral researcher and postdoc. This is a regulated medical device, so it needs CE marking under the MDR. Capital and time needs are high.
  - A staged route fits best. File patents first, run a larger clinical study with the hospital, then decide between a licence and a spin-off, possibly with a partner who brings regulatory capability.

## Benefits per costs
- Prototype bill of materials is about EUR 60.
- Accuracy against polysomnography:
  - AHI was within 4 events per hour in 91% of nights (46 nights, 31 patients).
  - Obstructive/central classification was correct 87% of the time.
- Patient benefit: nothing is worn, and the device could be used at home or on repeat nights.
- Clinic and health-system benefit: shorter queues and fewer lab nights. This is not quantified.
- Not stated: the target selling price, the cost per test against polysomnography or home tests, and reimbursement.
- "Within 4 events per hour" is a loose agreement band. It does not show how often the severity category (mild, moderate or severe) is right.

## Competition
**Our own patent data (stored_patents):** Patenting in this area is active. Most of it is therapy (implants from Medtronic, Inspire and Nyxoah) or wearable and clinical analytics. The closest filings are:
- [WO2024224391A1](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2024224391A1), Neteera: sleep apnea event determination with millimetre-wave or terahertz radar. This is the closest to the invention and a freedom-to-operate risk.
- [EP4257168A2](https://worldwide.espacenet.com/patent/search?q=pn%3DEP4257168A2), Fisher & Paykel: distinguishing central from obstructive apnea, but in a CPAP-type device. It shows the split has value and is already claimed in other forms.
- [WO2023176948A1](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2023176948A1), Health Sensing: non-contact AHI estimation from body vibration.
- [WO2026222959A1](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026222959A1), Air Force Medical University: EEG plus millimetre-wave radar sleep monitoring.
- ResMed Sensor Tech and Philips also appear in the results.

stored_companies returned no match for "sleep apnea radar".

**Web:**
- Sleepiz makes a bedside radar built on Infineon 60 GHz chips. It is FDA-cleared and has been validated against polysomnography for apnea diagnosis: [validation study](https://pubmed.ncbi.nlm.nih.gov/38744804/), [Infineon partnership](https://www.eenewseurope.com/en/infineon-sleepiz-use-radar-for-high-precision-home-sleep-monitoring/). This is the most direct competitor.
- A Korean IR-UWB radar apnea patent, [US 12,232,862](https://patentsgazette.uspto.gov/week08/OG/html/1531-4/US12232862-20250225.html).
- Amazon reportedly worked on a bedside radar device (2021 report, [Futurism](https://futurism.com/neoscope/alexa-device-scans-body-radar.md)). I found no later confirmation.
- Established alternatives are polysomnography and home sleep tests with belts and oximetry. I did not check specific products for these.

**Why this could be better:** The obstructive/central split without belts is the differentiator. I did not find another contactless method reporting it, which agrees with the researchers, but my search was limited. Radar sensing itself is not new, so the advantage rests on this classification and its validation.

## Team
- **Doctoral researcher:** wants to found a company after the PhD and has completed the Aalto Ventures Program.
- **Postdoc:** built the classifier and would join.
- **Professor:** stays in academia and supports a spin-off.
- **Missing:** medical device regulatory and quality expertise (MDR), a clinical lead, a business or CEO lead with health-tech sales experience, and hardware or manufacturing skills. The doctoral researcher cannot start full-time until after the PhD, and the timing is not stated.

## Readiness and funding
- **Readiness:** a working prototype tested on 46 nights with 31 patients against polysomnography at a university hospital. This is roughly technology readiness level 4 to 5 and clinical proof of concept. No regulatory work has been done.
- **IP:** nothing filed, and nothing published. A conference paper is planned for June 2027, so a priority filing must come before it.
- **Current funding:** a Research Council of Finland project (2024 to 2027). There is no commercialisation funding.
- **Possible next funding (my suggestions, not checked against current calls):** Business Finland programmes for research-to-business and health-tech, Aalto or Finnish proof-of-concept funding, and EU or hospital-partnered clinical study funding.

## Assessment
**Strengths**
- A clear clinical need, with a treatment decision tied to the output.
- A differentiating feature: the obstructive/central split without belts.
- Low hardware cost and privacy-friendly processing on the device.
- Early clinical data and a hospital partner that wants a larger study.
- Two companies have already shown interest.

**Risks**
- A small and possibly single-site dataset: 87% for the split is untested for generalisation, and the number of central events in the data is unknown.
- Crowded radar field, with Sleepiz cleared and Neteera patenting.
- No IP filed, and freedom to operate is unclear.
- The MDR pathway is costly and slow, and the team has no regulatory experience.
- Business model and reimbursement are undefined.

**Questions for the researchers**
1. How many central and mixed events were in the 46 nights? What are the sensitivity and specificity for central apnea, and the severity-category accuracy, not only AHI within 4/h?
2. What exactly is novel against Neteera, Sleepiz and the other radar and chest/abdomen-motion filings? Has anyone done a patent search, and can you file before the June 2027 paper?
3. What do the two Finnish companies want (licence, co-development, pilot), and have they said anything about terms?
4. Who owns the IP, and how do the hospital's contributions affect it? Can the doctoral researcher work full-time on this before the PhD ends?
5. Who would take on regulatory, clinical and commercial leadership, and what is the intended intended-use claim (screening, or diagnosis supporting treatment choice)?

**Score: 3.** A promising case with a real, differentiated need, but with clear gaps in IP, competition and regulatory team capability.
