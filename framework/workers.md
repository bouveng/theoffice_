# Worker Swarm

> 9 lightweight, specialized agents. Spawned on demand, torn down on completion. Narrow scope, minimal context, low RAM footprint.

---

## Overview

Workers are the operational backbone of the office. Each agent has a single, well-defined task. They are spawned by the [COO](../agents/specialists/coo/coo.md) (or any [Specialist](specialists.md)/[Management](management.md) agent) when a task requires them, execute with a clean and minimal context scoped only to that task, then are torn down. They do not persist between tasks.

This design is intentional: spawning fresh workers prevents context-rot, conserves RAM, and keeps each execution predictable and auditable. Workers operate under the values and rules of engagement defined in the [corporate statement](office-statement.md).

---

## The 9 Workers

### The Blueprint — Planning & Coordination
→ [Full agent profile](../agents/workers/blueprint/blueprint.md)
- **Model**: DeepSeek-R1 (distilled, 14B)
- **Task**: Spawned at the start of any initiative involving three or more agents. Produces a **Master Plan** — a shared, structured document that assigns tasks, declares dependencies, and gives every involved agent a consistent shared context to work from. Torn down once the plan is distributed to the [COO](../agents/specialists/coo/coo.md).

### The Signal Scout — Data Mining & Monitoring
→ [Full agent profile](../agents/workers/signal-scout/signal-scout.md)
- **Model**: Llama 3.1 8B
- **Task**: Scans 1,000+ RSS/social feeds per hour. Filters noise, escalates only high-signal events to the [CAO](../agents/management/cao/cao.md).

### The Hallucination Hunter — Fact-Checking & Verification
→ [Full agent profile](../agents/workers/hallucination-hunter/hallucination-hunter.md)
- **Model**: Phi-4 (14B)
- **Task**: Cross-references C-suite drafts against the local [ChromaDB](../research/architecture/data-storage.md). Flags logical contradictions and unsourced claims.

### The Digital Archivist — Memory Management
→ [Full agent profile](../agents/workers/digital-archivist/digital-archivist.md)
- **Model**: Mistral 7B v0.3
- **Task**: Summarizes every internal agent interaction. Converts logs into embeddings to maintain the organization's long-term memory.

### The Triage Coordinator — Email & Communication
→ [Full agent profile](../agents/workers/triage-coordinator/triage-coordinator.md)
- **Model**: Llama 3.1 8B
- **Task**: Monitors inbound emails and chat. Categorizes by urgency, drafts routine replies for [CFO](../agents/management/cfo/cfo.md)/[CCO](../agents/specialists/cco/cco.md) approval.

### The Media Assembly Line — Asset Preparation
→ [Full agent profile](../agents/workers/media-assembly-line/media-assembly-line.md)
- **Model**: Flux.1 [Schnell]
- **Task**: Generates image, video, layout, and design variations from [CCO](../agents/specialists/cco/cco.md) creative briefs. Outputs a curated gallery for final selection.

### The QA Specialist — Testing & Sandboxing
→ [Full agent profile](../agents/workers/qa-specialist/qa-specialist.md)
- **Model**: Qwen2.5-Coder 7B
- **Task**: Executes code from the [CTO](../agents/management/cto/cto.md) in isolated Docker sandboxes. Reports Pass/Fail logs before any deployment.

### The Compliance Watchdog — Security & Audit
→ [Full agent profile](../agents/workers/compliance-watchdog/compliance-watchdog.md)
- **Model**: Granite-3.0-8B
- **Task**: Scans system logs 24/7 for unauthorized API calls or CPU spikes. Issues a kill-switch alert if the system constitution is breached.

### The Executive Briefer — Reporting & Documentation
→ [Full agent profile](../agents/workers/executive-briefer/executive-briefer.md)
- **Model**: Phi-4 (14B)
- **Task**: Compiles a concise daily brief for the Board of Humans. Synthesizes KPIs from [CFO](../agents/management/cfo/cfo.md) and [CAO](../agents/management/cao/cao.md) into an 08:00 AM update.

---

## Summary Table

| Worker | Model | Domain |
|---|---|---|
| [Blueprint](../agents/workers/blueprint/blueprint.md) | DeepSeek-R1 14B | Planning |
| [Signal Scout](../agents/workers/signal-scout/signal-scout.md) | Llama 3.1 8B | Monitoring |
| [Hallucination Hunter](../agents/workers/hallucination-hunter/hallucination-hunter.md) | Phi-4 14B | Fact-checking |
| [Digital Archivist](../agents/workers/digital-archivist/digital-archivist.md) | Mistral 7B v0.3 | Memory |
| [Triage Coordinator](../agents/workers/triage-coordinator/triage-coordinator.md) | Llama 3.1 8B | Communications |
| [Media Assembly Line](../agents/workers/media-assembly-line/media-assembly-line.md) | Flux.1 [Schnell] | Visual assets |
| [QA Specialist](../agents/workers/qa-specialist/qa-specialist.md) | Qwen2.5-Coder 7B | Testing |
| [Compliance Watchdog](../agents/workers/compliance-watchdog/compliance-watchdog.md) | Granite-3.0-8B | Security |
| [Executive Briefer](../agents/workers/executive-briefer/executive-briefer.md) | Phi-4 14B | Reporting |

---

## Design Principles

- Narrow scope — one task per worker, done well
- Lightweight models — preserve RAM for [Management](management.md) tier
- Spawnable, not persistent — instantiated on demand, torn down after completion
- Clean context on every spawn — no carry-over from previous executions
- Escalation only — surface signal, not noise, to [Specialists](specialists.md)
