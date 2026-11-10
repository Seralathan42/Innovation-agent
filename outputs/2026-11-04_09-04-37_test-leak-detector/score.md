# Score: 48 / 100

**Needs more information.** Likely range 35 to 62, based on how confident the agents were.

## Sub-scores

| Criterion | Agent | Score (1 to 5) | Confidence | Weight | Evidence |
|---|---|---|---|---|---|
| team | nabc | 2 | high | 16% | Two researchers with solid technical results, but no business experience, the staff scientist will not lead, and the only founder candidate is free only after 2027. |
| novelty | ip | 3 | low | 12% | Active pulses, speed-free localisation and acoustic district heating monitoring are each known, but I found no source combining autonomous per-section speed and damping learning with permanent clamp-on sensors; only snippets of most patents were read. |
| need | nabc | 3 | low | 12% | The problem is credible, with weak or missing alternatives in older networks and an operator asking for a pilot, but the disclosure gives no figures for leak costs or market size. |
| benefits | nabc | 4 | medium | 12% | Field trial error of 2.1 m against 9.4 m for a manual correlator, with about 120 EUR parts per sensor, but only 3 leaks were tested and total customer cost and savings are not stated. |
| freedom to operate | ip | 3 | low | 10% | No patent found that clearly blocks the concept, but active Itron (US11788919, to about 2041) and Kamstrup families partly overlap and no professional FTO search or country-level status check has been done. |
| market size | market | 2 | low | 10% | Finnish network is 16,690 km (Finnish Energy 2024), so full-coverage hardware is only a few million euros, and I found no European market-size figures or Eurostat data. |
| technical maturity | ip | 3 | medium | 8% | Lab rig and a 4-month field trial on 2.3 km with 6 sensors show a working prototype (about TRL 5 by my estimate), but with only 3 known leaks and estimated battery life and cost. |
| route to market | market | 3 | low | 6% | A host energy company has asked about a 2027 pilot and DH utilities are a concentrated buyer group, but the team has no business experience and utilities buy slowly. |
| competition | market | 3 | low | 6% | Alarm wires, drones, manual correlators and some acoustic DH patents exist and the self-calibrating pulse approach looks new, but no patent search has been done. |
| funding availability | funding | 2 | medium | 4% | The autumn 2026 Business Finland R2B call has closed and the RCF Proof of Concept call has closed with possibly no 2027 round, so the main fit is a likely spring 2027 R2B round whose dates are unconfirmed. |
| funding fit | funding | 3 | medium | 4% | A validated field trial and a customer interested in a pilot fit R2B well, but there is no IP filing or business lead, and the RCF Proof of Concept and Horizon Proof of market calls do not fit the project's funding history. |

## Scorer's overall opinion

Independent holistic scores from 3 runs: 56, 57, 56. It counts for 25% of the final score.

- Real pain point with strong field evidence: 2.1 m mean error against 9.4 m for a manual correlator, and 3 of 3 known leaks found. A host utility has asked for a 2027 pilot, and hardware costs about €120 per sensor.
- Novelty is only partly supported. Older patents use active pulses and calibration, and the field is crowded with Itron, Xylem and Kamstrup. No patent search has been done, and the conference paper decision in December 2026 could destroy novelty before filing.
- The team has no business experience and the only founder candidate is free in 2027. The evidence is thin (6 sensors, 3 leaks, one network), and there is no market sizing or pricing. Business Finland R2B is a plausible funding route.

## Verification

**Verified.** The verifier scored the invention 58 on its own, 10 points from the final score.

The four reports match the disclosure closely, state their gaps openly, and the spot-checks support their key facts: the R2B autumn 2026 call closed on 16 September with decisions in January 2027, the next call is likely in early March 2027 but unconfirmed, and Itron's US11788919 does cover coordinated acoustic sampling at low flow. Two scores rest on searches that were too narrow or read the funding timing too harshly: market size looked only at Finland, and funding availability treated a call due in about four months as a weak option.
- **market_size**: The score rests on Finnish hardware parts cost only (about 2.5 to 6.7 million euros), which is the wrong measure for a sensor-plus-service business. The report also says no European pipe length was found, but Euroheat & Power gives about 190,000 km across about 17,000 networks, and another source gives about 199,000 km. At 1.5 to 4 sensors per km that is roughly 0.3 to 0.75 million sensor positions in Europe. Even with modest unit prices and service fees, that is a niche but meaningful market in the hundreds of millions of euros. (suggested score: 3)
- **funding_availability**: A well-fitting, grant-based route (R2B, 80% of eligible costs) is very likely open with a deadline around early March 2027, about four months away. Past spring deadlines were 6 March 2024 and 5 March 2025, and Business Finland says its 2027 R&D budget will rise to nearly 1 billion euros. That timing suits the planned IP filing and customer interviews. Scoring this 2 treats the closed autumn round as more important than it is. (suggested score: 3)
- **benefits**: The 2.1 m versus 9.4 m result comes from only 3 known leaks on one 2.3 km network. The reports do not ask whether the manual correlator was given good sound-speed values, which would make the comparison fair. Battery life and unit cost are estimates, and there were 2 false alarms in 4 months. A 4 is at the generous end, and confidence should be low rather than medium. (suggested score: 3)

## How this is calculated

Each agent scores its own criteria from 1 to 5. The score is the weighted average of those, turned into 0 to 100, then blended with the scorer's overall opinion (25%). The verifier scores the same reports without seeing the final score. Weights and bands are in `scoring.json`. This is a structured opinion, not a validated prediction.
