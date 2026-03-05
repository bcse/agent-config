---
name: gpt-5-2-prompt-optimizer
description: "Write, rewrite, and optimize prompts for GPT-5.2 with a focus on fast, reliable behavior using non-reasoning / reasoning_effort: none (low deliberation) settings. Use when asked to draft system/developer prompts, refactor bloated prompts, tighten constraints (verbosity/output schema/scope), reduce overthinking/tool spam, migrate prompts to GPT-5.2, or create eval-ready prompt variants for production agents."
---

# GPT-5.2 Prompt Optimizer (None-Reasoning Mode)

## Overview

Produce production-ready prompt drafts and rewrites that are optimized for GPT-5.2 running in non-reasoning / low-deliberation mode (typically `reasoning_effort: none`) by making goals, constraints, and output shape explicit.

## Workflow (Use Every Time)

### 0) Gather Inputs (Do Not Guess)

- Ask for (or infer from provided context) the minimum needed:
  - Target task(s) and success criteria (what “done” looks like).
  - Runtime constraints: latency target, tool availability, risk level (low/med/high stakes).
  - Required output shape (Markdown/bullets/JSON schema) and verbosity limits.
  - Any forbidden behaviors (no extra features, no web, no tool calls, etc.).

If the user provides an existing prompt, treat it as source-of-truth and preserve intent; avoid scope creep.

### 1) Diagnose Prompt Failures (Fast)

- Identify which failure class applies (often more than one):
  - Overthinking / slow TTFT, too much planning, too many tool calls.
  - Underthinking / misses edge cases, sloppy formatting, weak adherence.
  - Scope drift (especially design/UX/coding tasks).
  - Hallucination risk (ambiguous inputs, time-sensitive facts without tools).
  - Output-shape drift (schema violations, inconsistent formatting).

Use `references/gpt-5-2_prompting_guide.md` and `references/gpt-5_troubleshooting_guide.md` only if you need additional patterns or wording.

### 2) Rewrite Using “None-Reasoning Mode” Defaults

Assume `reasoning_effort: none` unless the user explicitly requests otherwise.

- Avoid instructions like “think step by step” or “show your reasoning”. Prefer:
  - “Be decisive and direct; do a brief self-check before answering.”
  - “If uncertain, ask up to N clarifying questions or state assumptions.”
- Make the “definition of done” concrete (stop condition).
- Clamp verbosity and output format explicitly.
- Add scope guards (“exactly and only what the user asked”) when relevant.
- For structured outputs: provide a strict schema, required/optional fields, and null-handling rules.

For copy-ready blocks and templates, use `references/prompt-optimizer-playbook.md`.

### 3) Deliverables (What to Output)

- **Rewritten prompt** in a clean, ready-to-paste format.
- **Change log** (≤5 bullets): what changed + why (tie to failure modes).
- **Runtime knobs**: recommended `reasoning_effort` (default none), verbosity, and tool policy.
- **Mini eval set**: 5–10 test cases (incl. 1–2 negative/adversarial) to validate behavior.

## Optional: Lint a Prompt File

If the user provides prompts as files, run `scripts/prompt_lint.py` to surface common “none-reasoning mode” gaps (missing output shape, contradictions, step-by-step leakage, etc.).
