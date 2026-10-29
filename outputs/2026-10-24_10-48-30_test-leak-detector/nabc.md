# NABC summary: Self-calibrating acoustic leak detection for district heating pipes

**Disclosure date:** 1 Oct 2026 · **Department:** Mechanical Engineering · **Inventors:** Dr C. Example (60%), M.Sc. D. Example (40%)
*(The form is marked as a fictional test disclosure.)*

> ⚠️ **Urgent: patent filing before publication.** A conference paper was submitted on 15 Sep 2026 and the decision is due in **December 2026**. In Europe, any public disclosure before filing destroys novelty, so a priority application must be filed before the paper or any preprint is published. Find out today what the paper reveals and whether any preprint or talk has already happened.

**One-sentence summary:** Battery-powered acoustic sensors clamped onto district heating pipes send known vibration pulses to each other to measure each pipe section's real sound speed and damping, so they can find leaks to within about 2 m without the hand-entered settings that make today's correlators inaccurate.

## Need
- **Who:** District heating network operators (energy companies and municipal utilities), especially those with older networks.
- **Problem:** Leaks waste hot water and heat and are hard to find. Current methods each have gaps:
  - Built-in alarm wires are often broken or missing in older networks.
  - Thermal drone flights only work in winter and give a rough location.
  - Listening by hand with ground microphones is slow.
  - Finding a leak "can take days of digging."
- **How important:** The disclosure gives no figures. It does not state the cost of a leak, the cost of digging, the water or heat lost, or the market size. One operator has shown real interest by asking about a larger pilot in 2027.

## Approach
- **Solution:** Sensors are clamped onto pipes in existing valve chambers, 300–800 m apart. Each one records for a few minutes every night, when the network is quiet.
- **What is new:** Each sensor sends a known pulse along the pipe, and its neighbours measure how fast the pulse travels and how much it weakens. This gives the real properties of each pipe section, which change with pipe size, insulation, age and water temperature. A small model on the server combines these values with the night recordings to flag leaks and locate them.
- **How it meets the need:** Monitoring is continuous and works all year. It does not depend on alarm wires, needs no digging to install, and gives a more precise location, so less digging is needed to reach the leak.
- **Likely route to market:** There are two options:
  - **Spin-off:** The doctoral researcher wants to found a company after the doctorate (expected 2027). This would probably be a hardware plus monitoring service.
  - **Licence:** License to an established vendor of leak-detection or network-monitoring products.

  The choice depends on finding a business co-founder and on how strong the patent is. The disclosure does not choose between them.

## Benefits per costs
| Item | From the disclosure |
|---|---|
| Location accuracy (field trial) | Average error **2.1 m**, against **9.4 m** for a manual correlator on the same data (about 4.5× better) |
| Detection (lab) | Leaks of 0.5 l/min, error under 1 m |
| False alarms | 2 in 4 months on 2.3 km, both caused by a pump station |
| Sensor part cost | About **€120** per sensor (off-the-shelf parts, prototype) |
| Sensor parts per km of network | About **€150–400** (my calculation: 1.25–3.3 sensors per km at 300–800 m spacing) |
| Battery life | About 5 years (**estimated, not measured**) |
| Installation | Uses existing valve chambers, no digging |

- **Customer gain:** Less digging per leak, faster repairs and less water and heat lost. The money value of this is **not stated**.
- **Not stated:** Selling price, installation cost, server or software cost, maintenance, and the cost of a typical leak or dig.

## Competition
- **Current alternatives:** Alarm wires, thermal drone flights, ground microphones, and portable acoustic correlators. These correlators are common for drinking water pipes but need pipe settings entered by hand, which are often 10–20% wrong.
- **Likely alternatives:** Vendors already sell fixed acoustic loggers for water networks. They could adapt these for district heating or add their own automatic calibration. Fibre-optic sensing and analysis of network flow and pressure data could also compete, though the disclosure does not discuss them.
- **Why this is better:** It measures the pipe properties of each section automatically with active pulses. The inventors know of no system that does this. It works all year, and in the trial it gave about 4.5× better location accuracy.
- **Caveat:** **No patent search has been done**, so novelty is not confirmed. The idea could also be copied unless the claims are well drafted.

## Team
- **Dr C. Example** (staff scientist, 60%): wants to stay in research but could act as an adviser.
- **D. Example** (doctoral researcher, 40%): wants to start a company after finishing in 2027.
- **What is missing:** Nobody has business experience. There is no commercial lead, and no stated skills in hardware productisation, certification, manufacturing or sales to utilities. The team needs a business co-founder or CEO.

## Readiness and funding
- **Readiness:** Validated in the lab and in a field trial on a real network (2.3 km, 6 sensors, 4 months, 3 known leaks found). Roughly TRL 5–6 (my estimate). The hardware is a prototype built from off-the-shelf parts.
- **Current funding:** Research Council of Finland project (2024–2027). The energy company gave access to its network but no money.
- **Possible next funding:**
  - Aalto internal proof-of-concept funding.
  - Business Finland Research-to-Business (R2B) for commercial validation and team building.
  - A paid or co-funded 2027 pilot with the host energy company.
  - Later, a spin-off could seek pre-seed funding.
  - Not stated in the disclosure: these are suggestions.
- **Ownership to check:** Whether there is any agreement with the energy company about results or IP. Not stated.

## Assessment
**Main strengths**
- A clear, specific technical advance (automatic calibration of each pipe section) with field data on a real network that shows a large accuracy gain.
- Low part cost and easy installation in existing valve chambers.
- A customer is already engaged and has asked about a 2027 pilot.
- A motivated potential founder.

**Main risks**
- **Patent timing:** the paper could be published before a patent is filed.
- Novelty is unconfirmed because no patent search has been done, and established vendors could build something similar.
- Thin evidence: only 3 leaks, one network, and a battery life that is estimated rather than measured. False alarms from pumps need solving before scaling up.
- No business skills in the team, and the potential founder is not available until 2027.
- The economic value to customers and the market size are not stated.

**Questions for the researchers**
1. Exactly what does the submitted paper disclose, and has anything been made public already (preprint, talk, thesis, poster)? Can publication be delayed or the paper narrowed until a patent is filed?
2. Is there any written agreement with the energy company about trial results, data or IP? What would the 2027 pilot look like, and would they pay for it?
3. What does a leak and its dig cost an operator, and what price per km or per sensor do you think they would pay? Have other operators or vendors been contacted?
4. How will you stop pump stations and other noise sources causing false alarms? Does the method work on supply and return pipes, all pipe sizes, and branched networks?
5. Who could be the business lead? Would D. Example commit full time from 2027? Do you prefer a spin-off or a licence?