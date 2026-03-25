# Skills

Shared capabilities available to all agents in the [Office](../framework/office.md) swarm. Each skill lives in its own subdirectory containing a `.md` spec and a `.py` implementation.

Skills are invoked by the agent runtime — not directly by humans. They are injected as callable tools at agent instantiation.

## Skills

| Skill | Description |
|---|---|
| [compile-constitution](compile-constitution/compile-constitution.md) | Assembles an agent's `[CONSTITUTION]` block from its trait and influence runtime fragments |
| [summarize](summarize/summarize.md) | Condenses text to brief, detailed, or bullet-point format; used by workers, the [Digital Archivist](../agents/workers/digital-archivist/digital-archivist.md), and the [Executive Briefer](../agents/workers/executive-briefer/executive-briefer.md) |

## Structure

Each skill follows this pattern:

```
skills/
└── skill-name/
    ├── skill-name.md     — spec: purpose, inputs, outputs, usage
    └── skill_name.py     — implementation
```

The `.md` file is the source of truth for what the skill does and how to call it. The `.py` file is the implementation. Neither should be modified without updating the other.

## Adding a skill

1. Create a new directory under `skills/` using kebab-case
2. Write the `.md` spec first — define inputs, outputs, and which agents use it
3. Implement the `.py` file
4. Register the skill in this README
5. Update any agent `.md` files that will use the skill
