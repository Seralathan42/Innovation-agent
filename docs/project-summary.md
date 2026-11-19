# Aalto Innovation Knowledge Hub: project summary

Course project TU-E700002 (Future Interfaces Project: AI agents and the real world), made with Aalto Innovation.

## The problem

Aalto Innovation advisors receive invention disclosures from researchers and must judge whether each one could become a successful patent, licence or start-up. That means hours of background research per disclosure: who else works on this, which patents already exist, how big the market is, which funding fits. Most of that time goes into finding and reading sources, not into the advice itself.

## Our answer

A local web app, the Knowledge Hub, that does the background research so the advisor can focus on judgement. It combines a live market terminal, a patent database of the advisor's own fields, a look back at past Aalto research, and AI agents that read and summarise public sources.

## What it does

1. **Overview and sectors.** Eight sectors mapped to Aalto's key research areas: AI and software, quantum technology, wireless and electronics, energy and storage, bio-based and advanced materials, health technology, built environment, and design and creative industries. Each sector shows breaking news, market figures from official sources (Eurostat, PRODCOM, trade data), open EU and Finnish funding calls, and the leading companies. An AI analyst updates every sector in the background every few days and keeps a memory of earlier findings.
2. **Patents.** Every European (EP) and international (WO) patent in those fields from the last five years, pulled from the European Patent Office: about 549,000 publications in 416,000 patent families. It refreshes every six hours. The advisor can filter by sector, company, inventor, class and year in a fraction of a second.
3. **Companies.** About 71,000 companies, built from patent applicants and the sector reports, with their patent counts and fields.
4. **Similar.** Paste a description of an invention and get the closest stored patents, ranked by text matching that runs entirely on the computer, so nothing confidential leaves it. A separate Summarise button gives an AI summary for public topics.
5. **Research: did Aalto miss an opportunity?** About 37,000 Aalto papers from 2012 to 2021, pulled from Aalto's research database (ACRIS). Each paper is checked against the patent database. So far 457 papers have close patents, and 286 of those have companies patenting something similar. On request, an AI agent searches the web, patents and papers and gives one of four verdicts: missed opportunity, partly missed, followed up by Aalto or the authors, or no commercial use found.
6. **Assistant and profiles.** A chat on the side answers questions from the stored library. Companies and people it mentions are clickable: one click builds a profile from public sources (what the company builds, key people with photos and past work, a person's current and earlier roles), which is then stored.
7. **Disclosure reports.** Drop a disclosure into the advisory app and agents write market, technology and IP, funding and NABC (Need, Approach, Benefits, Competition) reports, plus an overview.

## How it works

- **AI agents** built on Claude, one agent per task, each with only the tools it needs. Information finding uses Claude Sonnet to keep usage low. It runs on a subscription, not pay-per-use.
- **Free, official data sources:** European Patent Office (OPS), Google Patents, OpenAlex, EU Funding and Tenders portal, PRH (Finnish company register), Eurostat and OpenAIRE.
- **Fast local search:** the patents live in a local database with full-text search, rebuilt every hour, so filtering never waits on the internet.
- **Code first, AI second:** screening and similarity are plain code, which is fast and free. The AI only runs when a person asks for depth (Analyse, Summarise, a profile).

## Confidentiality

Aalto treats patent-sensitive information as secret, so it must not go into common AI tools. The project only uses fictional or public disclosures, the Similar search never leaves the computer, and we built a prototype "keyword firewall": a secure zone turns a disclosure into a public brief plus a list of secret terms, a person reviews the brief, and only then do cloud agents research it. Their findings are matched back to the disclosure inside the secure zone. The goal is a local model for that secure step.

## Results so far

- Background research that took an advisor hours is ready in minutes, with links to every source.
- A searchable patent landscape of Aalto's fields, kept up to date automatically.
- A first systematic look at past Aalto research that others may have turned into patents or products.
- An example: a 2016 Aalto paper on lignin nanoparticles. The agent found that Aalto later patented the method itself, and that an Austrian start-up now sells similar particles.

## Next steps

- A local model for the secure zone, so real disclosures can be handled.
- Merge the keyword firewall into the main app.
- Test with Aalto Innovation advisors on real workflows and measure time saved.
- Wider patent coverage (US and Asian patents) and more paper sources.

## Suggested visuals

- Title slide: a screenshot of the Knowledge Hub overview.
- Problem: an advisor's week, mostly background research.
- Product: one slide per tab with a screenshot (Sector, Patents, Similar, Research, profile popup).
- Architecture: data sources on the left, local databases in the middle, AI agents and the web app on the right.
- Confidentiality: the firewall as a flow from disclosure to secure zone to public brief to cloud agents and back.
- Numbers: 549k patents, 71k companies, 37k papers, 457 papers with close patents.
