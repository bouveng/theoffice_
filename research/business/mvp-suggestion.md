# MVP Suggestion — The Mini Office

## What the MVP Is

The MVP is the smallest version of the Office that completes a real task cycle end-to-end without human intervention between steps. Not a demo. Not a prototype that needs babysitting. A loop that runs.

The loop:

```
Human sets a goal
    → CEO decomposes it into a task DAG
        → COO routes tasks to Workers
            → Workers execute and write results
                → Digital Archivist stores to ChromaDB
                    → Executive Briefer produces daily summary
                        → Human reviews the brief
```

That is a complete, useful thing. It replaces what a small operations team does on a good day — with no meetings, no misunderstandings, and a full audit trail.

---

## Agent Composition

The full Office has 12 agents. The MVP runs 5.

| Agent | Tier | Model | Role in MVP |
|---|---|---|---|
| CEO | Management | Llama 3.1 70B | Receives goal, decomposes into task DAG, final quality gate |
| COO | Specialist | Llama 3.1 70B (4-bit) | Owns task queue, routes to workers, monitors completion |
| Digital Archivist | Worker | Mistral 7B v0.3 | Stores all results and logs to ChromaDB |
| Signal Scout | Worker | Llama 3.1 8B | Scans external feeds for relevant signals, surfaces to CEO |
| Executive Briefer | Worker | Phi-4 14B | Compiles and delivers the daily human-readable brief |

**Why these five?** They form a complete intelligence-and-reporting cycle without creative or engineering output. The CEO thinks, the COO routes, the workers gather/store/report. No code generation, no image generation — those add complexity without proving the core loop.

What's deliberately excluded from MVP:
- CTO, CFO, CAO (management depth — not needed to prove the loop)
- DOE, CMO, CCO (domain specialists — added in v1.1)
- Hallucination Hunter, QA Specialist, Triage Coordinator, Compliance Watchdog (quality and ops layers — valuable, not critical for MVP)

---

## Hardware for MVP

**Development hardware (start now):**

Mac Mini M4 Pro, 64GB unified memory — ~€2,200

- Runs Llama 3.1 70B at 4-bit (~40GB) for CEO/COO
- Runs 8B–14B workers concurrently in remaining memory
- Cannot run all five models simultaneously without model swapping, but sufficient for sequential task execution during development
- Available immediately, no lead time

**Production hardware (Q2 2026, when MVP goes live):**

Mac Studio M5 Ultra, 512GB unified memory — €17K–€23K

- All five MVP models resident in memory simultaneously (~250GB total)
- No model swapping between tasks
- Scales directly to the full 12-agent Office without hardware change

The MVP is developed on the Mac Mini and validated on the Mac Studio. The Mac Mini is not thrown away after — it becomes a secondary dev/test node.

---

## What the MVP Delivers

A single, demonstrable capability: **autonomous goal-to-brief execution**.

Give the system a goal in plain language. Example inputs suitable for a startup:

- "Research the three largest competitors entering our market this quarter and produce a summary of their positioning."
- "Monitor our top 10 industry sources this week and flag anything relevant to our product roadmap."
- "Compile the week's completed tasks, blockers, and open questions into a Friday brief."

The system:
1. Accepts the goal
2. Breaks it into discrete tasks with dependencies
3. Executes tasks using workers
4. Stores all outputs to the vector database
5. Delivers a structured brief by the defined deadline

Human involvement: setting the goal and reading the brief. Nothing in between.

---

## What the MVP Does Not Do

Being explicit about this matters for honest evaluation:

- **No autonomous decision-making.** The CEO decomposes and routes — it does not make strategic decisions without human input. The human sets the goal; the system executes it.
- **No financial autonomy.** CFO is not included. No autonomous spending, API cost management, or budget tracking.
- **No code output.** CTO and DOE are excluded. The MVP cannot build or modify software on its own.
- **No creative output.** CMO and CCO are excluded. No campaigns, no assets.
- **No email/communication handling.** Triage Coordinator excluded.
- **Not real-time.** The MVP runs task cycles on demand or on a schedule. It is not a persistent always-on process in v1.

---

## Success Criteria

The MVP is done when all of the following are true:

1. A human can submit a goal via a simple interface (CLI or basic web UI) and receive a structured brief without touching anything in between.
2. Every task execution is logged and retrievable — full audit trail, no black boxes.
3. The Digital Archivist correctly stores all results to ChromaDB, retrievable by later queries.
4. The system handles a failed worker gracefully — logs the failure, marks the task, surfaces it in the brief rather than silently dropping it.
5. The cycle completes in under 30 minutes for a typical research goal.
6. The system runs for 48 hours without human intervention on a drip-feed of scheduled goals.

---

## Build Sequence

### Phase 1 — Infrastructure (weeks 1–3)
- Install Ollama on Mac Mini, pull initial models (Mistral 7B first, then 70B)
- Validate Metal backend: confirm models load and infer correctly
- Set up ChromaDB instance, define schema for task logs and research outputs
- Implement the task queue: SQLite-backed DAG with status tracking

### Phase 2 — Worker Layer (weeks 4–6)
- Implement Digital Archivist: receives any text input, embeds, stores to ChromaDB
- Implement Signal Scout: polls RSS/feed list, filters by relevance keyword set, outputs structured signal objects
- Implement Executive Briefer: receives task results from queue, produces templated brief in markdown
- Unit-test each worker in isolation with fixed inputs

### Phase 3 — Orchestration Layer (weeks 7–9)
- Implement COO: reads task queue, assigns workers, monitors completion, escalates stalls
- Implement CEO: receives goal, produces task DAG, hands off to COO
- Integration test: single goal → full cycle → brief

### Phase 4 — Validation (weeks 10–12)
- Run 20 structured test goals covering different input types
- Measure: brief quality, task completion rate, failure handling, cycle time
- Fix the top 5 failure patterns
- 48-hour unattended run on Mac Mini hardware

**Target completion: end of Q2 2026 (June 2026)**

---

## What Comes After MVP

Once the loop works reliably, the additions are modular — each adds one domain:

| Version | Added agents | New capability |
|---|---|---|
| v1.0 (MVP) | CEO, COO, 3 workers | Goal-to-brief autonomous cycle |
| v1.1 | + CFO, Compliance Watchdog | Cost tracking, API spend monitoring |
| v1.2 | + CTO, DOE, QA Specialist | Code generation and testing |
| v1.3 | + CMO, CCO, Media Assembly Line | Marketing and creative output |
| v2.0 | Full 12-agent Office | Fully autonomous operations |

Each version is usable and deliverable to a real client. v1.0 is valuable to any information-heavy business. v1.1 adds financial oversight. By v1.3 you have a full marketing department.

---

## Example Flow — "Get Svenssons Sås into Scan's product lineup"

A startup has developed a small-batch Swedish BBQ sauce — smoked, locally sourced, genuinely good. They want Scan to carry it under the Scan Chark umbrella or as a co-branded product. They have a product, no sales team, and one founder with too much to do. They hand the goal to the Office.

---

### Input

The human types one goal:

```
We want to pitch Scan Food Group on carrying Svenssons Sås as part of
their chilled deli/BBQ lineup. Research their procurement process, current
product gaps, key contacts, relevant market trends, and any recent news.
Give me a pitch prep brief by Friday morning.
```

---

### Step 1 — CEO decomposes the goal

The CEO reads the goal and produces a task DAG:

```
GOAL: Pitch prep brief for Scan Food Group partnership
│
├── T1  Research Scan's current chilled/BBQ product range
│       → Who: Signal Scout
│       → Depends on: nothing
│
├── T2  Research Scan's procurement and partnership process
│       → Who: Signal Scout
│       → Depends on: nothing
│
├── T3  Identify key decision-makers (procurement, product development)
│       → Who: Signal Scout
│       → Depends on: nothing
│
├── T4  Scan recent news — acquisitions, sustainability commitments,
│       new product launches, supplier relationships
│       → Who: Signal Scout
│       → Depends on: nothing
│
├── T5  Swedish BBQ/condiment market trends — growth, consumer shifts,
│       premium/local positioning, competitor brands
│       → Who: Signal Scout
│       → Depends on: nothing
│
├── T6  Store all research to memory
│       → Who: Digital Archivist
│       → Depends on: T1, T2, T3, T4, T5
│
└── T7  Compile pitch prep brief
        → Who: Executive Briefer
        → Depends on: T6
```

Seven tasks. Five run in parallel (T1–T5). T6 runs when they complete. T7 runs last.

---

### Step 2 — COO routes and spawns

The COO reads the DAG, sees T1–T5 have no dependencies, and spawns five Signal Scout instances simultaneously. Each gets a clean, narrow context — no awareness of the other tasks running in parallel.

Signal Scout T1 gets:
```
Search for Scan Food Group's current chilled deli and BBQ product range.
List product lines, brand names, price positioning, and any gaps or
discontinuations. Return structured findings.
```

Signal Scout T4 gets:
```
Find recent news (last 6 months) about Scan Food Group Sweden.
Focus on: new product launches, sustainability announcements,
supplier partnerships, leadership changes, acquisitions.
Return a list of dated, sourced items.
```

And so on. Each Scout searches, filters, and returns structured output. The COO monitors status, marks tasks done as results arrive, and triggers T6 when all five are complete.

---

### Step 3 — Digital Archivist stores everything

The Digital Archivist receives the five Scout outputs, summarises each, generates embeddings, and stores them to ChromaDB under a project tag `scan-pitch-2026`. The full source text goes in. Nothing is lost.

---

### Step 4 — Executive Briefer compiles the brief

The Briefer queries ChromaDB for everything tagged `scan-pitch-2026` and produces:

---

**PITCH PREP BRIEF — Scan Food Group**
*Prepared by Office · Friday 06:00*

**The opportunity**
Scan's current BBQ/condiment shelf under Scan Chark is anchored by three SKUs, all mid-market. Their 2025 sustainability report committed to increasing locally sourced supplier partnerships by 30% before 2027. No premium small-batch condiment in their lineup. The gap is real.

**Their procurement process**
Scan runs a supplier portal (scan.se/leverantör). New food products under 500K SEK annual volume go through regional procurement, not central buying. Contact for new product partnerships: procurement team based in Helsingborg. Decision cycle typically 3–6 months from first contact to trial order.

**Relevant recent news**
- Nov 2025: Scan announced a new local producer partnership programme targeting Skåne and Blekinge suppliers
- Jan 2026: Scan relaunched their Chark premium line with updated packaging — signals renewed attention to premium positioning
- Feb 2026: Interview with product director in Livsmedelsindustrin — quoted as looking for "distinctly Swedish, story-driven" products

**Market tailwind**
Swedish condiment market grew 8% in 2025. Premium/artisan segment outperformed at 19% growth. Consumer preference data (HUI Research) shows "locally produced" is now a top-3 purchase driver for chilled deli products, above price.

**Suggested pitch angle**
Lead with the local sourcing story, not the product spec. Reference their 2027 sustainability commitment directly. Propose a 6-month regional trial (Skåne stores) rather than a national rollout ask — lower barrier to yes.

**Contacts to approach**
- Regional procurement, Helsingborg office (via supplier portal)
- Product development lead (name surfaced in Nov 2025 press release — confirm before outreach)

**Open questions for the founder to answer before the pitch**
- What is current production capacity? Can you supply a trial order of 2,000 units/month?
- Do you have food safety certification (FSSC 22000 or equivalent)? Scan will require it.
- What is your wholesale price point? Scan Chark premium typically retails at 49–79 SEK — work backwards from that.

---

**Total cycle time**: 23 minutes from goal input to brief delivery.
**Human involvement**: typing the goal, reading the brief.

---

### What this demonstrates

- The CEO produced a dependency-aware task plan without being told how to break the problem down
- Five workers ran in parallel — the cycle time is bounded by the slowest single task, not the sum of all tasks
- The Digital Archivist means the research is not lost after the brief is read — it is queryable for future tasks (follow-up pitch, competitor research, market updates)
- The Executive Briefer surfaced the three open questions the founder needs to answer — things no amount of external research can answer, but which will determine whether the pitch succeeds

The founder spent 23 minutes doing other things. On a normal day, this is 4–6 hours of research, note-taking, and synthesis.
