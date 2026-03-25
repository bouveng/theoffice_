# JSON Prompting — Structured Control for AI Systems

Natural language prompts are expressive but unpredictable. JSON prompting trades some of that expressiveness for determinism — making AI output machine-readable, testable, and composable by design. For a swarm of agents that need to hand work to each other cleanly, this matters.

---

## What It Is

JSON prompting is the practice of instructing a model to produce output that conforms to a predefined JSON schema, rather than generating free-form text. It can be implemented two ways:

**Instruction-based** — the prompt says "respond only in JSON with these fields." Unreliable: 15–20% failure rate. Models add wrapper text, hallucinate fields, or produce malformed output.

**Native structured outputs** — the schema is passed as a parameter to the API; the model's token sampler is constrained at generation time so invalid tokens are never emitted. This is what OpenAI's `response_format` and Anthropic's structured outputs do. Reliability: ~100% schema adherence.

For production use in a swarm, native structured outputs are the only option worth building on. Instruction-based JSON is a workaround.

---

## Why It Adds Control

The core gain is replacing ambiguous natural language with a contract.

| Property | Natural language output | JSON structured output |
|---|---|---|
| Structure | Unpredictable | Guaranteed by schema |
| Parseability | Requires heuristics | Direct deserialization |
| Validation | After the fact, fragile | During generation |
| Field presence | Optional, inferred | Enforced (required fields) |
| Type safety | None | Enforced (string, int, array, etc.) |
| Enum constraints | Not enforceable | Enforced (only allowed values) |
| Testability | Hard | Straightforward |

**What this makes possible:**
- An agent's output can be passed directly to another agent as structured input with no parsing step
- Outputs can be validated automatically against schema before any action is taken
- Schemas can be versioned — breaking changes are detectable
- Logging and auditing become trivial: every inter-agent message is a typed record

**The key tradeoff:** structured output slightly degrades generation quality on creative tasks — research shows ~17% average reduction in open-ended generation quality. For reasoning and extraction tasks, quality is maintained or improved. The practical rule: use JSON for *communication and extraction*, not for *the creative act itself*.

---

## Agent-to-Agent Communication

This is the most directly relevant use case for the [Office](../../framework/office.md).

Today, agents in a swarm typically communicate via natural language in a task queue. This works but creates brittleness: the receiving agent has to interpret, not just read. A malformed or verbose handoff degrades the downstream agent's context.

JSON changes the contract from "understand this" to "parse this."

### The pattern

Every agent-to-agent handoff is typed. Instead of:

```
"The CMO wants the CCO to produce three banner variations in a dark cinematic style,
targeting the enterprise market, sized for LinkedIn and Twitter, with the tagline
'Intelligence without overhead'. Priority is high."
```

You send:

```json
{
  "task": "generate_assets",
  "assigned_to": "cco",
  "priority": "high",
  "brief": {
    "format": ["linkedin_banner", "twitter_banner"],
    "variations": 3,
    "style": "dark_cinematic",
    "audience": "enterprise",
    "tagline": "Intelligence without overhead"
  }
}
```

The [CCO](../../agents/specialists/cco/cco.md) does not interpret — it reads typed fields and acts. The difference is reliability at scale.

### Existing protocols built on this

The ecosystem has already converged on JSON-RPC as the inter-agent layer:

| Protocol | Basis | What it's for |
|---|---|---|
| MCP (Model Context Protocol) | JSON-RPC | Tool use, resource access — the current standard |
| A2A (Agent-to-Agent) | HTTP + JSON-RPC 2.0 | Cross-system agent interoperability |
| ACP (Agent Communication Protocol) | HTTP conventions | Enterprise-grade agent integration |

MCP is the most immediately relevant. It defines a standard way for agents to call tools and access resources via structured JSON messages — which is exactly the pattern the [Office](../../framework/office.md) task queue should use.

### Recommendation for the Office

The shared task list (owned by the [COO](../../agents/specialists/coo/coo.md)) should use a typed JSON schema per task entry. The current conceptual schema in `agents/specialists/coo/coo.md` already has the right fields (`id`, `assigned_to`, `context`, `status`, `result`, `spawned_by`). The next step is formalizing `context` as a typed schema per task type rather than a freeform string — so the receiving Worker gets a guaranteed structure, not a blob of prose.

---

## Generative AI — Where JSON Prompting Shines

### Images

Early diffusion models (Stable Diffusion 1.x, 2.x) only understood natural language prompts. FLUX.1 and FLUX.2 changed this — they follow complex structured prompts with high accuracy.

**ComfyUI** is the fullest realization of structured image generation. It represents the entire generation pipeline as a JSON-serialized directed acyclic graph (DAG). Each node is a processing unit; edges represent data flow.

```json
{
  "1": {
    "inputs": { "ckpt_name": "flux1-dev.safetensors" },
    "class_type": "CheckpointLoaderSimple"
  },
  "2": {
    "inputs": { "text": "cinematic portrait, dramatic lighting", "clip": ["1", 0] },
    "class_type": "CLIPTextEncode"
  },
  "3": {
    "inputs": {
      "model": ["1", 0], "positive": ["2", 0],
      "steps": 30, "cfg": 7.5, "sampler_name": "euler", "seed": 42
    },
    "class_type": "KSampler"
  }
}
```

Why this is powerful:
- **Reproducible**: the same JSON on the same hardware produces identical output — `seed` is a parameter, not a prayer
- **Programmable**: the [CCO](../../agents/specialists/cco/cco.md) (or a Worker) can generate these workflow JSONs dynamically rather than clicking through a GUI
- **Composable**: add ControlNet, upscalers, LoRAs, refiners as additional nodes — the pipeline grows without rewriting anything
- **API-native**: ComfyUI exposes a `/prompt` endpoint that accepts this exact format; the [Office](../../framework/office.md) can call it directly from the task queue

For the [Office](../../framework/office.md), this means the [CCO](../../agents/specialists/cco/cco.md) doesn't "describe" an image — it *programs* the generation pipeline, then passes it to the [Media Assembly Line](../../agents/workers/media-assembly-line/media-assembly-line.md) worker to execute.

**Structured prompt for FLUX at the content level:**
```json
{
  "subject": "executive in a modern minimalist office",
  "composition": { "framing": "medium_shot", "depth_of_field": "shallow" },
  "lighting": "cool_directional",
  "style": "editorial_photography",
  "negative": ["text", "watermark", "cartoon", "illustration"],
  "seed": 7823641
}
```

### Video

Video generation has a worse version of the "cross-contamination" problem: when a natural language prompt tries to describe a multi-scene sequence, details bleed between scenes — characters appear in the wrong place, a color specified for scene 2 contaminates scene 1.

JSON solves this by making each scene a discrete, bounded object:

```json
{
  "style": "cinematic_documentary",
  "sequences": [
    {
      "id": "s1",
      "duration_s": 3,
      "scene": "wide establishing shot — glass office building exterior at dawn",
      "camera": "slow_push_in",
      "lighting": "cool_blue_dawn"
    },
    {
      "id": "s2",
      "duration_s": 4,
      "scene": "interior — agents at work, screens glowing",
      "camera": "handheld_subtle",
      "lighting": "warm_screen_glow",
      "audio": "ambient_hum"
    },
    {
      "id": "s3",
      "duration_s": 2,
      "scene": "close-up — text on screen: 'Intelligence without overhead'",
      "camera": "static",
      "transition_to_next": "fade_black"
    }
  ]
}
```

Google Veo 3 has native support for this pattern. The gain: the model processes each scene object independently while the JSON structure enforces temporal and visual consistency across them.

**For the [Office](../../framework/office.md):** the [CMO](../../agents/specialists/cmo/cmo.md) produces a campaign brief. The [CCO](../../agents/specialists/cco/cco.md) converts it to a JSON video spec. The [Media Assembly Line](../../agents/workers/media-assembly-line/media-assembly-line.md) executes it against the video generation API. Each stage is a clean typed handoff.

### Music

Music generation has unique structure that maps naturally to JSON: a song has discrete sections, each with different characteristics. Describing this in prose produces "soup" — the model loses track of transitions, energy arcs, and section boundaries.

**Structured music prompt:**
```json
{
  "genre": "electronic_ambient",
  "bpm": 98,
  "key": "D_minor",
  "duration_s": 180,
  "sections": [
    {
      "type": "intro",
      "duration_s": 20,
      "energy": 0.2,
      "elements": ["sparse_pad", "distant_pulse"],
      "mood": "tension_building"
    },
    {
      "type": "verse",
      "duration_s": 40,
      "energy": 0.5,
      "elements": ["bassline", "hi_hat", "lead_synth"],
      "mood": "focused"
    },
    {
      "type": "drop",
      "duration_s": 30,
      "energy": 0.9,
      "elements": ["full_drums", "bass_heavy", "stabs"],
      "mood": "peak"
    },
    {
      "type": "outro",
      "duration_s": 20,
      "energy": 0.2,
      "elements": ["fade_pad"],
      "mood": "resolution"
    }
  ],
  "references": ["Jon Hopkins", "Floating Points"]
}
```

This gives the generation model a compositional blueprint, not a vibe. The difference between "electronic ambient music that builds to a climax" (prompt) and the JSON above is the difference between hoping and specifying.

Suno supports structural tags (`[Verse]`, `[Chorus]`, `[Drop]`, etc.) directly in its prompt format — a lightweight version of this idea. A JSON wrapper around these tags is the next step toward full programmatic control.

---

## Implementation Ideas for the Office

### 1. Typed task queue entries

The most immediate and highest-value change. Formalize the [COO](../../agents/specialists/coo/coo.md)'s task schema so that `context` is typed per task type rather than a freeform string. Example schemas:

```json
{
  "task_type": "generate_image_assets",
  "schema": {
    "brief_id": "string",
    "format": ["linkedin_banner", "twitter_banner", "instagram_square"],
    "variations": "integer",
    "style_ref": "string",
    "tagline": "string | null",
    "seed": "integer | null"
  }
}
```

Each Worker type gets its own task schema. The [COO](../../agents/specialists/coo/coo.md) validates against schema before spawning. Invalid task entries are rejected before they waste a Worker spawn.

### 2. ComfyUI integration for the [CCO](../../agents/specialists/cco/cco.md)

The [CCO](../../agents/specialists/cco/cco.md) currently generates image prompts via Llama 3.1 8B and passes them to Flux.1 [dev]. The upgrade path:
- [CCO](../../agents/specialists/cco/cco.md) generates a **ComfyUI workflow JSON** instead of a text prompt
- [Media Assembly Line](../../agents/workers/media-assembly-line/media-assembly-line.md) Worker calls the ComfyUI `/prompt` API with that JSON
- The workflow JSON controls model, sampler, seed, ControlNet, upscaler — the full pipeline, not just the text
- Results are deterministic and reproducible (seed is part of the workflow)

This turns the [CCO](../../agents/specialists/cco/cco.md) from a prompt writer into a pipeline programmer.

### 3. Structured agent-to-agent messages via MCP

Replace natural language task delegation with MCP-compatible JSON-RPC messages. The [COO](../../agents/specialists/coo/coo.md) becomes an MCP server; Workers are MCP clients. Every task assignment is a typed RPC call with a guaranteed schema.

Benefit: the [Office](../../framework/office.md) can interoperate with any MCP-compatible tool ecosystem out of the box.

### 4. Skill: `validate_task`

A lightweight skill (not a full Worker) that accepts a task entry and a schema name, validates the task's `context` against the appropriate JSON schema, and returns `valid | invalid + errors`. Called by the [COO](../../agents/specialists/coo/coo.md) before spawning any Worker.

```python
# Usage
result = validate_task(
    task=task_entry,
    schema_name="generate_image_assets",
    schemas_dir=Path("schemas/")
)
# Returns: {"valid": true} or {"valid": false, "errors": [...]}
```

### 5. JSON spec layer for the [CCO](../../agents/specialists/cco/cco.md)'s creative output

Rather than the [CCO](../../agents/specialists/cco/cco.md) handing the [Media Assembly Line](../../agents/workers/media-assembly-line/media-assembly-line.md) a text prompt, it hands a structured creative spec:

```json
{
  "type": "image",
  "campaign_id": "office-launch-q3",
  "variant": 1,
  "pipeline": "flux_dev_standard",
  "prompt": {
    "subject": "minimalist office, soft morning light, single desk",
    "style": "clean editorial photography",
    "negative": ["clutter", "people", "screens"]
  },
  "parameters": {
    "width": 1200, "height": 628,
    "steps": 30, "cfg": 7.0, "seed": 98241
  }
}
```

The [Media Assembly Line](../../agents/workers/media-assembly-line/media-assembly-line.md) reads this spec, runs the generation, and writes back:
```json
{
  "status": "complete",
  "output_path": "assets/office-launch-q3-v1.png",
  "seed_used": 98241,
  "generation_time_s": 12.4
}
```

Every generated asset is traceable to its exact spec. Any asset can be regenerated identically. Variations are produced by diffing one field at a time.

---

## Libraries Worth Knowing

| Library | What it does | Best for |
|---|---|---|
| **Instructor** (Python) | Wraps OpenAI/Anthropic SDKs; Pydantic models as output schemas; auto-retry on validation failure | API-based agents ([management tier](../../framework/management.md)) |
| **Outlines** (Python/Rust) | Constrained decoding for local models; grammar → token masks at generation time | Locally-hosted agents ([workers](../../framework/workers.md)) |
| **Pydantic** | Python schema definition; used by Instructor and most structured output tooling | Schema definition everywhere |
| **ComfyUI API** | JSON workflow execution endpoint for image/video generation | [CCO](../../agents/specialists/cco/cco.md) + [Media Assembly Line](../../agents/workers/media-assembly-line/media-assembly-line.md) |

For the [Office](../../framework/office.md) specifically: Instructor for the [management](../../framework/management.md) and [specialist](../../framework/specialists.md) tier (using Claude/cloud models), Outlines for any Worker running a local model that needs structured output.

---

## Failure Modes to Know

**Creative degradation** — forcing a creative agent to output JSON while it's generating a creative artifact degrades the artifact by ~17%. The fix: let the agent reason and create in natural language, then extract to JSON as a final formatting step. Never force the creative act itself into a schema.

**Schema rigidity** — once agents depend on a schema, changing it requires coordinating all consumers. Version schemas from day one (`"schema_version": "1.0"`).

**Hallucination doesn't disappear** — structured output guarantees the *shape* of the response, not the truth of its contents. A JSON response with `{"revenue": 4200000}` is still a hallucination if the model invented that number. RAG reduces this; schemas alone do not.

**Local model limitations** — not all locally-hosted models reliably support constrained decoding. Outlines handles this, but adds overhead. Test each Worker model before committing to structured output in production.

---

## Open Questions

- **Should the task queue schema live in a `schemas/` directory at the root?** One file per task type. This becomes the authoritative contract for the whole swarm.
- **How strict should schemas be?** `additionalProperties: false` prevents agent improvisation — is that always desirable, or do some task types need an escape hatch?
- **ComfyUI as infrastructure vs. optional integration?** If the [CCO](../../agents/specialists/cco/cco.md) is always going through ComfyUI, it should be a documented dependency. If it's optional, the [CCO](../../agents/specialists/cco/cco.md) needs a fallback path.
- **MCP vs. custom task queue?** Adopting MCP gives interoperability but introduces a dependency and protocol overhead. A custom typed task queue is simpler and sufficient for a closed swarm. Worth deciding early.
- **Versioning strategy** — what happens when a schema changes and there are tasks in the queue using the old schema? The [COO](../../agents/specialists/coo/coo.md) needs a migration or rejection strategy.
