# R168 · Westside Watch 成長線與獎項差距評估
2026-11-27；研究文件，不改 OS、現有 artwork、P2 或 production。基準 R167 90ca37989030a111e49299d8e77fe7177ca163ed。

## 實證
R163 57幾何校樣（非57互異拓撲），R164 16藝術候選，R165 12同源構成，R166七材質研究，R167四精細刻線候選。R167 Chromium proof 成功（45991138554，artifact 15194145372，四種寬度）；Cloudflare commit 90ca379 部署成功：https://e41bcf0f.westsidewatch-github-io.pages.dev/experiments/seven-realm-r124/r167-context.html 。實際截圖顯示底紋退讓有效，但內容矩形扣除使以馬忤斯刻線零碎，書局僅餘狹窄中縫，缺乏主構圖；手機經文引文有截斷觀感，需單獨查證。R165 雙印 glyph 等待逾時（45989500535）；R164 母版仍 V18 review-only。R167 First Look Branch Preview 失敗（45991138692；job 140478953998），homepage must mount the 04 wrapper around the protected 01–03 source，期望 p2-0104-olive-continuation.html?embed=1；不能由此斷言現行 production 失敗。Doré Foundation Tests 成功不代表藝術驗收。

## 多雷研究方向與外部證據
本輪在可用 GitHub 與公開網站檢索，未直接調用獨立 Doré 執行引擎；保留來源與轉譯。
- Design Council Double Diamond：https://www.designcouncil.org.uk/resources/the-double-diamond/ — Discover/Define/Develop/Deliver；目前在 Develop，既有網站功能與新設計系統成熟度分開。
- Hood / Pentagram：https://www.pentagram.com/work/hood-museum-of-art — 建築磚石轉譯為出版、網站、導視；方形是生成模數，不是貼圖。導向成長線的版式、折角與短線。
- MIT Media Lab / Pentagram：https://www.pentagram.com/work/mit-media-lab/ — 共同格網與獨立識別；導向七章同紙同墨盲測與小尺度校正，不複製外部標誌。
- Whitney / Experimental Jetset：https://www.jetset.nl/archive/whitney-museum-identity — 回應內容的線形；導向方形錨點的響應式變化。
- Rijksmuseum / European Design Awards 2021 Gold：https://awards.europeandesign.org/winner/248792 — 大圖、簡潔、Stories 與不同觀眾路徑；導向真實編輯內容和完整任務。
- Museum London / RGD 2026 Element Award UX：https://rgd.ca/hiring-designers/award-winners/2026-branding-award-winners/element-awards/museum-london-website — 品牌與日常內容更新、活動發現連結；導向教會日程與入口、可維護編輯流程。
- Awwwards 評分：https://www.awwwards.com/about-evaluation/ — Design 40%, Usability 30%, Creativity 20%, Content 10%；HM jury 6.5+；不是自評即獎項分數。
- Webby：https://www.webbyawards.com/judging-criteria/ — content, structure/navigation, visual design, functionality, interactivity, overall experience。
- WCAG 2.2：https://www.w3.org/TR/WCAG22/；Core Web Vitals：https://web.dev/articles/vitals — LCP≤2.5s, INP≤200ms, CLS≤0.1 at p75，按桌面／手機；實測未完成，不聲稱通過。

## 十步流程與下一個關卡
1 品牌神學及藝術命題：已確立。2 參照研究及設計方法：已形成，受眾研究仍不足。3 幾何構成母本庫：研究基礎已完成，未正式發布。4 藝術選型、章形及材質：進行中。5 編輯構圖語法（大章主導、字體、圖片、細線、導航）：初步，未形成合格真頁。6 全站資訊架構及任務路徑：既有功能，成長線映射待驗。7 響應式及動效：既有 P2/虛擬教會保護，新的整體關聯尚未驗。8 設計系統/生產工作鏈：原 OS 已有，新規則未進正式元件。9 全站瀏覽器/可訪問/性能/用戶驗收：局部通過，全局未通過。10 上線與投稿：新設計未發布，不宜投稿。新流程完成前三步研究基礎，處於4–5；不是30%工時，也不是獎項分數。
P0: 修復 P2 掛載驗收，對比基準與當前分支，不改受保護 01–03；查明經文母版 clipping/valid 與 iframe 問題。建立全局頁面/路由/元件/資產/原稿 inventory（首頁、P2、第二層、第三層、工具、手機）。P1: 以馬忤斯、黎明書局選擇高品質真內容構圖；先用雙方大章與內容確立主構圖，後落小章、材質、細線；對比有無章紋、原/候選；保留01/04/粗信與06/07 R154。P2: 一份跨版塊 design grammar：geometry IDs, anchor, role, width, reading exclusion, responsive, motion, crop, navigation state, exception rationale；以原有 OS token 接候選元件，不另建模板。P3: 七域全層驗收、真用戶任務、WCAG AA、CWV、Safari/Firefox/Chromium、320/390/768/1440、減少動效、內容真實可用、授權。P4: 逐步合併、公開發布、策展 case study、獎項申請。每關有實際可用原型及明確藝術批准，不以 PR/截圖數量充當成果。
