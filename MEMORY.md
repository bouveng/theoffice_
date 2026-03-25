# The Office — Shared Decision Index

Cross-agent, cross-session decisions. Every entry links to the full rationale in the daily file.
For retrieval: run `memory_search` before starting any task with cross-session context.

---

## 2026-03-25 — Architecture baseline established
- **Decision:** `docs/ARCHITECTURE.md` is the authoritative system diagram and agent contract reference.
- **Rationale:** Single source of truth for system topology, agent registry, orchestration layer, and platform status.
- **Owner:** CTO
- **Ref:** memory/2026-03-25.md#architecture-baseline | task_id: ceo-20260325-001

## 2026-03-25 — Agent communication protocol established
- **Decision:** All inter-agent communication uses typed JSON contracts (delegation / result / escalation). No free-form messaging in automated flows.
- **Rationale:** Untyped messages are untraceable and unenforced. Contracts are the source of truth.
- **Owner:** CTO
- **Ref:** memory/2026-03-25.md#comms-protocol | task_id: ceo-20260325-002

## 2026-03-25 — Memory protocol established
- **Decision:** `docs/MEMORY_PROTOCOL.md` defines write standards, file naming, store taxonomy, and retention rules for all memory stores.
- **Rationale:** Unwritten decisions do not exist as far as the swarm is concerned. Protocol enforces discipline.
- **Owner:** CTO
- **Ref:** memory/2026-03-25.md#memory-protocol | task_id: ceo-20260325-003

## 2026-03-25 — CAO is sole ChromaDB write gateway
- **Decision:** All ChromaDB writes route through the Digital Archivist (write-only worker) under CAO management. COO gateway does not write to ChromaDB directly.
- **Rationale:** Single-writer principle — preserves auditability, prevents concurrent write conflicts.
- **Owner:** CTO
- **Ref:** memory/2026-03-25.md#chromadb-write-access | task_id: ceo-20260325-001
