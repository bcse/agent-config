---
name: conventional-commits
description: >
  Generate commit messages following the Conventional Commits 1.0.0 specification.
  Use when the user asks to write a commit message, generate a commit, describe changes
  for a commit, or review/fix an existing commit message. Triggers include: "write a
  commit message", "commit message for", "generate commit", "what should I commit this as",
  "conventional commit", or any request involving git commit message authoring. Also use
  when the user provides a diff, changeset, or description of code changes and wants a
  properly formatted commit message.
---

# Conventional Commits Message Generator

Generate commit messages conforming to the [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) specification.

## Commit Message Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## Types

Select the type that best matches the change:

| Type       | When to use                                        | SemVer impact |
|------------|----------------------------------------------------|---------------|
| `feat`     | New feature or capability                          | MINOR         |
| `fix`      | Bug fix                                            | PATCH         |
| `docs`     | Documentation only                                 | none          |
| `style`    | Formatting, whitespace, semicolons (no logic)      | none          |
| `refactor` | Code restructure without fixing bugs or adding features | none    |
| `perf`     | Performance improvement                            | none          |
| `test`     | Adding or correcting tests                         | none          |
| `build`    | Build system or external dependencies              | none          |
| `ci`       | CI configuration and scripts                       | none          |
| `chore`    | Maintenance tasks, tooling, configs                | none          |
| `revert`   | Reverts a previous commit                          | varies        |

## Rules

1. **Description line**: Imperative mood, lowercase first letter, no period, max ~72 chars.
   - Good: `feat(auth): add OAuth2 login flow`
   - Bad: `feat(auth): Added OAuth2 login flow.`

2. **Scope**: Optional noun in parentheses identifying the codebase section.
   - Derive from: module name, component, layer (e.g., `api`, `parser`, `ui`, `db`, `auth`).
   - Omit when the change is broad or scope is obvious.

3. **Body**: One blank line after description. Explain *what* and *why*, not *how*. Wrap at ~72 chars.

4. **Footer(s)**: One blank line after body. Format: `token: value` or `token #value`.
   - `BREAKING CHANGE: <description>` — required for breaking changes (MAJOR bump).
   - `Refs: #<issue>` — link related issues.
   - `Reviewed-by:`, `Co-authored-by:` — attribution.

5. **Breaking changes**: Indicate with `!` after type/scope (`feat(api)!: ...`) and/or a `BREAKING CHANGE:` footer.

## Workflow

When generating a commit message:

1. **Analyze input**: Read the diff, file list, or natural-language description.
2. **Classify**: Determine the primary type. If spanning multiple types, suggest splitting into separate commits or pick the dominant one.
3. **Identify scope**: Determine the most relevant scope from affected codebase area.
4. **Check for breaking changes**: Look for removed/renamed public APIs, changed defaults, dropped compatibility.
5. **Draft description**: Concise imperative summary ≤72 chars.
6. **Add body if needed**: For non-trivial changes, explain motivation and contrast with previous behavior.
7. **Add footers**: Issue refs, breaking change details, co-authors as applicable.
8. **Output** the message in a fenced code block for easy copying.

When multiple commits are appropriate, present each in its own code block with a brief explanation of why splitting is recommended.

## Examples

Single-line:
```
docs: correct typos in README contributing section
```

Feature with scope:
```
feat(lang): add Japanese language support
```

Bug fix with body and issue ref:
```
fix(api): prevent race condition in concurrent requests

Introduce a request ID and track the latest request reference.
Dismiss responses from outdated requests to avoid stale data.

Refs: #423
```

Breaking change:
```
feat(config)!: use YAML for configuration instead of JSON

Migrate all configuration files from JSON to YAML format for
improved readability and comment support.

BREAKING CHANGE: configuration files must be converted from
.json to .yaml format. Run `migrate-config` to auto-convert.

Refs: #891
```

Revert:
```
revert: remove flaky timeout workaround

Reverts the timeout workaround from a1b3c4d, no longer needed
after the race condition fix in e5f6g7h.

Refs: a1b3c4d, e5f6g7h
```
