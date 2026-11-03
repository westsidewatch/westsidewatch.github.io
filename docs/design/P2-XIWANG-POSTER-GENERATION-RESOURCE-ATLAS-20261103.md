# P2《西望》Poster Generation Resource Atlas｜海報生成資源多雷探索

**研究日期：2026-11-03。範圍：多輪外部資源＋開源程式、設計案例、實際原始碼／授權核驗。狀態：僅研究入庫；不出圖、不改 P2、不新增 Runtime。**

此文是現有 **Design OS Editorial Manual** 的補充研究，不建立第二套設計系統。最新人工決策始終優先：**A 僅一組「西」「望」豎排，重新製作全新字骨，不沿用被淘汰的任何既有西望 SVG；B 七組正立「西望」在同一畫面內疊合，七組有各自刻線及版塊色，刻線僅存在字內，背景不鋪紋。** 02 雜誌右側已定稿 5:8 封面及首頁七重折疊等現有動效不改。

## 1. 回讀手冊：已存在、應重用的參考

- **視覺參考**：[Recent](https://recent.design/)／[Siiimple Magazine](https://siiimple.com/category/magazine/)／[Siiimple Typography](https://siiimple.com/category/typography-2/)／[Cosmos](https://www.cosmos.so/)：找版式、比例、字形尺度及當代感，並非開源圖稿。
- **大型文字空間動效**：[Codrops KineticTypePageTransition](https://github.com/codrops/KineticTypePageTransition)／[SuperfluidLayout](https://github.com/codrops/SuperfluidLayout)／[FullscreenLayoutPageTransitions](https://github.com/codrops/FullscreenLayoutPageTransitions)：原 [動態字體參考](WESTSIDE_MAGAZINE_KINETIC_TYPOGRAPHY_REFERENCE.md) 已收錄，僅借機制，不重新創造一個動畫系統。
- **義大利雜誌／印刷文法**：[Italian Editorial Executable Grammar](../dore/italian-editorial-executable-grammar.v1.md)、[New Westside Visual Reference System](../../dore-design/new-westside/VISUAL-REFERENCE-SYSTEM.md)、[Visual Grammar](../../dore-design/knowledge-lab/skills/new-westside-editorial-web/references/visual-grammar.md)：紙／墨／刻線密度與視線主次；字本身應成為主題，不用圖案填補設計不足。
- **SVG 技術**：[SVG Exploration List](SVG-EXPLORATION-LIST.md)：SVG.js、SVGO、Motion、Flubber、Chrome repaint／性能基線。純 SVG 可直接進 P2，沒有必要複製另一個運行框架。
- **圖形字骨研究**：[A 多輪製字探索](P2-XIWANG-A-MULTIROUND-DORE-EXPLORATION-20261103.md)、[A/B 開源工具對照](P2-XIWANG-A-B-OPEN-SOURCE-CODE-EXPLORATION-20261103.md)：KAGE Editor、Kumiko、FANGCUN、Graphite、Inkscape、skia-pathops、penfill 等仍按最新的「全新字骨＋疊合刻線」藝術規範研究；不因新 poster tool 看起來強大，就推翻原創字形要求。

## 2. 第一輪新增：可重複輸出完整海報的開源引擎

| 資源／原始碼 | 經核對能力、授權與限制 | 對《西望》取捨 |
| --- | --- | --- |
| **[flowshape](https://github.com/Jossifresben/flowshape)**；[poster composer 規格](https://github.com/Jossifresben/flowshape/blob/main/docs/poster-composer.md) | **MIT；2026-10 最近 repo push；新專案，尚無大量社群實證**。官方說明 40 個 deterministic pattern generators；poster composer 把 layout 寫成資料（artwork/title/data/decoration regions、比例區間、相對 split），一個 render＋validator 生成多候選；具 8 個骨架／A3 下 68 個合法變體、URL state／seed、純 SVG export、字長與長寬比驗證、色彩角色。原始碼、docs/architecture.md 與 docs/poster-composer.md 已實讀。 | **第一優先研究架構**：用於 A/B 左頁 1:1 版式候選及自動幾何驗證；借其 layout data、seed、SVG node tree、overrun rejection，而不是套用它的現成背景圖案／文字模板。**此專案不是能獨立完成原創 CJK 字骨的工具。** |
| **[Poster / poster-ai](https://github.com/Michaelliv/poster)**；[README](https://github.com/Michaelliv/poster/blob/main/README.md) | **MIT；2026-05 push**。單 TSX 來源，以 CLI／SDK 輸出 HTML、PNG、PDF、SVG 等；官方文件稱 PNG 預設 Takumi；SVG／PDF 要 Chrome engine。含示例和尺寸可重複導出。 | **候補輸出層**：適合定好字稿後批次製作多種海報尺寸及右封面對頁；不要把 TSX 模板當成現代中文字海報的藝術品質保證。 |
| **[Satori](https://github.com/vercel/satori)** | **MPL-2.0；2026-10 push；成熟且有活躍社群**。把 HTML/CSS 轉成 SVG，通常將字轉 outlines；需提供包含繁體字的已授權 font。 | **候補排版編譯器**：小字刊次／宣傳 metadata、外部分享縮圖可以用；不是一個造「西望」新字骨的生成器。 |
| **[Typst](https://github.com/typst/typst)** | **Apache-2.0；2026-10 push**。成熟的編程排版系統、印刷頁面／PDF 輸出。 | **紙本海報與多頁出版分支**，不必進 P2 原生 SVG runtime。 |
| **[Paged.js](https://github.com/pagedjs/pagedjs)** | **MIT；2026-10 push**。CSS Paged Media、書冊與 print-to-PDF 頁面管理。 | **列印後期可選**，不適合造兩個原創字骨。 |

**重要借鑑（flowshape）**：一張「生成的海報」不應只是隨機大字放上去，而是由**可驗證的版面規則**篩除不合法構圖。把候選布局作為資料，不寫一大堆互相衝突的 CSS 變體；SVG 輸出必須可重現（相同 seed 輸出相同 path），小屏過度擠壓要拒絕版式，而不是任意縮小到不可讀。

## 3. 第二輪新增：原生向量線場／刻線的生成庫

| 資源／原始碼 | 實際特性／授權 | 對 A 或 B 的價值 |
| --- | --- | --- |
| **[canvas-sketch](https://github.com/mattdesl/canvas-sketch)** | **MIT；2026-06 push**。JavaScript generative art／CLI，提供 SVG/d3 與 penplot SVG 的實際示例；可快速做 seeded geometry 與調參。 | **B 的離線線場實驗台**，控制密度、結構、輸出；生成刻線後仍須對各自字形的外輪廓與字內孔洞精確裁切。 |
| **[p5.plotSvg](https://github.com/golanlevin/p5.plotSvg)** | **MIT；2026-10 push**。有完整示例的 plotter-friendly SVG path export；清楚限制：不支持一般填充、濾鏡、漸層、pixel images 等完整畫面語法。 | **B 的線段導出候補**；不適合獨自做 A 的幾何實心字。 |
| **[generative-poster](https://github.com/clawmaks/generative-poster)** | 2026-05 push；repo 有真實 Vite/p5 原始碼、15 種生成器（parallel hatch、crosshatch、contour、flow、noise、Voronoi、Bezier 等）；**已查 Git tree 沒有 LICENSE**。 | **讀算法分類／試驗路線，不複製程式碼**：公開 source ≠ 授權使用。須作者另行授權才能納入本站的程式。 |
| **[Graphite](https://github.com/GraphiteEditor/Graphite)** | **MIT/Apache-2.0；2026-11 仍更新；現為 alpha**。可視化非破壞性 node-based 向量形變與合成。 | **A 幾何重構**的操作工具候選。先做新的 CJK 構件，Graphite 才能研究楔形、弧面、字內白；不因工具能幾何變形就能交付好字。 |
| **[d3-shape](https://github.com/d3/d3-shape)** + **[d3-contour](https://github.com/d3/d3-contour)** | ISC；成熟 JS 曲線、等值線引擎。 | **B 每層不同方向場**，線段真正留在字形內而非字外填滿背景。 |
| **[penfill](https://github.com/piLeoni/penfill)** | MIT/Apache-2.0 的較新研究候選；以帶 holes 的 Region 配對 zigzag、concentric、waves、sunburst、stipple 等線場。 | **特別值得和 B 疊合構圖組裝驗證**；先實測極窄中文筆畫／字洞，不能直接宣稱已穩定進站。 |
| **[skia-pathops](https://github.com/fonttools/skia-pathops)** + **[SVGO](https://github.com/svg/svgo)** | BSD-3-Clause ＋ MIT；維護中的布林／SVG 優化工具。 | **離線收尾**：對外輪廓與 inner counters 作布林可靠性驗證，然後在不破壞 transform/pattern/ID 的前提下優化輸出。 |

**B 的警戒線**：所有線條只在字內，沒有背景紋／放射線延伸到字外。七組「西望」必須是 **7 個 0° 旋轉的正立字組，在同一中心構圖疊合／錯位印版**，不可做成七排橫向色卡，也不能沿用被否決的 A 字骨重複七次換色。這些引擎只處理線條及佈局，不取代七個字組的原創設計。

## 4. 第三輪新增：完整海報編輯器（重要，但不建議嵌入 P2）

| 資源 | 授權／功能／體積 | 判定 |
| --- | --- | --- |
| **[yft-design](https://github.com/dromara/yft-design)** | **MIT；2026-09 push**。Vue3/Fabric.js 的線上 poster editor，具 SVG／PDF／圖片匯出；README 明記 SVG 匯入 tspan 等限制，Demo 與商業 Pro 需區分。 | **借圖層與匯出工作流程**，不引入整個 Canvas editor 作 P2 依賴。 |
| **[Doory](https://github.com/shaongitbd/doory)** | **Attribution Assurance License，非標準 MIT/Apache**；2026-11 更新，包含前後端及 DB。已讀 LICENSE：對 redistribution/運行有署名與通知要求。 | **不採用**：與只需兩張原生 SVG 海報的工程相比，部署成本及特殊授權義務不值得。 |
| **[Poster Maker](https://github.com/dabodamjan/poster-maker)** | MIT；Claude Code 等代理工具驅動 HTML/CSS poster，可能涉及外部付費模型/訂閱。 | **僅借真實 Chrome 截圖迭代驗收方法**；不用付費生成依賴。 |

## 5. 第四輪新增：成熟海報作品庫（可以研究，不能直接複製）

| 設計參考入口 | 為何更適合《西望》 | 許可邊界 |
| --- | --- | --- |
| **[typo/graphic posters](https://www.typographicposters.com/)** | 專門策展的字體／圖形海報庫；聚焦「字即海報」，能比較巨字、獨特筆畫、疏密、重複與印刷處理。優先於一般 SaaS/UI 設計庫。 | 原作有各自作者／著作權，不是可直接抓進 P2 的 SVG 字型來源。 |
| **[Letterform Archive](https://letterformarchive.org/online-archive/)** | 有原件年代、設計師、材質／雕版／印刷細節；為 A 的新字骨和 B 的套版／刻線關係提供真實歷史證據。 | 公開研究不等於允許重製。 |
| **[Design Reviewed Archive](https://designreviewed.com/archive/)** | 8,000+ 作品，包含海報、字體標本、刊物與工業設計；適合看廣告海報如何以單一元素取得遠距辨識度。 | 逐件追蹤作者、年代、來源與權利。 |
| **[HMCT Archive](https://hmctartcenter.org/archive)** | 有 April Greiman、Armin Hofmann 等設計師的實物字體／海報資料。適合研究字體作為主要構圖。 | 館藏研究用途。 |
| **[Poster House](https://posterhouse.org/)** | 專門的海報博物館，區分廣告宣傳、藝術展示、印刷技術與當代設計。 | 展覽圖片並非可用素材。 |
| **[Fonts In Use](https://fontsinuse.com/)** | 對照真正發表的海報所使用字體、版式及字標關係；特別適合判定 A 是否還像普通字庫。 | 字體及原作需要各自授權。 |
| **[Type Directors Club](https://tdc.org/)** | 當代字體／lettering 的競賽與優秀案例，觀察整體視覺與可讀性。 | 只借原理，不照抄原作。 |

應按「**設計師／原作／日期／獨特造型機制／字形結構／主次與留白／可借的抽象規則／失敗風險／Westside 應用**」做案列紀錄，而非保存無署名參考圖。與本來的 Recent／Siiimple／Cosmos 串聯：前者找**專業海報字形**，後者找**數位雜誌的出版與互動表達**。

## 6. 一項真正值得做的小型、可重複試驗（尚未執行）

**A**：新做真正的「西」「望」字骨後，建立至少三個**布局機制明顯不同**的 1:1 poster composition record（滿版頂天立地、異常留白／軸線、字與封面邊界共享軸線），從排版規則而非更換顏色來比較。原創字骨本身要優於已否決的 A2，否則不進入版式評價。

**B**：獨立構造 7 層正立字組，每組由不同的 path/line 算法與 OS 版塊色生成，統一進一個正立的**重疊刻線字海報**。使用幾何 / counter-path 裁切，不在背景生成任何紋理。比較同軸精準套印、受控微位移及由深到淺的層疊秩序；不可退回七排色條。

**共同渲染**：只在 build-time 使用候選庫，最終交付單一可審查、可編輯 native SVG，仍由 P2 現有 scroll / sevenfold 進場顯示。驗收 1648、768、390、320px／200% zoom／reduced motion／反向捲動，對照原封面。版式以原手冊 10 項 0–2 rubric、15/20 探索門檻；build/CI 通過不是藝術定稿。

## 7. 授權與研究結論

**優先級**：海報 composition/測試架構首選 flowshape（**借原理**）；離線 SVG 生成 canvas-sketch／d3；向量形變 Graphite + PathOps；字形源仍先通過 KAGE/Kumiko/FANGCUN／新字骨試驗；產出後才考慮用 Poster 或 Satori 自動適配印刷／網路尺寸。

**嚴格禁止**：直接複製無 LICENSE 的 generative-poster 代碼；將 Doory 的特殊授權方案當 MIT；把公開的海報圖作可再發布字稿；導入需要付費模型 API 的 runtime；為了工具而新增 OS／前端編輯器／渲染時鐘。

**核驗範圍**：GitHub repo 元資料（license、push date、tree）＋選定上游 README、poster-composer.md、architecture.md、LICENSE；入庫不等於安裝／測試完成，更不等於視覺已通過。

**本輪結束狀態**：僅完成更大的有來源之工具及海報作品庫探索，沒有修改現有 Poster A/B 的 SVG、CSS、JS 或 P2 封面。