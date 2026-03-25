# Technical Summary — The Office

---

## TL;DR

A locally-hosted, three-tier agent swarm running frontier-class open models on Apple Silicon. No cloud. No API bills. No data egress. Agents compose via capability-keyed model switching, compile traits into fixed-cost system prompts, spawn stateless workers with scoped context, and offload completed work to a vector store — so the swarm performs identically on day 300 as on day 1.

---

## Stack

```
Runtime:         Python
Models:          Ollama / MLX (Apple Silicon) · llama.cpp Metal backend
Memory:          ChromaDB (vector) · JSONL (session) · heartbeat.md (operational state)
Communication:   MCP (Model Context Protocol) — JSON-RPC, inter-agent
Orchestration:   Custom gateway · SQLite DAG · COO process
Data:            Crawl4AI · ScrapeGraphAI · SearXNG · Perplexica · 20+ public APIs
Hardware:        Mac Studio M5 Ultra · 512GB unified memory (production)
```

---

## Agent Hierarchy

Three tiers. Hard separation of concerns.

```
Management    CEO / CTO / CFO / CAO    70B–405B    reasoning, planning, oversight
Specialists   COO / DOE / CMO / CCO    70B         domain execution, task routing
Workers       8 types + custom         7B–14B      narrow tasks, stateless, spawnable
```

**Management** runs frontier-class models because it does the hard reasoning. **Specialists** translate directives into concrete tasks. **Workers** are not processes — they are templates. The COO instantiates them, they execute one task, write the result back to the DAG, and are torn down. No worker persists between tasks. No context accumulates.

---

## Traits — Two-Layer Architecture

Every agent carries a set of traits. The insight: documentation and runtime instruction are two different things, and conflating them is a performance tax.

**Documentation layer** — full prose description of who the trait is, why it exists, where it conflicts. Written for humans. Lives in `traits/*.md`. **Never injected into any model context. Ever.**

**Runtime fragment** — `## Runtime Fragment` section at the end of each trait file. 5–8 bullet points, second-person imperative, ~150–200 tokens. Distilled to only what demonstrably changes model behavior.

At spawn, `compile_constitution.py` reads the agent's trait + influence list, pulls only the `## Runtime Fragment` from each file, and assembles a `[CONSTITUTION]` block in the system prompt. This happens **once**. The system prompt is fixed. It never changes during the session.

**The actual cost of a fully-specified CEO:**

| Component | Tokens |
|---|---|
| 7 trait runtime fragments (~175 tokens each) | ~1,225 |
| 1 influence runtime fragment | ~200 |
| Role block | ~100 |
| **Total** | **~1,525 tokens — fixed forever** |

A 500-turn session costs the same in constitution overhead as a 1-turn session. The per-message context window — where degradation actually happens — is governed separately.

---

## Influences — Reasoning Style, Not Just Behavior

Traits shape *how* an agent behaves. Influences shape *how* it thinks.

Each influence file models a real figure's core philosophy, decision patterns, and non-negotiables. Same two-layer structure. Same runtime fragment compilation. Different effect: an influence operates at the level of reasoning style and judgment, not behavioral rule.

Current influence assignments: Ayn Rand → CEO (first principles, zero compromise on logic) · Elon Musk → CTO (first-principles engineering, high velocity) · Warren Buffett → CFO (capital preservation, margin of safety) · Jack Welch → CAO (performance culture, rigorous candour).

---

## Context Discipline — The Core Architectural Principle

Context rot is a real, measurable failure mode. From production data on the OpenClaw gateway:

| Agent type | Context overhead after 1 month of daily use |
|---|---|
| Generalist (multi-purpose) | ~45,000 tokens — **40% performance drop** |
| Single-purpose (narrow scope) | ~1,400 tokens |

By month 6 of a generalist agent: 50–90% performance decrease, ~52¢ of extra cost per message *before the first word is generated*. The model is still capable. It is spending most of its attention budget on noise.

The Office treats this as a critical failure mode and builds against it at every layer:

**Workers start clean.** Every spawned worker gets a compiled, task-scoped context — ~1,400 token target. Nothing from prior tasks, nothing from other agents, nothing from the conversation history that doesn't belong to this task.

**Completed work leaves context.** When a worker finishes, its output writes to the task DAG and is immediately picked up by the Digital Archivist → embedded → stored to ChromaDB. From that point it is retrievable by query, not carried in any agent's context window. History accumulates in a searchable store. It does not accumulate in prompts.

**Parallel spawning isolates exploration.** When any agent needs to explore competing approaches (multiple code architectures, campaign directions, strategic paths), it spawns parallel sub-agents rather than exploring sequentially in its own context. The spawning agent compares returned results. Rejected paths are discarded before they enter the primary context window.

**Heartbeat compression.** The COO and CEO — which must maintain operational awareness over extended sessions — compress their working memory on a regular cycle. The COO writes a `heartbeat.md` on each tick: a curated, compressed state summary it will read on the *next* tick instead of its full session history. The COO literally programs its own future behavior by writing to the file it will next read. This is the mechanism that enables 24/7 autonomous operation without unbounded history growth.

**System prompt vs message thread.** The `[CONSTITUTION]` block lives in the system prompt — architecturally separate from the messages array. The messages array is where accumulation happens. The constitution does not participate in that accumulation. Day 1 and day 300 have identical constitution overhead.

---

## Model Switching — The `agnostic` Trait

Different phases of work call for different model tiers. Running every phase through the same model is both a quality failure and a compute waste.

| Capability | Model class |
|---|---|
| Deep reasoning, planning | 405B / frontier |
| Domain execution, synthesis | 70B instruction-tuned |
| Structured writing, summarisation | 14B (Phi-4) |
| Extraction, classification | 7B (Mistral) |
| Fine-tuned specialists | Any size, domain-trained |

An agent carrying the `agnostic` trait identifies which phase it is currently in, evaluates whether the next phase warrants a model switch, and if so: **serializes full task state to a checkpoint, terminates, and the orchestrator spawns a new instance under the target model with the checkpoint path.**

The critical constraint: when a model switches, the KV cache is gone. This is not CPU thread context-switching. It is a complete handoff between two separate inference processes. Whatever the previous instance knew must be in the checkpoint. Nothing outside it can be assumed.

**Checkpoint format (key fields):**
```json
{
  "goal": "original goal, verbatim",
  "phase_completed": "what just finished",
  "phase_next": "what to do next",
  "findings": "accumulated outputs",
  "context_summary": "compact, self-contained prose summary of all reasoning — the critical field",
  "model_from": "model that wrote this checkpoint",
  "model_to": "model to spawn next"
}
```

**The model registry** maps capability keys to model identifiers. Agents request a capability (`reasoning`, `writing`, `extraction`, `image`, `tts`, etc.) — never a specific model. The registry resolves it. Swapping to a better model means one line change. No agent code changes.

A single long-horizon task might use: 405B (planning) → 7B×5 parallel (signal extraction) → 14B (brief writing) → 7B (classification + tagging). Four models. One task. One preserved context thread.

The full registry covers 50+ capability keys across: text reasoning, code, security, vision, image generation, design tools, video understanding, video generation, music, TTS (five variants including voice cloning), transcription with speaker diarization, translation (200+ languages), embeddings, math, document parsing, table reasoning, 3D reconstruction, and biomedical/molecular science.

---

## Orchestration — Beyond a Task Queue

The current model: a flat task queue owned by the COO. The target: a proper orchestration layer with five components.

**1. The gateway (COO process)** — a persistent Python process that is the source of truth for workflow state. Not an agent — a process. The COO agent runs *inside* it. The gateway owns the DAG, not the agent.

**2. Task DAG** — replaces the flat queue. Each task carries: `id`, `type`, `assigned_to`, `status`, `depends_on[]`, `context_schema`, `spawned_by`, `retry_count`. The gateway walks the DAG, spawns workers for resolved dependencies in parallel, and tracks blocked/running/done state.

**3. Context compiler** — runs before every worker spawn. Reads the task's `context_schema`, retrieves relevant records from ChromaDB, assembles a minimal context block, validates against schema, and rejects if it exceeds the token budget. Target: ~1,400 tokens per worker spawn. This is the most important component currently missing — the difference between context discipline as aspiration and as hard architectural guarantee.

**4. Error classifier** — distinguishes: `transient` (retry with backoff) / `bad_output` (reformulate, retry max 2) / `scope_exceeded` (escalate to specialist) / `authority_exceeded` (pause, notify board) / `budget_exceeded` (hard stop, notify CFO) / `fatal` (mark failed, notify COO).

**5. Trace log** — append-only JSONL. Every spawn, every tool call, every handoff, every error classification. Input to the Compliance Watchdog. Source for the Executive Briefer's daily report.

**Candidate stack:** SQLite + Python DAG walker (Option A, build in weeks) → Temporal for durable replay on crash (Option B, production). Agent communication via MCP (JSON-RPC, interoperable). Traces via OpenTelemetry → Langfuse local.

---

## Sniper Agent Philosophy

> A single-purpose agent with a tightly scoped context and a small toolset outperforms a generalist by **5–10x** on its target task.

**The 7–10 tool limit.** Above this, the wrong skill gets selected at the wrong time, context fills with schemas rarely used, and behavior becomes inconsistent. This is an observable performance cliff, not a soft guideline. If a worker's tool list exceeds 10 items, split the agent.

**Pass/fail evaluability.** Narrow goals make performance binary. Either the research brief answers the brief or it does not. Generalist failures are always partially defensible. Sniper failures are not. This makes automated quality gates practical.

**Composability.** A narrow agent with well-defined inputs and outputs can be duplicated and repurposed with minimal work. A YouTube content worker becomes a TikTok worker by swapping the output format and posting tool. Workers are stamped from templates, not hand-crafted one-offs.

**Predictability = autonomy.** A narrow agent running 3 cron tasks is *more* autonomous than a generalist, not less — because its behavior is entirely predictable. Predictability is the prerequisite for trust. You can put a predictable agent into production and leave it alone.

---

## Shared Memory — The Digital Archivist Pattern

Narrow agents need cross-session context without carrying it themselves. The solution is not direct coupling between agents. It is a shared journal.

The Digital Archivist is that journal. Every completed task output is received, summarized, embedded, and stored to ChromaDB. Any agent that needs past work queries the Archivist. It receives a targeted retrieval result scoped to its current need — not another agent's full history.

**This is how the swarm shares knowledge without coupling agents to each other's context windows.**

ChromaDB + Nomic/MXBai embeddings for dense retrieval. The CAO (Chief Analytics Officer) is the query gateway for management and specialist agents. Workers can query directly for task-scoped retrieval.

---

## Local-First — The Non-Negotiable Architectural Choice

All inference runs locally. Not for cost reasons primarily — for architectural ones.

**Data sovereignty.** Every token generated stays on hardware the client controls. Relevant for legal (privileged communications), healthcare (HIPAA, EU sector rules), and financial services (AI Act audit trail requirements). Local deployment closes these gaps *structurally*, not contractually.

**Model ownership.** Local-first means you own the model stack. Fine-tune on internal data. Version-pin models so behavior doesn't change when a vendor pushes an update. Quantize for your hardware. Run multiple models simultaneously in 512GB unified memory. None of this is possible through a hosted API.

**Continuous improvement from production.** Every task the Office executes is potential training signal. Fine-tuning runs on the same hardware that runs inference. Real internal data — procurement documents, contract libraries, client interaction histories, brand voice examples — never leaves the premises. The model improves from production use. With a hosted API, outputs are discarded. Here they become training data.

**Fixed cost structure.** Hardware is a one-time capital expenditure. Zero marginal inference cost regardless of swarm size or call volume. At cloud API pricing for comparable throughput, a Mac Studio M5 Ultra (~€22K) pays for itself within months. Beyond that, every inference is free.

---

## The Meta Layer

The framework is both the factory and the first product. The office in `agents/` runs the business building this platform. Every improvement to the internal office makes the product better. Every client deployment generates patterns that feed back into the framework. Internal operation and product development are the same work.

---

*Context discipline: [`research/context-discipline.md`](../research/architecture/context-discipline.md) · Orchestration: [`research/orchestration.md`](../research/architecture/orchestration.md) · Local-first: [`research/local-ai.md`](../research/models/local-ai.md) · Model registry: [`traits/agnostic.md`](../traits/agnostic.md) · Full model catalogue: [`research/models.md`](../research/models/models.md) · Architecture: [`office.md`](../framework/office.md)*
