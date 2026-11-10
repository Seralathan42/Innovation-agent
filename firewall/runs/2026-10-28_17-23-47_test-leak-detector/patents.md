# Prior-art landscape: leak detection and condition monitoring for buried district heating (DH) pipes

**Basis and limits.** I ran four searches and opened one patent in full, US7960978B2. Everything else comes from search snippets, so claim details, owners, legal status and dates marked "unverified" need checking before anyone relies on them. I did not search the assignees directly (Logstor, Brandes, Isoplus, Kamstrup and others). Their patent portfolios are therefore probably under-represented.

## 1. Patents

### Verified by reading the record

**US7960978B2** — Thermacor Process Inc, priority 2008, granted 2011. Status: Active, adjusted expiry about 2029. [Link](https://patents.google.com/patent/US7960978B2/en)
- It covers an alarm-wire system in pre-insulated steam or hot-water pipe. The pipe has a carrier pipe, bonded foam and a polyolefin jacket.
- A bare conductor wire runs through the foam, parallel to the pipe axis. At barriers such as water stops or earth anchors, a length of polymer-coated wire exits the jacket and re-enters on the other side.
- The jacket openings are heat-fused to the coating to seal them. The bare ends connect to an external electrical circuit, which gives electrical continuity past the barrier and an indication of water ingress.
- This is a good reference for wire-based sensing hardware at barriers.
- Its citations include US3882382A (Transco, insulated conduit cover and leak detector), US4576661A (sealing the end of insulated pipes that have monitoring wires), US6112580A (Hesky, device for detecting leaks in pipelines) and US5795994A (measuring condensed moisture).

### Identified from search snippets only (unverified)

- **US4288653A and US4288654A** (about 1979–1981), "District-heating line" and a method of manufacturing it. [US4288653A](https://patents.google.com/patent/US4288653), [US4288654A](https://patents.google.com/patent/US4288654). Early pre-insulated DH lines with built-in electrical leak detection (G01M3/18). The CA1143671A family member is also listed.
- **US4746911A**, "Alarm device for isolated pipe systems." [Link](https://patents.google.com/patent/US4746911A/OSRAM). An alarm device for insulated pipe systems. It cites the older DH patents.
- **SE424359B**, a device for break indication in district heating pipes. [Link](https://patents.google.com/patent/SE424359B/esLanguage). An early Swedish alarm-wire concept.
- **EP0060552B1**. [Link](https://patents.google.com/patent/EP0060552B1/en). A signal line is embedded in the insulation between the steel medium pipe and the PE jacket.
- **EP0348920A2 / B1**. [Link](https://patents.google.com/patent/EP0348920B1/enExample). Metal plates or electrodes in the foam. Increased moisture creates a short circuit that signals a leak.
- **US3927351A**, insulated pipe systems with moisture-detecting means. [Link](https://patents.google.com/patent/US3927351A/enExample). Wires in the insulation, connected to means for detecting conductivity. The wet point can be located by a separate measurement on the wires.
- **US4013924**, methods and means for detecting moisture adjacent insulated pipes. [Link](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/4013924).
- **EP2696183A2** (about 2014). [Link](https://patents.google.com/patent/EP2696183A2). Two conductors in the insulation. A deviation in loop resistance indicates an interruption, and a deviation in insulation resistance indicates moisture.
- **US3838593A**, an acoustic leak location and detection system. [Link](https://patents.google.com/patent/US3838593A/enExample). This is a general pipe patent, not DH-specific.
- **US10502652B2**, a system for monitoring pipeline leakage and a pipeline element equipped with it (listed as similar to US7960978B2). Owner not checked.
- **US20250130134** (2025, via Justia), a system and method for acoustic leak detection in a utility distribution system. [Link](https://patents.justia.com/patent/20250130134). It uses multiple acoustic sensors that measure the acoustic profile of a pipe network, covers heating and water networks, and locates leaks by cross-correlation.
- **US 12455208**, acoustic leakage detection by use of an ultrasonic flow meter. [Link](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12455208). Consumer-site ultrasonic meters act as microphones that listen into the pipe network. The number format looks unusual, so verify it.
- **US 12687263**, acoustic leak detection in a district heat conduction network. [Link](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12687263). This is a heat meter with ultrasonic receivers and an acceleration sensor, switchable into a leak-detection mode. Two spaced sensors give the direction of an incoming signal, which filters out noise from nearby consumer sites. Verify the number and owner.
- **CN121999801A and CN121993747A** (recent), covering acoustic sensing arrays combined with AI to locate leaks in heating pipelines. [CN121999801A](https://www.goveda.com/patent/CN-121999801-A), [CN121993747A](https://www.goveda.com/patent/CN-121993747-A).

**Gaps to fill next.** I found no patents on these topics:
- TDR or pulse-reflectometry localization on alarm wires
- ground-microphone or correlator methods
- thermal or aerial imaging
- pressure-wave detection
- hydraulic-model or ML detection

Searching in CPC classes G01M3/24, G01M3/28 and F17D5/02 by assignee should surface them.

## 2. Papers

1. Valinčius et al. 2017, [pressure-wave leak detection in a DH network](https://doi.org/10.1080/15732479.2017.1330892). Field demonstration of pressure-transient detection (Lithuanian Energy Institute).
2. Xue et al. 2020, [machine-learning leakage fault detection for DH networks](https://doi.org/10.1016/j.enbuild.2020.110161). Data-driven detection (Harbin Institute of Technology).
3. Jallal et al. 2023, [assessing ML algorithms for leak detection in smart DH networks](https://openalex.org/W7106784711). Compares ANN, SVM, DT, RF, XGBoost and NB on topology, temperature, demand and differential-pressure data (CEA).
4. Jallal et al. 2025, [hydraulic and thermal sensors with ML for leak detection and localization](https://doi.org/10.11159/ffhmt25.220). Neural-network localization from pressure and temperature variations (CEA).
5. Koolivand et al. 2024, [a 65 nm TDR-based leak detection SoC for DH networks](https://doi.org/10.1109/cicc60959.2024.10528962). A 2-wire sensor along a twin pipe forms a transmission line. A moisture-soaked insulation section lowers the impedance, and the reflection locates it, with a claimed accuracy of 0.14 m (Aarhus University).
6. Risch et al. 2026, [guided leak detection in DH networks from aerial thermal imagery](https://doi.org/10.5194/isprs-annals-x-4-w8-2025-623-2026). Thermal anomaly detection guided to reduce false positives.
7. Vollmer et al. 2026, [economic viability of thermography-based leak detection](https://doi.org/10.1016/j.applthermaleng.2026.131038). A cost assessment of remote-sensing thermography (KIT).
8. Liu et al. 2025, [hydraulic-driven IIoT leak detection model](https://doi.org/10.1080/1573062x.2025.2608602). Combines a hydraulic model with IIoT data to identify leaking segments.
9. Chang et al. 2026, [pressure-wave leak detection under multiple operating conditions](https://doi.org/10.2139/ssrn.6333789). Feature selection for pressure-wave detection (Dalian University of Technology).
10. Kupperman and Karvelas 1988, [acoustic leak detection for DH systems](https://openalex.org/W1509174850). Argonne tests of piezoelectric sensors, accelerometers and capacitance microphones in a Scranton DH system. They report detection at several hundred metres and a location accuracy of a few metres.

## 3. Main players

- **Pre-insulated pipe makers with alarm-wire systems:** Thermacor (US), Logstor, Isoplus, Brugg, Powerpipe and Brandes (alarm and monitoring instruments). From my background knowledge, not verified in this search.
- **Heat-meter and ultrasonic-meter vendors adding acoustic listening:** Kamstrup, Diehl and similar. The US 12687263 and US 12455208 families appear to belong here (owners unverified).
- **Utility pilots:** HOFOR (Copenhagen) has trialled new technology for detecting DH pipe leaks, according to the [DOI.dk article](https://doi.dk/en/innovation/artikel/hofor-bruger-ny-teknologi-til-at-opdage-utaetheder-i-fjernvarmeroer).
- **Research groups:**
  - Lithuanian Energy Institute
  - CEA-LITEN (France)
  - Aarhus University (TDR chip)
  - Harbin Institute of Technology
  - Dalian University of Technology
  - University of Science and Technology Beijing
  - KIT (Karlsruhe)
  - Argonne (historical)
- **Chinese applicants:** many recent AI and acoustic-array filings.

## 4. Technology trends

- **Established:**
  - Alarm wires or moisture-sensing conductors in the pipe foam. They are read by resistance or impedance measurement, with pulse-echo or TDR location, and are standard in pre-insulated pipe.
  - Periodic walking surveys with ground microphones and correlators.
  - Thermal imaging surveys.
- **Growing:**
  - Hydraulic and thermal data (pressure, temperature, flow, differential pressure) analysed with ML to detect and localize leaks.
  - Pressure-wave detection.
  - Aerial thermography with automated anomaly detection, now being assessed on cost.
- **New:**
  - Reusing consumer-site ultrasonic heat or flow meters as permanently installed acoustic sensors, with direction discrimination.
  - Sensor arrays with AI for noise-robust detection of small leaks.
  - Integrated TDR chips with centimetre-scale location accuracy.
  - Fusion of several sensing modes with a digital-twin or hydraulic-model layer for maintenance planning.
- **Where the gaps may be:** I found no prior art combining these approaches in a single system. That is a limit of this search, not evidence that none exists, so a targeted search by assignee and CPC class (G01M3/24, G01M3/28, F17D5/02, F24D10/00) is needed.

Sources:
- [US7960978B2](https://patents.google.com/patent/US7960978B2/en)
- [US4288653A](https://patents.google.com/patent/US4288653)
- [US4288654A](https://patents.google.com/patent/US4288654)
- [US4746911A](https://patents.google.com/patent/US4746911A/OSRAM)
- [SE424359B](https://patents.google.com/patent/SE424359B/esLanguage)
- [EP0060552B1](https://patents.google.com/patent/EP0060552B1/en)
- [EP0348920B1](https://patents.google.com/patent/EP0348920B1/enExample)
- [US3927351A](https://patents.google.com/patent/US3927351A/enExample)
- [US4013924](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/4013924)
- [EP2696183A2](https://patents.google.com/patent/EP2696183A2)
- [US3838593A](https://patents.google.com/patent/US3838593A/enExample)
- [US 12687263](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12687263)
- [US 12455208](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12455208)
- [US20250130134](https://patents.justia.com/patent/20250130134)
- [CN121999801A](https://www.goveda.com/patent/CN-121999801-A)
- [CN121993747A](https://www.goveda.com/patent/CN-121993747-A)
- [HOFOR article](https://doi.dk/en/innovation/artikel/hofor-bruger-ny-teknologi-til-at-opdage-utaetheder-i-fjernvarmeroer)
- Papers: linked by DOI or OpenAlex URL in section 2.