# Anti-patterns

Recognizable tells, why they fail, and the specific fix. Use this two ways: to repair work that feels generic or cluttered, and as a final scan of your own output before delivering. Sections: AI tells · Amateur tells · Process smells.

## AI tells

The patterns that make viewers say "this looks AI-generated." Each is legitimate *somewhere*; the tell is that it appears regardless of subject — a default wearing the costume of a choice.

**Purple-to-blue gradient hero (or teal-to-violet) on white.**
Why it fails: it is the statistical average of the last decade of SaaS marketing — it signals "no one made a decision here."
Fix: one confident accent drawn from the subject's own world, or a palette the subject earns (a soil-and-moss palette for a gardening tool says more than any gradient). If a gradient truly serves the direction, keep it subtle and same-hue, and be able to say why.

**Default face with no reason (Inter / Poppins / Roboto / Space Grotesk everywhere).**
Why it fails: typeface is the strongest single carrier of voice, and these carry "unset."
Fix: choose from the direction — an editorial serif for long-form authority, a humanist sans for warmth, a grotesk for technical neutrality, a slab or mono as a deliberate texture. Vary across projects; converging on the same "interesting" face every time is the same tell one layer deeper.

**Emoji as icons or bullets in professional artifacts.**
Why it fails: emoji rendering varies by platform, sits off-baseline, ignores your palette, and reads as filler enthusiasm.
Fix: one real icon family at one stroke weight, or typographic markers (numbers, en dashes, small caps labels) — or nothing; most bullet lists read better as plain text with proximity grouping.

**The identical card grid.** White cards, 1px border *and* shadow, 16px radius, icon–title–two-lines, times three or six.
Why it fails: it imposes equal visual weight on unequal content and is the single most recognizable AI layout.
Fix: let content rank the layout — one featured item treated differently, the rest as a quiet list; or replace boxes with rules and whitespace. Merge cards whose content is too thin to deserve a container.

**Everything centered, every section symmetrical.**
Why it fails: symmetry is inert — no tension, no reading path, every section interchangeable.
Fix: establish a strong left edge or a deliberate asymmetric grid; let one element break it on purpose. Alignment with one violation is composition; alignment with many is noise.

**Effect confetti.** Glassmorphism, glows, gradient text, floating blobs — several at once.
Why it fails: effects are emphasis, and emphasis everywhere is emphasis nowhere; it also dates the artifact to whatever year the effects trended.
Fix: an effects budget of one signature effect that serves the direction; everything else flat and quiet.

**Placeholder-speak copy.** "Empower your workflow." "Seamlessly unlock insights."
Why it fails: abstract verb + abstract noun communicates nothing, and copy is part of the design surface — generic words make even good layout feel templated.
Fix: concrete nouns and verbs from the actual subject. Write the real copy *before* styling; design around what is actually being said.

**Uniform 16px gaps between everything.**
Why it fails: spacing is how grouping is communicated; uniform gaps mean no grouping, so every element must be parsed alone.
Fix: proximity grammar — inner gaps at most half the outer gaps; whitespace between sections should be visibly larger than whitespace within them.

**Dark mode by inversion.** Pure black ground, pure white text, same saturated accents, same shadows.
Why it fails: white-on-black at full contrast halates; saturated accents glow; shadows disappear against black.
Fix: rebuild the neutral ramp (near-black ground, off-white text), desaturate and slightly lighten accents, swap shadows for subtle borders or lighter surface tints.

## Amateur tells

Not AI-specific — the classic gaps between untrained and trained eyes.

**Full-width text lines** on desktop → cap the measure at 45–75 characters; add a max-width and let the whitespace exist.

**Centered paragraphs** → left-align anything over two lines; centering is for short display moments.

**Pure black on pure white** → soften both ends (≈#1A1A1A on ≈#FAFAF8); conversely, gray-on-gray that fails 4.5:1 body contrast is the opposite failure — check both directions.

**Font pile-ups** → three-plus faces, adjacent weights (400 next to 500), faux bold/italic. Two faces, skipped weights, real styles.

**Near-miss alignment** → edges off by a few pixels, labels not sharing baselines with their values. Snap to the grid; align baselines, not bounding boxes.

**All emphasis levers on one element** → big + bold + colored + boxed reads as panic. Pick one or two levers; mute the neighbors instead.

**Shadow chaos** → multiple light directions, heavy dark blurs. One light source, low opacity, blur 2–3× offset.

**Inconsistent micro-decisions** → mixed corner radii, mixed icon sets, Title Case in one label and Sentence case in the next. These are the details people *feel* without naming; sweep for them last, every time.

**Chart crimes** → rainbow series palettes, 3D pies, dual axes without a warning, legends far from the data, bar axes that do not start at zero. Gray defaults + one highlight color, direct labels, honest axes.

**Trapped whitespace** → a huge accidental gap in one region while another is cramped. Redistribute deliberately; density should be a choice with a gradient, not an accident.

## Process smells

Failures upstream of the pixels — if one of these is true, fix it before styling anything.

- **Color arrived before hierarchy.** The design only communicates through color. Rebuild in grayscale until the structure works, then re-add color as emphasis.
- **Additions used as balance repair.** Something felt empty, so an element was added; repeat until cluttered. The corrective move is remove or realign, almost never add.
- **The direction cannot be stated.** If it does not fit in three adjectives and a reference world, there is no direction — the artifact will average toward the defaults above no matter how carefully each part is styled.
