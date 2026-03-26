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

## 2026-03-26 — Context Reset Protocol established
- **Decision:** When users request "context reset" or similar, agents must respond with exact monospaced format: ` └ Done! Brain is reset! ⌁`. Monochrome zap only, ` └ ` as first character, no colored icons.
- **Rationale:** Standardized acknowledgment for context reset requests ensures consistent user experience.
- **Owner:** CEO
- **Ref:** memory/2026-03-26.md#context-reset-protocol-directive

## 2026-03-26 — Monochrome Icon Database mandated
- **Decision:** All messages must use UTF-8 monochrome icons from database (`resources/utf8‑icons/quick‑reference‑monochrome.md`) instead of colored emoji. Categories: navigation, status, box drawing, letterlike, currency, punctuation.
- **Rationale:** Professional cross‑platform consistency; replaces colored emoji with monochrome symbols.
- **Owner:** Board
- **Ref:** memory/2026-03-26.md#monochrome-icon-database-usage

## 2026-03-26 — Office Status Update Template defined
- **Decision:** DM status updates follow template: bold 1‑2 word headlines, monochrome icons, bullet structure, tweet‑size summary with `✓ → ✗ ⌁ ∞` icons. No channel posting when status requested in DM.
- **Rationale:** Structured, concise status reporting format for Board communications.
- **Owner:** Board
- **Ref:** memory/2026-03-26.md#office-status-update-template

## 2026-03-26 — Scheduled Office Status Posts implemented
- **Decision:** Three daily status posts to `#theoffice_` channel at 07:00, 13:00, 20:00 UTC. Cron jobs configured (Morning: `ed2f8aa6-5100-4a8c-9e58-25cec1d9b2d5`, Midday: `76947bb9-c44d-4995-bfb8-4a3f689f2e46`, Evening: `26aaba1e-d513-40a2-90e6-a97639d9b5ab`).
- **Rationale:** Regular visibility into office operations; replaces single morning brief with three daily updates.
- **Owner:** Board
- **Ref:** memory/2026-03-26.md#scheduled-office-status-posts
