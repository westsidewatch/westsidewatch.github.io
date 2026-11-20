# Westside Watch · W Icon release authority

Status: **R1 approved for use, not final artwork**. Owner approval: 2026-11-20.

## Single source of truth

`static/favicon.svg` is the one production W icon asset served to all Hugo pages by `layouts/_default/baseof.html` (`/favicon.svg`). Do not paste an old inline favicon or a competing data URI into P2, Olive, ONE, Cinema or later page templates. Those pages inherit the single root icon unless they have an explicitly authorised scoped asset.

R1 artwork comes from the owner-selected Westside Type Foundry master: Bodoni Moda SC / SIL OFL 1.1, weight 400, optical 72, scale 112%, horizontal +1, vertical 0, 12.5px square corner. The independently approved **R1 display export** keeps the source contours while applying optical placement: weight 400, optical 72, scale 114%, horizontal +0.6, vertical +0.4, radius 12.5. Colours: gold `#A2872A`, paper `#FAF9F5` only. R1 micro-variants are still available from the private Type Foundry; do not silently replace the production master with those variants.

## Why previous versions came back

The private icon design iterations and R1 Type Foundry were never wired to the main repository's existing `static/favicon.svg`. Main's old navy/gold skyline asset remained the actual Hugo source; the common base template continued to reference it. Later site deployments faithfully rebuilt that old asset. This is a **source-of-truth/integration gap**, not a browser rendering quirk. The exact individual merge that reintroduced the old version has not been established.

## Anti-regression contract

- Keep `static/favicon.svg` as the published, single canonical icon. Preserve root template link to it.
- Run `python3 scripts/check_w_icon_authority.py` on PRs and in Pages deployment before Hugo build.
- The lock rejects a change of approved R1 SVG bytes, missing brand markers, retired navy skyline colours, or a broken canonical `<link rel="icon">`. Changing the art intentionally requires a new release ID, updated explicit lock and visual approval.
- Never replace this asset as a side effect of unrelated P2, Olive or new-page merges. If a merge proposes a conflicting favicon, keep the approved current main version and resolve the conflict before deploying.

## Open refinement items

R1 is usable but not the final proprietary church typeface. Planned R2 work: edit the true glyph outline at Bézier/anchor level, calibrate top terminals and diagonal stroke joins, test antialiasing at 16/32/64 px, export dedicated raster icons, and revisit accessibility at low-density displays. Preserve R1 as a historical release.
