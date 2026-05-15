# NIBE Client Agent — Enterprise AI Agent for NIBE Industrier

**Prepared by:** @theoffice_ CEO  
**Date:** 2026-05-15  
**Classification:** Confidential — Internal Board Document

---

## 1. The Opportunity

NIBE Industrier AB is a Swedish heating, cooling, and energy systems manufacturer, founded in 1952 by Nils Bernerup. Headquartered in Markaryd, Sweden, the company is a constituent of the OMX Nordic 40 and operates three business segments:

| Segment | Share of Revenue | Description |
|---|---|---|
| Climate Solutions | ~68% | Heat pumps, water heaters, ventilation (residential, commercial, industrial) |
| Element | ~25% | Global leader in heating elements for industrial and medical sectors (counter-cyclical) |
| Stoves | <10% | Fireplace heating products |

### Market Context

- **European heat pump market:** $22.5B (2025) → $41.7B by 2032 (CAGR ~9.2%)
- **Policy tailwind:** REPowerEU mandates 60 million new heat pumps. EU Heat Pump Action Plan accelerates phase-out of fossil-fuel heating.
- **2025 growth:** Heat pump sales grew 11% across 16 European countries, reversing a 2024 downturn.
- **NIBE position:** Top-3 player in European residential heat pumps. 72% of group revenue from renewable products.

### Key Financials (2025)

| Metric | Value |
|---|---|
| Revenue | SEK 40.8 billion (flat YoY, Q4 recovery) |
| Operating margin target | 14–16% |
| Geographic split | Europe ~70%, North America ~25% |
| Employees | ~20,000 globally |

### Competitor Landscape

| Competitor | Profile |
|---|---|
| **Daikin** | Global volume leader, R&D advantage. Expanding Poland/Germany production. |
| **Viessmann** | Premium residential HVAC, strong digital push. Key in DACH region. |
| **Bosch Thermotechnology** | Broad HVAC portfolio, strong OEM channels. |
| **Carrier Global** | Transatlantic scale, commercial HVAC strength. |
| **Mitsubishi Heavy** | NIBE partner since 2009 (joint heat pump development). Also competitor in commercial. |
| **Others** | Vaillant, Panasonic, Hitachi, Alfa Laval, Danfoss (adjacent segments). |

---

## 2. Core Capabilities

### A. Knowledge Base (RAG)

Retrieval-augmented generation pipeline. Users ask natural-language questions and receive cited answers from authoritative sources.

**Data sources:** Annual/interim reports (10+ years), segment P&L data, product specifications, myUplink platform documentation, competitor filings, EU regulation database, acquisition history, patent landscape.

**Output:** Natural-language answers with source citations. Confidence scoring. Follow-up capability.

### B. Financial Intelligence

Automated extraction, visualization, and analysis of NIBE financial data. Trend analysis, peer benchmarking, scenario modeling.

- Quarterly report extraction → trend lines
- Segment P&L breakdown (Climate 68%, Element 25%, Stoves 7%)
- EBIT margin tracking vs 14–16% target
- Geographic revenue analysis (Europe 70%, NA 25%)
- Peer comparison (Daikin gross margin, Bosch HVAC revenue)
- What-if scenario modeling

### C. Competitive Intelligence

Continuous monitoring and structured analysis of competitor activity.

**Monitored:** Daikin (factories, products, M&A), Viessmann (digital platform, market share), Carrier (commercial deals, NA expansion), Mitsubishi (technology partnerships).

**Delivery:** Weekly Slack/Dynamics digest. On-demand competitor briefs. Alerts on significant moves (acquisitions, new products).

### D. Report & Presentation Generation

Converts raw data and analysis into structured deliverables.

| Format | Use Case |
|---|---|
| PDF | Board reports, strategy memos |
| PPTX | Strategy decks, sales presentations |
| HTML | Dashboards, internal wikis |
| Slack | Daily briefs, alerts |

**Templates:** Monthly board report, market entry memos, sales battle cards (vs Daikin, vs Viessmann), installer training materials.

### E. Executive Briefing

Role-specific daily summaries:

| Persona | Deliverable |
|---|---|
| CEO | 5-minute daily: market moves, competitor activity, regulatory changes |
| CFO | Financial extract + margin alerts, segment profitability flags |
| CCO | Sales enablement briefs: subsidy changes, competitor pricing, installer sentiment |
| CTO | Technology alerts: patents, natural refrigerant developments, efficiency benchmarks |

### F. Presentation & Training Production

End-to-end slide deck generation with narrative flow, data visualization, and branded formatting. Investor relations, partner enablement, product launches, installer training, trade show content.

---

## 3. Extended Use Cases

### A. Sales Enablement

- Generate proposals for developers with efficiency data, ROI, competitor comparisons
- Real-time subsidy lookup by country
- Building permit analysis → heat pump fit scoring
- Battle cards: counter-arguments for key competitors
- **Impact:** Proposals in minutes instead of days

### B. Marketing Team

- Thought leadership articles (REPowerEU angle)
- Share of voice analysis vs Daikin in trade press
- Case study templates from WaterFurnace installations
- SEO briefs by region

### C. Aftermarket & Service

- myUplink telemetry analysis → predictive maintenance alerts
- Warranty claims analysis by product line, region, installer
- Root cause pattern identification
- **Impact:** Reduced callout costs, improved customer satisfaction

### D. M&A Target Screening

- Screen European HVAC: SEK 200M–1B revenue, double-digit margins, no NIBE presence
- Monitor acquisition integration KPIs (e.g., Selmo)
- Technology mapping (natural refrigerants, modular heat pump patents)

### E. Regulatory Early Warning

- F-Gas phase-down schedule → model impact on refrigerant supply
- EPBD revision alerts with executive summary
- Country-level subsidy tracker (France, Germany, UK, Poland, Sweden)
- **Impact:** Proactive compliance, reduced regulatory risk

---

## 4. Technical Architecture

### Three-Layer Architecture

```
┌───────────────────────────────────────────┐
│ LAYER 1: DATA                              │
│ RAG pipeline — vector DB (Chroma/Pinecone) │
│ Financials | Products | Competitors         │
│ Regulations | News | myUplink               │
└───────────────────┬───────────────────────┘
                    ▼
┌───────────────────────────────────────────┐
│ LAYER 2: AGENT CORE                        │
│ Orchestrator (Hermes / LLM)                │
│ Query parsing | Context assembly            │
│ Response formatting | Tool routing          │
└───────────────────┬───────────────────────┘
                    ▼
┌───────────────────────────────────────────┐
│ LAYER 3: TOOLS & OUTPUTS                   │
│ Report gen (PDF/PPTX) | Data viz            │
│ Web search | Slack/Teams/PowerBI connector  │
└───────────────────────────────────────────┘
```

### Data Freshness Strategy

| Source | Refresh Frequency |
|---|---|
| Annual/interim reports | On publication (auto-alert) |
| Competitor news | Daily web scrape + RSS |
| Regulation tracker | Weekly EU/national policy DB check |
| Product data | Manual on NIBE updates |
| myUplink data | Real-time API (read-only) |

### Security & Governance

- **Auth:** NIBE SSO / Azure AD. Role-based access per department.
- **Data isolation:** Tenant-level separation. No cross-customer leakage.
- **Audit:** All queries logged with user, timestamp, content. Full traceability.
- **Compliance:** GDPR-compliant. Configurable data retention policies.

---

## 5. Execution Plan — MVP

**Scope:** Read-only Q&A on public NIBE data.  
**Timeline:** 3 weeks (assumes clean data access Day 1)

### Phase 1: Foundation (Week 1–2)

- Gather data sources (3 years NIBE reports, top-5 competitor filings, EU regulation summaries)
- Set up vector database (ChromaDB or Pinecone)
- Build ingestion pipeline. Index all documents.

### Phase 2: Agent Setup (Week 2–3)

- Deploy LLM backend (Hermes or equivalent)
- Build query → retrieval → answer pipeline
- Set up Slack bot connector
- Test with 20 real NIBE-relevant questions
- Iterate on answer quality and citation accuracy

### MVP Deliverables

- Working Slack bot answering questions about NIBE business, financials, competitors, regulations
- Source citations for every answer
- Confidence scoring (answers below threshold trigger fallback response)
- Simple usage dashboard (queries/day, satisfaction rate)

### MVP Exclusions

- No report generation (PDF/PPTX)
- No data visualization or charts
- No myUplink integration
- No automated news ingestion
- No role-specific briefings
- No permission system beyond basic auth

### Success Criteria

**Week 3:** A NIBE sales rep and product manager can query the bot and get useful, cited answers within 5 seconds. 80%+ answer satisfaction rate on a test set of 50 questions.

---

## 6. Execution Plan — Full Product

**Timeline:** 3 months total (including MVP phase)

### Month 1: Data & Infrastructure

- Complete data ingestion (10 years reports, patents, competitor library, subsidy databases)
- Production RAG pipeline with auto-refresh
- SSO integration (NIBE Azure AD)
- Tenant isolation + audit logging

### Month 2: Tooling & Connectors

- Report generation engine (PDF, PPTX)
- Data visualization (charts, trend lines, heatmaps)
- Slack, Teams, and Dynamics connectors
- Competitor news scraping pipeline
- myUplink API integration (read-only)

### Month 3: Pilot & Iteration

- Pilot with one department (Sales or Strategy)
- 20 users, 2-week sprint
- Collect feedback, measure time saved
- Fix quality gaps
- Handover documentation + NIBE admin training
- Go/no-go for enterprise rollout

### Full Product Deliverables

| Deliverable | Description |
|---|---|
| Board reports | Segment performance, competitors, regulation |
| Strategy decks | 5-slide narratives with data viz |
| Investor materials | IR decks, analyst briefs |
| Executive briefings | Role-specific daily summaries |
| Competitor digest | Weekly pushed to Slack with rankings |
| myUplink alerts | Predictive maintenance notifications |
| M&A screening | Automated target identification |
| Regulatory watch | EPBD, F-Gas, subsidy change alerts |
| Admin dashboard | Query analytics, satisfaction, data freshness |

---

## 7. Pricing Model

SEK/month retainer + usage. Three tiers.

### Tier Structure

| Tier | Price/Month | Range | Includes |
|---|---|---|---|
| **MVP** | SEK 50K | (85K) | One department (up to 20 users). Basic RAG (public data). Email support. No SLA. |
| **Standard** | SEK 150K | (250K) | Up to 100 users. All data sources. Report gen (PDF). Slack + Teams. Weekly refresh. Business hours support. 99% uptime SLA. |
| **Enterprise** | SEK 300K | (500K) | Unlimited users. Custom connectors. myUplink integration. Dedicated support engineer. Daily refresh. 99.9% SLA. On-prem option. |

### Rationale

SEK 150K–300K/month is below the cost of a single senior consultant or analyst, but delivers the equivalent of a team of 3–5 analysts. European enterprise SaaS for industrial companies typically lands at 100K–500K SEK/month for vertical AI agents.

### Contract Terms

| Phase | Cost |
|---|---|
| Setup fee | SEK 200K–500K (one-time, covers Month 1–2 build) |
| Month 1 | Build + data ingestion (setup fee only, no retainer) |
| Month 2 | Tooling + connectors (setup fee only, no retainer) |
| Month 3 | Pilot begins — retainer starts at pilot tier |
| Month 4 | Handover. Production SLA. NIBE admin trained. |
| Annual commit | 10–15% discount on monthly retainer |

---

## 8. Sales Pitch

### The Pitch

> *"NIBE already leads in hardware. This agent makes your information advantage match your product advantage."*

### The Problem

- A sales rep in Poland spends 2 hours searching for efficiency data to counter a Daikin proposal.
- The CFO wants to know the F-Gas phase-down impact on refrigerant costs — it takes 3 days to assemble the answer.
- Strategy needs a competitive landscape update before a board meeting — someone stays up all night compiling it.
- A German installer can't find the latest subsidy rates — they recommend a competitor's system instead.

### The Solution

One Slack bot. Any question, any time. Cited answers. Reports generated in seconds, not days. Proactive alerts when regulation or competition shifts. Role-specific briefings that save executives 5–10 hours per week each.

### The ROI

| Benefit | Value |
|---|---|
| Executive time | 10 hrs/week recovered (~1.3M SEK/year per executive) |
| Sales cycles | 2 days → 5 minutes for proposal data |
| Analyst replacement | Team of 3 replaced by one agent |
| Regulatory risk | Early warnings prevent compliance gaps |
| M&A efficiency | Target screening: weeks → minutes |

---

## 9. Next Steps

1. **VALIDATE** — Present this plan to NIBE CFO or Head of Strategy. Confirm pain points, budget timeline, stakeholder alignment.

2. **SCOPE** — Pick 2–3 use cases for initial deployment. Recommended: Financial Intelligence + Sales Enablement as highest-ROI entry point.

3. **PILOT** — Deploy MVP to one department (Strategy or Sales). 3-week sprint. Measure time saved, answer quality, user satisfaction. Iterate.

4. **EXPAND** — After 8-week pilot sign-off: full product rollout. Enterprise tenant. Admin training. Production SLA.

5. **RETAIN** — Weekly knowledge refresh. Quarterly roadmap review. Feedback loop → continuous improvement. The agent becomes as indispensable as NIBE's ERP.

---

*This document contains confidential information intended for the Board of @theoffice_. Not for distribution outside the organization.*

*Generated: 2026-05-15 | Prepared by: CEO of @theoffice_*
