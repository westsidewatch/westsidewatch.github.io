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


## 2026-11-06 二次程式碼稽核：使用者回報「刻線沒有一點點進展」

### 已核實的原因（非猜測）

1. **母本原地踏步。** `static/images/p2-realms/v15/04-olive-growth-field-v1.svg` 共 284 條 `<path>`，其中 12 組 `.olive-growth-branch` 各有 23 條植物路徑；逐項比較 `d` 值，12 組全都一致。所謂「十二組不同植物」只是同一母本的 12 次位移、縮放、鏡射／旋轉。最近三次修改只變更 JS/CSS/HTML，未重做該 SVG。
2. **動的是微小高光，不是生長中的植物。** `static/js/p2-0104-olive-continuation.js` 中真正改寫 `d` 的 `drawGrowingCurve()` 僅套用 8 條人工主幹；當 `local>=.99999` 時恢復原 `d`、隱藏筆尖。其餘 276 條植物與裝飾路徑主要靠 scroll-bound dashOffset 顯示，不會隨時間繼續生長。新 `livingFrame()` 只推進 `livingClock`；`paint()` 用它改動高光的 `strokeOpacity` 和 `strokeDashoffset`，沒有持續改變植物輪廓。
3. **高光可視量極小。** 新增 `.olive-growth-burin` 使用 `stroke-dasharray="35 965"`，即每條正規化路徑中一次只顯示約 3.5% 的金線段；CSS 沒有多層刻線光場或經藝術驗收的動態光線構圖。改進不應被描述為已完成的「金光生長刻線」。
4. **預覽入口選錯。** 上次提供給使用者的網址 `?d=17.55` 已超過 `T.indexStart=16.25`，此時 `speakerGrowth=1`，8 條線全部恢復靜態原樣，筆尖隱藏。此網址無法用於驗收「生長過程」。
5. **沒有把研究變成母本。** `docs/design/OLIVE-MOUNTAIN-ART-SOURCES.md` 已列植物解剖參照（William Miller）與橄欖山史地構圖參照（Woodward/Cousen），但兩者在目前母本中未轉化為成熟的植物／山形刻線構圖。全站刻線引擎文件 `docs/dore/motion/DORE-EDITORIAL-ENGRAVING-ASSET-ENGINE-2026-10-15.md` 明示 `PLANNED, NOT IMPLEMENTED`；不得宣稱已接入這個引擎。
6. **未執行驗收就提交並宣稱有實質進展。** 尚無可靠的實際瀏覽器前後對比、畫面評估及動態證據。程式碼有變更，使用者所要求的視覺結果沒有得到證明。

### 更正與責任

本項目的「實質進展」指藝術母本與可見動畫品質的提升，不等於 Git commit、CSS 數值、路徑數或增加 RAF。必須優先建立真正不同的歷史植物雕版群落、具有橄欖山地貌的整體構圖與持續生長的幾何刻線，再把這些主體接入可逆滾動與光層。保護已核准海報文字、Design OS 及 01–03；無實際視覺驗收前，任何「完成」說法均不成立。

**此節專門保留當天重複怠於做研究、假借節省算力反而加劇返工的工程後果。不得因往後修復而抹去。**


## 2026-11-06 — V2 第一輪實際工程交付（待藝術驗收）

這一輪不以討論或新 commit 數量代替畫面成果；原先 V1 的十二組植物曲線都是同一 23-path 母本變形，維持作為失誤與回退記錄，**不再使用它作為執行時植物母本**。

### 具體修改
- 新母本 `static/images/p2-realms/v15/04-olive-living-grove-v2.svg`：380 條原生 SVG 路徑；從可追溯的 V12 真實 OpenClipart 橄欖植物、V13 Walter Crane 公版植物、V11 原站樹皮雕版、V8 地形版畫四種不同素材整合；另獨立手繪 18 條根、枝、山脊、梯田生長中軸，沒有十二套完全同形的植物枝條。
- 真正切換 `static/js/p2-0104-olive-continuation.js` 的 `fetch` 來源至 V2，改接四種來源、18 條持續活動的中軸、金色筆鋒，保留可逆捲動與 reduced-motion。持續時間動畫不是簡單光點移動，結構線本身也按節制振幅更新 `d`。
- 使用 Design OS 橄欖綠／晨光金、保留原十二位講員 3:4 原作與英文排版，不修改 01–03。
- 更新 `tests/p2-0104-olive-continuation.cjs`：舊測試竟要求複製 12 套相同植物，現在改為要求四種來源與 18 條不同幾何路徑；驗證線條停滾仍動以及反滾生長長度一致。同步更新 `.github/workflows/p2-0104-olive-preview.yml`，將 V2 納入實際構建與截圖。

### 檢查與未完成項
- 已靜態驗證 V2 XML 標籤巢狀平衡、無非法 XML 實體，380 條路徑、18 條獨立中軸。
- **部署截圖、Chrome 動效、手機、反向捲動與美術是否足夠豐盛仍待 CI/瀏覽器證據；不宣稱藝術完成。**
- Core Contract 在較早的草稿合併測試中報出 `static/images/westside-watch-morning-star.svg` 的凍結首頁檔案差異；本輪沒有修改該檔案，必須獨立辨認既存差異，不能以此掩蓋本輪錯誤。
- 本輪一度漏掉真正執行時的 SVG fetch 位址，導致 CI 報錯、代碼看似修復但仍在載入 V1；已在 `ee098f7` 明確修正並記入此處，不能再讓未驗證的替換通過工程回報。
