# Market assessment: contactless radar screening of sleep apnea that separates obstructive from central events

Fictional demo disclosure dated 2026-11-02. Report date 2026-11-25. Web searches used only general terms, never invention details.

## 1. Possible applications

1. **Home sleep apnea screening and triage device, sold to hospital sleep units and public/private care providers (best case).**
   - What it is: a bedside radar unit with no worn sensors. It reports AHI and the obstructive/central split, and a clinician orders it instead of a belts-and-tube home test.
   - Who pays: Finnish wellbeing services counties and university hospitals; private sleep clinics; occupational health providers. Outside Finland the buyers are sleep-lab chains and telemedicine providers.
   - Why: the problem is real. Finnish secondary-care sleep apnea patients grew from 8,600 in 1996 to 61,000 in 2018 ([registry study via search summary](https://pmc.ncbi.nlm.nih.gov/articles/PMC8889373)). HUS cleared its waiting list in Dec 2024 through a digital care pathway and remote CPAP start ([HUS](https://www.hus.fi/en/newsroom/hus-has-eliminated-waiting-list-sleep-apnea-treatment)). So the waiting-list pain is easing in Helsinki, but the problem remains elsewhere.

2. **CPAP and therapy follow-up (treatment-emergent central apnea).**
   - What it is: contactless monitoring after CPAP start, to flag patients whose central events persist or emerge.
   - Who pays: care providers, and possibly CPAP makers who want a contactless data source (this is my inference, not found in a source).
   - Why: the central/obstructive split is the invention's distinctive point. Existing contactless products, such as the under-mattress mat and the radar unit described in section 3, are described as supporting OSA diagnosis or vital-sign monitoring. I did not find one that reports the split.

3. **Cardiology and heart-failure pathway screening.** Central apnea is common in heart failure (general clinical knowledge, not sourced here). Cardiology clinics would pay to screen patients without belts. This is speculative and needs the researchers' clinical input.

4. **Technology licence (radar and signal processing algorithm) to CPAP, bed or wearable makers or to existing contactless-sensor companies.** The buyers are ResMed, Philips, Withings and similar firms. This is the lowest-risk route for a team with no regulatory experience, though it earns less.

## 2. Market size

Best application: home sleep apnea testing and screening devices.

| Figure | Value | Source | Solidity |
|---|---|---|---|
| Adults with OSA worldwide (ages 30-69) | 936 million mild-to-severe; 425 million moderate-to-severe | [Benjafield et al., Lancet Resp Med 2019](https://pubmed.ncbi.nlm.nih.gov/31300334/) | Peer-reviewed, but ResMed-funded, modelled, with reliable data from only 16 countries |
| Share undiagnosed | "more than 85%" | [ResMed press release via News-Medical](https://www.news-medical.net/news/20190710/More-than-936-million-people-have-sleep-apnea-ResMed-led-analysis-reveals.aspx) | Company claim, weak |
| Home sleep apnea testing devices, global 2025 | USD 0.7-1.6 billion across publishers (Future Market Insights USD 712 million; Global Market Insights USD 1.6 billion) | [GlobeNewswire/FMI](https://www.globenewswire.com/news-release/2025/01/16/3010776/0/en/Home-Sleep-Apnea-Testing-Market-to-Surge-from-USD-712-3-Million-in-2025-to-USD-966-1-Million-by-2035-with-a-3-1-of-CAGR-driven-by-Rising-Awareness-and-Advanced-Diagnostic-Solutions.html), [GMI](https://gminsights.com/toc/detail/home-sleep-apnea-testing-devices-market) | Weak. Consultancy estimates differ by about 2x on definitions, and I did not see the methods. |
| All sleep apnea devices, 2025 | USD 9.3 billion, of which diagnostics USD 3.1 billion | [GMI](https://www.gminsights.com/industry-analysis/home-sleep-screening-devices-market) (via search summary) | Weak, broad scope |
| Finland patient base | About 61,000 secondary-care patients in 2018. An older guideline estimate was about 150,000 patients. | [PMC8889373](https://pmc.ncbi.nlm.nih.gov/articles/PMC8889373) (search summary) | Medium, but dated |

- **Reachable market:** I could not find a reliable figure. A rough approach for the advisor is to count tests per year in Finland and the Nordics times a price per test. I found no verified price or test volume, so I won't give a number.
- **Official statistics:** I did not run a Eurostat product-level (PRODCOM or Comext) query for a specific sleep-diagnostic code. Our health-tech notes give only broad figures. The EU manufacture of medical and dental instruments (NACE C32.5) had about 62,000 enterprises in 2024. Finland's HS 9018 exports were EUR 1.487 billion in 2025 ([Eurostat, via our health-tech memory.md](https://ec.europa.eu/eurostat/databrowser/view/DS-045409/default/table)). These are context, not a market size for this product.
- **Cost position:** the prototype costs about EUR 60 in parts (disclosure). I found no competitor price, so the margin cannot be assessed.

## 3. Competitors and alternatives

**Incumbent methods**
- Polysomnography in a sleep lab. It is the gold standard but costly and slow.
- Home tests with belts, nasal tube and finger clip, which are the cheap standard. The invention targets their patient burden.

**Contactless competitors**
- **Sleepiz (Switzerland), Sleepiz One+.** A radar bedside unit with FDA Class II 510(k) clearance (letter dated 2026-01-28) and a published validation against polysomnography ([FDA letter](https://www.accessdata.fda.gov/cdrh_docs/pdf25/K253388.pdf), [PubMed](https://pubmed.ncbi.nlm.nih.gov/38744804/), [Medical Device Network](https://www.medicaldevice-network.com/news/sleepiz-wins-fda-clearance-for-device-that-measures-vitals-during-sleep)). It has a CE mark from 2020; the class is inconsistently reported ([EIT Health](https://www.eit.europa.eu/news-events/news/eit-health-headstart-winner-sleepiz-earns-ce-certification)). Funding figures vary by source, from CHF 3 million non-dilutive to about USD 11.8 million total ([CB Insights](https://www.cbinsights.com/company/sleepiz)), so the total is uncertain. **This is the closest competitor and is ahead on regulation.** Nothing I found shows it reports the obstructive/central split, but this needs checking.
- **Withings Sleep Rx.** An under-mattress mat with FDA 510(k) clearance (Sept 2024) as an aid in diagnosing OSA, sold by prescription in the US ([Fierce Biotech](https://www.fiercebiotech.com/medtech/fda-clears-withings-contactless-mattress-mat-diagnosing-sleep-apnea), [Withings](https://www.withings.com/us/en/health-solutions/sleep-rx)).
- I found nothing on Sleep Number or Google Nest Hub apnea clearances. I did not research them.

**Patent landscape (our own patent database, EP and WO filings of the last five years)**
- [WO2024224391A1](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2024224391A1) (Neteera, Israel): sleep apnea event determination using radar. This is directly relevant freedom-to-operate prior art.
- [WO2023176948A1](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2023176948A1) (Health Sensing, Japan): contactless AHI estimation from body vibration.
- [WO2026222959A1](https://worldwide.espacenet.com/patent/search?q=pn%3DWO2026222959A1) (Air Force Medical Univ., China): millimetre-wave radar plus EEG sleep monitoring.
- [EP4257168A2](https://worldwide.espacenet.com/patent/search?q=pn%3DEP4257168A2) (Fisher & Paykel): distinguishing central from obstructive apnea inside a CPAP device. This is a risk to the novelty of the "split" claim, though it is not contactless.
- ResMed, Philips and Samsung also appear among active applicants, and the largest filers in the field are implant and therapy firms (Alfred E. Mann Foundation, Medtronic).
- This was a keyword search, not a legal freedom-to-operate analysis. Our company database had no entry for "sleep apnea" companies. Finnish register searches for "sleep" returned only unrelated or ceased firms, so I found no Finnish direct competitor. I found no Finnish company in this exact niche, which also means the Finnish partners need to be identified (see section 5).

**How the invention differs:** the chest/abdomen movement separation to classify obstructive versus central events, plus on-device classification so no raw data leaves the bedroom (a privacy and GDPR advantage). The 87% accuracy for the split is a single small study, not yet proof of a lead.

**Finnish context (our own health-tech memory.md):** Bittium Medical (sleep business in partner talks), Oura (sleep tracking, consumer), and Finland's wider healthtech cluster. The two Finnish firms that approached the team should be named by the advisor. Bittium's sleep business is a possible partner or buyer, but this is my inference.

## 4. Trends and drivers

- **Under-diagnosis and capacity strain:** the large undiagnosed share (company claim) and rising Finnish patient numbers push health systems toward home and remote pathways. HUS has already moved to remote CPAP start ([HUS](https://www.hus.fi/en/newsroom/hus-has-eliminated-waiting-list-sleep-apnea-treatment)).
- **Regulators now clear contactless tools** (Withings, Sleepiz), which shows a route exists.
- **MDR is a cost and time barrier.** The EU MDR/IVDR targeted revision (COM(2025) 1023) is in Parliament. Adoption is expected around Q2-Q3 2027, and current rules apply until then ([Emergo](https://www.emergobyul.com/news/europe-targets-revised-mdr-and-ivdr-adoption-q2-q3-2027?linkId=1018968549), via our memory.md). AI Act high-risk rules for AI in devices are deferred to 2 Aug 2028 (reported, not read in the Official Journal). Software with a diagnostic AI classifier will probably be Class IIa or higher.
- **Acquirers tie earn-outs to CE marks and reimbursement** in European health AI M&A ([Nelson Advisors](https://www.healthcare.digital/single-post/nelson-advisors-this-week-in-european-healthtech-medtech-and-health-ai-13th-november-2026)). A CE mark is therefore central to exit value.
- **Funding for a spin-off:** EIT Health Innovation Validation 2027 (deadline 2027-01-13; needs a company lead), EIC Accelerator, Business Finland Research to Business (decisions on call 2/2026 aimed for January 2027), and no Research Council of Finland Proof of Concept call in 2027 ([EIT](https://www.eit.europa.eu/our-activities/opportunities/innovation-validation-call-2027), [EIC](https://eic.ec.europa.eu/eic-funding-opportunities/eic-accelerator_en), [Business Finland](https://www.businessfinland.fi/en/services/funding/calls/2026/r2b-funding-call-2-2026/)).
- **Headwind:** reimbursement for a screening device is unclear, and the Finnish waiting-list pressure may be easing where digital pathways work.

## 5. Open questions for the researchers

1. **Patents:** nothing is filed, and the conference paper is planned for June 2027. File before any publication or talk. The seminar talk already given may count as disclosure, so what exactly was shown? Have they read Neteera WO2024224391A1 and the Fisher & Paykel family?
2. **Evidence:** 31 patients and 46 nights is small. How many were healthy, mild or central-dominant? How many central events were in the dataset, since 87% accuracy on the split depends on this? Were there bed partners, pets, blankets, or varied sleeping positions? What fraction of nights were excluded?
3. **Comparison:** how does 91% within 4 events/hour compare with Sleepiz One+ and Withings Sleep Rx published results? Does the classifier handle hypopneas and mixed apnea?
4. **Intended use:** diagnosis aid, screening or follow-up? That decides the MDR class and the clinical evidence needed.
5. **Regulation and team:** who will handle MDR, a quality system (ISO 13485) and a notified body? Is a licence to an established company preferable to founding a company?
6. **Interested companies:** which two Finnish healthtech firms asked, and what did they want? Is the hospital offering a co-development agreement, with the IP position clarified, given hospital data and staff involvement?
7. **Radar hardware:** which 60 GHz chip is used and is its licence compatible with medical use? What is the full bill of materials cost beyond EUR 60 (housing, power, certification, support)?
8. **Data and privacy:** how was the data consented, and can it be reused to train and validate the final model?
9. **Business model:** who pays per test, and is there a price reference? I found no verified price, so this must be gathered from clinicians.

## Score: 3 of 5
There is a real need, and the obstructive/central split is a genuine differentiator. But the field already has FDA- and CE-cleared contactless rivals (Sleepiz, Withings), relevant radar patents by others (Neteera), a heavy MDR burden, and a small first study. The market figures are weak consultancy estimates.
