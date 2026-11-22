# 黎明書局 P2 05｜多雷探索：圖像策展、封面牆、分類與閱讀

日期：2026-11-22｜研究狀態：**已查核公開案例與技術文件；尚未安裝或進行新一輪視覺實驗**。

依據：`docs/design/WESTSIDE-EDITORIAL-MANUAL.md` §9 Doré Exploration、§11 公開文案隔離，以及 `docs/design/DAWN-P2-EXHIBITION-CONTRACT.md`。本檔是内部研究記錄，**不得顯示到公開書局頁面**。

## 現況與不可破壞的邊界

- 現況：三晨星／策展集／光譜 2×2 大卡曾被金框、暗色遮罩與細線切割；目前紙質題簽方案仍需實際藝術驗收。
- 真實館藏入口必須為圖像分類牆而非只有網址參數可見的清單，主類→子類→書→原分類返回不可斷。
- 既有知識分類：7 主類、42 子類、8 個欄位；中文圖書是單獨的原始 47 部分類集合；2 萬餘筆全部書目未完成逐冊學科映射，不得偽稱其實已被精確標引。
- 書封、圖版的圖像身份必須同書同來源。不能拿其他書的插圖冒充本書，不能一律造黑色封面。
- 絕對禁止新黑金視覺；不動 OS tokens、已批准 V9、P2 01–04、原始館藏、正式主站或 ChatGPT Sites。只在 GitHub 隔離分支施工，Cloudflare 預覽。

## 15 個真實案例：獎項與實際用途分開標明

| # | 案例、研究 URL | 可確認的地位 | 可轉移的設計機制 | P2 對應 / 選擇 |
|---|---|---|---|---|
| 01 | Mosby's Files · https://www.mosbyfiles.com / https://tubikstudio.com/works/mosbyfiles | Tubik 官方案例列 Awwwards SOTD、Developer Award、FWA of the Day | 用文件夾的物理結構表示學科分類；CSS 夾層，分類不退化為平面表 | **採 IA 原理**；不採其深色首頁或仿真紙夾 |
| 02 | Creative Reference Library · https://crl-2026.webflow.io / https://animorio.com/en/journal/creative-reference-library-how-its-made/ | 2026-11-10 Awwwards SOTD、Developer Award（第三方技術拆解，需以獎項頁複核） | 精選作品的輪轉展示、極大字與明確分類、動效有整體語法 | **採策展節奏**；不採黑色畫面、WebGL 大字、897KB 的動畫負擔 |
| 03 | Rijksmuseum Online Collection · https://www.rijksmuseum.nl/en/about-collection-online / https://www.q42.nl/en/work/rijks-website1 | Q42 列 GLAMi Gold、European Design Gold、Lovie 等 | image-first 原作、多解析度裁切、故事層與原件層分工 | **最高優先：三欄目大卡與單書圖像** |
| 04 | Pell Mell · https://tympanus.net/codrops/2026/03/27/pell-mell-crafting-a-visual-exploration-platform-with-editorial-rhythm/ | Codrops 2026 技術案例；本研究未認證其獎項 | 克制 UI、嚴謹底層網格、IntersectionObserver、惰性圖像 | **最高優先：整體封面牆節奏** |
| 05 | Public Domain Image Archive · https://pdimagearchive.org/about/ | 公共領域圖像策展標竿；未以獎項為依據 | Catalogue / Infinite / Shuffle 三種檢索視圖；書內圖像裁切與原始權利鏈 | **最高優先：隨機封面牆＋缺封面的書內插圖** |
| 06 | The Public Domain Review · https://publicdomainreview.org/collections | 成熟編輯出版機構；未以獎項為依據 | 用作品媒材與深度敘事組織策展入口 | **採三晨星／策展集文案與作品關係** |
| 07 | Standard Ebooks · https://standardebooks.org/ebooks | 開源公共領域電子書製作平台；未以獎項為依據 | 真的封面、原書、版權、文字排版同時成立；作品頁細節 | **最高優先：書封身份與封面到閱讀連續性** |
| 08 | Wellcome Collection · https://wellcomecollection.org/collections / https://developers.wellcomecollection.org/api/catalogue | 公共館藏與 API 標竿 | 分類層、圖片／書／檔案共用工作 ID、subjects/languages 等 facets、IIIF | **最高優先：七主類／中文類／逐冊著錄的分離** |
| 09 | V&A Explore the Collections · https://www.vam.ac.uk/info/explore-the-collections/ | 大型館藏標竿；未以獎項為依據 | 主題瀏覽、圖片優先搜尋、作品 metadata 與來源 | **採館藏搜尋與分類篩選的界面** |
| 10 | The Met Open Access · https://www.metmuseum.org/hubs/open-access | 博物館開放資產標竿；未以獎項為依據 | work ID、CC0 元資料、對應原作高解像圖 | **採缺圖修復之來源和權利核對方法** |
| 11 | Art Institute of Chicago · https://api.artic.edu/docs/ | 開放 API + IIIF 技術標竿；未以獎項為依據 | artwork image_id、IIIF 自選尺寸、歸屬 metadata | **採響應式封面原尺寸與深讀圖版** |
| 12 | NYPL Digital Collections · https://api.repo.nypl.org/ | 大型圖書館數位收藏標竿；未以獎項為依據 | 從集合／館藏到單件作品與影像、身份標識、權利 | **採書目→原作影像→閱讀／來源的路徑** |
| 13 | Europeana Collections · https://www.europeana.eu/en/collections | 跨機構文化遺產瀏覽標竿；未以獎項為依據 | 主題／世紀／機構多軸導覽與有資料來源的集合 | **採 facets，不將「相關」誤作正式標引** |
| 14 | Getty Research Collections Viewer · https://www.getty.edu/news/first-release-of-gettys-new-research-collections-viewer-offers-digital-access-to-vast-archives/ | Getty 官方案例；未以獎項為依據 | 檔案組織不被影像牆打散；IIIF 高精度放大 | **採歷史圖冊、古地圖和聖經插圖深讀** |
| 15 | Are.na · https://www.are.na/about / https://help.are.na/docs/getting-started/channels | 創意資料組織平台；第三方評獎資料非本研究的正式獎項證據 | block 同時關聯多個 channels、跨策展集連接與回溯 | **採多分類引用而非複製相同作品** |

## 實作技術候選、授權／成本與取捨

1. **原生 CSS Grid / semantic HTML / image / IntersectionObserver**：零外部依賴，優先用在 6 列作品牆、2×2 策展 tile、主類／子類 cover 與 lazy load；不重新建立新全站 CSS。參考 Pell Mell 案例。**直接採**。
2. **GSAP Flip + ScrollTrigger**：已知 P2 歷史技術選項；GSAP 自 2025-04-30 起所有外掛免費，但仍遵守其 Standard License。案例： https://github.com/codrops/GridLayoutAnimation 、https://github.com/codrops/ScrollBasedLayoutAnimations ；只做分類封面放大／返回位置；不重新寫原 V9 旌旗。**adapter 可選，先測原生 View Transition**。
3. **View Transitions API**：https://developer.mozilla.org/en-US/docs/Web/API/View_Transition_API 。同頁 grid→分類的簡單轉場可直接使用，須測 Firefox／Safari 並準備無動畫 fallback。**優先可選**。
4. **imagesLoaded**：https://github.com/desandro/imagesloaded ，MIT，監控原作封面載入或錯誤避免佔位及重排。亦可直接採用原生 img.onload/onerror。**原生優先**。
5. **MiniSearch**：https://github.com/lucaong/minisearch ，瀏覽器端全文、前綴／模糊、欄位權重。2 萬本需在 Hugo 建置時按語言／子類分 shard，**不能直接把全部資料塞進首頁**。**條件採用**。
6. **TanStack Virtual**：https://github.com/TanStack/virtual ，大清單／網格虛擬化，可用原生 JS adapter；要先量測真正 DOM 瓶頸，且保持 SEO / keyboard / scroll restoration。**超大分類頁才考慮**。
7. **Muuri**：https://github.com/haltu/muuri ，MIT，responsive filtering grid；對既有 CSS Grid 的 6 列規格而言易造成額外重排與人工拖拽，**初期不採**。
8. **Embla Carousel + Autoplay**：https://www.embla-carousel.com/docs/plugins/autoplay ，適合明確的單列封面集，不適合讓整面 21,047 冊圖牆「每張卡同時跳動」。**單列才條件採用**。
9. **PhotoSwipe**：https://github.com/dimsemenov/PhotoSwipe ，MIT，可放大單件書內插圖；不應替代書目→正文閱讀頁。**條件採用**。
10. **OpenSeadragon**：https://github.com/openseadragon/openseadragon ，BSD-3-Clause，適用 IIIF 高解析古地圖／手抄本；載入成本高，只在有 IIIF 來源的單書詳細頁 on-demand。**深讀階段採用**。
11. **Internet Archive BookReader**：https://github.com/internetarchive/bookreader ，開源的掃描書頁閱讀器；不因使用者要求「不跳出原站」就非法重新鏡像外部版權資料。**有合法掃描資料和權利才接**。

## 三個必須區分的實作機制

- **「輪替的分類封面」不等於「書的封面」**：分類用於代表一個集合，可顯示多本已在該分類內的真實書封／原作圖版；單書只能顯示那本書的真實圖像。正式分類關聯缺失時，不能讓任意圖片視為該學科的代表作品。
- **「隨機」應是受控探索**：每次只替換少量封面； hover/focus/reduced-motion 時暫停；圖像載入完成才交替；避免類目位置改變。可設 5–8 秒、每次 1–2 張；速度是待用真實畫面裁決的初始候選，不是已審定設計。
- **「無封面」先找同冊內頁插圖**：檢查原書掃描頁、題名頁、卷首插畫、扉頁／版畫／地圖的來源與版權；若全無，展示有作品真實 metadata 的紙質字排，**不生成黑色假封面，也不借用無關作品圖**。最終目標每件有實際圖像仍須執行編目補全。

## 實施順序與驗收

**A（藝術）**：以 Rijksmuseum × Pell Mell × PDIA 的共同原理，選三個完全不同的「無邊框 2×2 大幅圖像與紙質標題」版面，真實封面不受暗層覆蓋，並保留周圍 1×1 封面；實測再決定是否採用。

**B（分類）**：中文圖書為明示第一級入口；七主類＋全部書目為同級；沿實際資料產生主類→子類→書→閱讀→返回的堆疊狀態（包括深連結、上一頁／返回與手機瀏覽）。

**C（圖像）**：先核對所有具合法封面的 Work ID；其次對原冊挖有權利的內文圖版、題名頁。首屏 100% 真實影像後，逐頁擴充；不可用任意跨作品替代充數。

**D（效能與 QA）**：兩層入口與完全退出後的 scroll restoration、桌面 1648×928／手機 390×844、200% 縮放、鍵盤、reduced-motion、重複返回、封面 404/熱鏈/慢速網路與 CLS、Chrome/Firefox。只見 CI 通過不等於藝術驗收。

**來源與授權結論**：網站作品只能參考構圖和 IA；不得複製對方品牌、版面程式或圖像。開源第三方 library 的版本與分發遵循各自授權；具公有領域標示的作品逐件核實原作與數位複製之權利。調研案例與技術並非「已在 P2 05 完成接入」。

