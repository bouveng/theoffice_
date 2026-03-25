# Management Tier

> Autonomous AI enterprise. Decentralized. Locally hosted. Total data sovereignty.

---

## Mission

Replace traditional management with a swarm of frontier-class AI models running entirely on local hardware — delivering executive-grade execution and strategic oversight with unprecedented efficiency.

See the [corporate statement](office-statement.md) for the Office's goal, stakeholders, values, and rules of engagement.

---

## Infrastructure

| Component | Spec |
|---|---|
| Chip | Apple M5 Ultra (32-core CPU / 80-core GPU) |
| Memory | 512GB Unified Memory *(non-negotiable)* |
| Storage | 4–8TB Internal SSD + 4–8TB External (OWC ThunderBlade) |
| UPS | APC Smart-UPS X 1500VA |
| Est. Cost | €17,000–€23,000 |

Unified Memory is the primary driver — it allows multiple large models to reside in memory simultaneously, avoiding I/O bottlenecks.

For the full model catalogue covering all capability domains available to the Office swarm, see [`research/models.md`](../research/models/models.md).

---

## Management Agents

### CEO — Strategic Director
→ [Full agent profile](../agents/management/ceo/ceo.md)
- **Model**: Llama 3.1 405B (Quantized) or DeepSeek-R1 (Full Reasoning)
- **Role**: High-level planning, conflict resolution between departments, final quality gate before delivery
- **RAM**: ~230GB

### CTO — Development & Architecture
→ [Full agent profile](../agents/management/cto/cto.md)
- **Model**: Qwen2.5-Coder 32B or DeepSeek-V3
- **Role**: Complex code, security audits, technical infrastructure oversight
- **RAM**: ~20–40GB

### CFO — Finance & Budget
→ [Full agent profile](../agents/management/cfo/cfo.md)
- **Model**: Mistral Large 2 or Llama 3.1 70B
- **Role**: API cost tracking, ROI calculation, autonomous wallet management, financial forecasting
- **RAM**: ~40GB

### CAO — Data & Market Research
→ [Full agent profile](../agents/management/cao/cao.md)
- **Model**: Command R+ (RAG/tool-use optimized)
- **Role**: Web research, PDF ingestion, maintaining the company vector database
- **RAM**: ~60GB

---

## Legal Structure

EU/SE law requires a natural person or board to hold legal responsibility. The **Board of Humans** sits above the autonomous [CEO](../agents/management/ceo/ceo.md) — this is the legally compliant path recommended by EU/SE experts for operating such a business today.

**Board**: Bouveng / Cedergren-Malmqvist / Dalesjö / Lundkvist / Wladyko / Zaleski

---

## Roadmap

| Quarter | Milestone |
|---|---|
| Q1 2026 | Research, prototyping, architectural design |
| Q2 2026 | Physical infrastructure install, technical layers, internal tooling |
| Q2 2026 | POC — office working for internal needs |
| Q3 2026 | Organisation running 24/7, full autonomous pipeline |
| Q4 2026 | Office setup with partners, private clients, SMBs, entrepreneurs |
