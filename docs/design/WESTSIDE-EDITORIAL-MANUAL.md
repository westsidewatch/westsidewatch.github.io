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

**Integration verified 2026-10-17:** The OS runtime already defines Bodoni Moda, genuine Bodoni Moda SC, Chiron Hei HK WS, Noto Serif TC, Chinese 200/400/600 weights and responsive `--ws-type-scale-*` semantics. Hence the old typography document's `typography-sitewide.css` authority statement is **superseded** by the OS umbrella and compatibility-runtime contract. It is not grounds to migrate or change working entry points.

**Entrypoint rules.** Hugo templates load OS through `layouts/_default/baseof.html`; standalone P2 loads `/css/westside-design-os.css` followed by its own `/css/p2-living-water.css`. Other standalone HTML is guarded by `scripts/check_design_os_entrypoints.py`: the OS stylesheet and `body[data-ws-scope]` must both exist. A manual consolidation **must not touch those references, their sequence, or any HTML/CSS/JS**.

## 2. Editorial hierarchy and real reading

Typography is architecture for reading, not decorative text. Decide the reader's sequence before choosing font sizes.

1. **Identity:** ecclesial/realm name, issue or section identity; usually one visual anchor.
2. **Primary heading:** one clear top-level editorial proposition.
3. **Section headings:** lower scale/weight than the primary title unless an explicit art-directed composition justifies parity.
4. **Body/metadata:** sufficiently legible at the actual viewport; time, author, source and captions must remain discoverable.
5. **Citation/folio:** distinct semantic typography and stable positioning; never compete with the content.

Select from the OS semantic scale; surface owners may bind scope-specific roles. Do not make a new `--root` type system and do not stretch fonts. Chinese 200 is for airy, sufficiently large editorial display; not tiny administrative descriptions. Chinese anchor 600 is for short structural titles, not whole paragraphs. English Roman/Italic Bodoni and real Small Caps retain distinct semantic roles.

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
| Fixed realm | `EMMAUS` + `以馬忤斯` | Bodoni 72–100px; Chinese Chiron 600 18–24px | Permanent dominant realm signature; no override by study state |
| Active Bible book | `JOHN` / `約翰福音` | Bodoni 40–56px; Chinese Chiron 600 26–34px | Actual book name (not just 43); second anchor |
| Active chapter | `03` + `第三章` | Bodoni 48–70px; Chinese Chiron 600 24–30px | Visible adjacent to book; canonical chapter index |
| Chapter subject | Actual ONE chapter title | Chiron 600 22–30px | Third-level feature heading, never tiny metadata |
| Study body | Scripture / book background / chapter content | Noto Serif TC 400, ~14–17px readable at actual folio | Main reading space and stable measure; preserve source text |
| Tools / notes / folio | Tabs, provenance, gold scripture, atlas captions | Chiron 400 for controls, 200 for meaningful micro-labels, subject to legibility | Quiet subordinate material; no row of miniature rectangular CTAs |

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
