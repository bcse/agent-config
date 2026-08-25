---
name: create-draft-pr
description: End-to-end pull request routine — open a draft PR, then iterate with GitHub Copilot's automated review until it stops finding things. Use when creating a PR, when asked to "run the PR routine" or "take this through review", or when driving an existing PR through automated review rounds to a clean state.
---

# PR Routine

Open a draft PR, then loop with Copilot's automated review until a round produces nothing new.

```
1. $write-pr       -> create draft PR
2. wait            -> Copilot posts its review (~5 min, sometimes longer)
3. read            -> collect root-level inline findings; ignore suppressed ones
4. validate        -> $receiving-code-review; verify each claim yourself
5. fix             -> cohesive commits, one per finding or coherent group
6. push + reply    -> reply in-thread, name the SHA
7. goto 2          -> until a round adds no new findings; stays in draft
```

Steps 3 and 6 are where this goes wrong in practice — the comments are not where they look like they should be, and replies land in the wrong place. Those sections are the reason this skill exists.

## 1. Open the draft PR

Before creating, confirm the branch is pushed, in sync, and carries only commits that belong to this PR:

```bash
git rev-list --left-right --count @{u}...HEAD    # want "0  0"
git log --oneline <base>..HEAD                   # every line must belong here
```

An unrelated doc or config commit riding along costs a reviewer's attention and muddies the diff. Move it to its own branch before opening.

Use `$write-pr` for the title and body, then:

```bash
gh pr create --draft --base master --head "$(git branch --show-current)" \
  --title "fix(scope): Imperative summary" --body-file pr-body.md
```

Draft on purpose: Copilot reviews drafts, so the automated rounds finish before a human is invited in. It stays a draft when the loop ends, too — see step 7.

## 2. Wait for the review

Never foreground-sleep. Poll in the background and get one notification when something new lands:

```bash
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
PR=645
SEEN=.git/pr-$PR-seen.txt; touch "$SEEN"     # ids already handled

for _ in $(seq 40); do                        # ~20 min ceiling
  gh api "repos/$REPO/pulls/$PR/comments" --paginate \
      --jq '.[] | select(.in_reply_to_id == null) | .id' \
    | grep -vxFf "$SEEN" | grep -q . && break
  sleep 30
done
```

Run it with `run_in_background: true`. If the first 5 minutes are quiet, give it another 5 — the first review on a large diff is routinely slower than on later rounds.

## 3. Read the findings

**`gh pr view --json comments` returns `[]` for review comments.** It reads the issue-comment timeline; Copilot's findings are pull-request *review* comments and live on a different endpoint. Looking only there reads as "no feedback" when there are findings waiting.

Two surfaces, both worth reading:

```bash
# The overview Copilot posts (file table, what it reviewed, how many comments).
# Splitting on "<details>" drops the suppressed-comments block — see below.
gh pr view "$PR" --json reviews \
  --jq '.reviews[] | {author: .author.login, state, body: (.body | split("<details>")[0])}'

# The actual findings
gh api "repos/$REPO/pulls/$PR/comments" --paginate \
  --jq '.[] | {id, user: .user.login, path, line, in_reply_to_id, body}'
```

- Root findings have `in_reply_to_id: null`. Your own replies come back in the same list — filter them out or you will re-answer yourself.
- **Do not truncate this output.** No `| head`, and skip any wrapper that caps stdout: comment bodies get cut mid-sentence and you act on half a finding. Pull one body in full with
  `gh api "repos/$REPO/pulls/comments/$ID" --jq '.body'`.
- Record handled ids into `$SEEN` as you go, so step 2 only wakes you for genuinely new ones.

**Ignore suppressed comments.** Copilot's review body often ends with a collapsed `<details><summary>Suppressed comments (N)</summary>` block, typically labelled "Previously missed — in code that hasn't changed since the last review". Those are not input to this loop. Copilot withheld them itself, they carry no comment id and so have no thread to answer in, and they target code the round did not touch — so working them turns a converging loop into an open-ended audit of the entire diff, growing the change set every round and delaying the human review the routine exists to reach. Do not fix them, do not reply to them, do not count them as findings.

Only the inline comments from the `pulls/$PR/comments` endpoint drive steps 4 through 7. If a suppressed item names something you believe is a genuine defect, that is separate work: finish the loop first, then raise it on its own.

Also check whether tests actually run on this PR:

```bash
gh pr view "$PR" --json statusCheckRollup --jq '[.statusCheckRollup[] | {name, conclusion}]'
```

If no test job appears, say so when you report — a green PR page is not a green suite, and your local run is the only evidence there is.

## 4. Validate before fixing

Load `$receiving-code-review` and follow it. The short version: verify each claim against the code before touching anything, and push back with reasoning when it does not hold.

Copilot is right often enough to take seriously and wrong often enough that you must check. From one real run of this loop, three findings:

| Finding | Verdict |
|---|---|
| A captured local went stale after an in-place refresh | Real bug, and worse than described — the staleness outlived the retry |
| An error payload reached API consumers via a store the raise site never mentions | Real, and the most severe of the three — and it only appeared in **round 2** |
| An un-awaited cancelled task "keeps this test flaky" | Cause did not hold — but a genuine unrelated defect sat on the same line |

Three lessons in that table:

- **The worst finding can arrive late.** Do not stop after round 1 because round 1 looked minor.
- **A wrong reason can still point at a bad line.** When you refute the stated cause, read the line anyway before moving on.
- **Claims about reachability deserve a probe, not reasoning.** Trace the path and run something.

When you refute, say so in-thread with the evidence, and fix the nearby real defect if there is one. Do not implement a change whose justification you know to be wrong.

## 5. Fix in cohesive commits

One commit per finding or per coherent group — never one squashed catch-all. The reviewer needs to see which change answers which comment, and a bad call has to be revertible on its own.

Prove each fix rather than asserting it:

```bash
# 1. write the test, confirm it fails against the current code
# 2. apply the fix, confirm it passes
# 3. revert the fix, confirm the test fails again, restore
```

That third step is what separates a test that pins the regression from one that merely passes. Run the project's full baseline suite before pushing, and put the numbers in the commit body.

## 6. Push and reply

Reply **in the thread**, not as a top-level PR comment — a top-level reply orphans the discussion from the line it is about:

```bash
gh api "repos/$REPO/pulls/$PR/comments/$COMMENT_ID/replies" -F body=@reply.txt
```

`-F`, not `-f`. With `-f` the comment body posts as the literal string `@reply.txt`. See `$gh-api-file-body-flag`.

A good reply names the commit SHA, states what was verified and how, and is explicit when you disagreed. Include the evidence — the failing assertion, the probe output — rather than claiming the check happened.

Update the PR body in the same pass when the change set moved:

```bash
gh pr edit "$PR" --body-file pr-body.md
```

## 7. Loop

Copilot re-reviews on every push and surfaces different things each round, so returning to step 2 is the point of the routine, not a formality.

Terminate when a round adds no new root-level inline comments. A review whose only content is a suppressed-comments block is a clean round — end the loop. Distinguish a clean round from "it has not reviewed yet" — compare the newest review against the current head:

```bash
gh pr view "$PR" --json headRefOid,reviews \
  --jq '{head: .headRefOid, last_review: (.reviews | last | .submittedAt)}'
```

When the loop is done, report: rounds run, findings per round, which you accepted and which you refuted and why, the verification evidence, and whether CI ran tests.

**Leave the PR in draft.** Do not run `gh pr ready`. Inviting human reviewers is the author's call — they may want another look at the diff, a live test run, or a decision on something you escalated before anyone is notified. Say the loop is clean and that the PR is ready to un-draft whenever they choose.

## Guardrails

- Every fix is scoped to the finding. A review comment is not license to refactor.
- Only inline review comments are findings. Suppressed comments are out of scope for the loop.
- Never widen a client-facing surface to satisfy an observability request — check where an error message or payload actually travels before enriching it.
- Keep unrelated commits off the branch for the whole loop, not just at creation.
- Never report the loop as clean on a round you did not actually read.
