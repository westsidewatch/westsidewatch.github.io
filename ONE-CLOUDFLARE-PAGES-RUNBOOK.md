# ONE Cloudflare Pages Runbook

## Purpose

Cloudflare Pages is an isolated preview and acceptance environment for Westside Watch. It must not replace or complicate the existing GitHub Pages production workflow unless a future migration is explicitly approved after testing.

## Current architecture

### Production

- Branch: `main`
- Host: GitHub Pages
- Existing ONE, Journal, Join, image publishing, and normal site workflows remain unchanged.

### Cloudflare preview

- Branch: `cloudflare-preview`
- Host: Cloudflare Pages
- Purpose: build and browser-test changes before they reach production.
- Do not use this branch as a reason to alter working production behavior.

## Verified Cloudflare Pages configuration

- Production branch: `cloudflare-preview`
- Framework preset: `Hugo`
- Hugo version: `0.164.0`
- Environment variable: `HUGO_VERSION=0.164.0`
- Build command: `hugo`
- Build output directory: `public`
- Root directory: repository root

The Hugo version is deliberately pinned to match the working GitHub Pages build. Do not casually upgrade it in Cloudflare independently of production.

## Phase 1 acceptance — 2026-08-21

The following path was tested successfully:

`GitHub cloudflare-preview -> Hugo 0.164.0 -> public -> Cloudflare Pages`

Browser acceptance passed for:

- Home page
- Journal
- ONE `/one/`
- ONE cover -> 66-book interface
- Join `/join/`
- Static images, CSS, typography, and core page routing observed during acceptance

The first Cloudflare build failed because Cloudflare's Hugo environment did not match production. The error included:

`can't evaluate field Locale in type *langs.Language`

The fix was to pin `HUGO_VERSION` to `0.164.0`, matching the existing successful GitHub Pages workflow. After that change, the Cloudflare Pages deployment succeeded.

## Working rule

Cloudflare must adapt to the existing working site. Do not modify a working production template merely to accommodate an unverified Cloudflare default.

If Cloudflare fails:

1. Stop at the failing stage.
2. Read the Cloudflare build log.
3. Compare the Cloudflare environment with the working GitHub Pages environment.
4. Fix the preview configuration first when possible.
5. Do not change `main` merely to make the preview build pass.

## Normal publishing workflow

Routine production publishing remains:

`main -> GitHub Pages`

Normal publishing does not require opening the Cloudflare dashboard.

## Large-change preview workflow

For substantial site changes:

1. Work on a dedicated change branch.
2. Complete and review the change.
3. Bring the intended preview state into `cloudflare-preview`.
4. Let Cloudflare Pages build automatically.
5. Perform browser acceptance on the Cloudflare preview.
6. Only after acceptance, merge the approved change to `main` for the normal GitHub Pages production deployment.

## Minimum acceptance checklist

Before treating a substantial preview as passed, verify:

- [ ] Cloudflare build succeeds.
- [ ] Home page loads with expected CSS, fonts, and static assets.
- [ ] Journal opens and its principal images/cards render.
- [ ] `/one/` opens.
- [ ] ONE cover interaction reaches the 66-book interface.
- [ ] `/join/` opens.
- [ ] Important images load without broken asset paths.
- [ ] Core JavaScript interactions used by the changed feature work.
- [ ] No production-only workflow has been replaced or disabled.

Add feature-specific checks when a change affects a particular page or interaction.

## Safety boundaries

Until explicitly approved after separate testing:

- Do not change the Cloudflare preview branch from `cloudflare-preview` to `main`.
- Do not attach the production custom domain to this preview project.
- Do not replace GitHub Pages production hosting.
- Do not introduce Cloudflare into the existing image publishing path merely because Cloudflare is available.
- Do not add Base64 conversion, WebP conversion, GitHub Actions, Workers, Wrangler, or other intermediary steps to an already working image workflow unless a specific requirement is established and separately validated.
- Do not delete or disable the existing working production workflow while experimenting with Cloudflare.

## Potential later phases

Cloudflare capabilities may be evaluated one at a time, behind this preview boundary, including:

- preview deployments and build diagnostics;
- caching and delivery performance;
- analytics;
- security / bot protection;
- image delivery optimization that does not alter canonical source assets.

Each capability must prove a concrete benefit without making the established publishing workflow less reliable.

## Key principle

**Existing successful publishing remains the source of truth. Cloudflare is an additional safety and delivery layer, not a prerequisite for ordinary publishing.**
