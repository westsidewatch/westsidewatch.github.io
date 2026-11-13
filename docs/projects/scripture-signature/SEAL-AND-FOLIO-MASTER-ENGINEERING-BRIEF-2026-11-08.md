# Westside Watch — Scripture Seal × Scripture Folio

> **IMPORTANT — SUPERSEDED PLACEMENT POLICY (2026-11-08, later decision):** The latest user direction requires a theme-scripture **Seal at the entrance to each of the seven first-layer realms**, where the impression marks the transition rhythm. This replaces this document's earlier selective/conditional placement recommendations. Retain the older matrix only as historical exploration. The **current authority** is [Seven-realm Scripture Seal transition decision](SEVEN-REALM-SCRIPTURE-SEAL-TRANSITION-DECISION-2026-11-08.md). The everyday Folio remains a separate derived system. No implementation/live approval is implied.

## 經文戳記動效母本與全站通用經文系統｜正式工程方案

**Decision date:** 2026-11-08  
**Status:** Design / engineering specification, approved direction; no new runtime implementation in this commit  
**Authority:** User direction, Westside Design OS, Color Authority, canonical site architecture  
**Implementation location:** separate isolated prototype, then Draft P2 review; no automatic production merge

## 0. Design decision

Design one **kinetic bilingual typography artwork** first, then extract only its proven recognizable design DNA for a family of applications. There are exactly **two usage implementations**, not four independent styles:

- **A. Scripture Seal / 經文戳記:** a square or almost-square, signature-grade composition. Interwoven vertical Traditional Chinese and horizontal English KJV, materially evocative of letterpress type formes, seals, blocks, or impressing type. Suitable for homepage focus scripture, hero, covers, key scroll moments and major chapter transitions. This is a memorable *artwork*, not a default quote container.
- **B. Scripture Folio / 通用經文版式:** the adaptable design family derived *after* Seal's approved master frame. For section headings, small headings, pull quotes, speaker-side passages, marginal annotations, cards and special highlights. The logo-like square can disappear in Folio while the optical DNA persists.

**Non-negotiable objective:** A reader who sees a non-body scripture component without its Westside Watch label should still recognize the typographic system as Westside Watch. Do not print literal “THE WORD / 經文” or other redundant interface identifiers. Avoid simply putting bilingual verses inside a framed card.

## 1. Origin and precedent

The most promising research route is **07 — Chinese/Western letterpress crossed axes**, based on the studied metal type / `Dream Pool of Gutenberg` direction. Integrate the site's existing square/block design language, not a borrowed stamp logo. Other research informs the solution only where useful: 02 shared glyph structure, 10 coordinated type DNA, 12 strong scale contrast.

Earlier Watchword V1 (L frame + seven decorative ticks) and V2 (stacked large Chinese + English italic + a line) were insufficiently distinctive. Retain these as comparative rejected/exploratory baselines; do not present them as finished designs or freeze their ornamental details as the brand.

**Meaning of "stamp":** density, registration, pressure, cut paper, deliberate typesetting and resulting impression—not a distressed fake ink texture, faux antique red seal or generic box icon.

## 2. Seal master: spatial grammar

Square base composition with an optical grid, explored at 1:1 and selected near-square ratios—not necessarily a rigid border.

1. **Chinese vertical spine:** one to three intentional vertical columns in Traditional Chinese, with meaningful semantic line breaks. Chiron Hei HK WS / approved Chinese OS display font or a documented *licensed* supplementary display cut. Use true vertical layout where the chosen browser/font supports it; do not rotate glyphs as a shortcut.
2. **English horizontal counter-axis:** KJV, using the OS Latin Bodoni Moda family, crossing **negative spaces / registers**, not obscuring the Chinese text. Optical weights can vary; italic only when it earns compositional meaning.
3. **Citation register:** chapter and verse as active compositional parts (e.g. separate vertical and horizontal alignments) and complete bilingual book/chapter citations visible without guessing. Do not invent variant Bible references.
4. **Typographic impression:** the square emerges from the alignments of strokes and margins; outer perimeter rule is not mandatory. Prefer the actual composed type as the shape.
5. **Positive-negative rhythm:** one dense axis, another open axis; large type, fine annotation and deliberate open corners. The large shapes cannot all compete.
6. **OS chromatic identity:** use only authorized color tokens and material/lighting roles. Ink- and paper-based editorial appearance should remain recognizably this brand in monochrome; avoid dark/gold dominant theme.

A signature may use a **registration notch, interruption or typographic crosspoint** if it is organically derived from the chosen lettering. Do not automatically add seven stripes or ornamental crosses.

## 3. Kinetic master — three acts

### Act I — The setting of type / 排字

The square working field becomes legible through a physically credible typographic arrangement: Chinese vertical characters register in their columns; the English horizontal measure moves into its own slots. A controlled sequence of discrete placements/pressures, not arbitrary drifting tiles, blind opacity fades, flashy explosions or spins. Staging should make the two writing directions intelligible.

### Act II — The impression / 落印

Bilingual axes align and settle into the **hero master frame**. A subtle compress-and-release of the optical grid and/or an engraved registration line may suggest printing; no excessive bounce. The strongest image is the stable completed composition, not the transition effect. Pause/hold must allow complete reading in both languages.

### Act III — The extraction / 萃取

Separate four or five *already-present* optical relationships, then show their transfer to a horizontal chapter masthead, editorial quotation, compact folio, and scroll interlude. **No new decorative symbols invented at extraction time.** The viewer should recognize continuity between Seal and Folio without requiring the entire square.

### Scroll/motion engineering requirements

- One scroll-position-driven controller when integrated into P2; scrub forward and reverse to identical visual states. No conflicting independent timeline or changed existing 01–03/04 transitions.
- Provide a standalone play/pause/scrub prototype for art review before connecting to P2.
- No invisible text as the only accessible passage: both translation texts remain real selectable HTML and are available in static/reduced-motion form.
- Honor `prefers-reduced-motion`, keyboard focus, reasonable frame pacing and responsive overflow.
- Permanent stable end-frame for offline printing, cover export, and non-animated contexts.

## 4. DNA extraction contract (not finalized before art approval)

| Invariant category | Seal source | Folio inheritance | Allowed variation |
|---|---|---|---|
| Typeface pairing | OS Chinese display × Bodoni Moda KJV | Same verified families and optical corrections | Approved cuts/weights for scale |
| Bilingual relationship | Vertical Chinese × horizontal Latin intersection | A related but readable multi-axis hierarchy | Stacking on narrow viewports |
| Grid and register | Square optical type register | Register coordinates, relative offsets, alignment rhythm | Aspect ratio and width |
| Hierarchy | Single dominant textual mass, fine annotation | Dominant verse + subordinate but meaningful countervoice | Scale/length |
| Citation | Bilingual source integrated in type arrangement | Stable bilingual citation grammar | Physical position |
| Material/color | OS semantic role tokens | Section branch identity with shared text/line roles | Chapter-specific field |
| Motion | Type-set → impression → stable → extraction | Light reveal / registration derived from Seal | Can be static |
| Prohibitions | No generic box or ornamental tick motif | No duplicated label, unreadable overlay, decorative clutter | None |

**Freeze only after side-by-side review:** font sizes, line heights, spacing, column count, margins, citation lettering and crosspoint proportions will be measured from the approved Seal, not assigned by arbitrary V1/V2 values.

## 5. Application matrix

| Use | Mode | Interpretation |
|---|---|---|
| Home featured Scripture | Seal | Full square, complete type-setting and impression |
| Homepage key transition | Seal | Scrubbable assembly + stable hold |
| Journal magazine cover | Seal or Seal-derived hero | Signature master composition without generic quote frame |
| P2 Olive Mountain section head | Folio | Preserve title/portrait clearance; unmistakable inherited typography |
| Speaker-adjacent quotes | Folio | Native CUV+KJV; maintain separation from flipping reverse card |
| Emmaus / ONE section theme | Folio | No interference with genuine Bible reading controls |
| Small headings / marginal notes | Folio | Compact, legible, no literal square requirement |
| Pull quotes / special emphasis | Folio | More expressive scale while preserving citation grammar |
| Cinema and scroll interludes | Folio or rare Seal | Reversible reveal, reading pause, no contrast loss |
| Ordinary Bible body text | **Neither** | Existing Bible reader and verse semantics unchanged |

## 6. First proof assignment

Use **Romans 10:17 / 羅馬書 10:17** as the initial fixed bilingual sample for direct comparison with the existing Olive P2 chapter; text must be checked against the authorized Chinese CUV and English KJV before art approval. For a design test requiring stronger spatial contrast, use Isaiah 55:9 only in a *separately labelled, text-verified* comparative test, not as a replacement for the chapter's established verse.

Deliverables:
1. **One finished square Seal** at 1:1, wide and mobile responsive, as native text + CSS and SVG *ornament only*, plus a static full-resolution stable frame.
2. **One actual scrubbable animated type-setting sequence** with Acts I–III, reversible, reduced-motion equivalent and non-animation still.
3. **Four Folio derivations** cut from the same master: section masthead, speaker-side quote, compact citation and scroll statement.
4. **DNA sheet:** the optical ratios, type choices, line-breaking rules, citation grammar, grid, tokens and motion timings exported as implementable component rules.
5. **Comparison board:** original Isaiah reference (for conceptual assessment only), V1, V2, Seal, four Folios at identical scale where relevant.
6. **Visual acceptance captures:** 1648 / 768 / 390 / 320px, including 04 scroll stages forward/backward.

## 7. Quality gate / award-direction rubric

- **Identity without logo:** Seal must be recognizable without brand name; Folio unmistakably retains design relationships from Seal.
- **Bilingual originality:** Removing one language must break the intended design; neither language is a tiny afterthought.
- **Reading:** Chinese and English can each be read accurately with correct Bible citations and excerpt notices where needed.
- **Composition:** Type mass/negative space/counter-axis have optical necessity. No labels, hairlines, seven marks or textures used merely to fill blank spots.
- **Movement:** Type-setting causally makes sense; full completed print image holds; reverse scroll restores states exactly.
- **Technical discipline:** Native selectable text, OS palette, accessible contrast, tested 320px, no extra horizontal scrolling, no conflicts with existing P2 compositor.
- **Independent art review:** CI pass alone is not acceptance; actual screenshot and motion review are required.
- **No premature rollout:** Do not touch homepage, main site or released P2 until approved in isolated Draft.

## 8. Engineering boundaries and ownership

The canonical Design OS remains authoritative: `static/css/westside-design-os.css`, `static/css/westside-color-authority.css`, `docs/WESTSIDE-COLOR-AUTHORITY.md`, `docs/DESIGN-OS-GEOMETRY.md`, and `docs/MASTER_SITE_ARCHITECTURE.md`. This brief is a daughter design rule, not permission to change architecture or rewrite existing animation.

Work should begin with the isolated Seal prototype; **do not overwrite** `static/experiments/p2-0104-olive-continuation.html`, its scroll controller, protected original posters, or already verified V82 without visual approval. Integration into Olive P2 should initially be an opt-in Draft proof or separate preview branch.

## 9. Current status

- Research of twelve distinct bilingual composition routes: completed as research direction.
- Agreement on two output implementations and three-act animated artwork: completed.
- Formal engineering brief: this file.
- Square artwork: **not yet produced**.
- Working kinetics and Folio derivations: **not yet implemented**.
- Browser art acceptance / launch: **not complete**.
