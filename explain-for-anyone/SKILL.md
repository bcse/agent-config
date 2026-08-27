---
name: explain-for-anyone
description: Use when a user asks to explain an unfamiliar topic simply to an adult with no prior subject knowledge, or requests a plain-language, visual, or shareable beginner guide.
---

# Explain for anyone

Topic: $ARGUMENTS

## Purpose

Teach an adult newcomer as one adult helping another. Give the reader a correct mental model before adding the technical words that name it.

## Reader contract

- Assume no knowledge of the subject. You may assume ordinary adult life experience.
- Start from the question, choice, or problem that made the topic relevant to the reader.
- Use common words and short paragraphs. Keep a necessary technical term, define it in plain words at first use, then use the same term consistently.
- Use an analogy only as a bridge. Follow it with the literal mechanism and say where the analogy stops matching reality.
- Separate the core truth from exceptions and advanced detail. Keep each simple sentence as accurate as the fuller explanation beneath it.
- Verify unstable, disputed, or high-stakes claims before teaching them.

## Build the explainer

Use this shape and scale each part to the topic:

1. **Direct answer.** Answer the central question in one to three sentences without unexplained terms.
2. **Visual map.** Show the essential parts and how they relate. Give the visual one teaching job and state its main point in nearby text.
3. **Walkthrough.** Explain the mechanism in a natural order. Each step should introduce one new idea and connect it to the previous step.
4. **Concrete example.** Use a familiar situation, realistic numbers, or one end-to-end case. Map every part of an analogy back to the real subject.
5. **Practical meaning.** Explain what the reader can now notice, choose, do, or avoid. Add limits or common misconceptions only when they affect understanding.
6. **Recap.** End with a compact statement of what happens, why it matters, and the one distinction worth remembering.

## Default deliverable

Respect any format, length, or style the user requested. When the format is open, deliver a shareable HTML artifact. Keep it portable: use semantic HTML, embedded CSS, and inline SVG without remote runtime dependencies. If a generated bitmap genuinely helps, save it beside the HTML and use a relative path so the folder remains portable.

For any deliverable that supports visuals, read [references/visuals.md](references/visuals.md) before choosing or building them.

## Quality gate

Before finishing, check the rendered artifact and its words:

- The opening and first visual let a newcomer state the central idea in their own words.
- Every necessary term is defined before it carries part of the explanation.
- Each step supplies the background knowledge needed for the next.
- Every visual is legible on a small screen and at 200% zoom.
- Color is never the only carrier of meaning.
- A reader who cannot see an image gets the same essential information from visible text.
- The tone sounds like one adult helping another, with no baby talk or false simplicity.
- The saved artifact opens correctly and all local assets resolve.
