"""
Skill: summarize
Shared across all agents in the office swarm.

Purpose:
    Condense any text input into a structured summary.
    Used by workers (Digital Archivist, Executive Briefer),
    specialists (COO, CMO), and management (CEO, CAO).

Input:
    text    (str)  — raw content to summarize
    mode    (str)  — "brief" | "detailed" | "bullets" (default: "brief")
    max_tokens (int) — output length cap (default: 256)

Output:
    dict with keys:
        summary  (str)   — the condensed output
        mode     (str)   — mode used
        truncated (bool) — whether input was trimmed before processing
"""

from dataclasses import dataclass
from typing import Literal


SummaryMode = Literal["brief", "detailed", "bullets"]


@dataclass
class SummaryResult:
    summary: str
    mode: SummaryMode
    truncated: bool


PROMPTS: dict[SummaryMode, str] = {
    "brief": "Summarize the following in 2–3 sentences:\n\n{text}",
    "detailed": "Provide a structured summary with key points and conclusions:\n\n{text}",
    "bullets": "Summarize the following as a concise bullet-point list:\n\n{text}",
}

# Soft input limit — trim before sending to model to avoid context overflow
INPUT_CHAR_LIMIT = 12_000


def summarize(
    text: str,
    mode: SummaryMode = "brief",
    max_tokens: int = 256,
    llm_call,  # injected by the agent runtime
) -> SummaryResult:
    truncated = len(text) > INPUT_CHAR_LIMIT
    if truncated:
        text = text[:INPUT_CHAR_LIMIT]

    prompt = PROMPTS[mode].format(text=text)

    result = llm_call(prompt=prompt, max_tokens=max_tokens)

    return SummaryResult(
        summary=result,
        mode=mode,
        truncated=truncated,
    )
