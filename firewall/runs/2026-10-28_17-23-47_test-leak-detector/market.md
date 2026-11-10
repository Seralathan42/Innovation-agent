# Market map: leak detection and condition monitoring for buried district heating pipes

Most market-size figures below are weak. Official statistics are solid but cover the whole district heating industry, not leak detection. I found no price data. Check prices with vendors directly.

## 1. Customers

**Who has the problem**
- **District heating operators and energy utilities.** Examples are Fortum, Helen and the many small municipal firms. They own the buried pipes and pay for the heat and water lost.
- **Municipal infrastructure owners.**
- **Maintenance and excavation contractors.** They are partners or channel buyers more than end customers.

**How many (Finland)**
- The Finnish network was 16,690 km at the end of 2024, up from 16,465 km in 2023 and 16,240 km in 2022. This is solid: [Energiateollisuus, District heating in Finland 2024](https://energia.fi/wp-content/uploads/2026/01/District_heating_in_Finland_2024.pdf).
- Eurostat counts 440 enterprises in "steam and air conditioning supply" (NACE D35.3) in Finland in 2024, with 2,149 people employed. This is solid: [Eurostat sbs_ovw_act](https://ec.europa.eu/eurostat/databrowser/view/sbs_ovw_act/default/table). Many of the 440 are probably very small, so the real buyer group is smaller.
- Finnish heat losses in the distribution network are 8–9% of the heat sent through the pipes. The page is undated and cites 2021 network data, so it is moderately reliable: [Energiateollisuus, District heating networks](https://energia.fi/?p=53217).

**How they buy**
- Sensors are usually specified when the pipe network is built, as alarm wires inside the pipe insulation, and bought together with the pre-insulated pipes. Brandes claimed more than 80% of networks use in-insulation monitoring, in a 2014 vendor presentation: [Brandes via SOGDE](https://sogde.org/site/assets/files/12099/franz_20_02_14.pdf).
- Operators later add monitoring cabinets, software and survey services.
- Pipe makers and valve makers sell monitoring as part of a system. Utilities pilot new technology first, as Fortum did in 2020 (see section 3).
- This is an inference from the sources, not something they state.

## 2. Market size

| Figure | Source | Reliability |
|---|---|---|
| District heating leak detection market: $0.8 bn in 2025, $1.5 bn by 2034 (about 7.2% a year) | [Market Intelo](https://marketintelo.com/report/district-heating-leak-detection-market/amp) | Low. One vendor-style publisher, and the method is not transparent. |
| District energy pipe leak monitoring (broader scope): $1.2 bn in 2025, $2.3 bn by 2034 | [Market Intelo](https://marketintelo.com/report/district-energy-pipe-leak-monitoring-market) | Low. The regional shares conflict with the other Market Intelo report (Europe 38.2% in one, Asia Pacific 38.2% and Europe 31.6% in the other). |
| Whole district heating and steam supply industry (D35.3), 2024: EU27 net turnover €56.8 bn and output value €51.8 bn; Finland net turnover €1.87 bn and output value €1.06 bn | [Eurostat sbs_ovw_act](https://ec.europa.eu/eurostat/databrowser/view/sbs_ovw_act/default/table) | High, but this is the customer industry, not the leak detection market. |
| Finnish gross investment in tangible assets by the industry, 2024: €229 m | [Eurostat sbs_ovw_act](https://ec.europa.eu/eurostat/databrowser/view/sbs_ovw_act/default/table) | High. It shows the size of the capital budget that monitoring would draw on. |

A rough check of my own: at about 8–9% heat loss and Finnish turnover of €1.9 bn, losses are worth tens of millions of euros a year. This is only an order-of-magnitude estimate, because the turnover figure includes more than heat sales.

## 3. Existing solutions and competitors

**Alarm wire systems (the incumbent standard)**
- **Kingspan LOGSTOR (Denmark).** Its Detector X6 cabinet takes up to four modules and supports Nordic and NiCr wire. It reads temperature and pressure through optional modules and connects to SCADA. Its Detect line sends GPRS alarms, and it has a hosted surveillance service. Sources: [Detect X6 brochure](https://www.logstor.com/media/8158/kingspan-logstor-detect-x6-en-012025.pdf), [surveillance handbook](https://www.logstor.com/media/7220/kingspan-logstor-surveillance-handbook-specifications-en-eur.pdf), [Detect news](https://www.logstor.com/it/chi-siamo/news/all-news/logstor-detect-takes-surveillance-to-the-next-level).
- **BRUGG Pipes LEAKGUARD (Switzerland).** The Basic model is mains-powered with two channels, to EN 14419. The Cloud model is battery-powered with LTE/GSM alarms: [Basic](https://bruggpipes.com/en/leakguard-basic), [Cloud](https://www.bruggpipes.com/en/leakguard-cloud/).
- **Brandes (Germany).** NiCr system. It claimed over 47,000 km of sensor cable delivered, as of 2014: [Brandes via SOGDE](https://sogde.org/site/assets/files/12099/franz_20_02_14.pdf).
- **Mittel (Pipeguard, Stateview).** Continuous monitoring and a portable locating tool: [vendor results via search](https://www.logstor.com/media/7220/kingspan-logstor-surveillance-handbook-specifications-en-eur.pdf). I could not confirm Mittel's own source page or base.
- **Vexve iSENSE Pulse (Finland).** Pulse measurement on alarm wires for real-time detection and location. The Kotkan Energia reference exists: [Vexve, Big savings with network monitoring](https://vexve.com/en/articles/big-savings-with-network-monitoring), [Kotkan Energia reference](https://vexve.com/de/referenzen/reference-kotkan-energia).

**Other methods**
- **Satellite and thermal imaging.** Fortum and Advian piloted satellite leak detection in the Espoo area in 2020 to replace helicopter thermal surveys: [Maintworld](https://maintworld.com/Asset-Management/Energy-Group-Fortum-to-pilot-district-heating-network-leak-detection-using-satellite-imagery). I found no result on whether it was adopted.
- **Remote monitoring devices.** [With the Grid](https://withthegrid.com/remote-monitoring-device-for-leak-detection-for-district-heating/) sells a remote device for district heating leak detection.
- **Acoustic correlators and ground microphones.** These are field tools used by contractors. I did not research specific products, so I name none.
- **Consulting and survey services.** An example is [Rossma's case study](https://pipeline.rossma.ru/en/blog/case-study-district-heating), which reports a 45% leak loss reduction. This is a vendor claim.

**Where the gaps are**
- Alarm wires degrade with age and give no data on old, bare or non-wired pipes.
- Wire systems detect moisture but are weaker at early warning.
- Imaging surveys are periodic and weather-dependent.
- An acoustic or sensor-plus-software approach for older networks is the likely opening. This is my inference, not something the sources state.

The 2024 thesis [Leak detection systems in Finnish district heating network](https://www.theseus.fi/handle/10024/872261) is a useful overview of Finnish practice.

## 4. Finnish companies in the field

**Possible competitors**
- **Vexve** is a valve and monitoring maker (iSENSE). Sources are in section 3.
- **Advian** worked with Fortum on the satellite pilot: [Maintworld](https://maintworld.com/Asset-Management/Energy-Group-Fortum-to-pilot-district-heating-network-leak-detection-using-satellite-imagery).

**Possible customers.** The Finnish Trade Register ([finnish_companies search, "kaukolämpö"](https://www.prh.fi/en/index.html)) shows 55 matches. Active district heating firms in the results:

| Company | Business ID | Location |
|---|---|---|
| Riihimäen Kaukolämpö Oy | 0276726-4 | Riihimäki |
| Turun Seudun Kaukolämpö Oy | 0300342-6 | Turku |
| Loimaan Kaukolämpö Oy | 0313531-4 | Loimaa |
| Kannuksen Kaukolämpö Oy | 0346378-0 | Kannus |
| Kauhavan Kaukolämpö Oy | 0355682-1 | Kauhava |
| Pargas Fjärrvärme Ab | 0508383-7 | Parainen |
| Mäntän Kaukolämpö ja Vesihuolto Oy | 0713539-7 | Mänttä |
| Kurikan Energia Oy | 0370685-0 | Kurikka |
| Nivalan Kaukolämpö Oy | 0291676-8 | Nivala |

Fortum is a larger customer, shown by its pilot (see section 3).

**Possible partners.** TLT-Energy Oy (0700928-6, Turku, specialised construction) came up in the register search. I did not check what it does.

I did not search for Helen, Oulun Energia or Tampereen Sähkölaitos, so they are not covered here.

## 5. Trends and regulation

**Growth drivers**
- **Network growth.** Finland added about 225 km in 2024 and 225 km in 2023 (see section 1).
- **EU rules.** The Energy Efficiency Directive (EU) 2023/1791 sets an "efficient district heating" definition in two phases. Systems above 5 MW fall under the criteria. Both points come from the trade and academic sources, not from the Directive text: [Solarthermalworld](https://solarthermalworld.org/news/what-is-in-the-fit-for-55-package-for-district-heating/), [eceee 2021](https://www.eceee.org/library/conference_proceedings/eceee_Summer_Studies/2021/3-policy-finance-and-governance/efficient-district-heating-and-cooling-does-it-promote-the-2050-decarbonisation-goals/). I could not confirm whether the final Directive sets explicit heat-loss rules, so check EUR-Lex (Article 26).
- **Lower-temperature, renewable networks.** Heat is getting more expensive to produce. Heat pumps and waste heat are costlier per unit, which raises the value of each lost unit. This is my reasoning, not sourced.
- **Digital tools.** Cloud alarms and hosted surveillance are already offered by vendors (see section 3). Operators are also piloting remote sensing, such as Fortum's satellite trial.

**Brakes**
- Sensors are tied to pipe suppliers' ecosystems, so a new entrant has to work with Nordic and NiCr wire standards, or replace them. The relevant standard is EN 14419.
- Many small municipal operators have little investment budget.
- The market-size forecasts above are not independently verified.

**Suggested next steps**
1. Check the Directive text on EUR-Lex.
2. Ask two or three Finnish operators what they spend on leak finding and repair.
3. Get prices for LOGSTOR, Vexve and BRUGG systems.

Sources: all links are inline above.