# The Office Library — Data Storage and Long-Term Memory

The office has no persistent state inside its agents. Every spawned Worker starts with a clean, minimal context and is torn down when its task completes. The library is what survives.

ChromaDB is the office's long-term memory: a local vector database that holds the institutional record across agent lifecycles, task cycles, and sessions. Anything worth keeping leaves the context window and enters the library.

---

## The Database: ChromaDB

ChromaDB is not a relational store. There are no tables, no primary keys, no `SELECT WHERE` queries.

Records are stored as **embeddings** — high-dimensional vectors that encode semantic meaning. Retrieval is by similarity: "what do we know about X?" finds the closest matches by meaning, not by exact text or ID. This suits agents well. They ask natural questions about topics, not structured queries against known schemas.

Properties:
- Runs locally — data sovereignty, no cloud dependency
- Owned and maintained by the **[CAO](../../agents/management/cao/cao.md)** (Chief Analytics Officer)
- Stored on local hardware; the [CAO](../../agents/management/cao/cao.md) is responsible for keeping it current
- Four content types, defined by the [Digital Archivist](../../agents/workers/digital-archivist/digital-archivist.md) input schema:
  - `task_output` — completed Worker results
  - `research` — ingested documents, feeds, external sources
  - `decision` — logged choices and rationale
  - `draft` — content pending verification or delivery

---

## The [Digital Archivist](../../agents/workers/digital-archivist/digital-archivist.md) — The Librarian

The [Digital Archivist](../../agents/workers/digital-archivist/digital-archivist.md) is the only agent with write access to ChromaDB. Its sole job is to index completed work.

| Field | Value |
|---|---|
| Model | Mistral 7B v0.3 |
| RAM | ~5GB |
| Access | Write-only |

**Input:**
```
content:      str         # raw interaction log, document, or task output
source:       str         # which agent produced it
content_type: str         # "task_output" | "research" | "decision" | "draft"
tags:         list[str]   # metadata for retrieval
```

**Output:**
```
embedding_id: str         # ChromaDB record ID
summary:      str         # human-readable summary of what was stored
status:       "stored" | "failed"
```

**Key constraints:**
- Never stores raw output verbatim — always summarizes first to reduce noise and improve retrieval quality
- Runs a deduplication check before writing — flags if a near-identical record already exists
- Write-only: cannot query or read records, which prevents accidental context contamination

The Archivist is spawned for a single indexing job and torn down immediately after. It costs ~5GB RAM while running and zero when not.

---

## Spawn Conditions — When It Is Called

Two triggers:

**1. Automatic — after every completed task cycle**

The [COO](../../agents/specialists/coo/coo.md) marks a task `done`. It immediately creates a new task entry pointing to the [Digital Archivist](../../agents/workers/digital-archivist/digital-archivist.md) with the task result as input:

```json
{
  "assigned_to": "digital-archivist",
  "context": {
    "content": "<task result>",
    "source": "<originating agent>",
    "content_type": "task_output",
    "tags": ["..."]
  }
}
```

This happens after every significant interaction — the Archivist is a routine post-task step, not an exceptional one.

**2. Explicit — any agent offloads content directly**

Any agent can write a task list entry targeting the [Digital Archivist](../../agents/workers/digital-archivist/digital-archivist.md). This is used when an agent produces content mid-cycle that should be preserved regardless of whether the overall task is done — for example, the [CAO](../../agents/management/cao/cao.md) indexing an ingested research document before proceeding to analysis.

---

## Access Control — Who Can Read and Write

| Agent | Access | Purpose |
|---|---|---|
| [Digital Archivist](../../agents/workers/digital-archivist/digital-archivist.md) | Write-only | Indexes all output after task completion |
| [Hallucination Hunter](../../agents/workers/hallucination-hunter/hallucination-hunter.md) | Read-only | Cross-references drafts against ground truth |
| [CAO](../../agents/management/cao/cao.md) | Read + Manage | Runs RAG queries; ingests external research |

This separation is intentional. The Archivist cannot corrupt records by querying them during a write pass. The Hunter cannot pollute records by writing back its findings. The [CAO](../../agents/management/cao/cao.md) is the only agent that both reads and manages the database, which concentrates ownership and makes the library's state auditable.

---

## Data Flow

```
Agent interaction / task output
        ↓
  [COO](../../agents/specialists/coo/coo.md) marks task done
        ↓
  Spawns [Digital Archivist](../../agents/workers/digital-archivist/digital-archivist.md)
        ↓
  Archivist summarizes → deduplication check → embeds → writes to ChromaDB
        ↓
       ChromaDB (the library)
        ↓              ↓
      [CAO](../../agents/management/cao/cao.md)        [Hallucination Hunter](../../agents/workers/hallucination-hunter/hallucination-hunter.md)
    (RAG)        (fact-check queries)
```

---

## Why This Architecture

**Context hygiene.** Completed work leaves agent context windows and enters the library. Agents stay small and focused; history accumulates in a searchable store, not in prompts.

**Separation of concerns.** The agent that writes (Archivist) is different from the agents that read (Hunter, [CAO](../../agents/management/cao/cao.md)). No single agent can both pollute and query the record.

**RAM efficiency.** The Archivist is torn down after each indexing job. The library itself — ChromaDB at rest — costs no RAM. Large-model agents ([CAO](../../agents/management/cao/cao.md) at ~60GB, [COO](../../agents/specialists/coo/coo.md) at ~42GB) are not running continuously; they're spawned when needed.

**Auditability.** Every stored record carries a source agent, content type, and tags. The [CAO](../../agents/management/cao/cao.md) can trace any retrieved fact back to its origin.

---

## Open Questions

- **Chunking strategy** — how should the [CAO](../../agents/management/cao/cao.md) split large PDFs before handing them to the Archivist? Fixed-size chunks, semantic paragraphs, or section-level?
- **Retention policy** — does the library grow indefinitely, or is there a pruning pass for stale or superseded records?
- **Embedding model** — Mistral 7B handles summarization, but is it also generating the embeddings? A dedicated embedder (e.g. `nomic-embed-text`) might give better retrieval at lower RAM cost.
- **ChromaDB persistence backend** — the default is DuckDB+Parquet; cloud sync is not applicable (local-only by design), but the persistence path and backup strategy need defining.
