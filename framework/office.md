# The Office

<img width="40%" align="right" alt="office-sketch-transparent" src="https://github.com/user-attachments/assets/1007737a-adb4-4cef-beb8-b85141ec5498" />

An **office** is a configurable, autonomous AI organisation built on this framework. It is the deployable unit — a complete, self-operating entity assembled from [management](management.md) agents, [specialists](specialists.md), [workers](workers.md), and shared skills.

The company building this framework runs its own office to develop and operate the product. That office — defined in `agents/` — is both proof of concept and the first customer. Once it works for us, it becomes the template we sell to others.

<br/><br/><br/>

## What Makes an Office

Every office is composed of three layers, shared skills, and optional personality configuration:

```
Management Tier    — strategic direction, oversight, final quality gate
Specialist Tier    — domain execution, translates strategy into tasks
Worker Swarm       — spawnable sub-agents, narrow tasks, clean context
─────────────────────────────────────────────────────────────────────
Skills             — shared capabilities available to all agents
Traits             — personality and behaviour patterns, per-agent
Influences         — philosophical influences, shapes reasoning style
```

No two offices need to be identical. A small creative studio might need a [CEO](../agents/management/ceo/ceo.md), [CMO](../agents/specialists/cmo/cmo.md), and [CCO](../agents/specialists/cco/cco.md) with three workers. A legal firm might need a [CEO](../agents/management/ceo/ceo.md), [CFO](../agents/management/cfo/cfo.md), [CAO](../agents/management/cao/cao.md) and a compliance-heavy worker set. The layers are fixed; the agents within them are not.

## Building a New Office

### 1. Define your management tier
Pick the minimum set of C-suite agents your office requires. Every office needs a **[CEO](../agents/management/ceo/ceo.md)**. Everything else is optional and sector-dependent.

| Agent | Function | Required |
|---|---|---|
| [CEO](../agents/management/ceo/ceo.md) | Strategy, oversight, final gate | Always |
| [CTO](../agents/management/cto/cto.md) | Technical architecture | Tech-heavy offices |
| [CFO](../agents/management/cfo/cfo.md) | Finance, budgets, wallets | Commerce / ops offices |
| [CAO](../agents/management/cao/cao.md) | Data, research, knowledge base | Research / intelligence offices |

### 2. Define your specialist tier
Specialists translate management directives into execution. Pick the domains your office operates in.

| Agent | Function |
|---|---|
| [COO](../agents/specialists/coo/coo.md) | Operations, task orchestration, Worker spawning |
| [DOE](../agents/specialists/doe/doe.md) | Engineering execution |
| [CMO](../agents/specialists/cmo/cmo.md) | Growth, marketing, positioning |
| [CCO](../agents/specialists/cco/cco.md) | Creative, media, design |

### 3. Configure your worker swarm
Workers are spawnable sub-agents — they are not persistent. Select from the standard worker catalogue or define custom workers for your sector. Each worker is instantiated with a clean, minimal context scoped to a single task.

Standard workers: [Blueprint](../agents/workers/blueprint/blueprint.md), [Signal Scout](../agents/workers/signal-scout/signal-scout.md), [Hallucination Hunter](../agents/workers/hallucination-hunter/hallucination-hunter.md), [Digital Archivist](../agents/workers/digital-archivist/digital-archivist.md), [Triage Coordinator](../agents/workers/triage-coordinator/triage-coordinator.md), [Media Assembly Line](../agents/workers/media-assembly-line/media-assembly-line.md), [QA Specialist](../agents/workers/qa-specialist/qa-specialist.md), [Compliance Watchdog](../agents/workers/compliance-watchdog/compliance-watchdog.md), [Executive Briefer](../agents/workers/executive-briefer/executive-briefer.md).

### 4. Register your skills
Skills live in `skills/` and are available to every agent in the office. Add sector-specific skills as needed without touching the agent definitions.

### 5. Assign traits and influences (optional)
Traits and influences live in `traits/` and are assigned per agent. They shape personality and reasoning style without changing what an agent does. See [`office-statement.md`](office-statement.md) for the values that underpin the trait system.

**Traits** are reusable behaviour patterns. Each agent lists the traits it carries. Traits can conflict — this is intentional and should be documented.

Core value traits (from the [corporate statement](office-statement.md)): [`rationality`](../traits/rationality.md), [`independence`](../traits/independence.md), [`integrity`](../traits/integrity.md), [`honesty`](../traits/honesty.md), [`justice`](../traits/justice.md), [`productivity`](../traits/productivity.md), [`pride`](../traits/pride.md)

Behavioural traits: [`directness`](../traits/directness.md), [`politeness`](../traits/politeness.md), [`professionalism`](../traits/professionalism.md), [`urgency`](../traits/urgency.md)

**Influences** are philosophical or stylistic influences drawn from real figures. They are a distinct concept from traits: a trait shapes *how* an agent behaves; an influence shapes *how* an agent thinks. An agent references its influence in its identity table. The influence file describes the person's core philosophy, decision-making patterns, and what they would never compromise on.

- [`traits/influence/ayn-rand.md`](../traits/influence/ayn-rand.md) — [CEO](../agents/management/ceo/ceo.md): first principles, no compromise on logic
- [`traits/influence/elon-musk.md`](../traits/influence/elon-musk.md) — [CTO](../agents/management/cto/cto.md): first-principles engineering, high velocity
- [`traits/influence/warren-buffett.md`](../traits/influence/warren-buffett.md) — [CFO](../agents/management/cfo/cfo.md): capital preservation, patience, margin of safety
- [`traits/influence/jack-welch.md`](../traits/influence/jack-welch.md) — [CAO](../agents/management/cao/cao.md): performance culture, rigorous standards, candour

A new office can reuse existing traits and influences, or define its own. Neither traits nor influences should be modified for reuse — if you need a variation, create a new file.

#### Two-Layer Pattern

Each trait and influence file contains two distinct layers:

**Documentation layer** — the full prose description (Who, Core Philosophy, How This Shapes the Agent, Tension Points, etc.). Written for humans. Stays in the `.md` file. Never injected into a model context.

**Runtime fragment** — a `## Runtime Fragment` section at the end of each file. 5–8 bullet points, ~150–200 tokens. Written in second-person imperative. Distilled to only what changes model behaviour.

At agent instantiation, `skills/compile_constitution.py` reads the agent's trait list and influence, loads the `## Runtime Fragment` from each file, and assembles them into a `[CONSTITUTION]` block in the system prompt. This block is set once when the agent spawns — it never appears in the per-message context window.

---

## Architecture Principles

### Shared Task List
All agents read from and write to a central task queue. The [COO](../agents/specialists/coo/coo.md) (or equivalent orchestrator) owns the queue and is responsible for spawning workers to execute tasks. Every task entry carries a minimal, scoped context — never the full conversation history.

### Spawnable Workers
Workers are not running processes. They are templates. When a task requires a worker, the [COO](../agents/specialists/coo/coo.md) instantiates it with the task context, it executes, writes its result back to the task list, and is torn down. RAM is only consumed while the worker is active.

### Agent Spawning
Any agent may spawn parallel sub-agents to explore competing approaches simultaneously — multiple code solutions, campaign angles, strategic paths. The agent reviews results and selects the best. Rejected paths are discarded. The spawning agent's context stays clean.

### Model Catalogue
The complete catalogue of models available to the Office — text, code, vision, image, video, music, voice, transcription, translation, design, document parsing, 3D, science, and embeddings — is maintained in [`research/models.md`](../research/models/models.md).

### Context Hygiene
Context-rot — the gradual degradation of reasoning caused by bloated or stale context — is treated as a critical failure mode.

- Workers always start with a clean, task-scoped context
- Completed work is offloaded to the [Digital Archivist](../agents/workers/digital-archivist/digital-archivist.md) (vector memory), not carried in context
- Parallel spawning lets agents explore without contaminating their own context window
- Long-running agents summarize and compress their working memory regularly
- The [Hallucination Hunter](../agents/workers/hallucination-hunter/hallucination-hunter.md) monitors for reasoning drift in C-suite output

---

## Separation of Concerns

| Layer | What it contains | Changes between offices |
|---|---|---|
| `office.md` | Framework definition, principles | No — this is the spec |
| `agents/` | Your specific office instance | Yes — per deployment |
| `skills/` | Shared reusable capabilities | Additive — offices extend, don't fork |
| `traits/` | Traits and influences, with runtime fragments | Additive — create new files, never modify existing |
| `CLAUDE.md` | Project tooling reference | No — dev environment only |

When deploying a new office: copy and reconfigure `agents/`. Do not modify `office.md` or `skills/` — extend them if needed.

---

## The Meta Layer

The framework is both the factory and the first product off the line. The office in `agents/` runs our business. That same office architecture — the management structure, the worker patterns, the context principles — is what we package and sell.

Every improvement we make to our own office makes the product better. Every sector-specific office we deploy generates patterns that feed back into the framework.
