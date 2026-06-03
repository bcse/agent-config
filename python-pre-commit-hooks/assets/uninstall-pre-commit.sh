#!/bin/sh
# Stop running the version-controlled hooks. Only unsets core.hooksPath when it
# points at this repo's .githooks/ — never touches an unrelated value.
set -eu

hook_dir=".githooks"

script_dir=$(CDPATH= cd "$(dirname "$0")" && pwd)
repo_root=$(CDPATH= cd "$script_dir/.." && pwd)

if ! git -C "$repo_root" rev-parse --git-dir >/dev/null 2>&1; then
    echo "Not inside a Git repository: $repo_root" >&2
    exit 1
fi

git_root=$(git -C "$repo_root" rev-parse --show-toplevel)
current_hooks_path=$(git -C "$git_root" config --local --get core.hooksPath || true)

case "$current_hooks_path" in
    "$hook_dir"|"./$hook_dir"|"$git_root/$hook_dir")
        git -C "$git_root" config --local --unset-all core.hooksPath
        echo "Uninstalled pre-commit hook."
        ;;
    "")
        echo "No local pre-commit hook is installed."
        ;;
    *)
        echo "core.hooksPath is '$current_hooks_path', not managed by this repo; refusing to unset it." >&2
        exit 1
        ;;
esac
