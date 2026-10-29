# NABC summary: Self-calibrating acoustic leak detection for district heating pipes

**Disclosure date:** 1 Oct 2026 · **Department:** Mechanical Engineering · **Inventors:** Dr. C. Example (60%), M.Sc. D. Example (40%)

**One-sentence summary:** Battery-powered acoustic sensors are clamped onto district heating pipes in existing valve chambers, and they measure each pipe section's sound speed and damping themselves with active pulses, so the system can find leaks much more precisely than correlators that rely on values entered by hand.

> ⚠️ **Urgent IP point:** A conference paper was submitted on 15 Sep 2026, two weeks before this disclosure. The decision is expected in December 2026. A patent application needs to be filed **before the paper or any preprint becomes public**. Europe has no grace period. Check right away whether a preprint or abstract is already online.

---

## Need
- **Who has the problem:** District heating network operators, mostly energy companies and municipal utilities. They run underground pre-insulated steel pipes.
- **What the problem is:** Leaks lose hot water and heat, and they are hard to find. The current tools all have gaps:
  - Alarm wires built into the pipes are broken or missing in many older networks.
  - Thermal drone flights only work in winter and give a rough location.
  - Listening with ground microphones is manual work.
  - Finding a leak "can take days of digging."
- **How important it is to them:** Clearly a real operational pain. However, the cost of a leak (lost water and heat, digging, repairs) and the number of leaks per km per year are **not stated**. Market size and the number of target operators are also **not stated**.
- **Validation:** One operator hosted the field trial and has asked about a larger pilot in 2027. That is a positive signal, but from a single customer only.

## Approach
- **Solution:**
  - Sensors are placed 300–800 m apart in existing valve chambers, so no excavation is needed.
  - They record pipe vibration for a few minutes each night, when the network is quiet.
  - Each sensor sends a known vibration pulse. Its neighbours measure how fast the pulse travels and how much it weakens. This gives the real sound speed and damping of each section, which vary with pipe size, insulation, age and water temperature.
  - A small server-side model combines the night recordings with these learned pipe properties to flag leaks and locate them.
- **How it meets the need:** It works year-round and does not depend on alarm wires. It removes the 10–20% error from hand-entered pipe parameters, which today shifts leak positions by tens of metres. The result is a narrower area to dig.
- **Likely route to market:** The team's stated preference is a **spin-off**: the doctoral researcher wants to found a company after the doctorate (expected 2027). Licensing the self-calibration method to an existing leak-detection or monitoring vendor is a credible alternative, since its value largely lies in improving existing correlator and logger hardware. The disclosure does not discuss licensing or sale.

## Benefits per costs
| Item | Figure from disclosure |
|---|---|
| Location accuracy (field) | Mean error **2.1 m**, versus **9.4 m** for a manual correlator on the same data (about 4.5× better) |
| Location accuracy (lab, DN100, 40 m) | Under 1 m; leaks of 0.5 l/min detected |
| False alarms | 2 in 4 months over 2.3 km, both caused by a pump station |
| Sensor parts cost | About 120 EUR per sensor (off-the-shelf prototype parts) |
| Battery life | About 5 years (an estimate, not measured) |

- **Derived figure (advisor's calculation, not in the disclosure):** At 300–800 m spacing, about 1.3–3.3 sensors are needed per km of pipe, which is roughly **150–400 EUR of parts per km**. Installation, servers and software are not included.
- **Customer gain:** Less digging, faster repairs, and less water and heat lost. The euro value of these gains is **not stated**.
- **Not stated:** Selling price, business model (hardware sale or subscription), installation cost, and the operator's current cost per leak.

## Competition
- **Current alternatives:**
  - Alarm wires in pre-insulated pipes
  - Thermal drone surveys
  - Manual ground microphones
  - Acoustic leak correlators, which are widely used for drinking water pipes
  - Fixed acoustic loggers from several vendors
- **Why this is claimed to be better:**
  - Automatic, active calibration of each pipe section, which the inventors are not aware of elsewhere
  - Works all year
  - Uses existing chambers
  - Shows better location accuracy than a manual correlator on the same data
- **Gaps:**
  - **No patent search has been done.**
  - Competing vendors are not named.
  - Not stated whether existing logger vendors already serve district heating or already offer any form of automatic calibration.
- **Likely future alternatives:** Not stated. Established water-leak vendors could add similar calibration, and fibre-optic sensing is another possible alternative. This is an advisor assumption that needs checking.

## Team
- **Dr. C. Example** (staff scientist): wants to stay in research but could advise.
- **M.Sc. D. Example** (doctoral researcher): a potential founder, available after the doctorate in 2027.
- **Missing:**
  - Nobody on the team has business experience. A commercial lead or co-founder is needed.
  - Product engineering skills are not stated. This covers ruggedised hardware, certification for use in chambers, and the software platform.
  - Experience in sales to utilities is not stated.

## Readiness and funding
- **Readiness:** Lab rig plus a 4-month field trial with 6 sensors on 2.3 km of network. This is roughly a prototype validated in a relevant environment (about TRL 5–6, advisor's estimate). The sensors are off-the-shelf prototypes, and battery life is estimated, not measured.
- **Current funding:** A Research Council of Finland project (2024–2027). The energy company provided access to its test network but no money.
- **Possible next funding (advisor suggestion):** Business Finland Research to Business (R2B) to validate commercial potential and build the spin-off team. The 2027 pilot with the energy company could also be paid or co-funded. Seed or pre-seed funding would come after a founder and business lead are in place.

## Assessment
**Main strengths**
- Clear, measurable technical advantage: about 4.5× better location accuracy in the field.
- Low-cost hardware that fits existing infrastructure: around 120 EUR in parts per sensor, installed in existing chambers.
- Real customer pull: the trial host wants a larger pilot.
- A motivated potential founder.

**Main risks**
- **IP:** The submitted paper could make the invention public before a patent is filed. No patent search has been done. The energy company's rights from the trial are unclear.
- **Limited evidence:**
  - Only 3 leaks in one network, and they were *already known*. Finding unknown leaks has not been demonstrated.
  - False alarms may scale badly on large networks.
  - Battery life is estimated.
- **Team:** No business experience, and the founder is not available until 2027.
- **Market:** Size, pricing and willingness to pay are not stated. All interest so far comes from one customer.

**Questions for the researchers**
1. Is the submitted paper, or any preprint or abstract, already public? Exactly what does it reveal about the self-calibration method? Can publication be delayed until a patent application is filed?
2. What agreement covers the field trial with the energy company (confidentiality, IP, data rights)? Would the 2027 pilot be paid?
3. Who are the main vendors of fixed acoustic loggers and correlators, and do any of them already serve district heating or offer automatic calibration? What is distinctive enough to protect?
4. How much does a leak cost an operator (water, heat, digging), and what would they pay per km per year? Have any operators other than the trial host been asked?
5. Do you prefer a spin-off or a licence? Who could join the doctoral researcher as a business co-founder, and what would make the system ready to sell (hardware, false-alarm handling, scaling)?