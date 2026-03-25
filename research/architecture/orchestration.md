# Agent Orchestration — Beyond the Task Queue

The [Office](../../framework/office.md) currently has a conceptual task queue owned by the [COO](../../agents/specialists/coo/coo.md). That is a start, not an orchestration layer. A task queue tells agents what to do next. An orchestration layer decides *how* agents coordinate, *what state* survives between them, *when* to route, retry, escalate, or spawn — and gives you visibility into all of it. This document maps the landscape, looks at the frameworks, and builds toward a concrete approach.

---

## OpenClaw — What It Is

OpenClaw is an open-source local gateway framework (145k+ GitHub stars) built around a single idea: a **centralized gateway process** that is the nervous system of the whole system. It connects agents to messaging platforms (Telegram, Signal, Discord, Slack), routes messages through an LLM-powered agent, and is fully local — no cloud dependency.

Its architecture has direct relevance to the [Office](../../framework/office.md):

- **Gateway** — a single persistent process (WebSocket/HTTP server running 24/7) that is the source of truth for sessions, routing, and context. Nothing passes between agents without going through it.
- **ReAct loop** — the agent reasons, calls a tool, observes the result, reasons again. This loop is the execution primitive.
- **Mission Control** — a unified operations dashboard for workflow visibility, approval-driven governance, and agent management.
- **Model-agnostic** — Claude, GPT, Gemini, or fully local via Ollama.

### Actual internals (from the NeurIPS paper author)

Understanding how OpenClaw works internally clarifies what the [Office](../../framework/office.md) needs to build:

- **Session persistence** — every message (user, assistant, tool call, tool result) is appended to a JSONL file. On each new request, the full file is parsed back into a messages array and sent to the model. Simple, append-only, crash-safe.
- **Context compaction** — when the context window would overflow, OpenClaw summarizes chunks, merges summaries, and retries until the context is below 50% of the model's limit. Not elegant, but it works as a floor.
- **Tool schema injection** — only tool *metadata and schemas* are injected into the context, not the full tool code. This limits overhead significantly. The tools themselves live outside the context window.
- **Heartbeat pattern** — a 30-minute timer fires a prompt; the agent reads `heartbeat.md` and acts on it. Crucially, the agent can *write* to `heartbeat.md`, so it programs its own future behavior. The agent becomes the author of its own operating rhythm.

### Context rot — hard numbers

The JSONL approach accumulates cost at a rate most builders underestimate:

- **Day 1 of a generalist agent**: ~7,000 tokens of fixed overhead before any task content
- **After 1 month of daily use**: ~45,000 tokens of history prepended to every call; measured **40% performance decrease** at this level
- **After 6 months of a generalist agent**: **50–90% performance decrease**; ~52 cents of extra cost per message before the first word is generated
- **Single-purpose email agent by contrast**: only ~1,400 tokens of overhead

This is the quantitative case for narrow agents and aggressive context hygiene. A generalist agent that seems fine in week one is quietly degrading toward uselessness by month three.

What OpenClaw makes clear: the gateway *is* the orchestrator. It is not a router sitting in front of agents — it is the persistent, stateful center that agents orbit. This is a useful mental model for the [Office](../../framework/office.md).

**What it is not:** a framework for complex, tiered agent hierarchies with parallel spawning, DAG execution, or fine-grained context isolation per agent. It is messaging-first, conversation-first. Good for personal agents and small teams. Not designed for a swarm with a [management](../../framework/management.md) tier, [specialists](../../framework/specialists.md), and disposable [workers](../../framework/workers.md).

---

## The Four Quadrants of Agent Design

Every agent — regardless of framework, model, or platform — can be fully described by four questions. This is the "harness" model, applicable to any agent in the [Office](../../framework/office.md):

**1. Triggers** — what wakes the agent up?
- Cron schedule (every 30 minutes)
- Heartbeat file (something changed in `heartbeat.md`)
- Webhook (inbound message, event from another agent)
- Manual invocation ([CEO](../../agents/management/ceo/ceo.md)/Board input)

**2. Injections** — what is loaded on every turn?
- System prompt (the agent's role, personality, constraints)
- History (JSONL session file, compiled context block, or nothing for stateless workers)
- Tool schemas (metadata only — not full code)

**3. Tools** — what can the agent call?
- Memory retrieval ([ChromaDB](data-storage.md), journal, archival store)
- Computer control (browser, file system, APIs)
- Skills (other agents as callable tools)
- Output channels (write to a file, post to a queue, call a webhook)

**4. Outputs/Writes** — what does the agent produce?
- Writes to a channel (Slack, Telegram, the Office message bus)
- Writes to memory (updates its own JSONL, writes to a shared log)
- Writes to a task queue (creates or resolves tasks)
- Returns a structured result to the caller

Mapping every [Office](../../framework/office.md) agent against these four quadrants before building it prevents ambiguity. If you cannot answer all four questions concisely, the agent's design is not complete. If two agents share the same quadrant profile, they may be duplicates.

---

## The Major Frameworks

### LangGraph
Graph-based orchestration from LangChain. LangChain itself now says: *"Use LangGraph for agents, not LangChain."*

Execution model: agents are nodes in a directed graph. Edges are conditional — the next node is selected based on state. State is typed and passed as deltas between nodes (not full history). Supports parallel branches, persistent checkpointing, and human-in-the-loop via `interrupt()`.

**Strengths:** precise state control, parallel execution, production-ready, used by Klarna and Replit. **Weakness:** steep learning curve, graph design requires upfront architectural work.

### CrewAI
Python framework built independently from LangChain. Role-based crews with two layers: **Crews** (dynamic role-based collaboration) and **Flows** (deterministic event-driven task orchestration). Simplicity-first.

**Strengths:** fast setup, clear role assignment, good for content and research workflows. **Weakness:** less flexible for complex hierarchies; structured output consistency depends on role design.

### Microsoft AutoGen
Conversational orchestration. Agents converse in a shared session and decide when to speak based on the ongoing exchange. Organic rather than rigid.

**Strengths:** flexible for open-ended iterative problem-solving. **Weakness:** less deterministic than LangGraph; harder to audit; output consistency varies.

### OpenAI Swarm → Agents SDK
Started as an educational framework. Now evolved into the OpenAI Agents SDK (production-ready). Core abstractions: **Agents** (instructions + functions), **Handoffs** (explicit agent-to-agent transfers), **Routines** (sequences of steps). Stateless between calls, runs almost entirely client-side.

**Strengths:** minimal, explicit, observable — you control exactly when control transfers and what travels with it. **Weakness:** tied to OpenAI's API, not suited for local models.

### Haystack (deepset)
Modular pipeline orchestration. Strong RAG story, modular components (retrieval, routing, memory, generation), agent-as-tool composition pattern. Fully vendor-agnostic.

**Strengths:** production-ready, serializable pipelines, local model support. **Weakness:** pipeline-first rather than agent-first — better for RAG systems than multi-agent swarms.

### Letta (formerly MemGPT)
Stateful agents with persistent memory. Three-tier memory model: **Core** (in-context, editable), **Recall** (full history, searchable), **Archival** (external vector DB). All state — messages, reasoning, tool calls — persists to a database. Agents learn during deployment, not just during training.

**Strengths:** true stateful agents, memory hierarchy similar to OS memory management. **Weakness:** higher infrastructure cost, more complexity for lightweight [workers](../../framework/workers.md).

### Temporal / Prefect
Not AI-specific — durable workflow orchestration. Temporal is used by OpenAI's Codex web agent. Any function becomes a durable step: if it crashes, it restarts from the last checkpoint. Handles retries, timeouts, and long-running waits without consuming compute.

**Strengths:** mission-critical reliability, automatic retry, deterministic replay. **Weakness:** significant infrastructure overhead for a local-first swarm; feels like using a sledgehammer for a nail at small scale.

---

## What Orchestration Is Beyond a Task Queue

A task queue answers: *what should be done, and by whom?*

An orchestration layer answers all of the following:

### 1. State management
Who owns the current state of a workflow? What state survives agent handoffs? What happens to state when an agent crashes mid-task? A task queue with a status field is not enough — state needs to be typed, versioned, and persistent. The [COO](../../agents/specialists/coo/coo.md) currently "owns" the task list conceptually, but the actual state lives nowhere durable.

### 2. Context compilation
When a [Worker](../../framework/workers.md) spawns, it does not get the full conversation history — it gets a compiled, scoped context. Who compiles it? What gets included? How is it compressed if it is too large? This is not a queue function — it is an orchestration function.

The numbers make this concrete: a generalist agent accumulates ~45,000 tokens of overhead after one month of daily use, producing a measurable 40% performance drop. A narrow, purpose-built worker with carefully scoped context stays at ~1,400 tokens. The context compiler's job is to ensure every spawned [Worker](../../framework/workers.md) gets the minimum viable context — no more, no less. Anthropic's research confirms that bad context passing is the single biggest cause of agent failure in multi-step pipelines.

### 3. Routing and planning
The [COO](../../agents/specialists/coo/coo.md) breaks a [CEO](../../agents/management/ceo/ceo.md) goal into tasks. But how does the [COO](../../agents/specialists/coo/coo.md) know which [Worker](../../framework/workers.md) handles which task type? How does it route a task that no existing Worker can handle? Static mapping (task type → Worker type) is fragile. The orchestrator needs a routing layer — either a registry of capabilities or a lightweight planning step.

### 4. Parallel execution
Some tasks depend on each other; some don't. A flat FIFO queue executes everything sequentially. A DAG (directed acyclic graph) maps dependencies and runs independent tasks simultaneously. If the [CMO](../../agents/specialists/cmo/cmo.md) needs market research *and* a competitor analysis before drafting a strategy, those two tasks should run in parallel. Without DAG execution, they run one after the other.

### 5. Error handling
Not all failures are the same:
- API rate limit → retry with backoff
- Model produces garbage output → reformulate and retry
- Missing input that requires human decision → pause and ask
- Tool unavailable → fallback or escalate
- Budget exceeded → hard stop, notify [CFO](../../agents/management/cfo/cfo.md)

A task queue with `status: failed` does not distinguish between these. The orchestration layer classifies errors and routes them to the correct response.

### 6. Human-in-the-loop
Some decisions should pause the workflow and wait for Board input — not because the agent is broken, but because the decision is above its authority threshold. The orchestrator needs to know where the pause points are, how to hold state across the pause (which may be hours or days), and how to resume cleanly.

### 7. Observability
Every agent invocation, tool call, handoff, retry, and result should be traceable. Not just for debugging — for auditing, cost accounting, and the [Compliance Watchdog](../../agents/workers/compliance-watchdog/compliance-watchdog.md). A task queue with a result field gives you the output. Tracing gives you the *path* that produced it.

---

## Architectural Patterns

### Supervisor / Worker (what the Office already has)
A central supervisor ([COO](../../agents/specialists/coo/coo.md)) coordinates specialized [workers](../../framework/workers.md). The supervisor decomposes, delegates, monitors, and synthesizes. Clear hierarchy, good traceability. The [Office](../../framework/office.md)'s current model.

**Limitation:** the supervisor is a bottleneck. Everything passes through the [COO](../../agents/specialists/coo/coo.md), including things the [COO](../../agents/specialists/coo/coo.md) doesn't need to see.

### DAG execution
Tasks are nodes; dependencies are directed edges. The orchestrator walks the DAG, spawning tasks as their dependencies resolve. Independent tasks run in parallel. Used by LangGraph, Apache Airflow, and most production workflow systems.

**For the [Office](../../framework/office.md):** the [CEO](../../agents/management/ceo/ceo.md) issues a goal. The [COO](../../agents/specialists/coo/coo.md) decomposes it into a DAG. Independent subtasks (market research, competitor analysis, cost estimate) run in parallel. Dependent subtasks (strategy draft, which needs all three inputs) wait for their dependencies.

### Event-driven orchestration
Agents emit events when they complete work. Other agents listen for events and trigger when their inputs are ready. No central orchestrator — the workflow emerges from event flows. O(n) connections (each agent connects to a broker) rather than O(n²) (each agent connects to each other).

**For the [Office](../../framework/office.md):** potentially powerful for the 24/7 operational layer. The [Signal Scout](../../agents/workers/signal-scout/signal-scout.md) emits a `high_signal_event`. The [CAO](../../agents/management/cao/cao.md) is listening and triggers. The [CAO](../../agents/management/cao/cao.md) emits `research_complete`. The [CMO](../../agents/specialists/cmo/cmo.md) is listening and triggers. No [COO](../../agents/specialists/coo/coo.md) needed in the loop for this chain.

### Blackboard architecture
A shared workspace (the blackboard) that all agents can read and write. Agents monitor the board and act when something in their domain appears. No central dispatcher — agents self-select based on what they see.

**Relevance:** the [Office](../../framework/office.md)'s [ChromaDB](data-storage.md) is already a partial blackboard. Formalizing it as a blackboard — where agents write structured entries and other agents react to them — is a natural evolution.

### Journal agent as shared memory

A practical alternative to a full blackboard: a dedicated **journal agent** whose only job is to log all activity to a shared structured store. All other narrow agents read the journal to understand system state, without needing direct coupling to each other.

The pattern:
1. Every agent, on completing a task, calls the journal agent with a structured log entry
2. The journal agent writes to a shared log (a file, a database, a Notion-style document)
3. Narrow agents that need cross-system context query the journal rather than holding that context themselves

This is how narrow agents share context without bloating their own history. The journal absorbs the accumulation; individual agents stay lean. In the [Office](../../framework/office.md), this role maps cleanly to the [Digital Archivist](../../agents/workers/digital-archivist/digital-archivist.md) — already responsible for institutional memory. Formalizing the [Digital Archivist](../../agents/workers/digital-archivist/digital-archivist.md) as the journal agent gives every other agent a single read/write interface to shared context, without direct coupling.

---

## Narrow Agents and the Skill Sweet Spot

The context rot numbers above make the case for narrow agents quantitatively. The operational case is equally strong.

### The sniper agent philosophy
A single-purpose agent with a tightly scoped context and a small, relevant toolset outperforms a generalist by **5–10x** on its target task. The generalist carries the overhead of everything it has ever done; the sniper carries only what it needs for the one thing it does.

Emmett Shear (former interim OpenAI CEO): *"Prompts are so late 2025. We are giving models intents now."* The shift from instructions to intents is the shift from telling an agent what to do to giving it a specific goal and letting it find the path. Narrow agents are the right shape for intent-driven operation: the goal is unambiguous, the tools are relevant, the context is clean.

### The 7–10 skill limit
The practical upper bound for tools per agent is **7–10**. Above this:
- The wrong skill gets selected at the wrong time
- The agent's context becomes clouded by tool schemas it rarely uses
- Personality and behavior become inconsistent ("personality jumble")

This is not a soft guideline — it is an observable performance cliff. When designing [Workers](../../framework/workers.md) for the [Office](../../framework/office.md), if the tool list exceeds 10 items, split the agent.

### Pass/fail evaluability
Narrow goals make agent performance **binary and therefore manageable**. Either the email draft is publishable or it is not. Either the research report answers the brief or it does not. This makes it easy to cut underperforming agents without qualitative judgment calls. A generalist's failures are always partially defensible ("well, it was juggling a lot") — a sniper's failures are not.

### Composability and remixability
A narrow agent with well-defined inputs and outputs can be duplicated and repurposed with minimal work. A YouTube content agent becomes a TikTok agent by swapping the output format and posting tool. This is not possible with a generalist whose behavior is entangled across dozens of tasks. The [Office](../../framework/office.md)'s [Worker](../../framework/workers.md) tier should be designed with composability in mind — Workers are stamped from templates, not hand-crafted one-offs.

### Predictable loops and true autonomy
A narrow agent running 3 cron tasks is more autonomous than a generalist, not less — because its behavior is entirely predictable. Predictability is the prerequisite for trust. You can put a predictable agent into production and leave it alone. A generalist with unpredictable behavior always needs supervision.

**For the [Office](../../framework/office.md):** the [Worker](../../framework/workers.md) tier is already narrow by design. This validates that instinct and extends it: Workers should be *opinionatedly* narrow — each with a defined trigger, a minimal skill set (≤10 tools), a specific intent, and an output that writes to a known destination.

---

## Build vs Use a Framework

### Use a framework when:
- Prototyping or validating a concept
- The framework covers 80%+ of your requirements
- Your team doesn't have the infrastructure capacity to maintain a custom layer
- Time to first working system matters more than long-term control

### Build your own when:
- You need fine-grained cost control (frameworks force one-model-per-agent patterns that are wasteful for lightweight [workers](../../framework/workers.md))
- You have strict safety requirements and need full auditability of every decision
- Your infrastructure (local models, custom hardware) conflicts with the framework's assumptions
- The framework's abstractions fight your architecture more than they help it
- You have unusual constraints — like context hygiene as a first-class architectural principle

**For the [Office](../../framework/office.md):** the case for building is strong. The [Office](../../framework/office.md) runs local models on custom hardware, has unusual context hygiene requirements, needs full data sovereignty, and has a pre-designed agent hierarchy that doesn't map cleanly onto any framework's opinionated abstractions. Frameworks built around cloud APIs, shared state, and conversational agents will fight the [Office](../../framework/office.md)'s architecture at every turn.

The risk of building: it is more work upfront, and the hard problems (state management, error classification, context compilation) take time to get right.

The case for a hybrid: use a framework for specific layers (Temporal for durability, an MCP client for tool access) while building the agent logic and orchestration logic yourself.

---

## A Concrete Approach for the Office

### The orchestration layer has five components:

**1. The Gateway (the [COO](../../agents/specialists/coo/coo.md) process)**
A persistent process — not an agent, a process — that is the single source of truth for the current workflow state. It owns the task DAG, not just a flat queue. It compiles context for [Workers](../../framework/workers.md) before spawning. It classifies errors. It knows which tasks are blocked, which are running, and which are done.

The [COO](../../agents/specialists/coo/coo.md) agent runs *inside* the gateway, using the gateway's state as its working memory. This distinction matters: the [COO](../../agents/specialists/coo/coo.md) agent reasons and plans; the gateway executes and persists.

**The [COO](../../agents/specialists/coo/coo.md)'s heartbeat loop:** the gateway fires a tick every N minutes. On each tick, it loads `heartbeat.md` — a file the [COO](../../agents/specialists/coo/coo.md) itself maintains — and passes it to the [COO](../../agents/specialists/coo/coo.md) agent as the current operational context. The [COO](../../agents/specialists/coo/coo.md) reads its own heartbeat, acts, and may update `heartbeat.md` with new priorities or deferred items. This gives the [COO](../../agents/specialists/coo/coo.md) a 24/7 operational rhythm without a human triggering it, and lets the [COO](../../agents/specialists/coo/coo.md) program its own future behavior by writing to the file it will read next.

**2. The task DAG**
Replace the flat task queue with a DAG. Each task entry has:
```json
{
  "id": "task_007",
  "type": "generate_strategy_brief",
  "assigned_to": "cmo",
  "status": "waiting",
  "depends_on": ["task_004", "task_005", "task_006"],
  "context_schema": "strategy_brief_input",
  "context": { ... },
  "spawned_by": "coo",
  "created_at": "2026-03-05T08:00:00Z",
  "result": null,
  "error": null,
  "retry_count": 0
}
```

The gateway walks the DAG, identifies tasks whose dependencies are resolved, and spawns [Workers](../../framework/workers.md) for them — in parallel where possible.

**3. Context compiler**
Before spawning any [Worker](../../framework/workers.md), the gateway runs a context compilation step:
- Reads the task's `context_schema` to know what shape of context the [Worker](../../framework/workers.md) expects
- Retrieves relevant records from [ChromaDB](data-storage.md) (via the [CAO](../../agents/management/cao/cao.md) or directly)
- Assembles a clean, minimal context block scoped to this task only
- Validates the compiled context against the schema before spawn

This is the component the [Office](../../framework/office.md) currently has no implementation for. It is the most important one. The target: every spawned [Worker](../../framework/workers.md) should receive a context comparable to the single-purpose agent floor — ~1,400 tokens of overhead, not 45,000.

**4. Error classifier**
When a task fails, the gateway classifies the error before deciding what to do:

| Error class | Response |
|---|---|
| `transient` (rate limit, timeout) | Retry with exponential backoff |
| `bad_output` (validation failure) | Reformulate context and retry (max 2) |
| `scope_exceeded` (task outside [Worker](../../framework/workers.md) capability) | Escalate to [Specialist](../../framework/specialists.md) |
| `authority_exceeded` (decision above tier threshold) | Pause, notify Board via [Executive Briefer](../../agents/workers/executive-briefer/executive-briefer.md) |
| `budget_exceeded` | Hard stop, notify [CFO](../../agents/management/cfo/cfo.md) |
| `fatal` (tool unavailable, model crash) | Mark failed, notify [COO](../../agents/specialists/coo/coo.md) |

**5. Trace log**
Every event written to an append-only trace log:
- Task created
- [Worker](../../framework/workers.md) spawned (with context hash — not full context)
- Tool called (name, inputs, outputs)
- Task completed (with result)
- Error classified and response taken
- Human approval requested / received

This log is what the [Compliance Watchdog](../../agents/workers/compliance-watchdog/compliance-watchdog.md) reads. It is also the basis for the [Executive Briefer](../../agents/workers/executive-briefer/executive-briefer.md)'s daily report.

---

## Candidate Stack

For a locally-hosted, data-sovereign [Office](../../framework/office.md):

| Component | Option A (minimal) | Option B (durable) |
|---|---|---|
| Task DAG store | SQLite + Python DAG walker | Temporal (durable, replay on crash) |
| Context compilation | Custom Python (`compile_context.py`) | Custom Python (same either way) |
| Agent communication | JSON typed messages, direct function call | MCP (JSON-RPC, interoperable) |
| Error handling | Python try/except with classifier | Temporal retry policies |
| Trace log | JSONL append-only file | OpenTelemetry → Langfuse local |
| Memory/archival | [ChromaDB](data-storage.md) (existing) | [ChromaDB](data-storage.md) (existing) |

**Option A** is the right starting point: a Python gateway process, a SQLite-backed DAG, a context compiler, and a JSONL trace log. This is buildable in weeks, fully local, fully auditable, and extends naturally to Option B when durability requirements grow.

**Option B** adds Temporal for durable execution (crash recovery, automatic retry) and OpenTelemetry for structured tracing. Overkill for a prototype; right for a 24/7 production swarm.

---

## Open Questions

- **Does the [COO](../../agents/specialists/coo/coo.md) agent run inside the gateway, or is it a separate agent that calls the gateway's API?** Keeping them separate is cleaner architecturally but adds a communication layer. Merging them is simpler but conflates reasoning with execution.
- **How is the task DAG visualized?** For the Board and for debugging, a visual DAG of in-progress work would be highly valuable. Does this belong to Mission Control (like OpenClaw's dashboard), or is the [Executive Briefer](../../agents/workers/executive-briefer/executive-briefer.md)'s report sufficient?
- **When does event-driven replace the [COO](../../agents/specialists/coo/coo.md)'s explicit dispatching?** The 24/7 operational layer ([Signal Scout](../../agents/workers/signal-scout/signal-scout.md) → [CAO](../../agents/management/cao/cao.md) → [CMO](../../agents/specialists/cmo/cmo.md) chain) could run entirely event-driven without [COO](../../agents/specialists/coo/coo.md) involvement. Defining the boundary between [COO](../../agents/specialists/coo/coo.md)-dispatched and event-triggered work is an early architectural decision.
- **Context compilation performance** — compiling context from [ChromaDB](data-storage.md) before every [Worker](../../framework/workers.md) spawn adds latency. Is this acceptable, or does the gateway need a context cache?
- **LangGraph as the DAG layer?** Rather than building a custom DAG walker, LangGraph could provide this layer while the [Office](../../framework/office.md) keeps its own agent definitions and context compilation. Worth evaluating before committing to fully custom.
- **Temporal overhead** — for a single-machine local deployment, is Temporal's durability worth its operational complexity? Or is a simpler crash-recovery strategy (checkpoint files, idempotent tasks) sufficient?
- **Heartbeat interval** — what is the right tick frequency for the [COO](../../agents/specialists/coo/coo.md)'s operational loop? Too frequent wastes compute; too infrequent makes the system feel unresponsive. Likely configurable per agent type.
- **Journal agent scope** — should the [Digital Archivist](../../agents/workers/digital-archivist/digital-archivist.md) act as the journal agent for all agents, or should each tier ([management](../../framework/management.md), [specialists](../../framework/specialists.md), [workers](../../framework/workers.md)) maintain its own journal? A single journal is simpler; tiered journals allow finer-grained access control.
