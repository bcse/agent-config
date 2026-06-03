# Image Prompt Patterns

Use these templates as starting points. Keep only the fields that matter for the user's task.

## Text To Image

```text
Create [deliverable/use case]: [specific subject] [action or state] in [setting/context].
Composition: [framing, angle, viewpoint, layout, aspect ratio].
Style: [medium, genre, visual treatment].
Lighting and color: [light source, time of day, contrast, palette].
Details: [materials, textures, props, atmosphere].
Constraints: [must include], [must avoid], [no extra text/watermark/logos if relevant].
```

Good structure: subject + action + location/context + composition + style.

## Photorealistic Image

```text
Create a photorealistic image of [subject] [action] in [real-world setting].
Make it feel like a real camera capture: [camera distance/framing], [natural lighting],
[believable textures], [ordinary imperfections], [realistic scale and shadows].
Avoid staged studio polish unless requested.
```

Use camera and lens terms for look and framing, not as exact physics guarantees.

## Image Edit

```text
Edit the provided image. Change only [specific target/change].
Preserve [identity, pose, expression, background, camera angle, lighting, colors, layout,
labels, surrounding objects].
The edit should look natural, with matched perspective, shadows, texture, and focus.
Do not alter [critical invariants].
```

Use imperative language. Repeat invariants on each follow-up edit.

## Multi-Image Reference Or Composite

```text
Use Image 1 as [role: base scene/person/product].
Use Image 2 as [role: style/object/pose/background/material reference].
Create [new result] by [relationship instruction].
Place [element] at [location] with matching scale, perspective, lighting, shadows, and texture.
Preserve [base image invariants].
```

For many references, list each image by index and role before giving the final instruction.

## Text Rendering And Localization

```text
Create [poster/package/ad/diagram/UI image] with the exact text "[TEXT]".
Typography: [font style, weight, color, size, casing].
Placement: [top/center/bottom, alignment, spacing, hierarchy].
Render the text verbatim with no extra words or characters.
If localizing, translate only the specified text into [language/locale] while preserving layout,
visual hierarchy, and brand elements.
```

For dense text, ask for a clean layout, strong contrast, and large readable labels. Tell the user to manually verify spelling and translation.

## Infographic, Diagram, Chart, Or Slide Image

```text
Create a [infographic/diagram/chart/slide] for [audience] explaining [objective].
Canvas: [orientation/size/aspect ratio].
Structure: [sections, flow, panels, hierarchy].
Required labels/data: [exact labels, numbers, axes, legends].
Visual language: [clean flat vector, editorial, scientific, business presentation].
Constraints: readable typography, consistent icon style, clear arrows, enough white space,
factually accurate depiction of [topic].
```

Use high-fidelity settings when available for small text, legends, axes, or dense labels.

## Product Mockup Or Ecommerce Asset

```text
Create a polished product mockup of [product] for [use case/channel].
Preserve [logo/label/packaging geometry] exactly.
Lighting: [studio setup, contact shadow, reflections].
Surface/background: [plain opaque background, lifestyle setting, shelf, hand-held].
Material detail: [plastic, glass, metal, paper, fabric, ceramic].
Constraints: clean edges, no label distortion, no added branding, no extra text.
```

For extraction, prefer an opaque neutral background and use downstream background removal when transparent output is required.

## Logo Or Brand Mark

```text
Create [number] original logo concepts for [brand/product].
Brand personality: [traits].
Design constraints: simple, scalable, high-contrast, balanced negative space,
recognizable at small sizes.
Style direction: [geometric, monoline, typographic, mascot, emblem].
Avoid: complex gradients, tiny details, stock symbols, imitation of existing brands.
```

Ask for variations when exploration is useful.

## UI Mockup

```text
Create a realistic UI mockup for [product] showing [specific screen/workflow].
Layout: [navigation, content areas, controls, density, hierarchy].
Visual system: [platform, typography, spacing, color, component style].
Content: [realistic labels, data, states].
Constraints: looks like a shipped interface, not concept art; readable text; no decorative clutter.
```

Focus on interface hierarchy and real controls instead of illustrative language.

## Character Or Identity Consistency

```text
Use the reference character as the identity anchor.
Preserve [face, proportions, hairstyle, outfit, age, expression style, distinctive traits].
Create a new scene where the same character [action] in [setting].
Change only [pose/environment/action] while keeping the character recognizable.
```

For multi-scene work, establish a character anchor first, then reuse the same anchor details in each prompt.

## Iteration Prompts

Use small follow-ups:

```text
Keep everything else the same. Make only this change: [single change].
Preserve [critical invariants].
```

When output drifts, restate the full preserve list instead of relying on "same as before."
