# EPO Open Patent Services (OPS): how it works

Checked on 9 November 2026 against the official [OPS 3.2 reference guide, v1.3.20 (June 2024)](https://link.epo.org/web/ops_v3.2_documentation_-_version_1.3.20_en.pdf), the [OPS OpenAPI file](http://ops.epo.org/wsdl/ops.yaml), the [fair use charter](https://www.epo.org/en/service-support/ordering/fair-use) and the [OPS terms and conditions](https://www.epo.org/en/service-support/ordering/terms-and-conditions/ops-terms-and-conditions). Page numbers refer to the reference guide.

## What we need

1. **An app on the EPO developer portal.** Register at [developers.epo.org](https://developers.epo.org/), then open My Apps and Add a new App. The app gives you a **consumer key** and a **consumer secret**. These are the "API keys".
2. **Put both in a `.env` file** in the project folder. It is excluded from git by `.gitignore`.
   ```
   EPO_KEY=your consumer key
   EPO_SECRET=your consumer secret
   ```
3. Nothing else: no payment, as long as we stay under the free weekly volume (see Limits).

## Logging in (OAuth 2.0, pages 36 to 37)

- Send `POST https://ops.epo.org/3.2/auth/accesstoken` with:
  - the header `Authorization: Basic <base64 of key:secret>`;
  - the header `Content-Type: application/x-www-form-urlencoded`;
  - the body `grant_type=client_credentials`.
- The JSON reply holds `access_token` and `expires_in` (1199 seconds). **A token lasts about 20 minutes.** Ask for a new one when OPS says the token is invalid.
- Every other request sends `Authorization: Bearer <access_token>`.

`epo.py` does all of this. It keeps the token for 19 minutes and logs in again when needed.

## Searching (pages 58 to 59 and 142 to 147)

```
GET https://ops.epo.org/3.2/rest-services/published-data/search/biblio?q=<CQL query>&Range=1-25
Accept: application/json
```

- Leave out `/biblio` to get only publication numbers. Use `/abstract`, `/biblio` or `/full-cycle` to get the data in the same call.
- **At most 100 results per request and 2,000 per query.** For more, narrow the query. The total hit count is capped at 10,000.
- Replies are XML unless you ask for `Accept: application/json`. Errors are always XML.
- "No results" comes back as HTTP 404.

**Query language (CQL).** Main fields:

| Field | Searches |
|---|---|
| `ti` | Title |
| `ab` | Abstract |
| `ta` | Title or abstract |
| `txt` | Title, abstract, inventor or applicant |
| `pa` | Applicant (for example `pa=aalto`; this also finds people and firms named Aalto, so `patents.py` keeps only applicants with AALTO plus UNIV or KORKEAKOULU) |
| `in` | Inventor |
| `ia` | Inventor or applicant |
| `cpc`, `ipc` | Classification (for example `cpc=H01M10`) |
| `pd` | Publication date (yyyy, yyyyMM, yyyyMMdd and others) |
| `pn` | Publication number or country (for example `pn=EP`) |
| `pr` | Priority number |
| `ct` | Cited document |
| `famn` | Family ID |

**Operators:**
- `and`, `or`, `not` (where `not` means "and not" and cannot start a query);
- `any` and `all` for word lists, for example `ti all "green energy"`;
- exact phrases in quotes, for example `ti="green energy technology"`;
- date ranges, for example `pd within "20250101 20251231"`;
- comparisons `<`, `>`, `<=`, `>=`;
- proximity, for example `ta=green prox/distance<=3 ta=energy`;
- truncation `*` (any characters), `?` (one or no character) and `#` (exactly one character).

Example used by the terminal: `cpc=H01M and (pn=EP or pn=WO) and pd within "20251109 20261109"`, meaning battery patents published by the EPO or under the PCT in the last 12 months.

## Getting more about one patent (pages 60 to 120)

| What | Path under `https://ops.epo.org/3.2/rest-services/` |
|---|---|
| Bibliographic data | `published-data/publication/epodoc/EP1000000/biblio` |
| Abstract, claims, description | `.../abstract`, `.../claims`, `.../description` |
| What full text exists | `.../fulltext` |
| Drawings (PDF/PNG/TIFF pages) | `.../images`, then `published-data/images/...` |
| Patent family (INPADOC) | `family/publication/docdb/EP.1000000.A1/biblio` (the family service needs docdb format) |
| Legal status | `legal/publication/docdb/EP.1000000.A1` |
| European Patent Register | `register/publication/epodoc/EP1000000/biblio`, `/events` and `/procedural-steps` |
| CPC classes | `classification/cpc/search?q=...` |

Full text (claims and description) is available only for EP, WO and some European countries (AT, BE, BG, CA, CH, CY, CZ, DK, EE, ES, FR, GB, GR, HR, IE, IT, LT, LU, MC, MD, ME, NO, PL, PT, RO, RS, SE, SK). There is no full text for US or CN documents (page 61).

## Limits (pages 40 to 43, fair use charter)

- **Free up to 4 GB a week**, counted Monday to Sunday (UTC). Above that, a paid yearly subscription is needed.
- **A 1 Mbit/s rule, enforced as about 450 MB an hour** on a rolling window.
- **Every reply carries usage headers:**
  - `X-IndividualQuotaPerHour-Used` and `X-RegisteredQuotaPerWeek-Used`;
  - `X-Throttling-Control`, for example `idle (retrieval=green:200, search=yellow:20, ...)`. It gives the system state (idle, busy or overloaded) and a traffic light with the number of requests allowed per minute for each service.
- **When a limit is reached, OPS answers 403** with an `X-Rejection-Reason` header. Very heavy users can be blocked.
- The EPO asks for bulk robot downloads between 19:00 and 07:00 GMT or at weekends.

**What we saw in practice (10 November 2026).** OPS was "overloaded" and allowed only 5 searches a minute. Sending about 12 in a minute got the reply 403 `CLIENT.RobotDetected`, and for a while searches were switched off completely (`search=black:0`), even though our weekly use was only about 2.5 MB. So `epo.py` now keeps searches at least 12 seconds apart and retries a throttled request up to 3 times with growing pauses. If a sector still fails, it simply gets its patents at its next refresh.

Our use is far below these limits. The terminal makes one search per sector every three days, plus searches you start yourself in the chat.

## Terms that matter for us

- We may use OPS data inside our own tools and products.
- We may **not** make the raw data available to the public, or copy and redistribute it as such.
- The key and secret must be kept private, which is why they live in `.env`.
- The EPO may monitor usage and block misuse.
