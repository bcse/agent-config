---
name: optimize-image-prompts
description: Optimize, rewrite, critique, or build prompts for AI image generation and image editing. Use when the user asks to improve an image prompt, turn a rough visual idea into a stronger prompt, adapt prompts for text-to-image, image editing, multi-image or reference-image workflows, text-in-image, localization, product mockups, logos, photorealism, diagrams, UI mockups, character consistency, or model-specific prompting for GPT Image, Gemini, Nano Banana, or similar image models.
---

# Optimize Image Prompts

## Overview

Use this skill to convert rough visual intent into clear, controllable image prompts. Preserve the user's core idea while adding only the details that improve generation, editing, composition, text fidelity, and iteration.

## Core Workflow

1. Identify the task type:
   - New image generation
   - Image edit or variation
   - Multi-image composition or reference-guided generation
   - Text-in-image, poster, packaging, infographic, chart, diagram, or UI mockup
   - Character, identity, product, logo, or brand consistency workflow

2. Extract or infer the core brief:
   - Intended output and audience
   - Subject, action, setting, style, mood, and use case
   - Composition, aspect ratio, camera angle, lighting, materiality, and color
   - Required text, labels, data, or factual constraints
   - Input image roles, if references are attached
   - What must change and what must remain unchanged

3. Ask at most two clarifying questions only when missing information would materially change the prompt. Otherwise make conservative assumptions and state them briefly.

4. Rewrite the prompt with a strong operation verb and a stable structure:
   - Operation: create, render, edit, replace, remove, translate, localize, composite, preserve
   - Subject and action
   - Setting and context
   - Composition and layout
   - Style, medium, lighting, color, texture, and camera cues
   - Constraints and invariants
   - Text instructions, if any
   - Reference image role assignments, if any
   - Output parameters, if the user needs them

5. Return the prompt in the format most useful for the user's next step. Prefer this default:

```text
Optimized prompt:
...

Suggested parameters:
...

Notes:
...
```

Omit parameters or notes when the user asks for only the prompt.

## Prompting Rules

- Be specific enough to guide the model, but do not overload the prompt with decorative detail that competes with the main subject.
- Use positive framing for desired content. Use negative constraints only for known failure modes such as extra text, watermarks, logos, extra fingers, or unwanted objects.
- Include the intended deliverable when it changes the output quality target: ad, product mockup, educational diagram, app screen, storyboard, poster, logo sheet, ecommerce photo, or print asset.
- For photorealism, use direct photographic cues: photorealistic, real camera capture, natural light, believable imperfections, material texture, and grounded scale.
- For layout-sensitive work, specify placement, hierarchy, margins, negative space, and canvas orientation.
- For people, specify body framing, pose, gaze, hands, object interactions, and identity-preservation requirements.
- For text in images, quote the exact text, describe typography and placement, and require verbatim spelling. For unusual words, spell them letter by letter.
- For edits, use direct imperative language: "Change only X. Preserve Y." Repeat invariants in every follow-up edit to reduce drift.
- For multi-image prompts, name each input by index and role, then describe how the references interact.
- For factual, educational, medical, historical, or data-driven visuals, require accuracy and tell the user that generated labels, diagrams, and numbers still need human verification.

## Reference Selection

Load [references/prompt-patterns.md](references/prompt-patterns.md) when the task needs a reusable template, such as product mockups, logos, UI mockups, infographics, text rendering, localization, character consistency, or image edits.

Load [references/model-notes.md](references/model-notes.md) when the user names a model family, asks for parameters, or needs model-specific guidance for GPT Image, Gemini, Nano Banana, or comparable image-generation models. Verify current official docs before relying on live API parameter names, model availability, or resolution limits.

## Quality Check

Before responding, check that the optimized prompt:

- Keeps the user's original intent intact
- Separates what changes from what must remain invariant
- Includes composition, lighting, style, and constraints only where useful
- Handles exact text, reference images, and factual requirements explicitly
- Avoids contradictory directions and excessive style stacking
- Gives the user a prompt they can paste directly into an image model
