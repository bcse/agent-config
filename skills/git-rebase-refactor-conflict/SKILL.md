---
name: git-rebase-refactor-conflict
description: |
  Handle merge conflicts during git rebase when code was refactored/moved in your branch
  but new features were added to the original location in master. Use when: (1) rebase
  conflict involves code that was moved or refactored in your branch, (2) after resolving
  conflict, you notice features from master are missing, (3) master added code to a
  location that your branch refactored into a different structure. Prevents accidental
  feature loss during rebase conflict resolution.
author: Claude Code
version: 1.0.0
date: 2026-01-22
---

# Git Rebase Refactor Conflict Resolution

## Problem

When rebasing a branch that refactored/moved code, and master added new features to the
original (pre-refactor) location, standard conflict resolution can accidentally drop the
new features from master because they appear in the "wrong" location.

## Context / Trigger Conditions

- You're rebasing a branch onto master
- Your branch refactored code by moving it to a new method/location
- Master added new features to the original location (before your refactor)
- After resolving the conflict by "keeping your version," features from master are missing
- The conflict markers show a large block from HEAD (master) that looks like old code

## Solution

1. **Before resolving**: Identify what master added by checking recent commits:
   ```bash
   git log --oneline origin/master --since="<branch-creation-date>" -- <conflicted-file>
   git show <commit-hash> -- <conflicted-file>
   ```

2. **During conflict resolution**: Don't just delete the HEAD block. Analyze what's new:
   - Your branch's version may have moved code to a new location
   - Master's version may have added NEW code to the old location
   - You need to identify the NEW code and add it to your NEW location

3. **Resolution pattern**:
   - Keep your refactored structure (the clean version)
   - Identify genuinely new features in the HEAD block
   - Add those new features to the appropriate location in your refactored code

4. **After resolving**: Verify nothing was lost:
   ```bash
   git diff origin/master -- <file> | grep -A5 -B5 "<feature-name>"
   ```

## Verification

After completing the rebase:
1. Check that the file compiles/passes syntax check
2. Search for the feature name that master added - it should exist in the new location
3. Run relevant tests if available

## Example

**Scenario**: Your branch refactored `setup_api_params()` by splitting it into:
- `_populate_params_for_api()` - pure param population
- `_validate_and_remove_invalid_apis()` - validation only

Master added "Feature X" handling to the original `setup_api_params()` location.

**Bad resolution** (loses feature):
```
<<<<<<< HEAD
    # 200 lines of param population including new Feature X handling
=======
>>>>>>> your-commit
    # Just validation code
```
Keeping empty (branch's version) loses Feature X.

**Good resolution**:
1. Note that Feature X handling is NEW in master
2. Keep your clean validation-only structure
3. Add Feature X handling to `_populate_params_for_api()` (the new location for param code)

## Notes

- This commonly happens with "extract method" or "split function" refactors
- The larger the refactored section, the more likely master added something to it
- Always check `git log` on conflicted files to see what master changed
- Consider doing a `git diff origin/master...HEAD -- <file>` before rebasing to understand changes

## References

- [Git Rebase Documentation](https://git-scm.com/docs/git-rebase)
- [Resolving Merge Conflicts](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging)
