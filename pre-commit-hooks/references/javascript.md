# JavaScript And TypeScript Pre-Commit Checks

Use this reference when a repo has `package.json`, `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `bun.lock`, Vite, Vitest, Jest, ESLint, Prettier, TypeScript, or frontend build scripts.

## Package Manager

| Lockfile | Commands |
|----------|----------|
| `package-lock.json` | `npm run <script>` |
| `pnpm-lock.yaml` | `pnpm <script>` or `pnpm run <script>` |
| `yarn.lock` | `yarn <script>` |
| `bun.lock` / `bun.lockb` | `bun run <script>` |

Use the package manager already established by the lockfile. Do not mix package managers in the hook.

## Command Selection

Prefer existing `package.json` scripts:

| Need | Common scripts |
|------|----------------|
| Format | `npm run format`, `npm run format:check` |
| Lint | `npm run lint` |
| Type check | `npm run typecheck`, `npm run build` if it runs `tsc` |
| Tests | `npm run test`, `npm test`, `npm run test:coverage` |
| Build | `npm run build` |

If `format` or `lint` auto-fixes, keep the hook's before/after diff guard so commits stop when files were rewritten.

Before using `npm test`, inspect the script. Some projects start watch mode by default; prefer non-watch scripts such as `test:run`, `test:ci`, `vitest --run`, or `jest --runInBand` when available.

## Audit And Dependencies

`npm audit` is a policy choice, not a default pre-commit gate. It can block unrelated commits because of newly published advisories. Prefer CI, scheduled dependency checks, or `npm audit --audit-level=high` if the team explicitly wants a local gate.

Never run `npm audit fix`, `npm update`, `pnpm update`, `yarn upgrade`, or `bun update` in pre-commit. Dependency changes should be explicit commits.

## Common Mistakes

- Calling `npx prettier --write .` when the repo already has scripts.
- Running `npm install` or `npm ci` on every commit.
- Committing generated `dist/` changes unintentionally after `npm run build`.
- Adding build to pre-commit when it is too slow for normal commits; move it to CI or pre-push instead.
