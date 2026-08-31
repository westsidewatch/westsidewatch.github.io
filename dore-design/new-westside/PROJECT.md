# New Westside Visual Structure / 新西望視覺構建

Status: ACTIVE
Established: 2026-08-31
Working environment: Doré Design
Main engineer: ChatGPT
Learning and bounded local execution: Doré

## Mission
承接已完成的 Westside Watch 視覺研究、現行主站、Figma/Penpot 實驗與 Doré Design 工程，重新建設可以實際工作的「新西望」網站視覺結構。不重新啟動 Visual Discovery。

## Immediate correction / 2026-08-31

先恢復，再改造。不得在 Doré Design 裡用臨時 mockup 取代主站已存在且仍有效的視覺資產。

1. **Journal / Vol.00 視覺暫不大改。** 第一階段從現行主站完整移植到 Doré Design，保留其現有刊頭、Opening、Contents、四樂章／三間奏、文章閱讀視覺與相關資產。只有在移植完成並與主站對照驗收後，才討論局部升級。
2. **刊頭必須使用主站現行刊頭資產。** 主站首頁目前使用 `static/images/westside-watch-masthead-landscape.svg`；同時保留 `westside-watch-masthead.svg` 與 morning-star 資產。Doré Design 不得自行用普通文字重新拼一個替代刊頭。
3. **Website 與 Journal 分層。** Journal 是網站中的出版物；Vol.00 的內部內容單元不是網站欄目。新西望永久網站視覺結構另行重建。
4. **主站現有成果先作 baseline。** `layouts/index.html`、`layouts/vol-00/*`、`layouts/partials/vol-00-contents.html`、相關 CSS/JS/images 是 Journal 移植基線，不得因重建網站 shell 而丟失。
5. **新建的部分是 permanent website shell / homepage / current four-column information architecture / Living Editorial Wall。** 不用 Vol.00 的內容結構代替網站 IA。

## Sources of truth
1. 主站現行可見實現與資產：最高視覺 baseline。
2. 現行網站／期刊內容資料。
3. `dore-design/NEW-WESTSIDE-CURRENT.md`：現行設計原則。
4. 黑膠牆、Visual Language Lab、Visual DNA、Figma/Penpot evidence：歷史設計推導，只提供 rationale，不覆蓋現行 baseline。
5. Chat memory 只作導航，不作版本真源。

## Locked architecture
Visual DNA: 光 · 線 · 紙 · 刻 · 築

Editorial Grammar: 磚 · 垛 · 流

- 5:8 = highest editorial gravity.
- Information is brick; editorial weight forms battlement; time forms flow.
- Crenellation 是 layout construction rule，不是城牆裝飾圖案。
- Color is metadata, not architecture.
- First Light Gold = highlight / trace，不作大片裝飾。
- Living Paper 與 Sacred Surface 分工。
- Engraving 以 trace / presence / image / rare immersive 分級。
- Journal 每期保持自己的 art direction；永久 Website Grammar 不吞掉 Journal，Journal 也不吞掉 Website。
- Mobile 保留 editorial hierarchy 與 Living Wall 邏輯。

## Mainline
A. **Recovery / transplant** — 把現行主站 Journal/Vol.00 與正式刊頭、圖像、Opening/Contents/reading states 移植進 Doré Design，建立 visual parity baseline。
B. **Website IA recovery** — 只從現行主站與 current project source 恢復網站真正的四欄目與永久內容關係，不再從 Vol.00 推導網站 IA。
C. **Foundations** — 在保留有效資產的前提下收斂 website tokens、type、grid、line、surface、responsive rules。
D. **Brick System + Living Wall** — 建永久網站的 editorial grammar。
E. **Homepage** — permanent Westside identity + current Journal presence + website four-column structure + church/knowledge/product relationships。
F. **Responsive + verification** — desktop/mobile 對照、same-artifact edit/render/verify、主站 implementation handoff。

## Acceptance
- Doré Design 中的 Journal baseline 與現行主站視覺對照一致，不再出現臨時文字刊頭替代正式刊頭。
- Journal 與 Website IA 不混層。
- Website 四欄目使用現行真源，而不是 Vol.00 內部內容單元。
- 新建 website shell 與既有 Journal 能在同一品牌系統中共存。
- human 與 Doré 可編輯同一 artifact，desktop/mobile 保留編輯層級。
- current/superseded 狀態明確，舊結構不能靜默返回。

## Working rule
ChatGPT 負責架構、設計合成、工程決策與驗證。Doré 在真實建造中觀看、學習、執行受控本機工作並留下證據。先恢復已有成果，再建新結構；沒有證據不得用新 mockup 覆蓋主站已存在的有效設計。
