# MASTER SITE ARCHITECTURE

> Canonical master index for Living Water Westside Watch / 西望 / 西望品牌 / 主站.
>
> This document is the single structural source of truth. Structure may only be changed by the user. Other agents, AI systems, Doré, Codex, engineering tools, and Storybook may inspect, discuss, and propose changes, but may not independently modify the site structure.

## 1. Main Site

```text
Living Water Westside Watch
＝ 西望
＝ 西望品牌
＝ 主站

├── Journal
├── 橄欖山 Mount of Olives
├── Church
└── About

全站功能
└── 多雷搜索
```

## 2. Journal

Journal is the publication / journal core. It is organized into four movements, twelve fixed columns, and three interludes.

### WATCH
- 米斯巴 Mizpah — 卷首、守望的起點。開啟一期的閱讀方向，可承載主題、核心經文、編者觀察與閱讀入口。
- 伯利恆一日 Bethlehem — 每日靈糧。A Day is its live/daily content form, not a thirteenth column and not a structural child. Daily scripture content follows verified-source rules and Toronto-date rotation; scripture text is not AI-generated or rewritten.
- The Gate 門 — 時代觀察、公共信仰思考、守望論壇。面向世界、時代與公共處境；與何烈山的啟示／認識神／敬拜邊界不同。
- 迦密 Carmel — 重大特稿、本期核心 Feature / Living Feature。是內容重量容器，可成為一期核心。

### Interlude
- Selah 細拉 — WATCH → WALK 的停頓、默想與回應。

### WALK
- 以斯帖 Esther — 歷史見證、人物專稿。歷史人物、神學家、作者、牧者、宣教士與歷代見證人。
- 亞杜蘭洞 Adullam — 當代見證、人物訪談。現今仍在服事的人物、呼召、事奉、掙扎與見證。
- 以馬忤斯 Emmaus — 同行入口、查經與共同學習工作台。「西區的夜晚」只作描述，不是正式欄目名稱。Emmaus 下承 ONE 與多寫，二者不是 Journal 同層欄目。
  - ONE — 查經前哨站；按卷、逐章敘事，不是逐節講解；提供背景、歷史、地圖、經文筆記、進度等。
  - 多寫 — 寫作／研究工作台，承載查經筆記、研究材料、寫作與成熟成果。

### Interlude
- 遠方無聲鴿 Jonath-elem-rechokim — WALK → WITNESS 的間奏；源自詩篇 56:1 的詩歌題名／調名意象。

### WITNESS
- 以琳 Elim — 神的供應、恩典與生命；根於出埃及記 15:27，可承載靈修、禱告、生命恢復與供應見證。
- 別是巴 Beersheba — 人的回應、盟約中的生命；信靠、順服、委身、記念神信實與盟約生活。
- 伯特利 Bethel — 神家中的共同生活、教會生活；團契、服事、彼此建立。
- 何烈山 Horeb — 神的啟示、認識神、因神是神而敬拜；不是單純神學知識。

### Interlude
- 基尼烈 Kinneret — WITNESS → WORSHIP 的間奏，承接見證並流向敬拜。

### WORSHIP
- 瑪拉拿 Maranatha — 閉卷禱告、盼望主再來；感恩、回應、代求、交託與等候。

## 3. News Broadcast

Cross-column function, not a thirteenth Journal column.

```text
新聞播報
├── 伯利恆一日 / A Day
├── Selah 細拉
├── 遠方無聲鴿 Jonath-elem-rechokim
└── 基尼烈 Kinneret
```

“秒報” is a rolling / instant news mechanism, not a literal every-second refresh requirement.

## 4. 橄欖山 Mount of Olives

```text
橄欖山 Mount of Olives
├── 黎明書局 / Dawn Library
├── 白晝咖啡館 / Daylight Café
├── 守望禱告會 / Watch Prayer
├── Podcast
├── Video
└── Newsletter
```

### 4.1 黎明書局 / Dawn Library

#### Positioning
Dawn Library is a digital resource and curation system with editorial judgment. It is not a website bookmark collection, URL list, search-results dump, or passive database. Its core question is: **哪些資源值得被保存、推薦、使用？**

Root principle:

> 經文在中心、工具服務經文、資源服務學習、設計服務使命。

The Library is a continuously accumulating knowledge/resource system, not a Journal issue-by-issue publication. Its resources may serve Journal, ONE, 多雷搜索、Church、Social、Visual research and other functions.

#### The three-layer editorial model

```text
Morning Star / 三晨星
        ↓
Spectrum / 光譜
        ↓
Collection / 策展集
```

These are three distinct underlying editorial logics:

- **三晨星 Morning Star —「什麼值得留下？」**
  - Not popularity, traffic, clicks, or usage ranking.
  - It is the Westside Watch editorial judgment standard for identifying resources that are genuinely valuable, trustworthy, useful, and worth long-term recommendation and preservation.
  - It is also a living output mechanism: daily recommendations can be selected under a **本週主題**, so Three Stars is not merely a static rating/index.

- **光譜 Spectrum —「這些知識彼此是什麼關係？」**
  - Spectrum was the corrected name replacing Topics.
  - It is not an ordinary tag or category. It reveals the **知識脈絡** and truth structure surrounding a question: how Scripture text, original languages, history, theology, archaeology, art, people, geography, and other resources illuminate one another.
  - Spectrum therefore builds relationships across resources and across disciplines, allowing the user to see how a body of knowledge is connected rather than merely where an item is filed.
  - It also expresses learning depth, such as **Beginner → Intermediate → Advanced → Academic**, and where appropriate other paths such as **Inspiration → Creation → Professional**.
  - **知識脈絡** is a core concept of Spectrum: the Library does not merely collect knowledge; it records, exposes, and navigates the relationships and development of knowledge around Scripture and learning questions.

- **策展集 Collection —「應該怎麼學？」**
  - Not a folder of similar URLs.
  - A Collection is an editorially designed **學習道路**: where to enter, what to read first, what follows, when original-language tools become useful, when to enter historical/background material, and what is appropriate for deeper study.
  - Collections can intentionally combine Scripture tools, books, articles, courses, historical resources, original-language tools, visual material, and other resource types when they serve one learning purpose.
  - A Collection should have a clear purpose, intended audience, learning/use order, cross-category composition where useful, and editorial guidance.

#### Knowledge context / 知識脈絡

Knowledge context is not a fourth peer layer replacing the three-layer model. It is the relational logic that Spectrum makes visible and that the whole Library gradually accumulates.

The distinction is:

```text
三晨星：判斷價值
光譜：建立／看見知識脈絡與真理結構
策展集：把知識脈絡轉化為可行走的學習道路
```

This means a resource can be understood not only by its metadata or category, but by its relationships to Scripture, other resources, historical development, concepts, people, places, disciplines, and levels of study. Over time, this accumulated knowledge context becomes one of the Library's most important forms of intellectual capital and supports ONE、 多雷搜索、Journal、字幕插件等 downstream systems.

#### Resource lifecycle

```text
Candidate Resource Pool
        ↓
Editorial Selection
        ↓
Morning Star / 三晨星
        ↓
Spectrum / 光譜／知識脈絡
        ↓
Collection / 策展集
        ↓
Resource Card
        ↓
Dawn Library collection
```

The Library must not collapse into:

```text
找到網站 → 列出網址 → 完成資源卡
```

#### Resource work phases

**Phase 1 — Resource Inventory / 資源盤點**
- collect resources
- classify
- display during inventory stage
- preserve screenshots where useful
- maintain Markdown records
- produce the Candidate Resource Pool

**Phase 2 — Editorial Curation / 編輯策展**
- editorial selection
- Three Stars judgment
- Spectrum / knowledge-context positioning
- color classification where applicable
- Resource Card creation
- Collection construction

#### Resource Master

Resource Master is the underlying single source of truth for individual online resources. Early-stage implementation may live in `data/resources.json` and be version-controlled in GitHub, with future migration to a database if needed.

Core fields include:
- Resource ID
- Resource Name
- Official URL
- Category
- Subcategory
- Language
- Resource Type
- Description
- Audio Available
- Free / Paid
- Morning Star Index
- Related Spectrum
- Related Collection

The Library should keep the public-facing structure simple while retaining richer internal intelligence. General resources should not create unnecessary front-end categories; books may require finer classification because books need stronger reading guidance.

#### Resource Card

A Resource Card is not merely a data summary. It is the presentation of a resource as a “book” in Dawn Library. It should communicate at least:
- name
- category
- positioning
- recommendation reason
- Spectrum / knowledge context
- Three Stars
- use scenario

Visual direction: vertical, generous whitespace, clear numbering/text hierarchy, classical catalogue/library-card character, aligned with the wider Westside Watch visual grammar. The standard card ratio is 5:8.

#### Living resource / content-generation system

Dawn Library is a living resource system. Resources are meant to be activated, recombined, and reused rather than merely stored.

```text
年度方向
↓
月度策展
↓
本週主題
↓
每日三晨星
↓
Journal / Social Media
```

A broader feedback loop is:

```text
資源池
↓
Weekly Theme / 本週主題
↓
Three Stars / 三晨星
↓
Curated Collection / 策展集
↓
Spectrum / 光譜／知識脈絡
↓
Journal / ONE / Social Media / other tools
↓
新的研究與內容沉澱回資源池
```

Therefore the Library is not merely a database or collection; it is a **生命系統／內容生成系統**.

#### Doré learning relationship

Dawn Library also functions as the mature public layer of Doré's long-term learning and research:

> 神學院是 Doré 的課程；黎明書局是他的筆記本、作業本和畢業成果庫。

Internally, Doré may have notebooks, coursework, research notes, and portfolio material that are not ready for public release. Only sufficiently mature, verified, and editorially selected work should become public Library material.

Thus the long-term relationship is:

```text
Doré learning / research
↓
notes / coursework / research materials
↓
maturity + verification
↓
editorial judgment
↓
public Library collection
```

The Library's intellectual quality is therefore also a visible measure of Doré's accumulated learning, synthesis, systematization, and ability to form coherent knowledge context.

#### Engineering / downstream role

Dawn Library is expected to support:
- ONE Bible study research
- global 多雷搜索
- Journal research and publication
- Church learning
- subtitle/media plugins
- visual research
- future knowledge and recommendation functions

The goal is not only to store more resources, but to improve the system's ability to summarize, relate, retrieve, recommend, and reuse knowledge while keeping Scripture at the center.

### 4.2 白晝咖啡館 / Daylight Café

Life/culture/common room for faith and work, city life, culture, coffee, architecture, film, conversation, and ordinary daylight. Not a Journal column and not a Church meeting page.

### 4.3 守望禱告會 / Watch Prayer

A continuous prayer content series / prayer space connected to Scripture, intercession, and the Watch for the Dawn theme. Distinct from Church → Prayer Meeting, which is the actual church meeting entry.

### 4.4 Podcast

Audio-native channel for conversations, readings, teaching, people’s voices, and other audio content.

### 4.5 Video

Visual-native channel for visual essays, teaching, worship, documentary material, and other video content.

### 4.6 Newsletter

Ongoing communication/subscription channel for new issues, articles, meetings, resources, and related updates.

## 5. Church

```text
Church
├── About
├── Sunday Worship
├── Bible Study
├── Prayer Meeting
├── Contact
└── Giving
```

Church is a public top-level sibling of Journal, Mount of Olives, and About. Journal → Emmaus may serve Bible Study, but does not replace the Church structure. Mount of Olives → Watch Prayer is a content/prayer series; Church → Prayer Meeting is the actual church meeting entry.

## 6. About

Top-level main-site About. It covers the identity, background, mission, brand/site explanation, and necessary information about Living Water Westside Watch / 西望. It is distinct from Church → About.

## 7. 全站功能：多雷搜索

Global search/retrieval function, not AI Chat and not a content block.

Search scopes:
1. Bible World Knowledge
2. Main Site content
3. Tool-internal content

Main-site scope can include Journal, interludes, Mount of Olives, Church, About, News Broadcast and related published content. Tool-internal scope includes ONE, 多寫 and future internal tool content.

Core search behavior includes:
- partial terms
- incomplete phrases
- approximate terms
- Chinese/English mapping
- common typos
- incomplete names, places, and Scripture terms
- semantic recall where the user remembers the meaning but not the exact title

Search and knowledge relationships may improve internal indexing within privacy and permission boundaries. Public product remains search/retrieval, not chat.

## 8. Storybook / Design Training Environment

Storybook is not a main-site block and was never bound to Dawn Library. It is the design training/validation environment for the entire Living Water Westside Watch design system.

It covers Journal, Mount of Olives, Church, About, global functions such as 多雷搜索, and future design-system components. It does not create a separate public product hierarchy.

## 9. 多雷探索 / Doré Exploration

「多雷探索」是一个已经约定的工作指令，不是主站结构中的公开栏目、产品、页面或独立工具，也不是「多雷搜索」的同义词。

当用户提出「多雷探索」时，表示针对当前具体问题，启动一次系统性的方案探索与研究：

1. **全网研究** — 不局限于现有项目或单一来源，全面寻找世界上已经存在的相关方案、工具、框架、实践与资料。
2. **优先开源资源** — 优先检查成熟的开源项目、公开资料、可自部署组件、现成 libraries / frameworks 与已有实现。
3. **优先成熟方案** — 不因为某个方案新颖就优先采用；需要考察实际使用、维护状态、社区／生态、稳定性、问题记录与长期可用性。
4. **成本优先考虑免费** — 优先寻找免费或无需持续付费的方案；如果存在收费部分，需要同时寻找和比较免费替代方案。
5. **轻量与低占用** — 特别评估 CPU、RAM、储存、依赖数量、部署复杂度以及对现有系统的负担；不是追求大而全。
6. **稳定与易维护** — 评估部署稳定性、故障排查难度、依赖健康、升级风险以及长期维护成本。
7. **优先利用现成能力** — 核心原则是「先研究世界上已经有什么，再决定我们需要自己做什么」，避免为了一个需求重新制造已经存在的系统。
8. **最后回到 Doré Core** — 将探索结果与现有 Doré Core 的 Memory / Context / Retrieval / Knowledge / Search、Provider、Research、Graph、现有工具及产品适配器进行对照，判断哪些可以直接使用、哪些可以 adapter 接入、哪些需要改造、哪些才值得自行实现。

「多雷探索」的输出不是简单地推荐一个工具，而应回答：

```text
这个问题全世界已经有什么？
↓
哪些是成熟的？
↓
哪些是开源的？
↓
哪些是真正免费的？
↓
哪些足够小、占用少、稳定、好维护？
↓
哪些能够与现有 Doré Core / 项目直接整合？
↓
哪些已经不需要我们自己重新造？
↓
最后才决定需要自己开发什么。
```

因此，「多雷探索」是 Doré 面对工程、知识、工具或系统问题时的**全面外部学习／方案发现程序**。它本身不改变主站结构；任何涉及主站结构的修改仍必须由用户决定。
