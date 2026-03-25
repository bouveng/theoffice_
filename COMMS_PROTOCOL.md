# The Office — Agent Communication Protocol
**Status:** v1.0 — Draft for CEO review
**Author:** CTO
**Date:** 2026-03-25
**Depends on:** `ARCHITECTURE.md`

---

## Principle

All inter-agent communication uses typed JSON contracts. No free-form messaging between agents in automated flows. Every message has a declared type, a sender, a recipient, and a traceable task ID. The contract is the source of truth — not the conversation history.

Three message types cover all cases:
1. **Delegation** — superior assigns work to subordinate
2. **Result** — subordinate returns outcome to caller
3. **Escalation** — any agent surfaces a blocker requiring a decision above its authority

---

## Chain of Authority

```
Board
  └── CEO
        ├── CTO → DOE → Workers (QA Specialist)
        ├── CFO
        ├── CAO → Workers (Digital Archivist, Signal Scout)
        └── COO → All Workers
```

Delegation flows **down**. Results flow **up**. Escalations skip tiers only when the immediate superior is the blocker.

---

## Message Type 1: Delegation

Used when a superior assigns a task to a subordinate.

### Schema
```json
{
  "msg_type": "delegation",
  "from": "<agent_id>",
  "to": "<agent_id>",
  "task_id": "<string>",
  "description": "<string>",
  "expected_output": "<string>",
  "deadline": "<ISO8601 or null>",
  "context": {
    "relevant_files": ["<path>"],
    "prior_decisions": ["<summary or task_id>"],
    "constraints": ["<constraint>"]
  },
  "authority_limit": "<string or null>",
  "created_at": "<ISO8601>"
}
```

### Field Definitions
| Field | Required | Description |
|---|---|---|
| `msg_type` | ✅ | Always `"delegation"` |
| `from` | ✅ | Sender agent ID (e.g. `"ceo"`, `"cto"`) |
| `to` | ✅ | Recipient agent ID |
| `task_id` | ✅ | Unique task identifier. Format: `<sender>-<YYYYMMDD>-<seq>` (e.g. `ceo-20260325-001`) |
| `description` | ✅ | What to do. Concrete, not abstract. |
| `expected_output` | ✅ | What done looks like. Specific enough to evaluate. |
| `deadline` | ✅ | ISO8601 datetime, or `null` if none |
| `context` | ✅ | Supporting material scoped to this task only |
| `authority_limit` | — | What the recipient may NOT decide unilaterally. Omit if no restriction. |
| `created_at` | ✅ | Timestamp of message creation |

### CEO → CTO Example
```json
{
  "msg_type": "delegation",
  "from": "ceo",
  "to": "cto",
  "task_id": "ceo-20260325-001",
  "description": "Draft the system architecture baseline document. Distill existing specs in /projects/Office/ into a working system diagram and agent contract format.",
  "expected_output": "ARCHITECTURE.md committed to /workspace/ with: system diagram, agent registry, orchestration layer, memory architecture, and current platform status.",
  "deadline": "2026-03-25T12:00:00Z",
  "context": {
    "relevant_files": [
      "projects/@theoffice_/docs/tech-summary.md",
      "projects/@theoffice_/framework/office.md",
      "projects/@theoffice_/research/architecture/orchestration.md"
    ],
    "prior_decisions": [],
    "constraints": ["Practical, not academic. Distill — do not reinvent."]
  },
  "authority_limit": null,
  "created_at": "2026-03-25T05:50:00Z"
}
```

---

## Message Type 2: Result

Used when a subordinate returns a completed outcome to the caller.

### Schema
```json
{
  "msg_type": "result",
  "from": "<agent_id>",
  "to": "<agent_id>",
  "task_id": "<string>",
  "status": "complete | partial | failed",
  "result": "<string or structured object>",
  "artifacts": ["<path or reference>"],
  "notes": "<string or null>",
  "created_at": "<ISO8601>"
}
```

### Field Definitions
| Field | Required | Description |
|---|---|---|
| `msg_type` | ✅ | Always `"result"` |
| `from` | ✅ | Agent returning the result |
| `to` | ✅ | Agent that issued the delegation |
| `task_id` | ✅ | Matches the originating delegation `task_id` |
| `status` | ✅ | `complete` = fully satisfies `expected_output`; `partial` = progress made, not done; `failed` = could not complete |
| `result` | ✅ | The output. String summary or structured object depending on task type. |
| `artifacts` | — | File paths, commit hashes, URLs produced. Omit if none. |
| `notes` | — | Deviations from spec, trade-offs made, recommended next steps. Omit if clean. |
| `created_at` | ✅ | Timestamp |

### CTO → CEO Example
```json
{
  "msg_type": "result",
  "from": "cto",
  "to": "ceo",
  "task_id": "ceo-20260325-001",
  "status": "complete",
  "result": "ARCHITECTURE.md authored and committed. Covers system diagram, agent registry (all tiers), orchestration layer with Task DAG schema and error classification, memory architecture, constitution system, model capability routing, and current platform status.",
  "artifacts": [
    "/home/ubuntu/.openclaw/workspace/ARCHITECTURE.md",
    "commit: 573a49c"
  ],
  "notes": "Comms protocol referenced as COMMS_PROTOCOL.md — pending as next deliverable.",
  "created_at": "2026-03-25T05:54:00Z"
}
```

---

## Message Type 3: Escalation

Used when an agent hits a blocker that requires a decision above its authority.

**Rule:** Escalation is not a status update and is not a question. It is a single, specific decision request. One escalation per blocker. State the blocker, state what decision is needed, and stop.

### Schema
```json
{
  "msg_type": "escalation",
  "from": "<agent_id>",
  "to": "<agent_id>",
  "task_id": "<string>",
  "blocker": "<string>",
  "decision_needed": "<string>",
  "options": [
    { "label": "<string>", "implication": "<string>" }
  ],
  "created_at": "<ISO8601>"
}
```

### Field Definitions
| Field | Required | Description |
|---|---|---|
| `msg_type` | ✅ | Always `"escalation"` |
| `from` | ✅ | Agent raising the blocker |
| `to` | ✅ | Agent with authority to resolve it |
| `task_id` | ✅ | Task that is blocked |
| `blocker` | ✅ | What is blocked and why. Factual, not emotional. |
| `decision_needed` | ✅ | Exactly what decision resolves the blocker. |
| `options` | — | Two to three concrete options with implications. Include when the path is not obvious. |
| `created_at` | ✅ | Timestamp |

### CTO → CEO Example
```json
{
  "msg_type": "escalation",
  "from": "cto",
  "to": "ceo",
  "task_id": "ceo-20260325-002",
  "blocker": "Context compiler (Task DAG component) requires direct ChromaDB write access. Current architecture routes all ChromaDB writes through the CAO. Bypassing the CAO would be faster but breaks the single-writer principle.",
  "decision_needed": "Does the COO gateway process get direct ChromaDB write access, or does all write traffic go through the CAO?",
  "options": [
    {
      "label": "Direct write (COO → ChromaDB)",
      "implication": "Lower latency, simpler implementation. Breaks CAO as sole write gateway — two agents with write access to the same store."
    },
    {
      "label": "CAO-gated write (COO → CAO → ChromaDB)",
      "implication": "Preserves single-writer principle. Adds one hop per worker completion. CAO becomes a bottleneck if task throughput is high."
    }
  ],
  "created_at": "2026-03-25T06:00:00Z"
}
```

---

## CTO → Specialist Chain

When the CTO delegates to the DOE, the same Delegation/Result/Escalation schema applies. The `from` and `to` fields change; the structure does not.

**CTO → DOE delegation example:**
```json
{
  "msg_type": "delegation",
  "from": "cto",
  "to": "doe",
  "task_id": "cto-20260325-001",
  "description": "Implement compile_context.py — the context compiler that runs before every worker spawn. Reads task context_schema, retrieves relevant ChromaDB records, assembles and validates a context block against the token budget.",
  "expected_output": "Working Python module at /workspace/src/compile_context.py. Unit tests passing. Token budget target: ≤1,400 tokens per compiled context block.",
  "deadline": "2026-04-01T00:00:00Z",
  "context": {
    "relevant_files": [
      "/home/ubuntu/.openclaw/workspace/ARCHITECTURE.md"
    ],
    "prior_decisions": ["Context discipline: 1,400 token target per worker spawn — ARCHITECTURE.md"],
    "constraints": [
      "Must validate compiled context against schema before spawn",
      "Must reject if over token budget — never silently truncate"
    ]
  },
  "authority_limit": "Do not modify ChromaDB schema without CTO sign-off.",
  "created_at": "2026-03-25T06:00:00Z"
}
```

**DOE escalation → CTO (not CEO):**
DOE escalations go to CTO. CTO resolves what it can; escalates to CEO only what is above CTO authority.

---

## Worker Contracts

Workers are spawned by the COO gateway process, not directly by agents. The delegation to a worker is not a message — it is a compiled context block (see `ARCHITECTURE.md` — Context Compilation). Workers return results by writing to the Task DAG, not by sending a message.

**Worker result write (Task DAG update):**
```json
{
  "task_id": "task_007",
  "status": "done",
  "result": "<structured output>",
  "artifacts": ["<path>"],
  "error": null,
  "completed_at": "<ISO8601>"
}
```

This is distinct from agent-to-agent messaging. Workers do not use `sessions_send`. They write to state.

---

## Task ID Convention

Format: `<sender_id>-<YYYYMMDD>-<seq>`

| Example | Meaning |
|---|---|
| `ceo-20260325-001` | First task issued by CEO on 2026-03-25 |
| `cto-20260325-001` | First task issued by CTO on same day |
| `coo-20260325-007` | Seventh COO-dispatched task |

Sequence resets daily. If a task spawns subtasks, subtasks inherit the parent ID as prefix: `ceo-20260325-001.1`, `ceo-20260325-001.2`.

---

## Routing Summary

| Scenario | Message type | From → To |
|---|---|---|
| Board issues directive | Delegation | Board → CEO |
| CEO assigns to CTO | Delegation | CEO → CTO |
| CEO assigns to COO | Delegation | CEO → COO |
| CTO assigns to DOE | Delegation | CTO → DOE |
| DOE hits blocker | Escalation | DOE → CTO |
| CTO hits blocker above authority | Escalation | CTO → CEO |
| CTO completes task | Result | CTO → CEO |
| DOE completes task | Result | DOE → CTO |
| COO spawns worker | Context block (DAG) | COO gateway → Worker |
| Worker completes task | DAG write | Worker → Task DAG |

---

## Protocol Constraints

1. **No free-form delegation.** If it is not a typed JSON contract, it is not a task.
2. **One escalation per blocker.** Do not stack questions. One decision request per message.
3. **Results match task_ids.** Every result must reference the task_id of its delegation. Orphan results are invalid.
4. **Workers don't message agents.** Workers write to the DAG. The COO gateway reads results and triggers the next step.
5. **Authority limits are binding.** If a delegation specifies an `authority_limit`, the recipient cannot exceed it without an escalation. No exceptions.
6. **All contracts are logged.** Every delegation, result, and escalation is written to the trace log (append-only JSONL) at send time.

---

*Depends on: `ARCHITECTURE.md`*
*Next: `memory/MEMORY_PROTOCOL.md` — memory write standards and decision persistence*
