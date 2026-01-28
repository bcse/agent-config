---
name: write-pr
description: Write clear, well-structured pull request titles and descriptions. Use when creating a PR, drafting PR content, or when the user asks to write/improve a PR description.
---

# Writing Pull Requests

Guide for crafting effective PR titles and descriptions.

## PR Title

Use Conventional Commits format:

```
<type>(<scope>): <description>
```

### Types

| Type       | Use for                                    |
|------------|--------------------------------------------|
| `feat`     | New feature                                |
| `fix`      | Bug fix                                    |
| `docs`     | Documentation only                         |
| `refactor` | Code restructure (no behavior change)      |
| `perf`     | Performance improvement                    |
| `test`     | Adding or fixing tests                     |
| `chore`    | Maintenance, dependencies, configs         |
| `build`    | Build system changes                       |
| `ci`       | CI/CD configuration                        |

### Scope

Optional noun in parentheses describing the affected area: `fix(auth):`, `feat(api):`, `docs(readme):`

### Description Rules

- Use imperative mood: "Add" not "Added" or "Adds"
- Start with capital letter
- No period at end
- Keep under 50 characters when possible

### Examples

```
feat(auth): Add OAuth2 login support
fix(api): Handle null response in user endpoint
docs: Update installation instructions
refactor(db): Simplify query builder logic
feat!: Remove deprecated v1 API endpoints
```

Use `!` before `:` to indicate breaking changes.

## PR Body Template

```markdown
## Summary

<What this PR does and why. Link related issues.>

Fixes #123

## Changes

- <Specific change 1>
- <Specific change 2>

## Testing

<How to verify these changes work>

1. Step to test...
2. Another step...

## Checklist

- [ ] Tests added/updated
- [ ] Documentation updated (if needed)
- [ ] Breaking changes noted (if any)
```

## Writing Guidelines

### Summary Section

Start with what and why: "This PR adds X to solve Y" or "Fixes a bug where X happened when Y."

- Be specific—avoid vague phrases like "improve performance" or "enhance UX"
- Link related issues using keywords: `Fixes #123`, `Closes #456`, `Related to #789`
- Don't assume readers will read linked issues—include essential context

### Changes Section

List concrete changes, not implementation details:

**Good:**
- Add rate limiting to API endpoints
- Update error messages to include request ID

**Avoid:**
- Changed line 42 in auth.js
- Refactored some code

### Testing Section

Provide actionable steps reviewers can follow:

1. Checkout this branch
2. Run `npm test` or equivalent
3. Navigate to /feature and verify X works

Include edge cases or specific scenarios to test.

### Breaking Changes

If the PR introduces breaking changes, add a section:

```markdown
## Breaking Changes

- `oldMethod()` removed—use `newMethod()` instead
- Config option `foo` renamed to `bar`
```

## Checklist Usage

- Mark items with `[x]` only when actually completed
- Remove items that don't apply, or mark as N/A
- Common items: tests, docs, migrations, changelog

## Quick Reference

| Do | Don't |
|----|-------|
| Use imperative mood | Use past tense |
| Link issues explicitly | Assume context |
| List specific changes | Be vague |
| Provide test steps | Say "tested locally" |
| Note breaking changes | Hide API changes |
