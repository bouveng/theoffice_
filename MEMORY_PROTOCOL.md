# The Office — Memory Protocol
**Status:** v1.0 — Draft for CEO review
**Author:** CTO
**Date:** 2026-03-25
**Depends on:** `ARCHITECTURE.md`, `COMMS_PROTOCOL.md`

---

## Principle

Memory is not a side effect of operation — it is a first-class system component. Every significant decision, architectural choice, and task outcome is written to a defined store, by a defined agent, at a defined time. Unwritten decisions do not exist as far as the swarm is concerned.

Two failure modes this protocol prevents:
1. **Context rot** — agents carrying history they should have offloaded
2. **Institutional amnesia** — decisions made and lost, repeated work, drift between sessions

---

## Memory Stores Overview

| Store | Scope | Owner | Format | Retention |
|---|---|---|---|---|
| `MEMORY.md` | Cross-agent, cross-session | All agents (write) | Markdown — rolling bullet index | Indefinite |
| `memory/YYYY-MM-DD.md` | Daily decision log | All agents (write) | Markdown — structured entries | 90 days, then archive |
| ChromaDB | Institutional knowledge base | Digital Archivist (write), CAO (manage) | Embeddings | Indefinite |
| `heartbeat.md` (per agent) | Operational state for persistent agents | COO / CEO (self-write) | Markdown — compressed state | Current cycle only |
| Task DAG (SQLite) | Live workflow state | COO gateway | JSON rows | Current workflow; archive on completion |
| Trace log (`trace.jsonl`) | Append-only audit trail | Gateway process | JSONL | Indefinite |
| Agent session JSONL | Per-agent message history | Agent runtime | JSONL | Session duration only |

---

## Store 1: `MEMORY.md` — Shared Decision Index

**Location:** `/home/ubuntu/.openclaw/workspace/MEMORY.md`

**Purpose:** A rolling index of significant cross-agent decisions, resolved architectural questions, and standing policy. Any agent that needs to recall "what did we decide about X" checks here first.

**What belongs here:**
- Architectural decisions with lasting effect (e.g. "CAO is sole ChromaDB write gateway")
- Policy decisions that constrain future agent behavior
- Standing directives from the Board or CEO that apply across sessions
- Links to daily memory files where full rationale is documented

**What does NOT belong here:**
- Task results or summaries (→ ChromaDB)
- Operational state (→ `heartbeat.md`)
- Full decision rationale (→ `memory/YYYY-MM-DD.md`)

**Write standard:**
```markdown
## YYYY-MM-DD — <Decision Title>
- **Decision:** <one sentence — what was decided>
- **Rationale:** <one sentence — why>
- **Owner:** <agent that owns enforcement>
- **Ref:** memory/YYYY-MM-DD.md#<anchor> | task_id: <id>
```

**Example:**
```markdown
## 2026-03-25 — CAO is sole ChromaDB write gateway
- **Decision:** All ChromaDB writes route through the CAO. COO gateway does not write directly.
- **Rationale:** Single-writer principle — preserves auditability and prevents concurrent write conflicts.
- **Owner:** CTO
- **Ref:** memory/2026-03-25.md#chromadb-write-access | task_id: ceo-20260325-001
```

**Write trigger:** Any agent that makes or receives a decision with cross-session or cross-agent impact writes an entry within the same session it is made.

**Who writes:** Any management or specialist agent. Workers do not write to `MEMORY.md` — they write results to the Task DAG, which the COO or CTO promotes to shared memory if decision-worthy.

---

## Store 2: `memory/YYYY-MM-DD.md` — Daily Decision Log

**Location:** `/home/ubuntu/.openclaw/workspace/memory/YYYY-MM-DD.md`

**Purpose:** Full record of decisions, rationale, options considered, and context for a given day. The index entry in `MEMORY.md` points here. This is where reviewers and future agents go for the full picture.

**File naming:** `YYYY-MM-DD.md` in UTC. One file per day. Create on first write of the day; append for subsequent entries.

**Entry format:**
```markdown
## <anchor> — <Decision Title>
**Time:** HH:MM UTC
**Agent:** <agent_id>
**Task ref:** <task_id or null>

### Decision
<What was decided. One to three sentences.>

### Context
<What problem this solves or what question it resolves.>

### Options considered
- **Option A:** <description> — rejected because <reason>
- **Option B:** <description> — rejected because <reason>
- **Chosen:** <description> — because <reason>

### Constraints
<Any limits or conditions that apply to this decision going forward.>

### Next action
<What happens next as a result of this decision, if anything.>
```

**Minimum viable entry** (for low-stakes decisions):
```markdown
## <anchor> — <Decision Title>
**Time:** HH:MM UTC | **Agent:** <agent_id> | **Task ref:** <task_id>

<Decision in one to two sentences. Rationale in one sentence.>
```

**Write trigger:** Any decision that changes how agents behave, what they build, or how resources are allocated. When in doubt, write it.

**Retention:** 90 days active. After 90 days, the Digital Archivist compresses and archives to ChromaDB (`content_type: "decision"`). The daily file is then deleted from `memory/`. The `MEMORY.md` index entry remains.

---

## Store 3: ChromaDB — Institutional Knowledge Base

**Location:** Local ChromaDB instance (path: `/data/chromadb/` — Q2 deployment)

**Purpose:** Long-term semantic search over completed task outputs, research, decisions, and drafts. The swarm's institutional memory. Retrievable by query, never injected wholesale.

**Content types:**

| Type | Description | Written by |
|---|---|---|
| `task_output` | Completed worker results | Digital Archivist (auto, post-task) |
| `research` | Ingested documents, external sources | Digital Archivist (explicit, via CAO) |
| `decision` | Archived daily memory entries | Digital Archivist (90-day compression) |
| `draft` | Content pending verification or delivery | Digital Archivist (explicit) |

**Write access:** Digital Archivist only — write-only, no read.
**Read access:** CAO (read + manage), Hallucination Hunter (read-only).
**Query gateway for agents:** CAO. Management and specialist agents request retrieval through the CAO. Workers with task-scoped retrieval needs may query directly via a restricted interface.

**Write standard (Digital Archivist input):**
```json
{
  "content": "<raw output or document>",
  "source": "<agent_id>",
  "content_type": "task_output | research | decision | draft",
  "tags": ["<tag>"],
  "task_id": "<task_id or null>",
  "created_at": "<ISO8601>"
}
```

**Trigger:** COO marks task done → spawns Digital Archivist with task result as input. This is automatic and mandatory for every completed task. No exceptions.

---

## Store 4: `heartbeat.md` — Operational State (Persistent Agents)

**Location:** Per-agent, in agent workspace (e.g. `/home/ubuntu/.openclaw/workspace-coo/heartbeat.md`)

**Purpose:** Compressed operational state for persistent agents (COO, CEO). The agent writes its own heartbeat — a curated summary of current priorities, in-progress tasks, and deferred items — at the end of each cycle. It reads this file at the start of the next cycle instead of its full session history.

**Who uses it:** COO (primary), CEO (when running extended sessions).

**Write standard:**
```markdown
# Heartbeat — YYYY-MM-DD HH:MM UTC

## Active tasks
- <task_id>: <one-line status>

## Waiting on
- <task_id>: <what is needed, from whom>

## Deferred
- <item>: <why deferred, target date if any>

## Alerts
- <anything that needs human attention or CEO escalation>

## Next tick priority
<What the COO should focus on when it next wakes. One to three items.>
```

**Retention:** Current cycle only. Overwritten on each write. Not archived — operational state has no long-term value after the fact. If a decision surfaces during a heartbeat cycle that has cross-session value, write it to `memory/YYYY-MM-DD.md` separately.

---

## Store 5: Trace Log (`trace.jsonl`)

**Location:** `/home/ubuntu/.openclaw/workspace/runtime/trace.jsonl`

**Purpose:** Append-only audit trail. Every delegation issued, worker spawned, tool called, task completed, error classified, and escalation raised is written here at the moment it occurs.

**Managed by:** Gateway process (COO). Agents do not write to the trace log directly — the gateway writes on their behalf.

**Entry schema:**
```json
{
  "ts": "<ISO8601>",
  "event": "delegation | result | escalation | worker_spawn | tool_call | task_done | task_failed | error_classified",
  "from": "<agent_id or system>",
  "to": "<agent_id or null>",
  "task_id": "<task_id or null>",
  "detail": "<event-specific payload — task_id, tool name, error class, etc.>",
  "context_hash": "<sha256 of compiled context, for worker_spawn events>"
}
```

**Retention:** Indefinite. Never delete. The Compliance Watchdog reads the trace log. The Executive Briefer uses it for daily reports.

---

## Write Rules — All Stores

1. **Write immediately.** Memory entries are written in the same session the decision is made. Not "later". Not "when the task is done". Now.

2. **Minimum viable entry over no entry.** A two-line minimum viable entry is better than silence. If time is short, write the decision and rationale; full options analysis can be omitted.

3. **Workers don't write to shared memory.** Workers write to the Task DAG. The COO or calling agent promotes to `MEMORY.md` / `memory/` if the output warrants it.

4. **One decision, one entry.** Do not batch multiple decisions into a single entry. Each stands alone, with its own anchor, rationale, and task ref.

5. **Cross-reference everything.** Every `MEMORY.md` entry references its daily file. Every daily file entry references its `task_id`. The trace log provides the full audit chain.

6. **Don't duplicate across stores.** `MEMORY.md` carries the index. The daily file carries the detail. ChromaDB carries the long-term archive. Nothing lives in more than one active store at the same time.

---

## Decision Taxonomy — What Gets Written Where

| Decision type | MEMORY.md | Daily file | ChromaDB |
|---|---|---|---|
| Architectural decision (lasting effect) | ✅ Index entry | ✅ Full entry | After 90 days |
| Policy / standing directive | ✅ Index entry | ✅ Full entry | After 90 days |
| Task outcome (task_output) | ❌ | ❌ | ✅ Immediately |
| Research / ingested document | ❌ | ❌ | ✅ Immediately |
| Escalation resolved | ✅ If policy-level | ✅ Full entry | After 90 days |
| Operational state (heartbeat) | ❌ | ❌ | ❌ |
| Failed task / error | ❌ | Only if decision resulted | ✅ trace.jsonl |

---

## Memory Retrieval — How Agents Read

**Before starting any task with cross-session context:** run `memory_search` against `MEMORY.md` and `memory/*.md`. This is mandatory, not optional. If a prior decision is relevant, it governs.

**Retrieval order:**
1. `memory_search` — semantic search across MEMORY.md + daily files
2. `memory_get` — pull specific lines once located
3. CAO ChromaDB query — for deeper institutional context (task outputs, research)

**Rule:** Never assume. If a decision might exist, search first. Duplicating work or contradicting a prior decision because you didn't check is a protocol violation.

---

## Bootstrap: Initial Memory State

As of 2026-03-25, no memory files exist. The first entries to be written are the decisions made during this architecture session:

1. Architecture baseline established (`ARCHITECTURE.md`)
2. Comms protocol established (`COMMS_PROTOCOL.md`)
3. Memory protocol established (this document)
4. CAO as sole ChromaDB write gateway — standing architectural decision

These will be written to `memory/2026-03-25.md` and indexed in `MEMORY.md` immediately after this protocol is approved.

---

*Depends on: `ARCHITECTURE.md`, `COMMS_PROTOCOL.md`*
*Next: Security audit baseline + Identity configuration (parallel tracks)*
