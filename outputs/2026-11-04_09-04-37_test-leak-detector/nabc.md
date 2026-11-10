# Self-calibrating acoustic leak detection for district heating pipes

**Summary:** Battery-powered acoustic sensors in valve chambers find and locate leaks in district heating pipes. They calibrate themselves by sending known vibration pulses between neighbouring sensors, so they learn the real sound speed and damping of each pipe section.

*(The disclosure is marked as a fictional test case. Disclosure date 1 Oct 2026. Aalto Mechanical Engineering.)*

## Need
- **Who:** District heating network operators. The disclosure names the energy company that hosted the trial and no other customers.
- **Problem:** Leaks lose hot water and heat and are hard to find. Alarm wires are broken or missing in many older networks. Drone thermography only works in winter and gives a rough position. Manual listening is slow. Locating a leak can take days of digging.
- **Importance:** It is a real operational pain point, but the disclosure gives no figures for the cost of leaks, the water and heat lost, the digging costs, or the size of the network base. Importance and urgency: Not stated in numbers. One operator has asked about a larger pilot, which suggests genuine interest.

## Approach
- **Solution:** Clamp-on sensors sit 300–800 m apart in existing valve chambers. Each records pipe vibration for a few minutes every night, when the network is quiet.
- **What is new:** Each sensor sends a known pulse into the pipe, and its neighbours measure the travel speed and attenuation. The system learns the sound speed and damping of every pipe section. A server-side model then combines the night recordings with these learned values to flag leaks and estimate their position.
- **How it meets the need:** Existing correlators need these values entered by hand and are often wrong by 10–20%. That moves the estimated leak position by tens of metres. Self-calibration should give more accurate positions and work in networks without alarm wires.
- **Route to market:** Not stated beyond the doctoral researcher's wish to found a company after the doctorate (expected 2027).
  - Option A: a spin-off selling sensors plus a monitoring service. This fits the team's intent but needs a business lead.
  - Option B: a licence or sale to an existing leak-detection or network-monitoring vendor. This is a lower-effort fallback and could be tested early, since no other companies have been contacted.

## Benefits per costs
- **Accuracy:** In the field trial (2.3 km, 6 sensors, 4 months) the mean position error was 2.1 m. A manual correlator on the same data gave 9.4 m, about 4.5 times worse.
- **Detection:** All 3 known leaks were found. The lab rig detected simulated leaks of 0.5 l/min with under 1 m error.
- **Cost:** Part cost is about 120 EUR per sensor, built from off-the-shelf parts. Battery life is an estimated 5 years. At 300–800 m spacing, that is roughly 1.5–4 sensors per km, or about 150–500 EUR of hardware per km. This is my arithmetic from the disclosure, not a stated figure. Installation, server, software, service and pricing are Not stated.
- **Customer gain in euros:** Not stated. It could be estimated from days of digging avoided, and water and heat saved through earlier detection.
- **Caveats:** The evidence is thin. There were only 3 leaks, and 2 false alarms in 4 months, both from a pump station. The 5-year battery life is an estimate, not a measurement.

## Competition
- **Current alternatives:** Alarm wires in pre-insulated pipes, thermal drone flights, manual listening with ground microphones, and manual correlators.
- **Likely competitors:** Acoustic correlators and fixed acoustic loggers are widely used on drinking water pipes, per the disclosure. Vendors could adapt them to district heating. Named companies and products: Not stated, and I did not research them.
- **Why this is better:** It calibrates automatically, which avoids the 10–20% property errors. It does not rely on alarm wires, and it works in any season. It is also permanent and automated, not a periodic survey.
- **Weak points:** No patent search has been done. The claim that nobody does active-pulse calibration is the researchers' own belief. A vendor with an installed base could add this feature.

## Team
- **Dr. C. Example** is a staff scientist who owns 60% of the invention. This person wants to stay in research and could advise.
- **M.Sc. D. Example** is a doctoral researcher who owns 40%. This person wants to found a company after finishing the doctorate in 2027.
- **Missing:** Nobody has business experience. There is no commercial lead, no sales or customer-development capability, and no hardware, product or industrialisation expertise. Sensor certification and manufacturing are Not stated. The only founder candidate is not available full-time until 2027.

## Readiness and funding
- **Readiness:** The lab rig and a 4-month field trial have been done (roughly TRL 5). The sensors are built from off-the-shelf parts. Scale is small: 6 sensors on 2.3 km. Tests on other pipe types, network sizes and noise conditions are Not stated.
- **Funding so far:** Research Council of Finland project (2024–2027). The energy company gave network access but no money.
- **Timing:** A conference paper was submitted on 15 Sep 2026, with a decision in December 2026. Publication could damage novelty for patenting. A patent filing should be considered before any public disclosure.
- **Possible next funding:** Not stated in the disclosure. Candidate sources are Business Finland, Research to Business or Aalto proof-of-concept funding, and a paid pilot with the energy company. A pilot is expected in 2027. These are my suggestions, not stated plans.

## Assessment
**Strengths**
- A clear technical differentiator with measured field evidence (2.1 m against 9.4 m).
- A real customer is asking for a larger pilot.
- Low hardware cost and a long battery life, if confirmed.
- It works where alarm wires are missing.

**Risks**
- The team has no business capability, and the founder is not free until 2027.
- Small trial: 3 leaks and 6 sensors.
- No patent search, and a publication decision is due in December 2026.
- Only one customer contact, and no figures on market size, willingness to pay or pricing.
- Sensor installation, certification, support and the server and software service are not covered.
- False alarms from pump stations and other noise sources may grow with scale.
- Competitors with existing installed bases.

**Questions for the researchers**
1. What exactly was submitted to the conference, and can a patent application be filed before it is public? Have you done any prior-art search?
2. What does the energy company want to pay for or commit to in the 2027 pilot? Who is the contact, and what are the terms on data and IP?
3. How would the system handle different pipe sizes, branches, pump noise and other leaks? What would reduce the false alarms?
4. What would a customer pay in total, including installation and software? How many leaks and how much digging cost per year would it save for a typical operator?
5. Who would join the venture as a business lead? Is the doctoral researcher committed to a spin-off, or open to licensing?
