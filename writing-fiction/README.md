# Writing Fiction: Research and Maintenance Notes

This file records the evidence and design rationale behind the skill. It is not runtime guidance and is intentionally not referenced from `SKILL.md`.

The studies below describe corpus-level tendencies. They do not prove the origin of an individual passage and must not become quotas or bans.

## Narrative construction carries most of the signal

StoryScope analyzed 61,608 prompt-matched stories through 304 discourse-level features. Narrative features alone reached 93.2% macro-F1 for broad source classification and retained most of the performance of systems that also used stylistic cues. The strongest shared tendencies included explicit themes, tidy single-track plots, protagonist-led resolution, reduced moral ambiguity, and lower temporal complexity.

Design implication: repair disclosure, causality, ambiguity, and resolution before editing vocabulary or punctuation.

Source: [StoryScope: Investigating idiosyncrasies in AI fiction](https://arxiv.org/abs/2604.03136)

## Tension often collapses late

The 100-Endings method measures how predictable a story's actual ending becomes at each sentence. Generated stories retained some early ambiguity but became substantially easier to forecast late, while professionally published short fiction kept more alternatives alive. A constraint-based planning pipeline improved this tension measure without relying on surface edits.

Design implication: audit the story near three-quarters, delay explicit confirmation, and preserve information asymmetry.

Source: [Spoiler Alert: Narrative Forecasting as a Metric for Tension in LLM Storytelling](https://arxiv.org/abs/2604.09854)

## Default invention can be measured

A study of 20,000 generated stories found that 11 words appeared in 88.3% of them. The cluster included lighthouses, keepers, several recurring names, and a small set of professions that were uncommon in the comparison literature. The concentration crossed systems, suggesting shared post-training pressure rather than a single source text.

Design implication: inspect first-choice names, professions, settings, and central objects. Reconsider collisions; do not merely substitute from another static list.

Source: [Elias in the Lighthouse, Again? Diagnosing Low Diversity in LLM Stories](https://arxiv.org/abs/2605.26492)

## Post-training compresses variation

Matched continuation experiments across several fiction domains found progressively more uniform thematic transitions, less high-intensity affect, and narrower stylistic diversity after post-training. The compression was largest against professional literary fiction.

Design implication: preserve changes of register, emotional extremity, lopsided scene movement, and domain-specific texture when the manuscript supports them.

Source: [Narrative Flattening: How Post-Training Compresses Thematic, Affective, and Stylistic Variation in LLM Fiction](https://arxiv.org/abs/2605.27878)

## Surface signs are descriptive

Wikipedia's field guide emphasizes that stylistic signs are neither proof of authorship nor rules for prose. It highlights regression from odd specific facts toward generic inflated claims, significance language, vague attribution, promotional tone, synonym cycling, and summary conclusions. It also warns that simple verbs, repetition of the right noun, hedges, and other supposedly “unpolished” choices can be more characteristic of human writing in that domain.

Design implication: protect exact detail and established voice. Report patterns and effects, not detector verdicts.

Source: [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)

## Updating the skill

When revising operational guidance:

1. Prefer replicated behavioral evidence over detector folklore.
2. Keep corpus observations framed as priors, not universal rules.
3. Put only actionable instructions in `SKILL.md` or its referenced runtime files.
4. Keep provenance, discarded alternatives, and maintenance rationale here.
5. Re-run the writing evaluations and definition validation after behavioral changes.
