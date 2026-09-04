# Conversation Archive — Publishing Program / Two Books

Date: 2026-09-03
Project: Westside Publishing Program / New Westside / 黎明書局
Record type: user-visible project dialogue

---

## User

不要摻雜偶像，小心屬靈爭戰。這部書最重的展示方式是這樣的，html線上就是一本打開的書，也是一扇一扇開啟的門，一座光明的城，就像是翻書一樣觀看，甚至到時可以直接印刷。現在journal上守望一座光明城，將是這本書的一個展示，也通過這個展示，推出journal的十二個欄目，因為我們所有欄目無論是名字還是定位還是功用，都有豐富的神學內容，更不要這方面還可以擴展。另外，第二本書也交給多雷寫「神很遠 神很近 天國語言極簡史」，這本書以文字為主，但大綱部分就可以變成一期journal的配圖特刊，文字5萬-10萬字，為的是鍛鍊多雷的語言能力，掌握風格，並希望可以中英文雙語。這本書我基本準備了有三四萬字，不算沒有基礎。這本書本身，還有一小篇偏學術的論文，這本書是完全結合黎明書局的loop，也就是說針對兩個主要的loop，我們都有書籍出版的結果對應。所以是兩本書單立項，各歸各的loop，還是立一個出版的項，調用融入結合不同的loop，這個邏輯和構架你可以考慮更好的。

### Uploaded source event

The user supplied two primary Book 02 sources in this conversation:

- `神很遠_神很近_54000.md`
- `天國語言極簡史｜論文.pdf`

The manuscript identifies the work as `神很遠 神很近 / 天國語言極簡史 / The Word Returned: A Brief History of the Language of Heaven` and already contains a substantial chapter structure and long-form prose. The academic paper presents a formalized thesis and argument chain around davar, saphah, Logos, glōssa, Babel, Pentecost and Corinth.

---

## Assistant / project decision

Adopt a **one-parent / two-book** architecture:

**Westside Publishing Program** is the orchestration layer.

- **Book 01 — 《聖靈也會參與設計嗎？》** remains an independent product owned by the New Westside / Brand Bible / visual-learning / Storybook product loop.
- **Book 02 — 《神很遠 神很近：天國語言極簡史》** is a separate independent product owned by the 黎明書局 / language / reading-writing product loop.

The parent publishing program supplies shared publication infrastructure: source/provenance, editorial standards, bilingual workflow, theological claim discipline, HTML book engine, print CSS/paged media, proofing, Journal adaptation, accessibility, and conversation archive. It must not flatten the two books into one voice or one visual system.

For Book 01, the canonical primary display concept is:

**HTML book = open book + opening gates + city of light + page-turning progression**, built so the same structured source can become a print-ready edition. `《守望，一座光明的城》` is a major Journal exhibition/entry surface for the book and should introduce/deepen the theological and editorial meaning of the twelve Journal columns.

For Book 02, the current manuscript is treated as a real authored foundation, not a blank assignment. Doré’s task is to learn the existing voice, improve long-form Chinese, build a durable style model, strengthen structure/source discipline, and eventually create a natural Chinese-English bilingual edition. The shorter academic paper remains a linked evidence/argument layer, not a replacement for the narrative book. Its Journal expression should be an illustrated special derived from the book’s outline/argument arc.

The user’s source boundary is strengthened: do not mix idol-centered, Buddhist, occult, New Age, syncretistic or unrelated sacred imagery/theology into Westside design/research as visual atmosphere or authority. Christian symbolism must also remain Scripturally/editorially grounded rather than decorative or superstitious.

Resulting project files/commits:

- `dore-design/publishing/PUBLISHING-PROGRAM.md` — `06459ae920be35a49fb19057b950490d8f135e31`
- `dore-design/publishing/books/BOOK-01-HOLY-SPIRIT-AND-DESIGN.md` — `5ab9b266251ccc1ae44fe966aef33bc56cc0481d`
- `dore-design/publishing/books/BOOK-02-GOD-FAR-GOD-NEAR.md` — `87258648b456974d3f114488d9ff2bdd404bd3eb`
- strengthened `SOURCE-BOUNDARIES.md` — `3f094976f9010cf21572ea5bc715b9c6c5bc45d0`
- rebound `BRAND-BIBLE-PRODUCT-LOOP.md` to Book 01 — `e7c863bc6008a94da03d3d311890d951316d39b7`

This archive preserves the decision as book/project provenance.
