# DORÉ EXPLORATION — Research & Reuse Index

> Status: living cross-project discovery index · Established 2026-10-16.
> Authority: [WESTSIDE-WATCH-MASTER.md](./WESTSIDE-WATCH-MASTER.md). This is a **research index**, not another Design OS, CI system or independent Loop.

## Purpose / 使用原則

Every 「多雷探索」 should be findable by **technical category** and **owning engineering project**. The same technology may serve multiple projects: store the reusable technical finding **once**, then add multiple project references; do not create duplicate research documents for each page.

**Fixed selection keywords:** 免費、小巧、簡單、不耗能、安全、穩定、長久、好維護、現代、成熟、開源。

**Method:** 搜索 → 比較 → 驗證 → 吸收 → 能力化。Keep the original source URL, license, evidence, trade-offs, adoption status and actual tests. Never mark an untested idea as deployed or accepted.

### Index taxonomy

| Category ID | Technical category | Typical contents |
|---|---|---|
| SVG | SVG / vectors / path morphing / engraving / geometry | Path morph, clipping, masking, engraving animation, vector assets |
| MOTION | Motion / scroll / transitions | Scroll synchronization, animation clocks, reversible transitions |
| TYPE | Typography / editorial composition | Font selection, safe areas, type scale, image-text composition |
| IMAGE | Images / media assets | Subject detection, crop, backgrounds, image delivery |
| VIDEO | Video / streaming / offline | Playback, subtitles, manifests, download/mux workflows |
| UI | Interface / responsive / accessibility | Layout, scale, interaction, reduced-motion |
| DATA | Search / indexing / corpus | Search, classification, metadata, IIIF |
| AI | AI / agents / loops | Doré capabilities, orchestration, context and evaluation |
| INFRA | Engineering / CI / deployment | GitHub, Cloudflare previews, testing, performance, security |

**Project tags** use actual workstreams, e.g. `P2`, `HOMEPAGE`, `CHURCH`, `OLIVE`, `CINEMA`, `ONE`, `DORE-FOLIO`, `DESIGN-OS`, `CALLIGRAPHY`, `JERUSALEM`, `GLOBAL`. A finding may have multiple tags.

## Discovery directory / 探索總索引

| ID | Date | Category | Engineering project | Subject / result | Status | Evidence |
|---|---|---|---|---|---|---|
| SVG-001 | 2026-10-16 | SVG, MOTION | P2, CHURCH | Continuous engraved-ocean rise and Red Sea opening: retain Fixed Ocean 2.5 SVG; evaluate unified water-height field and shared clock, instead of moving a page/clip alone | Candidate; not implemented or browser-verified | [simplex-noise.js](https://github.com/jwagner/simplex-noise.js), [noisejs](https://github.com/josephg/noisejs), [polymorph](https://github.com/notoriousb1t/polymorph), [flubber](https://github.com/veltman/flubber) |
| MOTION-001 | 2026-10-16 | MOTION, SVG | P2, CHURCH | Separate time-driven flowing motion from scroll-driven water level / parting; calculate in one animation loop; ensure reversible scroll | Proposed architecture; no visual acceptance | [MDN requestAnimationFrame](https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame), [MDN clip-path](https://developer.mozilla.org/en-US/docs/Web/CSS/clip-path) |

## Category: SVG — vector research / 向量技術

### SVG-001 — Engraved ocean: continuous rise → parting

- **Project:** P2 identity-to-church transition; reusable for CHURCH and other engraved SVG motion.
- **Existing baseline:** `static/experiments/assets/living-water-contour-engraving-v10.svg` and `static/p2/living-water.html` (verify current branch and actual runtime before editing). Approved ocean preset recorded in master: propagation 1.5; gradient 2.0; amplitude 6px; density 2.5; 620 paths.
- **User-visible problem:** Moving the panel, clipping it, or replacing the moving engraving with a static blue fill does **not** count as water rising. An attempted replacement also caused the animation to disappear.
- **Reusable design hypothesis:** One continuous engraved-water renderer, shared time base, explicit water surface/height field, and continuous line replenishment while rising. The *same* field transitions into left/right parting; no independent ocean overlay that hides the original.
- **Source candidates:** [simplex-noise.js](https://github.com/jwagner/simplex-noise.js) (small noise generator); [noisejs](https://github.com/josephg/noisejs) (noise alternative); [polymorph](https://github.com/notoriousb1t/polymorph) and [flubber](https://github.com/veltman/flubber) (shape morphing; evaluate only for appropriate boundaries).
- **Rejected/low priority:** Heavy fluid particle engines for this SVG engraving task; `clip-path` alone as a physical rise model.
- **License and footprint:** Check exact versions and current licenses before importing; no package selected or installed yet.
- **Acceptance pending:** Water itself visibly rises; engraved lines continue flowing during the rise; no static frame or seam; full-screen ocean then parts; reverse scroll restores prior state; real Cloudflare preview tested on desktop/mobile, including reduced motion.
- **Status:** Explored / proposed, **not implemented**, **not validated**.

## Category: MOTION — animation architecture

### MOTION-001 — Unified clock and scroll-driven geometry

- **Project:** P2 / CHURCH.
- **Rule:** Animation time controls continuous flow, scroll controls water height and opening. One shared render/update path prevents competing layers and timing drift.
- **Browser behavior to test:** Background tabs and hidden iframes may pause `requestAnimationFrame`; restore without jumping or losing the wave field.
- **Status:** Design recommendation only, not verified as the root cause of the existing failure.

## Filing rules / 新增探索時必須遵守

1. Add one row to the **Discovery directory** with unique `CATEGORY-NNN` ID, date, technical category, project tags, subject, verification status and source URLs.
2. Add or update its details under the **technical category**, not a separate duplicate per project. For a multi-category finding, choose one primary section and cross-reference the same ID elsewhere.
3. Preserve source URL, project/branch/PR where relevant, license (verified or pending), criteria comparison, accepted/rejected candidates, integration cost, tests and outcome.
4. Mark status explicitly: `Research` → `Candidate` → `Prototype` → `Verified` → `Adopted` (or `Rejected` / `Superseded`). Never promote status on assertion alone.
5. When an actual implementation is verified, append its canonical code path, PR/commit, browser preview and regression evidence. If superseded, keep history and link the successor.
6. Update this index as part of the **existing project PR/engineering batch**. Do not spawn a new PR or separate research infrastructure for each exploration.
7. Keep the master engineering memory concise: link to this index and retain only durable cross-project decisions there.

