# Context Discipline

Context is a finite, depletable resource. Every token that enters the context window displaces something else — or inflates the window until reasoning degrades. Context discipline is the practice of treating that resource with the same rigor as RAM or compute: measure what you spend, spend only what you must, and offload everything that does not need to be there.

The Office treats context rot — the gradual degradation of reasoning caused by bloated or stale context — as a critical failure mode, not an inconvenience.

---

## Why This Is the Condition for 24/7 Autonomous Operation

An agent running once is easy. An agent running continuously for 30 days, unsupervised, across thousands of tasks, is a different problem. Without context discipline, autonomous operation is not a feature — it is a slow failure mode. The agent degrades silently: reasoning becomes shallower, outputs become less precise, failures become more frequent, and no alarm sounds. The system appears to be working until it isn't.

Context discipline is what separates a system that can run for a day from one that can run for a year.

The Office is designed for the latter. Every architectural decision — how traits are compiled, how workers spawn, how completed work leaves context, how long-running agents compress their history — is made with continuous autonomous operation as the requirement, not an afterthought.

**The lean system prompt.** Traits and influences are compiled into a `[CONSTITUTION]` block of ~150–200 tokens per trait. A fully specified CEO with five traits and one influence carries ~1,500 tokens of behavioral instruction — fixed, set once at spawn, never repeated in the message thread. This is the agent's permanent character. It does not grow. Day 1 and Day 30 have the same system prompt overhead. The agent does not accumulate personality drift from its own prior outputs.

**Spawn-fresh workers.** Workers do not persist between tasks. Each spawn gets a clean context scoped to exactly one task. There is no history to corrupt, no prior task bleeding into the current one, no accumulated confusion. A worker on its ten-thousandth spawn is as sharp as on its first.

**Offload, don't carry.** Completed work exits the context window immediately — into ChromaDB via the Digital Archivist, where it is retrievable by query but absent from the working context. Agents stay lean. The institutional memory grows without individual agents degrading.

**Heartbeat compression for persistent agents.** The COO and CEO, which must maintain longer operational awareness, compress their working context on a regular cycle. The COO writes its own `heartbeat.md` — a curated state summary it will read on the next tick rather than its full session history. This is the mechanism that lets a management agent run 24/7 without accumulating weeks of conversational history into its context window.

The result: a swarm that performs on day 300 the same way it performs on day 1. That is not an aspirational property — it is an architectural guarantee, provided the discipline holds.

---

---

## The Cost of Context Rot — Hard Numbers

From the [orchestration research](orchestration.md), based on OpenClaw's measured behavior in production:

| Agent type | Context overhead after one month of daily use |
|---|---|
| Generalist agent (multi-purpose) | ~45,000 tokens |
| Single-purpose agent (narrow scope) | ~1,400 tokens |

A generalist agent running daily for one month accumulates roughly a **40% drop in task performance** — not because the model changes, but because its context fills with accumulated history, stale tool schemas, and irrelevant prior exchanges. The model is still capable; it is just spending most of its attention budget on noise.

This is the quantitative case for everything that follows.

---

## How Context Degrades

Context rot is not a single failure — it is several overlapping ones:

**Accumulated history.** A persistent agent that carries its full session history eventually spends the majority of its attention on old exchanges rather than the current task. The older the history, the less relevant it is and the more it crowds out what matters.

**Tool schema bloat.** Every tool schema injected into context costs tokens. An agent with 40 tools in context is spending a meaningful fraction of its window on schemas it will not use in a given task. The wrong tool also gets selected at the wrong time — not because the model is wrong, but because attention is split across too many options.

**Stale findings.** Completed work left in the active context window is dead weight. It was produced, it is done, it should not be in the prompt for the next task. Agents that carry their own output history inevitably start referring back to it inappropriately.

**Rejected paths.** An agent that explores multiple approaches and then keeps the rejected ones in context will have its reasoning anchored to those dead ends. The winning path is diluted by everything that lost.

**Personality jumble.** A poorly structured system prompt that inlines full documentation, reasoning traces, and behavioral guidance as flat text produces inconsistent behavior. The model cannot reliably distinguish what is instruction, what is example, and what is context.

---

## The Office's Approach

### Workers start clean

Every [Worker](../../framework/workers.md) is spawned with a minimal, task-scoped context — nothing more. No full conversation history, no prior task results, no cross-agent awareness. The [COO](../../agents/specialists/coo/coo.md) is explicitly required to compile a scoped context block before spawning; the constraint is structural, not aspirational.

The target, derived from the context rot data: **~1,400 tokens of overhead per spawned worker**. Every token above that is waste to be eliminated.

### Completed work leaves context

When a Worker finishes, its output does not stay in any agent's context window. It is written to the task queue (structured result), picked up by the [Digital Archivist](../../agents/workers/digital-archivist/digital-archivist.md), summarized, embedded, and stored to [ChromaDB](data-storage.md). From that point, it is retrievable by query — not by prompt injection.

This is the key distinction: **history accumulates in a searchable store, not in prompts.** Any agent that needs past work queries the library. It receives only the relevant fragment, scoped to the current need, not the entire prior record.

### Parallel spawning isolates exploration

When any agent needs to explore competing approaches — multiple code architectures, campaign angles, strategic paths — it spawns parallel sub-agents rather than exploring sequentially in its own context. Each sub-agent works in isolation. Results are returned; the spawning agent compares outputs and selects the best. Rejected paths are discarded before they ever enter the primary context window.

This is explicitly documented across the management and specialist tier agents:

> "The CEO's own context remains clean throughout."
> "The CTO reviews outputs and selects the best without contaminating its own working context."
> "The CMO evaluates and selects the strongest without carrying all drafts in its own context."

The pattern is consistent and intentional: exploration is parallelized precisely to protect the primary agent's context from the waste of paths not taken.

### Long-running agents compress

Management-tier agents that run extended sessions — particularly the CEO and COO — are expected to summarize and compress their working memory periodically rather than appending indefinitely. The COO's heartbeat loop is the mechanism for this: on each tick, it reads a managed `heartbeat.md` file rather than its full session history. The file is a curated, compressed state — written by the COO itself on the previous tick. This gives the COO a 24/7 operational rhythm without carrying an ever-growing conversation history.

### The Digital Archivist as shared memory

Narrow agents need context from outside their immediate task without holding that context themselves. The solution is not direct coupling between agents — it is a shared journal.

The [Digital Archivist](../../agents/workers/digital-archivist/digital-archivist.md) is that journal. It receives every task output, summarizes, embeds, and stores it. Any agent that needs cross-session or cross-agent context queries ChromaDB through the [CAO](../../agents/management/cao/cao.md) or directly. They receive a targeted retrieval result — not another agent's full history — and proceed with minimal overhead.

This is how the swarm shares knowledge without coupling agents to each other's context windows.

---

## System Prompt vs Runtime — Why Traits Are Not a Context Tax

A common assumption is that a richly specified agent — one carrying a full value set, behavioral guidelines, and an influence profile — pays a large token cost on every interaction. In the Office, this assumption is wrong. The architecture separates what goes into the **system prompt** from what enters the **per-message context window**, and it separates **documentation** from **runtime instruction**.

### The two layers of every trait and influence

Each [trait](../../traits/) and [influence](../../traits/influence/) file contains two distinct layers:

**Documentation layer.** The full prose — who this trait is, why it exists, how it shapes behavior, where it conflicts, where it is compatible. This layer is written for humans. It lives in the `.md` file. It never enters a model context window. Ever.

**Runtime fragment.** A `## Runtime Fragment` section at the end of each file. Five to eight bullet points, second-person imperative, ~150–200 tokens. Distilled to only what demonstrably changes model behavior. This is the only part that ever enters the model.

### Compilation — once, at spawn

At agent instantiation, `skills/compile_constitution.py` reads the agent's assigned trait and influence list, loads only the `## Runtime Fragment` from each file, and assembles them into a single `[CONSTITUTION]` block. That block is prepended with a `[ROLE]` block and injected as the system prompt.

This happens **once, at spawn time.** The system prompt is set and does not change.

The per-message context window — the messages array that grows with each exchange — never contains the constitution. It is in the system prompt, which the model sees but which is architecturally separate from the conversation history that accumulates token cost over time.

### The actual cost

An agent with seven core value traits and one influence:

| Component | Tokens |
|---|---|
| 7 trait runtime fragments (~175 tokens each) | ~1,225 |
| 1 influence runtime fragment (~200 tokens) | ~200 |
| Role block | ~100 |
| **Total constitution cost** | **~1,525 tokens** |

This is a fixed, one-time cost set at spawn. It does not grow. It does not compound. A 500-turn session with seven traits costs the same in constitution overhead as a 1-turn session.

The documentation layer — which for a rich trait file might run to 600–800 tokens of prose — is never loaded into any model. It costs zero at runtime.

### Why this matters for specialisation

Because trait cost is bounded and fixed, adding traits to an agent is not the same risk as adding to the messages history. Composing a CEO with seven value traits, one influence, and two capability traits (say, [`agnostic`](../../traits/agnostic.md)) adds ~1,700 tokens to the system prompt. That is the full cost. The CEO can operate for months without that cost increasing.

The per-message window — where context rot actually happens — is governed by a separate set of rules: task scoping, work offloading, compression, and spawn-fresh workers for heavy execution.

---

## The Context Compiler — The Critical Missing Piece

The system currently has the principles and the target (~1,400 tokens per spawned worker). What it does not yet have is the implementation: a context compiler.

Before spawning any Worker, the gateway (COO process) should run a compilation step:

1. Retrieves relevant records from ChromaDB scoped to the current task
2. Assembles a minimal context block: task goal, relevant prior findings, required tool schemas only
3. Validates the compiled context against the task's JSON schema before spawn
4. Rejects and recompiles if it exceeds the token budget

This is the component the Office does not yet have. It is also the most important one. The heartbeat loop, the parallel spawning, the Digital Archivist — all of these are hygiene. The context compiler is enforcement. Without it, context discipline is aspirational. With it, the 1,400-token floor is a hard constraint the system guarantees on every spawn.

See [orchestration.md](orchestration.md) for the full implementation design.

---

## Model Switching and Context Serialization

The [`agnostic`](../../traits/agnostic.md) trait introduces a specific context discipline problem: when an agent switches models mid-task, its KV cache is lost. The model is unloaded from unified memory; all internal working state evaporates. Whatever the agent knew must be reconstructed from external state alone.

The solution is the checkpoint. Before switching, the agent writes a `checkpoint.json` containing a `context_summary` field — a self-contained, compressed prose summary of all accumulated reasoning, findings, and decisions. This field is designed to be read cold by a new instance with no prior session history. Everything needed for continuity must be in it; nothing outside it can be assumed.

This is context discipline applied to the model handoff boundary: treat every model switch as a spawn of a fresh agent, and compile its context accordingly.

---

## Summary — The Rules

| Rule | Mechanism |
|---|---|
| Workers start with minimal, scoped context | COO context compiler (~1,400 token target) |
| Completed work leaves context immediately | Digital Archivist → ChromaDB |
| Exploration does not contaminate primary context | Parallel sub-agent spawning |
| Long-running agents do not grow unbounded | Heartbeat compression loop |
| Traits are fixed overhead, not accumulating cost | System prompt compilation, runtime fragment only |
| Documentation never enters context | Two-layer trait architecture |
| Model switching preserves continuity without KV cache | Checkpoint serialization (agnostic trait) |
| Shared knowledge is retrieved, not injected wholesale | ChromaDB query on demand |

Context discipline is not a constraint imposed on the agents — it is the condition under which agents remain capable. An agent with a bloated context is not a more informed agent. It is a degraded one.
