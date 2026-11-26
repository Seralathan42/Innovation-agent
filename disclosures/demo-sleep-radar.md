# Invention disclosure (FICTIONAL DEMO EXAMPLE)

**Title:** Contactless sleep apnea screening with a bedside radar that tells obstructive from central apnea

**Inventors:** M. Example (doctoral researcher), Dr. S. Example (postdoc) and Prof. K. Example, Department of Electronics and Nanoengineering

**Date:** 2026-11-02

## The problem
Sleep apnea affects close to a billion people worldwide, and most of them are never diagnosed. The standard test, polysomnography, means a night in a sleep lab wired to a dozen sensors, and waiting lists in Finland are often several months long. Home tests still need belts, a nasal tube and a finger clip, which many patients find hard to sleep with. Treatment also depends on the type of apnea: obstructive apnea (the airway closes) is treated with a CPAP machine, while central apnea (the brain stops sending the signal to breathe) needs a different treatment, and today telling the two apart needs chest and abdomen belts.

## The invention
A small bedside device with a low-power 60 GHz radar chip watches the sleeper's chest and abdomen from up to two metres away, with nothing worn on the body. Our signal processing separates the movement of the chest from the movement of the abdomen. During obstructive apnea the two move against each other as the person tries to breathe against a closed airway; during central apnea both stop. A small neural network running on the device classifies each event, so no raw radar data leaves the bedroom. It reports the apnea-hypopnea index (AHI) and the share of obstructive and central events.

## Results so far
- Tested on 46 nights with 31 patients at a Finnish university hospital sleep unit, side by side with polysomnography.
- AHI agreed with polysomnography within 4 events per hour in 91% of nights.
- Obstructive and central events were told apart correctly 87% of the time. We have not found another contactless method that reports this split.
- A working prototype costs about EUR 60 in parts.

## Prior publications
None. A conference paper is planned for June 2027. Nothing has been filed yet.

## Funding
Research Council of Finland project on radar sensing (2024 to 2027). No commercialisation funding yet.

## Commercial interest
The hospital sleep unit wants to continue with a larger study. Two Finnish health technology companies have asked about the results after a seminar talk. No agreements have been made.

## Team
The doctoral researcher wants to found a company after the PhD and has completed the Aalto Ventures Program. The postdoc built the classifier and would join. The professor will stay in academia and supports a spin-off. Nobody on the team has medical device regulatory experience (CE marking under the EU Medical Device Regulation).
