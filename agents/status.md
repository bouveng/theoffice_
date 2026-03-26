# Office Status Updates

Daily status briefs compiled by the CEO. Only the 5 most recent updates are kept.
Entries are separated by `---`.

---

## 2026-03-26 - Office Status

**Office Status — 2026‑03‑26**

🟡 **Infra:** Gateway running (systemd active), Tailscale reachable, update available (2026.3.24). 2 security warnings (denyCommands ineffective, multi‑user heuristic).
🟡 **Agents:** 3 agents active (CEO, CTO, main), 21 sessions. All using DeepSeek models (fallback from Claude due to billing). Latency penalty 10–15 s.
🟡 **Memory:** 1 daily memory file (2026‑03‑25), memory dirty, 0 chunks. ChromaDB not yet deployed.
🟡 **Security:** 2 warnings, 0 critical. Potential multi‑user setup; denyCommands matching limited.
💰 **Cost:** All agents on DeepSeek Reasoner/Chat (~$0.14/M in, $0.28/M out). Estimated 99% savings vs Claude Opus/Sonnet (~$374.22/month). Latency trade‑off accepted.

**Bottom line:** Office operational with DeepSeek fallback; security warnings need review.
---

## 2026-03-26 - Office Status

**Office Status — 2026‑03‑26**

🟢 **Infra:** Gateway active (pid 53886), systemd‑managed, Tailscale reachable. OpenClaw 2026.3.23‑2 stable, update available (2026.3.24). VPS uptime 1d 8h.

🟡 **Agents:** 3 agents deployed — main (DeepSeek Reasoner), ceo (Claude Opus → falling back to DeepSeek due to Anthropic billing issue), cto (Claude Sonnet → same fallback). 18 sessions active. Discord bots connected, `requireMention: true` + mention‑patterns working.

🟢 **Memory:** Daily file `2026‑03‑25.md` (3.7 KB) written, covers architecture baseline, comms/memory protocols, agent constitutions. Library reference (`rooms/library.md`) added, rooms concept documented.

🟢 **Security:** No warnings. Guild allowlist restricts Discord to Board members only. No unauthorised logins.

💰 **Cost:** Agents configured for Opus/Sonnet (~$378/month) but falling back to DeepSeek Reasoner (~$3.78/month) due to Anthropic billing issue. Savings: ~99% ($374.22/month). Latency penalty: ~10–15 s per turn.

**Bottom line:** Platform stable with three agents operational; model fallback to DeepSeek cuts costs but adds latency — Anthropic billing needs attention.