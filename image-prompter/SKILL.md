---
name: image-prompter
description: Create, rewrite, and optimize natural-language prompts for AI image generation from a text brief, a supplied image, or both. Use when the requested deliverable is prompt text for creating, recreating, editing, compositing, or restyling an image; for reverse prompting; for terse requests such as “what prompt recreates this?”; or when the skill is explicitly invoked with an image and no text. Do not use for direct image generation or editing, ordinary captions or alt text, OCR, visual critique, or identity recognition.
---

# Image Prompter

## Overview

Turn visual intent into one paste-ready prose prompt. Treat text optimization and image-guided prompting as the same synthesis task: gather evidence internally, resolve it, and return the optimized prompt without narrating intermediate analysis.

## Critical Output Contract

Return only the final prompt as plain text. Never wrap it in a Markdown code fence or quote block. Match its internal structure to the information density:

- **Simple brief:** one cohesive prose paragraph.
- **Complex brief or image reconstruction:** an opening creation instruction followed by applicable labeled prose sections in this order: `Subject`, `Wardrobe and accessories`, `Pose and gesture`, `Environment`, `Composition and camera`, `Lighting`, `Mood and style`, and `Constraints`.

Section labels organize the prompt; they are not analysis or commentary. Write complete natural-language sentences within every section. Omit only inapplicable sections, not supported visual details. If the user explicitly requests variants, separate complete prompts with blank lines.

Add no preface, explanation, assumptions, parameters, tag lists, weights, generator flags, or follow-up offer. Do not split image inspection and optimization into separate user-visible outputs.

## Workflow

1. **Classify the prompt operation.** Use this skill only when the deliverable is prompt text. Explicit invocation with an image and no accompanying text means: create a standalone reconstruction prompt. Otherwise distinguish:
   - **Standalone generation or reconstruction:** the final prompt must fully describe the target and work without access to the source image.
   - **Reference-guided edit or composite:** the final prompt may name supplied images because the downstream generator will receive them.
   - If the user wants an image produced or edited directly, use the image-generation workflow instead.

2. **Confirm usable inputs.** If the request depends on an image that is unavailable, ask the user to attach it. With multiple images, infer each role from the request; ask one concise question only when different role assignments would materially change the result.

3. **Build the visual brief internally.**
   - From text, preserve the core idea and extract the subject, action, setting, composition, visual treatment, lighting, palette, materials, exact text, requested changes, and invariants. Translate useful intent encoded in tags, weights, or flags into ordinary prose, then discard the syntax.
   - From an image, read [references/image-analysis.md](references/image-analysis.md) completely. Inspect the image at sufficient detail and carry the full supported evidence into the optimized prompt; use salience to order details, not prune them.
   - From text plus image, apply both sources in one pass. Explicit user instructions override conflicting reference details. Never return an image description and then offer to optimize it.

4. **Optimize without degrading fidelity.** Lead with the requested operation and defining subject. Order the remaining details by visual importance. Make composition and spatial relationships concrete, quote exact visible text, distinguish changes from preserved features, and remove verbal duplication without removing unique supported evidence. For image reconstruction, preserve category-by-category coverage even when the result is long. Resolve conflicts conservatively: explicit requirements outrank inferred details, later refinements outrank earlier rough wording, and functional constraints outrank decorative cues. When precedence remains tied, choose the least expansive interpretation that preserves the core subject and use case. Prefer positive descriptions; use brief exclusions only for a failure that would materially break the result.

5. **Use a focused pattern when helpful.** Read [references/prompt-patterns.md](references/prompt-patterns.md) for reconstruction, edits, composites, exact text, products, diagrams, interfaces, character consistency, or a complex new-image brief. Replace every placeholder and write natural-language prose; retain the labeled section structure for complex briefs and image reconstruction.

## Example

Input: `dreamy rooftop garden, fashion editorial, woman in red, sunset, cinematic, portrait crop`

Create a vertical high-fashion editorial portrait of a woman in a sculptural crimson gown standing in a rooftop garden at sunset.

Subject: The woman stands among wildflowers and trailing vines as a light breeze moves the gown's fabric and surrounding foliage.

Environment: Softly glowing city rooftops recede beyond the dense garden.

Composition and camera: Use a portrait crop, elegant subject placement, shallow depth of field, and enough environmental context to establish the rooftop setting.

Lighting: Warm golden light rims her silhouette through subtle atmospheric haze.

Mood and style: Refined cinematic color, rich natural texture, graceful motion, and the polished restraint of a luxury fashion campaign.

## Quality Gate

Before responding, confirm that the result:

- Preserves the user's intended subject, mood, use case, changes, and invariants.
- Resolves conflicting directions instead of repeating them.
- Front-loads the details that most strongly determine the image.
- Grounds image-derived claims in visible evidence and omits uncertain trivia.
- Retains every unique supported detail needed to reconstruct a complex source; optimization removes redundancy, not information.
- Preserves required text verbatim and makes important layout relationships explicit.
- Uses self-contained `Create`, `Render`, or `Photograph` wording for standalone reconstruction and reserves source-image wording for actual edit or composite prompts.
- Is plain text rather than a code block, with no surrounding commentary or model-specific syntax.
