# Westside Design OS · 七重疊雜誌式基準內頁

**狀態：** 可運行的獨立驗收版；**尚未經人工設計評審定稿**。屬於既有 Westside Design OS，不建立第二套視覺權限或獨立色彩／字體管理。

## 一、設計命題

**《西望》的編輯語法不是第八個模板，而是七重疊共同的排版基因。**

全站內頁不要求七種內容長得一模一樣，而要求它們共享可以辨識的編輯秩序：刊頭、卷次／版塊索引、雙語主標、主次頁面網格、經文方塊、正文、真正可閱讀的目錄、專題圖版、引註與頁尾。

**層級關係：**

1. Westside Design OS：唯一字體、色彩、字重、尺寸、間距、材料與動效權限。
2. Editorial Interior：以上共同的雜誌式組件及 Hugo 母版，不複製七份 HTML。
3. Realm scope：七種既有色彩／雕版／媒體身份的局部覆寫，不更改全域 `:root`。
4. Content：各版塊的真實內容和來源鏈接，不能用空版面冒充資料完成。

與既有 P2 之關係：**首頁、導航、Merci 轉場、七重疊、P2 翻頁、教會 3D、橄欖山卡片、黎明書局第二／三層的已審定成果均保持原狀**。此輪新增七個可實際瀏覽的 Hugo 內頁供設計驗收，通過評審後才將已批准組件漸進接入原版塊；不可先全站套版。

## 二、七個版塊一次成套，沒有遺漏

| 版塊 | 基準內頁路徑 | OS 色彩來源 | 原有內容入口 | 視覺差異保留 |
|---|---|---|---|---|
| 活水堂西區教會 | `/church/folio/` | `--ws-water` | `/church/`、`/church/visit/`、3D 導覽 | 原有中文藝術字形、活水、玻璃 |
| 西望雜誌 | `/journal/folio/` | `--ws-night`、`--ws-first-light` | `/journal/`、`/vol-00/` | 雜誌卷次、晨星、頁面節奏 |
| 以馬忤斯 | `/emmaus/folio/` | `--ws-first-light`、`--ws-papyrus` | `/emmaus/`、ONE | 經卷、蒲草紙、路加福音 24 |
| 橄欖山 | `/olive/folio/` | `--ws-olive` | `/olive/`、講員內容 | 講員海報、植物與等高刻線 |
| 黎明書局 | `/dawn-library/folio/` | `--ws-harvest` | `/dawn-library/`、完整館藏 | 書籍作品、書單、編輯策展 |
| 天堂電影院 | `/cinema/folio/` | `--ws-crimson` | `/cinema/` | 銀幕、影像策展、來源驗證 |
| 白晝咖啡館 | `/daylight-cafe/folio/` | `--ws-harvest`、`--ws-olive` | `/daylight-cafe/` | 七種出產、日常生活、餐桌 |

七個節點的順序與身份都由 `data/editorial/sevenfold.json` 控制，七個內容頁只提供 `editorial_key`、相同的 `layout` 和 OS 選擇，沒有可任意重排的獨立頁面 HTML。

## 三、共用設計組件

- `masthead`：真正克制的共用站名，沒有大型 Return 按鈕。
- `chapter-navigation`：七版塊完整序列，使用刊頭及章碼、當前標識；手機橫向卷軸而非硬擠。
- `folio-rail`：卷次、章碼與編輯頁眉。
- `identity-lockup`：Bodoni Moda／Small Caps＋Chiron Hei HK；教會中文字樣必須使用原有藝術成品，**不能重新打字**。
- `scripture-impression`：調用 **Scripture Studio V60** 已有中文豎排鉛字母版，使用真正 1:1 印面，於不同版塊繼承七重疊已有經文；外框承擔 OS 色彩與磨砂材質。
- `contents-index`：非等寬卡片的 1–4／1–N 編輯式行目錄，保留目的地真實鏈接。
- `editorial-spread`：跨頁敘事與已確認的藝術資產入口；未核對肖像、封面或片源不得擅自換圖。
- `colophon`：共同頁尾與原版塊返回路徑。

**非共用項目：** 教會 3D、各版塊既定 P2 動效、橄欖山講員肖像組、黎明館藏資料模型、天堂電影院片源驗證、咖啡館日課互動。這些仍由原有系統持有，只分享排版語法和受認可的接口。

## 四、實際程式與保護邊界

- **唯一資料母本：** `data/editorial/sevenfold.json`。
- **唯一頁面母版：** `layouts/partials/editorial/folio.html`，由 `layouts/_default/ws-editorial-interior.html` 掛載。
- **共用樣式：** `static/css/westside-editorial-interior.css`。僅在 `.Params.os_editorial` 路由載入，既有首頁／P2／正式內頁不受新的 CSS 污染。
- **原有經文鉛字：** `static/experiments/scripture-studio-motherform-live.html`；只新增 `layout=sevenfold-vertical` 的 scoped adapter，不改 V60 排版算法。
- **單一頁面資料：** `content/{realm}/folio.md`，共七份。
- **驗收入口：** `node scripts/editorial-sevenfold-contract.mjs`、`tests/editorial-sevenfold-browser.cjs`；瀏覽器保存桌面／手機的實際截圖供人工設計評審。

## 五、通過條件與失敗處理

必須七版塊 **7/7** 都可以在同一次 build 訪問，不能四頁成功就宣稱七頁完成。四頁（教會、以馬忤斯、橄欖山、黎明書局）完成深度編輯閱讀驗收，另外三頁（西望、電影院、咖啡館）必須同時通過可用的頁面、內容與視覺驗收，後者**不得標為僅規劃或空白佔位**。

技術方面核對 1440、390、320 CSS px、七節點導航、字體實際載入、經文豎排、正方形、文字完整、沒有裁切、沒有頁面橫溢。人工方面比較七個完整截圖的網格、留白、雙語節奏、顏色與材料識別；檢驗它們能否被認出是一套雜誌式網站，同時保持七種文化世界的獨立身份。**CI 全綠只代表技術通過，不代表已達獲獎水準。**

若有未審定的視覺或性能問題，保留 Draft PR 和預覽，不合併。待成套評審批准後再逐步以共享母版替換原有冗餘的第二、第三層靜態排版，不改已確認的 P2 場景與動畫。
