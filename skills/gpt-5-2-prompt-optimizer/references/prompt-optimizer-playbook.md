# Prompt Optimizer Playbook (GPT-5.2, `reasoning_effort: none`)

Use this playbook to draft or rewrite prompts so GPT-5.2 behaves fast, consistent, and eval-friendly in non-reasoning mode.

## Default Operating Assumptions (None-Reasoning Mode)

- Optimize for **clarity + constraints**, not “deep thinking”.
- Do **not** request chain-of-thought (avoid: “think step by step”, “show your reasoning”).
- Prefer **short self-checks** and **explicit stop conditions**.
- If ambiguity matters, either:
  - Ask up to **1–3 clarifying questions**, or
  - State **2–3 interpretations** with labeled assumptions.

## Prompt Skeleton (System / Developer)

Paste and adapt; keep sections short and non-contradictory.

```
You are <role>.

CORE MISSION
- <what to do>

DEFINITION OF DONE
- Stop when <concrete stop condition>.

OUTPUT FORMAT
- Return <format> with <exact structure>.
- Length: <max sentences/bullets/words>.

SCOPE & CONSTRAINTS
- Do exactly and only what the user asked.
- Do not <forbidden behaviors>.
- If required info is missing: <ask questions OR assumptions policy>.

RISK / ACCURACY (IF HIGH-STAKES)
- Do not guess numbers, dates, policies, or citations.
- If uncertain: say what is known from context and what is unknown.

TOOLS (IF ANY)
- Use tools only when <conditions>.
- After tool use: restate what changed + where + how validated.
```

## Copy-Ready Blocks

### Verbosity Clamp

```
<output_verbosity_spec>
- Default: 3–6 sentences or ≤5 bullets.
- For simple yes/no: ≤2 sentences.
- Prefer compact bullets over long paragraphs.
- Do not restate the user request unless needed for constraints.
</output_verbosity_spec>
```

### Scope Discipline (Prevents “extra features”)

```
<scope_constraints>
- Implement exactly and only what the user requested.
- No extra features, no embellishments, no speculative additions.
- If ambiguity exists, choose the simplest valid interpretation.
</scope_constraints>
```

### Ambiguity & Hallucination Control

```
<uncertainty_and_ambiguity>
- If underspecified, explicitly say what is missing and:
  - Ask up to 1–3 clarifying questions, OR
  - Provide 2–3 interpretations with labeled assumptions.
- Never fabricate exact figures, quotes, citations, or external references.
- Prefer “Based on the provided context…” over absolute claims.
</uncertainty_and_ambiguity>
```

### Structured Extraction (Strict JSON)

```
<extraction_spec>
Extract data into JSON and follow this schema exactly (no extra keys):
{
  "field_a": "string",
  "field_b": "string | null"
}
- If a field is missing, set it to null (do not guess).
- Before returning, re-scan the source for missed fields.
</extraction_spec>
```

### Tool Policy (Keeps `reasoning_effort: none` efficient)

```
<tool_use_policy>
- Prefer answering from provided context when possible.
- Use a tool only when it materially changes correctness (fresh/user-specific data).
- Cap tool calls at 2 per user request unless new information makes more strictly necessary.
</tool_use_policy>
```

## Rewrite Checklist (Use Internally)

- Goal is crisp (one sentence) and “done” is measurable.
- Output format is unambiguous (schema/examples if needed).
- Verbosity is clamped; no contradictory “be concise” + “be exhaustive” without a rule.
- Ambiguity policy is explicit (questions vs assumptions).
- Scope constraints exist when drift is likely (coding/design/agentic tasks).
- No chain-of-thought requests; no “think step by step”.
- Tool rules are explicit (when to use, caps, and post-tool reporting).

## Output Template (When Delivering a Rewrite)

1) **Rewritten prompt** (ready to paste)
2) **What changed (≤5 bullets)**: tie each to a failure mode
3) **Runtime knobs**: `reasoning_effort` (default none), verbosity, tool policy
4) **Mini eval set**: 5–10 tests + expected output shape

