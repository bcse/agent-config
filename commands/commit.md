---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Create a git commit
---

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Your task

Based on the above changes, create a single git commit.

You have the capability to call multiple tools in a single response. Stage and create the commit using a single message. Do not use any other tools or do anything else. Do not send any other text or messages besides these tool calls.

If user have already staged some changes, do not stage any more changes, only commit the staged changes.

### Commit Message Format

```
<one-line short summary>

[Why] <explanation of why the change was made. if the change is a bug fix, explain the bug and how the change fixes it. if the change is a new feature, explain the feature and why it was added. if the change is a refactor, explain what was refactored and why. preferably in bullet points.>
[How] <detailed description of how the change was made. include any relevant details about the implementation, such as algorithms used, data structures modified, or any other technical details that are important for understanding the change. preferably in bullet points.>
```

### Attribution

Add co-author to the commit message with your model name and email in the format `Co-Authored-By: <model name> <model email>`.

Examples:

- Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
- Co-Authored-By: GPT 5.3 Codex <codex@openai.com>
- Co-Authored-By: Gemini 3.1 Pro <noreply@antigravity.google>

### Commit Command

```
git commit -m "$(cat <<'EOF'
<one-line short summary>

<multi-line full description>

Co-Authored-By: <model name> <model email>
EOF
)"
```
