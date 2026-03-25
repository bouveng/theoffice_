# Local AI — The Case for Local-First Intelligence

The Office runs entirely on local hardware. No API calls to Anthropic, OpenAI, or any other third party. No data egress. No vendor dependency. No inference bills. This is not a cost-cutting decision — it is an architectural one, and it has consequences that reach into security, compliance, model strategy, specialisation, and the fundamental question of who controls the intelligence running your business.

This document makes the case for local-first AI and explains why, for an autonomous enterprise platform, it is not optional.

---

## What Local-First Means

Local-first means every inference step — every token generated, every decision made, every task executed — happens on hardware you own and control. The model weights live on your disk. The compute runs on your chip. The data never leaves your premises.

It does not mean:
- Offline-only (the agents can browse, call APIs, send emails — they just *run* locally)
- Inferior (frontier-class open models now match or exceed GPT-4 class performance on most benchmark tasks)
- Expensive to operate (fixed hardware cost replaces open-ended per-token billing)
- Inflexible (you can run any model, swap models, fine-tune models — none of which you can do with a hosted API)

The distinction is between **running inference** and **using results**. Local-first governs where inference runs. The agents can interact with the world freely — they just do it from hardware you own.

---

## Data Sovereignty

When you call a third-party API, you send your data to someone else's computer. That sentence is simple. Its implications are not.

**What leaves your organisation when you call a hosted LLM API:**
- The content of your prompts — which may contain client names, financial figures, unreleased product plans, legal strategy, personnel information, or competitive intelligence
- The structure of your workflows — the sequence of prompts reveals how you operate
- The content of your retrieved documents — if you use RAG with a hosted model, your document corpus is visible to the inference endpoint
- Your error patterns — failed or retried calls expose what your system cannot handle

Most enterprise API agreements include data processing terms. Those terms define how your data is handled, retained, and potentially used. Even when vendors promise not to train on your data, you are relying on contractual assurances and their internal controls — neither of which you can verify or audit.

With local inference, there is nothing to audit. The data does not leave. The question of what the vendor does with it does not arise, because there is no vendor in the loop.

---

## Security

### The attack surface of cloud inference

Every API call is a network request. Network requests can be intercepted, logged, rate-limited, blocked, or price-changed. The inference endpoint is a dependency you do not control.

**Prompt injection via third-party infrastructure** is a real vector. If your agents process external content (web pages, emails, documents) and send that content to a hosted model, a malicious actor who knows you use that endpoint can craft inputs designed to manipulate the model's output — knowing the model's behavior, its tendencies, its guardrails. With a local model, the attacker does not know what model you run, what quantization, what system prompt structure, or what fine-tuning has been applied. The attack surface shrinks dramatically.

**Credential and key management** is eliminated for the inference layer. No API keys to rotate, leak, or have stolen. No rate limit errors cascading into operational failures. No inference endpoint going down during a critical task.

**Audit trail completeness.** With local inference, every prompt and every completion can be logged in full, locally, permanently, without cost. This is an audit trail the organization controls. With a hosted API, you log what you send and receive — but the inference itself is a black box inside someone else's infrastructure.

### Compliance — EU, GDPR, and the AI Act

The EU General Data Protection Regulation requires that personal data be processed with a lawful basis and protected against unauthorized access. Sending personal data to a US-based cloud API is a cross-border data transfer subject to GDPR Chapter V restrictions. Standard Contractual Clauses (SCCs) provide a legal mechanism, but they create compliance overhead and residual risk.

With local inference: personal data processed by the agents never leaves the jurisdiction of the hardware. There is no cross-border transfer. The compliance question simplifies from "what are the transfer safeguards" to "who has physical access to this machine."

The EU AI Act introduces additional requirements for high-risk AI systems, including requirements for transparency, human oversight, and documentation. A local deployment, by its nature, produces a complete and auditable record of every inference step. A hosted deployment depends on the vendor's logging — which you do not control and which may not meet the Act's documentation requirements.

**Sector-specific compliance** is where local-first becomes non-negotiable for some clients:
- **Legal firms** cannot send privileged client communications to a third-party server. Legal professional privilege is jurisdiction-dependent but universally fragile when data leaves counsel's control.
- **Healthcare** operates under strict data protection frameworks (HIPAA in the US, sector-specific national rules in the EU). Patient data processed by an AI agent cannot, in most frameworks, be sent to a commercial API without explicit patient consent and specific contractual protections.
- **Financial services** face regulatory scrutiny over the use of AI in client-facing decisions. An institution that cannot produce a full audit trail of every AI inference — including the exact model version, the exact inputs, and the exact outputs — has a compliance gap.

A local deployment closes all of these gaps structurally, not contractually.

---

## Training on Sensitive Data

This is the most underappreciated argument for local-first.

A hosted API gives you a fixed model. You can prompt it cleverly. You can fine-tune it if the vendor offers that feature, but the fine-tuning pipeline goes through their infrastructure — your training data leaves your premises.

With a local model, you own the entire training pipeline. This changes what is possible.

### Fine-tuning on internal data

Every organization has accumulated knowledge that is not on the internet. Internal process documents. Client interaction histories. Proprietary research. Domain-specific terminology. Institutional decision patterns. None of this is in any pre-training corpus, which means no hosted model — however capable — has been trained on it.

Fine-tuning a local model on this data injects that knowledge directly into the model's weights. The result is not a generic assistant that has been told about your business via a system prompt — it is a model that has *learned* your business, at the weight level, the same way it learned general language.

**What this produces:**
- A worker fine-tuned on your procurement documents outperforms a general model with procurement data injected as context — by a significant margin on extraction tasks
- A model fine-tuned on your legal contract library handles contract clause analysis at a consistency level no prompted general model achieves
- A model fine-tuned on your customer interaction history can identify patterns and surface insights that require understanding your specific business vocabulary and client relationships

None of this is possible if training data cannot leave the building. Local-first makes it possible.

### Continuous improvement from production

A local deployment can log every inference, review outputs for quality, and feed high-quality examples back into a fine-tuning pipeline — a continuous improvement loop operating entirely on your hardware on your data. The model improves from actual production use. With a hosted API, you produce outputs and discard them. The model does not improve from your usage (or if it does, the improvement benefits all other users, not just you).

### Sensitive synthetic data generation

Local models can generate synthetic training data from real sensitive data without the sensitive data ever leaving your control. A legal firm can generate thousands of synthetic contract clause examples derived from their real contract library, use those to fine-tune a contracts worker, and the real contracts never leave the firm's servers. This is a training methodology that is structurally impossible with cloud-based APIs.

---

## Cost Structure

The economics of local-first are counterintuitive at first glance but compelling over any meaningful time horizon.

**Cloud API pricing** is per-token. It scales linearly with usage. A busy autonomous agent swarm making thousands of inference calls per day generates a significant and unpredictable monthly bill. As the swarm scales, the bill scales with it. There is no cap.

From the [budget](../../docs/office-budget.md):

> **No API costs**: the architecture runs entirely on local hardware — no OpenAI, Anthropic, or other inference API bills. This is a deliberate cost containment decision.

**Local hardware pricing** is a fixed, one-time capital expenditure. The Mac Studio M5 Ultra at ~€22,000 is expensive at purchase. It is free to operate. At cloud API pricing for a comparable inference volume — a full 12-agent swarm running continuous tasks — the hardware pays for itself within months. Beyond that point, every inference is free.

The fixed cost model also enables a different kind of client pricing: a flat monthly fee rather than usage-based billing. Clients get predictable costs. The Office gets predictable revenue. Neither party is exposed to inference price volatility.

---

## Model Flexibility and Specialisation

The deepest architectural benefit of local-first is control over the model stack itself.

With a hosted API, you are offered a menu. You pick from what the vendor provides. The models change when the vendor changes them. The pricing changes when the vendor changes it. The capability profile changes when the vendor changes it. You can adapt, but you cannot direct.

With local inference, you select the model. You quantize it as needed for your hardware. You fine-tune it for your domain. You swap it when a better option becomes available. You run multiple models simultaneously, or sequentially, or on demand. You are not a consumer of a model service — you are an operator of a model stack.

### The model registry

The Office's model registry maps capability keys to specific model identifiers:

```json
{
  "reasoning":       "llama3.1:70b-instruct-q4_K_M",
  "writing":         "phi4:14b-q4_K_M",
  "extraction":      "mistral:7b-instruct-v0.3-q4_K_M",
  "classification":  "mistral:7b-instruct-v0.3-q4_K_M",
  "fast":            "llama3.1:8b-instruct-q4_K_M"
}
```

Agents request a capability — not a specific model. The registry resolves it. Updating the registry to point `reasoning` at a newer, better model requires one line change and zero modifications to any agent. This abstraction is only possible because the model stack is under your control. A hosted API does not offer this kind of programmatic model selection and hot-swapping. The full catalogue of models available across all domains is documented in [models.md](models.md).

### Specialisation without vendor permission

A specialist model for a narrow task — fine-tuned on your data, quantized to fit your hardware, optimised for your output format — outperforms a general frontier model on that task at a fraction of the compute cost.

Some examples of what becomes possible:

| Task | General hosted model | Local specialist |
|---|---|---|
| Contract clause extraction | Good with careful prompting | Excellent, consistent schema, trained on your clause library |
| Competitor signal classification | Requires extensive prompt engineering | Reliable classifier trained on your labelled signal history |
| Executive brief formatting | Inconsistent, requires formatting instructions every time | Output is always in your house format — it is baked in |
| Domain-specific terminology | May hallucinate or misuse | Correct by training, not by instruction |

The local-first architecture does not commit you to using only local models for all tasks. Some tasks — rare, high-stakes, genuinely frontier-capability tasks — may warrant a carefully considered API call. The point is that local-first makes this a deliberate choice, not a structural dependency.

---

## Model Switching with Preserved Context

Because the Office owns the model stack, it can switch models mid-task — not just between tasks. The [`agnostic`](../../traits/agnostic.md) trait formalises this: an agent that recognises it has moved from a reasoning phase to a writing phase does not need to complete the entire task on the same model. It serializes its state to a checkpoint, terminates, and respawns under a model better suited to the next phase.

This is an architectural capability that exists only in a local-first deployment. A hosted API gives you one model per call. You cannot say "use GPT-4 for the first five steps, then hand off to a cheaper model for the writing pass, and bring the context with you." The model boundary is the API boundary.

Locally, the model boundary is a configuration decision. The checkpoint protocol — `context_summary`, `phase_completed`, `phase_next`, `model_to` — is the standard interface. Any model that can read the checkpoint format can be slotted in at any phase of any task. The agent's identity and task continuity are preserved; only the inference substrate changes.

This is what it means in practice for the depth of specialisation available:

A single long-horizon task might involve:
1. **70B reasoning pass** — decompose the goal, identify unknowns, produce a task plan
2. **8B extraction pass** — run five parallel Signal Scout instances to gather structured data
3. **14B writing pass** — compile findings into a polished brief
4. **7B classification pass** — tag the brief's findings against a relevance taxonomy before archiving

Four models. One task. One preserved context thread. Impossible to achieve with a single hosted API. Straightforward with a local model registry and the agnostic checkpoint protocol.

---

## Vendor Independence

Dependency on a third-party inference API is a business risk, not just a technical one.

**Pricing risk.** API prices have historically moved in both directions. A swarm architecture that is profitable at current pricing may not be at next quarter's pricing. Local hardware has a fixed amortised cost that does not change.

**Capability risk.** Models are updated, retrained, and deprecated by vendors without notice. A workflow tuned to the behavior of a specific model version may break silently when the model is updated. Locally, model versions are pinned. Nothing changes unless you change it.

**Availability risk.** API downtime is the vendor's problem but your operational failure. A local inference stack that is down is a hardware or software problem you can diagnose and fix. A hosted API that is down is a problem you wait out.

**Terms of service risk.** Vendors change what they allow. Use cases that are permitted today may be restricted tomorrow. A legal firm using an API for contract analysis has no guarantee that use remains permitted under future terms. Local inference operates outside any vendor's terms of service.

**Geopolitical risk.** US-based AI infrastructure is subject to US regulatory and governmental reach. The EU AI Act, GDPR, and future regulatory developments create genuine uncertainty about the long-term accessibility of US-hosted AI services for EU enterprises. Local deployment on EU-based hardware eliminates this exposure entirely.

---

## The Summary Argument

The case for local-first is not one argument — it is five independent arguments that each hold on their own:

| Argument | What it means in practice |
|---|---|
| **Sovereignty** | Your data never leaves. No exceptions, no fine print. |
| **Security** | Smaller attack surface, no credential exposure, complete audit trail |
| **Compliance** | GDPR, AI Act, and sector-specific frameworks met structurally, not contractually |
| **Training** | Fine-tune on real internal data; continuous improvement from production use |
| **Flexibility** | Own the model stack — swap, specialise, fine-tune, and version-pin without permission |
| **Cost** | Fixed hardware, zero marginal inference cost, predictable pricing for clients |
| **Independence** | No vendor pricing, availability, capability, or terms risk |

Any single one of these is a strong reason for a privacy-sensitive or compliance-bound organisation to prefer local inference. Taken together, for an autonomous enterprise platform handling real business operations, local-first is not a preference. It is the only defensible architecture.
