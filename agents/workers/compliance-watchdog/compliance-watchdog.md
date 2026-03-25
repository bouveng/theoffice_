# Compliance Watchdog — Security & Audit

## Identity

| Field | Value |
|---|---|
| Title | Compliance Watchdog |
| Tier | [Workers](../../../framework/workers.md) |
| Domain | Security & Audit |
| Spawned by | [COO](../../specialists/coo/coo.md) (continuous scheduled cycle) |

## Model

| Field | Value |
|---|---|
| Model | Granite-3.0-8B |
| RAM Allocation | ~5GB |
| Strength | Anomaly detection, log analysis, policy enforcement |

## Task

Scans system logs on a continuous cycle for unauthorized API calls, unexpected CPU/RAM spikes, and breaches of the agent constitution. Issues a kill-switch alert if a violation is detected. The most security-critical worker — it watches the watchers.

## Spawn Conditions

- Spawned by the [COO](../../specialists/coo/coo.md) on a fixed schedule (e.g. every 15 minutes)
- Also spawned immediately following any flagged anomaly or on-demand by the [CTO](../../management/cto/cto.md)

## Input

```
log_window: {
  start:      str             # timestamp
  end:        str             # timestamp
  sources:    list[str]       # log files or streams to scan
}
constitution: str             # path to the agent rules document
thresholds: {
  cpu_spike:  float           # % threshold for alert
  ram_spike:  float           # % threshold for alert
  api_calls:  list[str]       # disallowed external endpoints
}
```

## Output

```
status:    "clean" | "warning" | "breach"
findings:  list[{
  type:      str              # "unauthorized_api" | "resource_spike" | "constitution_breach"
  severity:  "low" | "medium" | "critical"
  detail:    str
  timestamp: str
  agent:     str              # which agent triggered the finding
}]
kill_switch: bool             # true if a critical breach was detected
```

A `kill_switch: true` result triggers an immediate alert to the Board of Humans and halts the implicated agent.

## Constraints

- Read-only access to logs — cannot modify system state directly
- Kill-switch alert must route to the Board of Humans — cannot be suppressed by any agent
- Cannot be spawned by any agent other than [COO](../../specialists/coo/coo.md) or [CTO](../../management/cto/cto.md) — prevents self-audit conflicts

## Skills Used

- `summarize` — compresses audit findings into the daily compliance report for the [Executive Briefer](../executive-briefer/executive-briefer.md)
