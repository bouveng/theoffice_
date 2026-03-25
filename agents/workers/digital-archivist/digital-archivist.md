# Digital Archivist — Memory Management

## Identity

| Field | Value |
|---|---|
| Title | Digital Archivist |
| Tier | [Workers](../../../framework/workers.md) |
| Domain | Memory Management |
| Spawned by | [COO](../../specialists/coo/coo.md) (after every significant agent interaction) |

## Model

| Field | Value |
|---|---|
| Model | Mistral 7B v0.3 |
| RAM Allocation | ~5GB |
| Strength | Summarization, embedding generation, structured indexing |

## Task

Summarizes completed agent interactions and task outputs. Converts them into embeddings and writes them to the [ChromaDB](../../../research/architecture/data-storage.md) vector database. Maintains the organization's long-term memory so agents can retrieve relevant context without carrying history in their own context windows.

## Spawn Conditions

- Triggered by the [COO](../../specialists/coo/coo.md) after every completed task cycle
- Also triggered when any agent explicitly offloads content to memory via the task list

## Input

```
content:     str         # raw interaction log, document, or task output
source:      str         # which agent produced it
content_type: str        # "task_output" | "research" | "decision" | "draft"
tags:        list[str]   # metadata for retrieval
```

## Output

```
embedding_id: str        # ChromaDB record ID
summary:      str        # human-readable summary of what was stored
status:       "stored" | "failed"
```

## Constraints

- Write access to [ChromaDB](../../../research/architecture/data-storage.md) only — cannot read or query records
- Must not store raw model outputs verbatim — always summarize first to reduce noise
- Deduplication check required before writing — flag if a near-identical record exists

## Skills Used

- `summarize` — primary tool; used to compress all content before embedding
