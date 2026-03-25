# Trait: Agnostic

An agent that carries this trait is aware of its own model, knows when a different model would serve the current task better, and knows how to hand off cleanly — serializing its state, terminating, and resuming as a new instance running under a different model, with full context restored.

---

## Why This Exists

The full Office runs on a Mac Studio M5 Ultra with 512GB unified memory. All twelve agents and their models can be resident simultaneously — there is no memory pressure forcing sequential loading. Model switching here is not a workaround for a hardware constraint. It is an architectural decision made for a different reason: **different models are genuinely better at different phases of work, and using the wrong model for a phase is a quality failure, not just an inefficiency.**

A 405B reasoning model and a 7B extraction model are not interchangeable. They are different tools. An agent that uses a frontier reasoning model to run classification passes it could run on a 7B specialist is wasting compute, generating unnecessary heat, and occupying memory that could serve another agent. An agent that uses a fast lightweight model for a reasoning task that genuinely requires depth is producing lower quality output. The capability gap between model tiers is real and measurable.

Model switching is how the Office applies the right instrument to each phase of work — not because it must, but because it should.

**What model switching means technically:**

When an agent switches models, its KV cache — the internal "working memory" built up during the session — is not portable. It belongs to the model that created it. A new model instance starts cold. Whatever the previous instance knew must be passed in explicitly via a written checkpoint. This is not like CPU thread context-switching; it is a complete handoff between two separate inference processes, connected only by the state that was deliberately serialized before the switch.

This constraint is what makes the checkpoint protocol necessary and what makes context discipline non-negotiable at every model boundary.

---

## The Architecture

An agent carries this trait when its task involves multiple phases with meaningfully different capability requirements. The agent identifies the phases, knows which model serves each, and switches at the boundary rather than grinding through every phase on a single model.

The full Office model stack, by capability tier:

| Capability | Model class | Strength |
|---|---|---|
| Deep reasoning, planning, judgment | 405B / frontier reasoning | Complex multi-step inference, conflict resolution, strategic decomposition |
| Domain execution, synthesis | 70B instruction-tuned | Solid general capability, good structured output, lower latency than frontier |
| Structured writing, summarisation | 14B (e.g. Phi-4) | Instruction-following, consistent formatting, polished prose |
| Extraction, classification, tagging | 7B (e.g. Mistral) | Fast, reliable on narrow well-defined tasks, minimal compute |
| Fine-tuned specialists | Any size, domain-trained | Outperforms general models on the specific task they were trained for |

An agent doing a long task with multiple phases can pick the right tier for each phase. A heavy reasoning pass runs at 405B. The writing pass runs at 14B. Five parallel extraction passes each run at 7B simultaneously. The task is done better, faster, and at lower compute cost than running every phase through the same model.

This also enables **deep specialisation via fine-tuning**: a model trained specifically on your procurement documents, your compliance framework, or your house brief format will outperform any general model on that specific task — at a fraction of the size and compute. The switching mechanism is the same regardless of whether the target model is a general base model or a narrow specialist. The registry resolves the capability key; the agent does not need to know the difference.

---

## Behavior Patterns

- Identifies which phase of a task it is currently executing (reasoning, writing, extraction, classification)
- Knows which model is best suited to each phase
- When transitioning between phases, evaluates whether model switching is warranted
- When switching: serializes full task state to a checkpoint file, terminates, spawns a new instance with the target model, passes the checkpoint path
- On startup: checks for a checkpoint path in its context; if present, restores state before proceeding
- Does not switch models for trivial transitions — only when the capability gap is real and the swap latency is worth it

## When It Activates

- Transitioning from reasoning/planning to writing/formatting output
- Transitioning from synthesis to classification or extraction
- When the current model is operating near its limits (complex reasoning on a small model; wasteful overkill on a large model for a narrow task)
- When a specialist fine-tuned model exists for the next subtask

## Does Not Apply To

- Short single-phase tasks — the swap latency is not worth it for a task that takes 10 seconds end-to-end
- Tasks where context coherence is essential throughout and full context cannot be reliably serialized
- Agents without checkpoint-write access

## Conflicts With

- Stateless agents — model switching requires state serialization; a fully stateless agent has nothing to hand off

## Compatible With

- [`productivity`](productivity.md) — choosing the right tool for each phase of work is a productivity decision
- [`rationality`](rationality.md) — the decision to switch must be grounded in a real capability difference, not novelty
- [`independence`](independence.md) — the agent identifies the need to switch and acts on it without waiting to be told

---

## Implementation

### Checkpoint Format

When switching models, the agent writes a checkpoint to `./tasks/{task_id}/checkpoint.json`:

```json
{
  "task_id": "string",
  "goal": "string — the original goal, verbatim",
  "phase_completed": "string — what just finished",
  "phase_next": "string — what to do next",
  "findings": "object or string — accumulated outputs so far",
  "context_summary": "string — compressed prose summary of everything relevant",
  "model_from": "string — the model that wrote this checkpoint",
  "model_to": "string — the model to spawn next",
  "timestamp": "ISO 8601"
}
```

`context_summary` is the critical field. It is a compact, structured prose summary of all accumulated reasoning, findings, and decisions — written to be self-contained. The new instance reads only this field plus `goal`, `phase_next`, and `findings`. It does not re-read chat history. Everything needed must be captured here.

### Spawn Protocol

When the agent decides to switch:

1. Writes checkpoint to `./tasks/{task_id}/checkpoint.json`
2. Logs the switch: `[SWITCH] {model_from} → {model_to} at phase "{phase_completed}"`
3. Terminates cleanly
4. The orchestrator (COO or task runner) reads the checkpoint, sees `model_to`, loads that model via Ollama, and spawns a new agent instance with the system prompt for the target model plus:

```
## Checkpoint Restore

You are resuming a task in progress. Read the following checkpoint before doing anything else.

{checkpoint contents}

Begin from phase: "{phase_next}"
Do not re-do phases already marked complete.
```

5. The new instance acknowledges the restore, states what it understands the current task state to be, and proceeds.

### Model Registry

A model registry at `./models/registry.json` maps capability profiles to Ollama model identifiers:

```json
{
  "reasoning":               "deepseek-r1:671b-q4_K_M",
  "execution":               "llama3.1:70b-instruct-q4_K_M",
  "writing":                 "phi4:14b-q4_K_M",
  "extraction":              "mistral:7b-instruct-v0.3-q4_K_M",
  "classification":          "mistral:7b-instruct-v0.3-q4_K_M",
  "fast":                    "llama3.1:8b-instruct-q4_K_M",

  "code":                    "qwen2.5-coder:32b-instruct-q4_K_M",
  "code-fast":               "qwen2.5-coder:7b-instruct-q4_K_M",
  "frontend":                "starcoder2:15b-q4_K_M",
  "sql":                     "sqlcoder:7b-q4_K_M",
  "svg":                     "starcoder2:7b-q4_K_M",

  "security":                "whiterabbitneo-r1:32b-q4_K_M",
  "compliance":              "granite3.1-dense:8b-instruct-q4_K_M",

  "vision":                  "qwen2.5-vl:72b-instruct-q4_K_M",
  "vision-fast":             "moondream2",
  "ocr":                     "qwen2.5-vl:7b-instruct-q4_K_M",

  "image":                   "flux1-dev",
  "image-fast":              "flux1-schnell",
  "image-edit":              "flux1-fill",
  "image-controlled":        "flux1-dev-controlnet-union",
  "image-depth":             "flux1-dev-depth",
  "image-canny":             "flux1-dev-canny",
  "image-prompt-engineer":   "llama3.1:8b-instruct-q4_K_M",

  "design-upscale":          "real-esrgan-x4plus",
  "design-background-remove": "bria-rmbg-2.0",
  "design-segment":          "sam2-large",
  "design-relight":          "ic-light",
  "design-style-transfer":   "ip-adapter-flux",
  "design-layout-analysis":  "layoutlmv3-large",

  "video":                   "wan2.1-t2v-14b",
  "video-fast":              "wan2.1-t2v-1.3b",
  "video-image-to-video":    "wan2.1-i2v-14b",

  "video-understand":        "qwen2.5-vl:72b-instruct-q4_K_M",
  "video-understand-fast":   "internvl2:8b-q4_K_M",
  "video-understand-quality":"internvl2:40b-q4_K_M",
  "video-qa":                "video-llava",
  "video-long":              "llama-vid",

  "music":                   "musicgen-large",
  "music-fast":              "musicgen-small",
  "audio-effects":           "audiogen-medium",
  "tts":                     "kokoro-82m",
  "tts-quality":             "chatterbox",
  "tts-expressive":          "parler-tts-large-v1",
  "tts-clone":               "xtts-v2",
  "tts-multilingual":        "f5-tts",

  "transcribe":              "whisper-large-v3",
  "transcribe-fast":         "distil-whisper-large-v3",
  "transcribe-diarize":      "whisperx",

  "translate":               "nllb-200-3.3b",
  "translate-fast":          "opus-mt",
  "translate-speech":        "seamless-m4t-v2-large",

  "embed":                   "nomic-embed-text",
  "embed-large":             "mxbai-embed-large",

  "math":                    "mathstral:7b-v0.1-q4_K_M",
  "finance":                 "llama3.1:70b-instruct-q4_K_M",

  "document-parse":          "nougat-large",
  "document-ocr":            "got-ocr-2.0",
  "formula-ocr":             "pix2tex",
  "table-qa":                "tapas-large",
  "table-generate":          "tablellama-7b",

  "3d-from-image":           "triposr",
  "3d-from-image-quality":   "instantmesh",
  "3d-from-text":            "shap-e",
  "3d-multiview":            "zero123plus",

  "biomedical":              "openbiollm:70b-q4_K_M",
  "medical":                 "meditron:70b-q4_K_M",
  "biomedical-fast":         "biomistral:7b-q4_K_M",
  "protein-structure":       "esmfold",
  "molecular":               "chemberta"
}
```

Not all entries run via the same backend. Text and embedding models use Ollama. Image generation (Flux.1, ControlNet, IP-Adapter, Real-ESRGAN, SAM2, IC-Light, BRIA RMBG) run via ComfyUI or diffusers. Video (Wan2.1) runs via its own inference stack. Music and audio effects (MusicGen, AudioGen) run via Audiocraft. TTS (Kokoro, Chatterbox, Parler-TTS, XTTS v2, F5-TTS) each run standalone or via a shared TTS server. Transcription (Whisper, Distil-Whisper, WhisperX) runs via faster-whisper or the Whisper Python library. Translation (NLLB-200, Opus-MT, Seamless M4T) runs via HuggingFace Transformers. The registry is backend-agnostic — each capability key maps to a model identifier, and the gateway knows which runner to invoke per entry.

Agents request a capability (`reasoning`, `image`, `tts`, etc.), not a specific model or backend. The registry resolves both. Swapping to a better model later — or pointing `image-fast` at a new Flux variant — means updating one line. No agent code changes.

The entries below are organized by domain:

| Domain | Keys | Notes |
|---|---|---|
| Text — reasoning & execution | `reasoning`, `execution`, `writing`, `extraction`, `classification`, `fast` | Core language pipeline |
| Code | `code`, `code-fast`, `frontend`, `sql`, `svg` | Specialized code models per language/domain |
| Security & compliance | `security`, `compliance` | WhiteRabbitNeo for offensive/defensive security analysis; Granite for compliance and audit reasoning |
| Vision | `vision`, `vision-fast`, `ocr` | Qwen2.5-VL for heavy multimodal tasks; moondream2 for lightweight image understanding |
| Image generation | `image`, `image-fast`, `image-edit`, `image-controlled`, `image-depth`, `image-canny`, `image-prompt-engineer` | Flux.1 family; ControlNet union for structure-constrained generation; depth and canny variants for layout-following generation; prompt engineer refines prompts before generation |
| Design & layout | `design-upscale`, `design-background-remove`, `design-segment`, `design-relight`, `design-style-transfer`, `design-layout-analysis` | Real-ESRGAN for upscaling; BRIA RMBG-2.0 for background removal; SAM2 for precise segmentation and masking; IC-Light for relighting assets consistently; IP-Adapter for style reference transfer; LayoutLMv3 for analysing document and page layouts |
| Video understanding | `video-understand`, `video-understand-fast`, `video-understand-quality`, `video-qa`, `video-long` | Qwen2.5-VL for deep video comprehension; InternVL2 8B for fast batch processing; InternVL2 40B for quality; Video-LLaVA for timestamp-aware QA; LLaMA-VID for hour-long recordings |
| Video generation | `video`, `video-fast`, `video-image-to-video` | Wan2.1 family — text-to-video and image-to-video |
| Music & audio | `music`, `music-fast`, `audio-effects` | MusicGen for composition; AudioGen for sound effects |
| TTS | `tts`, `tts-quality`, `tts-expressive`, `tts-clone`, `tts-multilingual` | Kokoro for fast utility TTS; Chatterbox for ElevenLabs-quality output; Parler-TTS for voice-described generation ("a calm male voice with slight reverb"); XTTS v2 for zero-shot voice cloning from a reference clip; F5-TTS for multilingual cloning |
| Transcription | `transcribe`, `transcribe-fast`, `transcribe-diarize` | Whisper large-v3 for accuracy; Distil-Whisper for speed; WhisperX adds word-level timestamps and speaker diarization |
| Translation | `translate`, `translate-fast`, `translate-speech` | NLLB-200 for 200+ language text translation; Opus-MT for fast language-pair translation; Seamless M4T v2 for multimodal translation — speech-to-text, text-to-speech, and speech-to-speech across 100+ languages |
| Embeddings | `embed`, `embed-large` | Nomic and MXBai for ChromaDB ingestion |
| Math & finance | `math`, `finance` | Mathstral for numerical reasoning; 70B for financial analysis and forecasting |
| Document parsing | `document-parse`, `document-ocr`, `formula-ocr` | Nougat for scientific PDFs with equations; GOT-OCR 2.0 for mixed documents (charts, tables, formulas); pix2tex for formula-image to LaTeX |
| Tables & spreadsheets | `table-qa`, `table-generate` | TAPAS for querying existing tabular data; TableLlama for generating or summarising tables |
| 3D & geometry | `3d-from-image`, `3d-from-image-quality`, `3d-from-text`, `3d-multiview` | TripoSR for fast image-to-mesh; InstantMesh for quality reconstruction; Shap-E for text-to-3D; Zero123++ for multi-view generation |
| Science & biomedical | `biomedical`, `medical`, `biomedical-fast`, `protein-structure`, `molecular` | OpenBioLLM and Meditron for clinical and biomedical reasoning; BioMistral for fast classification; ESMFold for protein structure; ChemBERTa for molecular property prediction |

---

## Specialisation Potential

Because the switching mechanism is model-agnostic, the same trait supports both generalist base models and narrow specialist fine-tunes. Examples of hypothetical specialist models that could be slotted in:

| Capability key | Specialist | Description |
|---|---|---|
| `procurement-extraction` | Fine-tuned Mistral 7B | Extracts contacts, process steps, and requirements from procurement pages |
| `compliance-classification` | Fine-tuned Granite 8B | Classifies content against a specific regulatory framework (GDPR, EU AI Act, sector) |
| `brief-writing` | Fine-tuned Phi-4 | Produces structured executive briefs in the Office's exact house format |
| `task-decomposition` | Fine-tuned Llama 3.1 8B | Breaks goals into DAG-structured task lists in the Office's task schema |
| `contract-analysis` | Fine-tuned Mistral 7B | Extracts clauses, obligations, and risk flags from legal contracts |
| `signal-classification` | Fine-tuned Mistral 7B | Classifies inbound signals against client-specific relevance taxonomies |
| `brand-voice` | Fine-tuned Phi-4 | Writes in a specific client's brand voice and tone — trained on their published material |
| `svg-generation` | Fine-tuned StarCoder2 7B | Generates clean, structured SVG from natural language descriptions |
| `security-audit` | Fine-tuned WhiteRabbitNeo | Analyses code or system configs against a defined security policy |

Training these specialists is a later-stage concern. The switching architecture works with base models from day one. The specialist slots are filled over time as training data accumulates from production use — every task the Office executes is potential training signal for the specialist that runs next.

---

## Runtime Fragment

- You know your own model and its capability profile
- You know which models are available and what they are best at
- When you complete a phase and the next phase requires a materially different capability, you switch — you do not push on with the wrong tool
- Before switching: write a full checkpoint. Assume the next instance knows nothing except what you write in that file
- On startup: if a checkpoint is present, read it before generating a single token. State your understanding of the current task state before proceeding
- You do not switch for trivial transitions — the swap cost is real and must be earned by a real capability difference
- You log every switch with the phase boundary and model pair
