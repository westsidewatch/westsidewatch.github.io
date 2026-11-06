# 橄欖山 V4 — 先設計後動效：多雷探索與靜態構圖母本
*2026-11-06 · PR #1385 Draft · 只研究藝術母本，不得視為上線批准*

## 結論：截至 V3.2 **沒有**符合獲獎級要求的藝術基礎

V3.2 擁有可回收的滾動生長技術，但「植物先畫滿 1600×900，再讓海報遮擋」造成實際屏幕只剩切碎枝葉；即使 1,225 條 SVG path 加上數千條葉片子路徑，也沒有建立成熟版畫。使用者提供的 2026-11-06 實際截圖確認：十二張講員海報仍然優秀，金線只是左右局部露出，山勢難辨，構圖欠缺獨立設計語言。此問題不是光效或動畫速度可以解決。

**禁止把 V3.2 當成 V4 藝術母本；只能複用其可靠的可逆捲動、原始海報版式測量、V10 活刻線機械和技術驗收。** 不改動已上線 01–03、ONE、十二張講員英文筆畫位置、兩次轉場、主站 5:8 經文封面。

## 多雷探索：已存在的成熟實作與授權（不是泛指 Gustave Doré 畫風）

| 候選與確切來源 | 美術價值／證據 | 權利及格式 | 採納決定 |
| --- | --- | --- | --- |
| **Walter Crane**, *Line and Form*（1914）；[OpenClipart #7331](https://openclipart.org/detail/7331/olive-branch)、[FreeSVG #136555](https://freesvg.org/johnny-automatic-olive-branch-1) | 有成熟葉群、雕版細節與分層刀法；早已真正向量化成站內 `04-olive-historic-engraving-v13.svg`（600×90），有真實耶路撒冷低地平線 | 公共領域 SVG；站內有可追溯原稿；FreeSVG 明示 Public Domain | **主體採納。** 刻線版式母本，僅用在海報外的紀念版芯／低位刻線，禁止放大成整張複製背景 |
| **G. Woolliscroft Rhead**, *The Principles of Design*（1905）；[OpenClipart #7176](https://openclipart.org/detail/7176/olive-branch)、[FreeSVG](https://freesvg.org/johnny-automatic-olive-branch) | 第二種成熟橄欖枝，歷史印刷裝飾可作更嚴謹的 botanical frame 對照 | OpenClipart 公開提供 SVG，FreeSVG 明示 Public Domain | **候選。** 不在未下載、核對造型尺寸與實際構圖前聲稱接入；可用於下一輪對照，未用作此次執行時資產 |
| **OpenClipart #81199**, [Olive Branch in Yellow](https://freesvg.org/olive-branch-in-yellow) | 站內 `04-olive-botanical-gallery-v12.svg` 保存實際公共領域植物形態；V12「整張斜枝穿過海報」曾被否決 | Public Domain/CC0，已存原生 SVG | **只有裁切的側邊參照，尚未通過藝術驗收。** V4 A/B 只留在海報安全區以外；絕不恢復被否決的整屏對角造型 |
| **John Douglas Woodward / Charles Cousen**, [NYPL: *Jerusalem from the Mount of Olives* 1881–84](https://old-digitalcollections.nypl.org/items/510d47d9-5d9b-a3d9-e040-e00a18064a99) | 完整的橄欖山視點、古樹、山谷、耶路撒冷城牆與銅版刻印技法；真正的地理辨識來源 | NYPL 標示美國公版、可無限制使用，並註明其他地區版權未獨立判定；掃描為點陣，不是 SVG | **地貌與構圖標準。** 暫不把整幅 JPEG 假裝向量化；先按海報實際安全區定義獨立 SVG 景觀需求 |
| **William Miller**, [*Olea europaea longifolia*, Botanical Cabinet plate 456](https://commons.wikimedia.org/wiki/File:Loddiges_456_Olea_europaea_drawn_by_W_Miller.jpg) | 真實枝、果、長葉的接法、疏密和銅版植物切面，而不是公式化葉輪廓 | 19 世紀植物圖譜，站內已保存研究鏈接；目前引用是歷史圖像，不是已取得的 SVG | **解剖／刀法檢查基準。** 不宣稱可直接投入生產 |
| [MDN SVG clipPath](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Element/clipPath) | 技術上可把版畫裁到有意義的可見範圍，不影響原始路徑幾何 | 標準瀏覽器能力，無需依賴新 runtime | **採納裁切策略。** 原始 3:4 全保護，不必新建動畫引擎 |
| [SVG.js](https://github.com/svgdotjs/svg.js)、[SVGO](https://svgo.dev/docs/introduction/) | SVG.js MIT、可操控時間軸；SVGO 清理設計工具多餘節點 | 工具已有成熟實作，需求與風險各不同 | **不引入 JS 依賴。** 構圖問題不是 library 可以修補；SVGO 僅限離線優化候選，須與原稿比對 |
| `docs/design/SVG-EXPLORATION-LIST.md` 和 `static/experiments/p2-v10-living-strokes.html` | 開源查核、單 RAF 與持續活刻線；已用過的 SVG 002/V10 技術 | 已在工程內；以測試記錄為準 | **保留生長技術，待藝術通過再接入。** 不再為了「動起來」重造植物 |

## 已確立的視覺設計基礎（真正保留）

1. **主角永遠是 12 張講員 3:4 成品**，含 `static/olive/components/speaker-baseline-v1/baseline.js` 的 frozen Shadow DOM **英文字母**。不得重新排英文、不能拿原始照片 PNG 代替批准的合成作品。六欄／兩列總覽是已經建立的版面約束，手機不同欄數只做正常裁切與重新排列。
2. **Design OS 顏色**：大背景 `--ws-olive: #738a5a`、經過定義的晨光金 `--ws-morning-gold: #d2bc69`、暖金 `--ws-warm-gold: #b79838`、紙色 `--ws-paper: #faf9f5`。嚴禁大面積黑底、任意深綠漸層、文字霓虹光斑。
3. **標題只存在一次**：`OLIVE MOUNTAIN`，可作 A 的中央古典軸線，或 B 的放大且偏左的義大利編輯刊頭，不得侵入第一行海報。經文與前一章封面不可被同名重疊使用。
4. **歷史植物只在能看見之處。** 先計算完整海報 bounding boxes 再放置植紋：側邊兩列、上方標題區、下方實際露出的地平線，不讓 85% 的植物畫在被海報蓋住的中段。獨立刻線不得露出被切斷的莖。
5. **動效順序不變**：從 03 MERSI 材質交接，到 04 的雙海報、固定版式後背景切換、講員成對展示、最後十二人 FLIP 總覽；藝術母本階段**不增加任何動效**。之後只對已成立可見的 SVG 添生長線條，不讓動畫重設頁面。
6. **義大利雜誌式雙層節奏**：第一層海報清楚、有表情；第二層採單一視點的低對比植物與城市刻線，而不是每格裝一個相同枝條。版畫應有留白和顏色紀律，不以「總路徑數」當品質。

## V4 實際靜態設計版｜已建立可操作的源碼，不是出圖

**[靜態藝術構圖 A/B 試驗頁](../../../static/experiments/olive-mountain-art-foundation-v4.html)**（部署網址 `/experiments/olive-mountain-art-foundation-v4.html`）。

- **A｜ARCHIVAL AXIS：** 古典中軸刊頭 + 兩側邊界線 + 真實公共領域橄欖植物*極窄邊緣剪裁* + 下方唯一 Walter Crane／耶路撒冷實際 V13 橫刻。十二張海報作為唯一圖像焦點；下方細版芯為自然閱讀收束。
- **B｜FOLIO PRESSURE：** 明顯不同的放大、偏左 Bodoni 刊頭與非對稱佈局；植物由左換成右外緣、壓低密度；V13 地平線偏到左下，保留足夠的空間。不是把 A 的顏色或路徑換個數字而已。
- **相同安全區：** 預覽用**真實十二張編輯海報，並逐張 mount 已凍結英文排版的原始組件**，沒有 placeholder、沒有新造英文字。桌面六欄兩列；平板四欄三列；手機三欄四列且允許上下閱讀，絕不把 3:4 原稿壓扁。按「檢查海報安全區」即可看到原稿實際保護輪廓。外置控制條不進入正式網站。
- **特別記錄**：V13 在這份設計中確實作為**已儲存原生 SVG**透過 CSS mask 引用；V12 只在邊緣裁切後作候選。NYPL 的 1881 年名作是構圖研究，不是這次網頁載入的資產。此區分必須誠實報告。

## 不得跳過的靜態藝術驗收

- 1648×928、1440×900、390×844：十二幅作品原字 3:4 完整，確定插圖刻線不蓋住、不裁斷、不模糊英文；不能用空白卡測試；
- 建立 B 與 A 的實際瀏覽器截圖，與 V1、V3.2 同場景對比；縮至 25% 能看出海報主次與印刷品的空氣；
- 刻線是否有真正的橄欖樹感、意義明確的山地、設計精度；如果安全區裁切只剩幾個碎枝，應立即淘汰該方案，不得宣稱畫面成熟；
- 按 `WESTSIDE-EDITORIAL-MANUAL.md` §6 **10 項 0–2**初審，分數需 `>=15/20`，意義／構圖區別／可近用／編輯性都不得得 0；人工作品評審未做以前不得先行宣稱通過；
- **只在上面通過後**將靜態母本拆為可長出的路徑並接入既有 MERSI scroll engine。不得因工程測試綠燈提前上線。
