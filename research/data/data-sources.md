# Data Sources — Web Intelligence, Scraping & Public APIs

The Office is only as good as the data it can reach. The [Signal Scout](../../agents/workers/signal-scout/signal-scout.md) monitors feeds. The [CAO](../../agents/management/cao/cao.md) conducts research and maintains the knowledge base. Neither can do their job without knowing where to look and how to get there.

This file covers the full data collection stack: AI-powered scrapers, browser automation, self-hosted search, feed aggregation, and public APIs organized by domain. Everything here runs locally or calls free/open public endpoints — no proprietary data pipeline required.

---

## Web Scraping — AI-Powered

Modern scraping is not about parsing HTML. It is about extracting structured, meaningful data from pages that were designed for humans, using models that understand what they are looking at.

---

### Crawl4AI
**Role in Office:** Primary web crawler — feeds the CAO's research pipeline
**Runner:** Python library / Docker · **Cost:** Free, open source

Built specifically for LLM data collection. Takes a URL, renders the page (including JavaScript), and returns clean markdown — not raw HTML. Supports batch crawling, deep crawling (follow links N levels deep), and extraction schemas (define the fields you want, get back structured JSON). Handles authentication, cookies, and dynamic content.

The CAO uses Crawl4AI as its default web fetching layer. When a Signal Scout event escalates a URL worth investigating, the CAO uses Crawl4AI to fetch the full page content in a format ready for the model to reason over — no HTML stripping, no boilerplate noise.

---

### ScrapeGraphAI
**Role in Office:** Intelligent structured extraction — describe what you want, get it back
**Runner:** Python library · **Cost:** Free, open source

Rather than writing XPath or CSS selectors, you describe the data you want in natural language: "extract the product name, price, and availability from this page." ScrapeGraphAI uses a local LLM to interpret the page and extract the defined schema. Works on pages whose structure changes frequently — because the extraction logic is semantic, not structural.

For the CAO: give it a list of competitor pricing pages and a target schema, and it returns structured data regardless of how each site organises its content.

---

### Firecrawl (open source)
**Role in Office:** Full-site crawling, sitemap traversal, bulk content ingestion
**Runner:** Self-hosted Docker · **Cost:** Free (self-hosted)

Crawls entire websites, converts every page to clean markdown, and returns a structured dataset of the site's content. Supports sitemap-guided crawling, so it can systematically cover a site's full knowledge base. The CAO uses this for deep research tasks: ingest all published content from a competitor, a regulatory body, or an industry publication into ChromaDB in one operation.

---

### Jina Reader (r.jina.ai)
**Role in Office:** Single-page fetch — clean markdown from any URL in one call
**Runner:** API (free tier generous) · **Cost:** Free up to rate limit

Prefix any URL with `https://r.jina.ai/` and get back clean, LLM-ready markdown of that page's content. No scraping setup, no JavaScript rendering infrastructure. The fastest way to fetch a single page's content in a model-consumable format. Rate-limited on the free tier but sufficient for targeted research tasks.

Signal Scout uses this when following a flagged URL to retrieve article content before passing it to the CAO for analysis.

---

### Browser-Use
**Role in Office:** Autonomous browser control — LLM-directed web navigation
**Runner:** Python library · **Cost:** Free, open source

Gives a language model direct control of a browser: click, type, scroll, navigate, fill forms. Useful for sites that require interaction to access data — search results that need a query submitted, paginated tables, login-gated content. The CAO can direct Browser-Use to navigate multi-step research paths that static scrapers cannot handle.

---

### Playwright
**Role in Office:** Programmatic browser automation for JavaScript-heavy sites
**Runner:** Python library · **Cost:** Free, open source

Microsoft's browser automation library. Handles sites that render entirely in JavaScript — single-page applications, infinite scroll feeds, dynamically loaded content. Used directly when the scraping target is known and structured (the same site, the same interaction, repeated). Browser-Use wraps Playwright; use Playwright directly when the automation logic is deterministic and does not need LLM reasoning.

---

## Self-Hosted Search

Rather than calling Google or Bing, the Office can run its own search infrastructure — returning results without rate limits, without tracking, and without commercial API costs.

---

### SearXNG
**Role in Office:** Primary search engine — aggregates results from 70+ sources
**Runner:** Docker (self-hosted) · **Cost:** Free

A self-hosted meta-search engine that queries Google, Bing, DuckDuckGo, Brave, Wikipedia, arXiv, GitHub, and 70+ other engines simultaneously, deduplicates and ranks the results, and returns a clean JSON response. No API key. No rate limit on your own instance. No data sent to any third party.

The Signal Scout uses SearXNG as its search backend when monitoring topics requires fresh web results rather than feed subscriptions. The CAO uses it for open research queries.

---

### Perplexica
**Role in Office:** AI research assistant — search + synthesis, fully local
**Runner:** Docker (self-hosted) · **Cost:** Free

An open-source Perplexity alternative. Takes a natural language research question, searches the web via SearXNG, retrieves the top results, and synthesises a sourced answer using a local LLM. Outputs both the synthesised answer and the sources it drew from.

The CAO uses Perplexica for research tasks that need a first-pass synthesised overview before deeper investigation — "what is Scan Food Group's current supplier partnership strategy?" returns a grounded summary with sources in one step.

---

## Feed Aggregation

RSS and Atom feeds are the most reliable, lowest-friction, highest-signal data streams available. Most publishers maintain them; most competitors do not monitor them at volume.

---

### Feed Sources for the Signal Scout

The Signal Scout is built to scan 1,000+ feeds per hour. The feeds below are organised by domain and represent the core subscription list for an Office doing business intelligence.

**News & Media**
- Reuters (`feeds.reuters.com`) — international wire
- Associated Press (`apnews.com/rss`) — US and international
- The Guardian (`theguardian.com/rss`) — international, strong on tech and business
- Financial Times (`ft.com/rss`) — financial and business (limited free)
- Hacker News (`news.ycombinator.com/rss`) — tech community signal
- TechCrunch, Wired, The Verge, MIT Technology Review — tech industry

**Swedish / Nordic**
- Breakit (`breakit.se/feed`) — Swedish tech and startup
- Di Digital (`di.se/rss`) — Swedish business
- SvD Näringsliv — Swedish business
- NyTeknik — Swedish technology and engineering

**Industry-Specific** (configure per client / sector)
- Any industry publication with an RSS feed — nearly all have one

**Academic / Research**
- arXiv (`arxiv.org/rss/`) — per-category feeds for new preprints
- PubMed (`ncbi.nlm.nih.gov/rss/`) — biomedical literature
- SSRN — economics and social science preprints

**Company Monitoring**
- Company press release feeds (usually `company.com/newsroom/rss`)
- Google Alerts RSS output — set up alerts for competitor names, product launches, key personnel
- SEC EDGAR (`sec.gov/cgi-bin/browse-edgar`) — US company filings feed

---

## Public Data APIs

Structured, authoritative data available via open or low-cost APIs. Organized by domain.

---

### News & Media

**NewsAPI** (`newsapi.org`)
Free tier: 100 requests/day. Searches 150,000+ news sources and blogs. Returns headlines, full article URLs, and metadata. Good for Signal Scout's headline monitoring when RSS coverage is insufficient.

**GDELT Project** (`gdeltproject.org`)
Free, no auth. The Global Database of Events, Language, and Tone — monitors print, broadcast, and web news in 100+ languages in near-realtime. Enormous scale. Useful for macro trend detection across global news rather than individual publication monitoring.

**The Guardian API** (`open-platform.theguardian.com`)
Free developer tier. Full article content access across The Guardian's archive. One of the few news APIs that returns complete article text rather than just headlines.

---

### Financial & Economic

**Alpha Vantage** (`alphavantage.co`)
Free tier: 25 requests/day. Stock prices (real-time and historical), forex, crypto, economic indicators, earnings data. The CFO uses this for market data and the CAO for macroeconomic context.

**Yahoo Finance** (unofficial API via `yfinance` Python library)
Free, no key required. Historical price data, financials, earnings calendars, analyst estimates. The most practical free source for equity data in Python.

**EDGAR (SEC)** (`data.sec.gov`)
Free, no auth required. All US public company filings: 10-K, 10-Q, 8-K, proxy statements, insider trading reports. Machine-readable JSON API. For the CAO researching US-listed companies or the CFO monitoring publicly disclosed financial data.

**Eurostat** (`ec.europa.eu/eurostat/api`)
Free, no auth. EU statistical data: GDP, inflation, trade, employment, industry output across all EU member states. The definitive source for European macroeconomic data.

**SCB (Statistics Sweden)** (`api.scb.se`)
Free, no auth. Swedish national statistics: population, economy, labour market, housing, prices. Essential for Sweden-focused Office deployments.

**World Bank Open Data** (`data.worldbank.org/api`)
Free, no auth. Global development indicators across 200+ economies. Long historical series. Good for the CAO building macroeconomic context for international market research.

**OECD Data** (`data.oecd.org/api`)
Free, no auth. Economic and social data across OECD member countries. Comparable cross-country statistics on trade, productivity, education, health.

---

### Company & Business Intelligence

**OpenCorporates** (`opencorporates.com/api`)
Free tier available. The largest open database of company information — 200+ million companies globally. Registered names, addresses, officers, incorporation dates, filing history. The CAO uses this for company research and verification.

**Bolagsverket** (Swedish Companies Registration Office)
Free access via `bolagsverket.se`. Swedish company registration, ownership, board members, annual reports. Authoritative source for Swedish corporate data.

**Companies House (UK)** (`developer.company-information.service.gov.uk`)
Free, requires registration. UK company data: officers, filings, accounts, persons with significant control. Same scope as Bolagsverket for UK entities.

**Wikidata** (`query.wikidata.org/sparql`)
Free, no auth. Structured knowledge base — companies, people, places, products, with cross-references to Wikipedia and other sources. SPARQL query interface. Excellent for entity resolution: "who are the board members of this company?" with links to their professional histories.

**Morten Lund** (Serial Entrepreneur)
Danish serial entrepreneur, investor, and startup founder. Key companies: BullGuard (sold), ZYB (sold to Vodafone), Podio (sold to Citrix), Vivino, Too Good To Go, Lunar, Pleo. Known for early-stage tech investments across Europe. Active in Nordic startup ecosystem.

---

### Academic & Scientific

**arXiv API** (`export.arxiv.org/api`)
Free, no auth. Query all arXiv preprints by topic, author, date. Returns full metadata and abstract. The CAO uses this to monitor new research in any scientific domain — results feed through Nougat for full paper ingestion.

**PubMed / NCBI E-utilities** (`eutils.ncbi.nlm.nih.gov`)
Free, API key optional. Biomedical literature search across 35+ million citations. Returns abstracts and, where available, full-text links. The primary data source for any Office doing healthcare or life sciences research.

**Semantic Scholar** (`api.semanticscholar.org`)
Free, no auth. Academic paper search with citation graphs, author profiles, and semantic similarity search. Unique feature: finds papers that cite a given paper (forward citation tracking), useful for following how a body of research has developed.

**CrossRef** (`api.crossref.org`)
Free, no auth. DOI metadata, citation counts, publisher information for 140+ million scholarly works. Used for resolving citations and verifying publication metadata.

**OpenAlex** (`api.openalex.org`)
Free, no auth. Open bibliographic database of research publications, authors, institutions, and research topics. More comprehensive than Semantic Scholar, structured for programmatic access.

---

### Government & Regulatory

**EUR-Lex** (`eur-lex.europa.eu/api`)
Free. Full text of all EU legislation, case law, and official publications. The Compliance Watchdog uses this to retrieve the current text of regulations relevant to a client's domain.

**Riksdagen Open Data** (`riksdagen.se/sv/dokument-lagar/oppna-data`)
Free. Swedish parliamentary documents, committee reports, motions, legislation. Useful for tracking regulatory developments in Sweden.

**SMHI** (`opendata.smhi.se/api`)
Free. Swedish Meteorological and Hydrological Institute. Weather data, climate statistics, forecasts. Useful for any Office doing logistics, agriculture, energy, or events.

**OpenStreetMap / Overpass API** (`overpass-api.de`)
Free. Query any geographic feature from the OSM database: business locations, road networks, POIs, administrative boundaries. The CAO uses this for location-based research tasks — finding all businesses of a given type in a given area, mapping competitor locations, etc.

---

### Social & Community

**Reddit (PRAW)** (`reddit.com/api`)
Free developer tier. Subreddit monitoring, post and comment retrieval, search. The Signal Scout uses PRAW to monitor industry-relevant subreddits for emerging topics, product feedback, and community sentiment before it surfaces in mainstream media.

**Hacker News (Algolia API)** (`hn.algolia.com/api`)
Free, no auth. Full HN search and story/comment retrieval. Strong early-signal for technology trends — topics appear on HN before they reach tech press.

**GitHub API** (`api.github.com`)
Free tier: 60 requests/hour unauthenticated, 5,000 authenticated. Repository metadata, stars, commits, issues, releases, trending. The Signal Scout uses this for the [repo-radar](repo-radar.md) workflow — monitoring what developers are building before products are announced.

---

### Search APIs

**Brave Search API** (`api.search.brave.com`)
Free tier: 2,000 queries/month. Web search results in JSON, with no Google dependency. The CAO's preferred search API when direct web search is needed and SearXNG is not appropriate.

**SerpAPI** (`serpapi.com`)
Paid (free trial). Returns Google, Bing, DuckDuckGo results in structured JSON. More comprehensive than Brave for SEO-related research tasks (SERP analysis, competitor ranking monitoring).

**DuckDuckGo Instant Answer API** (`api.duckduckgo.com`)
Free, no auth. Returns DuckDuckGo's instant answers — quick factual lookups, definitions, entity summaries. Not a full search API, but useful for rapid entity resolution without a paid subscription.

---

## The Collection Stack

How these tools and sources connect to the Office agents:

```
Signal Scout
    ← RSS/Atom feeds (1,000+ sources, hourly)
    ← SearXNG (real-time web search on monitored topics)
    ← Jina Reader (full article content on flagged URLs)
    → escalates high-signal events → CAO

CAO
    ← Signal Scout escalations
    ← Crawl4AI (deep-crawl research targets)
    ← ScrapeGraphAI (structured extraction from target sites)
    ← Perplexica (synthesised research on specific questions)
    ← Public data APIs (financial, academic, government, business)
    ← Browser-Use (interactive sites, paginated data, login-gated content)
    → embeds all findings → Digital Archivist → ChromaDB
```

The Signal Scout is the radar — continuous, broad, shallow. The CAO is the investigator — targeted, deep, structured. The data sources and tools above serve both roles, at different depths.

---

## Cloud Services — Output-Heavy, Input-Light

A local-first architecture does not mean refusing all external services. The distinction is what leaves the building. Sending a URL and receiving a full structured article back is categorically different from sending a confidential prompt to a cloud inference engine. The services below share a common property: **what goes out is minimal and non-sensitive — a URL, a domain, a search query — and what comes back is substantially more than what was sent**.

These are appropriate for the Office under the local-first principle. Private business data — client information, internal documents, agent reasoning — stays on-premises. Public information retrieval does not.

---

### Firecrawl (cloud)
**Cost:** Free tier (500 pages/month), paid tiers above that

The cloud version of the open-source Firecrawl. Sends a URL, gets back clean LLM-ready markdown — JavaScript rendered, boilerplate stripped, structured. Faster and more reliable than self-hosted for burst workloads. Use the cloud version for external research where speed matters; use the self-hosted version for high-volume internal pipelines. Input: a URL. Output: full page content.

---

### Tavily
**Cost:** Free tier (1,000 searches/month)

A search API built specifically for AI agents. Unlike general search APIs that return a list of links, Tavily fetches and processes the top results and returns their actual content — pre-cleaned, pre-ranked, ready for a model to reason over without additional fetching. One API call replaces: search → pick results → fetch each page → clean each page. Designed for agentic research loops. Input: a search query. Output: structured content from the top results.

---

### Exa
**Cost:** Free tier (1,000 searches/month)

Neural search — finds content by semantic similarity rather than keyword matching. Give it a URL or a piece of text and it returns the most semantically similar content on the web. Where Tavily answers "what does the web say about X?", Exa answers "what else exists that is like this?" Useful for the CAO finding comparable companies, similar research papers, or analogous market situations. Input: a URL or text fragment. Output: semantically related content.

---

### Diffbot
**Cost:** Free trial, paid plans

Structured web extraction at scale. Send any URL; Diffbot classifies the page type (article, product, company, person, event) and returns a fully structured JSON object with all relevant fields extracted. No scraping code, no prompt engineering, no schema definition — it just knows what kind of page it is and extracts accordingly. Also provides a Knowledge Graph: query for a company or person and get back a structured profile aggregated from across the web. Input: a URL or entity name. Output: structured JSON with extracted fields.

---

### BuiltWith
**Cost:** Free tier for basic lookups, paid for bulk

Send a domain, get back every technology that site runs: CMS, analytics, CDN, e-commerce platform, email provider, A/B testing tools, tracking pixels, payment processors. The CAO uses this for competitive intelligence — understanding what technology stack a prospect or competitor runs before a pitch or market analysis. Input: a domain. Output: full technology profile.

---

### Hunter.io
**Cost:** Free tier (25 searches/month)

Send a company domain, get back verified professional email addresses associated with it — found, pattern-inferred, and confidence-scored. Also supports person lookup: name + company → likely email. The Triage Coordinator uses this for outbound research. Not for bulk prospecting — for targeted contact verification. Input: a domain or name. Output: verified email addresses.

---

### Wayback Machine API (Internet Archive)
**Cost:** Free

Query the Internet Archive's 800 billion page archive. Retrieve historical snapshots of any URL at any point in time — how a competitor's website looked two years ago, what a company's pricing page said before the rebrand, whether a press release has been quietly deleted. The CAO uses this for historical research and change tracking. Input: a URL + date range. Output: historical page snapshots.

---

### Common Crawl
**Cost:** Free (AWS S3 public dataset)

A petabyte-scale dataset of crawled web pages, updated monthly. Approximately 3 billion pages per crawl. Not a real-time API — a batch data source. For the Office doing large-scale text analysis or training data collection, Common Crawl is the foundation. Query via AWS Athena or download specific subsets. Input: a domain or URL pattern filter. Output: all crawled content matching the filter.

---

### URLscan.io
**Cost:** Free tier (5,000 scans/month)

Submits a URL for security and content analysis: what the page loads, what JavaScript it executes, what external resources it contacts, what cookies it sets, what it looks like rendered. Produces a full screenshot and structured report. The Compliance Watchdog uses this when evaluating external links before the Office acts on them — particularly for client-submitted URLs or Signal Scout escalations from unfamiliar sources. Input: a URL. Output: full security and content analysis with screenshot.

---

### VirusTotal API
**Cost:** Free tier (4 lookups/minute)

Send a URL, domain, IP, or file hash; get back security intelligence from 70+ antivirus engines and threat intelligence databases. The Compliance Watchdog uses this as a standard check on any external URL before it enters the Office's research pipeline. Input: a URL or hash. Output: threat intelligence from 70+ sources.

---

## Responsible Use

The Office scrapes and collects data at scale. Several constraints apply:

- **robots.txt** — respect `Disallow` directives. Crawl4AI checks this by default; do not override.
- **Rate limiting** — even free APIs have limits. The COO's task scheduler should enforce per-source rate limits to avoid bans and maintain access.
- **Terms of service** — some platforms explicitly prohibit automated data collection (LinkedIn, for example). These are not in the source list above; do not add them.
- **Data retention** — data collected from third parties should be stored in ChromaDB with source attribution and collection timestamp. This is an audit and provenance requirement.
- **Personal data** — any data that could identify individuals (names, emails, profiles) is subject to GDPR. The Compliance Watchdog monitors for PII in incoming data streams.
