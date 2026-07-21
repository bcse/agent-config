# Fundamentals

The craft layer: rules with numbers, and the reasoning behind them so you can break them deliberately. Sections: Hierarchy · Typography · Spacing & Layout · Color · Depth & Ornament · Motion · Charts & Data · Per-medium notes.

One tiering note before reading: the contrast floors, reduced-motion behavior, never-color-alone rule, and chart-honesty rules below are **requirements to verify**. Everything else in this file is a default to adapt or a preference to trade away when the direction — or a governing brand system — says otherwise.

## Hierarchy

One focal point per view, slide, or spread. If everything is emphasized, nothing is — and the fastest fix for a busy layout is not making the primary element louder, it is making everything else quieter.

Build at most three levels per screen: primary (exactly one thing), secondary (a few things), tertiary (everything else). Give each level a fixed treatment and reuse it; hierarchy is a system, not a per-element negotiation.

Emphasize with one or two levers at a time — size, weight, color, surrounding space, position. Stacking all five on one element (big AND bold AND red AND boxed) reads as shouting; using different levers for different peers reads as chaos. De-emphasis is the classier tool: softer gray, lighter weight, more distance.

Respect reading gravity. Text-heavy layouts are scanned in an F or Z pattern from the top left; hero moments read center-out. Put the focal point where the eye lands anyway, and only fight that gravity when the tension is the point.

## Typography

**Faces.** One typeface is safe; two is plenty. Pair by contrast — a characterful display face with a quiet text face, or serif against sans. Two similar faces of the same class (two geometric sans, say) read as a mistake rather than a pairing. Choose faces from the direction: a face carries a voice before a single word is read.

**Scale.** Pick a ratio and snap every size to it: 1.2 (minor third) for dense UI and dashboards, 1.25–1.333 for editorial and marketing pages, ~1.4–1.5 for slides because they are read at distance. Sizes off the scale are where visual noise comes from.

**Body settings.** Web body ≥16px. Line-height 1.5–1.7 for body text; tighten to 1.1–1.25 for large headings — big type set with body line-height looks like it is floating apart. Measure 45–75 characters per line, ~60 ideal. Full-width text on a desktop screen is the single most common legibility error in documents and websites.

**Letter-spacing.** Slightly negative on large display type (−1% to −3%): big glyphs optically drift apart. Positive on all-caps and small labels (+4% to +10%): capitals need air. Never loosen lowercase body text; it destroys word shapes.

**Weight.** Skip weights so contrast is legible: 400/600/700 reads clearly, 400/500 is mush. When space is tight, change weight before size — it creates hierarchy without breaking the layout.

**Craft details that read as care.** Real apostrophes and quotes (' " "), en and em dashes instead of hyphens, tabular (fixed-width) figures in any numeric column so digits align, no faux bold or faux italic. These are subliminal — nobody names them, everybody feels them.

**Centering.** Do not center more than about two lines of text. Centered body copy has ragged edges on both sides, which makes every line start in a different place; it belongs on wedding invitations, not interfaces or documents.

## Spacing & Layout

**One scale, used everywhere.** 4-based works for UI: 4/8/12/16/24/32/48/64. Double it for slides and posters. The scale is what makes a layout feel engineered — if a gap is not on the scale, treat it as a bug.

**Proximity is grammar.** The space inside a group must be visibly smaller than the space between groups — aim for the outer gap to be at least 2× the inner gap. Most layouts that feel "cluttered" actually have *uniform* gaps: nothing reads as belonging to anything, so the eye has to parse every element individually.

**Whitespace is material, not leftover.** More padding signals more importance and more luxury; density signals urgency or utility. Choose the density deliberately for the medium and audience — a data tool can be dense if it is consistent; a landing page earns trust with air. What kills a layout is *uneven* unintentional space: a giant trapped gap in one place and a cramped block in another.

**Alignment.** Fewer alignment lines = calmer page. Pick a grid (12 columns for web, 3–4 for slides), and let elements share edges. Mixing centered and left-aligned elements in the same region is the classic amateur tell. Optical beats mathematical: icons beside text, play triangles, and asymmetric marks need manual nudging until they *look* aligned — then stop trusting the ruler.

**Nesting.** Padding proportional to container size — big containers need big padding. For nested rounded rectangles, inner radius = outer radius − gap, or the corners visibly fight.

## Color

**Grayscale first.** Get the hierarchy working in black, white, and grays, then add color for meaning and emphasis. If the design only communicates because of color, the hierarchy is broken underneath — and it will fail for color-blind viewers and in print.

**Palette.** Neutrals do most of the work; one accent, two at the outside; roughly 60/30/10 dominant/secondary/accent. The accent is a scarce resource — spend it only on the most important thing (the primary action, the one number the slide exists for). An accent used everywhere is a neutral that happens to be loud.

**Neutrals with temperature.** Tint grays toward the accent hue or its complement instead of using pure gray — pure #808080-family neutrals are the strongest "default settings" smell in a palette.

**Not-quite-black on not-quite-white.** Pure black on pure white vibrates at reading sizes; something near #1A1A1A on something near #FAFAF8 reads as considered. In dark mode, avoid pure white text (~#E6E8E8 territory instead) and desaturate accents — saturated color glows harshly on dark grounds. Dark mode is a rebuild of the neutral ramp, not an inversion.

**Contrast floors.** 4.5:1 for body text, 3:1 for large text and UI outlines. Check the accent-on-white case explicitly: most brand colors fail it as text color, which is why accents belong in fills and graphics more than in prose.

**Meaning.** One hue keeps one meaning across the artifact (red is destructive everywhere, or nowhere). Never encode state in color alone — pair it with a label, icon, or weight change.

**Saturation vs area.** Inverse relationship: large areas take muted color; tiny areas (badges, rules, dots) can go loud. A saturated full-bleed background is a deliberate maximalist move, not a default.

## Depth & Ornament

**One separation strategy per surface.** Borders OR shadows OR background-shift — pick one as the default and use the others sparingly. Cards wearing all three at once are the number-one source of visual heaviness.

**Shadows that read as light, not dirt.** Small y-offset, blur ≈ 2–3× the offset, opacity ≤10% — e.g. `0 2px 8px rgba(0,0,0,.08)`. One consistent light source (all shadows fall the same way). Two elevation levels are enough for most interfaces; a third means something is genuinely floating (modals, menus).

**Radius is a voice.** 0 = editorial, technical, brutalist. 4–8px = neutral product. 12–24px = friendly consumer. Full pill = playful. Pick one small and one large value and stop; a screen with four different radii reads unconsidered even to people who cannot say why.

**Ornament must earn its place.** Decoration either carries information or builds the atmosphere the direction calls for; anything that could be deleted with zero loss should be. When a layout feels unbalanced, the instinct is to add something — the better move is almost always to remove or realign.

**Icons.** One family, one stroke weight, one size grid. A mixed icon set is instantly visible even to people with no design vocabulary.

## Motion

Micro-interactions 120–250ms; page and scene transitions 250–400ms. Slower does not read as luxurious, it reads as broken. Ease-out for entrances (fast start, soft landing), ease-in for exits, linear only for continuous loops like spinners.

Animate opacity and transform only; animating layout properties (width, height, top) stutters. Motion exists to explain causality — where did this panel come from, what did my click do — or to set atmosphere. One orchestrated moment (a staggered page-load reveal) lands harder than ten scattered wiggles. Always respect reduced-motion preferences.

## Charts & Data

The data is the hero; everything else is chrome. Maximize the share of ink that encodes data: drop chart backgrounds, heavy borders, redundant gridlines, and all 3D effects.

Gray is the default series color. Color highlights *the* series or *the* point the argument is about — a chart where every series is saturated is a chart with no argument. Label lines and bars directly where possible instead of using a legend the eye must ping-pong to.

Axis honesty: bar charts start at zero (bar length *is* the encoding); line charts may zoom the axis to show change, but say so. One chart, one claim — if the takeaway needs a paragraph, it needs a different chart or two charts.

## Per-medium gravity

**Slides.** One idea per slide. Use roughly twice the font size that feels natural on your screen — slides are read at distance, and 24pt is a floor for body text, not a target. Think poster logic (a glance) not document logic (a read); move the prose to speaker notes.

**Posters.** Design for three distances: the message legible at 5 meters (one element), scannable structure at 2 meters (a few), and rewarding detail at arm's length. If the 5-meter read fails, nothing else gets seen.

**Documents.** Measure and vertical rhythm dominate everything else. Headings take more space above than below so they visually attach to the text they introduce. One accent color maximum; documents earn authority through restraint.

**Dashboards & UI.** Density is fine when the scale is consistent. Alignment, tabular figures, and a disciplined hierarchy of grays matter far more than any flourish; the flourish budget goes to the one state or number users came for.
