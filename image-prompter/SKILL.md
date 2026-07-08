---
name: image-prompter
description: Use when the user wants a prompt for AI image generation or editing — whether they provide an image or text. Triggers - sharing an image and asking for a prompt that recreates it ("reverse prompt", "image to prompt", "describe this for Midjourney/Flux/SDXL/DALL·E"), asking to optimize, rewrite, critique, or build an image prompt from a rough idea, or needing prompts for image edits, multi-image or reference workflows, text-in-image, localization, product mockups, logos, UI mockups, photorealism, diagrams, character consistency, or model-specific prompting for GPT Image, Gemini, Nano Banana, and similar image models.
---

# Image Prompter

## Overview

Turn the user's input — a provided image, a rough visual idea, or an existing draft prompt — into one optimized prompt they can paste into an image model. The deliverable is the prompt itself, not an image critique or a prompting lecture.

## Routing

| Input | Path |
|---|---|
| Image (attached or a readable path) + wants to recreate or reproduce it | Stage 1 (describe) → Stage 2 (optimize) |
| Image + wants to change, edit, or composite it | Stage 2 as an edit prompt; from the image, describe only the invariants to preserve |
| Text only (idea, draft prompt) | Stage 2 (optimize) |
| Mentions an image but none is present or readable | Ask for the image. Never invent a subject. |
| Several images | Ask which one — or for composite/consistency work, assign each image a role |

Stage 1 output is working material: fold it into the optimized prompt. Never deliver two prompts.

## Stage 1 — Describe the image

Read the image first; confirm it is actually present. Then draft an objective reconstruction description, weighted by importance: lead with a one-line gist (subject + shot + style), then cover:

1. **Subject** — form and build; for people: face, eyes, hair, skin, expression; for objects/products: shape, scale cues, material, surface finish.
2. **Clothing and accessories** — type, color, material, pattern, fit, notable details.
3. **Pose and gesture** — stance, hand positions, head tilt, eyeline, body language.
4. **Scene and environment** — background, surfaces, visible objects, fore/mid/background layering.
5. **Composition and framing** — camera angle, shot type, subject placement, aspect ratio if evident, depth of field.
6. **Lighting** — source, direction, quality (hard/soft), color temperature, shadows.
7. **Mood and atmosphere** — grounded adjectives.
8. **Overall style** — medium (photo, cinematic, 3D render, anime cel, flat illustration…) plus rendering cues (grain, bokeh, line weight, shading model).

Skip person-specific points for non-person subjects — the schema is a checklist, not a mandate.

Writing rules:
- **Definitive, no hedging.** Drop "appears to be" / "might be". For genuinely ambiguous details, commit to the most probable reading the image supports — but never invent details it doesn't.
- **No names.** Describe features; never identify a real person.
- **Weight by identity.** If a detail wouldn't change whether the regeneration reads as "the same image", it is low priority.

## Stage 2 — Optimize

1. Identify the task type: new generation, edit or variation, multi-image composite or reference-guided, text-in-image (poster, packaging, infographic, chart, diagram, UI mockup), or character/product/logo/brand consistency.
2. Extract the brief: intended output and audience; subject, action, setting, style, mood; composition, aspect ratio, camera, lighting, color; exact text or data; reference-image roles; what must change vs. stay invariant.
3. Ask at most two clarifying questions, only when the answer would materially change the prompt. Otherwise make conservative assumptions and state them in Notes.
4. Rewrite in a stable order, each slot present when relevant: operation verb (create, render, edit, replace, remove, translate, localize, composite, preserve) → subject and action → setting → composition and layout → style, lighting, color, texture, camera → constraints and invariants → exact text → reference roles → output parameters. The prompt's first word is the operation verb.

Rules:
- Replace quality filler ("8k", "masterpiece", "best quality", "epic") with concrete visual description; keep detail specific but not so dense it competes with the main subject.
- Positive framing for desired content; negatives only for known failure modes (extra text, watermarks, logos, extra fingers).
- Photorealism → real-camera language: photorealistic, natural light, believable imperfections, material texture, grounded scale.
- Text in image → quote the exact text, specify typography and placement, require verbatim spelling; spell unusual words letter by letter.
- Edits → "Change only X. Preserve Y." Repeat invariants in every follow-up edit.
- Multi-image → name each input by index and role, then how they interact.
- Factual, educational, or data-driven visuals → require accuracy and tell the user generated labels and numbers still need human verification.

## Reply format

The reply's first line is **Optimized prompt:** — Stage 1 analysis stays internal. Then, in order:

1. A fenced ```text block containing only the prompt, pasteable as-is.
2. **Suggested parameters:** — aspect ratio, quality settings, negative prompt, model flags, when useful.
3. **Notes:** — assumptions made, verification warnings, offers to reformat for a specific model.

Omit Suggested parameters and Notes when the user asks for only the prompt.

## Adapting to the target model

Default is natural-language prose (GPT Image, Gemini, Flux, SD3/SDXL, DALL·E, Imagen). Adjust when the user names a target:

- **Midjourney** — compact comma-separated phrases, strongest descriptors first, flags at the end (e.g. `--ar 3:4 --style raw`).
- **Booru-tag / anime models (NovelAI, Pony, Illustrious)** — comma-separated Danbooru-style tags ordered most → least defining.
- **Unknown target** — give prose and offer to reformat for a specific model.

## References

Load [references/prompt-patterns.md](references/prompt-patterns.md) when the task fits a reusable template: product mockups, logos, UI mockups, infographics, text rendering, localization, character consistency, image edits.

Load [references/model-notes.md](references/model-notes.md) when the user names a model family or needs parameters. Verify current official docs before relying on live API parameter names, model availability, or resolution limits.

## Quality check

- Recreation prompts would regenerate something recognizably the same image, lead with defining features, contain no hedges and no invented specifics, and name no individual.
- Optimized prompts keep the user's intent, separate what changes from what stays invariant, and avoid contradictory directions and style stacking.
- The fenced block is pasteable as-is, in the format matching the target model.
