# Rooms — Spatial Architecture for the Office

## Concept

The Office is not a flat chat interface. It is an organisation with physical-analogue **rooms** — discrete spaces that define who belongs, what context is present, and how communication flows. Each room is a Discord channel with a defined purpose, audience, and interaction protocol.

Rooms impose structure without overhead. An agent reading its room assignment knows immediately: what is expected of it here, who else is present, and what it should and should not initiate.

---

## Room Map

```
┌─────────────────────────────────────────────────────┐
│                   THE OFFICE                        │
│                                                     │
│  ┌──────────────┐   ┌──────────────┐               │
│  │  CEO Office  │   │  CTO Office  │  Management   │
│  └──────────────┘   └──────────────┘               │
│  ┌──────────────┐   ┌──────────────┐               │
│  │  CFO Office  │   │  CAO Office  │               │
│  └──────────────┘   └──────────────┘               │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │              Board Room                      │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │              Open Floor                      │  │
│  │   (Specialists + Workers)                    │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │              Library                         │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

---

## Rooms

### Management Offices (individual)
One channel per C-suite agent. Private workspace for that agent's own context, decisions, and DMs from the Board. No other agents respond here unless invited.

| Room | Agent | Purpose |
|---|---|---|
| `#ceo` | CEO | Strategic direction, goal intake, Board DMs |
| `#cto` | CTO | Technical architecture, code, security |
| `#cfo` | CFO | Finance, budgets, wallet oversight |
| `#cao` | CAO | Research, data, knowledge base |

### Board Room
`#board-room` — Humans only. The Board submits goals, reviews briefs, and approves escalations here. Agents post to this channel only when escalating or delivering a final brief. Agents do not respond to messages here unless directly addressed.

### Open Floor
`#theoffice_` — The shared working space for all agents and Board members. All inter-agent work summaries, task status updates, delegations, and results are posted here. This is the visible heartbeat of the organisation.

Specialists and Workers operate primarily from this room. No private context — everything posted here is visible to the full team.

### Library
`#library` — Read-only reference space. Contains the canonical list of external documentation, tools, APIs, and resources available to all agents. Agents read from here when they need an authoritative reference URL. No conversation happens in this channel — it is a reference index, not a workspace.

See: [`/rooms/library.md`](../../rooms/library.md)

---

## Interaction Protocols by Room

| Room | Agents respond to | Agents initiate |
|---|---|---|
| Management offices | Direct address or delegation | Never unprompted |
| Board Room | Escalation delivery only | Never |
| Open Floor | @mention from allowed users | Task updates, status, results |
| Library | Never | Never (read-only) |

---

## Implementation

Each room maps to a Discord channel. The `rooms/` directory contains one `.md` file per room with its purpose, contents, and update protocol. Agents load the relevant room file when context about that space is needed — not on every turn.

Room files are not injected into system prompts. They are reference documents, loaded on demand — consistent with the Office's context discipline principle.

---

## Related
- [`rooms/library.md`](../../rooms/library.md) — external reference index
- [`research/architecture/orchestration.md`](orchestration.md) — agent communication patterns
- [`research/architecture/context-discipline.md`](context-discipline.md) — why rooms stay lean
