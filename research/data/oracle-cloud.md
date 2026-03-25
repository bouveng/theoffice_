# Oracle Cloud Infrastructure (OCI)

Exploration of whether and how OCI — specifically OCI Supercluster — could host Office workloads at various scales, from a single standalone bot to a full deployed office swarm.

Source: [OCI Supercluster whitepaper](https://www.oracle.com/uk/a/ocom/docs/cloud/accelerate-ai-with-oci-supercluster.pdf) (Oracle, 2025)

---

## What OCI Supercluster Actually Is

OCI Supercluster is Oracle's GPU cluster offering, launched in 2023. The headline numbers from the whitepaper:

- **Up to 131,072 NVIDIA Blackwell GPUs** in a single cluster (2025)
- **GPU generations available**: GB200 (Grace Blackwell), B200 (Blackwell), H200, H100
- **Bare metal instances** — no hypervisor overhead, direct hardware access
- **RDMA networking** — hardware-enabled, non-blocking, ultra-low latency inter-node communication
- **Substantial local NVMe storage** — more local storage than AWS, Azure, or GCP per node
- **Petabyte-scale managed file systems** — High Performance Mount Targets and fully-managed Lustre for trillion-parameter models
- **Network throughput** — 200 Gb/sec per H200 instance for data ingestion/retrieval

GPU performance benchmarks vs H100 baseline:
- **H200**: 1.9X better LLM inference, 76% more GPU memory, 40% more bandwidth
- **B200 / GB200 (Blackwell)**: 30X better inference, 4X better training vs H100

**Pricing**: OCI claims global uniform pricing that is "significantly less" than AWS, Azure, and GCP. No regional price premiums.

**Distribution options**: 160+ regions globally, plus Dedicated Region (OCI hardware in your own data center), Isolated Region, Oracle Alloy (partner-operated), EU Sovereign Cloud, Government Cloud, and Roving Edge Devices.

**NVIDIA software stack included**: NIM microservices, DGX Cloud, AI Enterprise, RAPIDS, TensorRT-LLM, Triton Inference Server.

**Orchestration**: Oracle-managed Kubernetes (OKE) and self-managed Kubernetes, with native GPU node pools. Supports PyTorch, TensorFlow, JAX, Kueue.

---

## Tension with the Local-First Principle

The Office has a strong local-first stance (see [`local-ai.md`](../models/local-ai.md)) — data sovereignty, no vendor lock-in, full control over inference. OCI does not automatically resolve that tension, but it partially addresses it:

| Concern | Local Mac | OCI Public Cloud | OCI Dedicated Region |
|---|---|---|---|
| Data sovereignty | Full control | Trust Oracle | Full control (hardware in your DC) |
| Vendor lock-in | None | Medium (OCI APIs) | Low (standard hardware) |
| Inference cost | Hardware CAPEX | Usage-based OPEX | Negotiated contract |
| Scale ceiling | ~1-2 GPUs (M-series) | 131,072 GPUs | As contracted |
| 24/7 uptime | Fragile | Robust | Robust |
| Privacy of training data | Absolute | Requires DPA/agreements | Absolute |

**OCI Dedicated Region** is the most compatible with local-first values — it puts OCI hardware physically in a controlled data center while giving access to the full OCI software stack. For an enterprise deploying the Office at scale, this is the path that preserves data sovereignty while gaining GPU scale.

For a smaller deployment (one office, no custom training), the public cloud is acceptable if the inference models stay on-prem or use the Claude API. OCI would host the orchestration layer, not the model weights.

---

## Mapping Office Components to OCI

### Small: Discord Scribe (standalone bot)

The Discord Scribe only needs a Linux server to run. No GPU required unless doing local Whisper inference.

**Recommended instance**: `VM.Standard.A1.Flex` (Ampere A1)
- 4 OCPUs, 24 GB RAM
- **Available in OCI Always Free Tier** — zero cost
- Enough for: discord.py bot process, `small`/`base` Whisper on CPU, transcript storage, API calls to Claude for summarization

If faster Whisper is needed (medium/large-v3 locally):

**Recommended instance**: `VM.GPU.A10.1`
- 1x NVIDIA A10 GPU, 24 GB VRAM
- Handles `large-v3` Whisper comfortably in near real-time
- Also handles local LLM inference (Llama 3, Mistral) if the Claude API is not used

The Scribe's full stack fits in a single small instance. At the free tier, it costs nothing to run permanently.

---

### Medium: Single Office Deployment (swarm of agents, API-backed inference)

A deployed office — CEO, CTO, COO + specialist tier + worker swarm — running with Claude API for inference, local ChromaDB for the Digital Archivist, and MCP for agent communication. The compute here is Python processes, not GPU inference.

**Compute**: `VM.Standard.A1.Flex` or `VM.Standard.E5.Flex`
- 8–16 OCPUs, 32–64 GB RAM
- Runs the orchestration layer, MCP server, agent process pool, task queue
- ChromaDB vector store fits comfortably in RAM at this scale

**Storage**: OCI Block Volume (50–200 GB)
- Transcript archive, agent memory files, vector index persistence

**Networking**: Standard OCI VCN — not RDMA, not needed here

At this scale, OCI is just a reliable Linux server in the cloud. The Always Free A1 instance can run a small office indefinitely if inference is API-backed.

---

### Large: Office with Local Inference (self-hosted LLM tier)

When the Office runs its own LLM inference — replacing or supplementing the Claude API with locally-hosted models (Qwen, Llama, Mistral) — GPU instances become necessary.

**Inference tier** (serving the swarm):

| Model size | Instance | GPU | VRAM | Use case |
|---|---|---|---|---|
| 7B–13B (fast workers) | `VM.GPU.A10.1` | 1x A10 | 24 GB | Llama 3 8B, Mistral 7B |
| 30B–70B (specialists) | `VM.GPU.A10.2` | 2x A10 | 48 GB | Llama 3 70B Q4 |
| 70B+ (management tier) | `BM.GPU.H100.8` | 8x H100 | 640 GB | Full-precision 70B, early 405B |
| 400B+ (frontier local) | `BM.GPU.H200.8` | 8x H200 | ~1.1 TB | Llama 3.1 405B, future 1T+ models |

**NVIDIA TensorRT-LLM** + **Triton Inference Server** (both available natively on OCI) are the right serving stack here. TensorRT-LLM handles quantization (FP8, INT4 AWQ, INT8), in-flight batching, and paged KV caching — exactly what's needed to serve a high-concurrency agent swarm efficiently.

**Estimated inference throughput** (H200 instance):
- Llama 3 70B at INT8: ~500–800 tokens/sec with TensorRT-LLM
- Sufficient for ~20–50 parallel agent contexts without queuing

**Orchestration**: OCI Container Engine for Kubernetes (OKE) with a GPU node pool makes sense at this scale. Workers spawn as pods; the inference tier is a Deployment with autoscaling. The task queue (Redis or a lightweight broker) runs on a CPU node.

---

### Extra-Large: Custom Model Training / Fine-Tuning

If the Office eventually needs fine-tuned models — sector-specific agents, proprietary data, custom behaviour shaping — OCI Supercluster is the obvious venue.

**Fine-tuning a 7B–13B model**: `BM.GPU.H100.8` (8x H100, 640 GB VRAM)
- Typical LoRA fine-tune: 2–8 hours
- Full fine-tune: 12–48 hours depending on dataset size

**Fine-tuning a 70B model**: multi-node H100 or H200 cluster
- RDMA networking is critical here — without it, multi-node training is bottlenecked by network
- OCI's hardware-enabled RDMA on non-blocking InfiniBand (Quantum-2) is a genuine competitive advantage vs AWS/Azure at this tier

**Storage for training**: OCI Managed Lustre (announced 2025)
- Designed for trillion-parameter model training
- High-throughput parallel reads across many GPU nodes simultaneously
- Replaces the need to pre-stage training data locally on each node

This tier is not relevant for early Office operation, but it becomes relevant when the Office starts building proprietary models trained on accumulated company data — a clear long-term direction.

---

## Deployment Topology: Recommended Starting Point

For the Office in its current stage (local-first, API-backed, small team):

```
OCI Always Free Tier
├── VM.Standard.A1.Flex (4 OCPU, 24 GB)
│   ├── Discord Scribe bot
│   ├── Office orchestration layer (MCP server, task queue)
│   ├── Agent process pool (CEO, CTO, COO, specialists)
│   └── ChromaDB (Digital Archivist vector store)
└── OCI Block Volume (50 GB)
    ├── Transcript archive
    └── Agent memory / knowledge base files
```

Cost: **$0/month** (within free tier limits)
Claude API charges for inference are separate and usage-dependent.

When the office grows past the free tier or needs GPU inference:

```
OCI Pay-as-you-go
├── VM.Standard.E5.Flex (16 OCPU, 64 GB) — orchestration
├── VM.GPU.A10.1 — local Whisper + small model inference
├── OCI Block Volume (200 GB) — persistent storage
└── OCI Object Storage — transcript archive, long-term retention
```

Estimated cost: ~$200–400/month depending on inference load.

---

## OCI vs Other Hosts

| | OCI | AWS | Hetzner | Local Mac |
|---|---|---|---|---|
| Free GPU tier | No | No | No | Yes (M-series MPS) |
| Free CPU tier | Yes (A1, generous) | Limited | No | Yes |
| GPU cost at scale | Low (claimed ~30-50% cheaper) | High | No large GPU | N/A |
| Bare metal | Yes | Yes | Yes | Yes (it is bare metal) |
| RDMA multi-node | Yes (InfiniBand) | Yes (EFA) | No | No |
| Sovereign/on-prem option | Yes (Dedicated Region) | Yes (Outposts) | No | Yes |
| NVIDIA software stack | Native | Native | Manual | Manual (MLX) |
| 160+ regions | Yes | Yes | Limited | N/A |

For a solo developer running the Office locally, **Hetzner** is still cheaper for a single GPU box (AX102 with RTX 4090 for ~€200/month). OCI becomes competitive when you need: burst-to-cluster scale, RDMA multi-node training, managed Kubernetes, or the Dedicated Region sovereign option.

---

## What to Explore Further

- **OCI Always Free Tier details** — confirm A1 instance specs and perpetual availability
- **OCI pricing calculator** — model exact cost for a GPU inference instance serving the swarm 24/7
- **OCI Dedicated Region minimum commitment** — likely enterprise-tier, not relevant early
- **TensorRT-LLM benchmarks** on OCI H200 vs Apple Silicon M4 Ultra for the specific models in the Office stack (Qwen2.5, Llama 3.3)
- **OCI GenAI Service** — Oracle's managed LLM API (Cohere, Llama 3 models) — may be simpler than self-hosting inference for mid-scale deployments without fine-tuning requirements
