# New Westside Motion System / 新西望動畫系統

Status: ACTIVE
Established: 2026-08-31
Scope: Permanent Website + Living Wall + Journal transitions

## Purpose
動畫不是裝飾層，而是把新西望已確立的「磚・垛・流」從靜態版面變成真正活的 editorial system。動態必須回答：內容如何進場、如何取得重量、如何讓位、如何沉降、如何重新見光。

## External references to study, not copy

### Motion.dev — primary motion engine candidate
Use for layout transitions, shared-layout transitions, scroll-linked/scroll-triggered states, SVG/path drawing, gesture response and reduced-motion handling. Its layout animation model directly對應華容道：DOM/editorial state先改，Motion負責把舊位置到新位置的位移連續化。

### Kokonut UI — component-motion reference library
Use as a source of bounded interaction patterns and source-owned React/Motion components. Study particle/button/path/background techniques only where they can be retokenized into Westside. Do not import its demo aesthetic or SaaS component language.

### Anime.js — secondary sequencing candidate
Reserve for deterministic timelines, SVG/DOM sequencing or non-React contexts when Motion is not the best fit. Do not add merely for novelty.

### Canvas/WebGL/particle systems — exceptional layer
Only for rare atmospheric scenes where DOM/SVG cannot express the idea efficiently. Never become the permanent background or default interaction language.

## Westside motion grammar

### 01 / DAWN — 光發生
Motion meaning: revelation / arrival, not glow decoration.
- fine gold trace draws or catches light;
- image/engraving can emerge from darkness/paper density;
- preferred duration 700–1400ms for major scene, 180–360ms micro state;
- opacity alone is insufficient: combine crop, trace, local contrast or restrained translation.

### 02 / BRICK ENTERS — 磚進場
A new editorial object enters with weight already assigned.
- no generic fade-up card cascade;
- entry origin follows reading/time direction;
- scale change restrained; no bouncy app-card motion;
- 5:8 hero should feel like territory being opened, not a modal popping up.

### 03 / HUARONG DISPLACEMENT — 華容道讓位
Core Living Wall motion.
- editorial state changes first;
- neighboring bricks move/resize to make room;
- preserve spatial continuity so the reader understands what moved where;
- Motion layout/layoutId is primary implementation candidate;
- transitions interruptible when new information arrives;
- no random masonry reshuffle.

### 04 / CRENELLATION BREATH — 垛口呼吸
Negative space is part of architecture.
- gaps may open/close as editorial weights change;
- skyline changes slowly and quietly;
- no perpetual floating/bobbing;
- motion should make the wall feel inhabited, not unstable.

### 05 / TIME SETTLES — 時間沉降
Older material does not simply disappear.
- move toward lower editorial gravity;
- reduce image dominance/density before reducing legibility;
- archive transition may compress/crop/reposition;
- temporal demotion should remain traceable.

### 06 / DORÉ TRACE — 刻線生成
Doré engraving motion is line/process based.
- SVG path drawing, mask reveal, crop reveal, local ink-density change;
- Trace / Presence / Image / Immersive levels inherit the static engraving system;
- avoid turning engraving into neon-outline animation;
- First Light Gold may catch selected engraved edges, never recolor the whole engraving gold.

### 07 / JOURNAL THRESHOLD — 期刊進入
Website → Journal is a threshold, not an unrelated page load.
- current issue territory can expand toward the Journal cover/surface;
- masthead and issue identity retain continuity;
- Journal then follows its own art direction;
- returning to Website restores the permanent Living Wall state.

### 08 / THE GATE — 門
The Gate is singular and architectural.
- opening/reveal can use clip/path/door-like spatial transition;
- no literal 3D castle door required;
- motion should communicate passage from editorial/publication space toward Living Water West / Join.

## Motion intensity

0 / Still — reading body, long scripture, accessibility/reduced motion.
1 / Trace — 1px line, ink density, tiny positional response.
2 / Presence — ordinary hover, reveal, metadata transition.
3 / Structural — Living Wall displacement, issue expansion, Gate transition.
4 / Immersive — rare cover/feature moment only; never default homepage state.

## Anti-patterns
- generic fade-up every section;
- parallax everywhere;
- infinite floating cards;
- particle effects without semantic purpose;
- spring/bounce as default personality;
- WebGL just to look expensive;
- autoplay movement competing with reading;
- motion that destroys the wall's editorial hierarchy;
- different animation language for every component.

## Implementation priority
1. Native CSS for micro transitions and reduced-motion fallback.
2. Motion.dev for React layout, scroll, gesture, shared-element and SVG motion.
3. Anime.js only where timeline/SVG sequencing is materially simpler.
4. Canvas/WebGL only after a specific visual requirement proves DOM/SVG insufficient.

## Required reference specimens
MOTION-01 Dawn Trace
MOTION-02 5:8 Territory Opens
MOTION-03 Huarong A→B displacement
MOTION-04 Editorial promotion/demotion
MOTION-05 Crenellation gap opens/closes
MOTION-06 Doré engraving trace→presence→image
MOTION-07 Website→Journal threshold
MOTION-08 Gate passage
MOTION-09 Time settling / archive
MOTION-10 reduced-motion equivalents

## Acceptance
A motion pattern enters New Westside only if it improves at least one of: hierarchy comprehension, spatial continuity, time comprehension, material/engraving expression, navigation orientation. If it only adds spectacle, reject it.
