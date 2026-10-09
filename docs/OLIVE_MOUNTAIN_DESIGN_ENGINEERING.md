# 橄欖山｜版塊設計與 UI Scale 工程備忘錄

> 記錄日期：2026-10-09
> 狀態：設計探索與工程規範已記錄；**不代表已修改網頁、完成驗收或部署**。
> 適用：橄欖山講員長廊、講道系列頁、播放頁，以及其設計管理與響應式規則。
> 結構權威：`docs/MASTER_SITE_ARCHITECTURE.md`。本文件是**橄欖山講道介面的設計工程記錄**，不得自行改寫主站資訊架構。

## 一、探索背景與來源

使用者要求根據三張截圖重新執行「多雷探索」：
1. 以 Awwwards、Webby Awards、FWA 的獲獎級網站作為品質參照，從排版、留白、視覺層級、色彩、動效、微互動、響應式及原創性自檢與持續優化。
2. 「Astra · Skills Workspace」列出的候選設計資源，包括 awesome-design-md、black-white-ui-prototyping、brands-design-md、design-harness-components、flapkit、gsap、gsap-skillpack、image-to-ui-skill 等。
3. 同一工具列表後段的 mist、openui、personal-website-animation、polish、prototype、quieter 等。

這些是**探索候選**，並非已驗證或已安裝的依賴。引入任何第三方工具前必須核對原始來源、授權、維護狀態、效能成本及現有系統相容性。

### 原始三個網頁範例的追溯狀態

- **Aparelho**：有明確工程證據，PR #1077 描述「Aparelho-style visual preview」，並確認橫向編輯式人物長廊。
  - https://github.com/westsidewatch/westsidewatch.github.io/pull/1077
  - https://aparelho.com/
- **TED**：使用者提供的原始探索線索；講員、演講影片、系列與觀看流程值得研究。**尚未定位到當次探索發圖的原始記錄**。
  - https://www.ted.com/speakers
  - https://www.ted.com/talks
- **第三個原始網站**：尚未核實。**禁止以新找到的相似網站冒充原始第三例**。

Awwwards、Webby Awards、FWA 是**品質參照／案例搜尋來源**，不是已確認的「原始第三個網站」。

## 二、定位與設計結論

橄欖山講道介面不是一般影片列表，也不是普通講員資料庫；應是一個可觀看、探索、持續擴充的**編輯式講道影像館**。

設計融合：
- 義大利編輯式人物海報與大型視覺構圖；
- Aparelho 方向的橫向人物長廊、懸停／鍵盤焦點大型預覽；
- TED 方向的講員、系列、講道影片與觀看路徑；
- 獲獎網站標準下的留白、字體、動效、響應式、易用性及原創性。

### 三個介面層（本輪新方案；不是「原始三個網站」）

1. **The Speakers｜講員長廊**：十二位講員依既定出生年代排序；橫向編輯式人物海報；桌面懸停或焦點出現大型預覽；可進入講員與系列；手機使用原生橫向滑動。
2. **The Sermons｜講道劇場**：大幅 16:9 播放器；系列、集數、講員介紹、下一集形成連貫觀看流程；不支持嵌入時顯示明確外部觀看入口，禁止黑屏假播放。
3. **The Archive｜講道檔案館**：系列封面、主題索引、講員篩選與關聯內容；維持編輯視覺層級，避免無序縮圖牆。

以上是**設計提案**，不得擅自取代主站既有橄欖山總版塊與其正式子欄目。

## 三、十二位講員海報的不可破壞規則

- **永遠禁止拉伸字體**，不得使用非等比 `scaleX`／`scaleY` 改變字形。
- 已完成的十二張講員海報是既有設計資產；調整網頁 UI Scale **不得重新洗掉各張海報的獨立構圖**。
- 英文姓名（Bodoni Moda 等已批准字體）、中文極細字、人物、金色幾何裝飾各自保留原先的相對比例與圖層關係。
- 英文字號必須相對於**海報容器本身**，而非全局 viewport；優先採用 container query units／局部設計座標。
- 不得因縮放造成英文壓住「進入」、中文壓字、文字壓人物肩膀／衣服／手部或跨出安全區。已批准的特殊遮擋（如指定講員人物在文字前）依個別海報保留。
- 文字與人物遮擋必須是**受控圖層設計**，不是全站 CSS 的意外覆蓋。
- 海報外層容器可隨螢幕變化；海報內層構圖維持既定長寬比、座標與字圖關係。
- 不使用全頁 `transform: scale()` 作為響應式方案；不以全局 `vw` 控制海報內英文姓名。

## 四、唯一 UI Scale／設計權威

**一個全站設計管理工程，允許橄欖山局部調整。禁止另起第二套字體、顏色、CSS、動效管理系統。**

區分兩層：
- **外層 responsive layout**：viewport、長廊、卡片容器、間距、導航、播放器。
- **內層 poster coordinate system**：固定海報比例、字體相對尺寸、人物圖層、中文位置、幾何裝飾、個別講員覆寫。

不同設備：
- 桌面：大型海報、橫向拖曳／滾動、hover 與 keyboard focus 預覽。
- 平板：中型橫向長廊、觸控滑動、點按預覽。
- 手機：一張主海報並露出下一張；原生橫向滑動；點按進入；播放器滿寬 16:9。
- 支援 reduced-motion；不能因動畫阻斷閱讀、點擊、鍵盤導航或播放。

## 五、工具採用策略

- **GSAP／ScrollTrigger**：優先評估既有依賴能否滿足橫向滾動、轉場及響應式動畫；避免重複引入。
- **polish、quieter**：吸收設計檢查與降低視覺噪音的方法，不必安裝另一套框架。
- **awesome-design-md、brands-design-md**：借鑑設計語言文件化方法，整合到現有設計權威。
- **prototype、image-to-ui-skill、personal-website-animation**：僅作原型比較與特定實作候選；不得以原型直接覆蓋生產頁。
- **mist、flapkit、openui、design-harness-components**：無明確必要前暫不引入，避免額外依賴與第二套 UI 系統。

## 六、獲獎級品質驗收

1. **Composition**：十二張海報人物、字圖、遮擋、幾何裝飾均保留既定視覺比例。
2. **Typography**：英文不變形，中文極細字正確，沒有非預期重疊。
3. **Motion**：橫向移動順暢，預覽轉場不跳動，頁面不卡死。
4. **Navigation**：講員 → 系列 → 單集／播放路徑明確；滑鼠、觸控、鍵盤皆可用。
5. **Responsive**：桌面、平板、手機及瀏覽器 80%–150% 縮放視覺回歸。
6. **Playback**：可播資源實際驗證；不可嵌入資源顯示外部連結，不顯示假播放器。

## 七、完整工程節奏（避免拆成零碎補丁）

**階段一｜Authority Audit**：審查橄欖山現有 HTML／CSS／JS、設計 tokens、十二講員資料、正式規範與臨時覆蓋，定位真正控制 UI Scale 的規則。

**階段二｜三層版面整合**：在不改內容、既有 URL、十二張海報構圖的前提下，整體調整長廊、系列與播放介面的容器、比例、間距、預覽及導航。

**階段三｜唯一管理系統接入**：將局部比例、字體、色彩、動效參數納入全站唯一設計權威，保留頁面級覆寫，不建立平行系統。

**階段四｜Visual Regression Gate**：十二講員 × 多設備 × 縮放、互動、播放驗收；CI 與正式部署確認後才算完成。

## 八、實作與狀態紀律

- 本文件僅保存探索結論及工程規範，**未宣稱完成任何代碼修復、PR 合併或網站部署**。
- 後續每一輪工程必須更新本文件中的實際改動、commit／PR、驗收結果與剩餘問題。
- 原始第三個參考網站仍須追溯資料庫中的歷史圖片及當次多雷探索記錄；找到後補入此處，不可猜測。

## 九、2026-10-09｜第一階段實際啟動：Authority Audit

已直接讀取正式 `main` 的 `olive/index.html`、`olive/olive.js`、`layouts/olive/surface-carrier.html`。確認目前**同時存在兩個不同的橄欖山介面實作**：

- `olive/index.html`：獨立 `/olive/` 頁，內聯 CSS（大量累積覆寫）、三欄 speaker-grid、十二張 editorial poster，海報已採 `container-type:inline-size`、`aspect-ratio:3/4`、`font-size:var(--poster-size)`，另有黃淑華與賴若瀚的前景遮擋規則。
- `layouts/olive/surface-carrier.html`：Hugo 橄欖山 surface，首屏大衛鮑森 feature 與橫向講員 rail，與 `/olive/` 的獨立頁並非同一個渲染模板。
- `olive/olive.js`：保留十二講員 registry、獨立 editorialOrder、海報載入與系列導航。注意：JS 同時定義 birth chronology 和獨立 editorialOrder，**不可未經確認直接覆寫排序**。

**第一個核心風險：兩個 UI surface 的樣式與行為可能分叉；不得把修正其中一個誤報為整個橄欖山已修復。**

**第二個核心風險：現有 `olive/index.html` 在單一 inline stylesheet 內累積大量重複／`!important` 規則。後續須先建立樣式權威表，再集中清理，不應再補一層盲目覆蓋。**

已建立第一個自動檢查：`scripts/check_olive_scale_authority.py`，檢查 3:4、container query、poster-relative English typography、字體合成、reduced motion、海報來源與既定圖層；此階段**尚未改動正式頁面視覺**。檢查腳本需要 CI 執行確認，不能宣稱已 PASS。

工程分支：`design/olive-responsive-authority-20261009`。下一步在此分支統一兩個 surface 的 UI Scale 權威，先保護十二張海報，再做橫向長廊與系列／播放整合。合併前必須跑 CI、視覺與播放驗收。

## 十、第二階段進度｜共用 UI Scale 已接線（2026-10-09）

- 新增 `static/css/olive-ui-scale.css`：單一橄欖山**外層**比例 Token，包括 gutter、gap、canvas 與 Hugo 橫向 rail 卡片寬度；以響應式斷點管理桌面／平板／手機。
- `olive/index.html` 和 `layouts/olive/surface-carrier.html` 均已引入同一份 CSS，避免兩套 surface 各自設定外層 Scale。
- **保護邊界**：未改動十二張講員海報內部的 `--poster-*`、3:4 比例、英文相對字號、個別遮擋、JS registry、播放內容或 URL。
- 此輪**不是**完整視覺重構；兩個舊 stylesheet 的重複宣告仍需審計與移除。待 CI、瀏覽器截圖、播放驗收後才能合併。

## 十一、使用者確認的原始設計權威（2026-10-09）

**重要更正：大衛鮑森主視覺＋橫向講員長廊正是先前多雷探索選定並已實作的設計結果。這是應保留的正式視覺方向，不是待淘汰的舊設計。**

- **已批准的視覺基準**：`layouts/olive/surface-carrier.html` 的大衛鮑森沉浸式主視覺、橫向講員長廊、懸停預覽、系列進入動線。
- **必須整合的成熟資產**：`olive/index.html` / `olive/olive.js` 的十二張講員海報、英文相對尺寸、中文字體、各人物遮擋和系列內容；不得重做或失去這些資產。
- **單一渲染權威目標**：完成實際路由與部署映射審計後，將兩套重複實作整合；不能先刪獨立頁而導致 `/olive/` 或系列頁 404，也不能把新建的三層設計提案凌駕於已批准的主視覺上。
- **工程糾偏**：先前將兩套頁面共用 UI Scale 只是過渡接線，不是兩套永久並行的設計方案。PR #1234 在完成整合與驗收前保持 Draft，不合併。

## 十二、最終整合決策｜一套設計、三個體驗層、十二講員資產（2026-10-09）

**使用者正式確認：橄欖山不得出現兩套、三套設計。僅保留一套完整設計系統。十二位講員既有頁面、海報與字圖關係屬正式版塊資產，必須原樣保護並整合進這套系統。**

### 唯一整合形態

1. **The Speakers｜講員長廊（首頁）**：原多雷探索成果——大衛鮑森沉浸式主視覺與橫向講員長廊；十二張既有講員海報直接作為長廊正式資產，不重新設計、不重製字圖比例。
2. **The Sermons｜講道劇場**：由講員導入系列、集數、單集播放器；維持清晰的返回講員與下一集路徑。
3. **The Archive｜講道檔案館**：系列、主題、講員索引與歷史館藏；沿用同一視覺語言與資料權威。

**三層是同一體驗的三個內容層級，不是三套模板、三套 CSS、三個網站。**

### 不可破壞與去重原則

- 保留十二位講員已完成的海報、人物遮擋、字體比例、局部設計座標、對應講員頁與既有內容 URL。
- 不再讓 `olive/index.html` 和 `layouts/olive/surface-carrier.html` 各自維護獨立的橄欖山首頁設計。先審計正式路由／建置輸出，確認單一生產入口，再移除或轉接重複入口；不得造成 404。
- 字體、顏色、尺寸、動畫採全站唯一設計管理權威；橄欖山僅保留局部 token，不能另建平行系統。
- 先完成單一頁面／資料／導航整合，之後才進入視覺微調；禁止為十二張海報重寫獨立 CSS。

### 工程狀態

此節是已批准的設計決策，**不代表三層整合已完成或部署**。PR #1234 保持 Draft，待單一生產入口整合、回歸測試與視覺驗收。

## 十三、第三階段實作｜原橫向長廊接入十二張海報（2026-10-09）

- 新增 `static/js/olive-editorial-rail.js`，由原 `layouts/olive/surface-carrier.html` 的既有橫向講員 rail 讀取 `olive-editorial-covers.v1.json`；以既有講員名稱映射到十二張 `/images/olive/*.png`。未新增第二套頁面或第二套講員內容來源。
- `static/css/olive-ui-scale.css` 新增海報圖像適配：原圖 `object-fit:contain`、不拉伸；海報圖片載入成功後隱藏原 rail 的重複文字；保留按鈕、講員路由、鍵盤焦點與原有動畫。
- 原 Hugo surface 已載入 adapter；原大衛鮑森主視覺、影片互動和講員 rail 不替換。
- **限制**：目前僅完成源碼接線，尚未取得瀏覽器視覺截圖、CI PASS 或部署結果；長廊尺寸／裁切效果需視覺驗收，且 The Sermons／The Archive 仍未完成一體化。

## 十四、完整階段｜單一三層導航與資產整合（2026-10-09）

本輪已實際提交：
- `static/js/olive-journey.js`：以既有大衛鮑森主視覺與橫向長廊為 The Speakers，向同一 Hugo surface 添加 The Sermons 與 The Archive 兩個內容區塊和三層錨點導航；保留既有講員按鈕路由。
- `static/css/olive-ui-scale.css`：統一三層的 spacing、字體 token、色彩 token、桌面與手機佈局；講道劇場目前為 16:9 的導覽／說明面板，**不是第二個影片播放器**，播放仍由原主視覺承擔。
- `layouts/olive/surface-carrier.html`：引入 journey adapter，不重建原主視覺。
- `scripts/check_olive_scale_authority.py`：增加原主視覺、三層接線、十二張海報 manifest 的靜態檢查。

**仍未完成／不可宣稱：** 這輪尚未執行 CI 與瀏覽器視覺驗收；Hugo surface 和獨立 `/olive/` 的實際部署路由尚未統一，原獨立頁 CSS 去重也尚未完成；The Archive 目前是既有系列索引入口而非新建完整館藏索引；The Sermons 尚未有獨立集數播放器與播放可用性驗證。PR #1234 繼續保持 Draft，禁止在上述缺口未核實前宣稱上線。

## 十五、單一首頁路由修復（2026-10-09）

**定位到確切衝突：** `hugo.toml` 把 `olive/` 掛載到 `static/olive`，會把 `olive/index.html` 與 `content/olive/_index.md` + `layouts/olive/surface-carrier.html` 的 Hugo 生成首頁放在同一輸出路徑。原先兩套首頁不是純視覺問題，而是建置輸出權威衝突。

**已提交修改：** 在 `hugo.toml` 的 Olive mount 設定 `excludeFiles = ["index.html"]`，保留其他 `olive/` 子頁、JS 和資產，令 `/olive/` 唯一首頁由 Hugo surface 生成；將三層導覽中指向已退出生產首頁的 `/olive/#olive-series` 錯誤錨點改為有效的本頁講道入口；回歸檢查加入 Hugo 唯一路由和舊連結防退化。

**重要未驗收項目：** 需要實際 Hugo build 確認輸出 `public/olive/index.html` 包含 Pawson hero，且 `public/olive/olive.js` 與十二講員子頁仍在；需瀏覽器核實長廊及播放器。舊 `olive/index.html` 保留作未部署的來源資產，不是第二個正式首頁；後續可在完成內容遷移後清理。PR 繼續 Draft。


## 16. 沉浸式影片首頁預覽權威（2026-10-09）

- 首頁是 **video-first** 播放場景，不以講員人物海報代替影片預覽。依序載入 YouTube `maxresdefault.jpg` → `hqdefault.jpg` → 已批准的 `/images/olive/{speaker}-editorial.png` 後備。
- 排除 YouTube 回傳的極小佔位圖；預覽圖與當前影片使用同一個 `featured[index]` 來源。點擊播放才載入 `youtube-nocookie` iframe。
- `NEXT FEATURE` 同步切換講員、影片名稱、預覽圖、播放器來源；現有第一批為大衛鮑森四段、江秀琴一段、劉彤一段。未經核實不得宣稱所有來源均可嵌入播放。
- 長廊的十二張已批准人物海報獨立存在，保持原始字形、構圖與比例，不以影片縮圖替換。
- 尚待瀏覽器實測：每段影片縮圖解析度、嵌入可播放性、手機布局、鍵盤導航、輪換後播放器是否對應、fallback 是否正確。Draft PR #1234 在通過前不得合併。

- 播放後備：沉浸式主視覺提供隨當前影片同步更新的 `WATCH ON YOUTUBE` 官方來源連結；嵌入播放不成功時，使用者仍能前往影片來源。外部來源連結不是站內播放成功的證明。
