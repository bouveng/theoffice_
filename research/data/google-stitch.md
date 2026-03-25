# Google Stitch

Exploration of how Stitch — Google Labs' AI-native design platform — could integrate with the Office to produce design assets, maintain a shared design language, and plug into the agent pipeline without transmitting sensitive data.

Source: [Introducing "Vibe Design" with Stitch](https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-ai-ui-design/) (Google Labs, March 2026)

---

## What Stitch Is

Stitch is a browser-based, AI-native design canvas. Free, no download, sign in with Google at `stitch.withgoogle.com`.

The core idea — "vibe design" — mirrors vibe coding: instead of specifying exact instructions, you describe intent (business objective, desired feeling, inspiration references), and the AI explores directions. You iterate from there.

**Key features:**

- **Infinite canvas** — early ideation to working prototype in the same space
- **Voice canvas** — speak to the agent in real time ("give me three menu options", "show me this in different palettes") and watch the canvas update live
- **Design Agent** — tracks full project history, reasons across all versions and branches
- **Agent Manager** — explore multiple design directions in parallel without losing any branch
- **DESIGN.md** — an agent-friendly markdown file that encodes a complete design system; can be exported from any URL or imported into any Stitch project or external tool
- **Direct edits** — manual text, image, and fine-detail tweaks without re-prompting
- **Auto-prototyping** — static screens automatically become clickable, shareable interactive flows
- **Figma export** — paste with Auto Layout and fully editable layers

**Native integrations via SDK and MCP server:**
- Claude Code
- Cursor
- Google AI Studio / Gemini CLI
- Antigravity (Google's AI IDE)
- Figma

The MCP server is the critical detail for the Office.

---

## The MCP Hook

The Office already uses MCP as its agent communication layer. Stitch ships with an MCP server. This means Office agents can call Stitch tools directly from within the same protocol stack — no separate API integration, no glue code, no leaving the environment.

In practice, an agent running in Claude Code can talk to Stitch's MCP server to:
- Create or open a project
- Describe a UI requirement in natural language
- Retrieve generated HTML, CSS, or React component code
- Export a DESIGN.md for the current project
- Get a shareable prototype URL

Output comes back through MCP, enters the normal Office task pipeline, and can be routed to the Digital Archivist for storage, the DOE for implementation, or the CEO for sign-off via a prototype link.

---

## Data Boundary: What Is and Is Not Safe to Send

Stitch is an external Google service. The local-first principle applies: only send what you would be comfortable making public or sharing with a vendor under a standard DPA.

**Safe to send:**

| Data type | Why it's safe |
|---|---|
| Natural-language design briefs | Generic intent, no proprietary logic |
| Brand style guidelines (colors, fonts, tone) | Intended to be externally visible anyway |
| Layout and UX descriptions | No business logic embedded |
| DESIGN.md files | Design tokens and rules, not data |
| Generated code (HTML, React, CSS) | Front-end output, already public-facing |
| Prototype review requests | Visual feedback on non-sensitive UI |
| Wireframe concepts | High-level sketches, no internals |

**Do not send:**

| Data type | Why it's risky |
|---|---|
| Internal agent prompts or system architecture | Reveals platform design |
| Proprietary business logic | Competitive exposure |
| Customer data or user behaviour | Privacy/compliance |
| Database schemas or API structure | Security surface |
| Internal financial or strategic data | Obvious |

The safe subset is large enough to be genuinely useful. A full design sprint — brief, iteration, prototype, export — can happen without touching anything sensitive.

---

## DESIGN.md as a Shared Design Trait

The most structurally interesting feature for the Office is DESIGN.md. The Office already represents agent behaviour in markdown files (traits, influences). DESIGN.md extends that pattern into the visual layer.

A DESIGN.md encodes:
- Typography stack (families, weights, sizes, line heights)
- Colour palette (primary, secondary, semantic tokens)
- Spacing and grid system
- Component conventions (buttons, forms, cards, navigation)
- Tone and visual personality

Once the CCO produces and owns a canonical DESIGN.md, it becomes a shared reference that every agent producing visual output can import. It's the design equivalent of a trait — not injected into model context at full length, but referenced when visual output is in scope.

**In practice:**

```
CCO uses Stitch to iterate on brand identity
  → exports DESIGN.md to Office knowledge base (Digital Archivist)
  → DOE imports DESIGN.md when scaffolding any front-end component
  → CMO references DESIGN.md when briefing Stitch for campaign assets
  → Media Assembly Line worker imports DESIGN.md for any generated imagery prompts
```

Every Office output that has a visual dimension draws from the same source of truth. Consistency becomes structural rather than a matter of individual agent discipline.

---

## Agent Mapping

### CCO — Chief Creative Officer
**Primary user.** Stitch is the CCO's native tool for design execution.

- Opens Stitch with the design brief as the vibe prompt (brand objective + desired feeling + inspiration references)
- Uses Agent Manager to explore 3–5 directions simultaneously
- Iterates with voice canvas for rapid palette, layout, and component variations
- Signs off on a direction, exports DESIGN.md and React/HTML components
- Maintains the canonical DESIGN.md in the Digital Archivist

The CCO does not need to know how to use Figma or write CSS. Stitch handles both, with Figma export available if human designers need to take over or refine.

---

### CMO — Chief Marketing Officer
**Consumer and requester.** The CMO briefs the CCO or directly prompts Stitch for campaign-specific assets.

- Landing pages for campaigns: describe the business objective and target feeling → Stitch generates multiple directions → pick one → export code or prototype
- Social media UI mockups: frame sizes, copy, visual hierarchy described in natural language
- A/B test variants: Agent Manager runs two design directions in parallel → prototype links shared for stakeholder review before engineering builds either

The CMO's briefs to Stitch stay at the level of marketing intent ("we want users to feel confident and modern") — no sensitive data involved.

---

### DOE — Director of Engineering
**Implementer.** Receives design output from Stitch and implements it.

- The Claude Code + Stitch MCP integration means the DOE's coding environment can pull Stitch components directly — the design-to-code handoff happens in the same tool
- Stitch-generated React components drop into the front-end codebase; the DOE reviews, adjusts for integration, and ships
- DESIGN.md imports into the IDE context so component styling decisions are automatically consistent with the established design system
- Prototype links allow the DOE to review exact expected interactions before writing implementation code

The DOE shortcircuits the traditional designer → Figma → dev handoff cycle. Stitch produces working code directly, the DOE integrates rather than translates.

---

### CEO — Strategic sign-off
**Reviewer.** Stitch's clickable, shareable prototype URLs are the relevant feature here.

- Before engineering begins any significant UI sprint, a Stitch prototype link goes to the CEO for sign-off
- No design tool access required — just a browser link
- Comments and direction changes happen at the prototype stage, before implementation cost is incurred
- This fits naturally into the CEO's oversight role without requiring the CEO to operate Stitch directly

---

### Digital Archivist — Knowledge store
**Asset library.** The Archivist stores and versions all design assets produced by Stitch.

- DESIGN.md (canonical, versioned)
- Exported component code (HTML, React, CSS)
- Prototype URLs with metadata (which brief, which campaign, which version)
- Design brief history (what was prompted, what directions were explored, what was chosen and why)

This gives the Office a searchable design history. When a new campaign starts, the CMO or CCO can retrieve past briefs and designs as context before opening Stitch, rather than starting from nothing each time.

---

### Signal Scout / Research workers
**Indirect consumer.** When researching competitors, market trends, or design references, a worker could pull screenshots or describe competitor UI in natural language and use Stitch to generate comparable or contrasting directions. Entirely safe — no internal data involved, only external reference material.

---

## Workflow: Full Design Sprint

```
CMO identifies need (new product landing page)
          │
          ▼
CMO writes design brief (objective, audience, feeling, inspiration URLs)
[sent to Stitch as vibe prompt — safe, no sensitive data]
          │
          ▼
CCO opens Stitch, pastes brief, uses Agent Manager to generate 3 directions
          │
          ▼
CCO uses voice canvas to iterate on the best direction
("show me this with a darker hero", "give me two navbar options")
          │
          ▼
CCO exports prototype link → CEO reviews and approves
          │
          ▼
CCO exports React components + DESIGN.md
  → Components → DOE (via MCP, directly into Claude Code)
  → DESIGN.md → Digital Archivist (updates canonical design system)
          │
          ▼
DOE integrates components, ships
          │
          ▼
Digital Archivist stores brief, prototype URL, component code,
and updated DESIGN.md for future reference
```

Total external data exposure: the design brief (plain language intent) and the exported code (front-end output). Nothing internal crosses the boundary.

---

## What Stitch Does Not Replace

- **Copywriting** — Stitch generates layout and UI, not editorial voice. The CCO still produces written content separately.
- **Brand strategy** — Stitch executes design direction; it does not set it. The CMO and CEO still own brand positioning.
- **Engineering architecture** — Stitch outputs front-end components. The DOE still owns back-end architecture, integrations, and performance.
- **Local inference** — Stitch is a Google cloud service. Any design work requiring confidential data must happen in a local or sovereign tool. Stitch is for the public-facing layer only.

---

## Cost and Access

Free. Google account required. Available in all regions where Gemini is available. No API key needed for browser-based use. MCP server access may require additional configuration — check Stitch documentation at `stitch.withgoogle.com`.

---

## Things to Validate

- **MCP server setup** — confirm the exact configuration needed to connect Stitch's MCP server to Claude Code and what tools it exposes
- **DESIGN.md spec** — what fields and format it uses, whether it's stable enough to treat as a long-term canonical file or likely to change across Stitch versions
- **Export code quality** — whether Stitch's React/HTML output is production-ready or requires significant cleanup by the DOE
- **Voice canvas privacy** — confirm whether voice input is processed by Google's servers and what the retention policy is before using it for any brand-sensitive direction discussions
- **Rate limits** — whether the free tier imposes limits on generation volume that would affect a high-frequency design workflow
