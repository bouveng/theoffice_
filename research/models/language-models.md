# Language Models — Selecting and Training for the Office

The [Office](../../framework/office.md) runs locally. No API calls to Anthropic, no dependency on OpenAI's infrastructure, no third-party data egress. This is a hard constraint, not a preference. This document covers what an LLM actually is under the hood, what it costs to build one from scratch versus running existing open weights, and what the right model strategy looks like for a local, sovereign [Office](../../framework/office.md) swarm.

For the complete model catalogue — every model in the Office stack by capability domain — see [models.md](models.md). This document covers the underlying architecture, training methodology, and strategic model tiering.

---

## What's in a Model File

An LLM checkpoint is a **single large matrix of floating-point numbers** — the model's weights. Nothing else. No executable code, no logic. The architecture (the code that reads and interprets those weights) is a separate, small file.

```
[transformer_block_0.attention.W_q: float16[4096, 4096]]
[transformer_block_0.attention.W_k: float16[4096, 4096]]
... × N layers × {Q, K, V, O, FFN_up, FFN_down, ...}
```

A 7B parameter model at float16 precision = ~14 GB on disk. A 70B model = ~140 GB. Quantized to 4-bit (GGUF/AWQ formats) cuts that approximately 4×. A 70B model quantized to 4-bit fits in ~40 GB VRAM — two consumer-grade 24 GB GPUs, or one high-end 80 GB A100.

**Practical implication for the [Office](../../framework/office.md):** hardware procurement is a model selection decision. The [CTO](../../agents/management/cto/cto.md) cannot finalise infrastructure requirements until the model tier strategy is set.

---

## Core Architecture (No Hand-Waving)

**Transformer architecture** — Every major LLM is a stack of identical blocks, each containing:

- **Multi-head self-attention** — scores which tokens should attend to which via Q/K/V dot-product. This is where relationships and context are resolved.
- **Feed-forward network** — two linear projections with a nonlinearity (SwiGLU or GELU). This is where most factual "knowledge" is encoded.
- **Layer norm + residual connections** — numerical stability; allows very deep stacks.

**Tokenization** — Input is chunked into tokens (~3–4 characters average, using BPE or SentencePiece). The model never sees characters or words — only integer IDs mapped to embedding vectors. The Office's agents communicate in natural language, but every prompt becomes a token sequence before the model ever touches it.

**Inference** — Pure matrix multiplication. Token in → logits out → sample next token → repeat. It is stateless between calls except for the **KV cache** (cached attention keys/values for the active context window). This is why context hygiene matters: a bloated context means a bloated KV cache, which means more VRAM, slower inference, and degraded reasoning.

**Quantization** — Reducing weight precision from float16 to int8 or int4. Minor quality degradation, major VRAM and speed gains. GGUF (llama.cpp format) and AWQ/GPTQ (vLLM format) are the two dominant quantization approaches. Both are viable for local deployment.

---

## Building a Model From Scratch

### Phase 1 — Pre-training (the expensive part)

Pre-training is next-token prediction on massive raw text corpora. The model learns to complete documents. It learns grammar, facts, reasoning patterns, and code — not by being told, but by predicting billions of tokens.

```
Loss = -log P(token_t | token_0 ... token_{t-1})
```

| Scale | Params | Training tokens | GPU-hours (A100) | Estimated cost |
|---|---|---|---|---|
| Research/toy | 125M | 1–5B | ~500 | ~$200 |
| Useful small | 7B | 1T | ~180,000 | ~$150K |
| GPT-3 class | 175B | 300B | ~3.6M | ~$5M+ |
| Frontier class | 70–200B+ | 2–15T | Tens of millions | $50M–$500M+ |

**Data pipeline matters more than architecture.** Pre-training data sources — FineWeb, Common Crawl, The Pile, GitHub, arXiv, curated books — are deduplicated, filtered, and weighted. A poorly curated dataset with a good architecture will lose to a well-curated dataset with a standard architecture.

### Phase 2 — Fine-tuning and Alignment

After pre-training you have a **document completer**, not an assistant or agent. You then apply one or more alignment stages:

1. **SFT (Supervised Fine-Tuning)** — typically 10K–1M high-quality instruction/response pairs. Teaches the model to be helpful and follow instructions.
2. **RLHF (Reinforcement Learning from Human Feedback)** — train a reward model, run PPO. The classic alignment pipeline.
3. **DPO (Direct Preference Optimization)** — simpler alternative to RLHF, now the dominant approach for most fine-tuning projects. Trains directly on preference pairs without a separate reward model.
4. **RLAIF / Constitutional AI** — AI provides feedback rather than humans, enabling scale. Anthropic's approach.

### Phase 3 — Agentic and Multi-Agent Training

This phase is directly relevant to the [Office](../../framework/office.md). A model that has completed Phases 1 and 2 can answer questions. It cannot reliably operate as an autonomous agent in a multi-tier swarm unless trained on agentic patterns specifically:

- **Tool-use training** — function calling, JSON mode output, and tool schema comprehension baked into the fine-tuning corpus. Without this, workers produce inconsistent structured output.
- **Long-horizon reasoning** — chain-of-thought, scratchpad patterns, task decomposition. The [CEO](../../agents/management/ceo/ceo.md) and [COO](../../agents/specialists/coo/coo.md) need this; [workers](../../framework/workers.md) generally do not.
- **Context discipline** — knowing when to call a tool versus reason internally. A model untrained on this will over-reason internally or over-call tools, both of which degrade performance in the [Office](../../framework/office.md)'s ReAct-loop execution model.
- **Multi-agent message protocols** — training on orchestrator/subagent roles explicitly. The model needs to have seen examples of: receiving a task from an orchestrator, executing it cleanly, and returning a typed result. Without this, handoff quality is unpredictable.
- **Sparse reward handling** — agentic training reward signals are sparse and long-horizon. **RLVR (Reinforcement Learning with Verifiable Rewards)**, as used in DeepSeek-R1, is the most promising current approach: use tasks with objectively verifiable outputs (math, code, structured data) as reward signals, not human preference ratings.

---

## The Three Paths to Independence

### Option A — Run Existing Open Weights (Recommended First Step)

The open-weight ecosystem has closed the gap with frontier proprietary models significantly. The [Office](../../framework/office.md) can achieve near-frontier capability today without any training budget:

- **Llama 3.3 70B** — Meta. GPT-4 class on most benchmarks. 4-bit quantized fits in ~40 GB VRAM. Apache 2.0 licensed.
- **DeepSeek-V3 / R1** — DeepSeek. Opus-competitive. Fully open weights. R1 specifically trained for reasoning and chain-of-thought, which makes it a strong candidate for the [management tier](../../framework/management.md).
- **Qwen 2.5 72B** — Alibaba. Strong coding and instruction-following. Good for [DOE](../../agents/specialists/doe/doe.md) and engineering-heavy tasks.
- **Mistral / Mixtral** — European, strong multilingual support. Mixture-of-experts variants offer good throughput-to-quality tradeios for the [specialist tier](../../framework/specialists.md).

Local runtimes:
- **Ollama** — wraps llama.cpp with a clean HTTP API. Uses Apple Metal backend on Apple Silicon. The primary runtime for the Office on the Mac Studio M5.
- **MLX** — Apple's own ML framework, optimised for the unified memory architecture of M-series chips. Best for fine-tuning on Apple Silicon; also supports fast inference.
- **vLLM** — production-grade, high-throughput inference with PagedAttention (efficient KV cache management). CUDA-only — does not run on Apple Silicon. Right choice for NVIDIA-based deployments only.
- **llama.cpp** — lowest hardware floor, runs quantized models on CPU+GPU hybrid. The backend Ollama wraps; directly usable for edge deployments.

**For the [Office](../../framework/office.md):** Option A is the starting point. Run DeepSeek-R1 or Llama 3.3 70B for the [management tier](../../framework/management.md); run a 7–13B model for [workers](../../framework/workers.md). Validate the full system before spending on training data.

### Option B — Fine-tune Open Weights on Office-Specific Data

Start from an Option A base and fine-tune it on your own data + agentic task patterns. This is what most "independent" organisations actually do in practice.

- **LoRA / QLoRA** — Low-Rank Adaptation. Instead of updating all weights, you train a small adapter layer (typically < 1% of total parameters). QLoRA extends this to 4-bit quantized base models. A 70B model can be QLoRA fine-tuned on 1–2 A100s. This is the feasible path for the [Office](../../framework/office.md) at reasonable cost.
- **Training data for the Office** — fine-tuning corpus should include: task decomposition examples (CEO/COO patterns), typed JSON output examples (worker patterns), tool-calling sequences with realistic Office tools, failure recovery examples, and Office-specific domain knowledge.
- **Evaluation** — critical. Before and after fine-tuning, run the model on a fixed benchmark set covering the tasks each tier is responsible for. The [Hallucination Hunter](../../agents/workers/hallucination-hunter/hallucination-hunter.md) should be part of the eval pipeline.

**For the [Office](../../framework/office.md):** Option B becomes relevant once the swarm is operational and producing real task data. The [Digital Archivist](../../agents/workers/digital-archivist/digital-archivist.md)'s trace logs are training data. Every successful task the [Office](../../framework/office.md) completes — and every failure — is a data point for future fine-tuning.

### Option C — Pre-train From Scratch

Only makes sense if:
- Your domain is so specialised that general pre-training is noise (e.g., a heavily regulated sector with a proprietary knowledge corpus that cannot be publicly disclosed)
- You have regulatory or IP requirements to control every training byte
- You need to exclude specific knowledge domains entirely from the base model

Budget: **$500K minimum** for anything useful. **$5M+** for GPT-3.5 class capability. This is not a near-term path for the [Office](../../framework/office.md).

---

## Model Strategy Per Office Tier

The [Office](../../framework/office.md)'s three-tier architecture maps directly onto a model tiering strategy. This is not optional — running the same model at every tier is wasteful and architecturally unsound.

```
Management Tier  →  70B class (DeepSeek-R1, Llama 3.3 70B)
                     High reasoning, long-horizon planning, strategic synthesis
                     Slower inference is acceptable; these agents run infrequently

Specialist Tier  →  30–40B class (Qwen 2.5 32B, Mistral 24B)
                     Domain execution, translates strategy into tasks
                     Balance of reasoning and throughput

Worker Swarm     →  7–13B class (Qwen 2.5 7B, Llama 3.2 11B)
                     Narrow tasks, strict JSON output, fast inference
                     High throughput, low VRAM per instance
                     Spawned and torn down per task — cheapness is a feature
```

**Critical point from [orchestration research](../architecture/orchestration.md):** context hygiene already established that a narrow single-purpose worker runs at ~1,400 tokens overhead versus ~45,000 for a generalist after one month of operation. The same principle applies at the model level. Do not use a 70B model for a worker that outputs JSON. It is not safer, it is slower and it wastes inference compute. Worker tasks should be structurally impossible to get wrong at 7B with the right context — if they aren't, the task definition or the context schema needs to change.

---

## Agentic Training Requirements for the Office

If the [Office](../../framework/office.md) reaches Option B (fine-tuning), the training data and objectives for each tier are distinct:

### Management Tier Training (CEO, CTO, CFO, CAO)
- Multi-step reasoning with explicit chain-of-thought
- Goal decomposition into dependency-aware task DAGs (links to [orchestration.md](../architecture/orchestration.md) task DAG format)
- Authority threshold recognition: knowing when to escalate versus decide
- Output: structured strategic directives, not prose
- Failure mode to train against: over-confidence on incomplete information

### Specialist Tier Training (COO, DOE, CMO, CCO)
- Task routing: given a directive and a worker registry, assign correctly
- Context compilation: given a task and a ChromaDB query interface, produce minimal scoped context
- Structured handoffs: typed inputs/outputs at every agent boundary
- Failure mode to train against: scope creep — specialists absorbing worker tasks

### Worker Tier Training
- Strict schema adherence: output must pass JSON validation on first attempt
- Tool selection discipline: ≤10 tools in context, select the right one without hallucinating tool names
- Idempotency awareness: the same task with the same inputs should produce the same result
- Graceful failure: when the task is outside scope, return a typed error rather than hallucinating a result
- Failure mode to train against: tool hallucination — calling tools that don't exist

---

## Reward Signals in Agentic Training

The hardest part of Phase 3 training is the reward signal. Human preference ratings (RLHF) do not scale to long-horizon agentic tasks — the latency between action and outcome is too long, and human raters cannot evaluate complex multi-step agent behaviour at volume.

**RLVR (Reinforcement Learning with Verifiable Rewards)** is the right approach:
- Use tasks whose outputs are objectively verifiable: code that runs and passes tests, JSON that validates against a schema, SQL that returns the correct result, plans whose sub-tasks are all executable
- The reward model is a verifier, not a preference rater
- DeepSeek-R1 demonstrated this at scale: the model trained entirely on verifiable mathematical and code tasks and generalised to broad reasoning capability

**For the [Office](../../framework/office.md):** worker tasks are naturally suited to RLVR. Worker outputs are typed, schema-validated, and their correctness is deterministic. The [QA Specialist](../../agents/workers/qa-specialist/qa-specialist.md) is essentially a reward model — formalising it as one for training purposes is a natural evolution.

---

## Hardware Baseline for Local Independence

### Primary setup: Mac Studio M5 Ultra (512GB)

The Mac Studio M5 Ultra is the chosen hardware for the Office. The decisive advantage is **unified memory** — CPU and GPU share the same 512GB pool with no VRAM ceiling. All tiers of the Office swarm can reside in memory simultaneously.

Expected model fit:

| Agent tier | Model | Memory footprint |
|---|---|---|
| CEO (management) | Llama 3.1 405B Q4 / DeepSeek-R1 | ~230GB |
| CTO + CFO + CAO | Qwen 32B, Mistral Large 2, Command R+ | ~20–60GB each |
| COO + DOE + CMO (specialists) | Llama 3.1 70B (4-bit) | ~40GB each |
| Worker swarm (×4 concurrent) | Llama 3.2 8B / Qwen 7B | ~5–8GB each |
| **Total** | Full Office swarm | ~400–480GB |

512GB is non-negotiable — running CEO + 2 specialists + 4 concurrent workers simultaneously requires it. 192GB (M5 Max) is insufficient for the management tier.

**Runtime:** Ollama (dev/prod — wraps llama.cpp Metal backend) or MLX (Apple's own framework, best for fine-tuning on Apple Silicon). vLLM is CUDA-only and does not run on Apple Silicon.

### Apple Silicon runtime implications

Running on the Mac Studio M5 means the runtime stack is Ollama or MLX — not vLLM. This has practical consequences:

- **No tensor parallelism** — Ollama runs a single model instance per process; parallel workers share the same Ollama daemon via queued requests, not multi-GPU tensor splits.
- **Quantization tooling** — GGUF (llama.cpp format) is the primary quantization format for Ollama. AWQ/GPTQ (vLLM formats) are not applicable here.
- **Fine-tuning** — QLoRA via HuggingFace Transformers does not run on Apple Silicon. MLX provides its own fine-tuning toolchain (`mlx-lm`), which is the correct approach for Option B work on this hardware.
- **Memory management** — Ollama loads and unloads models from unified memory on demand. Running multiple large models simultaneously requires configuring Ollama's model keep-alive to hold models in memory rather than evicting between requests.

### Hardware comparison

| Setup | Key specs | Memory | Est. cost | Runs Office swarm? | Notes |
|---|---|---|---|---|---|
| **Mac Studio M5 Ultra** | M5 Ultra, 512GB unified | 512GB unified | €17K–€23K | ✓ Full swarm | Chosen setup. Silent, 300W. Ollama/MLX only. |
| **Mac Mini M4 Pro** | M4 Pro, 64GB unified | 64GB unified | ~€2,200 | Dev/workers only | Good for prototyping. Cannot run 70B+. |
| **Single RTX 4090 workstation** | i9/Threadripper, 24GB VRAM | 24GB VRAM | ~€5K–7K | Workers only | Max ~30B at 4-bit with CPU offload. vLLM supported. |
| **Dual RTX 4090 workstation** | Threadripper, 48GB total VRAM | 48GB VRAM | ~€10K–14K | Specialists + workers | Runs 70B at 4-bit. No 405B. vLLM supported. |
| **Single A100 80GB server** | Supermicro/Dell, 256GB RAM | 80GB VRAM | ~€12K–18K (used) | Management (70B) + workers | Runs 70B at full precision. vLLM supported. |
| **8× H100 cloud node** | Lambda Labs / CoreWeave | 640GB VRAM total | ~$20–30/hr | Full swarm + headroom | No upfront cost. Not sovereign. |

---

## Open Questions

- **Which 70B base for the management tier?** DeepSeek-R1 has the strongest reasoning benchmark profile. Llama 3.3 70B has the most active fine-tuning ecosystem. Both are viable; the choice depends on reasoning task performance measured against the [CEO](../../agents/management/ceo/ceo.md)'s actual decision patterns.
- **Single Ollama instance or per-tier instances?** A single Ollama daemon serving all tiers simplifies ops but creates contention when models need to be swapped in/out of unified memory. Per-tier persistent model loads allow independent scaling — workers can run their own 7B model without evicting the management-tier model from memory.
- **Context window size requirements per tier?** The [COO](../../agents/specialists/coo/coo.md) needs to hold the full task DAG. At what point does DAG complexity exceed the management-tier model's context window? This sets an upper bound on how complex a single workflow can grow before summarisation is required.
- **Fine-tuning trigger conditions** — at what point does Option B become worth the effort? A reasonable threshold: once the [Office](../../framework/office.md) has generated 10,000+ verified task completions in the trace log, evaluate whether a fine-tuned 7B worker outperforms the base model on Office-specific tasks. If it does by >10%, invest in a training run.
- **Quantization quality floor** — 4-bit quantization is a known quality trade-off. For management-tier reasoning tasks, is 4-bit DeepSeek-R1 good enough, or does the [CEO](../../agents/management/ceo/ceo.md) require full float16 precision? Run comparative eval before committing to hardware.
- **Model versioning and rollback** — when a new fine-tuned model replaces the base model, what is the [Office](../../framework/office.md)'s procedure for validating the replacement before going live? The [Hallucination Hunter](../../agents/workers/hallucination-hunter/hallucination-hunter.md) and [QA Specialist](../../agents/workers/qa-specialist/qa-specialist.md) should run a regression suite against a fixed task benchmark before any model swap.
- **Training data provenance** — if the [Office](../../framework/office.md) fine-tunes on its own trace logs, the training data contains the outputs of the current model. This is a form of model collapse risk. How does the [CAO](../../agents/management/cao/cao.md) curate and filter trace log data to prevent degradation loops?
