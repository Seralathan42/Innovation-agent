# First screening: water-based lignin binder for Li-ion cathodes (NMC811)

*Aalto Innovation, technology and IP screening. Not a legal opinion. Confidential.*

**Search note:** To protect the disclosure, all searches used only general terms (lignin, binder, cathode, aqueous, NMC, company names). The disclosure doesn't say how the lignin is chemically modified. Several conclusions below depend on that answer, so the inventors need to supply it.

---

## 1. Technology in plain words

**What it does.** A battery cathode is made by coating a paste of active particles, carbon and a binder ("glue") onto aluminium foil. The usual glue is PVDF, a fluorinated plastic that has to be dissolved in NMP. NMP is a toxic, costly solvent, and recovering it takes energy-hungry drying ovens. PVDF also faces pressure from PFAS restrictions. The invention swaps PVDF for kraft lignin, a cheap by-product of pulp mills. The lignin is chemically modified so that it dissolves in water and sticks well to nickel-rich NMC811 particles. The whole slurry is water-based.

**Claimed results (lab scale):**
- 91% capacity kept after 500 cycles in coin cells, against 89% for PVDF.
- Peel strength similar to PVDF.
- Cheaper material and lower drying energy.

**What is new compared with the state of the art:**
- Lignin binders are well known for **anodes** (Borregaard, South China University of Technology, SUSTech) and have been shown for **LFP and NMC111 cathodes** (RISE/KTH; NTNU/UCL).
- What looks new is a **modified kraft lignin that works with Ni-rich NMC811 in water over 500 cycles**. That is the hardest case: Ni-rich materials leach lithium in water, push the pH up and corrode aluminium foil.
- The real inventive step is probably **the specific modification chemistry**, plus any slurry measures that deal with NMC811's sensitivity to water. Neither is described in the disclosure.

**TRL estimate: 3 (moving towards 4).**
- Proof of concept exists: coin cells, 500 cycles, peel tests, 50 g binder batches.
- There is no pouch or multi-layer cell, no roll-to-roll coating, no testing at industrial electrode loadings, and no shown reproducibility across lignin batches.
- A 2% difference over PVDF in lab coin cells isn't conclusive evidence of better performance. "Comparable to PVDF" is a safer claim.

---

## 2. Patent landscape

| Number | Owner | Priority | Status (Google Patents) | One-line summary |
|---|---|---|---|---|
| [EP3266057B1](https://patents.google.com/patent/EP3266057B1/en) / [US10439204B2](https://patents.google.com/patent/US10439204B2/en) (also CN, SE, WO) | RISE Innventia AB (Sweden) | 2015 | **Granted, active.** EP expires around 2036-03; US adjusted expiry 2036-06 | Water-based electrode slurry with isolated (e.g. LignoBoost kraft) lignin as binder, pre-treated to remove electrolyte-soluble fractions below 1000 Da. **Covers cathodes, explicitly including LiNi₁₋ₓ₋ᵧMnₓCoᵧO₂ (NMC) and NCA.** Has both electrode and method claims. |
| [EP3544099A1](https://patents.google.com/patent/EP3544099A1/en) / [US20200411873A1](https://patents.google.com/patent/US20200411873A1/en) (also CN, WO) | Borregaard AS (Norway) | 2018 | EP shown as "ceased"; US shown as pending | Water-soluble (sulfonated, carboxylated or aminated) lignin plus CMC as binder and dispersant. Claims are aimed at the **negative electrode** (Si, Si/C). |
| [CN106025283A](https://patents.google.com/patent/CN106025283A/en) (granted as B) | South China University of Technology | 2016 | Granted, CN only, expires around 2036 | Water-soluble lignin (lignosulfonate, or sulfonated/carboxylated/aminated alkali lignin) plus SBR binder for **anodes**. |
| [CN110752370A](https://patents.google.com/patent/CN110752370A/en) | Guangzhou Great Power Energy & Technology | 2019 | Shown as pending (unusually long; probably abandoned or rejected, needs checking), CN only | **Positive-electrode** water-based binder: modified alkali or enzymatic lignin (sulfonic, carboxyl, ammonium or amine groups) plus polyacrylic acid. **The closest prior art to the concept.** |
| [CN110061239A](https://patents.google.com/patent/CN110061239A/en) (granted as B) | Southern University of Science and Technology | 2018 | Granted, CN, expires around 2038 | Lignin grafted with PAA, PAN or similar prepolymers, or CMC/alginate, giving a water-soluble binder. Mainly for anodes. |
| WO2024189952A1, WO2025047011A1 | Nippon Paper Industries | 2023 | Applications | Lignin-type additives and compositions for **negative** electrodes. Shows a pulp company actively filing in battery uses. |
| US8092557B2 family | (synthetic water-soluble binders) | 2000s | n/a | Water-soluble acrylic binders for cathodes, including Ni-containing oxides. General background on aqueous cathode binders. |

**Main patent holders:**
- **RISE Innventia (SE):** the key cathode-relevant European patent.
- **Borregaard (NO):** lignosulfonate supplier.
- **Chinese universities, mainly SCUT and Guangdong University of Technology** (Qiu Xueqing / Qian Yong group, with many lignin-binder filings, mostly for Si anodes) and SUSTech.
- **Chinese cell makers** such as Great Power.
- **Nippon Paper.**
- Stora Enso is active in lignin for batteries, but as **hard-carbon anode material (Lignode)**, not as a binder. I found no Stora Enso or UPM binder patent in this screening.

---

## 3. Initial novelty check

**Already known (don't expect to claim these broadly):**
- Lignin as a binder in water-processed Li-ion electrodes, **including NMC cathodes**: RISE EP3266057B1 / US10439204B2 (2015); Bryntesen et al., NTNU/UCL, [Mater. Adv. 2022](https://doi.org/10.1039/d2ma00850e) and [J. Mater. Chem. A 2023](https://doi.org/10.1039/d2ta08606a) (kraft lignin, water-processed NMC111, comparable to PVDF).
- Chemically modified, water-soluble lignin (sulfonated, carboxylated, aminated) as a binder: Borregaard, SCUT, and for cathodes specifically CN110752370A.
- Modified kraft lignin (carboxymethylated, sulfomethylated) as a water-based binder: Izaguirre et al., [ACS Appl. Polym. Mater. 2025](https://doi.org/10.1021/acsapm.4c04099) (anodes).
- Hydrothermally modified kraft lignin as a water-based binder: [Electrochim. Acta 2026](https://doi.org/10.1016/j.electacta.2026.149973).
- A lignin-functionalised supramolecular binder for high-voltage, high-capacity ("aggressive") cathodes: SCUT, [JACS 2026](https://doi.org/10.1021/jacs.6c01326). **This needs close reading.** It may be the nearest academic work, although it doesn't appear to be water-processed kraft lignin.
- Benefits of water processing (NMP removed, lower drying energy, lower cost): general knowledge.

**Possibly new (depends on details we don't yet have):**
- **The specific modification chemistry** of the kraft lignin, if it differs from sulfonation, carboxylation, carboxymethylation, amination, simple grafting, or the fractionation used by RISE.
- **Proven compatibility with Ni-rich NMC811 in water**, especially any mechanism that limits lithium leaching, pH rise or aluminium corrosion (for example buffering or pH-control groups on the lignin, or particle-surface interaction). Water-processed lignin/NMC811 with 500-cycle stability wasn't found in the literature checked.
- Process features such as slurry formulation windows, drying conditions and binder content, if they are non-obvious.

**Bottom line:** A broad claim to "a modified lignin water-based binder for Li-ion cathodes" would very likely **not be novel**. A narrower claim to the specific modified lignin, and its use with Ni-rich cathodes, **may be novel and inventive**. Whether it is depends on the chemistry.

---

## 4. Freedom to operate (first indication only)

- **RISE Innventia, EP3266057B1 / US10439204B2: the main FTO risk.**
  - It is active until about 2036 and covers water-based electrode coatings (NMC listed) with "isolated lignin" as binder, *pre-treated to remove electrolyte-soluble fractions below 1000 Da*.
  - If Aalto's process includes any step that removes low-molecular-weight lignin, such as solvent washing, fractionation or ultrafiltration (common when cleaning up kraft lignin), the electrode could fall within these claims.
  - Chemical modification alone may avoid literal infringement, but this needs a claim-construction opinion.
  - Which European countries the patent was validated in, and whether renewal fees are paid, **must be checked in the EPO Register and national registers**. Sweden is certain. Finland and Germany should be checked.
- **CN110752370A (Great Power):** CN only. If it was ever granted, it could matter for production or sales in China (modified lignin plus PAA for cathodes). Check its legal status.
- **Borregaard US20200411873A1 / EP3544099A1:** limited to negative electrodes and lignin+CMC. Low risk for a cathode product unless the formulation uses CMC and claims are broadened. Watch the US status.
- **SCUT and SUSTech patents:** CN only and anode-focused. Low risk outside China.
- **Wider aqueous-binder patents** (Zeon, JSR, Arkema, Solvay, Chinese PAA suppliers) may cover co-binders, dispersants or additives the final formulation might use. **A professional FTO search is needed before any licence or spin-out**, once the final formulation is fixed.

---

## 5. Competing technologies and companies

- **Fluorinated binder improvements:** water-based PVDF latexes and new PVDF grades (Arkema, Solvay/Syensqo, Kureha). Incumbents with strong customer relationships, but under PFAS pressure.
- **Synthetic water-based cathode binders:** polyacrylic acid types (for example the LA133 family from Chinese suppliers, a "drop-in" PVDF replacement), and acrylic/SBR systems from Zeon and JSR. ORNL showed several water-based binder combinations for NMC811 in pouch cells ([Sahore et al. 2022](https://ornl.gov/publication/performance-different-water-based-binder-formulations-ni-rich-cathodes-evaluated-lini)).
- **Bio-based alternatives:** CMC, alginate, carrageenan (for NMC811, [Rolandi et al. 2023](https://doi.org/10.1021/acsaem.3c01662)), chitosan, and poly(ionic liquid)s. Academic groups active here include POLYMAT/UPV-EHU, Deakin, NTNU, RISE and SCUT.
- **Dry electrode processing (no solvent at all):** Tesla (ex-Maxwell), LiCAP, AM Batteries, and Fraunhofer work. This is the strongest alternative route to removing NMP. It typically uses PTFE, which is itself a PFAS concern.
- **Lignin value-chain players** (possible partners or competitors): Stora Enso (Lineo lignin, Lignode anode carbon, working with Northvolt in the past), UPM, Borregaard, Suzano, Nippon Paper, RISE (Sweden). The Finnish pulp company that has shown interest fits naturally into this landscape.
- **Funded research:** OpenAIRE showed no EU or Finnish project on lignin cathode binders specifically, only lignin flow batteries (BALIHT, EU) and flotation (Vinnova). Most activity is in individual academic groups: NTNU/UCL, POLYMAT, SCUT, RISE, Otago.

---

## 6. IP recommendation

**Recommendation: investigate further now (2 to 4 weeks), then most likely file a priority patent application before the spring 2027 manuscript is submitted. Keep the production process know-how as trade secrets.**

Reasons:
1. **Timing.** Europe has no grace period. The manuscript, and any thesis, poster, conference abstract or project report (check the Business Finland and Academy of Finland reporting), would destroy novelty. Any filing must happen before the first public disclosure. Agree an internal deadline with the inventors, ideally Q1 2027.
2. **The broad concept is known.** RISE, Borregaard, Chinese filings and the NTNU papers mean value lies only in a **specific modified lignin and its use with Ni-rich NMC**. Before filing, get from the inventors:
   - the exact modification chemistry and degree of substitution;
   - whether any low-molecular-weight removal or fractionation is used (this matters for the RISE patent);
   - how lithium leaching and aluminium corrosion are handled;
   - data on several NMC grades and on several lignin sources.
3. **Commercial route.** Binder suppliers and pulp companies license composition and process patents. Without a patent, a Finnish pulp partner has little reason to invest, and a spin-out would have nothing to defend. Possible claims:
   - the modified lignin;
   - a cathode slurry or electrode with Ni-rich NMC and that lignin;
   - the manufacturing method.

   Detailed synthesis parameters, purification and batch-to-batch control can stay as know-how.
4. **Strengthen before filing if possible.** One or two extra data sets would make the application much stronger: a second Ni-rich material (NMC622 or NCA), higher loadings, and if feasible a small pouch cell.
5. **Publish only** if the chemistry turns out to be an obvious variant of known modifications (sulfonation or carboxymethylation). In that case, publishing would mainly build academic reputation and block others.

**Other actions for the advisor:**
- Order a **professional novelty search** focused on the actual modification chemistry, covering CN-language filings, which are numerous here.
- Order a **legal status and validation check of EP3266057B1** (RISE).
- Read the [JACS 2026 SCUT paper](https://doi.org/10.1021/jacs.6c01326) and the [Green Chemistry 2026 review](https://pubs.rsc.org/en/content/articlehtml/2026/gc/d5gc05761b) in full.
- Confirm ownership: university inventions under the Finnish University Inventions Act, plus the Business Finland and Academy of Finland terms.
- Put an NDA in place before any technical talks with the pulp company.
- The postdoc wants to continue, so consider a Business Finland Research to Business commercialisation project and adding a business-side team member. Early contact with a cell maker or electrode coater would help validate demand.

---

### Sources
- Patents: [EP3266057B1](https://patents.google.com/patent/EP3266057B1/en), [US10439204B2](https://patents.google.com/patent/US10439204B2/en), [EP3544099A1](https://patents.google.com/patent/EP3544099A1/en), [US20200411873A1](https://patents.google.com/patent/US20200411873A1/en), [CN106025283A](https://patents.google.com/patent/CN106025283A/en), [CN110752370A](https://patents.google.com/patent/CN110752370A/en), [CN110061239A](https://patents.google.com/patent/CN110061239A/en), [CN110518243B](https://patents.google.com/patent/CN110518243B/en), [ES3005100T3](https://patents.google.com/patent/ES3005100T3/en) (Knauf, not battery-related), [US8092557B2](https://patents.google.com/patent/US8092557), [Justia US10439204](https://patents.justia.com/patent/10439204)
- Papers: [Bryntesen 2022](https://doi.org/10.1039/d2ma00850e), [Bryntesen 2023](https://doi.org/10.1039/d2ta08606a), [Izaguirre 2025](https://doi.org/10.1021/acsapm.4c04099), [Gonçalves 2026](https://doi.org/10.1016/j.electacta.2026.149973), [Chen et al. JACS 2026](https://doi.org/10.1021/jacs.6c01326), [Rolandi 2023](https://doi.org/10.1021/acsaem.3c01662), [Sahore 2022 / ORNL](https://ornl.gov/publication/performance-different-water-based-binder-formulations-ni-rich-cathodes-evaluated-lini), [Dobryden 2023 (RISE review)](https://doi.org/10.3390/ma16165553), [Lignin binder for LFP/graphite (PMC5456705)](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5456705/), [Green Chemistry 2026 review](https://pubs.rsc.org/en/content/articlehtml/2026/gc/d5gc05761b)
- Industry: [Stora Enso Lignode (designboom)](https://designboom.com/technology/batteries-made-from-trees-lignode-11-07-2022), [Northvolt–Stora Enso partnership](https://reglobal.org/northvolt-and-stora-enso-partner-to-produce-wood-based-batteries-￼/), [LIGNODE trademark](https://gleanmark.com/trademark/uspto-79323510), [e-Mobility Engineering on aqueous binders](https://www.emobility-engineering.com/content/uploads/magazines/EME035/60), [Sheffield thesis (PFAS/PVDF)](https://etheses.whiterose.ac.uk/id/eprint/37302/), [EU NoVOC project report](https://cordis.europa.eu/project/id/101069612/reporting), [Otago lignin binder project](https://www.otago.ac.nz/profiles/jacob-lamb)