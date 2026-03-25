# compile-constitution

Assembles the `[CONSTITUTION]` block for an agent's system prompt at instantiation time.

## What it does

Reads the `## Runtime Fragment` section from each of the agent's assigned trait and influence files, and concatenates them into a single `[CONSTITUTION]` block prepended with a `[ROLE]` block. The compiled prompt is injected once when the agent spawns — it never appears in the per-message context window.

This enforces the [two-layer pattern](../../framework/office.md#two-layer-pattern) defined in `office.md`: the documentation layer (full prose in each `.md` file) is for humans; the runtime fragment is the only part that reaches the model.

## Inputs

| Parameter | Type | Description |
|---|---|---|
| `role` | `str` | Short role description, e.g. `"You are the CEO. You set strategy..."` |
| `traits` | `list[str]` | Trait names matching files in `traits/` (without `.md`), e.g. `["directness", "rationality"]` |
| `influence` | `str \| None` | Influence name matching a file in `traits/influence/` (without `.md`), e.g. `"ayn-rand"`. Pass `None` if no influence. |
| `traits_dir` | `Path` | Path to the `traits/` directory |

## Output

A single string with the format:

```
[ROLE]
{role}

[CONSTITUTION]
- bullet from trait 1
- bullet from trait 2
- ...
- bullet from influence
```

## Usage

Called by the agent runtime at spawn time. Not called per-message. Example:

```python
from pathlib import Path
from skills.compile_constitution import compile_constitution

system_prompt = compile_constitution(
    role="You are the CEO. You set strategy, resolve conflicts, and act as the final quality gate.",
    traits=["rationality", "directness", "independence"],
    influence="ayn-rand",
    traits_dir=Path("traits/"),
)
```

## Implementation

[`compile_constitution.py`](compile_constitution.py)
