# Confidentiality

Research from 24 October 2026 on keeping invention disclosures confidential in this project.

## Aalto's rules

Aalto's guidance on AI in research ([aalto.fi](https://www.aalto.fi/en/services/using-artificial-intelligence-in-research-activities), updated 22 October 2026) treats **patent-sensitive information as Secret**. Secret data must not go into common AI tools; it must stay in the SECDATA environment, which can run local language models. Personal AI accounts may only be used with public data. Aalto's own AI Assistant and AI APIs are approved for data up to Confidential.

What this means:
- **This course project:** use only fictional or already-published disclosures, like `disclosures/example.md`.
- **A real platform:** the full disclosure cannot be sent to Claude or any other cloud AI.

## Where data goes today

| Where | What it receives | How long it's kept |
|---|---|---|
| Anthropic (Claude) | The full disclosure and all reports | 30 days with model training off, 5 years with it on (Pro plan) |
| Search and data services (Brave for web search, OpenAlex, the EU portal, OpenAIRE, PRH, Eurostat, any site an agent opens) | Search words and your IP address. Google Patents only sees patent numbers | Their own policies |
| This Mac, `~/.claude/projects/` | Plain-text transcripts of every agent run and chat | 30 days by default |
| iCloud | This whole folder, because the Desktop syncs to iCloud ("Desktop & Documents Folders" is on) | Until deleted |

One good sign: FileVault disk encryption is on.

## What can be done

**In the code:**
1. **Stop saving transcripts:** set `CLAUDE_CODE_SKIP_PROMPT_HISTORY` for the agents. The chat's memory currently relies on saved transcripts, so it would need another way to keep context. `claude purge` deletes old transcripts.
2. **Turn off non-essential traffic:** `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` stops usage statistics, error reports, surveys and feedback uploads.
3. **Block secret terms:** a short secret-terms list per disclosure, enforced by a hook that blocks any web search, page fetch or data tool call containing one of them. Today this is only an instruction in the prompt.
4. **Log what leaves:** write every outgoing query to the run folder, so advisors can check what was sent.
5. **Limit reading:** allow agents to read only the input files.

**Settings to change by hand:**

6. **Model training off:** claude.ai/settings/data-privacy-controls (30-day retention instead of 5 years).
7. **No transcript sharing:** never answer "Yes" when Claude Code asks to look at your session transcript, and don't send `/feedback` from sessions with disclosures (5-year retention).
8. **Stop the iCloud upload:** turn off Desktop & Documents Folders under System Settings > your name > iCloud > iCloud Drive, or keep this folder outside Desktop and Documents.

**For a real platform:**

9. **Two zones:**
   - A **secret zone** inside SECDATA, running a local model. It reads the full disclosure, writes the NABC summary, and writes a cleaned public brief (field, problem, product type, general search words; no inventive step, names or numbers). A person checks the brief.
   - A **research zone** in the cloud, where the market, IP and funding agents only see the public brief.
10. **Use Aalto's AI services for the research zone.** They are approved up to Confidential.
11. **File before exposing.** The European Patent Office requires absolute novelty and has no general grace period. Law firms say the risk depends on whether the AI input stayed confidential, and no court has ruled on it yet. File a priority patent application before a disclosure is used anywhere outside a confidential setting.

## Sources

- [Claude Code data usage](https://code.claude.com/docs/en/data-usage)
- [Claude Code local data](https://code.claude.com/docs/en/claude-directory)
- [Aalto AI services](https://www.aalto.fi/en/services/ai-services)
- [Brave as Claude's search provider](https://simonwillison.net/2025/Mar/21/anthropic-use-brave/)
- [Polsinelli on generative AI and patents](https://www.polsinelli.com/publications/disclosure-generative-ai-tools-patent-prosecution-risk)
- [Womble Bond Dickinson on accidental disclosure](https://www.womblebonddickinson.com/us/insights/digital-solutions/102mvof/the-accidental-disclosure-trap-how-generative-ai-can-void-your-patent-rights)
- [UC Berkeley AI confidentiality notice](https://ipira.berkeley.edu/researchers/intellectual-property-protection/disclose-invention)
- [Notre Dame 2026 guidance](https://ideacenter.nd.edu/assets/672301/ideacenter_useofai_patentaabilityimpact_2026_01.pdf)
