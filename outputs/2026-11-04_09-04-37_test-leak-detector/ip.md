# Screening report: Self-calibrating acoustic leak detection for district heating pipes

*First screening only. This is not a legal opinion or a patent search. I did not do a professional search, and I read only three patents in full. The others are known from search snippets.*

## 1. Technology in plain words

**What it does.** Battery-powered acoustic sensors are clamped onto pre-insulated district heating pipes in existing valve chambers, 300–800 m apart. Each sensor records pipe vibration for a few minutes every night. A leak makes a broadband hiss that travels along the pipe in both directions. Standard cross-correlation of two sensors' recordings gives the leak position, but it needs the sound speed in each pipe section.

**What is claimed as new.**
- Each sensor sends a known vibration pulse into the pipe.
- Neighbouring sensors measure the travel time and the attenuation of that pulse.
- From this the system learns the sound speed and damping of each pipe section, with no manual input.
- A small server-side model combines the night recordings with these learned values to flag and locate leaks.

The disclosure says manual values are often 10–20% wrong, which moves the estimated position by tens of metres.

**Evidence in the disclosure.**

| Test | Result |
|---|---|
| Lab rig, DN100, 40 m | Simulated 0.5 l/min leaks detected, position error under 1 m |
| Field trial, 2.3 km, 6 sensors, 4 months | 3 known leaks found, mean error 2.1 m (manual correlator: 9.4 m) |
| Field trial false alarms | 2 in 4 months, both from a pump station |
| Battery life | About 5 years (estimated, not measured) |
| Sensor cost | About 120 EUR in parts (estimated) |

**TRL estimate: about 5.** This is a prototype built from off-the-shelf parts. It was validated in a real operating network, with comparison against a baseline method. The field trial is small, though: 3 leaks, 6 sensors, 4 months. Battery life and cost are estimates, and there is no ruggedised product, no certification and no multi-site data. I would call it TRL 5, borderline 4–5.

## 2. Patent landscape

I found no patent that clearly covers the full combination. The field is crowded around the individual elements, so claim scope will matter.

| Number | Owner | Year | Summary | Link |
|---|---|---|---|---|
| US6082193 | Pure Technologies | 1997 (expired) | Fixed sensors at pipeline access points. An acoustic signal is generated after a detection and recorded at two or more sensors. A pulse is also used for timer synchronisation. | [link](https://patents.google.com/patent/US6082193A/en) |
| US11788919 | Itron | 2021 (active, expires about 2041) | Leak sensors that adapt their sampling time to flow and pressure. Coordinated multi-sensor sampling and leak location. This overlaps with night-time recording and multi-sensor location. | [link](https://patents.google.com/patent/US11788919B2/en) |
| EP4083592 | Kamstrup | 2021 (granted 2025; active) | Leak detection with ultrasonic flow meters at consumer connections. Uses wave direction as a filter and records only at low or zero flow. | [link](https://patents.google.com/patent/EP4083592B1/en) |
| US6595038 / EP1114990 | Not checked | about 2000 | Fixed plus mobile sensor that locates a leak without an accurate sound speed. This is relevant to the calibration idea. | [link](https://patents.google.com/patent/US6595038) |
| EP2352979 | Not checked | – | Leak detector that estimates velocity from the leak signals and the sensor spacing. | [link](https://patents.google.com/patent/EP2352979) |
| US6567006, US6957157 and related | Flow Metrix / Itron | 1999–2005 | Vibration monitoring in a pipeline network. Likely older or expired, but a core family. | [link](https://patents.google.com/patent/US5974862) (US5974862, same company) |
| US8311759 / US20110161038 | Not checked | about 2010 | Acoustic source on an in-pipe vehicle that calibrates sensor distances. | [link](https://patentimages.storage.googleapis.com/b4/f1/e0/9f8b759bf84ddc/US8311759.pdf) |
| CN121993747 | Not checked | – | Distributed acoustic sensing and digital twin for heating pipeline leaks. | [link](https://www.goveda.com/patent/CN-121993747-A) |
| US4288654, CA1143671 | – | old | Pre-insulated district heating line construction, with alarm wires. | [link](https://patents.google.com/patent/US4288654) |

**Main holders.** These are Itron/Flow Metrix, Pure Technologies (Xylem), and Kamstrup (heat and water meters). Other likely players are Gutermann, Hydrovision and Echologics (Mueller). That list comes from my general knowledge, not from the searches.

## 3. Initial novelty check

**Looks known:**
- Clamp-on or fixed acoustic loggers, with overnight recording when the network is quiet (Itron, Kamstrup).
- Cross-correlation location, which is standard for water pipes.
- Location without an accurately known sound speed, by multipath or time-difference-of-arrival methods ([Uchendu et al., 2025](https://doi.org/10.1016/j.jsv.2025.118970)), by a mobile reference sensor (US6595038), or by estimating speed from the leak signal (EP2352979).
- Active acoustic pulses in pipelines, for timing synchronisation and calibration (Pure Technologies, 1997; the in-pipe source in US8311759).
- Acoustic leak detection in district heating (Argonne work from 1987–92; [Ji et al., 2022](https://doi.org/10.6110/kjacr.2022.34.8.380); the CN patent).
- Wave-speed evaluation in pressurised pipes ([Green & Cascante, 2025](https://doi.org/10.58286/31359)).

**Possibly new:**
- Permanent clamp-on sensors that autonomously and periodically send pulses to neighbours, and learn both speed and damping per pipe section.
- Using the learned values as inputs to the server-side leak flag and location model, with drift tracking (temperature, ageing).
- The application to pre-insulated steel district heating pipes, with demonstrated field results.

The inventors' belief that no one measures speed and damping with active pulses is only partly supported. The general idea of active calibration pulses appears in older patents, so novelty probably depends on the specific claim wording. I could not read the full text of every candidate.

**Publication risk.** A conference paper was submitted on 15 September 2026, with a decision in December. If the paper or a preprint is public, novelty in Europe is lost. A filing before any publication is essential. Check at once whether the submission is public, for example on arXiv or in an open review system.

## 4. Freedom to operate

- No single patent found clearly blocks the concept. Active pulses plus clamp-on sensors on heating pipes looks reasonably open.
- **Itron US11788919** (active to about 2041, US/EP/AU/CA) covers coordinated sampling at low flow with multi-sensor location. A night-recording scheme could touch its claims, so the claims need review.
- **Kamstrup EP4083592** (active to 2041) is narrow, covering ultrasonic flow meters at consumer connections. The risk is low.
- The Pure Technologies patent has expired. Several older Flow Metrix and correlator patents are probably expired as well, since they date from before 2006.
- I did not check legal status in Finland, Sweden, Denmark, Germany or Poland, which are the key district heating markets. Pending applications from the last 3–5 years, such as the CN filing and the Itron family continuations, are the main unknown.
- A professional FTO search is needed before commercialisation, with claim-by-claim analysis in the target countries.

## 5. Competing technologies and companies

**Incumbent district heating methods:**
- Alarm wire systems (Nordic firms such as Logstor and Brugg, and others).
- Thermal drone or satellite surveys.
- Manual ground microphones.

**Acoustic loggers and correlators (water and gas):**
- Itron/Flow Metrix.
- Xylem/Pure Technologies.
- Gutermann.
- Echologics.
- Fixed hydrophone networks.

**Other approaches:**
- Meter-based acoustic detection (Kamstrup).
- Fibre-optic distributed acoustic sensing.
- A low-power TDR system powered by the pipe's own temperature gradient ([Koolivand et al., 2025](https://doi.org/10.1109/jsen.2025.3588959)).
- Academic groups working on wave-speed identification (Southampton, Waterloo, the Chinese Academy of Sciences, Hong Kong PolyU).

**Research projects.** My one funded-project search ("leak detection pipe") returned nothing, which is a thin result, not evidence that nobody is working on this. Check the Horizon Europe and national heat-sector programmes further.

## 6. IP recommendation

**Recommendation: investigate further, then file a focused priority application, in time.**

1. **Publication timing.** Confirm whether the conference paper is public. If not, request that it stay unpublished, or file before any publication. The submission date does not itself destroy novelty, but any public posting would.
2. **Professional prior-art search.** Cover the active-pulse calibration of speed and damping in pipes (CPC G01M3/24, G01N29, F17D5/06, G01S5/18, F24D/F16L59 for district heating), plus the full Pure Technologies, Itron and Flow Metrix families.
3. **Draft claims** around the combination. These are the autonomous inter-sensor pulse exchange, per-section learning of speed and damping, and use of the result in localisation. Add dependent claims for continuous drift tracking and for pre-insulated pipes.
4. **Ownership.** Check the employment and funding terms, including the Research Council of Finland project and any energy-company agreement. The company gave access only and no money, but confirm that it has no data or invention rights.
5. **Business route.** The doctoral researcher wants to found a company, but the team has no business experience. Support with a pilot agreement (the 2027 pilot with the host utility), customer discovery beyond one company, and a licence or spin-out structure. Keep the model and the calibration algorithm as know-how alongside the patent.
