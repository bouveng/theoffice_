# QA Specialist — Testing & Sandboxing

## Identity

| Field | Value |
|---|---|
| Title | QA Specialist |
| Tier | [Workers](../../../framework/workers.md) |
| Domain | Testing & Sandboxing |
| Spawned by | [DOE](../../specialists/doe/doe.md) or [CTO](../../management/cto/cto.md) |

## Model

| Field | Value |
|---|---|
| Model | Qwen2.5-Coder 7B |
| RAM Allocation | ~5GB |
| Strength | Code comprehension, test execution, failure analysis |

## Task

Executes code produced by the [CTO](../../management/cto/cto.md) or [DOE](../../specialists/doe/doe.md) in isolated Docker sandboxes. Reports pass/fail results with logs and error traces. Nothing is deployed until this worker returns a `pass`.

## Spawn Conditions

- Spawned by [DOE](../../specialists/doe/doe.md) or [CTO](../../management/cto/cto.md) whenever code is ready for validation
- Re-spawned automatically on failure if the originating agent submits a fix

## Input

```
code:        str             # code to execute
language:    str             # e.g. "python", "bash", "typescript"
test_cases:  list[{
  name:      str
  input:     any
  expected:  any
}]
timeout_ms:  int             # max execution time per test
```

## Output

```
verdict:  "pass" | "fail"
results:  list[{
  test_case:  str
  status:     "pass" | "fail" | "error" | "timeout"
  output:     str
  error:      str | null
  duration_ms: int
}]
sandbox_log: str             # full execution log
```

## Constraints

- All execution happens inside an isolated Docker container — no host system access
- Network access disabled inside sandbox by default
- A `fail` verdict blocks deployment and returns control to the originating agent
- Cannot modify the code — testing only

## Skills Used

- `summarize` — compresses sandbox logs when returning results to a long test suite
