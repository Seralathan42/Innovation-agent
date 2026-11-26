# First screening: contactless sleep apnea screening with a bedside 60 GHz radar (obstructive vs central)

*First screening only, not a legal opinion. The EPO and Google data below are partial, and a professional patent search is needed before any filing decision.*

## 1. Technology in plain words

**What it does.** A small bedside device with a 60 GHz radar chip watches the sleeper's chest and abdomen from up to 2 m. Nothing is worn. Signal processing separates chest motion from abdomen motion. In obstructive apnea the two move against each other (paradoxical breathing). In central apnea both stop. A small neural network on the device classifies each event. It reports AHI and the obstructive/central split. Raw radar data stays on the device.

**What is claimed as new.**
- Contactless obstructive/central classification.
- Edge processing for privacy.
- A parts cost of about EUR 60.
- Validation of 91% AHI agreement within 4 events/h on 46 nights and 31 patients, and 87% correct obstructive/central classification.

**TRL estimate: 4 to 5.**
- It is a working prototype, validated against polysomnography in a real hospital sleep unit.
- The sample is small, from a single site.
- There is no regulatory or clinical-grade product yet.
- It is not yet a medical device. That needs MDR CE marking (probably Class IIa) and a larger multi-site study.

**State of the art.** Radar apnea detection is a very active field. A search of our own data tool (OpenAlex) found about 2,240 papers on "radar sleep apnea detection". Output grew from 92 papers in 2018 to about 310 per year in 2025 and 2026. Aalto has only about 10 papers on the broader topic, mostly older RF-based breathing sensing (for example "Breathfinding", 2014). The leading institutions are Chinese Academy of Sciences, Glasgow, Eindhoven and Harvard.

## 2. Patent landscape

Sources are marked: **[own]** is our stored database, **[EPO]** is the EPO search tool.

| Number | Owner | First filing | Status | Summary |
|---|---|---|---|---|
| CN120616491A/B [EPO] | Qinglan Tech (Shenzhen) | about 2025 | **Granted in CN (B, Oct 2025)**; family of 2, CN only | "Sleep apnea type distinguishing method based on mmWave radar." Body-movement, chest-reflection and respiratory-amplitude features go into a self-attention classifier to determine apnea type. Very close to the core idea. |
| CN122767790A [EPO] | Hangzhou Maidong Shukang | 2026 (published Sep 2026) | Application | mmWave radar separates thorax and abdomen targets. It extracts the thoracoabdominal phase difference and a respiratory effort index, then classifies event types and computes AHI. This is very close to the chest/abdomen separation feature. |
| CN121242558A [EPO] | Daobo Medical (Beijing/Suzhou) | 2025 | Application | CPAP machine with radar: airflow drop with no chest motion means central apnea, and with chest motion means obstructive. It is a ventilator fusion, not standalone. |
| CN121031700A [EPO] | Beijing Qinglei / Shanghai 6th People's Hospital | 2025 | Application | Neural network from radar thoracoabdominal signals, reconstructing airflow and predicting apnea. |
| WO2024224391A1 [own, EPO] | Neteera Tech (IL) | 2023 | IL granted (IL302379B1/B2). US application and EP4701519A1 pending (request for examination 2026). | THz/mmWave radar, ML apnea event count and AHI. It does not appear to claim the obstructive/central split. |
| EP4257168A2 [own] | Fisher & Paykel | 2013 | Application (EP publication 2023) | Distinguishing central and obstructive apnea inside a CPAP device. It is not radar. |
| EP4603005A2 [own] | ResMed Sensor Tech | 2020 | Application | Sleep status detection for AHI from non-contact movement sensing. ResMed is the strongest non-contact incumbent. |
| WO2023272383A1 [own] | Bresotec (CA) | 2021 | Application | Accelerometer-based OSA/CSA analysis. |
| WO2023176948A1 [own] | Health Sensing (JP) | 2022 | Application | Contactless AHI estimation from body vibration. |
| WO2026014502A1 [EPO] | Mari Co (JP) | 2024 or later | Application | Radar-based apnea/hypopnea and cardiovascular index. |
| CN120167935A [EPO] | Hikvision | 2025 | Application | Radar apnea identification. |
| CN122163164A, CN122140189A, CN121647606A, CN121489404A [EPO] | Various Chinese applicants | 2025 to 2026 | Applications | Radar apnea detection, some multi-modal. |

Our stored database also lists Infineon, Samsung, Philips and Mari among the top applicants in the closest 100 patents. I did not review those filings individually.

**Main holders and trend.**
- *Our own data:* of the 100 nearest patents, first filings by year were 2020: 4, 2021: 8, 2022: 31, 2023: 28, 2024: 16, 2025: 10. The late years are probably undercounted because of the 18-month publication lag.
- Top applicants in that set are Alfred E. Mann Foundation, Medtronic, Infineon, Philips, ResMed and Nyxoah. Most of those are implant or therapy filings, not radar screening.
- The EPO search for radar plus apnea found 66 patents. Almost all are 2025 to 2026 filings, and the majority are Chinese. Chinese filing in this niche is rising sharply.
- I did not find any Finnish or Aalto filing.

## 3. Initial novelty check

| Feature | Assessment |
|---|---|
| Contactless radar apnea detection and AHI | **Known.** Many patents (Neteera, Chinese filings) and papers (Kyoto, Chinese Academy of Sciences, Taipei, UCLA). |
| 60 GHz FMCW chest/abdomen signal | **Known.** CN122767790A, CN121031700A and papers. |
| Separating chest from abdomen, with paradoxical versus absent movement | **Largely known.** CN122767790A and CN120616491 describe it. The disclosure's physical principle is textbook (PSG effort belts). |
| Radar-only classification of obstructive vs central | **Not new as a concept.** CN120616491 is granted in CN, and CN121242558A uses radar with airflow. The claim in the disclosure that no other contactless method reports the split is **not supported** by our search. No EP or US counterpart for CN120616491 was seen, but that is not confirmed. |
| On-device neural network, no raw data leaving the room | Edge inference is generic. It is possibly useful as a dependent feature, but weak. I did not check this feature specifically. |
| Clinical performance (91% / 87%), EUR 60 BOM | Results, not patentable as such. They are valuable as data and for a regulatory file. |
| Specific algorithms (feature definitions, network architecture, training approach) | **Possibly new.** The claim details are unknown to me. A detailed comparison against the claims of the Chinese filings is needed. |

Only patents' abstracts and one set of claims (Neteera) were read, and no full-text claim analysis was done.

## 4. Freedom to operate (FTO)

No definitive blocker was found, but several filings need a proper review.

- **CN120616491B (Qinglan Tech):** granted in China only (family of 2, CN). Radar apnea type distinguishing. It does not block Europe or Finland unless a counterpart exists (a PCT or EP filing could still appear, because of publication lag). It matters if you plan to manufacture or sell in China.
- **CN122767790A (Hangzhou Maidong):** a pending Chinese application. It could be extended abroad via PCT within 12 months of priority. Monitor it.
- **WO2024224391 / EP4701519A1 / US20260033774A1 (Neteera):** pending in EP and US. The IL patent is granted. Claim 1 requires an ML apnea-event-count model, segmented displacement signals, sleep status and AHI. It could be a risk if the invention's AHI pipeline is similar, so a claim review is necessary. It does not mention obstructive/central.
- **ResMed Sensor Tech EP4603005A2, Philips, Infineon, Samsung, Health Sensing, Bresotec:** broad non-contact sleep and AHI portfolios. EP4603005A2 is a pending application. I did not check family or legal status for these, so they are open.
- **Fisher & Paykel EP4257168A2:** CSA/OSA classification in a CPAP device, so only relevant if the product is combined with therapy.
- The database does not show legal events for most of these. The status of EP and US applications changes, and a professional FTO search is needed before commercial launch, especially for EU, US and CN.

## 5. Competing technologies and companies

- **Contactless radar and sensing:** Neteera, ResMed (Sleep Score, SleepBase), Sleepiz (CH, contactless sleep monitoring), Infineon (radar chips), Withings (under-mattress), Google Nest Hub (Soli), Mari, Chinese vendors (Hikvision, Qinglan, and others).
- **Home sleep tests:** type III devices (belts, nasal flow, oximetry), WatchPAT, wearables (Apple, Samsung, oximeter rings). Home tests are cheap and reimbursable, so this is the main commercial alternative.
- **Research:** NIH-funded "Contactless and Engagement-free Sleep Apnea Monitoring and Characterization" (2023 to 2027) and Taipei, Kyoto, CAS and UCLA groups. I did not find an EU or Research Council of Finland project on the same topic in this search.

## 6. IP recommendation

**Investigate further first, and do not publish yet.** Decide on a narrow filing, or keep as know-how.

1. **Do not present or publish** before deciding. The June 2027 conference paper would destroy novelty. Ask for a prior-art search before that date. Only a priority filing or a decision not to file should release the paper.
2. **Commission a professional prior-art and FTO search** focused on CN120616491, CN122767790, Neteera, ResMed and Infineon, including full claims and any EP/US/PCT counterparts. The broad claim of radar chest/abdomen OSA/CSA classification is probably unpatentable.
3. **If anything remains, file a narrow provisional or priority application.** Candidates are specific algorithmic features (how chest/abdomen decoupling is computed and robust to posture, bed partner and distance), the training or labelling method, and the on-device pipeline with its performance. Value is likely modest and strategic.
4. **Treat the clinical dataset, the labelled radar-PSG data and the trained classifier as know-how and trade secrets.** These are probably the strongest assets, together with the speed to market.
5. **Commercial route:** MDR regulation, clinical evidence and partnering matter more than a patent. Talk to the two Finnish companies under an NDA, and find regulatory expertise (CE marking under MDR, possibly Class IIa) and a larger multi-site study.

## Patent position score: 2 of 5

Radar-based apnea detection and even obstructive/central distinction using chest and abdomen signals already appear in several recent Chinese filings (one granted in CN), leaving mostly narrow implementation details and clinical validation to protect.

The score could rise to 3 if a professional search finds that the specific algorithm is distinct from those filings.
