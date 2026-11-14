# P2 04 / OLIVE — V78 多雷探索：成熟翻卡、捲動平滑及植物背景

日期：2026-11-08。狀態：研究與**隔離動效試稿**；未改動正式 01–03、已鎖定 12 張講員正面及 04 主體翻卡。所有工程試稿仍在 Draft。

## 0. 問題與不可破壞的合約

- 使用者指出：目前終場植物背景由很亂改到太少。新目標不是「葉子越多越好」，而是**疏密有致的雕刻版面**：兩組主枝承接左下／上方，約三組次枝在版面外緣穿行，局部橄欖果實與細刻線補充，卡片間的留白不灌滿、不得遮蓋原版海報和主標。以上是藝術方向，不能把圖像生成參考說成已接入 SVG 工程。
- 翻卡：保留已核准 3:4 原圖、所有英文字排版 Shadow DOM、中文、雙實體卡、左右交替、六個正反面編號、十二講員終場，原本 P2 捲動契約 `scrollY → d → 唯一幾何 pose`。
- 《WESTSIDE-EDITORIAL-MANUAL.md》 §9：多雷探索是對外研究及技術選型，不是 Gustave Doré 風格。八準則：全網、開源、成熟、免費、輕量、可維護、先複用、回 Doré Core。
- 《MASTER_SITE_ARCHITECTURE.md》 §11：**滾多少走多少、停手即停、反向即回**；禁止時間滯後追趕、無關新 RAF／第二時鐘。可以用位置函數 easing；不得用延遲補丁遮掩效能問題。
- 所有「獎項」字樣只表示藝術目標。瀏覽器截圖與手感測試不可由 CI 綠燈代替。

## 1. 當前 V77 翻轉的真正技術診斷

- `static/js/p2-0104-olive-continuation.js`：`T.pairStart=11.95, indexStart=20.20`，11 次接續，每個事件約 **0.75 個視窗高度**。
- `entering=ease((beat-.04)/.44)`，`retreat=ease((beat-.55)/.40)`：每張牌的 180 度幾乎都集中於一個事件約 40–44% 的距離。於 844px 手機高度約 253–279px 捲動完成 180°，滑鼠捲輪很容易直接跨幀，這是**設計時距偏短的確定事實**，不能把它說成已量得 60fps 掉幀。
- `turnFace` 每幀重設 `transformOrigin` 和 `perspective(px) rotateY(deg)`；同期 `measure()`、`position()`、`setFigure`、6 個植物印次和 64 條背景路徑透明度也在同一 `paint()` 路徑更新，具有可能的主執行緒負載。
- `setFigure` 大部分幀有 speakerIndex 提前退出，但事件切換時仍替換圖片來源及凍結字體 Shadow DOM；需在實際瀏覽器抓 `Long Tasks` / transform 軌跡，不能猜已確認掉幀。
- 兩面目前由一個 rigid carrier 旋轉，符合歷來用戶對「不要把正面文字拆開／失真」的保護；**不要回退到三層各自旋轉**。

## 2. 世界成熟範例與可合法採用的技術

| 來源 | 可複用之處 | 授權/成本 | 資源與風險 | V78 選擇 |
| --- | --- | --- | --- | --- |
| **FLOT NOIR / MERSI 2026** https://tympanus.net/codrops/2026/07/27/between-print-and-digital-the-making-of-mersis-website/ | 單一 scroll float 同步正反遮罩與中間題字，入內過場 `Flip.fit`；手機縮減複雜 flip | 案例與解說可讀，案例本身不是可任意複製的資產；底層 GSAP 依其 standard license | 非所有轉場都用 3D；它是現有 P2 自己引用的原始參照 | **首選設計原則**，不挪用專案原程式 |
| **Eduard Bodak / Codrops 2025** https://tympanus.net/codrops/2025/07/29/built-to-move-a-closer-look-at-the-animations-behind-eduard-bodaks-portfolio/ | 說明真實 front/back 3D 卡、離場與回轉分階段；結合滾動 | 公開教學，非整個網站公開 MIT 的證明 | 不要模仿花哨的浮空、滑鼠追逐與多個自主時計 | **卡體與節奏參照** |
| **Codrops 3DStackMotion 2024** https://github.com/codrops/3DStackMotion | 自主可部署 3D 構圖 / GSAP scroll 卡片分層 | 專案**MIT**；底層 GSAP 另有官方授權 | 例子偏 NFT、卡堆，表演性強，需簡化 | **工程示例，拒絕直接套視覺** |
| **Codrops ScrollBasedLayoutAnimations 2026** https://github.com/codrops/ScrollBasedLayoutAnimations | ScrollTrigger + Flip 改變圖卡布局，與十二人終場相關 | 範例專案 **MIT**；GSAP 自己 standard license | 布局重排思想有用，但 P2 現有十二人座標系不可直接替換 | **作十二卡結尾參照** |
| **Motion for JS** https://github.com/motiondivision/motion 與 https://motion.dev/docs/scroll | `scroll()` 直接綁 scroll，支持瀏覽器 ScrollTimeline；Motion 本體 **MIT**、公開 API 免費 | 免費核心 MIT，另有可選 Motion+ 付費資產（**不需要**） | 若新套件與 P2 原 JS 同時寫 transform 會衝突；不要使用 spring 值延時追蹤手勢 | **可選 adapter；不是目前必要依賴** |
| **GSAP ScrollTrigger** https://gsap.com/docs/v3/Plugins/ScrollTrigger/ | 時序編排、scrub、snap、單控制器 | GSAP 官方 standard 「no charge」條款；**不是 MIT**，需逐項遵守 | `scrub:0.5` 的「追趕」違反手冊 §11；雙控制器會互相覆寫 | **僅比較，不直接裝到主 P2** |
| **Lenis** https://github.com/darkroomengineering/lenis | 原生滾動上的滑順處理 | **MIT**，免費 | 官方列出 iframe wheel 不轉發、Safari 低功耗幀數、主執行緒負載等限制；P2 含 Emmaus iframe | **目前不採用**，不以改滑輪手感掩蓋事件過快 |
| **原生 CSS 3D / ScrollTimeline** https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/backface-visibility 及 https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations | `perspective`, `preserve-3d`, `backface-visibility`；捲動直連 compositor 的時間線 | 瀏覽器免費標準，零外部相依 | `animation-timeline` 瀏覽器版本差異需檢驗；iframe 場景原已有 single authority | **先採**，原生 3D + 不改時鐘 |

以上所有開源套件**未宣稱已安裝到 P2**。非 MIT 的 GSAP、網站案例、作品圖像需分別遵守原本授權，不把公開教學等同公共領域。

## 3. 現代翻卡設計提案（先隔離原版比對）

**A / Museum Folio（首選）**：一張真正厚度可感的印刷卡，中心 Y 軸、不傾斜，正面原講員海報完整；90° 邊緣位置只顯示薄金色紙邊，翻過去是可辨認的植物／地形完整版畫。單事件的「翻＋停＋另一側翻」以**相同捲動值**逐段控制，不另啟動畫，卡片寬高不在動效中改變；永遠可逆。重點研究更多**實際 scroll distance** 而非 `scrub:0.5`。

**B / Printed Leaf Hinge**：卡片繞靠外側 3D 軸緩緩打開，再回到原對開格位；另一側保持穩定，適合左右海報的「先右後左」。軸心與海報原位置不一致會造成原稿平移，需額外幾何校正。可隔離測試，不能直接替換已核准正面。

**C / Editorial Split Reveal**：完全不做 3D，一個實體卡封面與背面由左右相反方向的遮罩一進一出，配合細金線壓印。非常平滑且可回退；但若失去「確實翻卡」的物理敘事，需要用戶判斷。MERSI 的非 flip 主過場是此方案成熟技術參照。

## 4. 建議下一步的實作順序

1. **不先引入新庫。** 先做單檔隔離動效 proof：V77 原來的快翻、A 中心軸更長行程、B 書葉外側轉軸、C 版畫遮罩過場，全部用同一手勢／滑桿及相同 3:4 示例卡測試（示例卡不假冒正式十二位的原始文字）。
2. 對照 1648、390、320 實際滾動 10/30/60px 的 pose、回退幾何與卡片是否出現背面斷層；快速反向、停止、鍵盤、prefers-reduced-motion 和 Firefox/Safari（如環境允許）。
3. 移植選定姿態函數到現有 `turnFace`，保留基準字型、攝影海報、十二人排列和一個 `paint()`。使用 `performance.mark/measure` 或 Playwright trace 識別 layout/repaint，先減少同一 scroll frame 的樣式寫入，不用新的 RAF 追趕。
4. 植物背景的設計：中等偏豐富、邊緣完整枝葉與局部果實，保留講員卡縫和視覺核心的呼吸；**先作 SVG 母本並並排比對，最後才裝進實際背景**。禁止直接把 AI 產生的參考圖貼作網頁背景。

**決策**：首選 A + 原生 CSS 3D；C 作穩定降級方案；B 作創意備選。Lenis 與 Motion.js 皆非立即必要，GSAP 可作技術參照，暫不新增 JS 依賴。這份比較受 Design OS 的唯一 scroll authority 約束。
