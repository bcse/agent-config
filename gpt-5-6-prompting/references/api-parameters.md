# GPT-5.6 parameters that replace prompt text

Everything here is configuration, not prose. If a prompt is trying to achieve one of these effects with words, move it to the parameter.

Contents:
1. Model tiers
2. `reasoning.effort`
3. `reasoning.mode` — pro
4. `reasoning.context` — persisted reasoning
5. `text.verbosity`
6. Prompt caching
7. Programmatic Tool Calling wiring
8. Images
9. Safeguards and `safety_identifier`
10. Sample request

---

## 1. Model tiers

GPT-5.6 uses a new naming scheme. Pick by workload, not by habit:

| Slug | Use for |
|---|---|
| `gpt-5.6-sol` | Frontier capability; hardest tasks |
| `gpt-5.6-terra` | Strong performance at lower price; balanced default |
| `gpt-5.6-luna` | Efficient, high-volume workloads |

The bare `gpt-5.6` alias routes to `gpt-5.6-sol`. Use the Responses API for reasoning, tool-calling, and multi-turn workflows.

---

## 2. `reasoning.effort`

Ladder: `none`, `low`, `medium`, `high`, `xhigh`, `max`.

- `medium` is the balanced starting point; `low` for latency-sensitive work.
- `none` is a latency baseline — but test `low` too when the workflow benefits from reasoning or tool use.
- `high` / `xhigh` when more reasoning produces a *measured* quality gain.
- `max` is new in 5.6, reserved for the hardest quality-first workloads that need more exploration and verification. If you currently use `xhigh`, compare both.

Migrating from 5.5 or 5.4: keep your current setting as the baseline, then test the same setting *and one level lower*. GPT-5.6 often holds or improves quality with fewer tokens, so the level below your old default is frequently the right answer.

---

## 3. `reasoning.mode` — pro

Set `reasoning.mode: "pro"` on your chosen GPT-5.6 model. There is no separate Pro model slug.

Pro mode applies more model work before returning a single final answer. It raises latency and aggregates the extra tokens into reported usage, billed at the model's standard rates.

Use it when a marginal quality improvement materially changes the outcome and the task is hard enough to benefit — complex optimization, high-value coding or review, deep analysis with clear evaluation criteria. Prefer standard mode for routine, latency-sensitive, or high-volume work, and any time your evals don't show a real gain.

Mode and effort are independent. Start pro mode at the same model and effort as your standard-mode baseline, then compare — highest effort is not automatically the best tradeoff. If you omit effort, both modes default to `medium`.

Prompt unchanged: state the goal, context, constraints, required evidence, success criteria, and output format. Don't tell it to use pro mode or generate multiple candidates.

---

## 4. `reasoning.context` — persisted reasoning

GPT-5.6 can reuse reasoning items across turns, improving multi-turn quality and cache efficiency. GPT-5.6 defaults to `all_turns`; earlier models defaulted to `current_turn`.

- Omit it or set `auto` to get `all_turns`. Check the response's `reasoning.context` field to confirm what actually applied.
- `all_turns` when goals, assumptions, and priorities stay stable across turns. Continue with `previous_response_id` so earlier reasoning is available.
- `current_turn` when earlier reasoning is no longer relevant.
- Managing history yourself: preserve and resend previous user inputs and *every* response output item. Under `store: false` or Zero Data Retention, replay the encrypted reasoning items the API returns by default.

---

## 5. `text.verbosity`

`low`, `medium`, or `high` — the default level of detail for a request. This is the right lever for global length control; use the prompt only for task-specific length, structure, or required content.

Pairs with the brevity snippet in `prompt-templates.md`: verbosity sets the dial, the prompt says what must survive when the dial is low.

---

## 6. Prompt caching

Implicit caching still works with no code changes. What's new in 5.6 is explicit control over which reusable prefixes get cached.

Cost note: cache **writes** bill at 1.25× the uncached input rate; reads stay discounted. Track `cached_tokens` and `cache_write_tokens` to see net effect — naive caching of rarely-reused prefixes can cost more than it saves.

- Use explicit breakpoints or `prompt_cache_options.mode: "explicit"` to avoid unnecessary writes.
- `prompt_cache_retention` is replaced by `prompt_cache_options.ttl`.

Prompt-design consequence: keep stable content at the very start of the prompt *and* among the first parameters in the request body. Per-request context goes last.

---

## 7. Programmatic Tool Calling wiring

Add the `programmatic_tool_calling` tool and opt eligible tools in via `allowed_callers`. GPT-5.6 writes JavaScript that calls those tools in a hosted runtime, passing results between calls. It is ZDR-compatible with no additional container costs.

Your application must handle `program` items, program-issued function calls, and `program_output` items, preserving each call's `call_id` and `caller` linkage.

Tool descriptions should document expected return fields, types, and error behavior. If the model can't determine the return shape before writing the program, prefer direct tool calling.

Benchmark before adopting: compare task success, final-answer completeness, required evidence, total tokens, latency, and cost. Fewer calls, turns, or intermediate outputs are improvements only when the final answer still meets the quality bar.

---

## 8. Images

With `original` or `auto` detail, GPT-5.6 preserves original image dimensions instead of resizing to a patch budget or pixel limit. Large images can consume substantially more input tokens and add latency — set detail deliberately if you're passing large images at volume.

---

## 9. Safeguards and `safety_identifier`

Real-time cyber and biology misuse classifiers review outputs as they generate. Some requests get blocked; others pause mid-stream for several seconds while classifiers review. Safeguards can occasionally intervene on legitimate work, particularly in dual-use areas where defensive and offensive activity look similar early on — code review, vulnerability research, patch development, security education.

If your application serves individual end users, send a stable, privacy-preserving `safety_identifier` with each request.

---

## 10. Sample request

```python
response = client.responses.create(
    model="gpt-5.6-terra",
    reasoning={"effort": "medium"},          # start here, test one level lower
    text={"verbosity": "low"},               # global length dial
    instructions=SYSTEM_PROMPT,              # stable prefix — cacheable
    input=user_turn,                         # per-request content
    safety_identifier=hashed_user_id,        # if serving end users
)
```

Add `reasoning={"effort": "high", "mode": "pro"}` for quality-first work. Pin production to specific model snapshots and keep prompt builders in code near the feature they support — OpenAI is deprecating reusable prompt objects (de-emphasized from June 3 2026, `v1/prompts` shutting down November 30 2026).
