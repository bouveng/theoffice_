# Specialists Tier

> Mid-level execution layer. Translates C-suite strategy into concrete deliverables across engineering, operations, marketing, and media.

---

## Overview

Specialists receive direction from the [Management](management.md) tier ([CEO](../agents/management/ceo/ceo.md)/[CTO](../agents/management/cto/cto.md)/[CFO](../agents/management/cfo/cfo.md)/[CAO](../agents/management/cao/cao.md)) and break it down into actionable tasks for the [Worker Swarm](workers.md). They own their domain and are accountable for output quality within it. All specialists operate under the values and rules of engagement defined in the [corporate statement](office-statement.md).

---

## Specialist Agents

### COO — Operations Manager ("24/7 Watchdog")
→ [Full agent profile](../agents/specialists/coo/coo.md)
- **Model**: Llama 3.1 70B
- **Role**: Breaks down [CEO](../agents/management/ceo/ceo.md) goals into granular tasks for [Workers](workers.md). Monitors the 24/7 heartbeat of the organization.
- **RAM**: ~42GB

### DOE — Director of Engineering
→ [Full agent profile](../agents/specialists/doe/doe.md)
- **Model**: Qwen2.5-Coder 32B or DeepSeek-V3
- **Role**: Complex code development, security audits, managing the technical infrastructure of other agents
- **RAM**: ~20–40GB

### CMO — Growth Strategy & Market Positioning
→ [Full agent profile](../agents/specialists/cmo/cmo.md)
- **Model**: Llama 3.1 70B (4-bit)
- **Role**: Translates [CEO](../agents/management/ceo/ceo.md) vision into go-to-market strategy. Uses [CAO](../agents/management/cao/cao.md) data to define audiences and directs [CCO](../agents/specialists/cco/cco.md) asset production.
- **RAM**: ~42GB

### CCO — Media & Design
→ [Full agent profile](../agents/specialists/cco/cco.md)
- **Model**: Flux.1 [dev] (images) + Llama 3.1 8B (prompt engineering)
- **Role**: Brand visuals, social media assets, video storyboards. Tasks the GPU for image/video generation.
- **RAM**: ~35GB

---

## Models in Use

| Agent | Model | Strength |
|---|---|---|
| COO | Llama 3.1 70B | General task orchestration |
| DOE | Qwen2.5-Coder 32B / DeepSeek-V3 | Code & architecture |
| CMO | Llama 3.1 70B 4-bit | Strategy & language |
| CCO | Flux.1 [dev] + Llama 3.1 8B | Visual generation |

---

## Position in the Org

```
Board of Humans
    └── CEO
        ├── COO ← orchestrates Worker Swarm
        ├── DOE
        ├── CMO ← directs CCO
        └── CCO
```
