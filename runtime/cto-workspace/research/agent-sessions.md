# Agent Session Mechanics in OpenClaw

**Date:** 2026-03-26  
**Author:** CTO  
**Topic:** Session isolation, context, and concurrency

## Session Definition

A "session" in OpenClaw is an isolated conversation context with specific properties:

1. **Unique Identifier:** Each conversation (DM, channel, thread) gets a unique session key
2. **Workspace Isolation:** Sessions can share or have separate workspaces
3. **Memory Scope:** Session-specific context and history

## Current CTO Session Configuration

### Session Properties
- **Current Session:** PM with bouveng (Board)
- **Session Key:** `agent:cto:discord:user:708808214371762267`
- **Workspace:** `/home/ubuntu/.openclaw/workspace-cto`
- **Memory Access:** MEMORY.md + memory/*.md in workspace

### Context Boundaries
- **Included:** Workspace files (SOUL.md, AGENTS.md, research/, etc.)
- **Excluded:** Other session histories unless explicitly fetched
- **Shared:** Memory files (persistent across sessions)

## Session Isolation & Concurrency

### Multiple Concurrent Sessions
If you (@bouveng) and @jonas talk to the CTO simultaneously in different PMs:

```
Scenario:
- Session A: CTO ↔ @bouveng (PM)
- Session B: CTO ↔ @jonas (PM)

Mechanics:
1. Each session runs independently
2. Separate conversation histories
3. Same workspace (unless configured otherwise)
4. Shared memory files (MEMORY.md, memory/*.md)
5. No automatic cross-session awareness
```

### Knowledge Access Across Sessions

**What the CTO can access:**
- ✅ Same workspace files (SOUL.md, AGENTS.md, research/, etc.)
- ✅ Shared memory (MEMORY.md, memory/*.md)
- ✅ System tools and configuration
- ✅ Git repository state

**What the CTO cannot automatically access:**
- ❌ Other session conversation histories
- ❌ Session-specific temporary context
- ❌ Private attachments from other sessions
- ❌ Real-time awareness of other active sessions

### Manual Cross-Session Access
The CTO can explicitly access other sessions using:
```javascript
sessions_list()          // List all active sessions
sessions_history()       // Fetch history of specific session
sessions_send()          // Send message to another session
```

## Memory Persistence Model

### Tier 1: Session Memory (Volatile)
- Current conversation context
- Last few messages
- Tool call results
- **Lost when session ends**

### Tier 2: Workspace Memory (Persistent)
- Files in workspace directory
- Research documents
- Configuration files
- **Persists across sessions**

### Tier 3: Shared Memory (Global)
- MEMORY.md
- memory/*.md files
- **Shared across all CTO sessions**

## Practical Implications

### For Users
1. **Context Preservation:** Workspace files maintain continuity
2. **Privacy:** PM conversations remain isolated unless explicitly shared
3. **Consistency:** Shared memory ensures aligned knowledge base
4. **Concurrency:** Multiple users can interact with CTO simultaneously

### For CTO Operations
1. **Identity Consistency:** SOUL.md defines behavior across all sessions
2. **Task Management:** Tasks.md coordinates work regardless of session
3. **Research Continuity:** Research/ directory accumulates knowledge
4. **Memory Discipline:** Must use memory_search() for prior work recall

## Example: Concurrent Task Coordination

```
Session A (bouveng): "Analyze domain setup"
- CTO creates research/domain-web.md
- Updates tasks.md
- Commits to git

Session B (jonas): "What's the domain status?"
- CTO can:
  1. Read research/domain-web.md (workspace file)
  2. Check tasks.md (workspace file)
  3. Report current status
- CTO cannot:
  1. See bouveng's specific instructions
  2. Know bouveng is also discussing domains
  3. Share bouveng's private attachments
```

## Security & Privacy Considerations

### Data Isolation
- **PM Conversations:** Isolated by session key
- **File Attachments:** Stored in session-specific locations
- **Temporary Data:** Cleared with session termination
- **Access Control:** Manual cross-session access requires explicit tool calls

### Information Flow Control
- **Default:** No automatic information sharing between sessions
- **Explicit Sharing:** Requires sessions_send() or shared files
- **Audit Trail:** All cross-session access via tool calls is logged

## Best Practices

### For Users
1. **Reference Prior Work:** "Check research/domain-web.md"
2. **Use Shared Files:** Place collaborative work in research/
3. **Be Specific:** Reference file paths for context
4. **Assume Isolation:** Don't assume CTO remembers other PM conversations

### For CTO
1. **Memory Discipline:** Always use memory_search() for recall
2. **Workspace Hygiene:** Keep research/ organized
3. **Context Declaration:** State what context is being used
4. **Explicit Sharing:** Use sessions_* tools for cross-session communication

## Technical Implementation Notes

### Session Keys Format
```
agent:{agentId}:{channel}:{targetType}:{targetId}
Example: agent:cto:discord:user:708808214371762267
```

### Workspace Inheritance
- Agent sessions inherit parent workspace by default
- Can be overridden with cwd parameter in sessions_spawn()
- Sub-agents get isolated workspaces unless configured otherwise

### Memory Search Scope
```javascript
memory_search(query) searches:
1. MEMORY.md in current workspace
2. memory/*.md in current workspace
3. Optionally: session transcripts (if configured)
```

## References

- [OpenClaw Session Documentation](https://docs.openclaw.ai/agents/sessions)
- [Memory System](https://docs.openclaw.ai/agents/memory)
- [Tool Reference: sessions_*](https://docs.openclaw.ai/tools/sessions)