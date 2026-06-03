# Commit Message

Generates well-structured git commit messages following a consistent format with clear rationale and technical detail.

## Output Format

```
<one-line short summary>

[Why] <explanation of why the change was made. if the change is a bug fix, explain the bug and how the change fixes it. if the change is a new feature, explain the feature and why it was added. if the change is a refactor, explain what was refactored and why. preferably in bullet points.>
[How] <detailed description of how the change was made. include any relevant details about the implementation, such as algorithms used, data structures modified, or any other technical details that are important for understanding the change. preferably in bullet points.>
```

### Attribution

Add co-author to the commit message with your model name and email in the format `Co-Authored-By: <model name> <model email>`.

Examples:

- Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>
- Co-Authored-By: GPT 5.5 <codex@openai.com>
- Co-Authored-By: Gemini 3.5 Flash <noreply@antigravity.google>

## Workflow

When generating a commit message:

1. **Analyze input**: Read the diff, file list, or natural-language description.
2. **Classify**: Determine the primary type. If spanning multiple types, suggest splitting into separate commits or pick the dominant one.
3. **Identify scope**: Determine the most relevant scope from affected codebase area.
4. **Check for breaking changes**: Look for removed/renamed public APIs, changed defaults, dropped compatibility.
5. **Draft short description**: Concise imperative summary ≤72 chars.
6. **Add [Why] section**: Explain the motivation and context.
7. **Add [How] section**: Describe the implementation approach with technical detail.
8. **Add footers**: Co-authors as applicable.
