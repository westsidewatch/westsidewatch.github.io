# Doré Training — Storybook 9 Package Model

Date: 2026-09-01
Trigger: real task failed at `npm install` with `ETARGET: No matching version found for @storybook/addon-essentials@^9.1.3`.

## Diagnosis

This is not a network retry problem and not a missing executable problem anymore. The dependency specification itself is stale/wrong for Storybook 9.

Storybook 9 consolidated/removed multiple packages. The official Storybook 9 migration guide explicitly states that **essential addons moved to core**. `@storybook/addon-essentials` should therefore not be required as a Storybook 9 dependency/config entry. Storybook's current Essentials documentation describes these capabilities as zero-config core features.

## What Doré should learn

1. Never infer package availability by copying an older Storybook package list into a newer major version.
2. Before installing a framework/tool major version, check that major version's official migration/package model.
3. `npm ETARGET / notarget` means the requested package/version cannot be resolved. First inspect the requested package/version and current official package model; do not blindly retry `npm install`.
4. Storybook 9 requires Node 20+ and npm 10+; current Mac evidence (Node 26.7.0, npm 11.19.0) satisfies those minimums, so this failure is not primarily an engine-age problem.
5. For this React/Vite lab, keep the minimum package set needed for the framework and Storybook itself. Do not add legacy Essentials just because Storybook 8 tutorials used it.
6. After correcting dependencies/config, run `npm install`, verify the local Storybook executable, then `npm run build-storybook`, then verify `storybook-static/index.html`.

## Self-learning heuristic

When an install returns `ETARGET`, Doré should automatically enter a dependency-research state:

`ETARGET → identify exact package/version → check official docs for current major → check migration notes → correct package model → controlled install → build acceptance → record lesson → return to parent goal`

This is a reusable rule for npm ecosystems, not only Storybook.

## Authoritative sources

- Storybook 9 migration guide: https://storybook.js.org/docs/9/releases/migration-guide
- Storybook 9 addon migration guide: https://storybook.js.org/docs/9/addons/addon-migration-guide
- Storybook Essentials: https://storybook.js.org/docs/essentials/index
- Storybook install: https://storybook.js.org/docs/get-started/install
- npm run: https://docs.npmjs.com/cli/v11/commands/npm-run/

## Exam

A PASS requires Doré to demonstrate through the real task that it can:
- stop retrying the invalid dependency;
- remove the obsolete Storybook 9 Essentials dependency/config entry;
- install a valid Storybook 9 React/Vite dependency set;
- produce a local Storybook executable;
- build the static Storybook successfully;
- preserve the original parent goal: an executable Westside Design Knowledge Lab.
