# Model Benchmark Plan — Frontier vs Open-Source
**Status:** Planned — pending execution
**Author:** CTO
**Date:** 2026-03-25

---

## Objective

Determine whether Claude Sonnet 4.6 (current CTO/MAIN model at ~$3/M tokens) can be replaced with a cheaper alternative without meaningful quality loss on the tasks the Office actually runs.

## Candidates

| Model | Provider | Est. Cost/M tokens | Notes |
|---|---|---|---|
| Claude Sonnet 4.6 | Anthropic | ~$3.00 | Baseline |
| DeepSeek-V3 | DeepSeek API | ~$0.27 | Frontier-class, cheapest |
| Qwen2.5-72B-Instruct | Together.ai / Fireworks | ~$0.90 | Strong open-source |

## Test Tasks

**Task 1: Structured JSON output**
Prompt: `Given this agent roster [CEO, CTO, CFO, CAO, COO, DOE, CMO, CCO], produce a task delegation JSON matching the COMMS_PROTOCOL.md schema for: 'Draft a go-to-market brief for Q3'`
Evaluate: schema correctness, field completeness, no hallucination

**Task 2: Technical decision with trade-offs**
Prompt: `We need to choose between SQLite (Option A) and Temporal (Option B) for our Task DAG. Context: local-first, single machine, Q1 prototype. Give a recommendation with reasoning.`
Evaluate: reasoning quality, identifies correct trade-offs, doesn't hedge

**Task 3: Code generation**
Prompt: `Write a Python function that reads a JSONL trace log, aggregates estimatedCostUsd by agent prefix, and returns a dict: {agent: cost}. Handle malformed lines gracefully.`
Evaluate: correctness, error handling, runs without modification

**Task 4: Memory discipline — context summarisation**
Prompt: `Summarise the following session history into a heartbeat.md entry [~500 token session dump]`
Evaluate: compression quality, no hallucination, correct format

## Scoring

Each task scored 1–5 on: accuracy, format compliance, reasoning quality.
Total: /20 per model. Cost per 1,000 tasks estimated alongside score.

## Method

Sub-agents call each model API in parallel with identical prompts. Results posted side-by-side in `#theoffice_`. CTO scores — Board decides.

**APIs required:**
- DeepSeek API key
- Together.ai or Fireworks API key

## Expected Outcome

If DeepSeek-V3 scores ≥16/20: recommend switching CTO/MAIN to DeepSeek-V3.
Estimated monthly savings: ~$1,200–1,300/month vs current Anthropic spend.
Workers: move to open-source regardless of management-tier outcome.

---

*Blocked on: API keys for DeepSeek and Together.ai*
*Schedule: when Board approves and keys are available*
