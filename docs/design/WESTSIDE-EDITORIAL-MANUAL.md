# Westside Design OS — Editorial Manual

Status: **operational chapter of the single Westside Design OS**, not a parallel visual authority.  
Audience: Church, First Look, Journal, Olive Mountain, ONE, Dawn Library, Cinema, Search, tools, and Doré Design agents.  
Source of truth: [WESTSIDE-DESIGN-OS.md](WESTSIDE-DESIGN-OS.md) → `design-system/tokens/westside.tokens.json` → `static/css/westside-design-os.css` → approved `data-ws-scope` overrides.

## 1. Authority, layers and safe integration

This manual merges design **judgment, editing and verification** into the existing OS. It is a Markdown reference, **not loaded by public pages**. Nothing in it authorizes an extra CSS entry point, a new global palette, a competing type scale, a second CI pipeline or a site-wide geometry patch.

| Layer | Existing authority | Editorial manual action |
|---|---|---|
| Normative tokens: font, color, weight, spacing, motion | `design-system/tokens/westside.tokens.json`; `design-system/scopes.json` | **Refer to**, never redefine |
| Loaded runtime | `static/css/westside-design-os.css` | Preserve existing stylesheet links/import order |
| Surface geometry and transitions | Existing owning CSS/JS files; `data-ws-scope` | Review locally; no universal overrides |
| Editorial font detail | `docs/design/WESTSIDE-EDITORIAL-TYPOGRAPHY.md` | Keep as detailed reference; defer to OS on conflict |
| Award precedents and UI Skills | Research documents in `dore-design/` | Interpret into review criteria and exercises |
| Acceptance | Existing OS, first-look, build and deployment checks + actual browser visual inspection | Do not replace visual QA with CI status |

**Integration verified 2026-10-17:** The OS runtime already defines Bodoni Moda, genuine Bodoni Moda SC, Chiron Hei HK WS, Chiron Hei HK WS, Chinese 200/400/600 weights and responsive `--ws-type-scale-*` semantics. Hence the old typography document's `typography-sitewide.css` authority statement is **superseded** by the OS umbrella and compatibility-runtime contract. It is not grounds to migrate or change working entry points.

**Entrypoint rules.** Hugo templates load OS through `layouts/_default/baseof.html`; standalone P2 loads `/css/westside-design-os.css` followed by its own `/css/p2-living-water.css`. Other standalone HTML is guarded by `scripts/check_design_os_entrypoints.py`: the OS stylesheet and `body[data-ws-scope]` must both exist. A manual consolidation **must not touch those references, their sequence, or any HTML/CSS/JS**.

## 2. Editorial hierarchy and real reading

Typography is architecture for reading, not decorative text. Decide the reader's sequence before choosing font sizes.

1. **Identity:** ecclesial/realm name, issue or section identity; usually one visual anchor.
2. **Primary heading:** one clear top-level editorial proposition.
3. **Section headings:** lower scale/weight than the primary title unless an explicit art-directed composition justifies parity.
4. **Body/metadata:** sufficiently legible at the actual viewport; time, author, source and captions must remain discoverable.
5. **Citation/folio:** distinct semantic typography and stable positioning; never compete with the content.

Select from the OS semantic scale; surface owners may bind scope-specific roles. Do not make a new `--root` type system and do not stretch fonts. For P2 Emmaus editorial non-body Chinese use airy Chiron 200; body prose uses Chiron 400. Maintain text contrast and legibility for small controls. Chinese anchor 600 is for short structural titles, not whole paragraphs. English Roman/Italic Bodoni and real Small Caps retain distinct semantic roles.

Composition is measured by *text length, optical alignment, baseline, measure, contrast and breathing room*. A technically right-aligned row may still have a broken time-to-event association when the two columns are visually detached. Negative space needs a function, not merely width.

## 3. Award-calibre precedent method

The award corpus is a **research evidence bank**, not a list of winners to imitate or a claim of affiliation with Awwwards, Webby, FWA, Red Dot or D&AD. The internal phrase “Red Dot-level or reject” describes a design ambition, not an official certification.

For every candidate, document:

`reference → concept → spatial/narrative mechanism → typography/hierarchy → IA/reading path → transferable primitive → constraint → failure mode → OS-scope application → experiment`.

Transfer useful mechanisms, not surface styling:

| Precedent from award corpus | Transferable editorial insight | Guardrail |
|---|---|---|
| **The Boat** | Scroll, illustration and prose can form a single authored reading sequence | Motion must follow reading, not obscure it |
| **We Choose the Moon** | Canonical chronology can itself become information architecture | Provide clear wayfinding and overview |
| **Museum of the World** | Time and semantic relationships can spatialise a large collection | Maintain legibility and access to details |
| **Bear 71** | A linear story and an explorable information system can coexist | Avoid burying core actions behind immersion |
| **Species in Pieces** | Signature interaction comes from subject-specific metaphor | Reject ornamental effect without meaning |
| **Bascule / Microdot** | Scroll or timeline can become expressive navigation | Novelty does not excuse scroll lock or exclusion |
| **KUUM / Communication through the Ages** | Subject geometry and visual invariants can drive transitions | Preserve spatial continuity and orientation |

For Westside, engraving line, paper, dawn, water and scripture chronology may define transitions. They must **not** be used to justify content invisibility, long empty scroll bands or read-blocking animation.

## 4. UI Skills routing and acceptance

Load only the skills needed for the present defect. Imported Skills are **inspiration and decision aids**, not an installed guarantee or a replacement for Westside's OS.

| Task | Capability bundle derived from Doré research | Expected artifact |
|---|---|---|
| Layout and typography | `ui.visual-hierarchy`, `ui.design-system`, `ui.taste-anti-slop` | Type-role map, grid and optical alignment measurements |
| Motion and transitions | `ui.motion-system`, `ui.motion-forensics`, `ui.performance` | Purpose/timeline/interruption/return/reduced-motion review |
| Usability and accessibility | `ui.interaction-quality`, `ui.accessibility` | Reading order, focus/keyboard, contrast and small-screen test |
| Final polish and release | `ui.critique`, `ui.visual-verification` | Severity-tagged review and before/after screenshots |
| Variant exploration | `variant` / `prototype` / pairwise Taste Memory | A/B comparison on **one meaningful axis**, including rejection reason |
| **Poster production (A/B)** | **[《西望》Poster Toolchain](XIWANG-POSTER-TOOLCHAIN-EXECUTION.md)**: mono-color art direction → original glyph tools → path/engraving tools → native SVG → real browser QA | **Tool execution receipt** with actual input/output, tool availability, vector source, screenshots and acceptance; research alone is not execution |

This incorporates UI Skills explorations R1–R4: route the minimum capability, test motion separately from motion authoring, deliberately break at edge states, compare against the current version, and record contextual outcomes and uncertainty. Do not generate cosmetic alternatives solely to accumulate screenshots; do not compress all user tastes into one global score.

For code and motion, make the change-level critique concrete: **block / important / polish / approve**, with a reproducible defect, owning file, anticipated visual delta and evidence.

## 5. Editorial composition and motion grammar

Follow the experimental Italian editorial grammar as a **method**, not a second visual system:

- Begin with a one-sentence visual proposition and dominant reader task.
- Map composition grid, content priority, focal point, text-safe zone, cropping, paper/ink roles and deliberate blank regions.
- Keep live text in semantic HTML/CSS; image-generation prompts describe text-free artwork.
- Compare supported composition families (quiet field, overscale tension, two-scale encounter) within the same approved OS palette and fonts.
- Motion must explain state, route, hierarchy or narrative passage; prefer existing OS motion primitives and surface-owned implementation.
- Static composition must read correctly **before** motion begins and after it settles.
- Never add a new global cascade override to patch a single screen; use the owning `data-ws-scope` and stylesheet.

Review at desktop, tablet and phone widths; normal and reduced motion; initial, mid-scroll, end, interruption and return. Browser measurements and screenshots are distinct from build-status success.

## 6. Unified editorial review / promotion gate

Record one **evidence-led** review per change, using the project skill's existing directional rubric (0–2 each across **meaning, subject, composition distinction, typography, two-ink discipline, hierarchy, interaction meaning, mobile, accessibility, editability**; 20 possible). Its original exploratory threshold is **15/20** with no zero for meaning, distinction, accessibility or editability. This is a **local creative-review screen, not an official award score or a substitute for acceptance tests**. Surface-specific feasibility, reading and performance are independent release gates.

1. **Brief:** reader goal, real copy, current viewports, locked assets and immutable sections.
2. **Before:** fetch the actual current file and prior approved screenshot; record measured DOM and type metrics.
3. **Candidate:** smallest coherent scoped change, with OS-approved tokens; preserve all source content.
4. **Evidence:** before/after and desktop/mobile screenshots; accessibility, keyboard, zoom, scroll and reduced-motion behavior.
5. **Judgment:** rubric + blocking issues + any A/B winner/loser reasoning in context.
6. **Promotion:** existing OS contract and build/CI, Cloudflare preview and **actual browser visual check**. Green CI cannot override a known visual defect.
7. **Learning:** record what worked, what failed and where; keep source research linked rather than creating a second authority.

## 7. P2 Church / Sunday schedule — Italian editorial folio

The P2 split composition preserves its water engraving, rise and opening doors on the left and the warm-paper schedule on the right. **The previous requirement to keep seven gold right-aligned headings is withdrawn** by the 2026-10-17 editorial review; it must not be treated as a locked visual asset.

- **Separate, untouched church identity:** church logo, English church name and street address are outside the Sunday programme's editorial scope. Preserve their current sizes, typography, spacing, alignment and markup; do not treat them as a schedule header.\n- **Protected:** original service times, seven worship texts and their order, ministry copy, scripture, church-name artwork, left water and door mechanics, existing OS tokens and palette.
- **Reading hierarchy:** issue/date folio → one Chinese main title → ministry context → seven numbered programme rows → next-service details → scripture.
- **Italian editorial grammar:** use a three-column folio (01–07 / tabular time / left-aligned programme), restrained hairlines, editorial whitespace and optical left alignment. English Bodoni for metadata and times; Chiron Hei HK WS for Chinese heading and reading; avoid artificially stretched type.
- **Color:** ink is the programme text; the approved palette remains available for subtle accents. The old repeated gold right-aligned headline treatment is not mandatory.
- **Implementation:** owning `static/css/p2-living-water.css` only; do not create another runtime, modify OS globals, replace engraving artwork or interfere with scroll/door choreography. CSS counters supply numbers without altering source copy.
- **Proportional folio (2026-10-17):** make the schedule-owning right pane an inline-size container; use percentage-based inner gutters, container-relative column proportions and `cqi` fluid type with readable clamp bounds. Do not use CSS `transform:scale` on typography or the entire schedule. Preserve whitespace on both sides at any zoom and stack columns below the narrow-container threshold.\n- **Scripture:** the theme scripture remains left-aligned editorial reading; the independent Acts 4:12 closing citation is centered, including its reference.\n- **Acceptance:** actual 1648×928, 768px and 390px previews, 200% zoom, longest-row wrapping, keyboard and reduced-motion review, plus existing CI. A green CI alone does not certify editorial quality.

## 8. Seven-surface P2 — Magazine-anchored fixed field and native engravings (2026-10-30)

**Composition decision.** Chapter 01 LivingWaterWest is deliberately exceptional:
its living-water / Red Sea split, door and Christian-institutional reading
structure have their own accepted proportions. Beginning with Chapter 02
Magazine, the remaining six realms reuse the **exact 5:8 cover + square
Contents + original seven-color spine outer spread bounds**, measured from
the existing Magazine folio rather than recreated by another CSS percentage
or a new full-screen return animation. On mobile, the Magazine's approved
stacked geometry determines the outer proportions; a new fixed crop must
not override it. The surrounding background field is spatially continuous;
its contents, not its size, change across realms.

**The background belongs to each realm, not to a universal film loop.** The
Magazine retains its original homepage six-clip video in the already accepted
proportion. Bible, Sermon, Book, Cinema and Life may replace THAT SAME
background region with their subject-specific engraving, paper tone and ink,
using the one existing visual authority
`static/css/westside-engraving-authority.css`. Do not replay the Magazine
video in every chapter, create duplicate media players or make a full-screen
film-to-engraving transformation. The per-chapter motif must be readable
in the exposed non-content field while the actual chapter's paper/imagery
stays opaque above it.

| P2 chapter | Existing engraving owner / subject | Editorial character |
|---|---|---|
| 01 Church | `sites-section-church`: living currents / baptismal flow | **Distinct composition**; no compulsory Magazine geometry |
| 02 Magazine | `sites-section-journal` / `sites-section-vol-00`: editorial folds and page diagonals | Original video outside cover, Contents and original spine |
| 03 Bible / Emmaus | `sites-home-realm[data-realm=bible]`: canonical page/folio contours; existing manuscript scroll-edge SVG | ONE golden paper and real 241-image Doré gallery inside spread |
| 04 Sermon / Olive | `sites-section-olive`: olive terraces / hillside contours | Speaker portraits and words on opaque paper |
| 05 Book / Dawn Bookshop | `sites-section-dawn-library`: layered leaves, folios | Book material / fine plate-edge hatches |
| 06 Cinema / Paradise | `sites-section-cinema`: **tabernacle veil** / curtain of the Most Holy Place (Ex 26:31–33; Heb 10:19–20) | Christ opens the new and living way; a theatrical curtain is only the spatial metaphor, never the theological source |
| 07 Life / Daylight Café | `sites-section-daylight-cafe`: **五穀與新酒** (Deut 11:14; 8:8) | Crop/fruit intaglio: the promised land’s seven products, harvest, gratitude; tableware is supporting material only |

**Art-direction requirement.** These CSS motifs are an existing *semantic
engraving grammar*, **not accepted award-grade artwork**. Each chapter's
authentic subject, original engraved source or approved authored SVG,
cross-hatching density, line direction, texture scale, dark/light falloff,
text-safe zone and material color must still be developed and visually
reviewed. Do not mark generic repeating CSS patterns as complete engraving
art. Chapter 03/04 are the only implemented follow-up candidates today;
05–07 are design rules rather than invented completed screens.

### P2 各版塊主題經文與刻線來源 / Scripture-to-engraving contract (2026-10-30)

**本輪決定：每一個版塊必須有自己的一組「主題經文 → 具體形體 → 隨形刻線 → 動態語義」。**
Primary Scripture is one real passage per chapter, with distinct supporting
passages for object provenance and narrative action. The thematic object must
come *from* the biblical text; a generic visual trope is not evidence.
Church (01) and Magazine (02) are protected reference works, **not included
in the new five-surface production batch**. Verses for 03–05 below are
proposed art-direction assignments pending theological/editorial acceptance;
06’s curtain and 07’s 五穀與新酒 are explicit user decisions. Scripture
references do **not** mean all quoted passages must be printed on screen;
the final bilingual wording and placement must be approved separately.

| P2 | 主題經文 / Primary verse | Supporting Scripture | Biblically sourced engraved subject | Scripture-to-art rule |
|---|---|---|---|---|
| 01 Church / 活水 | **約 7:38 / John 7:38** (already shown in approved P2) | 約 7:37–39 | Living water currents | **Protected V75**; no repaint, reanimation or ratio changes |
| 02 Magazine / 西望 | **羅 13:12 / Rom 13:12** (existing Watch for the Dawn identity) | 彼後 1:19, star/light association for study only | Dawn / the already frozen Morning Star–derived engraving | **Protected cover, Contents and spine**; no new Mother artwork this batch |
| 03 Bible / Emmaus | **路 24:27 / Luke 24:27** *(proposed)* | 路 24:32 | The Scriptures opened and explained concerning Christ: manuscript scroll curvature and incised folio edges | Must communicate Christ opening the Scriptures; avoid generic letter or paper wallpaper |
| 04 Sermon / Olive Mountain | **太 24:3 / Matt 24:3** *(proposed)* | 亞 14:4; 徒 1:12; 王上 6:31–33 for olive-wood ornament as a distinct source | Olive Mount as the teaching location; olive leaves, branch structure, oil-wood carved detail | Do not substitute topographic map stripes or falsely attribute Sermon on the Mount (Matt 5) to Olive Mountain |
| 05 Book / Dawn Library | **耶 30:2 / Jer 30:2** *(proposed)* | 提後 4:13; 哈 2:2 | Written and preserved words: book, parchment, tablets, folio cut-edge and binding | Focus on faithful recording/transmission, not generic bookshop furniture |
| 06 Cinema / 天堂電影院 | **來 10:19–20 / Heb 10:19–20** *(thematic direction confirmed)* | **出 26:31–33** (veil material & cherubim), **太 27:51** (veil torn top to bottom), **約 1:14** (Word dwells/tabernacles with us), **林後 5:18–19** (reconciliation) | **會幕／至聖所幔子**: woven blue/purple/scarlet linen, living fabric curvature, cherubim relief and opening passage | **大幕揭開 = 因基督的身體、寶血，隔絕被除去，人得以親近神。** Stage curtain is the editorial metaphor, not the model. Christ fulfills God’s dwelling with humanity; do not claim the theatrical screen is itself sacred or make projected light the central motif |
| 07 Life / 白晝咖啡館 | **申 11:14 / Deut 11:14** (五穀、新酒和油) | **申 8:8** (seven products), **書 5:11–12** (after crossing, fruit of the land replaces manna), 何 2:8 (gift unacknowledged; warning, not only celebration) | **「五穀與新酒」**: wheat, barley, vine/grapes, figs, pomegranates, olive/oil, honey. Grain & vine can lead; use harvest and bounty rather than café cup rings | **七種出產不是七種穀物、也不等於七個版塊**；「五穀」在這個中文主題是穀物的統稱，並非精確五類穀物；「蜜」的具體植物來源須獨立核實 |

**Biblical source distinction.** The list of seven land products is
**Deuteronomy 8:8, spoken before Joshua’s entry**, not a list in Joshua’s
book. **Joshua 5:11–12** records Israel actually eating the land’s produce
and the cessation of manna. **Deuteronomy 11:14** directly names grain,
new wine and oil, and therefore anchors the Café’s *primary* verse.
Hosea 2:8 is prophetic criticism of failing to acknowledge the Provider,
so it must not be cropped into an unconditional feel-good blessing.

**Cinema — theology determines the picture and movement.** Christ is the
fulfillment of divine dwelling among us (John 1:14 uses tabernacle/dwelling
imagery); Hebrews 10:19–20 links access to God to Jesus’ blood and the
veil, interpreted as his flesh. Matthew 27:51 describes the **temple veil
torn from top to bottom**, not a conventional theater curtain parting.
A cinema-sized grand curtain may be the design analogy, but its *drawn*
fabric, needlework, cherubim and opening sequence must be rooted in
Exodus 26:31–33 and the New Testament fulfillment. Test a top-origin
release/parting grammar rather than generic side-to-side curtain animation.
Reconciliation (2 Cor 5:18–19) is the meaning; lights, film projector beams,
floating particles and lens flare may be absent or subordinate.

**Production/QA binding:** for all five newly produced surfaces register
`realm`, `primary_scripture`, `supporting_scriptures`,
`biblical_subject`, `source_and_rights`, `engraved_material`,
`direction_field`, `hatch_density_and_lighting`, `motion_semantics`,
`print_safe_area`, `reduced_motion`, and `acceptance_state`.
All five should be art-directed as one **coherent Doré Motion batch**,
then independently judged. A single repeated CSS gradient cannot pass.
Do not edit accepted Church/Magazine sources, author new literal Bible
quotations without verifying the translation, or merge experiments
before real visual review.

Scripture links (KJV cross-check):
[John 7:38](https://www.biblegateway.com/passage/?search=John+7%3A38&version=KJV) ·
[Rom 13:12](https://www.biblegateway.com/passage/?search=Romans+13%3A12&version=KJV) ·
[Luke 24:27](https://www.biblegateway.com/passage/?search=Luke+24%3A27&version=KJV) ·
[Matt 24:3](https://www.biblegateway.com/passage/?search=Matthew+24%3A3&version=KJV) ·
[Jer 30:2](https://www.biblegateway.com/passage/?search=Jeremiah+30%3A2&version=KJV) ·
[Heb 10:19–20](https://www.biblegateway.com/passage/?search=Hebrews+10%3A19-20&version=KJV) ·
[Ex 26:31–33](https://www.biblegateway.com/passage/?search=Exodus+26%3A31-33&version=KJV) ·
[Matt 27:51](https://www.biblegateway.com/passage/?search=Matthew+27%3A51&version=KJV) ·
[Deut 11:14](https://www.biblegateway.com/passage/?search=Deuteronomy+11%3A14&version=KJV) ·
[Deut 8:8](https://www.biblegateway.com/passage/?search=Deuteronomy+8%3A8&version=KJV) ·
[Josh 5:11–12](https://www.biblegateway.com/passage/?search=Joshua+5%3A11-12&version=KJV).

**Acceptance.** Preserve the frozen original seven-color Magazine spine
and original Church as read-only source layers; compare exact bounding
rectangles of Magazine, Bible and Sermon at 1648×928 and 390×844, plus
reverse scroll, 200% zoom and reduced motion. The fixed outer field and
individual inner layouts have different owners: do not force every chapter's
content into the same typography or internal grid merely because their
outer rectangle aligns. Keep all work under Design OS and the existing P2
owning CSS/JS; do not introduce a second global engraving manager.

### P2 / 03 — EMMAUS / ONE 三重身份與選卷可見性（多雷探索，2026-11-01）

**Status: comparative editorial research and implementation brief, not a visually accepted or deployed design.** This is an application of §2's hierarchy / §3's reference method to the 03 Bible folio. It does not create a new global OS rule, supersede existing tokens, change 02 Magazine, or approve any screenshot.

**Current failure, from P2 visual review:** the fixed chapter title EMMAUS / 以馬忤斯, selected Bible book, selected chapter number and chapter study title have competing or nearly identical apparent weights; reader cannot identify the book (e.g., John / 約翰福音) or chapter (e.g., Chapter 03) without searching microscopic metadata. Multiple atlas/chronology/commentary modules crowd the top while the center has dead space. Decorative scripture gold cannot compensate for absence of meaningful grid, type scale, or current-location hierarchy.

**Non-negotiable information architecture (three distinct identities):**

1. **Realm, persistent and unmistakable:** `03 / 07 — EMMAUS / 以馬忤斯`. An art-directed editorial masthead in a fixed position. This DOES NOT change as the user chooses books.
2. **Selected source, equally unmistakable:** `JOHN / 約翰福音` (or the canonical selected book from original ONE), followed immediately by `CHAPTER 03 / 第三章`. This pair MUST update together on selection and remain visible; a tiny `BOOK 43` or an unlabeled `03` is not sufficient.
3. **Current chapter topic and reading:** the real chapter heading from ONE, then Scripture / authentic ONE chapter study content. Book name, chapter number, and topic may not have near-equal size/weight. Fallback for absent commentary should NEVER invent content.

**Proposed desktop optical hierarchy at the APPROVED inner Magazine folio (measured in the actual left 2/3, not whole viewport):**

| Role | Visible example / data | Indicative local size (adjust via cqi and OS scope) | Visual rule |
|---|---|---|---|
| Fixed realm | `EMMAUS` + `以馬忤斯` | Bodoni 72–100px; Chinese Chiron 200 18–24px | Permanent dominant realm signature; no override by study state |
| Active Bible book | `JOHN` / `約翰福音` | Bodoni 40–56px; Chinese Chiron 200 26–34px | Actual book name (not just 43); second anchor |
| Active chapter | `03` + `第三章` | Bodoni 48–70px; Chinese Chiron 200 24–30px | Visible adjacent to book; canonical chapter index |
| Chapter subject | Actual ONE chapter title | Chiron 200 22–30px | Third-level feature heading, never tiny metadata |
| Study body | Scripture / book background / chapter content | Chiron Hei HK WS 400, ~14–17px readable at actual folio | Main reading space and stable measure; preserve source text |
| Tools / notes / folio | Tabs, provenance, gold scripture, atlas captions | Chiron 200 for every non-body Chinese editorial label, including controls, subject to legibility | Quiet subordinate material; no row of miniature rectangular CTAs |

The sizes are **research candidates requiring actual viewport and OS token verification**, not replacements for `westside-design-os.css`; ensure 200 weight never substitutes for actual readable Chinese body. Use bounded cqi only after measuring the inner container. Book/chapter must be prominent at 1648×928, 768, 390 and 320; restore / preserve the **original one-row scrolling 66-book canonical rail** as approved, rather than 22×3 or any hidden drawer.

**Chosen composition, proposed for one A/B candidate:**

- **Editorial top (~15–18% of left folio):** fixed `EMMAUS / 以馬忤斯` with the gold Luke 24:27 / 24:32 frame subordinate. This is a REAL identity, not small admin text.
- **Source hero (~17–22%):** selected book and explicit chapter pair, `JOHN / 約翰福音  |  CHAPTER 03 / 第三章`, plus ONE's actual topic, separated from controls. On selection, update all of these atomically.
- **Primary content (~43–48%):** dominant Scripture reading/study column (~62–66%) and quieter context column (~34–38%). Atlas / chronology / links are contextual views, NOT four co-equal cards; show actual available ONE data, never an invented map or generic empty placeholder.
- **Bottom (~15–20%):** original one-row, big-number 66-book rail, selected book centered; chapter selection remains visible but light, subordinate and separate. Only ONE primary `open full ONE within P2` action.
- **Print / typographic discipline:** one structural gold scripture frame; no ornamental engraving within tool content; no background-image filling whitespace. Align columns to an optical grid. Never reflow during 02→03 / 03→04; preserve approved 2/3 + 1/3 folio dimensions and original Doré artwork.

**Evidence reviewed using §3 method; transferable mechanisms, not copied visual assets:**

| Precedent | Transferable mechanism | Constraint / failure risk |
|---|---|---|
| [Logos — Studying a Bible Passage](https://support.logos.com/hc/en-us/articles/28756499675277-Studying-a-Bible-Passage-with-Logos) | Scripture primary; linked context and research panel secondary | Don't import desktop multi-panel density |
| [Sefaria Resource Panel](https://help.sefaria.org/hc/en-us/articles/18472472138652-Quick-Guide-Meet-the-Sefaria-Library-Resource-Panel) | Contextual cross-references appear beside selected text | Don't make resource discovery overwhelm content |
| [ESV.org layout](https://d33n9snnr16ctp.cloudfront.net/articles/esvorg-how-to-change-the-interface-layout/) | Primary Bible always stays in main panel | Flexible support panes, stable reading text |
| [Bible Gateway tutorial](https://www.biblegateway.com/help/tutorial) | Explicit Book → Chapter → Passage sequence | Book selector and chapter may not vanish into metadata |
| [YouVersion book/chapter](https://help.youversion.com/l/en/article/o1fuge3gfh-change-bible-version-or-language) | Current Book + Chapter permanently observable | Don't transplant mobile chrome into magazine |
| [STEP Bible](https://stepweb.atlassian.net/wiki/spaces/SUG/overview) | Original languages and scholarly research accessible from reading | Deep tools are on-demand, not always visible |
| [Blue Letter Bible Tools](https://blogs.blueletterbible.org/blb/2025/10/23/new-tools-functionality/) | Research follows the selected verse and next/previous context | No button explosion in base folio |
| [BibleProject app](https://bibleproject.com/app/) | Canonical narrative / book context frames reading | Avoid decorative tiles supplanting Scripture |
| [Bible Hub Commentary](https://www.biblehub.com/commentaries/) | Rich commentary attached to actual reference | Density is NOT the desired magazine layout |
| [Met Heilbrunn Timeline](https://www.metmuseum.org/ko/toah/about) | Real chronology and geography linked to curated textual explanation | No invented timelines; don't force unrelated map |
| [The Paris Review — Pentagram](https://www.pentagram.com/work/the-paris-review) | Authored hierarchy, controlled literary masthead, negative space earned by reading | Use Westside OS fonts, not its proprietary typography |
| [The Pudding — 2025 OJA](https://awards.journalists.org/entries/the-pudding-4/) | Reader-led visual explanation with interactive affordances | Never trade discoverability for novelty |

**Award-calibre gate:** [D&AD 2026 Digital Experience Design](https://www.dandad.org/awards/d-ad-awards/categories/digital-experience-design) explicitly prioritises **execution over idea**; design distinction does not excuse a hidden reading position. Acceptance is blocked unless: (a) at 1648×928 the user can visually identify EMMAUS, selected book and selected chapter immediately, in that hierarchy; (b) clicking John / chapter 3 updates primary source title, chapter number, text and linked Doré state without reflow; (c) readability survives 390/320px, keyboard and reduced motion; (d) original 66-book horizontal navigator works, and no unwanted secondary CTA row is introduced; (e) real browser screenshots, not JS syntax or Cloudflare deploy, show coherent composition and no overlap. These are implementation/review gates, **not claims of award certification**.

---

### 2026-11-02 / 多雷探索 — 三個新參考入口與 P2 ONE 版式定向

**工作指令語義：** 沿用本手冊「多雷探索」：外部成熟實例／開源／免費／成本／維護搜尋 → 提煉可複用機制 → 回到 Design OS 與原工程 → P2 真實畫面驗收。此處「多雷」不是限定畫家 Gustave Doré 或雕版畫風；不是要求重新出圖。使用者提供的兩張 P2 截圖為真實缺陷基線。

**新列入並保留的三個長期研究入口（2026-11-02 查證）：**

| 原站及直達入口 | 成熟度與用途 | 開源／成本／限制 | 本輪採用決策 |
| --- | --- | --- | --- |
| [Recent](https://recent.design/)／[Websites](https://recent.design/websites)／[Info](https://recent.design/info) | 2023 年建立、2026 年重啟並取代 Godly；含網站、動效、品牌和介面案例，有 Editorial 類型。 | 公開案例可瀏覽；個別案例著作權不代表開源。網站部份素材在純文字擷取只露縮圖，須逐例查證。研究使用不加 P2 程式依賴。 | **收錄：近期數位編輯／動效發現入口**。提取版式運作方式，不抄表面。 |
| [Siiimple](https://siiimple.com/)／[Magazine](https://siiimple.com/category/magazine/)／[Typography](https://siiimple.com/category/typography-2/)／[Grid](https://siiimple.com/category/grid/) | 自 2008 年起長期人工策展的極簡網站庫；標籤分類可追蹤，適合比對排版、留白與可讀性。 | 免費公開瀏覽；被收錄圖片及字體並不授權複製，不能把設計案例當成可直接移植的開源碼。 | **優先採用：用作減少噪音、層級、字距與留白評鑑庫**。 |
| [Cosmos](https://www.cosmos.so/)／[官方基本說明](https://help.cosmos.so/en/articles/17508467-cosmos-basics)／[訂閱說明](https://help.cosmos.so/en/articles/17508556-your-account-and-subscription) | 可保存視覺元素、組 collections，支援色彩搜尋與相似元素探索；web／iOS／Android。 | 一般使用免費，Premium 可選，進階協作／批量匯出／自訂 grid 屬付費功能；每項圖片的權利逐件核實。使用者指定 [元素 915285079](https://www.cosmos.so/e/915285079) 本次無法讀取其實際畫面，**待人工核對，不推測其構圖或授權**。 | **收錄：參考保存與視覺比對入口**；該單一元素在確認前不作版式依據。 |

**有來源的成熟參考與採否理由**（全部只借機制，非已取得的可重用素材）：

1. [Domus / Salottobuono 十二欄編輯格線](https://www.domusweb.it/en/interviews/2011/05/16/the-new-look-of-domus-an-interview-with-salottobuono.html)：按文章需要組合「兩欄正文＋一欄邊註」，控制圖文資料的閱讀優先度。**本輪首選原理**。
2. [Domus / Mark Porter](https://markporter.com/work/domus)：同一刊物的歷史編輯身份可以用在印刷與數位；採用跨媒介格線概念，不引入外來字體。
3. [The Paris Review / Pentagram](https://www.pentagram.com/work/the-paris-review)：文學標題與節制的負空間；借秩序不借巨大標題。
4. [Sight and Sound / Pentagram](https://www.pentagram.com/work/sight-and-sound/story)：明確格線／閱讀節奏；借欄位導航，不借跨過正文的視覺撞字。
5. [Siiimple / Cereal Magazine](https://siiimple.com/category/magazine/)：留白與輕量索引；借選卷資訊的 microtype，不縮小經文。
6. [Siiimple / MacGuffin Magazine](https://siiimple.com/category/magazine/)：邊緣導覽與雜誌核心視覺分工；不移植購物導向 CTA。
7. [Siiimple / Aeon](https://siiimple.com/category/magazine/)：文字為中心的文學編輯層級；不把長文堆疊在多雷版畫上。
8. [Siiimple / Palime Archive](https://siiimple.com/category/magazine/)：緊湊的索引和資料 register；不借其大面積高飽和色彩。
9. [Siiimple / Migrant Journal](https://siiimple.com/category/magazine/)：強烈獨立刊物身份；**不採用其撞色**，P2 有固定 ONE 紙色。
10. [Siiimple / London Gallery Weekend](https://siiimple.com/category/magazine/)：文獻導覽和圖像空間的分工；採用邊註概念。
11. [Recent / Editorial 網站分類](https://recent.design/websites)：持續發現新作品；個別未核對案例不算已驗證實例。
12. [Cosmos / 915285079](https://www.cosmos.so/e/915285079)：**待確認來源內容，不能冒稱已看見畫面**。
13. [Sefaria / Resource Panel](https://help.sefaria.org/hc/en-us/articles/18472472138652-Quick-Guide-Meet-the-Sefaria-Library-Resource-Panel)：經文主體維持中心，旁欄依所選經文顯示上下文。
14. [Logos / Studying a Bible Passage](https://support.logos.com/hc/en-us/articles/28756499675277-Studying-a-Bible-Passage-with-Logos)：研究資料可深度開展，但基礎畫面不能被工具淹沒。

**正式版式候選：Domus manuscript + responsive marginalia**

- P2 整體仍是左 2/3 ONE 研讀、右 1/3 原多雷圖庫；左頁內部採約 **7/10 經文閱讀＋3/10 研究邊註** 的桌面格線。用「選卷與章次刊頭 → 中英逐節聖經正文 → 右側按需讀的史地／段落／六種 ONE 功能 → 底部原 66 卷導覽」建立清楚的階層。這是 Domus「正文＋邊註」的延伸，不是新增四張卡片。
- 中文經文以 Design OS 長讀字體和 400 weight 呈現；Chiron 200 只用於夠大的空靈標題，不用於微小控制。English quotation 用現有 Bodoni Moda，經文引用用 genuine italic；真實字寬與中英孤字需在 browser 驗。
- 原有 66 卷橫向導覽、章次、逐節、史地、串珠、問題、預備和原 241 幅圖庫保留且同步；小屏優先展示正文，工具退到從屬但仍可操作的位置。
- 綠色 5:8 EMMAUS 右封面只保留 **路加福音 24:27**，移除 24:32。經文只佔金色植物框**內側的純綠安全區**，不能壓住左右植物壓花；整體封面幾何、壓花母本及翻頁軸不動。
- **工程／成本判決：** 使用原生 CSS Grid、既有 Westside Design OS token、P2 scope CSS 與 ONE 實數據；不裝新 JS 庫、付費參考工具、另一設計系統或沒有必要的 grid 依賴。研究網站是資料來源，並非 runtime。
- **實際驗收：** 1648×928、390×844、320px、200% zoom、單字孤行、長卷名、切章切卷、鍵盤、scroll reverse 和 reduced motion 的真實 screenshot + DOM 檢查，未取得視覺證據前不宣稱獲獎級或已定稿。

### 2026-11-02 / P2 ONE 書卷研讀頁 — Domus 研究正式落地 V20

此輪**不是**再單獨修改 7:3 CSS 欄寬，而是將現有 ONE HTML 的閱讀區重構為完整編輯格線，實際工程僅在 PR #1381 Draft；尚未進行真實 Chromium 全視口驗收，不等同通過獲獎標準。

- **新的唯一左頁版式 owner**：`static/css/p2-emmaus-domus-folio-v20.css`（排在所有舊 ONE／Scripture／bookbinding 之後，並與主題經文封面的獨立 CSS 分隔）；外側雜誌、原 Church、右側 241 幅多雷、正反翻頁及原 66 卷導航均不重新繪製。
- **Editorial book masthead**：固定承接 ONE 真實選卷／章次；英文字卷名使用既有 Bodoni Moda，在桌面最大約 100px；右側是獨立的大章次約 118px；完整章節條跨左頁整寬，長卷名依真實字數縮放，不可截成無意義省略號。
- **Chapter→reading**：原 `emmaus__study-cols` 改為 `display:contents`，使章題、雙語逐節經文真正在網格主欄；章題自微小元資料提升為可辨識大標，經文獨立滾動但保留 CUV/KJV 原字、章節和節號。
- **Marginalia**：原 `emmaus__context` 成為右側連續邊註欄，新增語義 `研讀邊註` header；原有史地、段落、導讀／歷史／串珠／問題／地圖／預備、以及四個 ONE 入口仍以原數據和行為受控，沒有在雜誌左頁製造另一套資料或不必要的元件。
- **Mobile**：此重排限定在 `min-width:901px` 桌面展示；原 390px／320px 選卷與研讀互動維持，新增邊註刊頭在窄屏不額外占用第四行。
- **工程驗證**：`tests/p2-emmaus-olive-preview.cjs` 新增真 DOM 的位置和 computed-style 關係驗收：卷名／章次主標，整頁章次條，主經文與右側筆記格線，全部六個工具分頁和四個入口。此項只描述已加入的測試，沒有聲稱瀏覽器全測已成功。

**藝術判斷**：以已核實的 *Domus* 十二欄「正文＋邊註」為排版機制，參照 *The Paris Review* 的小標記和高對比層次；不是把整頁資料變成四卡 dashboard。下一輪評估必須比較舊圖中「LUKE / 24 僅佔局部，祂已經復活了很小，研究欄過密」和新版畫面，從真實截圖決定是否還要再壓縮研究密度。

### 2026-11-02 / P2「西望」雙字：12 張 Cosmos 漢字設計研究 → 新字骨提案

**本輪新增交叉參照（已提交到 P2 Draft）：**[P2-XIWANG-TYPE-REDESIGN-COSMOS-20261102.md](P2-XIWANG-TYPE-REDESIGN-COSMOS-20261102.md)。按使用者實際提供的十二張 Cosmos 網頁截圖逐張標記可觀察的漢字海報特徵、可借的設計原理和不可移植的風格；照片不能當作可直接使用的 SVG 字型，也不冒認原作者或授權。

**定向：**以 A「筆骨・活字 / Ink-Bone Letterpress」為下一輪**優先試稿**；B「反白字骨」是幾何負形對照；C「墨勢重疊」是書寫動勢對照。重點是「西」「望」的真正原創**字內白、粗細承重、重心、結體、真實墨肉與墨筆收束**，而非沿用現有 2.1 MB 遮罩再改顏色和陰影。此現代視覺研究與已批准的**張即之真寺額、07/09 雙基準、正楷向大行草、雄渾、禁篆隸／清皇帝／摩崖取字**保持連續，不把任何已淘汰的歷史字形偷渡回來。

**實際 P2 工程安全線：**現有 \`static/images/xiwang-ink-vector.svg\`、晨星 v5.3、\`#dual-dore-plate\`、12 種 Contents 目錄、右側正式 \`westside-watch-masthead-landscape.svg\` 完全保留；新字形必須先在 Draft 的 opt-in native SVG 對照中接受 1648／768／390／320px、正逆滾動及減少動效檢查。**此輪是已歸檔的可施工修改方案，還不是已製成／上線的字標。**

### 2026-11-03 / New authoritative poster decision — overrides the old Magazine spine and calligraphy

**User-approved supersession:** the Magazine no longer needs its legacy Doré plate or brush-written Xi Wang; Doré's art now specifically identifies Emmaus. The Magazine owns **two full-size graphic-design campaign posters**, not an engraving+Contents folio. [A1 Geometry / B1 Engraving / Sevenfold poster contract](P2-XIWANG-CAMPAIGN-POSTER-SEVENFOLD-20261103.md) is authoritative for Chapter 02 and overrides earlier conflicting "frozen spine", "same artwork" and "Zhang Jizhi mandatory letterform" rules. Existing approved RIGHT 5:8 official cover stays protected.

**Sevenfold = homepage mechanics, not a narrow rail.** Actual source checked: first-look-host.js makeFolds() creates seven full-viewport descending planes on the same reversible timeline; sevenfold-dawn.css uses scaleY from the top; SEVENFOLD-DAWN-NAVIGATION.md describes all seven Design OS tokens, intact homepage film and links. In P2 the old colored #dual-continuum is **visually removed and inert** while a temporary geometry-only anchor is kept to avoid damaging downstream 03–07 coordinates. Seven OS folds now occupy the entire left poster surface, then reveal A1 or B1; no persistent colored bands. P2 scroll reversibility calls for deterministic rather than homepage randomized order.

**Two complete routes:** A1 large modern geometric Xi Wang word-image, B1 engraved native-SVG dot/wave/line-density type. The user-supplied pink-red and grey-engraving posters are reference methods, **not cleared reusable assets**. Both variants are original editable SVG studies, no generated image, no external paid dependency. Current type silhouettes are still preliminary Chiron-based compositions; a final custom-optical wordmark is not yet approved. Responsive, 200% zoom, reduced-motion, scroll reversal and real screenshots are mandatory before release.

### 2026-11-03 / A 幾何字型＋B 3–7 組刻線字的開源工程探索

**最新使用者要求：**A 只做一組巨大的兩字「西望」；B 不沿用 A 的字形輪廓作表面換皮，而用 **3–7 組各自有不同刻線結構／不同 Design OS 版塊色的「西望」**，可以評估 3／5／7 組的真實雜誌對開節奏。**專門的代碼／授權／維護／集成研究**： [P2-XIWANG-A-B-OPEN-SOURCE-CODE-EXPLORATION-20261103.md](P2-XIWANG-A-B-OPEN-SOURCE-CODE-EXPLORATION-20261103.md)；此文取代過往「B = A 一組巨大刻線字」的設計假設。

**選型：**A 首選 [PathBool.js](https://github.com/r-flash/PathBool.js)（MIT）＋[opentype.js](https://github.com/opentypejs/opentype.js)（MIT）取得／重組兩字 Bézier 輪廓；以 [Paper.js](https://github.com/paperjs/paper.js)（MIT）與 [skia-pathops](https://github.com/fonttools/skia-pathops)（BSD-3-Clause）驗證複合 path／精修。B 首選 [d3-shape](https://github.com/d3/d3-shape)＋[d3-contour](https://github.com/d3/d3-contour)（ISC）作順形與彎曲刻線幾何引擎，參照 [flow-lines](https://github.com/msurguy/flow-lines)、[hatched](https://github.com/plottertools/hatched)、[svg-halftone](https://github.com/evestera/svg-halftone)（均 MIT）分別研究流線、平行／同心線與網點。工具**只在 offline SVG 生成階段使用**，不添加 web runtime 依賴，未經許可不動現在 PR 的 poster render 文件。

**重要授權否決：**公開 GitHub 上的 [Halftone Pro](https://github.com/petra-dot/halftone-pro/blob/main/LICENSE) **實為 Proprietary License**，不是開源代碼，且依賴 Adobe Illustrator；禁止複製或直接納入 P2。A 工具 [Glyphr Studio 2](https://github.com/glyphr-studio/Glyphr-Studio-2) 是 GPL-3.0，可作外部獨立編輯器，**不將其程式碼嵌入站點**。另核實 Noto CJK 輪廓實際 OFL license，不能假定所有第三方字體素材可任意再授權。

**進度區別：**本輪 **來源 research＋選型＋手冊入檔完成**；並非已完成 A 重新製字或 B 多組 SVG，更不是視覺驗收成功。A、B 的現有 v1 已知同源字骨與常規效果問題，必須重建再用 1648／768／390／320 真實 browser 畫面校準。

### 2026-11-03 / 《西望》A2+B2 正式工程接入與可重建向量母本（非藝術定稿）

**已經實際製作／接入 P2 Draft：** `scripts/xiwang/generate-posters.mjs` 生成 `static/images/xiwang-poster-a-v2.svg` 和 `static/images/xiwang-poster-b-v2.svg`。`static/js/p2-vol00-poster.js` 改為載入上述 **外部原生 SVG、不是運行時幾何生成**；保留原 sevenfold 全幅倒帶、A／B query 切換、舊七彩條退出及右側正式 5:8 封面。舊 runtime 已封存 `static/js/p2-vol00-poster-v1-archived.js` 作安全回退。

A2 為兩個手工構造的大型幾何「西」「望」向量構件，`data-authority="original-geometry"`，不繼承 v1 Noto 普通粗字骨作 A 圖本體。B2 是真正的七組橫排「西望」，每組 `data-poster-word="1..7"`，分别對應 Design OS 七種原色，使用 flow、radial、halftone、contour、hatch、crosshatch、concentric 七種實際原生 SVG 線場，而非把 A 改色。B 的文字形狀輪廓起點來自已授權的 Noto CJK（OFL 1.1），本輪沒有新增 JS runtime 依賴。

**驗收紀錄：** 原生 generator 可重複 build 並通過 GitHub Actions `git diff --exit-code`，Cloudflare 已成功部署到 PR #1381 的隔離頁。已實際檢視 Chromium 1648 與 390 截圖：兩張非空白，B 七組可見且具有編輯節奏；A 與 B 均需下一輪**藝術品質／字骨光學**驗收，不能聲稱得獎級。第一次 CI 於手機 239×240 縮圖對七色的精確 RGB 匹配過度嚴格，測試已改為「桌面驗證 5+ 色、手機檢查真實圖形密度並核對 source 7 色」；不因此放寬圖形顯示本身的驗證。

**主站保護：** P2／03 Emmaus、教會、homepage 七層折疊、右頁城市封面及其 scripture 原碼未修改。所有修改維持 Draft，不自動合併 main。

### 2026-11-03 / 最新覆核：淘汰版「西望」不得再用，B 改成正立疊合刻線（研究定向）

**最高優先的新規格**：[《西望》字骨重製／B 七層疊合刻線多雷探索](P2-XIWANG-NEW-GLYPH-OVERLAY-ENGRAVING-RESEARCH-20261103.md)。本項研究已確定此前 A2 一般幾何巨字及 B2 七排橫向字樣不符合使用者參考；**不能以已淘汰的「西望」SVG（含舊刊頭和 A2/B2）為新字骨**。A 從新字骨製作僅一組上「西」下「望」的正立巨字；B 以原灰底刻線參考為尺度，**七組各自有獨立刻線和 OS 色的「西望」共同豎直疊合成一幅構圖**，不得傾斜、七個獨立橫列、字外刻線／底紋、舊字形七次換色。

**研究的開源路線**：A = FontForge／fontTools + skia-pathops（PathBool.js 只作可核查候補）；B = 在字形 `Region(outer,holes)` 上生成真正受輪廓約束的線條，重點審查 [penfill](https://github.com/piLeoni/penfill)（MIT／Apache-2.0，較新的實驗候選）、d3-contour／d3-shape、vpype；另對 FANGCUN 和 VecGlypher 保留研究但不當作可直接生產的可靠字稿。**本輪僅查資料與手冊修訂，不出圖、不施工、不修改現有 P2 runtime。**

### 2026-11-03 / 必須多輪多雷探索，不能再以「尚未找到工具」草率結案

**最新 A 海報工程決策**：[A 巨字海報 — 多輪開源製字工具與原始碼驗證](P2-XIWANG-A-MULTIROUND-DORE-EXPLORATION-20261103.md)。使用者要求**必須多輪探索，直到能找到具體可執行、適合全新「西望」字骨的工具為止**；遇到普通黑體加效果、只找到 README 或字型二進位、無法核實授權／輸出、兩字認不出來時，**必須繼續探索而不是把未通過的方案做成定稿**。舊 A2、淘汰刊頭和舊母本不可當新字骨。

已完成三類非重複搜尋（CJK stroke skeleton；現代 font editor／modular type；SVG glyph geometry），加一輪實際 GitHub tree／license 核查；**深入核對修正**：Skel Sans 有 OFL 字體但其 GitHub repo 沒有生成器源碼；**FANGCUN 確有約 3.6 MB 的單檔 index.html 程式碼**，不是只有 README，但公開說明有未填／待核實欄位、且尚未實測「西望」輸出。**第五輪最新技術候選**：先比較真正有原始碼的 **KAGE Editor（漢字筆畫編輯）、Kumiko（繁體 IDS 部件組合）、FANGCUN（3.6 MB 單檔參數化 App，待實測）** 的新「西」「望」字骨；再用 **Graphite／Inkscape** 做非破壞形變，以 **skia-pathops** 清理布林輪廓。不把 GPL 編輯器程式植入 P2。這些均未通過新字稿的光學驗收，不能宣稱「已找到滿意工具」。**這不是最終選型通過**：必須先用真「西」「望」新筆段做黑白 1:1 光學試驗、各尺寸與實際對開驗收；若仍像一般黑體，開下一輪搜尋，不能只調色／加斜切。

**工作狀態：本輪只多雷探索與記錄，未出圖、未生成新 SVG、未改動 P2 或右封面。** 此處研究僅在 single Design OS Manual 內作鏈接，不增加第二套 OS。

### 2026-11-03 / Poster-generation resources — existing corpus + new open-source poster engines

**先讀既有手冊，不要從零搜尋**：本 OS 原有 [Recent](https://recent.design/)、[Siiimple](https://siiimple.com/)、[Cosmos](https://www.cosmos.so/)、[Codrops kinetic typography](WESTSIDE_MAGAZINE_KINETIC_TYPOGRAPHY_REFERENCE.md)、[Italian Editorial Executable Grammar](../dore/italian-editorial-executable-grammar.v1.md)、[SVG Exploration List](SVG-EXPLORATION-LIST.md)，以及 [Westside Visual Reference System](../../dore-design/new-westside/VISUAL-REFERENCE-SYSTEM.md)。它們仍是 source of design judgment，**不是可直接貼進網站的授權海報/字體**。

**最新補充：[P2《西望》Poster Generation Resource Atlas](P2-XIWANG-POSTER-GENERATION-RESOURCE-ATLAS-20261103.md)**。開源／原始碼篩查包含 **flowshape**（MIT，資料化 poster composer、合法 aspect ratio、字長溢出處理、seeded SVG）、**Poster/poster-ai**（MIT，TSX→SVG/PDF/PNG）、**Satori**（MPL-2.0，HTML/CSS→SVG）、**canvas-sketch**（MIT，離線 generative drawing）、**p5.plotSvg**（MIT，筆繪 SVG 線條）、**Graphite**（MIT/Apache-2.0，非破壞性幾何）、**d3-contour/d3-shape + penfill**（B 字內線場）、**yft-design**（MIT，獨立 poster editor 研究）及印刷輸出 Typst/Paged.js。**重要排除**：generative-poster 雖有可觀察的 15 種生成器，repo 未發現 LICENSE，不能抄程式；Doory 是 Attribution Assurance License 且屬完整多層編輯器，並非適合本站輕量 SVG 的 MIT 組件；付費黑箱工作流不採用。

**成熟海報研究新增入口**：[typo/graphic posters](https://www.typographicposters.com/)、[Letterform Archive](https://letterformarchive.org/online-archive/)、[Design Reviewed Archive](https://designreviewed.com/archive/)、[HMCT Archive](https://hmctartcenter.org/archive)、[Poster House](https://posterhouse.org/)、[Fonts In Use](https://fontsinuse.com/)、[TDC](https://tdc.org/)；按設計師／時間／造型／可借機制入庫，**不得把作品展示等同於開源授權**。

**本輪藝術閘門不變**：A = 新字骨、僅上「西」下「望」兩個巨大正立字，不沿用已淘汰 SVG；B = 七組正立「西望」同幅疊合、各用獨立刻線與既有七種 OS 色，字外完全無底紋，不能退回七條橫向展示列。**研究只記錄選型，不等於批准某一工具或海報 artwork，未出圖／未施工／未改 P2 runtime。**

## 9. Research retained as source-of-evidence

These files remain archived intact; they do not operate as independent OS authorities:

- [Westside Editorial Typography](WESTSIDE-EDITORIAL-TYPOGRAPHY.md)
- [Doré Award-Calibre Digital Art Direction Corpus](../../dore-design/AWARD-CALIBRE-DIGITAL-ART-DIRECTION-CORPUS-2026-09-09.md)
- [UI Skills Exploration R1](../../dore-design/UI-SKILLS-EXPLORATION-2026-09-12.md), [R2](../../dore-design/UI-SKILLS-EXPLORATION-R2-2026-09-12.md), [R3](../../dore-design/UI-SKILLS-EXPLORATION-R3-2026-09-12.md), [R4](../../dore-design/UI-SKILLS-EXPLORATION-R4-2026-09-12.md)
- [Executable Italian Editorial Grammar](../dore/italian-editorial-executable-grammar.v1.md)
- [Magazine Kinetic Typography Reference](WESTSIDE_MAGAZINE_KINETIC_TYPOGRAPHY_REFERENCE.md)
- [New Westside Editorial Web Skill](../../dore-design/knowledge-lab/skills/new-westside-editorial-web/SKILL.md) and [Visual Grammar / Creative Rubric](../../dore-design/knowledge-lab/skills/new-westside-editorial-web/references/visual-grammar.md)
- [Editorial Web Maturity Study](../../dore-design/knowledge-lab/research/editorial-web-maturity-study-20260901.md)
- [Camera and Attention Grammar](../../dore-design/DORE-EXPLORATION-CAMERA-ATTENTION-GRAMMAR-2026-09-09.md)

**Revision rule:** update the relevant chapter *here* for any new editorial judgment; update OS tokens only if an approved cross-surface token truly changes. Never import original research documents as CSS/JS, and never replace an existing HTML asset merely to attach the manual.


### 2026-11-03 / 新增 mono-color-skill；海報工具必須實際調用，不再只研究

**已收錄：[yanliudesign/mono-color-skill — Monocolor Editorial Print](https://github.com/yanliudesign/mono-color-skill)**（上游 README v1.2.0；[SKILL.md](https://github.com/yanliudesign/mono-color-skill/blob/main/SKILL.md)；[LICENSE](https://github.com/yanliudesign/mono-color-skill/blob/main/LICENSE)；[ASSET-LICENSE.md](https://github.com/yanliudesign/mono-color-skill/blob/main/ASSET-LICENSE.md)）。該 Skill 的一/雙油墨角色、25–55% 結構性留白、單一視覺主題、不自動做舊及印刷主次，列為《西望》A/B 海報的**藝術方向方法**，不是現成的 CJK SVG 刻線生成器。軟體及 Skill 指令採 MIT，但 `examples/` 作品和第三方參照圖不涵蓋在 MIT 之內，不能直接挪用為本站圖稿。

**執行路由正式入口：[《西望》Poster Toolchain — 實際工具執行規範](XIWANG-POSTER-TOOLCHAIN-EXECUTION.md)**。這不是新 OS 或 runtime；任何後續海報工作，在出稿之前須依任務選工具並記錄 `researched / available / executed / reviewed`，不可跳過字骨/刻線/版式工具直接把生成點陣圖宣稱為原生 SVG。**B 的七個 Design OS 語義色與七組正立字保留，不能因 mono-color 只有兩色印刷示例就改掉七層規格**。A 為單組原創西望巨字；B 為七組不同筆骨/刻線在同一版心交疊，不傾斜、線條只存在字內、不用七排色標／無故黑底／額外圖示。

**本地工具入口：** `node scripts/xiwang/poster-toolchain.mjs plan a|b` 預檢是否找到本機需要的工具；`init a|b RECEIPT.json` 生成空白執行記錄；`verify RECEIPT.json` 阻擋未附原生 SVG、實際工具操作證據、完整尺寸截圖與人工藝術判斷的交付。它不會替使用者自動安裝/執行第三方 GUI 工具，亦不會修改 P2；通過紀錄檢查不等於設計必然獲獎。若工具在環境不可用，要明確標註並選實際可運行的替代，不能假裝調用。下一步才是在隔離 Draft 上以工具真的製作 A/B，不再重複純出圖。

### 2026-11-03 / 不是再收藏工具：B 真實 SVG 印版生產已可重建，藝術仍未過關

**實際工程成果與多輪判定：[《西望》B Poster Toolchain RUN](XIWANG-POSTER-TOOLCHAIN-RUN-20261103.md)**。已在本輪用 `fontTools` 輸出 licensed CJK glyph contours、`Shapely` 真正做字孔/線場交集、`SVGWrite` 匯出原生路徑，並由 Inkscape 1.4 完成 B4–B9（含隔離 B7）的向量渲染及 B7 四寬度 export。B7 第二次建置 SHA-256 完全一致，含 7 個 `data-word-layer`、1275 paths、0 `<image>`、0 rotate；運行工具與候選庫的「已閱讀但未使用」明確區分。

**工程入口已從 `plan` 擴為實際 `build b`**：`node scripts/xiwang/poster-toolchain.mjs build b ./xiwang-poster-output`，調用 `scripts/xiwang/build-engraved-b.py`，需本機免費 Python build 依賴與明確的 OFL CJK 字型。生成器/隔離 [B7 SVG](../../static/experiments/xiwang-printplate-b7.svg) 和 [獨立預覽](../../static/experiments/xiwang-printplate-b7.html) 均不接管 P2 runtime；工具不可用即報錯，不能聲稱調用成功。

**藝術否決仍有效：** B7 字骨還以 Noto CJK 輪廓為源，缺乏獨立原創結構及足夠強的七組套版構圖，不能以 CI/轉圖成功判定「獲獎級」。B4、B5、B6、B8、B9 及其失敗原因已回填 run log，禁止下輪又換色/換同一種線場當成新進展。Chromium local/localhost 被此環境的 administrator 封鎖，真 browser P2、zoom、反向滾動及右封面對開尚未驗收；Draft #1381 不應合併或替換正式海報。下輪先真正重建字骨與套版關係，再做完整對開藝術驗收。

### 2026-11-04 / 《西望》A/B 設計方法改為「先案例、再排版、最後工具」

**正式研究索引：[P2 《西望》海報 A/B Composition & Case Atlas](P2-XIWANG-POSTER-COMPOSITION-CASE-ATLAS-20261104.md)**。已在使用者的 Library 中找回 **2026-11-02 的 12 張原始 Cosmos 收藏牆截圖（22.02.17 至 22.03.03）**，與 11-03 的粉底紅字／灰底白色刻線兩張最核心參考相互核對。**這十二張是多件作品的收藏牆截圖，而非十二張只有一件作品的海報；原圖只作使用者內部研究，不轉存公開 repo、不推定它們可商用**。

**新優先順序：**以使用者 22.02.59 截圖中的粉底紅色巨字作為 A「單組巨字／原創幾何筆畫與字內白」的主構圖案例；以用戶灰底點陣／同心圓／波浪／放射白線字海報作為 B「七組正立西望共同版心、不同密度/方向線場塑造一張海報」的主案例。參考圖的底色不是規範本體，B 不使用無理由的黑底；A 不能沿用 A2 字骨，B 不能變成七排字或 A 的換紋理。

**開源設計方法的新補充：**[350-layout-compositions](https://github.com/nevertoday/350-layout-compositions)（CC BY 4.0；版面構圖資料庫，注意二次素材授權）、[evo-poster](https://github.com/sergiomrebelo/evo-poster)（MIT；版式變化方法）、[Paper.js](https://paperjs.org/about/)（MIT；原創漢字筆段和負形）、[bouffont](https://github.com/meodai/bouffont)（MIT；字骨重組／SVG，**CJK 必須實測**）、[TYPE-O](https://github.com/lnyssen/type-o)（MIT；recipe、字形可讀性判據，內建以 Latin 為主）、[poster-grid-inspector](https://github.com/Ygria/poster-grid-inspector)（MIT；構圖格線判讀，可選模式需模型服務）；[Volorf/Processing-Posters](https://github.com/Volorf/Processing-Posters) 有 7 張真正成品和 p5.js→Figma 的作業方法，但未核到 LICENSE，**只借完整排版工序，不複製原碼**。之前 mono-color skill 的藝術主次、印版分工與留白原則仍使用。

**真正的下一輪要交付五個不同機制的比較 SVG 草案，不是再換色：**A1 原創全幅幾何巨字、A2 偏置負空間、B1 七重印版同軸交織、B2 連續刻線形成字、B3 受控錯版節奏。均不擅自改動 P2 右 5:8 封面、教會／Emmaus、首頁七重折疊或主站。這輪只完成案例找回、授權比對、設計方案和可施工訓練 brief，**還沒有新的可通過獲獎級驗收的 A/B 海報，不能宣稱定稿**。


### 2026-11-04 / 已選定 A 午夜藍海報接入 P2 Draft

**最新人工批准的決定：**以一組正立、上「西」下「望」的**深夜藍幾何巨字 A 海報**作為 P2 02 Magazine 左頁對開預設；B 七重刻線仍保留獨立創作與 `?poster=b` 對照，不代表 B 退出研究。與右側正式 5:8 午夜藍城市之光封面並排，以「大塊平面字形 vs 金光/城牆/經文細節」形成疏密對照。

**已在 Draft PR #1381 實際接入：**新增 `static/images/xiwang-poster-a-night-blue-approved-p2.svg`，由使用者選定的深夜藍 A 海報字形剪影製作**獨立原生 SVG 雙字路徑（西、望各一個）**並重排於 P2 1:1 左頁；維持深夜藍與柔和紙底。為避免與右側封面重複印刷刊次，對開稿只保留二字，不重複 `WESTSIDE WATCH`、`VOL.00` 或 slogan。這是已批准點陣視覺的輪廓向量化衍生，**不是宣稱已取得原始手工筆段曲線的完全可編輯源字稿**；獨立 PNG 原稿仍只供對照，不轉存為運行時 raster。

**路由：** `static/js/p2-vol00-poster.js` 的 default `poster=a` 現讀取上述 SVG；`poster=b` 分支和原七重全頁折疊/正反捲動控制原封不動。原 A2 SVG 保留為只讀歷史資產，不作現版母本；右側封面、Church、Emmaus、Homepage、Contents 時序及 03–07 均未改動。隔離實驗頁 `static/experiments/p2-double-square-video-lab.html` 更新腳本快取版本。

**驗收區分：** SVG XML/兩原生路徑、資產載入路由、B 不動、右側封面 DOM 仍在，都已靜態核對；**GitHub Actions 與真實 P2 browser 視覺、1648/768/390/320、200% 縮放、逆捲動及右側視覺光學 QA 尚待當前 commit 產生實際證據，不以靜態檢查取代批准**。Draft 未合併主站。


### 2026-11-04 / P2 雜誌最終過場：雙頁定格後縮小露出原影片；禁止持續霓虹

**使用者最新確定的動效方向：**保留 P2 02 已選的 A 午夜藍「西望」海報＋右側正式 5:8《城市之光》封面，待七重折疊與兩張作品均到位後，才將**整組對開同步縮小**，使原本已播放的首頁 `/preview/watch-city-vol00/hosanna/?cover=1` 影片從四周露出。不可從場景外飛入新圖，不可新建影片播放器或第二個 RAF clock。反向滾動同一條軌道完全回復；reduced motion 直接在最後狀態定格。

**已在 Draft 隔離 P2 實作：** `static/experiments/p2-double-square-video-lab.html` 使用原本的 `progress`，在 `p=.91..995` 用 smoothstep 將 `.dual-panels`（左海報＋右封面）整組從 `scale(1)` 收到 `scale(.85)`，不移動單頁相對位置；只在原本 poster/cover 均到位後動作。輸出 `data-poster-pullback`、`data-poster-spread-scale` 以利捲動斷點與 QA。這是 scene-owned transform，不改原有右封面 SVG、Church / Emmaus、sevenfold 或 P2 parent video。**真正瀏覽器畫面及 320/390/768/1648、反向滾動尚待實測驗收。**

**藝術評價：**七色可在開場擔任七重折疊的印版角色，但**不採用七色持續閃爍的霓虹海報**。原因：會破壞 A 巨字／紙底的明晰度、干擾右封面金色城牆和經文，並造成閃爍/可及性風險。若後續探索，僅可隔離 A/B 比較一輪極短、不重複的七色印版校準；不改正式 A 的深夜藍定格，也不能加入快速閃頻或持續光變。

### 2026-11-04 / P2 A Poster：七種字色＋背景同受「滾動」控制（最新決策，覆蓋七重折疊入場）

**本輪使用者明確要求的是 scroll-scrubbing，不是 auto-playing / time-driven flashing：** P2 02 Magazine 左側 A 海報的**字色和底色**都必須依循同一個可逆 `progress`（來自既有 P2 父頁滑鼠滾輪／觸控板捲動，`westside-p2-dual-progress` 同源訊息）前進或倒退；不可新建 RAF、setInterval、CSS keyframes 或第二套 wheel timeline。獨立 `p2-double-square-video-lab.html` 可在非 embed 模式由 wheel/trackpad 直接 scrub，用來驗證，嵌入式頁面不得自行攔截父頁滾動。

**新色彩段（可逆）**：`p .30–.76` 是七個原有 Design OS 語義色（活水、Magazine、Emmaus、Olive、Bookshop、Cinema、Cafe）的依序印版配色；字形主墨色依版塊色與深夜藍混合，**同時**左側紙／底色按對應語義色調和，不做外加的七張純色遮幕。`p .77–.8555` 收斂到正式 **午夜藍底 `--ws-night` + 黎明金 `--ws-morning-gold`「西望」**，以原本 A 字形雙 path 的透明 `mask` 與極克制的**靜態箔紋漸層**做燙金質感，沒有光效 timer；下方只以極細金線＋小型 *Watch for the Dawn* 補充編輯留白。七個色彩帶不是同時閃爍，也不是換掉 A 原本字形。原 A 深藍紙底 SVG 是 fallback / 舊母本保留，不把 mask 假稱原生新筆段。

**完整定格才縮小**：原兩頁已達到 5:8 封面＋1:1 左海報的對開布局，`p .8555–.945` 為藍金海報與右封面的完成狀態／捲動停留區；`p .945–1` 才使 `.dual-panels` 整組從 `scale(1)` 收至 `.85`，露出既有首頁影片。捲動倒退時整組放大並把字色與底色逐步倒帶，沒有另造影片、七色霓虹或外部進場素材。

**工程 owner（Draft PR #1381）**：`static/js/p2-vol00-poster.js`（純 `paint(progress)`、七色路由及墨紙混色）；`static/css/p2-vol00-poster.css`（遮罩、薄箔、slogan）；`static/images/xiwang-poster-a-glyph-mask.svg`（從已批准的 A 雙 path 提取**透明字形**）；`static/experiments/p2-double-square-video-lab.html`（parent progress + standalone wheel scrub / 完成後才縮小）。`poster=b` 保留 B 原圖作對照，不繼承已取消的七重遮幕；原 Church、以馬忤斯、右封面、Homepage 原七重折疊和已存在的影片播放器不改。

**進度/驗收區分：** 靜態核對通過（所有七色 token 有定義、mask 只有兩個 glyph path 沒有底色矩形、JS 語法和父頁進度綁定、無七重遮幕）。真 P2 Chrome/Safari 視覺、字形金箔渲染、1648/768/390/320、200% zoom、上下滾動和 reduced-motion 必須在最新 Cloudflare Preview 完成，**不能以程式核對取代藝術驗收**。

### 2026-11-04 / P2 A 藍金海報 → 原版 Contents → 整組縮小（最新驗收方向）

**使用者以 04:34 的真實 P2 截圖提出三個藝術問題：** 七色滾動已接近預期但略快；左側午夜藍與右側正式封面無分界地連接，損及右封面的獨立整體性；左側海報的孤立 slogan 沒有編輯版心依據。更重要的是 **Contents 必須在海報結束後出現，整個對開不得在 Contents 進場前縮小**。這項決定覆蓋上段過時的「藍金海報一完成便縮小」敘述，但不取消既有七色 scroll-scrubbing 與右封面保護規範。

**新過場（受父頁同一可逆 scroll progress 控制）：**
- `p .26–.77`：七種 OS 字色與背景逐版進行；比前一版的 `.30–.76` 區間更長；隔離預覽 wheel 敏感度從 `/2400` 改為 `/3450`，無自動計時。
- `p .77–.845`：收束午夜藍底＋黎明金燙金「西望」；`.845–.86` 完整雙頁定格。左海報字形不縮小。
- `p .86–.945`：左頁海報**不改自身整頁尺寸**，由現有 approved A glyph-mask 的兩個漢字 *縮至左上編輯刊頭*；底色同時釋放，下方露出原生 `#dual-stone-contents` / `p2x--10` Cereal 十二欄目與已有四篇章跳轉、全文閱讀入口，不另造/覆寫十二欄目資料。**右側 5:8 正式封面維持完整。**
- `p .945–.965`：Contents＋右封面完成後暫停，呈現實際對開排版。
- `p .965–1`：只在此時將兩頁 `.dual-panels` 同步從 100% 收至 85%，露出原先就在後面的首頁影片；反向滾動精確倒帶到完整海報；reduced-motion 可直接定位。

**版心藝術修正：** 原被隱藏的七重書脊所保留的 14–24px 位置，之前錯放在左頁**外側**，令兩張午夜藍連成一片；現在只在 P2 海報模式把間距移到真正的**左海報/右封面中間**，輔以一條極細的印版金色界線，而不是重新設計或拉扯右側城牆/門光。海報底部的 `Watch for the Dawn` 不再孤立漂浮，改成一條極細上引線下的左右 editorial folio，右端引用 `ROMANS 13:12`，全部遵守 OS 非正文極細層級；入 Contents 時退場，不與新目錄的 header 爭搶層級。

**工程 owner（Draft PR #1381）：** `static/js/p2-vol00-poster.js`（七色＋底色與 A 字形縮放）；`static/css/p2-vol00-poster.css`（印刷字骨、folio、Cereal Contents 局部排版覆寫）；`static/experiments/p2-double-square-video-lab.html`（正確書脊間距、目錄與縮小相位）；`tests/p2-vol00-campaign-posters.cjs`（真 browser 驗證雙頁間隙、12 筆資料、完整海報先於目錄、目錄先於整組縮小、反向倒帶）。現有 `p2-contents-twelve.js` 原資料、右側正式封面、教會、Emmaus、首頁七重折疊及影片 player 不修改；B 保留獨立 SVG 模式，不繼承 A 的 Contents 設計覆寫。

**品質界線：** 工程提交、腳本語法、現有字骨及 browser 截圖測試合格也不自動代表獲獎級藝術驗收。至少核對 desktop 1648、mobile 390、完整 Contents 狀態與逆向移動的真實 Cloudflare Preview，再決定版心和 slogan 的最終微調。Draft 禁止自動合併主站。


**封面滿版刊頭補充（使用者 2026-11-04 最新指令）：** 完整尺寸對開期間，右側官方 `westside-watch-masthead-landscape.svg` 刊頭的金色英文須**左右撐滿其 5:8 封面版心**；西望 A 的巨字縮成 Contents 角落編輯刊頭，絕不可造成右封面刊頭跟著收窄。既有 SVG 原稿與右封面城牆光線不改；以 scoped CSS `static/css/p2-vol00-poster.css` 設定光學寬度 106%、無額外 `transform`，讓 SVG 內建左右留白在當前封面比例下得到校正。只在 Contents 完整進場、對開停留完成後，`p .97–1` 才由 `.dual-panels` 整組縮放。新增 Chromium 測試檢查 `p .84` 和 `p .95` 的刊頭寬度比至少 1.055、局部 transform 必須為 none；不以代碼靜態檢查取代視覺驗收。


### 2026-11-04 / P2 Contents「Cereal × 編輯雙欄」重排與 03 以馬忤斯真實銜接

**來源／問題：** 使用者在 P2 100% Contents 實頁截圖中指出：西望金色角標、英文 Contents、四個篇章、十二個欄目沒有足夠清楚的視覺主次。舊版 `p2x--10` 來源是 Cereal × Engraved Light，但實際套用於左側正方形時出現主標過小、細字過密、可讀性不足。**這不是再做一個視覺圖或重畫 Contents 資料。**

**研究案例與轉用：** 以已收錄的 [十二種目錄案例實作](../../static/experiments/p2-contents-twelve.js) 為依據：Cereal（#10）紙張質感及精緻留白；François Girard-Meunier Swiss Counterpoint（#08）的雙欄資訊層級；W Magazine（#11）的英文主標尺度；Eye（#12）的目錄雙語索引。巨字「西望」已由 A 海報縮為小型燙金角標，現在要由 *Contents.* 而不是角標主導左頁。

**施工 owner：** 只在 `static/css/p2-vol00-poster.css` 對 `data-p2-poster=a` + 原 `#dual-stone-contents .p2x--10` 加排版層：頁眉 VOL.00 纖細、英文 Contents 大號 Bodoni Moda、Chiron 200 中文「目錄」、四篇章 WATCH/WALK/WITNESS/WORSHIP 雙欄網格、01–12 序號及中英正文足夠字級、金色只限極細索引及分隔線。正文及完整索引均由原 `static/experiments/p2-contents-twelve.js` 從 canonical `dual-movement` 資料生成，**十二個欄目、一切文案和全文閱讀入口不刪減**。當方形寬度不夠時，使用單欄可捲動的真文字頁，而非縮到 7px 或靠背景圖顯示漢字。閱讀者可點 FULL INDEX 開啟原有完整目錄。

**03 真實續接：** 不新增假以馬忤斯插圖，也不複製 ONE 另一份資料源。原 `static/experiments/p2-emmaus-olive-handoff-lab.html` 早已擁有同一個連續捲動 owner，內嵌 **教會→雜誌** 原畫面，`distance=6.50` 保持完成的 02 對開，之後沿既有轉頁 timeline 進入 **03 以馬忤斯 ONE（66 卷、章節、CUV/KJV、史地、241 多雷插圖）**，再接 04 橄欖山及 05–07。新版從完成 Contents 定格處開啟；在 02 專門調試頁中加入實際連續預覽入口。反向滾動回到 02，不二次載入模擬 Contents。右側 5:8 正式封面、滿版刊頭、原影片與教會畫面保持。**完整 P2 預覽應用此連續舞台路線，而非只有 02 的獨立 square lab。**

**獲獎級驗收：** 以 1648、768、390、320px + 200% zoom 覆核主標、角標、雙欄篇章與全文入口的實際閱讀次序；檢查 02→03→02 正逆捲動、ONE 66 卷可操作、圖片不破版、不重複播放器；附 Chromium 真截圖及失敗原因。這次 CSS 工程／連續路由能運作，並不自動表示已達藝術定稿；P2 Draft #1381 不合併主站。


### 2026-11-04 / 真實 P2 截圖再驗收：The Paris Review Contents × 封面完整翻頁 × ONE 經文

**來源與藝術機制。** 2026-11-04 06:17–06:18 四張使用者實際動效截圖。錯誤包括：（一）Contents 的 12 欄目被壓至頁面上半部，底部剩下大塊沒有理由的空白；（二）金色「西望」角標壓在頂部極細刊期字上；（三）Luke 24:27 的 ONE 主題經文在轉場可見於**雜誌**的藍金城門封面；（四）正式封面只轉約 86°，被切成一條窄條；（五）額外的「經上所指的基督」純文字頁缺乏多雷插圖，削弱過場節奏。

**The Paris Review 研究依據，不是拷貝字型或版式。** Pentagram 的 Matt Willey（2021）改版：https://www.pentagram.com/work/the-paris-review/story；AIGA Eye on Design 對於緊湊書本尺度、收斂封面字量、紙張觸感與閱讀比例的分析：https://eyeondesign.aiga.org/whats-past-is-prologue-inside-the-redesign-of-the-paris-review/。取用其**從內容密度建立版心**的設計方法：不設無用途的空白，不把 12 欄當可縮到 7px 的宣傳卡片，對齊刊號、標題、編輯分部與全文入口。在現有批准的雙頁內，左頁保留 OS Bodoni Moda 大號 *Contents.*、纖細 Chiron 中標、四個 WATCH／WALK／WITNESS／WORSHIP 目錄組，兩列按頁高比例分配；原 12 欄目真實 DOM 文字、次標、中英索引及完整閱讀器保留。小版寬仍為可捲動單欄。與巴黎評論不共用其商業字型，不改 Design OS。

**避免壓字。** 原 A 海報兩字印版縮為固定角標後，`p2x-cereal-tiny` 的刊期、編輯印記一律移到角標右側，不再從左 5% 開始而被金字壓住；P2 封面 `WESTSIDE WATCH` 左右撐滿、5:8 比例不變。

**主題經文與 OS：** 03 以馬忤斯真正的主題經文僅 `Luke 24:27 / 路加福音 24:27`，在自己的綠布燙金花卉封面展示，**不能**移到 02《西望》藍金城門封面。中文經文是正文，依 `static/css/westside-design-os.css` 的 `--ws-weight-zh-standard:400` + Chiron HK WS reading 角色；中文參照屬非正文極細 `--ws-weight-zh-air:200`；英文經文出處使用真正 Bodoni Moda Italic 400（依 OS 備註經文數字也為 italic），不可把引用本身變成硬 bold，也不可讓孤字修復 span 另起字重。入場的綠色 underleaf 在正面雜誌尚未翻開時 `display:none` 或 opacity 0，回捲同樣清除；正式封面沒有 ONE 經文節點。

**真正的翻頁，不裁切。** 原 cover 的 5:8 正式 DOM 構圖不可被縮窄或剪裁成半幅；以源 `#dual-cover` 沿書脊旋轉完整約 172°，讓原封面正面、極薄側邊以及素紙背面連續呈現。只在翻頁狀態臨時釋放內層 `dual-stage`／`dual-panels` 的 overflow，背面是位於相同書頁上的紙張，綠布新封面在下方；逆向滑動沿同一進度倒播，無額外動畫計時器。第二次打開綠布前恢復該頁真正的多雷插圖。受保護的城門和印刷刊頭 SVG 均不改。

**不再有「經上所指」過渡頁。** `p2-emmaus-prologue` 的插入函數及其內嵌 CSS/文字完全刪除；一旦右封面翻至 ONE，直接進入綠布書頁→多雷插圖→ONE 經文與 66 卷，原 `03→04` 功能不改。縮短第一翻、第二翻及研讀頁進場前的無效停留，保持父頁 scroll-scrub 與反向回捲。

**工程檢查與限制：** 改動限 Draft PR #1381 的 `static/css/p2-vol00-poster.css`、`static/css/p2-emmaus-theme-verse.css`、`static/js/p2-emmaus-olive-preview.js` 及 preview 引用、`tests/p2-vol00-campaign-posters.cjs`。檢查桌面與手機角標無壓印、最後一組目錄實際到頁下部、逐章可讀、02→03→02 經文不可跨封面、完整背面和無文字空頁；**程式/CI 合格不等於藝術完成**，需要真實 Cloudflare Chromium 截圖再作藝術驗收。封面、教會、ONE 正文資料與主站不合併不重寫。


### 2026-11-04 / MERSI 式 Contents→ONE 版面交接＋七色縮小刊名；封面經文極細（最新指令）

**使用者真實截圖（06:54）反證：** 03 經文頁與 02 Contents 同時半透明，會把兩套正文重疊在同一版心；這不是「雜誌化」，也不是 MERSI 的滾動印版動效。**本節覆蓋上節的封面經文採標準 400 的舊規格**。以馬忤斯**綠布封面**的路加福音 24:27 全句按使用者最新指定改為**極細 Chiron Air / `--ws-weight-zh-air:200`**，末尾 `ws-editorial-no-orphan-tail` 仍精確繼承。中文出處維持 200，英文出處保持 Bodoni Moda true italic 400；這是**封面詩句特殊字重**，不影響 ONE 聖經逐節正文的標準閱讀字重，也不把 Luke 24:27 放到 02 藍金城門封面。

**真正的 MERSI 動效參考：** [FLOT NOIR / Codrops — Between Print and Digital: The Making of MERSI’s Website](https://tympanus.net/codrops/2026/07/27/between-print-and-digital-the-making-of-mersis-website/)。該案例同步控制兩欄內容，`clip-path: inset(...)` 從相反方向展示，不用互相疊加的 opacity。研究與實作應借「**相同一個滾動進度；成對的幾何遮罩；文字不透明；可回捲**」機制，無需導入其 Webflow／GSAP／Taxi 技術棧。實作位置是連續 P2 02→03 舊 Contents 左頁 `sourceTile` 與真正 ONE `emLeft`：`oneDrop` 進度內，目錄從右向左被遮罩退出（`inset(0, p×100%,0,0)`），ONE 經文頁從書脊即左頁的右側向左揭示（`inset(0,0,0,(1−p)×100%)`）；兩頁均保持**完全不透明**、實際同一矩形，沒有兩套可讀的文字重疊。原地恢復 source Contents 的 clip／pointer state，回滾必須完全倒帶；不加自動 timer，不讓過場更動右頁多雷插圖或頁面骨架。

**Contents 左上縮小「西望」七色：** A 的原 SVG 雙字路徑仍是唯一字形母本；海報停在午夜藍底／黎明金燙金大字之後（`p≤.941` 不改），縮至 Contents 左上小型刊名後，僅**小刊名**用現有七個 OS 色彩 `--ws-water / first-light / pale-gold / olive / harvest / crimson / daylight-mauve` 隨既有 02 頁內 `p .944–1` 正反捲動逐次過版。入色時靜態 gold foil opacity 隨之退掉，否則金箔會蓋住七色；背景紙、右側 5:8 官方封面、Contents 四個篇章與全文閱讀入口完全不變。它不是自動閃燈、不可使用 CSS keyframes 或自己的 wheel/RAF。小字被 ONE 新頁遮罩替換後不應在其他版塊憑空出現新圖。

**owner：** `static/js/p2-emmaus-olive-preview.js` 管理對向遮罩（替換此前 `emLeft.style.opacity=oneDrop`）；`static/js/p2-vol00-poster.js` 只對小刊名輸出七色 `--xw-ink` / `data-poster-corner-palette`；`static/css/p2-emmaus-theme-verse.css` 在**封面 quote 限定 selector**採 200，不動 ONE 內頁經文；`tests/p2-vol00-campaign-posters.cjs` 檢查七色可回捲、MERSI 相向遮罩及封面字重。以上維持 P2 Draft PR #1381，不合併主站。

**未經完整驗收不得宣稱定稿：** Chromium 實際連續滾輪關鍵幀（Contents 100%、遮罩 25/50/75%、ONE 100%、逆回 Contents）、手機寬度及增大字級、左右書脊 1px 分界、七色彩墨能否被清楚辨識均須視覺檢查。工具/CI/光學通過和獲獎標準是不同的 gate。


### 2026-11-04 / 緊急校正：大「西望」海報動效，不是縮小角標

**用戶最新糾正：**「不是縮小的動效有問題，是大西望動效出現了嚴重的問題。」診斷顯示 02 的父頁 `static/experiments/p2-double-square-video-lab.html` 雖已移除彩色七片遮幕，卻仍對 A 版用舊 `fold=ease((progress-.755)/.105)` 同時重算 `contentsW`、`contentsX`、`contentsH` 和右封面位置；又對整個 A 左頁使用 `gold.style.clipPath='inset(...)'`。結果是在七種印版墨色變化途中整張巨字海報發生尺寸/位置變形並被二次裁切，**不是原本批准的「同一張海報僅隨滾動更換字色與背景」**。這一診斷有確切程式路徑，目視的具體失常程度仍應由新截圖驗證。

**永久約束：** A 巨字於 `p 0–.88` 必須站在穩定的 1:1 左頁正方形；右 5:8 官方封面保留固定相對邊距；七種配色只更改同一 approved A glyph mask 和紙底，絕不挪動、扭曲、重算縮放字骨，也絕不套用舊七片版心變形/整頁 clip curtain。原 `fold` 在 02 A 路線永遠等於 1，其餘 legacy/B 路線可繼續保留舊引擎以便對照。**縮小到 Contents 角標**仍由獨立的 `p .88–.95` 動作完成，不得提前觸發。全對開縮小只在 Contents 完成之後的 `p .97–1` 發生。

**縮小之後的霓虹慢變色，是另一個不同的功能：** 舊方案把七色擠進 `p .944–1` 最後 5.6% 的輪控區間，快速滑鼠滑動會看起來像閃爍。新方案在小刊名**完全落定**後才啟動約 **32 秒／一輪** 的七色平滑變化，單色過渡約 4 秒，僅使用 OS 真正的七色 token 與輕微固定邊緣光，不做瞬間亮滅，也不讓字形位置動。使用者向上滾回大海報時，微型霓虹立即停用，完整尺寸 A 仍只接受原來的可逆 scroll progress；`prefers-reduced-motion` 下禁用色彩循環並停在金色。這一特例**不得**重新導入大海報的自動播放或破壞其七色+背景滑鼠控制邏輯。

**回歸測試**必須比較七個色站與金箔定格的左方形 `getBoundingClientRect()` 寬、高、座標及 `clipPath='none'`，不能只比較七種顏色的數值。還要驗證巨字從來沒有 `animation`，縮小到 Contents 前無另一套計時器；小角標完成後才有約 32 秒動畫，反向滑動恢復無動畫。保留 P2 Draft #1381，未有新 Chromium 視覺證據之前不能稱藝術驗收通過。


### 2026-11-04 / Contents「西望」刊名字形的專業版心註冊：最新視覺覆核

**新版真實截圖（07:56）觀察：** 左側獲批准的「西望」兩字可見墨色範圍約 `x=76–395, y=19–462`（在使用者提供的 2048×558 頁首截取圖中）；右側 `WESTSIDE WATCH / INDEX` 約在 `y=85`，主標 `Contents.` 的主要字形約在 `y=255–363`。問題不只是左邊距：刊名幾乎觸及頁頂，缺少與右側眉題及 Contents 主標的節奏關聯；刊名視覺重量過大，下方即將進入目錄的橫線也需要呼吸距離。這是 **optical registration** 的問題，不能僅以 SVG 外層盒子 bounding rect 冒充實際字骨的可視筆畫。

**最終本輪修正（取代舊 2.2% inset / 0.23 scale 規格）：** 全幅 A 巨字仍保留原路徑、位置、七種紙/墨配色和午夜藍＋黎明金燙金定格。只在 `p .88–.95` Contents 進場，讓「西望」兩條原生 SVG 墨版以相同的 scroll-linked `contents` 進度從 `scale(1)` 過渡至 **`scale(.21)`**；同時將整個印版的 **水平 inset 從 0 → 6.4%**、**垂直下降從 0 → 3%**（百分比均相對於左頁正方形，而非字形筆畫自身的 bbox）。此組光學座標依據截圖估計讓成品可見墨色約從左緣 5.8–8% 的版心起筆；上端與 `WESTSIDE WATCH / INDEX` 的眉題接近同一水平，而字形下端在四章索引首條金線前仍有白。這是可視校正的**初始工程值**，要在雲端真實截圖覆核才能正式確定。

**版面層級依 The Paris Review 書冊式索引案例：** `西望` 是 editorial signature（比正文有權重，但不能取代 Contents 主標）；`Contents.` 用 OS Bodoni Moda 保持英文主標地位；`WESTSIDE WATCH / INDEX` 與 `VOL.00` 為一條上層細字資訊帶；`目錄` 與 `FOUR MOVEMENTS / TWELVE DESKS` 位於次級基線。把刊名下移並略縮小後，左側上下字結構與右方標題兩層節奏對位，保留具有意義的白，不以額外裝飾線填空。右側正式 5:8 官方封面與其左右撐滿的 `WESTSIDE WATCH` 刊頭不變。

**實作與限制：** `static/js/p2-vol00-poster.js` 僅新增 `--xw-mark-drop` 並修改角標註冊值；`static/css/p2-vol00-poster.css` 對主墨和箔層共同使用 `translate(var(--xw-mark-inset),var(--xw-mark-drop)) scale(var(--xw-mark-scale))`，確保不出現兩張重影。完整大海報 `p≤.88` 的 inset/drop 必須為 0，七色 scroll wheel 原樣；完成的 Contents 小刊名仍約 32 秒一輪七色柔和霓虹慢變（reduced-motion 停用）。頁面底紙、四章十二欄文案、字級、ONE 與右側封面不受此調整影響。Regression 應檢查 `p=.85,.90,.95,1,.53` 的位置、縮放、倒帶與大海報位移為零；桌面 1648 與手機 390 確認不壓刊期、不撞目錄導覽線。仍在 Draft PR #1381，未合併主站，不能以靜態代碼檢查宣稱獲獎級視覺驗收已完成。
