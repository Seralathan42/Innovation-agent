# First screening: self-calibrating acoustic leak detection for district heating pipes

*Disclosure: "Self-calibrating acoustic leak detection for district heating pipes" (fictional test disclosure, dated 1 Oct 2026). This is a first screening, not a legal opinion. In the searches I used only general terms and no distinctive details from the disclosure.*

> ⚠️ **Urgent: deadline.** A conference paper was submitted on 15 Sep 2026 and the decision is expected in December 2026. Once it is published, or presented, or put online as a preprint or camera-ready version, the invention can no longer be patented in Europe. A patent application (at least a Finnish or EP priority filing) must be filed **before** the paper becomes public. Ask the inventors now whether a preprint or abstract is already online.

---

## 1. Technology in plain words

**What it does:** It finds and locates hot-water leaks in buried district heating pipes without digging and without relying on alarm wires.

**How it works:**
- Small battery-powered vibration sensors are clamped onto pipes inside existing valve chambers, 300–800 m apart.
- They record for a few minutes each night, when the network is quiet. A leak makes a broadband hiss that travels along the pipe both ways.
- The server compares the arrival times at neighbouring sensors (leak-noise correlation) to estimate where the leak is.
- **The new part is self-calibration.** Each sensor can send a known vibration pulse into the pipe. Its neighbours measure how fast the pulse travels and how much weaker it gets. This gives the real sound speed and damping of each pipe section.
- Today's correlators use sound speeds that people enter by hand, and these are often 10–20% wrong, which shifts the leak position by tens of metres.
- A small model on the server combines the night recordings with the measured pipe properties to flag leaks and estimate their position.

**Compared with the state of the art:**
- Fixed acoustic loggers and correlators are well established for drinking-water networks (Gutermann, Mueller/Echologics, Aquarius Spectrum and others).
- Measuring sound speed with an active pulse between two sensors is also known, but mainly as a separate pipe-condition survey done by a crew (NRC Canada / Echologics / Mueller).
- What looks new is putting these together: permanent, battery-powered nodes that **measure both speed and damping per section automatically and repeatedly, and use them directly for leak location**, aimed at pre-insulated steel district heating pipes.

**TRL estimate: TRL 5** (validated in a relevant environment).
- A lab rig (DN100, 40 m) showed detection of 0.5 l/min leaks with under 1 m position error.
- A 4-month field trial on 2.3 km of a real network with 6 prototype sensors found 3 known leaks with a mean error of 2.1 m, against 9.4 m for a manual correlator on the same data. There were 2 false alarms, both caused by a pump station.
- It is not TRL 6–7 because the sensors are built from off-the-shelf parts, the trial was small, and the 5-year battery life is an estimate, not a measurement. Pump-noise rejection and long-term robustness have not been demonstrated.

## 2. Patent landscape

| Number | Owner | Year (priority) | Status | Summary |
|---|---|---|---|---|
| [US11726064B2](https://patents.google.com/patent/US11726064B2/en) | Mueller International | 2020 | Active (US; CA family), expires ~2041 | Measures the speed of sound in a pipe segment: repeated impulses are generated outside the sensor pair, the arrivals are averaged at the near and far sensors, and the time delay gives the speed. Claim 6 covers an impulse generator and claim 8 a timing sensor next to it. CPC classes also include attenuation. **Closest prior art and main FTO concern in the US.** |
| [US11609348B2](https://patents.google.com/patent/US11609348B2/en) | Mueller International | 2020 | Active (US), ~2041 | Impulses at two locations, at least one between the two sensors, give the speed of sound for one section, used to assess pipe condition. |
| [US12196714B2](https://patents.google.com/patent/US12196714B2/en) | Mueller International | 2021 | Active (US; WO filed), ~2042 | Speed of sound for each individual pipe length, from pulse reflections at pipe joints. |
| [US10690630B2](https://patents.google.com/patent/US10690630B2/en) | Mueller International | 2017 | Active (US), ~2037 | Sound attenuation for each pipe–soil combination, **calculated from a model** (not measured), used to plan where to place sensor nodes. |
| [US7328618B2](https://patents.google.com/patent/US7328618B2/en) / [US6561032B1](https://www.google.de/patents/US6561032) | NRC Canada → Echologics / Mueller | 2005 / 2000 | Expired / lapsed (US6561032 likely expired; not checked) | Measure the propagation speed of a disturbance between two points on the pipe and work out wall thickness from it. Key prior art for "active speed measurement". |
| [US5974862A](https://patents.google.com/patent/US5974862A/en) | Flow Metrix → Itron | 1997 | Expired | Networked digital correlator. According to the search summary it describes vibrating the pipe with a "token signal" from one sensor processor so the system can find sensor spacing automatically. **This is close prior art for sensor-emitted pulses** (should be checked in the full text). |
| [WO2011021039A1](https://patents.google.com/patent/WO2011021039A1/en) | Severn Trent Water | 2009 | Ceased | Works out the sound speed from the leak signal itself (phase versus frequency) and uses it to locate the leak. This is passive self-calibration of speed. |
| [US12540876B2](https://patents.google.com/patent/US12540876B2/en) | M. Pieneman (individual) | 2022 | Active (US; PCT filed) | An emitter inside the pipe sends acoustic pulses, and frequency sensors plus mass-flow sensors locate the leak. Different design. |
| [US12687263B2](https://patents.google.com/patent/US12687263B2/en) | Kamstrup A/S | 2021 | Active (US; EP, CN, WO filed) | **Acoustic leak detection in district heating** using the ultrasonic flow meters in customers' heat meters, with pump-noise filtering. |
| [US12523507B2](https://patents.google.com/patent/US12523507B2/en) | Sagemcom | 2020 | Active (US, EP, CN, ES, FR) | Leak detection from noise levels measured by ultrasonic water meters. |
| [US20190128766A1](https://patents.google.com/patent/US20190128766A1/en) | Mueller | 2017 | Abandoned | Time-synchronisation correction between correlating nodes. |
| CN121993747A (seen in search results, not read) | – | recent | Unknown | Heat-supply pipe leak diagnosis using distributed acoustic sensing (fibre) and a digital twin. |

**Main patent holders:**
- **Mueller International / Echologics** dominate both active speed-of-sound measurement and fixed acoustic node networks.
- Others: Itron/Flow Metrix (older), Gutermann, Aquarius Spectrum (US8665101B2, not read), Kamstrup and Sagemcom (meter-based detection), NRC Canada (origin of the Echologics patents).
- Few patents are specific to district heating. Kamstrup is the main one.

## 3. Initial novelty check

**Already known (from patents and papers):**
- Fixed or temporary acoustic sensors on pipes, with cross-correlation leak location (US5974862, US6530263, many others).
- Measuring section sound speed with an active impulse and two sensors (US6561032, US7328618, US11726064B2, US11609348B2).
- Sensor processors sending a test vibration to calibrate the system (US5974862, per the search summary).
- The problem that hand-entered speeds are wrong, and estimating speed in place (Severn Trent WO2011021039; UNESP work on in-situ wave speed in plastic pipes; [Green & Cascante 2025](https://doi.org/10.58286/31359); [Uchendu et al. 2025](https://doi.org/10.1016/j.jsv.2025.118970), which estimates speed and location together from reflections; [Matos et al. 2024](https://doi.org/10.1088/1742-6596/2647/8/082011)).
- Night-time recording and suppressing pump noise (Kamstrup US12687263B2).
- Acoustic leak detection in district heating in general (Argonne reports 1987–1992; [Ji et al. 2022](https://doi.org/10.6110/kjacr.2022.34.8.380); Korean KICT machine-learning pilot).

**Possibly new (to be confirmed by a professional search):**
- Battery-powered nodes in valve chambers where **the same node both sends the pulse and listens**, and the system **re-calibrates automatically and repeatedly** (for example to follow changes in water temperature), without a field crew.
- Measuring **damping/attenuation per section** and using it directly in leak detection and location. In the patents found, attenuation is either modelled (Mueller US10690630) or used for condition assessment.
- A server model that combines the measured section properties with the night recordings, specifically for pre-insulated steel district heating pipes.

**Assessment:** The individual building blocks are known. Patentability will mainly depend on **inventive step for the combination**, which is the weak point. The strongest claims will probably be the detailed ones: tracking calibration over time and temperature, using attenuation in the location estimate, the node that both sends and receives, and the measured improvement in accuracy (2.1 m versus 9.4 m). A professional novelty search, including EP, DE, DK, SE, CN and JP documents, is needed.

## 4. Freedom to operate (indicative only)

- **Mueller US11726064B2 (US, plus a Canadian family member):** This is the most relevant. Claim 1 requires *several* impulses generated *outside the sensor pair*, recovery of precise impulse timings, and **averaging of the aligned impulses** at both sensors to get the speed of sound. If the invention averages repeated pulses sent from one end node and measured by its neighbour, it could come close. Whether a pulse sent *at* a sensor location counts as "out-of-bracket" needs a claim-by-claim analysis. **It is relevant only for the US and Canada.** No EP family member was seen, but this needs to be verified.
- **Mueller US11609348B2 / US12196714B2 (US):** These need an excitation point *between* the sensors, or reflections from pipe joints. The disclosed design seems to fall outside them, but this should be checked.
- **Mueller US10690630B2 (US):** Concerns a modelled attenuation map for planning node placement. Probably not infringed.
- **Kamstrup US12687263B2 (US, with EP, CN and WO filed):** Requires using the ultrasonic flow meters in heat meters to detect leaks. The invention uses its own pipe-clamped sensors, so the risk looks low. The EP status should be checked, because Kamstrup is a likely partner or competitor in the Nordic district heating market.
- **The older foundational patents** (NRC, Itron, Severn Trent) are expired or ceased, so they are free to use and useful as prior art.
- **Overall:** No blocking patent was found for **Finland or the EU**. The **US** is crowded by Mueller's active-acoustics patents. A professional FTO analysis is needed before entering the US market, and also to check EP/DE/DK equivalents and recent Chinese filings.

## 5. Competing technologies and companies

- **Alarm-wire surveillance built into pre-insulated pipes:** the established method. Pipe makers such as Logstor and Isoplus, and monitoring suppliers such as RATMON. As the disclosure notes, the wires are broken or missing in many older networks.
- **Thermal drone flights:** HOFOR and others; KIT has published an economic study (2026). They only work in winter and give a rough location.
- **Manual acoustic listening and correlators:** Gutermann, Sewerin, SebaKMT, HOFOR's trained field crews.
- **Fixed acoustic loggers for water networks:** Gutermann ZONESCAN, Mueller/Echologics EchoShore, Aquarius Spectrum, Itron. These could be adapted for district heating.
- **District-heating-specific newcomers:** Pipeguard Nordic (remote listening to vibrations); Kamstrup (heat meters used as leak sensors); Aarhus/Aalborg University's self-powered TDR system ([Koolivand et al. 2025](https://doi.org/10.1109/jsen.2025.3588959), under 0.55 m error); fibre-optic distributed acoustic sensing (Chinese filings); Hydraulic Analysis Ltd (machine-learning acoustics).
- **Inline tools:** Xylem/Pure Technologies SmartBall.

The OpenAIRE search did not find a funded project working on the same specific approach. Related funded work is mostly on water networks, for example UK "Smart Leak Detection Pipes".

## 6. IP recommendation

**Recommendation: investigate further, and urgently. If the professional search does not find anticipating prior art, file a Finnish or EP priority application before the conference paper is published.**

Reasons:
1. **Deadline:** publication is expected after December 2026. Filing a priority application first keeps the option open at low cost and gives 12 months to decide on PCT, informed by the 2027 pilot.
2. **Commercial case:** the doctoral researcher plans a spin-off in 2027 and an energy company is asking for a larger pilot. A start-up in a market where Mueller holds many patents will benefit from having its own filing.
3. **Inventive step risk:** active speed measurement is known, so claims should focus on the automatic, repeated calibration of speed and attenuation by the nodes themselves, how that calibration feeds the leak-location model, and the district heating setting. The professional search should check the full texts of US5974862 and the Mueller family first.
4. **Keep as know-how:** the server model, training data, rules for rejecting pump noise, and installation methods. Leave these out of both the patent application and the paper.
5. **Check before filing:**
   - whether any preprint or abstract is already public;
   - the terms of the agreement with the energy company (confidentiality, IP or data rights, whether the field trial counts as "public use");
   - the IP terms of the Research Council of Finland funding;
   - inventor shares (60/40) under the Finnish University Inventions Act.
6. **If no filing:** publishing then makes the approach free for everyone to use, including the spin-off, which then has to compete on speed to market and know-how.

**Needs a professional:** a novelty and inventive-step search, an FTO opinion on Mueller's US patents and any EP equivalents, and a check of Kamstrup's EP status.

---

**Sources:** [Google Patents US11726064B2](https://patents.google.com/patent/US11726064B2/en) · [US11609348B2](https://patents.google.com/patent/US11609348B2/en) · [US12196714B2](https://patents.google.com/patent/US12196714B2/en) · [US10690630B2](https://patents.google.com/patent/US10690630B2/en) · [US7328618B2](https://patents.google.com/patent/US7328618B2/en) · [US6561032B1](https://www.google.de/patents/US6561032) · [US5974862A](https://patents.google.com/patent/US5974862A/en) · [WO2011021039A1](https://patents.google.com/patent/WO2011021039A1/en) · [US12540876B2](https://patents.google.com/patent/US12540876B2/en) · [US12687263B2](https://patents.google.com/patent/US12687263B2/en) · [US12523507B2](https://patents.google.com/patent/US12523507B2/en) · [US20190128766A1](https://patents.google.com/patent/US20190128766A1/en) · [US6530263B1](https://patents.google.com/patent/US6530263B1/en) · [CN102997056A](https://patents.google.com/patent/CN102997056A/en) · [UNESP in-situ wave velocity](https://repositorio.unesp.br/entities/publication/a1acdf74-b83c-4ecf-8454-ff32fe64ef22) · [Argonne DH acoustic leak detection](https://trid.trb.org/View/287134) · [HOFOR / DK article](https://doi.dk/en/innovation/artikel/hofor-bruger-ny-teknologi-til-at-opdage-utaetheder-i-fjernvarmeroer) · [Pipeguard Nordic](https://india.innovationsaccelerator.com/?p=2344) · [RATMON](https://ukdea.org.uk/ratmon-uk/) · [Gutermann ZONESCAN](https://img0.hospitalityhub.com.au/gutermann-correlating-noise-logger-zonescan-820/p/108211) · [Xylem Wrocław case](https://www.xylem.com/siteassets/support/case-studies/case-studies-pdf/fortum-power-and-heat-polska--wroclaw-poland.pdf) · [KICT district heating diagnosis](https://www.newswise.com/articles/new-diagnosis-technology-for-preventing-water-leaks-from-district-heat-pipes) · Papers via OpenAlex as linked above.
