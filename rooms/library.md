# Library

Reference index for all external documentation, tools, APIs, and platforms used by the Office.
Load this file when you need an authoritative URL — do not rely on memory for links.

---

## Agent Infrastructure

### OpenClaw
The gateway and agent runtime powering the Office.
- Docs: https://docs.openclaw.ai
- Source: https://github.com/openclaw/openclaw
- Community: https://discord.com/invite/clawd
- Skills marketplace: https://clawhub.com
- Local docs: `/home/ubuntu/.npm-global/lib/node_modules/openclaw/docs/`

---

## AI Providers

### Anthropic (Claude)
Primary LLM provider. CEO runs Opus, CTO/main run Sonnet.
- Docs: https://docs.anthropic.com
- API reference: https://docs.anthropic.com/en/api/getting-started
- Model overview: https://docs.anthropic.com/en/docs/about-claude/models/overview
- Console: https://console.anthropic.com

### Ollama
Local model serving for self-hosted inference (planned).
- Docs: https://ollama.com/docs
- Model library: https://ollama.com/library
- GitHub: https://github.com/ollama/ollama

### MLX (Apple Silicon)
Local inference framework for Apple Silicon (Mac Studio production target).
- Docs: https://ml-explore.github.io/mlx/
- Models: https://huggingface.co/mlx-community

---

## Orchestration & Memory

### ChromaDB
Vector database for agent long-term memory (planned — Digital Archivist target).
- Docs: https://docs.trychroma.com
- GitHub: https://github.com/chroma-core/chroma

### LangGraph
Graph-based agent orchestration (evaluated, not yet adopted).
- Docs: https://langchain-ai.github.io/langgraph/

---

## Data & Research

### Firecrawl
Web search and scraping. Currently active (web search provider).
- Docs: https://docs.firecrawl.dev
- Dashboard: https://www.firecrawl.dev/app

### SearXNG
Self-hosted meta-search engine (planned).
- Docs: https://docs.searxng.org
- GitHub: https://github.com/searxng/searxng

### Crawl4AI
Web extraction for research pipelines (planned).
- GitHub: https://github.com/unclecode/crawl4ai
- Docs: https://crawl4ai.com/mkdocs/

---

## Infrastructure

### Oracle Cloud (OCI)
Current hosting provider for the `theoffice` VPS.
- Console: https://cloud.oracle.com
- Docs: https://docs.oracle.com/en-us/iaas/

### Tailscale
Secure network overlay. `theoffice.tail285214.ts.net` is the public gateway URL.
- Docs: https://tailscale.com/kb/
- Admin: https://login.tailscale.com/admin/

---

## Communication

### Discord Developer Portal
Bot management for CEO and CTO bots.
- Portal: https://discord.com/developers/applications
- CEO app: https://discord.com/developers/applications/1486220650195714208
- CTO app: https://discord.com/developers/applications/1486154132275335359

---

## Office Project

### Repository
- GitHub: https://github.com/bouveng/theoffice_
- Local: `/home/ubuntu/.openclaw/workspace/projects/@theoffice_/`

### Key documents
- Architecture: `/home/ubuntu/.openclaw/workspace/docs/ARCHITECTURE.md`
- Comms protocol: `/home/ubuntu/.openclaw/workspace/docs/COMMS_PROTOCOL.md`
- Memory protocol: `/home/ubuntu/.openclaw/workspace/docs/MEMORY_PROTOCOL.md`
- Office spec: `projects/@theoffice_/framework/office.md`
- Exec summary: `projects/@theoffice_/docs/exec-summary.md`

---

*Last updated: 2026-03-25 by main agent*
*To add an entry: append to the relevant section with name, one-line description, and URL.*
