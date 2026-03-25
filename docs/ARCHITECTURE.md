# The Office — System Architecture
**Status:** v1.0 — Draft for CEO review
**Author:** CTO
**Date:** 2026-03-25

---

## System Overview

The Office is a three-tier autonomous AI swarm running local-first on Apple Silicon. Agents do not talk directly to each other — they communicate via structured task contracts flowing through a central gateway process owned by the COO.

```
┌─────────────────────────────────────────────────────────────┐
│                     BOARD (Human oversight)                 │
│              Authority gate for decisions above             │
│              autonomous threshold                           │
└──────────────────────────┬──────────────────────────────────┘
                           │ directive / approval
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                   MANAGEMENT TIER                           │
│                                                             │
│  CEO (405B)     CTO (32B Coder)   CFO (70B)   CAO (60B)    │
│  Strategy       Architecture      Finance     Data/Research │
│  Final gate     Security          Cost        Vector DB     │
└──────┬──────────────────────────────────────────────────────┘
       │ task delegation (JSON contract)
       ▼
┌─────────────────────────────────────────────────────────────┐
│                   SPECIALIST TIER                           │
│                                                             │
│  COO (gateway process owner)   DOE   CMO   CCO             │
│  Orchestration / DAG           Eng   Mkt   Creative        │
└──────┬──────────────────────────────────────────────────────┘
       │ compiled task context (~1,400 tokens)
       ▼
┌─────────────────────────────────────────────────────────────┐
│                   WORKER SWARM                              │
│   (spawned per task, stateless, torn down on completion)    │
│                                                             │
│  Blueprint  Signal Scout  Hallucination Hunter              │
│  Digital Archivist  Triage Coordinator  QA Specialist       │
│  Media Assembly Line  Compliance Watchdog  Exec Briefer     │
└──────┬──────────────────────────────────────────────────────┘
       │ result write
       ▼
┌─────────────────────────────────────────────────────────────┐
│                   SHARED MEMORY                             │
│                                                             │
│  ChromaDB (vector)    JSONL (session)    memory/*.md        │
│  Task DAG (SQLite)    Trace log (JSONL)  heartbeat.md       │
└─────────────────────────────────────────────────────────────┘
```

---

## Hardware & Runtime

| Component | Spec |
|---|---|
| Hardware | Mac Studio M5 Ultra — 32-core CPU / 80-core GPU |
| Memory | 512GB Unified Memory |
| Storage | 4–8TB Internal SSD + 4–8TB External (OWC ThunderBlade) |
| Inference | Ollama / MLX / llama.cpp Metal backend |
| Runtime | Python |
| Communication | MCP (JSON-RPC), sessions_send (OpenClaw gateway) |
| Vector DB | ChromaDB + Nomic/MXBai embeddings |
| Task state | SQLite DAG |
| Tracing | JSONL append-only trace log → Langfuse (local) |

---

## Agent Registry

| Agent | Tier | Model | RAM | Primary Function |
|---|---|---|---|---|
| CEO | Management | Llama 3.1 405B / DeepSeek-R1 | ~230GB | Strategy, oversight, final gate |
| CTO | Management | Qwen2.5-Coder 32B / DeepSeek-V3 | ~20–40GB | Architecture, code, security |
| CFO | Management | Mistral Large 2 / Llama 3.1 70B | ~40GB | Cost, budget, wallet management |
| CAO | Management | Command R+ | ~60GB | Research, vector DB, data pipelines |
| COO | Specialist | 70B instruction-tuned | ~40GB | Orchestration, DAG ownership |
| DOE | Specialist | 70B instruction-tuned | ~40GB | Engineering execution |
| CMO | Specialist | 70B instruction-tuned | ~40GB | Growth, marketing |
| CCO | Specialist | 70B instruction-tuned | ~40GB | Creative, media |
| Workers (9 types) | Worker | 7B–14B | ~5–8GB each | Narrow single-task execution |

---

## Orchestration Layer

The COO process is the gateway — a persistent Python process that owns the task DAG and compiles context for workers before spawn. The COO *agent* runs inside it. The gateway executes and persists; the COO agent reasons and plans.

### Task DAG Schema
```json
{
  "id": "task_007",
  "type": "generate_strategy_brief",
  "assigned_to": "cmo",
  "status": "waiting | running | done | failed | blocked",
  "depends_on": ["task_004", "task_005"],
  "context_schema": "strategy_brief_input",
  "context": {},
  "spawned_by": "coo",
  "created_at": "ISO8601",
  "deadline": "ISO8601 or null",
  "result": null,
  "error": null,
  "retry_count": 0
}
```

### Error Classification
| Class | Response |
|---|---|
| `transient` (rate limit, timeout) | Retry with exponential backoff |
| `bad_output` (validation failure) | Reformulate context, retry max 2 |
| `scope_exceeded` (worker can't handle it) | Escalate to specialist |
| `authority_exceeded` (above agent's threshold) | Pause, notify Board via Exec Briefer |
| `budget_exceeded` | Hard stop, notify CFO |
| `fatal` (model crash, tool unavailable) | Mark failed, notify COO |

### Context Compilation (per worker spawn)
Target: **~1,400 tokens** per spawned worker. Steps:
1. Read task `context_schema`
2. Retrieve relevant records from ChromaDB (CAO gateway)
3. Assemble minimal scoped context block
4. Validate against schema — reject if over token budget
5. Spawn worker with compiled context only — no history

---

## Memory Architecture

| Store | Purpose | Owner | Retention |
|---|---|---|---|
| `memory/MEMORY.md` | Shared cross-agent decisions | All agents (write) | Indefinite |
| `memory/*.md` | Daily decision logs by date | All agents | Rolling |
| ChromaDB | Completed task outputs, embeddings | Digital Archivist / CAO | Indefinite |
| `heartbeat.md` (per agent) | COO operational state across ticks | COO | Current session |
| SQLite Task DAG | Live workflow state | COO gateway | Current workflow |
| JSONL Trace Log | Append-only audit trail | Gateway | Indefinite |
| JSONL Session files | Per-agent message history | Agent | Session |

**Context discipline rule:** Completed work leaves the context window immediately — written to Digital Archivist → embedded → ChromaDB. It is then retrievable by query, not carried in any agent's active context.

---

## Constitution System

Every agent carries a compiled `[CONSTITUTION]` block injected once at spawn into the system prompt. It never appears in the per-message context window.

**Assembly:** `compile_constitution.py` reads the agent's trait + influence list, pulls only the `## Runtime Fragment` from each file (~150–200 tokens each), and assembles the block.

**Cost per fully-specified management agent:**
| Component | Tokens |
|---|---|
| 7 trait runtime fragments | ~1,225 |
| 1 influence runtime fragment | ~200 |
| Role block | ~100 |
| **Total** | **~1,525 — fixed forever** |

A 500-turn session costs the same constitution overhead as a 1-turn session.

---

## Model Capability Routing

Agents request a **capability key**, not a specific model. The registry resolves it. Swapping to a better model = one line in the registry.

| Capability | Model class |
|---|---|
| `reasoning` / `planning` | 405B / frontier |
| `execution` / `synthesis` | 70B instruction-tuned |
| `writing` / `summarisation` | 14B (Phi-4) |
| `extraction` / `classification` | 7B (Mistral) |
| `code` | Qwen2.5-Coder 32B |
| `embeddings` | Nomic / MXBai (local) |

When a task phase changes capability tier, the active agent serializes full task state to a checkpoint and terminates. The gateway spawns a new instance under the target model with the checkpoint as its starting context.

**Checkpoint key fields:** `goal`, `phase_completed`, `phase_next`, `findings`, `context_summary`, `model_from`, `model_to`

---

## Data Flow: CEO → Worker → Memory

```
1. Board / CEO issues directive
2. CEO composes delegation task (JSON contract)
3. CEO → COO via sessions_send
4. COO decomposes into DAG subtasks
5. Gateway identifies unblocked tasks
6. Context compiler assembles ~1,400 token context per task
7. Gateway spawns Worker with compiled context
8. Worker executes, writes result to DAG
9. Digital Archivist receives completed output
10. Digital Archivist embeds + stores to ChromaDB
11. Gateway marks task done, walks DAG for next unblocked tasks
12. COO synthesizes final result → CEO
13. CEO delivers to Board
```

---

## Agent Communication Protocol
*(See: `COMMS_PROTOCOL.md` — authored separately, pending CEO review)*

Summary: all inter-agent communication uses typed JSON contracts. Three message types:
- **Delegation** (management → specialist): task assignment with full spec
- **Result** (specialist/worker → caller): structured outcome with status
- **Escalation** (any tier → superior): blocker requiring decision above authority

---

## Current Platform Status (Q1 2026)

| Component | Status |
|---|---|
| Agent definitions (all tiers) | ✅ Specced |
| Constitution compilation | ✅ `compile_constitution.py` exists |
| OpenClaw gateway / sessions_send | ✅ Live (current runtime) |
| ChromaDB / vector memory | 🔴 Not deployed |
| Task DAG (SQLite) | 🔴 Not built |
| Context compiler | 🔴 Not built |
| Trace log | 🔴 Not built |
| Hardware (Mac Studio M5 Ultra) | 🔴 Q2 2026 install |
| COO gateway process | 🔴 Q2 2026 |
| Full model stack (Ollama/MLX) | 🔴 Q2 2026 |

**Current operation:** OpenClaw gateway on Oracle Cloud ARM (arm64, 6GB RAM) running Claude Sonnet as proxy for all agents. All agent identity/protocol work is in effect; local model stack deploys Q2.

---

## Roadmap

| Quarter | Milestone |
|---|---|
| Q1 2026 | Architecture docs, comms protocol, memory discipline ← **now** |
| Q2 2026 | Hardware install, model stack, COO gateway process, Task DAG |
| Q2 2026 | POC — full office operating for internal needs |
| Q3 2026 | 24/7 autonomous operation, context compiler live |
| Q4 2026 | Client deployments |

---

*Source specs: `docs/tech-summary.md` · `research/architecture/orchestration.md` · `framework/office.md` · `framework/management.md`*
*Comms protocol: `COMMS_PROTOCOL.md` (next deliverable)*
