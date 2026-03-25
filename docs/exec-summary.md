# Executive Summary — The Office

---

## What

The Office is an autonomous AI enterprise platform — a configurable swarm of locally-hosted AI agents that runs business operations without human involvement between steps. It replaces the operational layer of a company: research, monitoring, coordination, reporting, creative output, and quality control, executed continuously by a structured hierarchy of specialised agents.

The platform ships as a deployable framework. An Office is configured for a specific client — selecting the right agents, models, and data sources for their sector — and operates their business functions autonomously from day one.

The company building this framework runs its own Office to develop and operate the product. That office is the proof of concept, the first client, and the template sold to others.

---

## Why

Small companies cannot afford the operational capacity they need. A two-person founding team spends more time on research, reporting, coordination, and content than on the work that actually creates value. Hiring solves the capacity problem but introduces management overhead, communication lag, personnel risk, and cost that scales linearly with output.

Existing AI tools do not solve this. A chatbot answers questions. A copilot assists a human. Neither runs unsupervised, produces a complete output cycle end to end, or maintains an audit trail. They are accelerators for human work — not replacements for the operational layer.

The Office is different: a goal goes in, a structured output comes out, and nothing in between requires a human. The first time a founder submits a research goal at 22:00 and reads a polished brief at 06:00 without having touched anything overnight, the value proposition is self-evident.

---

## How

The Office runs a three-tier agent hierarchy on local hardware:

**Management** (CEO, CTO, CFO, CAO) — receives goals, decomposes them into task plans, oversees quality, and maintains strategic direction. Runs on frontier-class models (70B–405B parameters) capable of genuine reasoning and long-horizon planning.

**Specialists** (COO, DOE, CMO, CCO) — translate management directives into concrete tasks routed to the worker swarm. Own their domain and are accountable for output quality within it.

**Workers** — eight lightweight agents spawned on demand for a single task and torn down on completion. Signal Scout monitors feeds. Digital Archivist maintains institutional memory. Executive Briefer produces the daily human-readable output. No worker persists between tasks; no context accumulates; no state degrades.

All inference runs locally on an Apple Silicon Mac Studio — no cloud API, no data egress, no per-token billing. The full model stack spans 40+ models across text, code, vision, image, video, music, voice, transcription, translation, and domain-specific science. Models switch mid-task as the work demands, with context preserved across the handoff via a checkpoint protocol. The complete model catalogue is in [`research/models.md`](../research/models/models.md).

Data collection runs through a parallel stack: Crawl4AI and ScrapeGraphAI for web extraction, SearXNG and Perplexica for self-hosted search, 20+ public data APIs for structured intelligence across news, finance, company data, academic literature, and government sources. Details in [`research/data-sources.md`](../research/data/data-sources.md).

---

## Benefits

**Total data sovereignty.** Every inference step, every document, every task output stays on hardware the client controls. No third-party cloud exposure, no GDPR cross-border transfer risk, no vendor data retention. Directly relevant for legal, healthcare, financial services, and any client handling sensitive information. The full argument is in [`research/local-ai.md`](../research/models/local-ai.md).

**24/7 autonomous operation.** The Office does not sleep, context-switch, or require management. It runs scheduled cycles, responds to events, and delivers outputs on time — without a human triggering each step.

**Consistent quality, auditable decisions.** Every task is logged. Every agent decision is traceable. Every output has a full audit trail from goal to brief. No black boxes, no silent failures.

**Composable and sector-adaptable.** A legal firm's Office has different agents, models, and data sources than a marketing agency's. The framework is the same; the configuration changes. New sector deployments add capability without modifying the core.

**Self-improving.** Every task the Office completes is training signal for fine-tuning the next generation of specialist models. The system improves from production use, on data that never leaves the client's premises.

---

## Economy

**Hardware.** One-time capital expenditure. Development on a Mac Mini M4 Pro (~€2,600). Production on a Mac Studio M5 Ultra (~€22,000). No ongoing infrastructure cost beyond power and internet.

**No inference bills.** Zero API costs. A swarm making thousands of inference calls per day generates no per-token charges. At cloud API pricing for comparable volume, the hardware pays for itself within months.

**Build cost.** Full detail in [`office-budget.md`](office-budget.md).

| Milestone | 1 person | 2 people |
|---|---|---|
| MVP (4 months, dev hardware) | ~€23K | ~€39K |
| First production deployment (7 months, incl. Mac Studio) | ~€60K | ~€89K |

**Client pricing model.** Because the Office's cost structure is fixed hardware rather than variable API usage, clients are offered a flat monthly subscription — predictable for them, high-margin for the Office once the hardware is amortised. A single client at €3,000–€8,000/month covers the hardware cost within a quarter.

**The meta layer.** The Office framework is both the factory and the first product. Every improvement made while operating the internal office makes the product better. Every client deployment generates patterns and training data that feed back into the framework. The internal operation and the product development are the same work.

---

*Architecture: [`office.md`](../framework/office.md) · Agents: [`management.md`](../framework/management.md), [`specialists.md`](../framework/specialists.md), [`workers.md`](../framework/workers.md) · Models: [`research/models.md`](../research/models/models.md) · Local-first: [`research/local-ai.md`](../research/models/local-ai.md) · Budget: [`office-budget.md`](office-budget.md)*
