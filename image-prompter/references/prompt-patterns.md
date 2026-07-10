# Natural-Language Prompt Patterns

Use these structures as thinking scaffolds. Their code fences are documentation only; never reproduce a fence in the user-facing answer. Replace every bracketed field. For simple briefs, collapse the result into cohesive prose. For complex briefs and image reconstruction, keep the applicable labeled prose sections and preserve every distinct supported detail; remove only inapplicable placeholders and duplicated wording.

## New image

```text
Create a [orientation and use-case] image of [specific subject] [action or state] in [setting]. Frame the scene with [composition, viewpoint, placement, and depth]. Render it as [medium and visual treatment], lit by [lighting] with [palette, material, texture, and atmosphere]. Include [essential details] while keeping [critical exclusion] out of the scene.
```

Use one primary visual language and only a few supporting cues. Resolve incompatible style requests instead of stacking them.

## Standalone reconstruction from image evidence

Use this when the source image is evidence for writing a prompt, but the downstream generator should not need that image. The final prompt is a complete description of the target and never mentions a supplied, provided, original, source, or reference image.

```text
Create a [orientation and aspect ratio] [medium or deliverable] showing [one-sentence subject, action, setting, and style gist].

Subject: [Complete appearance or physical construction, including distinctive geometry, surface, face, eyes, hair, skin, expression, and condition where applicable.]

Wardrobe and accessories: [Every visible garment, material, fit, construction detail, wear pattern, accessory, and carried object.]

Pose and gesture: [Torso, head, gaze, shoulders, each visible limb and hand, stance, weight, movement, interaction, and occlusion.]

Environment: [Setting, architecture, materials, wear, foreground, middle ground, background, repeated structures, openings, and distinctive secondary objects.]

Composition and camera: [Crop, shot type, camera height and angle, subject placement, negative space, framing, visual rhythm, perspective, focus plane, depth of field, and aspect ratio.]

Lighting: [Source, direction, softness, temperature, highlight and shadow placement, material response, background exposure, and subject-background separation.]

Mood and style: [Atmosphere, palette, medium, realism, texture, grading, contrast, grain, and finish.]

Constraints: [Only evidence-based exclusions that prevent a known failure.]
```

Use every applicable section. Lead with defining evidence, but retain unique supporting evidence instead of shortening the prompt. Do not add unsupported details.

## Image edit

```text
Edit the supplied image by changing only [target] to [requested result]. Preserve [identity or form, pose, composition, background, viewpoint, lighting, palette, layout, text, and surrounding objects]. Integrate the change with matching scale, perspective, focus, material texture, reflections, and shadows so it belongs naturally in the original image.
```

Name both the change and the important invariants. Avoid vague instructions such as “keep everything the same” when drift would be costly.

## Multiple-reference composite

```text
Use the first image as the base [scene or composition], the second as the reference for [subject or object], and the third as the reference for [visual role]. Create [desired result] by placing [element] at [location and scale], preserving [base invariants] and matching perspective, lighting, shadows, color, focus, and texture across the composite.
```

Assign each reference one clear role by default. If the user explicitly assigns a reference multiple roles, honor them without inheriting unrelated content.

## Exact text or localization

```text
Create a [poster, package, sign, diagram, or interface] featuring the exact text “[TEXT]” with [typographic character, weight, case, color, and scale] at [precise placement]. Preserve the wording, spelling, punctuation, hierarchy, alignment, and spacing exactly, with no added copy. [For localization: Replace only “[SOURCE TEXT]” with “[TARGET TEXT]” while preserving every other visual element and the original layout.]
```

For multiple strings, give each exact string and its placement in a separate prose sentence. Include only the applicable localization sentence. For dense or production-critical copy, keep text large and visually distinct enough to verify in the generated result.

## Product or branded object

```text
Create a [use-case] image of [product] shown [position and angle] on [surface or setting]. Preserve [shape, proportions, packaging geometry, label, and exact text]. Use [lighting setup] to reveal [materials, texture, transparency, reflections, and contact shadows], with [background and palette] and enough negative space for [intended layout need]. Add no unrequested branding or copy.
```

## Diagram or infographic

```text
Create a [diagram or infographic] for [audience and purpose] on a [orientation] canvas. Organize it into [sections or regions] with [hierarchy, flow, axes, arrows, or legends]. Use the exact labels and data “[CONTENT]”, readable typography, consistent spacing, clear alignment, and [visual system]. Depict only the supplied facts and keep relationships unambiguous.
```

Supply exact facts, labels, and numbers in the prompt rather than asking an image generator to retrieve them.

## Interface mockup

```text
Create a realistic interface mockup for [product and platform] showing [specific screen or workflow]. Arrange [navigation, content regions, controls, and actions] with [density, hierarchy, spacing, and alignment], and show [realistic labels, data, and the relevant empty, loading, error, or success state]. Use [typographic, color, and component treatment] so the interface is coherent, readable, and ready for production rather than decorative concept art.
```

## Character consistency

```text
Use the supplied character as the visual anchor, preserving [face and body proportions, hairstyle, age range, outfit, palette, and distinctive traits]. Show the same character [new action] in [new setting], changing only [pose, action, expression, or environment] while keeping the character immediately recognizable. Match the established [medium, line treatment, lighting, and rendering finish].
```

Describe visible identity traits without trying to identify an unknown real person.
