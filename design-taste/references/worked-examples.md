# Worked examples

Two complete passes — one creation, one critique — showing how direction, system, the four checks, and the three-fix limit compose. Both are condensed transcripts of the *reasoning*; a real run produces the artifact itself.

## Creation: seed pitch deck

**Brief.** "Make our 10-slide seed deck for a battery-recycling startup look investor-ready." A slide skill handles the deck mechanics; this skill supplies the pass below.

**1. Direction.** First instinct — near-black background, acid-green accent, techno grotesk — failed the swap test before a single slide existed: it is the current default costume for "clean-tech deck" and could belong to any of fifty companies. Revised direction: *industrial, optimistic, precise*, drawn from the subject's own world — materials science, sorted metal fractions, plant-floor signage.

**2. System.**
- Type: one grotesk display + one humanist text face; slide scale ≈1.45; 30pt body floor, 44pt claims.
- Palette: paper-white ground, graphite ink, a single copper accent (the metal being recovered), spent only on the one number each slide exists for.
- Spacing: 8-based, doubled for the medium (16/32/64/128). Radius 0 — industrial. Separation by hairline rules, not shadows.
- Signature: a thin "material flow" line running through every footer, marking where the story sits in the input → recovery → output chain.

**3. Execute.** One claim per slide at 44pt; supporting prose moved to speaker notes. Data slides: gray series with the copper highlight on the series being argued, direct labels, zero-based bars.

**4. Checks.**
- *Squint:* every slide blurs to one dominant claim plus one visual — pass.
- *Inventory:* 2 faces, 5 sizes, 4 colors, 5 spacing values, 1 radius — pass.
- *Alignment:* all slides share one left margin and a baseline grid; two captions were off it — snapped, pass.
- *Swap:* the copper accent and material-flow footer only make sense for this company — pass.

Requirement verification before delivery: graphite on paper-white computed at 13.9:1; copper as text on white computed at 3.2:1 — passes only at large sizes, so copper stays in fills, rules, and 44pt claims, never in body text.

## Critique: ops dashboard

**Brief.** "Feedback on this warehouse-ops dashboard my teammate built?" Screenshot provided — so the critique is of rendered output, not code. Context gathered: internal tool, checked hourly by ops leads, working draft.

**0–1. Context and first impression.** Working draft → structural feedback is fair game; polish nits are premature. Five-second read: the eye lands on a rainbow chart legend, top right; the exception counts — the reason the screen exists — read last.

**2–3. Squint and inventory.** Blurred, nothing dominates: the KPI row and the chart block carry equal weight. Counts: 3 typefaces (one default sans slipped into tooltips), 9 colors, spacing values of 8/10/12/14/16/18/24.

**4–5. Passes and swap.** Hierarchy and spacing carry the biggest problems; typography and color mostly inherit from them, so feedback stops at the highest broken layers. Swap test: could be any ops tool — acceptable for an internal draft; noted, not prioritized.

**Delivered feedback.**

Keep: the two-panel structure — summary row above, detail table below — matches how the leads actually work (glance, then drill). Don't lose it while fixing the rest.

1. Nothing outranks anything (observation), so an operator cannot find the exception count in one glance (effect). The KPI row and the chart share size and weight (cause). Make the exceptions KPI the single primary — roughly 2× number size, ink-dark — and drop the other KPIs to gray labels with tabular figures (fix).
2. Every chart series is saturated (observation), so the chart argues nothing (effect). The palette is the charting library's default (cause). Gray for all series, the alert series in the one accent, direct labels replacing the legend (fix).
3. Gaps run 8/10/12/14/16/18 (observation), which makes the panels feel untidy even where the content is fine (effect); values were chosen ad hoc per widget (cause). Snap to 8/16/24/32 with inner gaps at most half the outer gaps (fix).

Minor, take or leave: unify on one sans (tooltips differ); tabular figures for timestamps; two radii → one.

Requirement note, measured not estimated: the proposed gray labels compute to 4.6:1 on this background — passes; the accent computes to 2.9:1 as text — fails, so it stays in fills and chart marks only.
