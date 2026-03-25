# The Model Catalogue

Every model the Office has access to, organized by what it does. This is the full buffet — text, code, vision, image, video, music, voice, transcription, translation, design, security, embeddings. All local, all sovereign, all running on the Mac Studio M5 Ultra.

For technical architecture and training strategy, see [language-models.md](language-models.md). For how agents switch between models mid-task, see [traits/agnostic.md](../../traits/agnostic.md). For why everything runs locally, see [local-ai.md](local-ai.md).

---

## Text — Reasoning & Language

The cognitive core of the Office. These models think, plan, write, extract, and classify.

---

### DeepSeek-R1 671B
**Role in Office:** CEO — strategic reasoning, goal decomposition, final quality gate
**Runner:** Ollama · **VRAM:** ~230GB (4-bit) · **Context:** 128K tokens

The strongest open reasoning model available. Trained entirely on verifiable mathematical and coding tasks using RLVR (Reinforcement Learning with Verifiable Rewards) — the result is a model that shows its work, reasons step by step, and does not confabulate. Where most models generate a plausible-sounding answer, R1 works through the problem. Chain-of-thought is not a prompt technique here — it is baked into the weights.

For the Office CEO: this is the right model for goal decomposition into dependency-aware task DAGs, conflict resolution between departments, and any decision that requires holding multiple competing hypotheses simultaneously before committing.

---

### Llama 3.1 70B (Meta)
**Role in Office:** COO, CMO — domain execution, task orchestration, strategy translation
**Runner:** Ollama · **VRAM:** ~40GB (4-bit) · **Context:** 128K tokens

Meta's most capable openly licensed model. GPT-4 class on most benchmarks. Instruction-following is clean, JSON output is reliable, and it handles long contexts without significant degradation. Apache 2.0 licensed — no usage restrictions.

The sweet spot for the specialist tier: capable enough to translate strategic directives into structured task plans, fast enough to run continuously as the COO's operational backbone, small enough to fit alongside other models in memory.

---

### Llama 3.1 405B (Meta)
**Role in Office:** CEO fallback / heavy reasoning tasks
**Runner:** Ollama · **VRAM:** ~230GB (4-bit) · **Context:** 128K tokens

The largest openly licensed model Meta has released. On broad capability benchmarks it sits between GPT-4 and GPT-4o. Where DeepSeek-R1 wins on structured reasoning tasks, Llama 405B has broader world knowledge and stronger prose generation. The two are complementary: R1 for chains of reasoning, 405B for synthesis and strategic narrative.

---

### Phi-4 14B (Microsoft)
**Role in Office:** Executive Briefer — structured writing, summarisation, instruction-following
**Runner:** Ollama · **VRAM:** ~9GB (4-bit) · **Context:** 16K tokens

A small model that consistently punches above its weight on writing and instruction-following tasks. Microsoft trained it on carefully curated synthetic data rather than raw web text — the result is unusually clean, precise output for its size. The Executive Briefer uses this model because the task is well-defined (take structured inputs, produce a formatted brief) and Phi-4 executes it reliably without the overhead of a 70B model.

Also a strong candidate for any fine-tuning work: at 14B it is small enough to QLoRA fine-tune on Apple Silicon via MLX, which makes it the right base for an Office-specific brief-writing specialist.

---

### Mistral 7B v0.3 (Mistral AI)
**Role in Office:** Digital Archivist, classification tasks, extraction tasks
**Runner:** Ollama · **VRAM:** ~5GB (4-bit) · **Context:** 32K tokens

Fast, reliable, and small. Not for complex reasoning — for narrow, well-defined tasks where the output schema is fixed and the input is structured. Classification, extraction, tagging, summarisation of individual documents. Runs in ~5GB, which means multiple instances can run in parallel without pressuring the memory budget.

European origin, multilingual capable. Mistral AI is a French company; the model has noticeably stronger French, German, and Italian performance than US-trained models of comparable size.

---

### Llama 3.1 8B (Meta)
**Role in Office:** Signal Scout, fast utility tasks
**Runner:** Ollama · **VRAM:** ~5GB (4-bit) · **Context:** 128K tokens

The workhorse of the worker tier. Same architecture lineage as the 70B but at a fraction of the cost. Long context window (128K) is genuinely useful for Signal Scout's feed-scanning workload — it can hold a full batch of RSS entries in context and filter by relevance in a single pass. Spawnable in under 3 seconds, tears down cleanly, leaves nothing behind.

---

### Qwen 2.5 72B (Alibaba)
**Role in Office:** Heavy specialist tasks, strong multilingual execution
**Runner:** Ollama · **VRAM:** ~42GB (4-bit) · **Context:** 128K tokens

Alibaba's flagship. Benchmark performance comparable to Llama 3.1 70B with notably stronger multilingual capability — Chinese, Japanese, Korean, Arabic in particular. Strong structured output discipline. A solid alternative to Llama 70B for any Office deployment that handles non-English source material at volume.

---

### Mathstral 7B (Mistral AI)
**Role in Office:** Math-heavy reasoning, financial calculation, quantitative analysis
**Runner:** Ollama · **VRAM:** ~5GB (4-bit) · **Context:** 32K tokens

A Mistral 7B fine-tuned specifically on mathematical reasoning. Outperforms the base model significantly on numerical tasks — not because it knows more facts, but because it has been trained to reason through calculation steps rather than pattern-match to a plausible number. Use this when the CFO needs to run numerical projections or when a task requires verifiable arithmetic chains.

---

## Code

Models that write, review, and reason about software.

---

### Qwen 2.5 Coder 32B (Alibaba)
**Role in Office:** CTO, DOE — complex code, architecture, security audits
**Runner:** Ollama · **VRAM:** ~20GB (4-bit) · **Context:** 128K tokens

The strongest open code model available by most benchmarks. Outperforms GPT-4o on HumanEval and similar coding benchmarks. Trained specifically on code rather than code-as-a-subset-of-general-training. Handles architecture-level reasoning, multi-file context, and refactoring with a consistency that general models do not match.

The CTO and DOE run on this. When the Office is writing or reviewing software, this is the model doing the work.

---

### Qwen 2.5 Coder 7B (Alibaba)
**Role in Office:** Fast code tasks, boilerplate, formatting
**Runner:** Ollama · **VRAM:** ~5GB (4-bit) · **Context:** 128K tokens

The smaller sibling. Loses to the 32B on complex architecture tasks but matches it on narrow, well-defined coding tasks: write a function with this signature, convert this JSON schema, generate a regex for this pattern. Spawnable quickly, cheap to run. Use it when the task is too mechanical to justify 32B but too code-specific for a general 7B model.

---

### StarCoder2 15B (Hugging Face / ServiceNow)
**Role in Office:** Frontend development, HTML/CSS/JS, SVG generation
**Runner:** Ollama · **VRAM:** ~9GB (4-bit) · **Context:** 16K tokens

Trained on 600+ programming languages with particularly strong coverage of frontend technologies — HTML, CSS, JavaScript, TypeScript, React, Vue. StarCoder2 has seen more SVG in training than most models: its spatial reasoning about SVG paths, transforms, and viewBox geometry is noticeably better than general code models.

The natural choice when the CCO needs code-generated design assets, the DOE needs frontend scaffolding, or any task requires structured XML-like output where the syntax is as important as the content.

---

### StarCoder2 7B (Hugging Face / ServiceNow)
**Role in Office:** SVG generation, lightweight frontend tasks
**Runner:** Ollama · **VRAM:** ~5GB (4-bit) · **Context:** 16K tokens

Same training lineage as the 15B, at half the footprint. For SVG specifically — icons, diagrams, simple illustrations — the 7B is often sufficient. SVG generation is a narrow, structured task; the benefit of the larger model only appears on complex, multi-element compositions.

---

### SQLCoder 7B (Defog AI)
**Role in Office:** SQL generation, database queries, data retrieval
**Runner:** Ollama · **VRAM:** ~5GB (4-bit) · **Context:** 8K tokens

A Mistral 7B fine-tuned entirely on text-to-SQL tasks across dozens of database schemas. It does one thing: takes a natural language question and a schema description and returns a syntactically correct SQL query. Outperforms GPT-4 on text-to-SQL benchmarks. When the CAO or Digital Archivist needs to query structured data, this is cleaner than asking a general model to write SQL.

---

### WhiteRabbitNeo R1 32B (WhiteRabbitNeo)
**Role in Office:** Security analysis, penetration test reasoning, vulnerability assessment
**Runner:** Ollama · **VRAM:** ~20GB (4-bit) · **Context:** 32K tokens

A model fine-tuned specifically for cybersecurity — both offensive and defensive. Trained on security research, CVE databases, penetration testing methodology, and secure code review. Understands attack vectors, can reason about system configurations from a security perspective, and produces actionable findings rather than generic warnings.

The Compliance Watchdog and CTO use this for code security audits, infrastructure review, and threat modelling. Not a replacement for human security review — a force multiplier for it.

---

### IBM Granite 3.1 Dense 8B
**Role in Office:** Compliance classification, regulatory reasoning, audit trail analysis
**Runner:** Ollama · **VRAM:** ~5GB (4-bit) · **Context:** 128K tokens

IBM's enterprise-focused model, trained with particular attention to compliance, governance, and structured reasoning about rules and regulations. Performs well on tasks that require mapping content against defined frameworks (GDPR, EU AI Act, ISO standards) and producing structured findings rather than prose summaries.

The Compliance Watchdog uses this. It is not the smartest model on the list — it is the most disciplined about applying rules consistently.

---

## Vision & Multimodal

Models that see, read, and understand images and documents.

---

### Qwen2.5-VL 72B (Alibaba)
**Role in Office:** Heavy visual analysis, document understanding, multimodal research
**Runner:** Ollama · **VRAM:** ~42GB (4-bit) · **Context:** 128K tokens

The most capable open vision-language model. Give it an image, a document scan, a screenshot, a chart, a diagram — it reads and reasons about it. Strong enough to extract structured data from complex tables, understand the hierarchy of a page layout, and describe spatial relationships in detailed images. The CAO uses this for research tasks that involve visual source material.

---

### Qwen2.5-VL 7B (Alibaba)
**Role in Office:** OCR, fast visual extraction, document parsing
**Runner:** Ollama · **VRAM:** ~5GB (4-bit) · **Context:** 32K tokens

The lightweight vision model. Same architecture, smaller weights. Loses to the 72B on complex reasoning tasks involving images, but holds up well on OCR and structured extraction from clean documents. Considerably faster and cheaper per inference. The right tool when the task is "read this invoice and return the line items as JSON," not "analyse what this chart implies about market trends."

---

### Moondream2 (Vikhyatk)
**Role in Office:** Lightweight image understanding, caption generation, quick visual checks
**Runner:** Ollama · **VRAM:** ~2GB · **Context:** 2K tokens

Tiny and fast. 2GB footprint, sub-second response times. Not for complex reasoning — for answering simple questions about images at high volume: "does this image contain a person?", "what is the dominant colour?", "is this a product photo or a lifestyle shot?" The Media Assembly Line uses this for quick quality checks on generated assets before passing them to the CCO.

---

### LLaVA 1.6 34B (Haotian Liu / Microsoft)
**Role in Office:** Visual reasoning, alternative to Qwen-VL for specific tasks
**Runner:** Ollama · **VRAM:** ~20GB (4-bit) · **Context:** 4K tokens

An established vision-language model with a strong track record. Slightly less capable than Qwen2.5-VL on recent benchmarks but with a larger community of fine-tunes and adapters. Worth keeping as a fallback and for tasks where fine-tuned LLaVA variants exist for a specific domain (medical imaging, satellite imagery, technical diagrams).

---

## Image Generation

The CCO and Media Assembly Line's primary output tools. All run via ComfyUI or diffusers on the Mac Studio GPU.

---

### Flux.1 [dev] (Black Forest Labs)
**Role in Office:** Primary image generation — quality output
**Runner:** ComfyUI / diffusers · **VRAM:** ~24GB

The current gold standard for open-source image generation. Significantly better than Stable Diffusion XL on prompt adherence, text rendering within images, and photorealistic detail. Slower than Schnell but produces images that genuinely look like they came from a professional creative pipeline.

The CCO uses Flux.1 [dev] for campaign assets, brand imagery, and anything that will be seen by a client.

---

### Flux.1 [schnell] (Black Forest Labs)
**Role in Office:** Fast iteration, concept generation, Media Assembly Line volume output
**Runner:** ComfyUI / diffusers · **VRAM:** ~24GB

Flux at speed. Four inference steps instead of twenty. Quality is lower than [dev] but the gap has narrowed with distillation improvements. For generating ten variations of a concept to present to the CCO for selection, Schnell is the right tool — you want volume and speed, not the final polished output.

---

### Flux.1 Fill (Black Forest Labs)
**Role in Office:** Image editing, inpainting, extending compositions
**Runner:** ComfyUI / diffusers · **VRAM:** ~24GB

Takes an image and a mask and regenerates only the masked area, conditioned on the surrounding context. The cleanest inpainting model available. Used when an existing asset needs elements added, removed, or replaced without regenerating the whole image. Pairs with SAM2 for mask generation: SAM2 selects the object, Fill replaces it.

---

### Flux.1 ControlNet Union (Black Forest Labs / community)
**Role in Office:** Structure-constrained generation, layout-following image creation
**Runner:** ComfyUI · **VRAM:** ~28GB

ControlNet adds structural guidance to Flux generation: give it a pose, a depth map, a line drawing, or a wireframe, and the generated image follows that structure while Flux handles the aesthetic. Union refers to a single model that handles multiple control types (pose, depth, canny, normal, segment) rather than needing a separate ControlNet per type.

This is how the CCO generates images that must fit a specific layout — a product shot in a defined spatial composition, a person in a precise pose, a scene that matches an existing background.

---

### Flux.1 Depth (Black Forest Labs)
**Role in Office:** Depth-guided generation, spatial consistency across assets
**Runner:** ComfyUI · **VRAM:** ~28GB

Generates images conditioned on a depth map extracted from a reference image. Preserves the three-dimensional spatial structure of the reference while allowing full creative freedom in style, lighting, and content. Useful for maintaining spatial consistency across a set of images — a product in the same scene geometry but different styles, for example.

---

### Flux.1 Canny (Black Forest Labs)
**Role in Office:** Edge-guided generation, brand-consistent visual derivatives
**Runner:** ComfyUI · **VRAM:** ~28GB

Generates images that follow the edge structure of a reference image. The output respects every major contour of the input while generating entirely new content. Use this when you need a new image that is clearly "the same thing" as an existing asset but rendered differently — a logo illustration that maintains shape while changing style, a product silhouette that becomes a painting.

---

## Design & Post-Production

Models that process, enhance, and manipulate existing visual assets. Not generators — operators.

---

### Real-ESRGAN x4+ (xinntao)
**Role in Office:** Asset upscaling, resolution enhancement
**Runner:** standalone / ComfyUI

Takes any image and upscales it 4× with AI-generated detail, not bicubic interpolation. The difference is visible: Real-ESRGAN adds realistic texture and sharpness where a standard upscaler adds blur. Essential for taking a Flux.1 Schnell draft (fast, lower resolution) and preparing it for print or large-format digital use.

---

### BRIA RMBG 2.0 (BRIA AI)
**Role in Office:** Background removal for product shots, portraits, brand assets
**Runner:** standalone / ComfyUI

State-of-the-art background removal. Handles complex edges — hair, fur, transparent objects, fine detail — that earlier models like rembg struggled with. Fully local, no API, processes in under a second per image. The Media Assembly Line uses this to isolate subjects from generated backgrounds before compositing into campaign layouts.

---

### SAM2 Large (Meta)
**Role in Office:** Precise image and video segmentation, mask generation
**Runner:** standalone / ComfyUI

Segment Anything Model 2 — point at any object in any image or video frame and SAM2 produces a precise mask around it. The mask feeds into Fill for inpainting, into ControlNet for structure extraction, or into compositing pipelines for isolation. Also handles video: track an object across frames and maintain a consistent mask throughout.

---

### IC-Light (lllyasviel)
**Role in Office:** Relighting, lighting consistency across asset batches
**Runner:** ComfyUI

Takes a foreground subject (typically a product or portrait with background removed) and applies a new lighting environment to it. Produce a set of product shots with consistent studio lighting regardless of when or how the source images were generated. Particularly useful for the Media Assembly Line when building a campaign that needs visual coherence across many assets.

---

### IP-Adapter Flux (Tencent / community)
**Role in Office:** Style reference transfer, brand consistency
**Runner:** ComfyUI

Takes a reference image and uses it to condition the style of new Flux generations — without fine-tuning. The new generation inherits colour palette, mood, texture, and visual language from the reference. The CCO uses this to maintain brand visual consistency across generated assets: give it a hero brand image and generate new assets that unmistakably belong to the same family.

---

### LayoutLMv3 Large (Microsoft)
**Role in Office:** Document layout analysis, structured document understanding
**Runner:** HuggingFace Transformers

A model specifically trained to understand the spatial layout of documents — not just the text, but the relationship between text blocks, images, tables, and headers on a page. Used when the CAO or Signal Scout is processing competitor materials, PDFs, or printed collateral and needs to extract not just text but structured understanding of the page's intent and hierarchy.

---

## Video Understanding & Analysis

Models that *watch* video — transcribing speech, reading on-screen content, and reasoning about what is visually happening across frames. The counterpart to video generation: ingestion and comprehension rather than output.

The typical pipeline for learning from a video source (YouTube, lecture recordings, screen captures):

```
yt-dlp → download video
    → Whisper / WhisperX → transcribe audio + speaker diarization
    → Qwen2.5-VL / InternVL2 → understand visual content frame by frame
    → CAO / Digital Archivist → embed and store to ChromaDB
```

The transcript gives you what was said. The video understanding model gives you what was shown — slides, code, diagrams, demonstrations, on-screen text — which is often where the actual knowledge lives.

---

### Qwen2.5-VL 72B — Video Mode (Alibaba)
**Role in Office:** Deep video comprehension, lecture and tutorial analysis
**Runner:** Ollama · **VRAM:** ~42GB (4-bit) · **Context:** 128K tokens

Already listed under Vision, but Qwen2.5-VL natively accepts video input — not just images. Feed it a video file and it reasons across the full temporal sequence: what changed between frames, what the presenter pointed at, what appeared on screen at a given timestamp. For long-form educational content (conference talks, technical tutorials, course lectures), it produces structured summaries that combine the spoken content with the visual demonstrations in a way audio transcription alone cannot.

The CAO uses this to ingest video research material — turning hours of conference recordings into queryable knowledge in ChromaDB.

---

### InternVL2 8B (Shanghai AI Lab)
**Role in Office:** Fast video understanding, screen recording analysis, slide decks
**Runner:** Ollama / HuggingFace · **VRAM:** ~6GB (4-bit) · **Context:** 8K tokens

A compact but capable vision-language model with strong video comprehension. At 8B it is fast enough to process video at scale — the right choice when the CAO is processing a batch of recordings rather than a single high-value video. Particularly strong on structured visual content: slide decks, terminal output, code on screen, diagrams. What appears visually in a technical tutorial is often more information-dense than the narration; InternVL2 reads both.

---

### InternVL2 40B (Shanghai AI Lab)
**Role in Office:** High-quality video analysis, complex multi-scene understanding
**Runner:** HuggingFace · **VRAM:** ~24GB (4-bit) · **Context:** 32K tokens

The larger InternVL2 variant for when video comprehension quality matters more than throughput. Handles longer videos with more scene changes more coherently than the 8B. Use this for high-value source material — a keynote from a domain expert, a detailed technical walkthrough, a recorded client presentation — where the quality of comprehension justifies the extra compute.

---

### Video-LLaVA (PKU-YuanLab)
**Role in Office:** Video question answering, timestamp-aware retrieval
**Runner:** HuggingFace · **VRAM:** ~14GB · **Context:** 4K tokens

Specifically trained on video QA tasks — "what is the presenter doing at the 4-minute mark?", "when does the diagram first appear?", "summarise the third section of this lecture." Where Qwen2.5-VL is a general vision model that happens to handle video well, Video-LLaVA is purpose-built for video comprehension tasks. Strong on temporal reasoning and explicit timestamp-based queries.

---

### LLaMA-VID (CUHK / Microsoft)
**Role in Office:** Long-video understanding — hour-long recordings
**Runner:** HuggingFace · **VRAM:** ~14GB · **Context:** variable

Most video understanding models struggle past a few minutes because the frame count exceeds the context window. LLaMA-VID compresses each video frame into two tokens, allowing it to process hour-long videos within a standard context budget. The compression is lossy but the temporal coherence across the full video is preserved. Use this when the source material is long — a two-hour conference recording, a full course module — and other models would need to be chunked and stitched.

---

## Video Generation

The Office can produce video from text or image references, entirely locally.

---

### Wan2.1 T2V 14B (Wanvideo / Alibaba)
**Role in Office:** Primary text-to-video generation
**Runner:** Wan2.1 inference stack · **VRAM:** ~22GB

The leading open-source text-to-video model as of early 2026. Produces 720p video up to ~10 seconds from a text prompt. Motion is coherent, subjects maintain consistency across frames, and the output genuinely looks like produced video rather than interpolated stills. The Media Assembly Line uses this for social content, product demos, and video ad concepts that the CCO then reviews and selects from.

---

### Wan2.1 T2V 1.3B (Wanvideo / Alibaba)
**Role in Office:** Fast video iteration, concept generation
**Runner:** Wan2.1 inference stack · **VRAM:** ~4GB

Lightweight sibling. Much faster, much lower quality — but adequate for generating ten rough video concepts in the time it takes the 14B to produce one. Use it to iterate on direction and narrative before committing to a quality render.

---

### Wan2.1 I2V 14B (Wanvideo / Alibaba)
**Role in Office:** Image-to-video — animating still assets
**Runner:** Wan2.1 inference stack · **VRAM:** ~22GB

Takes a still image and animates it according to a text prompt. The starting frame is your image; the model generates plausible motion forward from it. A product photo becomes a product reveal. A brand illustration becomes an animated logo. A portrait becomes a talking head. The I2V variant preserves the visual identity of the source image in a way that pure T2V cannot.

---

## Music & Audio

The Office can generate original music, sound effects, and spoken audio — all locally.

---

### MusicGen Large (Meta / Audiocraft)
**Role in Office:** Original music composition for campaigns, content, presentations
**Runner:** Audiocraft · **VRAM:** ~6GB

Meta's text-to-music model. Describe what you want — "upbeat electronic track with a 120bpm rhythm and a sense of forward momentum, no vocals" — and MusicGen produces an original audio clip. Also takes an existing audio clip as a continuation reference. Output is royalty-free by default since it is generated, not sampled.

The CMO and CCO use this for campaign audio, background music for video assets, and presentation soundscapes. Not a replacement for a professional composer on hero work — ideal for everything below that threshold.

---

### MusicGen Small (Meta / Audiocraft)
**Role in Office:** Fast music generation, iteration on musical direction
**Runner:** Audiocraft · **VRAM:** ~2GB

Smaller, faster, less expressive. The right model for quickly generating five variations of a musical direction to present for selection — the final production can then run on Large.

---

### AudioGen Medium (Meta / Audiocraft)
**Role in Office:** Sound effect generation, ambient audio, UI audio
**Runner:** Audiocraft · **VRAM:** ~3GB

Generates non-musical audio from text descriptions: "the sound of rain on a metal roof," "a notification chime, soft and clear," "city ambience with distant traffic." Not music — sounds. The Media Assembly Line uses this to generate audio assets for video content, app interfaces, or presentation environments.

---

## Voice — Text-to-Speech

The Office has a full TTS stack ranging from fast utility voice to ElevenLabs-quality expressive synthesis.

---

### Kokoro 82M
**Role in Office:** Fast utility TTS — agent voice output, internal briefings
**Runner:** standalone · **VRAM:** ~1GB

Tiny and extremely fast. 82 million parameters, sub-100ms latency on Apple Silicon. Not the most expressive voice on the list — the most efficient. Use it for agent status readouts, internal briefing audio, quick voice previews. The Executive Briefer can use Kokoro to deliver its morning brief as audio rather than text.

---

### Chatterbox (Resemble AI)
**Role in Office:** High-quality expressive TTS, client-facing voice output
**Runner:** standalone · **VRAM:** ~4GB

Resemble AI's open-source model, released 2025, built explicitly to compete with ElevenLabs. The output is genuinely good — natural prosody, emotional range, no robotic cadence. The model responds to emotion tags in the input, allowing the CMO to specify not just what is said but how it sounds: confident, warm, urgent, authoritative.

For any Office output that a human will actually listen to — client presentations, video voiceovers, audio briefs — Chatterbox is the default.

---

### Parler-TTS Large v1 (Hugging Face)
**Role in Office:** Voice-described synthesis, custom voice generation without cloning
**Runner:** standalone · **VRAM:** ~6GB

A unique approach: rather than selecting a voice from a menu, you *describe* the voice you want in natural language. "A deep male voice with slight warmth, calm delivery, minimal reverb, recorded in a quiet studio." The model generates speech matching that description. No reference clip needed.

Useful when the Office needs a voice that fits a specific brand or character brief — describe the voice the way you would brief a casting director.

---

### XTTS v2 (Coqui AI)
**Role in Office:** Zero-shot voice cloning, consistent character voice generation
**Runner:** standalone · **VRAM:** ~3GB

Provide a six-second reference audio clip and XTTS v2 will clone that voice and speak any text in it — in 17 languages. The clone is good enough for most production uses. The CCO uses this when a client wants AI-generated audio in a consistent recognisable voice without an actor contract — record a short reference, clone it, generate unlimited content.

---

### F5-TTS
**Role in Office:** Multilingual voice cloning, cross-lingual content
**Runner:** standalone · **VRAM:** ~4GB

Zero-shot voice cloning with a strong emphasis on multilingual fidelity. Where XTTS v2 can produce accented output in non-native languages, F5-TTS maintains the cloned voice characteristics more consistently across language boundaries. For an Office client doing multilingual campaigns with a consistent brand voice, F5-TTS handles the language switching more naturally.

---

## Transcription

The Office can transcribe any audio — meetings, calls, interviews, video — to text, locally.

---

### Whisper Large-v3 (OpenAI)
**Role in Office:** Accurate transcription of meetings, calls, interviews, video
**Runner:** faster-whisper · **VRAM:** ~3GB

The gold standard for local speech-to-text. Over 99 languages supported. Word error rate competitive with cloud transcription services on clean audio. Runs via faster-whisper (a CTranslate2 reimplementation), which is 4× faster than the original Whisper library on the same hardware.

The Triage Coordinator uses Whisper to transcribe inbound audio messages. The CAO uses it to extract text from video research material. Any audio that needs to become searchable, storable text goes through Whisper.

---

### Distil-Whisper Large-v3 (Hugging Face)
**Role in Office:** Fast transcription, real-time or near-real-time use cases
**Runner:** faster-whisper · **VRAM:** ~1.5GB

A distilled version of Whisper large-v3: 6× faster, 49% fewer parameters, less than 1% WER degradation on clean audio. For high-volume transcription tasks — processing fifty meeting recordings overnight — Distil-Whisper is the right choice. The quality difference is not perceptible on clean audio; it only appears on degraded or heavily accented input.

---

### WhisperX
**Role in Office:** Transcription with speaker diarization and word-level timestamps
**Runner:** standalone · **VRAM:** ~3GB + pyannote

WhisperX wraps Whisper with two additions: **word-level timestamps** (every word knows when it started and ended) and **speaker diarization** (who said what). Feed it a recorded team meeting and get back a transcript that looks like a screenplay — each line attributed to the right speaker at the right time. The Digital Archivist uses this for meeting records; the Triage Coordinator uses it to attribute inbound audio to the right contact.

---

## Translation

The Office handles translation natively — 200+ languages, text and speech.

---

### NLLB-200 3.3B (Meta)
**Role in Office:** Primary text translation, 200+ languages
**Runner:** HuggingFace Transformers · **VRAM:** ~7GB

No Language Left Behind — Meta's multilingual translation model covering 200 languages, including many low-resource languages that Google Translate handles poorly. Quality on major European languages (EN, FR, DE, ES, IT, SV, NL, PL) is strong. Quality on less-resourced languages is best-in-class for an open model.

The Signal Scout uses this to translate source material before analysis. The CAO uses it for multilingual research. Any task involving non-English source material routes through NLLB.

---

### Opus-MT (Helsinki NLP)
**Role in Office:** Fast translation, language-pair specific high-quality output
**Runner:** HuggingFace Transformers · **VRAM:** ~0.3GB per pair

Hundreds of small, specialized translation models — one per language pair. Each model is trained specifically on EN→SV, EN→DE, FR→EN, etc. rather than trying to handle all languages at once. The tradeoff: narrower coverage but faster inference and often higher quality on the specific pair it was trained for. At 300MB per model, multiple pairs can be loaded simultaneously without memory pressure.

Use Opus-MT when you know the language pair and need fast throughput. Use NLLB when the language is unusual or the source language is unknown.

---

### Seamless M4T v2 Large (Meta)
**Role in Office:** Multimodal translation — speech to text, text to speech, speech to speech
**Runner:** HuggingFace Transformers · **VRAM:** ~10GB

Meta's multimodal translation model. A single model that handles all four translation modalities: speech-to-text, text-to-text, text-to-speech, and speech-to-speech — across 100+ languages. The distinctive capability is speech-to-speech: take a spoken statement in Swedish, output the same statement spoken naturally in German, no intermediate text.

For Office clients doing international presentations or multilingual media: generate the content once in one language and let Seamless produce the other-language audio versions.

---

## Embeddings

Not generative — these models convert text into vectors that ChromaDB stores and retrieves. The foundation of the Office's long-term memory.

---

### Nomic Embed Text (Nomic AI)
**Role in Office:** Primary embedding model for ChromaDB
**Runner:** Ollama · **VRAM:** ~0.3GB · **Dimensions:** 768

Fast, small, and performant on retrieval benchmarks. Handles documents up to 8,192 tokens — long enough for full task outputs, research summaries, and brief sections to be embedded as single units rather than split into chunks. The Digital Archivist uses this to embed everything it stores.

---

### MXBai Embed Large v1 (MixedBread AI)
**Role in Office:** High-quality embeddings for precision retrieval tasks
**Runner:** Ollama · **VRAM:** ~0.5GB · **Dimensions:** 1024

Higher dimensional embeddings than Nomic — better at capturing nuanced semantic relationships, at the cost of slightly larger vector storage. Use this when retrieval precision matters more than speed: legal document search, compliance clause matching, finding the most semantically similar prior task to a new input.

---

## Document Parsing & PDF Intelligence

Models that extract structured knowledge from PDFs, scientific papers, and complex documents — not just raw text.

---

### Nougat Large (Meta)
**Role in Office:** Scientific PDF parsing — research ingestion for the CAO
**Runner:** standalone / HuggingFace · **VRAM:** ~4GB

Scientific papers are not plain text. They contain equations in LaTeX, tables with complex spanning cells, figures with captions, and hierarchical section structures that a standard PDF reader destroys on extraction. Nougat converts scientific PDFs directly to structured markdown, preserving mathematical notation in LaTeX, maintaining table structure, and correctly attributing figure captions.

The CAO uses Nougat as the first step when ingesting research papers, technical reports, or any PDF that contains structured knowledge beyond prose. The output is markdown that the Digital Archivist can meaningfully embed and the CEO can actually reason over.

---

### GOT-OCR 2.0 (University of Hong Kong)
**Role in Office:** Universal document OCR — formulas, tables, charts, molecular structures
**Runner:** standalone / HuggingFace · **VRAM:** ~3GB

A single model that handles every type of content found in real documents: plain text, mathematical formulas, tables, bar charts, music scores, and even molecular structure diagrams — in one pass. Where traditional OCR pipelines need a separate model for each content type, GOT-OCR handles them all with a unified architecture.

Useful wherever the document is visually complex: financial reports with embedded charts, legal contracts with structured tables, technical specifications with diagrams. Pairs with Nougat for a complete document ingestion pipeline — Nougat for scientific papers, GOT-OCR for everything else.

---

### pix2tex / LaTeX-OCR (Lukas Blecher)
**Role in Office:** Formula extraction — convert equation images to LaTeX
**Runner:** standalone · **VRAM:** ~1GB

Takes an image of a mathematical formula — from a textbook, a paper scan, a screenshot — and outputs valid LaTeX. Fast, small, accurate on standard mathematical notation. The CAO uses this when processing source material that contains embedded formulas that Nougat or GOT-OCR have not cleanly captured. Output feeds directly into the Digital Archivist as structured, searchable, renderable notation.

---

## Tables & Spreadsheets

Models that understand, query, and reason over tabular data.

---

### TAPAS Large (Google)
**Role in Office:** Table question answering, spreadsheet reasoning
**Runner:** HuggingFace Transformers · **VRAM:** ~1.5GB

A BERT-based model trained specifically to understand tabular data as tables — not as serialized text. Ask it a question about a table ("what was the highest revenue quarter?", "which product had the lowest margin?") and it reasons over the table structure rather than treating the data as a flat string. Significantly more reliable than asking a general language model to answer questions about pasted CSV data.

The CFO uses TAPAS for structured queries against financial data tables. The CAO uses it for extracting insights from research datasets. Any task that involves answering questions about rows and columns rather than prose routes through TAPAS.

---

### TableLlama (OSU NLP)
**Role in Office:** Table generation, structured data synthesis
**Runner:** HuggingFace Transformers · **VRAM:** ~5GB

A Llama fine-tuned on table-centric tasks: generating tables from natural language descriptions, completing partial tables, and performing table-to-text summarisation. Where TAPAS answers questions *about* existing tables, TableLlama *creates* tables from instructions. The Executive Briefer uses this to produce structured summary tables from unstructured research findings.

---

## 3D & Geometry

The Office can generate and reconstruct three-dimensional assets locally — from text descriptions or single images.

---

### TripoSR (Tripo AI / Stability AI)
**Role in Office:** Image-to-3D mesh generation — product visualisation, spatial assets
**Runner:** standalone / diffusers · **VRAM:** ~8GB

Feed it a single photograph of an object and TripoSR produces a textured 3D mesh in under a second on a modern GPU. The quality is not production-ready for AAA game assets, but it is absolutely ready for product visualisation, spatial planning, and creative exploration. A client photographs their product on a plain background; TripoSR produces a rotatable 3D model in seconds.

The CCO uses TripoSR to generate spatial assets for product presentations, AR-ready previews, and design iteration. No 3D modelling software or expertise required.

---

### Shap-E (OpenAI)
**Role in Office:** Text-to-3D and image-to-3D generation
**Runner:** standalone / diffusers · **VRAM:** ~6GB

OpenAI's 3D generation model, fully open weights. Takes a text description ("a wooden chair with curved legs") or an image and generates a 3D implicit function that can be rendered as a mesh or a NeRF. Slower than TripoSR and lower geometric detail, but stronger at generating objects from text descriptions — where TripoSR needs a real photograph, Shap-E can work from imagination.

---

### InstantMesh (Tencent)
**Role in Office:** High-quality image-to-3D reconstruction
**Runner:** standalone / diffusers · **VRAM:** ~16GB

A more capable image-to-3D pipeline than TripoSR: it generates multi-view images of the object first, then reconstructs a clean mesh from those views. The output geometry is more accurate and the texture quality is higher — at the cost of more compute and time. Use TripoSR for fast iteration, InstantMesh for final-quality 3D assets that will appear in client deliverables.

---

### Zero123++ (Sudo AI)
**Role in Office:** Multi-view generation — 3D exploration from a single image
**Runner:** ComfyUI / diffusers · **VRAM:** ~8GB

Takes a single image and generates six consistent views of the same object from different angles. Not a final 3D model — a consistent multi-view set that feeds into a reconstruction pipeline (InstantMesh, TripoSR) or stands alone as a multi-angle product presentation. The CCO uses this to generate product photography from multiple angles when only one reference shot exists.

---

## Science & Biomedical

Domain-specific models for research-heavy Office deployments in healthcare, life sciences, and academic research.

---

### OpenBioLLM 70B (Saama AI)
**Role in Office:** Biomedical reasoning, clinical literature analysis
**Runner:** Ollama · **VRAM:** ~42GB (4-bit) · **Context:** 128K tokens

A Llama fine-tuned on a comprehensive biomedical corpus: PubMed abstracts, clinical notes, medical textbooks, and biomedical benchmarks. Outperforms GPT-4 on several medical QA benchmarks including MedQA and PubMedQA. For an Office serving healthcare or life sciences clients, this replaces the general 70B for any domain task — the specialisation produces measurably better output on clinical and biomedical questions.

---

### Meditron 70B (EPFL)
**Role in Office:** Clinical guidelines, medical decision support
**Runner:** Ollama · **VRAM:** ~42GB (4-bit) · **Context:** 4K tokens

EPFL's medical model, trained specifically on clinical guidelines (PubMed, MedC-PT) and designed for evidence-based medical reasoning. Strong on clinical protocol questions, drug interactions, and guideline compliance. More conservative and citation-aware than OpenBioLLM — the right choice when accuracy and traceability matter more than breadth.

---

### BioMistral 7B (Yanis Labrak)
**Role in Office:** Fast biomedical classification and extraction
**Runner:** Ollama · **VRAM:** ~5GB (4-bit) · **Context:** 32K tokens

Mistral 7B fine-tuned on PubMed Central. At 7B it cannot match the 70B biomedical models on complex reasoning, but it handles classification (is this text clinically relevant?), extraction (pull the dosage information from this abstract), and summarisation of individual biomedical documents reliably and at high throughput. The biomedical equivalent of Mistral 7B in the general stack.

---

### ESMFold (Meta)
**Role in Office:** Protein structure prediction from amino acid sequence
**Runner:** standalone / HuggingFace · **VRAM:** ~16GB

Meta's protein language model that predicts 3D protein structure from sequence alone — without multiple sequence alignment, which makes it dramatically faster than AlphaFold 2 (seconds vs minutes per prediction). For Office deployments serving biotech, pharmaceutical, or synthetic biology clients, ESMFold enables protein structure analysis as a standard workflow step rather than a specialised compute job.

---

### ChemBERTa (Seyonec)
**Role in Office:** Molecular property prediction, chemical similarity
**Runner:** HuggingFace Transformers · **VRAM:** ~0.5GB

A RoBERTa trained on SMILES molecular notation — the text representation of chemical structures. Understands molecules the way BERT understands language. Useful for molecular property prediction, chemical similarity search, and as the backbone for chemistry-specific fine-tuning. For Office clients in materials science, pharmaceuticals, or specialty chemicals: give it a SMILES string, get back an embedding that captures chemical properties.

---

## Summary — The Full Stack

| Domain | Primary | Fast / Fallback |
|---|---|---|
| Reasoning | DeepSeek-R1 671B | Llama 3.1 405B |
| Execution | Llama 3.1 70B | Qwen 2.5 72B |
| Writing | Phi-4 14B | — |
| Extraction / Classification | Mistral 7B | Llama 3.1 8B |
| Code — architecture | Qwen 2.5 Coder 32B | Qwen 2.5 Coder 7B |
| Code — frontend / SVG | StarCoder2 15B | StarCoder2 7B |
| Code — SQL | SQLCoder 7B | — |
| Security | WhiteRabbitNeo R1 32B | — |
| Compliance | Granite 3.1 8B | — |
| Math | Mathstral 7B | — |
| Vision — heavy | Qwen2.5-VL 72B | LLaVA 1.6 34B |
| Vision — fast / OCR | Qwen2.5-VL 7B | Moondream2 |
| Image — quality | Flux.1 [dev] | Flux.1 [schnell] |
| Image — edit | Flux.1 Fill | — |
| Image — controlled | Flux.1 ControlNet Union | Flux.1 Depth / Canny |
| Design — post | Real-ESRGAN, BRIA RMBG, SAM2, IC-Light, IP-Adapter | — |
| Layout analysis | LayoutLMv3 Large | — |
| Video understanding | Qwen2.5-VL 72B | InternVL2 8B |
| Video understanding — quality | InternVL2 40B | — |
| Video QA / timestamps | Video-LLaVA | — |
| Video — long form | LLaMA-VID | — |
| Video — quality | Wan2.1 T2V 14B | Wan2.1 T2V 1.3B |
| Video — image-to-video | Wan2.1 I2V 14B | — |
| Music | MusicGen Large | MusicGen Small |
| Audio effects | AudioGen Medium | — |
| TTS — utility | Kokoro 82M | — |
| TTS — quality | Chatterbox | Parler-TTS Large |
| TTS — cloning | XTTS v2 | F5-TTS |
| Transcription | Whisper Large-v3 | Distil-Whisper Large-v3 |
| Transcription + diarization | WhisperX | — |
| Translation — text | NLLB-200 3.3B | Opus-MT |
| Translation — speech | Seamless M4T v2 | — |
| Embeddings | Nomic Embed Text | MXBai Embed Large |
| Document parsing | Nougat Large | GOT-OCR 2.0 |
| Formula OCR | pix2tex | — |
| Table QA | TAPAS Large | — |
| Table generation | TableLlama | — |
| 3D from image — fast | TripoSR | Zero123++ |
| 3D from image — quality | InstantMesh | — |
| 3D from text | Shap-E | — |
| Biomedical — heavy | OpenBioLLM 70B | Meditron 70B |
| Biomedical — fast | BioMistral 7B | — |
| Protein structure | ESMFold | — |
| Molecular properties | ChemBERTa | — |
