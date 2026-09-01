# Doré Training — Storybook Runtime Basics

Date: 2026-09-01
Purpose: train Doré to distinguish configuration presence from executable readiness before building Storybook.

## Core facts to learn

1. A valid `package.json` does **not** prove that its dependencies are installed.
2. In npm local mode, packages are installed into the project `node_modules/` directory, and package executables are linked into `node_modules/.bin/`.
3. `npm run <script>` automatically adds `node_modules/.bin` to PATH. Therefore a script such as `"build-storybook": "storybook build"` only works after the Storybook package has been installed locally and its executable exists.
4. `sh: storybook: command not found` with npm script exit code 127 is strong evidence that the Storybook executable is unavailable to the script, usually because dependencies were not installed successfully or the local install is incomplete.
5. Storybook 9 requires a modern Node/npm environment. Current local evidence already shows Node v26.7.0 and npm 11.19.0, so version age is not the first hypothesis for this failure.
6. The normal Storybook static-build acceptance is `npm run build-storybook`; success should produce a static Storybook application.

## Execution discipline

Before running a Storybook build, Doré should check in this order:

- project directory exists
- `package.json` exists and declares Storybook
- `node_modules/.bin/storybook` exists (or another package-manager-equivalent executable is resolvable)
- if executable is missing, run dependency installation rather than attempting the build repeatedly
- if install fails, preserve install command, return code, stdout and stderr and classify the actual failure (network/registry, dependency resolution, engine compatibility, permissions, lockfile, disk, etc.)
- only after installation succeeds, run `npm run build-storybook`
- verify generated `storybook-static/index.html`

## Failure-learning rule

Do not repeat `npm run build-storybook` when the executable is known to be missing. Change the hypothesis to dependency installation/readiness. A repeated failure without new evidence is not progress.

## Sources

- Storybook official installation documentation: https://storybook.js.org/docs/get-started/install
- Storybook 9 documentation: https://storybook.js.org/docs/9
- Storybook publishing/static-build documentation: https://storybook.js.org/docs/9/sharing/publish-storybook
- npm `npm run` documentation: https://docs.npmjs.com/cli/v11/commands/npm-run/
- npm folder/executable documentation: https://docs.npmjs.com/files/folders.html/

## Current real-work lesson

Observed failure: `npm run build-storybook` -> return code 127 -> `sh: storybook: command not found`.

Interpretation: configuration exists, but runtime dependency readiness is incomplete. The next action is installation/readiness verification, not another blind build retry.
