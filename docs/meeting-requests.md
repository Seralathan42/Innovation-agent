# Requests for the meeting with the Head of Innovation Services

Bottlenecks found while building the prototype (agents, web app, keyword firewall), in order of importance.

## Must have

**1. Real test material that is safe to use**
- 5 to 10 past invention disclosures whose patents or papers are already **public**, on Aalto's **real disclosure form**.
- For each one, what the advisors actually concluded (evaluation, NABC, decision, what happened next).
- Why: today we test on made-up disclosures. Without real cases and the advisors' verdicts we cannot measure whether the agents are right, which is the main question of the project.

**2. A secure place to run a model on the confidential part**
- Access to **SECDATA** for the project, and a local language model running there. Ask who in Aalto IT or Research Software Engineering sets this up.
- A written decision on **data classification**: is the cleaned "public brief" (field, problem, keywords, no inventive step) Public or Confidential? Then we know whether the research part can use Aalto's AI APIs or outside providers.
- Why: Aalto's AI rules class patent-sensitive information as Secret, so real disclosures cannot go into Claude or any common AI tool. The keyword firewall only works with a secure zone.

**3. Patent search access: Patsnap**
- A trial **Patsnap API or MCP key** (Discovery / Eureka) for the project, and confirmation that its terms allow automated use by AI agents.
- Why: Google Patents has no search API and forbids automated searching, and we were asked not to use EPO OPS. Today agents find patents through general web search, which is the weakest part of the IP analysis.

**4. How the process works today**
- A 1-hour interview with an advisor (Juha Siivola or Janne Raula), or sitting in on one case review.
- Copies of the **standard evaluation templates** and the NABC template the advisors use.
- Answers to:
  - Who receives a disclosure and what happens in the first week?
  - Which steps take the most advisor time?
  - What makes a case "promising", and how are team, technology, business model, customer need and funding weighed?
  - What exactly should the 1 to 2 page case summary contain?
- Why: the agents' reports are guesses at what advisors need. Matching their templates and criteria makes the output usable straight away.

## Should have

**5. An approved AI account for the project**
- Access to **Aalto's AI APIs** or an Aalto-provided Claude (Education or Enterprise) account for the research part.
- Why: the prototype runs on a personal Claude Pro subscription. It has usage limits (a full run uses a noticeable share), and personal accounts may only be used with public data.

**6. Market and company data**
- Which paid databases Aalto Innovation already uses (for example PitchBook, CB Insights, Dealroom, Statista), and whether any have API access we could use.
- Whether we may use **Orbis**, **Zephyr** and **Statista** exports (Aalto library licences) in the project.
- Why: free sources cover statistics and Finnish companies, but not startup deals, funding rounds or market reports.

**7. Funding data**
- Whether Aalto Innovation has structured data on Business Finland and other funding decisions, or a list of the funding instruments it normally recommends.
- Why: Business Finland only publishes Excel exports, so the funding agent relies on web search for Finnish funding.

## Good to know

**8. Internal systems, for later integration**
- Which systems hold disclosures, cases and past projects (CRM, document management, the historical projects database), and whether an export or test copy could ever be made available.

**9. Sign-off and success criteria**
- Who should approve the public brief before research starts (the advisor? the IP manager?).
- What a successful outcome looks like at the end of the course, and which one or two advisors could test the tool and give feedback.
