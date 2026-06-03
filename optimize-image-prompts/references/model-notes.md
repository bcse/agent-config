# Model-Specific Notes

These notes are distilled from curated image-prompting guides. Treat live model names, API fields, and resolution limits as volatile; verify current official documentation when implementation depends on exact parameters.

## GPT Image Family

- Use a structured brief order for production prompts: background or scene, subject, key details, constraints, and intended use.
- For `gpt-image` style workflows, prompt format can be plain paragraphs, labeled blocks, JSON-like specs, or tag lists. Prefer the clearest, most maintainable format.
- For photorealism, include "photorealistic" or comparable real-camera language directly.
- For text-heavy images, diagrams, close portraits, identity-sensitive edits, and high-resolution outputs, consider higher quality settings when available.
- For edits, state exclusions and invariants explicitly: preserve identity, geometry, layout, brand elements, lighting, and camera angle.
- For small text, unusual names, labels, and brand copy, quote exact text and spell difficult words letter by letter.
- For multi-image input, identify each image by index and role, then describe the relationship between them.
- For iteration, prefer short single-change follow-ups and re-specify critical invariants when drift appears.

## Gemini And Nano Banana Style Workflows

- Start with a strong verb that names the operation: create, transform, replace, remove, localize, composite, render, or preserve.
- Use this base formula for new generation: subject + action + location/context + composition + style.
- Use this base formula for reference-guided generation: reference images + relationship instruction + new scenario.
- For edits, focus on the target change and explicitly state what should stay the same.
- For text rendering, quote the exact words, specify font style and placement, and ask for verbatim rendering.
- For localization, specify the target language or locale and require layout, hierarchy, and brand elements to remain intact.
- For real-world or current-information visuals, ask the model to retrieve or use current source data, then state how to translate that data visually. Verify final factual content.
- For creative direction, control lighting, camera angle, lens feel, color grading, film stock, materiality, and texture.
- For multi-image workflows, assign roles to reference images such as pose, style, character, product, texture, or background.

## Common Parameter Guidance

- Aspect ratio should match the use case: square for general assets, portrait for posters/social stories, landscape for slides/web banners, ultrawide for cinematic scenes.
- Resolution and quality should match risk: drafts can use faster/lower settings; final text-heavy, identity-sensitive, or detailed assets usually need higher quality.
- Do not rely on camera specs for exact simulation. Use them to communicate perspective, depth of field, and visual style.
- Avoid stacking too many styles. Pick one primary visual language and a few supporting cues.

## Known Failure Modes To Guard Against

- Text may be misspelled, duplicated, or reflowed. Use quotes, large readable typography, and manual verification.
- Edits can drift beyond the requested change. Use "change only X" and a preserve list.
- Composites can have mismatched shadows, perspective, scale, or lighting. Require these to match explicitly.
- Dense diagrams and infographics can contain factual or numerical errors. Provide exact labels/data and verify the output.
- Identity or character consistency can degrade across scenes. Use a reference anchor and repeat invariant traits.
- Transparent backgrounds may produce edge artifacts. Prefer clean opaque backgrounds unless the target tool reliably supports transparency.
