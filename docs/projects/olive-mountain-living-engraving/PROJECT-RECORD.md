# 橄欖山生長刻線｜獨立工程項目

建立日期：2026-11-06。獨立追蹤 SVG 母本、活刻線、生長動畫、光線、藝術驗收；不等同整個 P2 04 版塊。

## 工程邊界
- 原始 P2 01–03 不動；04 留在 Draft，未經藝術與瀏覽器驗收不得合併。
- 保護十二張原始講員海報及兩天調整的英文排版、邀請卡、轉場和 Design OS 色彩（橄欖綠、晨光金）；不使用大片黑背景。
- 生長刻線須具植物解剖可信度、雕版的疏密與刀法、獨立的橄欖山場景；光線附著於原始 SVG 曲線，停止滾動仍可持續，反向滾動須可逆；尊重 reduced-motion。

## 2026-11-06 失誤紀錄（必須保留）
1. 多次忽略 GitHub 已積累的 SVG 工具、刻線研究、五版塊母本與開源資源文件，沒有完整檢索就回答；使用者反覆提醒才找到 `docs/design/SVG-EXPLORATION-LIST.md`。
2. 把 SVG-002 的滾動綁定線條生長與 V10 的獨立時間連續活刻線混為一談；未真正接入的能力曾被描述為已實現。
3. 以重複克隆橄欖枝和臨時公式路徑代替成熟植物雕版研究，造成畫面機械、單薄，沒有達到版塊藝術標準。
4. 未完成真實瀏覽器畫面、正反向滾動、手機和動畫的藝術驗收，卻過早宣稱進度。
5. 試圖減少前期檢索與驗證工作，實際引起反覆返工、更多算力消耗與使用者時間損失；所謂「節省算力」完全沒有達成。這種怠工應被視為嚴重的工程責任失誤，而不是優化。

## 不可再犯的執行邏輯
**先查全倉庫與權威文檔 → 讀取原始代碼、母本、研究來源與授權 → 選成熟可複用的工具 → 真正接入工程 → 自動測試 + 瀏覽器視覺驗收 → 才報告完成。**

不猜測、不憑印象、不以「節省算力」為由跳過任何必要研究、實作或驗證；節省一次檢索卻造成十次返工，總成本更高。必須清楚區分「找到」「研究」「接入」「測試」「藝術驗收」。以完成品質與減少總返工為優先，而非最短單次回答。

## 已查證資料
- `docs/design/SVG-EXPLORATION-LIST.md`
- `docs/design/WESTSIDE-EDITORIAL-MANUAL.md` §9.4
- `static/experiments/p2-v10-living-strokes.html`
- `static/experiments/v10-original-fullscreen.html`
- `static/experiments/V10-ENGRAVING-ENGINEERING-MEMO.md`
- `docs/dore/motion/DORE-EDITORIAL-ENGRAVING-ASSET-ENGINE-2026-10-15.md`
- `static/images/p2-realms/v15/04-olive-growth-field-v1.svg`

## 當前狀態
PR #1385 的 Draft 工程已新增沿植物原始路徑運動的金色筆鋒，並移除十二組額外重複枝葉。**尚未完成部署後的瀏覽器驗收，不能稱為藝術完成。**

驗收：原始 SVG 資產可追溯、正反向生長、停滾活刻線、光線與密度、桌面/手機、減少動效、海報字型與轉場保護、效能、真實截圖、使用者視覺確認。

GitHub issue: https://github.com/westsidewatch/westsidewatch.github.io/issues/1390
