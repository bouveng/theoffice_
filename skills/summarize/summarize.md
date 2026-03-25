# summarize

Condenses any text input into a structured summary. Used across all tiers — workers pass output through it before writing to the task queue, the [Digital Archivist](../../agents/workers/digital-archivist/digital-archivist.md) uses it before writing to ChromaDB, and the [Executive Briefer](../../agents/workers/executive-briefer/executive-briefer.md) uses it to compress source material before drafting reports.

## What it does

Takes raw text and a mode, builds a prompt, calls the agent's injected `llm_call`, and returns a typed `SummaryResult`. Handles oversized input by trimming at a soft character limit before sending to the model.

## Inputs

| Parameter | Type | Description |
|---|---|---|
| `text` | `str` | Raw content to summarize |
| `mode` | `"brief" \| "detailed" \| "bullets"` | Output style. Default: `"brief"` |
| `max_tokens` | `int` | Output length cap. Default: `256` |
| `llm_call` | `callable` | Injected by the agent runtime. Signature: `(prompt: str, max_tokens: int) -> str` |

### Modes

| Mode | Output |
|---|---|
| `"brief"` | 2–3 sentence summary |
| `"detailed"` | Structured summary with key points and conclusions |
| `"bullets"` | Concise bullet-point list |

## Output

A `SummaryResult` dataclass:

```python
@dataclass
class SummaryResult:
    summary: str       # the condensed output
    mode: str          # mode used
    truncated: bool    # whether input was trimmed before processing
```

## Usage

```python
from skills.summarize import summarize

result = summarize(
    text=raw_output,
    mode="bullets",
    max_tokens=300,
    llm_call=self.llm_call,
)
```

Input over 12,000 characters is trimmed automatically. The `truncated` flag signals to the caller that the summary may be incomplete.

## Implementation

[`summarize.py`](summarize.py)
