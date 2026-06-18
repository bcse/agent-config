# Rust Pre-Commit Checks

Use this reference when a repo has `Cargo.toml`, `Cargo.lock`, Cargo workspaces, Clippy, rustfmt, or Rust tests.

## Command Selection

| Need | Common command |
|------|----------------|
| Format | `cargo fmt` or `cargo fmt --check` |
| Lint | `cargo clippy --all-targets --all-features -- -D warnings` |
| Tests | `cargo test` |
| Workspace tests | `cargo test --workspace --all-features` |
| Workspace lint | `cargo clippy --workspace --all-targets --all-features -- -D warnings` |

Use `cargo fmt --check` for non-mutating hooks. Use `cargo fmt` only when the hook includes a diff guard and the team wants auto-formatting before commit.

## Adding Clippy

Before adding `-D warnings`, run the exact command. If the repo has existing warnings, fix them in a separate commit first or use a weaker gate temporarily. Do not make every commit fail on known debt.

## Common Mistakes

- Adding `--all-features` when feature combinations are not expected to compile.
- Running `cargo update` in pre-commit.
- Assuming a workspace root when the Rust crate lives in a subdirectory.
- Adding Clippy as a strict gate without first cleaning existing findings.
