# P2《西望》｜A／B 字體海報「案例 → 排版 → 開源設計方法」多雷探索

**2026-11-04 · Art-direction research and executable layout briefs, NOT an approved artwork; no P2 runtime or final asset changes.**

Authority: [WESTSIDE-EDITORIAL-MANUAL.md](WESTSIDE-EDITORIAL-MANUAL.md) → [WESTSIDE-EDITORIAL-TYPOGRAPHY.md](WESTSIDE-EDITORIAL-TYPOGRAPHY.md) → [latest A/B poster brief](P2-XIWANG-NEW-GLYPH-OVERLAY-ENGRAVING-RESEARCH-20261103.md). This document does **not** reinstate the superseded brush/temple-plaque brief. Older [12-Cosmos study](P2-XIWANG-TYPE-REDESIGN-COSMOS-20261102.md) is evidence only; its proposed brush-calligraphy implementation is *no longer binding*. Right-hand approved 5:8 magazine cover, 03 Emmaus Doré gallery, homepage full-plane sevenfold, Church and Design OS runtime remain protected.

## 1. 找回十二張使用者「真正」的字體海報截圖

已從使用者的檔案 Library 找回 **12 張 2026-11-02 原始 Cosmos 網頁截圖（每張是多件作品構成的收藏牆，而非十二件同一作品）**：

`Screenshot 2026-11-02 at 22.02.17.png`、`22.02.21.png`、`22.02.25.png`、`22.02.29.png`、`22.02.33.png`、`22.02.37.png`、`22.02.41.png`、`22.02.45.png`、`22.02.50.png`、`22.02.54.png`、`22.02.59.png`、`22.03.03.png`（全為 2048×1152 原始螢幕截圖）。

**權利：**上述截圖與其中的海報原圖**只在使用者對話／設計研究內部查看**；不重新發佈、抓取為網站素材或把截圖拼貼上傳到公共 GitHub。逐件原作者大多未確認；不因出現在 Cosmos 上就稱為開源。此文只記使用者檔案的時間戳、可觀察設計機制及對應設計練習。

### 十二張截圖的設計判讀索引（來源：使用者原截圖與舊研究）

| 截圖 | 有用的當代文字設計機制 | 優先案例方向 |
| --- | --- | --- |
| 22.02.17 | 巨字與細索引的尺度對撞、局部異質墨版 | A 字作整張版心 |
| 22.02.21 | 極窄字列與自由黑白領域；不是無限制拼貼 | A 的負空間／小字區 |
| 22.02.25 | 黑白高反差、局部切面與縱向節奏 | A 的字內白 |
| 22.02.29 | 字群垂直佔位、滿版與留邊互抵 | A 的視覺承重 |
| 22.02.33 | 大文字壓縮、印版異色局部介入 | A 的字骨重構；B 的極少色版 |
| 22.02.37 | 厚重巨字與細英文 folio 分明 | A/B 雜誌身份主次 |
| 22.02.41 | **巨型紅色幾何字**：模組形體可形成完整海報，不靠裝飾 | A 優先，比例與筆畫雕刻 |
| 22.02.45 | 細線、幾何與書寫密度並置，字內留白明確 | B 的疏密和方向 |
| 22.02.50 | 巨字壓邊、留白、少量 editorial metadata | A 的一字獨大／雙字相接 |
| 22.02.54 | 圖形刻線與文字一起作視覺重量，不堆背景 | B 的微型刻線系統 |
| 22.02.59 | **粉底紅字「純情」海報**在原頁首排，巨型獨立字形、切面、負空間連成一張；其他頁面有字內微線與規整刊次 | **A 的第一張直接構圖案例** |
| 22.03.03 | 大字與短小細註、非對稱廣告版面 | A/B 的真正 poster hierarchy |

另有使用者直接提供的**深灰底白色點陣／同心圓／波紋／放射刻線中字海報**：此為 **B 的第一直接構圖案例**，研究不同線場如何令「同一巨幅字體」形成*連續張力*；灰底的「字形與密度對比」是參考方法，**不是授權《西望》使用黑灰背景的理由**。

## 2. 不再把「會輸出 SVG」誤當「會設計海報」

研究時必須分清三種來源：

- **成熟設計案例（可觀察構圖，不可直接複製）**：使用者的 Cosmos 原始截圖；[純情 4th giant-letter study](https://www.pinterest.com/pin/565835140696146335/)（二次轉載、作者/原作鏈待進一步追認）；[Taipei Graphic Interflow Festival 2019](https://www.behance.net/gallery/87365359/Taipei-Graphic-Interflow-Festival-2019)（線條扭曲構成清楚的整體圖形）；[Beijing Design Week 2019 Ink Art](https://www.behance.net/gallery/86613943/Beijing-Design-Week-2019-Ink-Art-posters/modules/501167937)（連續線場與密度高低）；[Lacking Sound Festival 100](https://www.behance.net/gallery/33426771/100Lacking-Sound-Festival-100)（極細字體主題）；[TPDA 30 poster exhibition](https://www.graphicarts2001.com/article.php?action=show&id=118)（編輯資訊與巨型幾何表面的分工）；[Typographic Posters Archive](https://www.typographicposters.com/)，[Letterform Archive](https://letterformarchive.org/online-archive/)。以上均為案例研究，不代表開源素材。
- **真的展示「程式 → 實際海報」的開源／公開碼案例**：[Volorf/Processing-Posters](https://github.com/Volorf/Processing-Posters)（7 張真正 poster；作者的 pipeline 為 p5.js *生成主圖形* + Figma *做最終海報排版*；目前未看到 LICENSE，**可以學方法，不得直接複製程式到本站**）；[350 layout compositions](https://github.com/nevertoday/350-layout-compositions)（350 個編輯／構圖範式，**CC BY 4.0**，作品再利用須履行署名）；[evo-poster](https://github.com/sergiomrebelo/evo-poster)（**MIT**，內容與圖像為輸入的可變版式組合器，舊專案未證明能直接做優質漢字字骨）；[flowshape](https://github.com/Jossifresben/flowshape)（**MIT**，具體 poster layout/data and SVG compositional constraints）。
- **字體與印版創作後端（只有通過案例約束後才調用）**：[bouffont](https://github.com/meodai/bouffont)（**MIT**，從骨架與字形增生為 SVG、支援 letter grouping / geometry；CJK 原生字骨與 readable counters **必須以真「西望」實測**）；[TYPE-O](https://github.com/lnyssen/type-o)（**MIT**，在真正字體 contours 上堆疊 fracture、stencil、swell、halftone 並保存 recipe；當前官方內建字型主要 Latin，**不當作已驗證 CJK 工具**）；[Paper.js](https://paperjs.org/about/)（**MIT**，貝茲布林與自定義筆段）；[poster-grid-inspector](https://github.com/Ygria/poster-grid-inspector)（**MIT**，分析構圖格線與輸出 SVG guides，Skill 可依 host model；可選 Web/API mode 可能需模型服務；**不是藝術判斷代用品**）；[mono-color-skill](https://github.com/yanliudesign/mono-color-skill)（**MIT source/skill, not example artworks**，專管留白、單一主視覺、印版角色），加上既有 [Inkscape](https://inkscape.org/)／[Shapely](https://github.com/shapely/shapely) 真正可運行的 SVG 構建。

**不收或降級：**未找到 LICENSE 的海報碼不可照搬；只隨機換色的 generator 不會自動提升設計品質；[Void](https://mishaivanov.com/void/) 非商業免費使用、商用需另尋授權，且以 Latin/Cyrillic 為主；[posterly](https://github.com/Chenruishuo/posterly) 是 AGPL-3.0 的學術研究海報工具，會涉及來源公開條件和不同工作目標，不嵌入西望；[Sai Poster Studio](https://github.com/wyuee912-ops/sai-poster-studio) 有 template editor、batch contact-sheet 工作流，但根目錄未核到 LICENSE，先只研究「批次比較」方法。

## 3. A — 一組巨大、正立、全新字骨的「西／望」海報

**核心參考不是一般黑體，而是 22.02.59 粉底紅字案例的「字形自身即整張海報」；再交叉比 22.02.41、22.02.50 的大字和字內白。**

### A-1｜Sculpted Monolith / 雙字同一建築體（優先候選）
- **版心：**左頁 1:1 獨立方形內，一個上「西」下「望」，光學視覺寬度極大（從左/右各預留約 5–8% 空白起作實驗，不直接照搬參考裁邊）；上下字共有垂直重心，但兩字沒有非必要旋轉和透視。
- **字骨：**必須重新雕刻兩個字的**承重筆段、曲面與三角形／弧形負空間**；不要把 Noto A2 斜切就當原創。西頂框是一道橫向張力，望的上/中/下與底部要有可見的受力關係。每個封閉字孔連貫、有呼吸，不可讀性優先於炫技。
- **圖像面：**只有字形填實的主印，背景是有理由的 OS paper（非自動泛黃），輔助資訊局限兩角：WESTSIDE WATCH / VOL.00。沒有圖示、晨星、城牆、主題經文、色塊拼貼、側邊七目錄。
- **開源設計方法：**先依參考人工設計筆段 → [Paper.js](https://paperjs.org/about/) / Inkscape 畫不同輪廓 → 字孔布林 → [350 compositions](https://github.com/nevertoday/350-layout-compositions) 的滿版/失衡軸線作排版練習 → mono-color 驗收。外部工具不能自行創造藝術字骨。

### A-2｜Editorial Off-Axis / 巨字偏置與受控留白
- 西、望保持正立的雙字結構，整組可沿共同軸**平移而不是傾斜**；側邊只留 10–20% 編輯負空間，外緣的 folio 不侵入字孔。適合和右頁正式封面建立明確主次，不靠更多東西填滿空白。
- 同一字骨但**不同空間構圖**，不是換背景色；以 [flowshape](https://github.com/Jossifresben/flowshape) / [evo-poster](https://github.com/sergiomrebelo/evo-poster) 參考 ratio/overrun 裁決再作真 SVG。

### A-3｜Shared Edge / 利用對開界線作版面關係
- A 左側主印在接近右邊界處留出最窄的呼吸空間，使右側 5:8 正式封面出現時形成正負形對位，但不跨入/覆蓋正式封面；這是純**構圖關係**，不是新畫一張封面。
- 在左頁單獨 1:1 和真對開（左/右固定比例）兩種場景一起驗收；獲獎級要求不只是一張漂亮孤立圖片。

**A 的藝術否決：**仍是普通黑體／舊 A2，字孔裝飾性亂切，巨字破碎認不出西望，右頁封面主次被搶，任何一項即重新造字，而不是微調濾鏡。

## 4. B — 七組正立字骨與七種刻線共同構成一張印刷海報

**第一參考：使用者的深灰白線「點陣 → 同心／方向 → 波浪 → 放射」整體字海報。借的是構圖連續性、線條密度的敘事和方向組織，非黑灰底、非左邊七個圖示。**

### B-1｜Integrated Print Plates / 同一巨型版心的七重套印（優先候選）
- **不是** 7 排字、7 套各自孤立的 logo，也不是一套 Noto font 變 7 色，更不是 A 的線紋皮膚。七個各自帶 `data-word-layer` 的「西望」構件共享一個*主構圖中心*，以不同尺度（小幅度、需光學校正）與少量位移互相穿插，所有字零度旋轉。
- 先指定**一層最可讀的大形體**（主印/最優 `西望` 黑量），再控制另外六組的 **密度、局部出現的位置、明暗與印版相位**。七個 OS 版塊色是來源色；在總體上必須形成有主次的面積與灰階，不能七色等分。
- **刻線只在字內**：以 glyph polygon + counter holes 確定 Region，對每組先生成自己的線段、再作幾何交集，不用畫滿全頁後再用 browser mask 假裁切。背景不出現刻線或象徵圖示。參考 [Volorf 七張成品的「主視覺生成 → 最終排版」分工](https://github.com/Volorf/Processing-Posters)，不要複製未核授權原始碼。

### B-2｜Continuous Engraved Field / 刻線連續場，由密度塑出文字
- 如原灰底案例，放射／網點／等距曲線**不是七種濾鏡**，而是一種由上至下的方向流動；其內在分區在不同字形上具有情感與閱讀節奏。用半色調密度和方向線相遇處建立主視覺，字外必須仍是乾淨底紙。
- 各七組仍是獨立可編輯印版，但在構圖上形成**局部一個連續視覺場**，不是 seven blocks。以 [AlgorithmicTypography](https://github.com/MichailSemoglou/AlgorithmicTypography)（MIT，網格波場及 SVG/PDF 匯出，具體 CJK 展示/實用性待測）研究圖形語義，再由現有 Shapely 真裁切。
- 此路線最有機會接近原參考，但如果「看見刻線，讀不出西望」，必須退回字骨，不應以刻線多寡轉移問題。

### B-3｜Registration Rhythm / 七個正立 word groups 的輕微套印相位
- 不是做大幅位移或任意錯版。以 1 主版 + 2–3 副版高可見度 + 其餘 3–4 層低對比邊緣／細節的節奏，保持七組可分辨的原生 layer；在受控範圍內做光學位移以塑造流動，不改方向、不旋轉、不把一個字裁成七個物件。
- 可借 [TYPE-O](https://github.com/lnyssen/type-o)「每套變體有明確 recipe 和 legibility gate」的設計方法，但它未驗證繁體西望，不拿內建 Latin 字體當母本。

**B 七種版塊刻線語義：**可由既有 P2 版塊逐一導出無需畫物件的方向場：教會/活水＝湧流與回旋；雜誌/第一光＝正立字的分割與秩序；以馬忤斯/道路＝連續方向與轉折；橄欖山＝分枝狀細脈（**不是畫橄欖葉**）；黎明書局＝印版短線與漸變疊印；Cinema＝像拉開布幔的平行張力；白晝咖啡館＝豐盛的密度與節奏（**不是畫杯子/麥穗/葡萄**）。這些只是刻線的生成規則，不能變成背景圖案或概念插圖。

**B 的藝術否決：**七排、無主次七色、同一舊字骨換色、斜字、畫在字外的紋理、黑底無設計因由、過量標籤或圖示、無法縮小辨認，均否決。

## 5. 下輪真正「照案例做」的設計練習，而不是繼續羅列工具

| 練習 | 首選參照 | 交付草圖與測量問題 | 要測的藝術分歧 |
| --- | --- | --- | --- |
| **A-1** | Cosmos 22.02.59 的紅／粉巨字 + 22.02.41 幾何字 | 1:1 上下「西望」原創 path，首屏沒有 metadata 和紋理 | 字骨不靠特效是否已成海報 |
| **A-2** | Cosmos 22.02.50 的巨字偏置/細字留白 | 同一字骨，非中心構圖和右 5:8 封面對照 | 留白是真排版還是浪費面積 |
| **B-1** | 灰底白色網點/同心/波紋/放射用戶參照 | 7 個有意義的 Region，主要深墨版 + 局部色印版，極少 folio | B 是一個結構還是 7 種填充 |
| **B-2** | Taipei Graphic Interflow / Beijing Design Week 的線場性格 | 單一連續方向場承接七個可編輯字組，線條全部字內 | 字形是否由刻線真正塑成 |
| **B-3** | Letterform Archive 的印刷套版原理；Volorf 生成圖+排版工作流 | 七層微套印，主次 1+2+4，真 1:1 與 P2 對開比較 | 交疊是否有光學秩序 |

**測試規則：**每種練習先做「只有字骨」+「字骨與必要刊次」兩張清晰樣本，再由同一 OS 細排版校正，不要一開始加入裝飾資訊；桌面、768、390、320、200% zoom 以及 P2 真實對開再作人眼判定。既有 [OS 0–2×10 / 15–20 探索 gate](WESTSIDE-EDITORIAL-MANUAL.md) 只是内部評估，非任何得獎認證。**沒有真正 A1/B1 對開畫面，就不宣稱藝術定稿。**

## 6. 研究結論與進度邊界

1. A、B 的關鍵已由「SVG 會不會生成」轉為**哪一個案例的字形和版心機制能真實轉移到西望**。從「先選作品」到「抽象規則」再到「選工具」，不再倒過來。
2. A 主方案：**A-1 原創幾何巨字＋受控內白**；B 主方案：**B-1 七印版共享同一主視覺＋B-2 連續刻線的密度節奏**。不能讓 B 退化成 A 的線條填色。
3. 本輪已找回 12 張原始 2048×1152 Cosmos 收藏牆截圖、完成成熟案例／可用開源方法／授權區分和可施工設計方案。**未宣稱任何新 SVG 已按此 Art Direction 製造、未進行 P2 真 browser 及得獎級人工視覺驗收。**
4. 原始截圖僅在對話檔案/私有 working container 做分析，不提交公開 repo。後續做 5 個獨立 SVG 草圖時，不可借由 API 生圖替代上述真正的字形/線場設計步驟。
