# Westside agent entrypoint (routing only)

This file is **not a second design system**, and it authorizes **no** automatic deployment, broad refactor or modification to protected P2 screens. The single authority remains [Westside Design OS Editorial Manual](docs/design/WESTSIDE-EDITORIAL-MANUAL.md) and its linked OS tokens/owning components.

## When the task is a Xi Wang / 西望 poster (Chapter 02, A or B)

**Before any generation, rendering or code changes:**
1. Read [the OS Editorial Manual](docs/design/WESTSIDE-EDITORIAL-MANUAL.md) and [Xi Wang Poster Toolchain — Execution](docs/design/XIWANG-POSTER-TOOLCHAIN-EXECUTION.md), plus the current art-direction decisions in [Poster Generation Resource Atlas](docs/design/P2-XIWANG-POSTER-GENERATION-RESOURCE-ATLAS-20261103.md).
2. Run `node scripts/xiwang/poster-toolchain.mjs plan a` or `plan b` in an actual local checkout. Record **which tools are available**, not only which ones were researched. A link to GitHub, a README summary or invented command output does **not** constitute tool execution.
3. For art direction, explicitly read [mono-color-skill/SKILL.md](https://github.com/yanliudesign/mono-color-skill/blob/main/SKILL.md) and apply **one focal event, intentional paper/ink hierarchy and negative space**; the skill is not automatically installed by its inclusion here. For A, construct new glyph geometry with an actual vector/CJK tool. For B, actually construct 7 different upright glyph/line systems with a vector/line engine. Do not simply call an image generator and relabel the raster output SVG.
4. Create a fresh `init` receipt; log each **actual** editor/program operation and output file, even when using a valid substitute because a preferred library is unavailable. Run `verify` and report blocked stages truthfully; visual/art acceptance still requires actual browser evidence and a human design review.
5. Keep Church, Emmaus, homepage sevenfold, right 5:8 official cover and existing scroll runtime unchanged unless the user specifically requests a separate scoped alteration. Never merge the Draft PR automatically.

**Authoritative visual distinction:** A = one large original upright 西 above 望. B = seven **upright, overlapping** groups of 西望 with different internal engraving systems in **one cohesive poster**, OS colors controlled by the user's decisions, no background engraving or extra pictograms. No tilted text, no seven horizontal color ribbons, no recycling rejected A2/B2 outlines.

For tasks outside the Xi Wang poster scope, this additional routing is inactive; follow existing repository and user instructions.
