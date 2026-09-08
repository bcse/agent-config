---
name: image-prompter
description: Create, rewrite, and optimize natural-language prompts for AI image generation from a text brief, a supplied image, or both. Use when the requested deliverable is prompt text for creating, recreating, editing, compositing, or restyling an image; for reverse prompting; for terse requests such as “what prompt recreates this?”; or when the skill is explicitly invoked with an image and no text. Do not use for direct image generation or editing, ordinary captions or alt text, OCR, visual critique, or identity recognition.
---

# Image Prompter

Turn text, images, or multiple prompts into one paste-ready image prompt. Resolve the inputs internally and describe the intended visual result directly.

## Choose the operation

Use this skill when the deliverable is prompt text. If the user requests an image itself, use the image-generation workflow.

- **Prompt optimization or merging:** Write a self-contained description of the final image that works without the input prompts or conversation history. Express revisions as final attributes: "The subject wears a blue jacket." Never mention source prompts, previous versions, or the optimization process. Avoid revision instructions such as "replace," "change," "instead of," "keep the original," or "as described above." Revising prompt text does not itself imply an image-editing task.
- **Standalone generation or reconstruction:** Describe the complete target without referring to the source image. Explicit invocation with an image and no accompanying text means standalone reconstruction.
- **Reference-guided edit or composite:** Use this operation only when the downstream generator will receive images to modify or combine. Identify each supplied image by a clear label or role. Specify the desired edits and preserved features. Image references and edit language are appropriate here; references to earlier prompt wording are not.

If a required image is unavailable, ask the user to attach it. Infer multiple images' roles from the request; ask one concise question only when competing assignments would materially change the result.

## Gather and resolve the visual brief

From text, extract the subject, action, wardrobe, setting, composition, visual treatment, lighting, palette, materials, intended use, exact text, and required final attributes. Translate meaningful tags, weights, and flags into natural-language descriptions.

When an image supplies visual evidence, read [references/image-analysis.md](references/image-analysis.md) completely before inspection. Inspect at sufficient detail to capture distinct supported visual features. Use salience to order details, not discard them. Describe ambiguous features only as specifically as the evidence permits.

Combine compatible requirements and resolve conflicts internally. Explicit user requirements outrank inferred details; later refinements outrank earlier wording; functional constraints outrank decorative cues. For remaining ties, choose the least expansive interpretation that preserves the core subject and intended use. Retain only the resolved requirements, not superseded alternatives.

Read [references/prompt-patterns.md](references/prompt-patterns.md) for reconstruction, edits, composites, exact text, products, diagrams, interfaces, character consistency, or complex new-image briefs. Adapt the applicable pattern to the output contract and fill every placeholder.

## Write the prompt

Lead with the image operation and defining subject. For optimization, merging, and standalone generation or reconstruction, begin with Create, Render, or Photograph.

Make placement, scale, composition, and spatial relationships concrete. Preserve required image text verbatim in quotation marks, including any words that would otherwise be inappropriate as prompt instructions.

Describe the desired appearance positively. Include brief exclusions only when they prevent a materially incorrect result. Add specificity only when supported by the inputs or necessary to express the requested result.

Remove duplication while preserving unique supported information consistent with the resolved brief. For complex reconstruction, retain category-by-category visual coverage even when the prompt becomes long.

## Output contract

Return only the final prompt as plain text. Include no code fence, quote block, preface, explanation, assumption report, tag list, weight syntax, generator parameter, or follow-up offer. A necessary input question under the operation rules is the only exception.

- **Simple brief:** Write one cohesive prose paragraph.
- **Complex brief or image reconstruction:** Begin with an opening image instruction, followed by applicable labeled prose sections in this order: Subject, Wardrobe and accessories, Pose and gesture, Environment, Composition and camera, Lighting, Mood and style, Constraints.

Use complete sentences within sections. Omit inapplicable sections without dropping relevant details. If the user explicitly requests variants, separate complete prompts with blank lines; each prompt must stand on its own.

## Completion check

Verify that the prompt satisfies the resolved brief, preserves required text exactly, makes important spatial relationships explicit, and follows the output contract.

For optimization, merging, and standalone reconstruction, test the prompt in isolation: a generator receiving only this text must have everything needed to depict the intended result. For reference-guided edits or composites, its only external dependencies may be the supplied images.