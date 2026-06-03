#!/bin/sh
# Point this repo's git hooks at the version-controlled .githooks/ directory.
# Idempotent and safe: refuses to clobber a core.hooksPath set to something else.
set -eu

hook_dir=".githooks"

script_dir=$(CDPATH= cd "$(dirname "$0")" && pwd)
repo_root=$(CDPATH= cd "$script_dir/.." && pwd)

if ! git -C "$repo_root" rev-parse --git-dir >/dev/null 2>&1; then
    echo "Not inside a Git repository: $repo_root" >&2
    exit 1
fi

git_root=$(git -C "$repo_root" rev-parse --show-toplevel)
hook_file="$git_root/$hook_dir/pre-commit"

if [ ! -f "$hook_file" ]; then
    echo "Missing pre-commit hook: $hook_file" >&2
    exit 1
fi

current_hooks_path=$(git -C "$git_root" config --local --get core.hooksPath || true)

case "$current_hooks_path" in
    "$hook_dir"|"./$hook_dir"|"$git_root/$hook_dir")
        chmod +x "$hook_file"
        echo "Pre-commit hook already installed."
        exit 0
        ;;
    "")
        ;;
    *)
        echo "core.hooksPath is already set to '$current_hooks_path'; refusing to overwrite it." >&2
        exit 1
        ;;
esac

chmod +x "$hook_file"
git -C "$git_root" config --local core.hooksPath "$hook_dir"

echo "Installed pre-commit hook."
echo "Git will run $hook_dir/pre-commit before each commit."
echo "Set SKIP_PRE_COMMIT=1 to skip the hook for one command."
