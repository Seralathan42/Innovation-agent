# Assessment: Self-calibrating acoustic leak detection for district heating pipes

*Confidential. Based only on the disclosure (1 Oct 2026) and the three outside reports. Today is 2026-10-28.*

## 1. Verdict

The invention looks promising but is not yet protectable on a safe footing. The self-calibration idea (active pulses to learn sound speed and damping per pipe section) does not appear in the reports, and the field results (2.1 m vs 9.4 m error) address a real weakness of existing correlators. However, a conference paper was submitted on 15 September 2026, so the publication clock is the most urgent issue, and the team has no business experience and no patent search yet.

## 2. Novelty

**Important limit:** the outside agents saw only the field, not the invention's features. Their reports map the district heating leak detection landscape. They do not show that the self-calibration feature is new. A confidential professional patent search is still needed. The patent report itself says its search was shallow (four searches, one patent read in full, assignees not searched).

**Closest items in the reports, and what they already show**

| Item | What it already shows | Relevance |
|---|---|---|
| [US20250130134](https://patents.justia.com/patent/20250130134) (unverified, snippet only) | Multiple acoustic sensors on heating and water networks, locating leaks by cross-correlation | Closest to the overall system. Need to read claims to see whether it covers sound-speed estimation or active pulses. |
| [US 12687263](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12687263) (unverified) | Permanently installed acoustic sensing in a DH network, two spaced sensors, direction discrimination | Shows fixed acoustic monitoring in DH. Different sensor type (heat meter). |
| [US 12455208](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12455208) (unverified) | Ultrasonic flow meters used as microphones in the pipe network | Fixed acoustic listening, not self-calibrating as far as the snippet shows. |
| [US3838593A](https://patents.google.com/patent/US3838593A/enExample) | General acoustic leak location and detection | Old, generic. Likely expired. |
| [Kupperman and Karvelas 1988](https://openalex.org/W1509174850) | Acoustic leak detection in a DH system, detection at several hundred metres, location within a few metres | Shows that acoustic DH detection with sensors and metre-level location is old. The disclosure's accuracy claim alone is not novel. |
| CN121999801A / CN121993747A (unverified) | Acoustic arrays with AI for locating leaks in heating pipelines | Overlaps with the server-side model. |
| [Koolivand et al. 2024](https://doi.org/10.1109/cicc60959.2024.10528962) | Active pulse and reflection (TDR) for locating faults on a wire in DH | Uses active pulses, but electrically on the alarm wire, not acoustically in the pipe. Relevant to how a reviewer might see "active pulse" as known. |
| Vexve iSENSE Pulse (market report) | Pulse measurement on alarm wires | Same point: electrical pulses are established. |
| Alarm-wire patents (US7960978B2 and the older family) | Wire-based moisture detection | Different mechanism, background only. |
| Hydraulic and ML papers (Jallal 2023/2025, Liu 2025, Xue 2020) | ML/hydraulic models for detection and localisation | Overlap with the "small model on the server" only. |

**Features that appear already known (in the field)**
- Battery-powered or fixed acoustic sensors on DH or water pipes, with cross-correlation to locate leaks.
- Acoustic detection in DH with metre-scale location.
- Active pulses for locating faults, but electrical, not acoustic.
- ML-based leak detection and localisation.

**Features that look new, as far as the reports show**
- Sensors sending known vibration pulses into the pipe so neighbours learn sound speed and damping of each section automatically.
- Using the learned properties in the leak-position estimate, replacing manually entered values.
- Nightly recording scheduling plus self-calibration on clamp-on sensors in valve chambers.

The patent report states it found no prior art combining approaches, but says this is a limit of the search, not evidence. Self-calibration of velocity in correlators may exist in water-pipe literature or in the unread claims of US20250130134 and the Chinese filings. The reports did not search for it.

## 3. Market fit

**Customers.** The buyers are DH operators. Finland has 16,690 km of network (2024), 440 enterprises in NACE D35.3 (many very small), and 8–9% heat losses in distribution ([Energiateollisuus](https://energia.fi/?p=53217)). The host energy company already wants a larger pilot in 2027, which is a real signal.

**Where it fits.** The market report names the likely opening as old, bare or non-wired pipes where alarm wires have degraded, and where an acoustic or sensor-plus-software approach is useful. That matches the disclosure's problem statement (broken or missing alarm wires in older networks). This is the report's inference, not a sourced fact.

**Competitors.** Incumbents sell alarm-wire systems: Kingspan LOGSTOR (Detect X6, hosted surveillance), BRUGG LEAKGUARD (including a battery/LTE Cloud model), Brandes, Mittel, and Finnish Vexve (iSENSE Pulse). They bundle monitoring with pipe sales, and claim more than 80% in-insulation coverage (Brandes, 2014, vendor claim). Other approaches: satellite/thermal surveys (Fortum/Advian), With the Grid's remote device, and contractor correlators. The invention differs by not needing a wire and by improving position accuracy, which could save excavation. It could also be complementary to wire systems rather than a replacement.

**Market size.** The only leak-detection figures ($0.8 bn in 2025 rising to $1.5 bn by 2034) come from a low-reliability publisher whose reports conflict with each other. Do not use them in a business case. No price data exists in the report. The sensor cost estimate of about 120 EUR (off-the-shelf parts) cannot be compared to competitor prices yet.

**Brakes.** Sensors are tied to pipe suppliers' ecosystems and EN 14419 wire standards. Small municipal operators have little budget. The sale will probably need pilot references.

## 4. Funding fit

Deadlines as stated in the funding report; none of the call texts were read in full.

1. **Business Finland Research to Business (R2B)** is the best fit. It pays 80% of costs (typically EUR 400k–700k) for customer discovery, field testing and team building. Applicant must be the research organisation. Call 2/2026 closed on 16 September 2026 (decisions January 2027), so the next window is expected around spring 2027 (date unconfirmed). Start preparing now. [Call 2/2026](https://www.businessfinland.fi/en/services/funding/calls/2026/r2b-funding-call-2-2026/).
2. **Business Finland Co-Innovation / Veturi route.** The 2027 pilot with the host energy company is a natural basis, but the timing and eligibility need checking with Business Finland. [Overview](https://www.businessfinland.fi/en/whats-new/news/2026/what-do-business-finlands-funding-services-look-like-at-the-beginning-of-2026/).
3. **Business Finland Sprint** is for small companies, so it becomes relevant only after a spin-out exists. The 2026 pilot ran 2.3–31.8.2026, and whether it continues is unknown.
4. **HORIZON-BRIDGING-2027-01-12** (AI-driven energy platforms, Apply AI): deadline 2027-02-16. Needs a consortium with utilities, and the AI scope is a moderate fit. Probably too early for this team.
5. **HORIZON-CL6-2027-02-CLIMATE-01-two-stage** (Water Resilience): opens 2027-02-04, deadline 2027-09-14. Stretch for a closed-loop heating network.
6. **Not recommended now:** I3-2023-INV2a (deadline 2026-11-09, needs multi-region partnership); MSCA Doctoral Networks (training, not commercialisation; 2026-11-24 and 2027-11-23); Climate-Neutral Cities platform call (not a technology call); CL5 building/waste heat topics (weak fit).
7. The Research Council of Finland, TTO funds, Tesi and others were not verified in the report. Check those through Aalto Innovation directly. The EIC was not found in the call listings, so its status is unknown.

The closest precedent is the EU-funded Jensen Predictive Maintenance project (EUR 50,000, 2015–16, IoT monitoring and fault location for DH pipes), which suggests that this topic has been funded before.

## 5. Risks and next steps

**Risks**
- **Publication and novelty.** A conference paper was submitted on 15 September 2026. Whether submission itself is public (preprint, public proceedings or talk) is unknown. If any public disclosure occurs before a patent application is filed, novelty in most jurisdictions is lost. The decision is expected in December 2026, and publication would follow.
- **Freedom to operate and prior art.** US20250130134 and the unread Chinese filings could cover parts of the system. Claims were not read.
- **Ownership.** The research was funded by the Research Council of Finland, and an energy company provided a test network. Rights under the university's policy and any agreement with the energy company (data, test access, inventions) need to be confirmed. Even though the company gave no money, there may be terms attached to the test access.
- **Evidence base is small.** The field trial had 6 sensors, 2.3 km, 3 known leaks and 4 months. Two false alarms came from a pump station. Battery life is estimated, not measured. Long-term pulse injection effects on battery and pipe are untested.
- **Generalisation.** Whether self-calibration holds across pipe sizes, twin pipes, bends, branches, and insulation types is not shown. Only DN100 in the lab is reported.
- **Team.** No business experience, the doctoral researcher is expected to leave in 2027, and the main scientist will stay in research.
- **Market data is weak** (see section 3).

**Next steps**
1. **Immediately:** confirm what has been made public and when. Ask the authors to hold any public posting. If a patent application is intended, file a priority application before any publication or presentation. Talk to the conference about camera-ready timing.
2. Commission a confidential professional patent search focused on the invention's own features: self-calibration of sound speed/damping, active acoustic pulses, and a read of US20250130134, US 12687263, US 12455208 and the Chinese filings, using the CPC classes the patent report lists (G01M3/24, G01M3/28, F17D5/02, F24D10/00).
3. Review the agreement with the energy company and the Research Council project terms regarding IP.
4. Discuss with the energy company a pilot agreement for 2027 that settles IP and data terms before the pilot starts. Do not share details beyond what is public or covered by an NDA.
5. Prepare an R2B application for the spring 2027 window; confirm the date with Business Finland.
6. Interview two or three Finnish operators and get prices for LOGSTOR, Vexve and BRUGG systems (the market report's own suggestion).
7. Check EU Directive 2023/1791 Article 26 for heat-loss rules.
8. Consider support for the doctoral researcher on business skills and a possible co-founder.

## 6. Questions for the researchers

1. Has the conference paper, an abstract, a preprint, a poster or a talk made any part of the method public? Who has seen the details, and under what confidentiality?
2. What exactly does the paper describe, in particular the calibration pulses?
3. Who owns what under the Research Council project and the university's rules? What does the agreement with the energy company say about inventions, data and publication?
4. Is the calibration pulse method truly new to you? Have you seen it for water pipes, or in correlator products or literature?
5. How were the pulses generated (actuator type), and what are the energy cost per pulse and the effect on battery life? Is 5 years measured or modelled?
6. How well does calibration work on branches, bends, valves, twin pipes and different diameters? How stable are the learned values over seasons and temperature?
7. In the field trial, how were the 3 leak positions established, and were the manual correlator inputs set by the same standard practice an operator would use? Were there leaks the system missed?
8. How would the pump-station false alarms be handled in operation?
9. How does the server model work, and what training data did it need? Does each new network need retraining?
10. What does the energy company want from a larger pilot (scale, timing, budget), and would it pay?
11. Would you see the product as a sensor-plus-service offer, software licensed to existing vendors, or a complement to alarm-wire systems? Have any pipe makers or meter vendors been in touch?
12. What is the doctoral researcher's realistic plan and timeline, and how much time can each of you commit to a pilot and to an R2B application?