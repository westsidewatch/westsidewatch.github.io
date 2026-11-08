# Westside Watch — Scripture Editorial Design System / 經文編輯視覺系統

**Status:** Design direction / proposal, not deployed, not a universal CSS override.  
**Date:** 2026-11-08  
**Source of direction:** User-supplied Isaiah 55:9 visual reference and V82 Olive Mountain bilingual scripture editorial design.  
**Scope:** All Westside Watch scripture presentation; no change to canonical information architecture or existing animation.

## 0. Brand decision — ONE signature, every non-body scripture instance

**2026-11-08 user direction supersedes the previous proposal for four independent design modes.** All Scripture appearing outside ordinary body reading must immediately read as **Westside Watch**, whether cover, journal masthead, section head, subsection, speaker-side excerpt, pull quote, exceptional callout or scroll narrative. The signature is a single compositional family, not a menu of different styles.

**Working name: WATCHWORD / 守望經文銘式.** This is an internal design name, *not* an extra public label printed on all verses.

**Five invariant identity anchors:**
1. Visually dominant Chinese scripture phrase in the OS Chinese display family.
2. Deliberate KJV English typographic counter-rhythm in Bodoni Moda (real italics permitted).
3. Separate top-right italic English Bible citation paired with a legible Chinese book/chapter citation.
4. The **Watch Gate / 守望門線** open L-shaped hairline: vertical left rule + horizontal base, plus precisely seven progressively rising tiny engraved ticks; this geometry is the distinct stable brand sign. Do not put a full frame around Scripture.
5. Fixed relationship of asymmetrical breathing space, main verse, English verse, source, the seven-tick mark and translation information.

**Responsive scaling, not format fragmentation:** The five components remain recognizable on covers, 1648px section spreads, 390/320px mobile, narrow folios and scroll chapters. Layout can stack; type-size may scale with existing OS tokens; color adapts to each approved branch; reading order remains Chinese -> KJV -> labels, with reference visually separate. Never put brand identification solely in color.

**Scope exception:** Continuous Bible text in ONE/other actual reading body remains untouched; ordinary verse numbers and inline citations do not become Watchword. Any Scripture intentionally pulled out of the body and designed as heading, quotation, featured verse or scroll statement uses Watchword.

**Visual proof (isolated, not live):** `experiments/watchword-signature-v1.html`. It demonstrates five scales from the same mother composition: cover, Olive section header, editorial pull quote, small folio and scroll. This is a test of the structural grammar, **not yet approved or browser-verified final artwork**. Text remains native HTML, with CSS linework; maintain the authorized palettes and typography. Specific line weight, spacing, seven-tick rhythm and bilingual typographic balance must pass artistic review before implementation on production sections.

**Technical decision:** Establish reusable semantic class contracts (`.watchword`, `.watchword__citation`, `.watchword__frame`, `.watchword__zh`, `.watchword__en`, `.watchword__mark`, `.watchword__translation`) from this single proof only after visual approval. Do not deploy a blanket selector or interfere with ordinary paragraphs and Bible reader.

## 1. Thesis / 主張

Scripture is editorial content, not utility text, a caption or generic quote card. Give it a distinct typographic and compositional language that preserves readability, verifiable text and the identity of each site section.

Reference strengths: unusually generous asymmetric negative space; text rather than illustration as the composition; expressive italic scripture reference contrasted with emphatic verse; restrained fine gold rules; low-contrast paper grain. **Translate these relationships, not the reference's exact colors, fonts, wording, or layout.**

## 2. Non-negotiable OS alignment

- Consume existing `static/css/westside-design-os.css` scripture reference and editorial type roles, and `static/css/westside-color-authority.css` semantic color roles. Do not create local raw HEX palettes.
- Respect `docs/WESTSIDE-COLOR-AUTHORITY.md`: Identity × Material × Light; Silence 70–90%, Voice 10–25%, Event ≤5%; do not introduce dark+gold dominant treatments.
- English: Bodoni Moda for editorial heading/reference, with a true italic. Chinese display: Chiron Hei HK WS; long-form scripture reading may use Noto Serif TC. Distinguish display, citation and reading text; avoid synthetic italics/forced scaling.
- Chinese Scripture and English KJV must be accurately transcribed, with source/translation labels; abbreviated excerpts must be explicit. No generated or paraphrased verse presented as a quotation.
- Preserve reading order and semantics: `figure` / `blockquote` / `figcaption` / `cite` or appropriate editorial HTML. Copyable, selectable text, not text baked into SVG.
- On small screens, stack language blocks without microscopic citations, broken single words or image-overlay collisions. Respect reduced motion.

## 3. Historical exploration — four use cases now unified under ONE Watchword signature

### A. Scripture Monument / 經文碑銘
Use for hero / section theme verses; 1–4 lines. Verse itself is dominant display typography, source sits separately in italic reference, meaningful asymmetric breathing room and a deliberate rule. **Do not automatically uppercase Chinese; avoid mass uppercase English in long passages.**

### B. Bilingual Editorial Spread / 雙語對開
Use for Olive Mountain speaker-side quotations and section mastheads. Chinese and KJV are equally available, but hierarchy responds to context: Chinese primary reading / English literary counterpoint, or opposite when appropriate; never bury Chinese as a tiny caption. Citation follows each version or clearly shared pairing.

### C. Engraved Margin / 刻線邊註
Use for ONE / Emmaus and long-reading pages. Compact marginal scripture with a narrow vertical or horizontal engraved rule; verse numbers and book/chapter remain legible; scripture block does not compete with navigation or obscure Doré illustration.

### D. Meditative Interlude / 默想留白
Use for Selah, prayer, transitions and appropriate cinema treatments. Sparse verse excerpt plus a refined citation; motion reveals words or illumination only if explicitly designed, and never impairs a reader's ability to pause/scroll/reverse.

## 4. Surface adaptation (preserve existing section's artwork)

| Surface | Editorial treatment |
| --- | --- |
| Church / 活水堂 | Sacred scripture inset: water/Temple Stone material with readable light surface; no large black+gold field |
| Journal / 西望 | Magazine-grade scripture folio; typography and measured whitespace before decorative engraving |
| Emmaus / ONE | Papyrus and thin engraved rules; true biblical reading/navigation remains primary |
| Olive Mountain / 橄欖山 | Speaker-adjacent CN/KJV excerpt as established in V82; botanical/hillside engraving belongs to section, not pasted behind text |
| Dawn Library / 黎明書局 | Book-plate or marginal scripture, restrained harvest identity, source/translation as metadata |
| Cinema / 電影院 | Caption-like scripture typographic treatment, legible over film/curtain; no disruptive animation |
| Daylight Café / 白晝咖啡館 | Small meditative passage with botanical/harvest relationship, avoiding crowded decorative flourishes |

## 5. Design acceptance criteria

1. A verse has a demonstrable main reading anchor and a clear separate citation, **not simply two equal-weight paragraphs**.
2. Citations are legible and accurately linked to the text; bilingual translation labels are present.
3. The typographic block follows deliberate line breaks without orphan words, accidental single-character Chinese lines, text clipping or overflow.
4. Verse, margins, fine rules and engraved material make a unified composition, not a floating generic card.
5. Color consumes existing branch tokens; section-specific identity is not overwritten by this reference image's green/gold.
6. At 1648, 768, 390 and 320px, verify actual browser screenshots, bounding boxes and contrast. Keyboard/selection/reduced-motion cases are included.
7. Existing section layouts, scroll timing, original imagery and motion are preserved unless explicitly approved for change.
8. No claim of visual acceptance based solely on CI/build passing.

## 6. Engineering rollout

**Phase 0 — this document:** Establish design authority and reference; no live code changes.  
**Phase 1 — isolated proof:** Validate the one Watchword identity at five scale/use cases in `experiments/watchword-signature-v1.html`, with Chinese+KJV, responsive proof and browser screenshots. Do not bake scripture words into images or SVG.  
**Phase 2 — integration:** Adapt existing reusable scripture components, preserving owning CSS and current section geometry. Pilot on the already-draft Olive Mountain and Emmaus before widening to all surfaces.  
**Phase 3 — validation:** Compare canonical screenshots before/after, visually inspect every breakpoint and scroll/reverse state. Any release to main remains a separate decision.

## 7. Reference caution

The Isaiah 55:9 image is a **design reference**, not an approved site asset to copy. Its all-caps block, orange-gold color, line breaks, exact typefaces and text treatment are not automatically OS-compliant. Preserve the hierarchy and rhythm while using the site's existing type/color authority.
