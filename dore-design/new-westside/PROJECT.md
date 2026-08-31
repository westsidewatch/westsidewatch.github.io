# New Westside Visual Structure / 新西望視覺構建

Status: ACTIVE
Established: 2026-08-31
Working environment: Doré Design
Main engineer: ChatGPT
Learning and bounded local execution: Doré

## Mission
承接已完成的 Westside Watch 視覺研究、Figma/Penpot 實驗、現行主站內容與 Doré Design 工程，重新建設可以實際工作的「新西望」網站視覺結構。不重新啟動 Visual Discovery。

這不是單獨做 Homepage v2，也不是把某一期 Journal 當成全站模板。目標是建立 Westside Watch Design System + Living Editorial Grammar，並以新首頁作第一個完整實例。

## Sources of truth
1. 現行內容與排序：`data/volumes/vol-00.yaml` 及主站現行資料。
2. 現行設計狀態：`dore-design/NEW-WESTSIDE-CURRENT.md`。
3. 歷史設計推導：黑膠牆、Visual Language Lab、Visual DNA、Figma/Penpot evidence，只提供推導依據，不覆蓋現行真源。
4. 工作實體：`dore-design/` 下的 Doré Design workspace 與工程。

衝突優先級：主站現行資料 > Current Design State > 已批准項目決策 > 歷史研究 > chat memory。

## Locked architecture
Visual DNA: 光 · 線 · 紙 · 刻 · 築

Editorial Grammar: 磚 · 垛 · 流

- 5:8 = highest editorial gravity.
- Information is brick; editorial weight forms battlement; time forms flow.
- Crenellation 是 layout construction rule，不是城牆裝飾圖案。
- Color is metadata, not architecture.
- First Light Gold = highlight / trace，不作大片裝飾。
- Living Paper 與 Sacred Surface 分工。
- Engraving 以 trace / presence / image / rare immersive 分級，不作普通背景紋理。
- Journal 每期保持 editorial freedom，不吞掉永久 Website Grammar。
- Mobile 必須保留 editorial hierarchy 與 Living Wall 邏輯，不退化成普通 feed。

## Current content invariant
現行 12 欄目只讀 `data/volumes/vol-00.yaml`。第 10 為伯特利 / Bethel / Church Life。任何已被現行資料取代的舊欄目結構不得重新生成進 current workspace。

## Mainline
A. Current-state recovery — 收攏現行決策並清除 stale workspace structure。
B. Foundations — 色彩角色、Typography、spacing/grid、1px identity line、5:8、image/engraving、responsive。
C. Brick System — 建立少量 editorial weights 與內容 primitive，不做 generic card system。
D. Living Wall — skyline、negative space、promotion/demotion、quiet reflow。
E. Homepage — permanent Westside identity + Journal Tower + current editorial content + Gate/church entry architecture。
F. Responsive + verification — desktop/mobile 驗收、Doré Design same-artifact edit/render/verify、主站 implementation handoff。

## Acceptance
完成不是「一張 mockup 好看」，而是 Doré Design 內有可編輯的 approved visual system 與 homepage states；現行主站內容正確映射；human 與 Doré 可修改同一 artifact；desktop/mobile 保留編輯層級；工程可直接依 design tokens/rules 實現，而不必從 screenshot 猜設計；current/superseded 狀態明確，舊結構不能靜默返回。

## Working rule
ChatGPT 負責架構、設計合成、工程決策與驗證。Doré 在真實建造中觀看、學習、執行受控本機工作並留下證據。除非現有證據暴露真正未解的設計問題，不重新開始一輪 Visual Discovery。
