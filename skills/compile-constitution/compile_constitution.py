"""
Skill: compile_constitution
Shared across all agents in the office swarm.

Purpose:
    Assemble the [CONSTITUTION] block for an agent's system prompt at
    instantiation time. Reads the Runtime Fragment from each of the agent's
    assigned traits and influences and compiles them into a single block.

    The compiled system prompt is set once when the agent spawns.
    It never appears in the per-message context window.

Input:
    role        (str)       — the agent's role description (e.g. "You are the CEO...")
    traits      (list[str]) — trait names (e.g. ["politeness", "directness"])
    influence   (str | None)— influence name (e.g. "ayn-rand"), or None
    traits_dir  (Path)      — path to the traits/ directory

Output:
    str — the full system prompt block: [ROLE] + [CONSTITUTION]

Two-Layer Pattern:
    Each trait and influence .md file contains a documentation layer (human-readable)
    and a Runtime Fragment section (model-facing). Only the Runtime Fragment is
    extracted and injected — the full prose never enters the context window.
"""

from pathlib import Path


RUNTIME_FRAGMENT_HEADING = "## Runtime Fragment"


def _extract_runtime_fragment(md_path: Path) -> list[str]:
    """Return the bullet lines from the ## Runtime Fragment section of a .md file."""
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    in_fragment = False
    bullets: list[str] = []

    for line in lines:
        if line.strip() == RUNTIME_FRAGMENT_HEADING:
            in_fragment = True
            continue
        if in_fragment:
            # Stop at the next ## heading
            if line.startswith("## ") and line.strip() != RUNTIME_FRAGMENT_HEADING:
                break
            stripped = line.strip()
            if stripped.startswith("- "):
                bullets.append(stripped)

    return bullets


def compile_constitution(
    role: str,
    traits: list[str],
    influence: str | None,
    traits_dir: Path,
) -> str:
    """
    Compile the system prompt for an agent.

    Args:
        role:       Short role description, e.g. "You are the CEO.
                    You set strategy, resolve conflicts, and act as the final
                    quality gate before delivery."
        traits:     List of trait names corresponding to files in traits_dir/
                    (without the .md extension), e.g. ["politeness"].
        influence:  Influence name corresponding to a file in traits_dir/influence/
                    (without the .md extension), e.g. "ayn-rand". Pass None if
                    the agent has no influence.
        traits_dir: Path to the traits/ directory.

    Returns:
        Full system prompt string with [ROLE] and [CONSTITUTION] blocks.
    """
    bullets: list[str] = []

    for trait in traits:
        path = traits_dir / f"{trait}.md"
        if not path.exists():
            raise FileNotFoundError(f"Trait file not found: {path}")
        bullets.extend(_extract_runtime_fragment(path))

    if influence is not None:
        path = traits_dir / "influence" / f"{influence}.md"
        if not path.exists():
            raise FileNotFoundError(f"Influence file not found: {path}")
        bullets.extend(_extract_runtime_fragment(path))

    constitution_block = "\n".join(bullets)

    return (
        f"[ROLE]\n{role}\n\n"
        f"[CONSTITUTION]\n{constitution_block}"
    )
