---
name: design-taste
description: Aesthetic judgment for any visual artifact — web UI, slides, posters, dashboards, charts, documents, diagrams. Use this skill whenever visual quality matters, even if the user never says the word "design" - when creating anything visual, when asked to make something "look better", "more professional", "less generic", "more polished", or "prettier", when restyling or theming existing work, and when reviewing or critiquing a design ("why does this look off?", "feedback on my landing page / deck / poster"). Also use it proactively to self-critique any visual artifact before delivering it.
---

# Design Taste

Taste feels like mystique, but it decomposes into three learnable moves:

1. **Commit** to one clear direction instead of averaging safe defaults.
2. **Execute** with a small, consistent system — few typefaces, few colors, one spacing scale.
3. **Diagnose** — look at the result, name what is off, and fix the biggest lever first.

Most bad design is not a wrong direction; it is the *absence* of one, plus inconsistency in the fundamentals. Fix those two things and almost any artifact looks intentional.

## Workflow when creating something visual

Work in this order. Each step constrains the next, and that chain of constraints is what makes the result cohesive rather than assembled.

**1. Direction — before any pixels or code.**
Name the direction in 2–3 adjectives ("warm, editorial, unhurried" / "dense, technical, precise") plus one reference world the subject actually lives in (lab notebooks, transit signage, vinyl sleeves, terminal UIs). If you cannot state the direction in one sentence, you do not have one yet — and no amount of styling will hide that. Derive it from the subject and audience, not from what is easy to render. When building web UI and a `frontend-design` skill is available, use that skill for direction and ideation; this skill supplies the craft rules and the critique pass.

**2. System — tokens before layout.**
Commit to: 1–2 typefaces with a type scale ratio, a palette of neutrals + one accent (two max), one spacing scale, one corner radius pair (small + large), one separation strategy (borders OR shadows OR background shifts). Writing these down first is what prevents drift — every later decision becomes a lookup instead of a fresh choice.

**3. Execute.**
Build with the system. When a value is not on the scale, that is a bug, not an adjustment. For detailed decisions (pairing type, tuning shadows, chart styling, per-medium rules for slides vs posters vs documents), read `references/fundamentals.md`.

**4. Self-critique — before delivering, every time.**
Run the four checks below. If any fail, fix and re-check. This pass is cheap and it is where most of the perceived quality comes from.

## The four checks

**Squint test.** Blur the artifact (mentally, or actually screenshot and blur). Does exactly one thing dominate? Do related items still read as groups? If everything blurs into even gray noise, hierarchy is missing; if three things fight for attention, de-emphasize two — muting the losers works better than amplifying the winner.

**Inventory count.** Count distinct typefaces, text sizes, colors, spacing values, corner radii, icon styles. Refined work uses startlingly few of each (often 2 faces, 4–5 sizes, 5–6 colors, 6–8 spacing values, 2 radii). High counts predict the vague "something's off" feeling more reliably than any single flaw, because every extra value is a small broken promise of consistency.

**Alignment sweep.** Trace the left edges, top edges, and baselines. Fewer alignment lines = calmer page. Anything off by a few pixels, or centered while its neighbors are left-aligned, gets snapped to the grid. Check optical alignment for icons and asymmetric shapes — visually centered beats mathematically centered.

**Swap test.** Could this artifact belong to any other product, topic, or company with only the logo changed? If yes, the direction never made it into the work. The fix is rarely "add more decoration" — it is pulling one signature element from the subject's own world and letting everything else stay quiet.

## Quick numbers

Defaults, not laws — deviate on purpose, not by accident.

| Decision | Default |
|---|---|
| Type scale ratio | 1.2 dense UI · 1.25–1.333 editorial · ~1.4+ slides |
| Body text | ≥16px web · line-height 1.5–1.7 · 45–75 char measure |
| Headings | line-height 1.1–1.25 · letter-spacing −1% to −3% when large |
| All-caps labels | letter-spacing +4% to +10% · never loosen lowercase body |
| Spacing scale | 4/8/12/16/24/32/48/64 (double it for slides & posters) |
| Grouping | gap inside a group ≤ ½ the gap between groups |
| Palette | neutrals do the work · ~60/30/10 · accent only on what matters most |
| Contrast | 4.5:1 body text · 3:1 large text & UI outlines |
| Shadows | small y-offset, blur ≈ 2–3× offset, ≤10% opacity, one light source |
| Motion | 120–250ms micro · 250–400ms transitions · ease-out in, ease-in out |

## When critiquing someone else's design

Do not free-associate observations. Read `references/critique.md` and follow its protocol: context first, first-impression capture, the four checks, then leverage-ordered passes, then at most three prioritized fixes phrased as observation → effect → cause → concrete change. Feedback that cannot be acted on without a follow-up question is not finished.

## When something "looks AI-generated" or amateur

Read `references/anti-patterns.md`. It is a diagnostic table of the recognizable tells — the default-gradient hero, the identical card grid, emoji-as-icons, uniform 16px gaps, rainbow charts — each with why it fails and the specific fix. Use it both to repair existing work and as a final scan of your own output.

## Reference files

- `references/fundamentals.md` — the craft layer: hierarchy, typography, spacing, color, depth, motion, charts, and per-medium rules with concrete numbers. Read when making detailed styling decisions or when a check fails and you need the underlying rule.
- `references/anti-patterns.md` — recognizable failure patterns and their fixes. Read when diagnosing work that feels generic, cluttered, or off.
- `references/critique.md` — the review protocol, critique vocabulary, and how to phrase feedback. Read before giving design feedback on anything.
