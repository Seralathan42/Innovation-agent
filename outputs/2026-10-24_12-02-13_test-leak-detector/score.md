# Score: 44 / 100

**Pass.** Likely range 35 to 53, based on how confident the agents were.

## Sub-scores

| Criterion | Agent | Score (1 to 5) | Confidence | Weight | Evidence |
|---|---|---|---|---|---|
| team | nabc | 2 | high | 16% | One doctoral researcher wants to found a company in 2027, the senior inventor will only advise, and nobody in the team has business experience. |
| novelty | ip | 2 | medium | 12% | Measuring section sound speed with active pulses between two sensors (NRC/Echologics/Mueller) and sensor-emitted calibration signals (Itron US5974862) are known, so only the combination is possibly new: nodes that automatically and repeatedly calibrate speed and attenuation and feed them into leak location in district heating. |
| need | nabc | 3 | medium | 12% | Operators clearly struggle to locate leaks (alarm wires broken or missing, drones winter-only, days of digging) and one operator wants a larger pilot, but losses and costs are not quantified. |
| benefits | nabc | 3 | medium | 12% | Field position error fell from 9.4 m to 2.1 m with about 120 EUR of parts per sensor, but price, installation cost, savings per leak and false-alarm handling at scale are not stated. |
| freedom to operate | ip | 3 | low | 10% | No blocking patent was found for Finland or the EU, but Mueller's active patents in the US (especially US11726064B2 on averaged impulses to measure speed of sound) could be close for US sales, and EP equivalents were not checked. |
| market size | market | 2 | medium | 10% | Finland has 16,690 km and Europe roughly 190,000 km of district heating network, but the reachable segment (older networks without working alarm wires) suggests only a few million euros a year in the Nordics, and the figures come from my own sensor-spacing and price assumptions. |
| technical maturity | ip | 4 | medium | 8% | A 4-month trial on 2.3 km of a real district heating network located 3 known leaks with 2.1 m mean error, but with only 6 prototype sensors built from off-the-shelf parts and an estimated (not measured) battery life. |
| route to market | market | 3 | medium | 6% | One utility has asked for a 2027 pilot and there are natural licensees or partners (Vexve, Gutermann or its distributors, Kamstrup), but utility procurement is slow, the team has no business experience, and the pre-filing publication puts IP at risk. |
| competition | market | 2 | medium | 6% | Alarm wires are standard on new pipes, Gutermann loggers already do nightly neighbour correlation on district heating networks via DWI, Kamstrup holds a 2026 US patent on acoustic district heating leak detection, and thermal surveys are established; the self-calibration is a real but narrow difference. |
| funding availability | funding | 3 | medium | 4% | One very strong option (Business Finland R2B) is expected in spring 2027 but not currently open, and the other options either close soon and fit only partly (research organisations and SMEs call, 18 Dec 2026), need a company (EIC Accelerator, start-up funding) or need an international consortium (CETP 2027). |
| funding fit | funding | 4 | medium | 4% | Field-validated TRL 5–6 results, a spin-off-minded doctoral researcher and an operator asking for a 2027 pilot match R2B's purpose and Aalto's eligibility well, but the lack of IP protection before an imminent publication, possible Kamstrup patents and no business experience in the team are real gaps. |

## Scorer's overall opinion

Independent holistic scores from 3 runs: 52, 52, 50. It counts for 25% of the final score.

- The field trial shows a clear technical gain (2.1 m vs 9.4 m position error). The sensors are cheap (about €120 each), and the host utility has asked about a 2027 pilot. The problem on older networks with broken alarm wires is real.
- IP is shaky. The individual building blocks are known: Mueller/Echologics patents cover active sound-speed measurement, and an expired Itron patent describes sensor-sent pulses. Patentability rests on a weak inventive step for the combination. The conference decision in December 2026 also forces an urgent filing before publication, and no patent search has been done.
- The market is niche, with perhaps a few million euros a year in the Nordics. The team has no business experience and only one founder, who is still finishing a doctorate. The evidence is thin: 3 known leaks, 6 sensors, one network. A clear funding path exists through Business Finland R2B.

## Verification

**Verified.** The verifier scored the invention 47 on its own, 3 points from the final score.

The four reports agree with one another, quote the disclosure accurately, and are open about what they did not check. My spot-checks held up: Mueller's US11726064B2 is active and has no EP family member listed, the Business Finland call for research organisations and SMEs does close on 18 Dec 2026, and Itron's US5974862 does describe a sensor sending a signal into the pipe to measure sound speed. The main weaknesses are that the funding and NABC reports are more optimistic than the IP evidence allows, and that technical maturity is scored a little high for a 6-sensor, 4-month trial.
- **novelty**: The score of 2 is right, but the IP report still calls US5974862 'per the search summary' and says the full text should be checked. I read the full text: it explicitly has a processor send a random token signal into the pipe as vibration and use the travel time to measure sound speed and sensor spacing. Sensor-sent active calibration is therefore confirmed prior art, and only the damping/attenuation measurement and the repeated recalibration over temperature might still be new. That makes inventive step weaker than the reports suggest, and the funding and NABC reports do not take it into account. (suggested score: 2)
- **technical_maturity**: A 4 means mature for TRL 5, but the evidence is 6 hand-built sensors, one network, one season and 3 known leaks. No unknown leak has been found. The 5-year battery life is only an estimate and has not been checked against the extra energy needed to send active pulses. Pump-noise false alarms are also unresolved. (suggested score: 3)
- **funding_fit**: The funding report rates R2B as 'very strong' and presents Kamstrup's patent as the main IP risk. The IP report finds Kamstrup a low risk and the real weakness to be prior art from Mueller and Itron, which could leave little patentable to license. R2B also needs a market study and a commercialisation lead, and neither exists yet, so fit is moderate rather than strong. (suggested score: 3)
- **benefits**: The benefit table leaves out the cost of the 2 false alarms in 4 months on 2.3 km (about 2.6 per km per year). Scaled to a network of hundreds of km, that could cancel out much of the time saved by more accurate location, so the score should note this as a material unknown. The score itself is acceptable. (suggested score: 3)

## How this is calculated

Each agent scores its own criteria from 1 to 5. The score is the weighted average of those, turned into 0 to 100, then blended with the scorer's overall opinion (25%). The verifier scores the same reports without seeing the final score. Weights and bands are in `scoring.json`. This is a structured opinion, not a validated prediction.
