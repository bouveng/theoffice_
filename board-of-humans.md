# Board of Humans

The Board holds legal responsibility and ultimate authority over the autonomous agent swarm. Board approval is required for decisions above the CEO's autonomous authority threshold.

---

## Members

| Name | Discord ID | Role | Authority Scope |
|---|---|---|---|
| Bouveng | 708808214371762267 | Board member | All scopes |
| Dalesjö | 395265200367992843 | Board member | All scopes |
| Cedergren-Malmqvist | TBD | Board member | All scopes |
| Lundkvist | TBD | Board member | All scopes |
| Wladyko | TBD | Board member | All scopes |
| Zaleski | TBD | Board member | All scopes |

*Discord IDs to be filled in as members are onboarded. Only members with a confirmed Discord ID are eligible to cast binding votes.*

---

## Authority Scopes

Board approval is required when any of the following thresholds are crossed:

| Scope | Trigger |
|---|---|
| `agent_constitution_change` | Any modification to a management-tier agent's system prompt or traits |
| `budget_above_threshold` | Any single expenditure or commitment above the CEO's autonomous budget limit (TBD — CFO to specify) |
| `client_contract` | Any client engagement or commercial agreement |
| `new_agent_deployment` | Deployment of a new management-tier agent |
| `security_exception` | Any exception to the security baseline defined by the CTO |
| `data_sovereignty_exception` | Any decision to route data off local hardware |

---

## Approval Flow (Option A — Active)

### How a request is raised

An agent (CEO or CTO) posts an approval request to `#theoffice_` in the following format:

```
🗳️ APPROVAL REQUEST
Task ID: <task_id>
Scope: <authority_scope>
Motion: <one sentence — what is being approved>
Context: <brief rationale — 2-3 sentences max>
Threshold: <simple_majority | unanimous>
Deadline: <ISO8601 or "no deadline">
```

### How Board members vote

React to the approval request message with:
- ✅ — Approve
- 🚫 — Reject

Only reactions from Discord IDs listed in this file are counted as binding votes.

### How the result is recorded

On threshold met (approve or reject), the gateway writes the outcome to:
`/home/ubuntu/.openclaw/workspace/runtime/approvals/<task_id>.json`

```json
{
  "task_id": "<task_id>",
  "scope": "<authority_scope>",
  "motion": "<motion text>",
  "threshold": "simple_majority | unanimous",
  "votes": {
    "approve": ["<discord_id>"],
    "reject": ["<discord_id>"]
  },
  "outcome": "approved | rejected | pending",
  "resolved_at": "<ISO8601 or null>",
  "deadline": "<ISO8601 or null>"
}
```

The requesting agent is notified via `sessions_send` with the outcome JSON.

### Threshold definitions

| Threshold | Rule |
|---|---|
| `simple_majority` | More than half of voting members approve. Non-votes are abstentions. |
| `unanimous` | All members with confirmed Discord IDs must approve. |

Default threshold: `simple_majority` unless the request specifies otherwise.

---

## Roster Update Process

To add or update a Board member's Discord ID:
1. Board member confirms their Discord ID in `#theoffice_`
2. CTO updates this file and commits
3. Change is logged to `memory/YYYY-MM-DD.md` under the `board-roster-update` anchor

---

*Approval results archive: `runtime/approvals/`*
*Decision log: `MEMORY.md` + `memory/YYYY-MM-DD.md`*
*Protocol version: Option A (file-based). Migrates to SQLite Task DAG (Option B) in Q2.*
