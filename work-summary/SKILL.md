---
name: work-summary
description: Use when asked to summarize recent work over a date range, such as "what did I do", "weekly report", "standup update", "activity since Friday", "this week", manager updates, or retrospectives across local repositories.
---

# Work Summary

## Goal

Produce a concise, evidence-backed activity report for a person over a date
range. Prefer local git evidence first, then use session, PR, or issue context
only when it helps explain work that commits do not capture.

## Inputs

Resolve these from the request. Ask only if the missing value would materially
change the report.

- **Author**: name or email. Default to the user's known git author if available;
  otherwise infer from recent commits and state the assumption.
- **Date range**: absolute dates or relative ranges such as "since last Friday",
  "this week", or "from 5/8 to today". Resolve relative dates in the user's
  timezone before querying.
- **Scope**: default to `/Volumes/Predator/Users/bcse/Documents` unless the user
  names a repo or folder.
- **Sources**: default to committed git history. Include uncommitted work,
  stashes, Codex sessions, PRs, or issues only when requested or needed to
  explain non-commit activity.

## Procedure

1. **Normalize the range.**
   - Convert relative dates to exact dates.
   - State inclusivity, for example "including Friday, May 15, 2026".
   - Convert the result to `--since` and `--until` values for `git log`.

2. **Discover repositories.**
   - Search the requested scope for git repositories.
   - Include these known project directories when no narrower scope is given:
     `/Volumes/Predator/Users/bcse/Documents/editing_copilot`,
     `/Volumes/Predator/Users/bcse/Documents/copilot_cli`,
     `/Volumes/Predator/Users/bcse/Documents/copilot_cli_test`,
     `/Volumes/Predator/Users/bcse/Documents/makeup_bestie`,
     `/Volumes/Predator/Users/bcse/Documents/portfolio`, and
     `/Volumes/Predator/Users/bcse/Documents/YMK/pft-flutter-common`.
   - Skip vendor, dependency, build, cache, and inaccessible directories.
   - Report how many repositories were scanned.

3. **Collect git evidence.** For each repo, use the same author and date filters
   throughout the report:
   ```
   git -C {repo} log --all --author="{author}" --since="{start}" --until="{end}" \
       --format="%h%x09%ad%x09%D%x09%s" --date=short --no-merges
   ```
   For touched areas, collect file names from the same commit set:
   ```
   git -C {repo} log --all --author="{author}" --since="{start}" --until="{end}" \
       --name-only --format="commit %h %ad %s" --date=short --no-merges
   ```
   If line counts are useful, compute them from `git log --numstat` over that
   same filtered commit set. Do not use the working tree diff as date-range
   evidence.

4. **Add non-git context sparingly.**
   - Use Codex or other session history to name themes and include research,
     review, planning, or debugging work not captured by commits.
   - Use GitHub or `gh` only when PR, issue, review, or CI context matters.
   - Treat session text as context, not proof of a shipped change, unless it is
     confirmed by git, source files, PRs, issues, or another relevant system.

5. **Synthesize for a human reader.**
   - Group by project and theme, not by raw commit order.
   - Mention concrete artifacts: commits, files, specs, PRs, tests, generated
     docs, decks, or investigations.
   - Separate shipped code, docs/plans, reviews, and investigations when that
     distinction matters.
   - Keep tokens, secrets, raw auth data, and private local paths out of any
     shareable report unless the user explicitly asks for local detail.

## Output Shape

- Exact date range and scanned scope.
- Repo-level counts: repositories scanned, repositories with matches, and commit
  totals.
- Three to seven main themes with concrete examples.
- Notable tests, PRs, docs, generated artifacts, or deliverables.
- Caveats: inaccessible repos, uncommitted work excluded, identity assumptions,
  or non-git sources used.

Do not create a file unless the user asks to save the report.

## Common Pitfalls

- Do not leave relative dates ambiguous. Say the exact dates used.
- Do not use `git diff --stat` without a revision range for historical
  statistics.
- Do not claim a change shipped from session history alone.
- Do not bury important caveats. Put them near the top or bottom of the report.

## Example

User: "What did I do since last Friday?"

Actions:
1. Resolve "last Friday" to an exact date in the user's timezone.
2. Scan the requested scope, or the default documents root.
3. Collect commits by the user's git author and cluster them by project/theme.
4. Add session or PR context only if it explains work the commits do not.

Result: a scannable markdown activity report suitable for a weekly update,
standup, or manager brief.
