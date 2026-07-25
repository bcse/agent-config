# Continuity Ledger for Long Fiction

Use this reference for novels, series, novellas drafted across sessions, and manuscript continuations with substantial prior context.

The ledger is durable working state, not passive notes and not an outline to obey blindly. Its purpose is to let a later session recover exactly what has been established, what remains planned, what must be checked, and where drafting should resume.

## Contents

- [Authority and location](#authority-and-location)
- [Ledger cycle](#ledger-cycle)
- [Ledger template](#ledger-template)
- [Foreshadowing lifecycle](#foreshadowing-lifecycle)
- [Drift checks](#drift-checks)
- [Recovery after interruption](#recovery-after-interruption)

## Authority and location

Use this precedence when records disagree:

1. Explicit user correction
2. Current manuscript
3. Ledger entry backed by a manuscript source
4. Deliberate plan
5. Inference

Never promote a plan or inference into `CANON`. Mark unsupported facts `unknown`.

Before creating a ledger, look for an existing story bible, continuity file, or project convention. Extend it with the minimum missing fields rather than replacing it. Otherwise create `continuity-ledger.md` beside the manuscript or at the fiction project's root. Keep one ledger for the work; do not create a new one per chapter.

When file access is available, read and update the ledger file rather than relying on conversation memory. Without file access, maintain the same structure in working context and surface a handoff copy only when requested or needed for continuation.

## Ledger cycle

Run the cycle for every chapter or substantial scene.

### 1. Locate or reconstruct

Before drafting:

1. Read the existing ledger.
2. If none exists, reconstruct one only from supplied manuscript evidence and explicit user plans.
3. Give established entries a source such as chapter, scene, or distinctive textual anchor.
4. Record contradictions instead of silently choosing a version.
5. Stop reconstruction at the latest available text; do not invent connective canon.

### 2. Open the current unit

Read only the ledger slices needed for the unit:

- `BOOK CONTRACT`, `VOICE`, and `BOUNDARIES`
- participating characters and their knowledge limits
- recent causal and relationship state
- open promises and foreshadowing whose window is near
- relevant `SPENT` entries

Fill `CURRENT UNIT` before drafting. Its fields are the handoff contract for this unit. Set its status to `planned`; once prose exists, set it to `drafted`.

### 3. Draft from the handoff

Draft one unit. Do not resolve an `unknown` merely to simplify the scene. Mention a foreshadowing ID in `CURRENT UNIT` only when the unit will plant, echo, pay, subvert, or retire it.

### 4. Audit the finished unit

Before opening another unit, verify:

- the entry state, turn, exit state, and carried uncertainty match the prose
- every new fact and knowledge transfer has on-page support
- character, timeline, relationship, and genre boundaries still hold
- a plant is perceptible under an innocent surface reading
- an echo changes pressure or interpretation rather than merely repeating an image
- a payoff is traceable to fair prior evidence

If the audit fails, revise the prose or mark the conflict. Do not edit the ledger to make a contradiction disappear.

### 5. Commit the new state

Immediately after the audit:

1. Reread the final prose, not the pre-draft plan.
2. Update canon, knowledge, event chain, timeline, relationships, pressure, open promises, and spent details.
3. Advance `planted`, `echoed`, `paid`, or `subverted` only for actions that occurred on the page; add the source.
4. Mark an abandoned plan `retired` with the editorial reason; do not present it as a historical fact.
5. Add the unit to `UNIT LOG`, name the uncertainty it carries, and set `CURRENT UNIT` to `checked`.

Mark a unit `checked` only when the prose exists and all five ledger updates above are complete. On the next cycle, replace `CURRENT UNIT` only after its checked result appears in `UNIT LOG`.

## Ledger template

Use `WITHHELD` for who lacks information, `OPEN PROMISES` for reader-facing obligations, and `FORESHADOWING` for the evidence-and-payoff lifecycle. When one thread spans sections, give it a `FORESHADOWING` ID and reference that ID elsewhere instead of duplicating its history.

```text
BOOK CONTRACT
genre promise | audience/rating | realism rules | ending obligations

VOICE
60-100 words of established prose
POV | tense | psychic distance | diction boundary | recurring syntax

CAST
name | role | present desire | leverage | false belief or evasion
what changed most recently | what this person cannot know

CANON
fact | source chapter/scene | who knows it | whether the reader knows it

EVENT CHAIN
event -> consequence | why the consequence follows | unresolved fallout

WITHHELD
information | withheld from whom | reason it remains unavailable
earliest fair clue | intended payout window | alternate interpretation

TIMELINE
story time | told order | duration | age/date anchors | time jumps

RELATIONSHIPS
pair | current alignment | pressure point | last irreversible change

PRESSURE
chapter/scene | 1-5 pressure | source of pressure | release or reversal

OPEN PROMISES
question/thread | first planted | latest development | must close?

FORESHADOWING
id | kind: clue/setup/motif/promise | plant and source | surface reading
latent possibility | who knows | what reader knows | intended window
status | latest echo/source | next action

SPENT
names | professions | settings | objects | images | gestures | revelations

BOUNDARIES
facts or choices the next chapter must not contradict

CURRENT UNIT
unit | status: planned/drafted/checked | POV | story time and place
entry state | intended turn | intended exit state | carried uncertainty
threads advanced | foreshadowing action and ID | knowledge limits | boundaries

UNIT LOG
unit | manuscript source | exit state | foreshadowing changed
new canon or knowledge | open carry | ledger checked?
```

Keep the ledger compact. Store source pointers and short anchors, not copied scenes.

## Foreshadowing lifecycle

Give each thread a stable ID such as `F01`. Do not renumber IDs when chapters move.

| Status | Meaning | Required evidence or action |
|---|---|---|
| `planned` | Intended but absent from the manuscript | Keep outside canon; name the intended window |
| `planted` | First fair trace exists on the page | Record source, surface reading, and latent possibility |
| `echoed` | A later trace renews or alters pressure | Record source and what changed; repetition alone does not qualify |
| `paid` | The expected significance becomes consequential | Link payoff to its prior plant and echoes |
| `subverted` | A fair alternate reading becomes consequential | Show why the earlier evidence supports both readings |
| `retired` | Deliberately abandoned or invalidated | Record why; remove any dependent plan |

At each unit, choose deliberately among advance, hold, or pay. Not every open thread should appear in every chapter. If a planned payoff changes, update the plan while preserving the factual record of what readers have already seen.

## Drift checks

Run at chapter boundaries and across the manuscript around 25%, 50%, and 75%.

| Drift | Evidence | Correction |
|---|---|---|
| Voice | Chapter cannot sit beside the VOICE sample without a register jump | Re-derive the noticing, judgment, distance, and syntax |
| Canon | A fact, date, object, or relationship changed without an event | Restore canon or dramatize the change |
| Knowledge | A character acts on information they cannot possess | Add a transmission event or remove the knowledge |
| Disclosure | WITHHELD items are explained early or forgotten | Rebuild the clue and payout schedule |
| Causality | Episodes could be reordered without effect | Add consequences that constrain later choices |
| Pressure | Scores stay flat or only rise one step at a time | Add release, reversal, delay, or a different pressure source |
| Relationship | Characters reset after conflict | Carry the irreversible interpersonal change forward |
| Motif | The same image or gesture returns without development | Transform it, retire it, or make the recurrence consequential |
| Genre | The book stops delivering its central promise | Reassert the contract in the next meaningful unit |

## Recovery after interruption

On resumption:

1. Read the ledger before generating new prose.
2. Find `CURRENT UNIT` and the latest `UNIT LOG` entry.
3. If status is `planned`, first check whether that unit already exists in the manuscript. If it exists, set it to `drafted` and audit it; otherwise verify the brief and draft it.
4. If status is `drafted`, audit and commit its state before continuing.
5. If status is `checked`, begin the next unit; do not redraft it.
6. Reconcile later user edits against the ledger before trusting either.

The ledger is a recovery map, not proof. When its sourced record conflicts with the manuscript, inspect the cited passage and repair the ledger. When the source leaves a fact ambiguous, keep it unknown. Require on-page authorization before crossing an established realism, style, or genre boundary.
