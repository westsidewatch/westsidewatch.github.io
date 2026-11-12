每次啟動 Scripture Studio 工程，必須先讀取工程章程、編輯手冊、Design OS、V14 硬性規範、三條鉛字語法、既有多雷探索與版本／驗收記錄，盤點並優先調用工程已具備且實際可用的聖經原文及 USFM 詩行解析、V16–V18 語義鎖定與合法斷句、雙語同帶交錯、真實字型量測、可變版心求解、SVG／HTML 輸出、瀏覽器跨尺寸檢查及 GitHub 工具，沿用已驗證成果並先做來源與權限核查，只有確認缺口後才增補能力，不得另造已存在工具、擅改經文或硬約束、以生成圖片代替工程、未驗收便宣稱達標。

# 多雷探索 R2｜Square Ground / 字塊背景與共用印版（2026-11-11）

## 工作定義

按 `docs/design/WESTSIDE-EDITORIAL-MANUAL.md §9`，此研究尋找世界既有的真正設計作品和可轉移機制；**不是搜尋 Gustave Doré 版畫、不是生成美術圖，也不把引用的作品當可無條件重用的素材。** 對 15 個有作品頁或館藏依據的實例提取共通結構，而非模仿外觀。研究來源供學習，不表示所引用作品曾獲指定設計獎。

## 15 個有來源的實例

| # | 作品及來源 | 可移植機制 | 本案採用／禁忌 |
|---|---|---|---|
| 1 | [Wim Crouwel — Vormgevers (1968)](https://www.sfmoma.org/artwork/2015.658/) | visible modules shape negative/positive letter identities | **Primary A** — Use square grid as shared text/background registration, not a checkerboard |
| 2 | [Wim Crouwel — Visuele Communicatie Nederland (1969)](https://www.si.edu/object/visuele-communicatie-nederland-visual-communication-netherlands-stedelijk-museum-amsterdam%3Achndm_2009-13-1) | square letter cells over bar-like grounds | **Primary A** — Background stripe aligns to modular type advances |
| 3 | [Piet Zwart — NKF, 1928](https://www.moma.org/collection/works/7741) | letterpress, offset and rectangular visual hierarchy | **Primary B** — Blocks mark meaningful entry/shift in reading |
| 4 | [Piet Zwart — NKF, c.1924](https://www.moma.org/collection/works/7745) | minimal graphics as building blocks of typesetting | **Primary B** — Use typographic runs, not bespoke unrelated illustration |
| 5 | [Piet Zwart — International Film Festival (1928)](https://www.moma.org/collection/works/5677) | orthogonal geometry, color and lettering | **Secondary** — Reject angle/diagonal in physical reversible seal |
| 6 | [El Lissitzky — For the Voice (1923)](https://www.moma.org/collection/works/14473) | letterpress printed shapes and sizes become textual pacing/index | **Primary B** — Blocks distinguish breaks without altering Bible source |
| 7 | [Paula Scher / Pentagram — The Public Theater](https://www.pentagram.com/work/the-public-theater) | rectilinear typographic field creates architectural identity | **Primary A** — Block sizes derived from phrase extents |
| 8 | [Pentagram — MIT Media Lab identity](https://www.pentagram.com/work/mit-media-lab/) | generative modular identities from consistent grammar | **Primary A** — Variable passage lengths must retain coherent visual DNA |
| 9 | [Ladislav Sutnar — 4-Square Lumber Products (1944)](https://www.moma.org/collection/works/129042) | square modules encode information groupings | **Primary B** — One block can have semantic role without random duplication |
| 10 | [Otl Aicher — München 1972 (SFMOMA)](https://www.sfmoma.org/exhibition/otl-aicher/) | system-wide modular composition across media | **Secondary** — Reusable background grammar across realm folios |
| 11 | [Otl Aicher — 169 square pictograms](https://www.cooperhewitt.org/2017/12/29/faster-higher-stronger/) | squares as rigorous formal units | **Secondary** — Do not use icons, transfer only measured square-cell logic |
| 12 | [Wolfgang Weingart — Typographic Process (1971–74)](https://www.moma.org/collection/works/86484) | type-space experimental layering and visual rhythm | **Caution** — No unsafe overlap of bilingual Bible quotations |
| 13 | [April Greiman — Does It Make Sense? (1986)](https://www.moma.org/collection/works/172729) | multiple planes and precise graphic layering | **Caution** — Physical foil layer must remain one mother-forme |
| 14 | [Studio Dumbar — DEMO 2019](https://studiodumbar.com/work/demo) | programmable identity derived from script | **Secondary** — Do not use animation to disguise poor still-form composition |
| 15 | [Josef Müller-Brockmann — Musica Viva concert (1958)](https://socks-studio.com/2016/11/30/joseph-muller-brockmann-musica-viva-posters-for-the-zurich-tonhalle/) | quadrilateral color weight contrasted with narrow information text | **Secondary** — Study mass and axis only; no tilted stamp or color imitation |

## 下一步方向評判

- **A / Registered Ink Tiles「套版字塊」：優先。** 以每段真實字形的 bounding box 作矩形模組、分配紙墨反差；方塊隨 **同一個字柱母版** 90° 翻轉。不是單獨的裝飾背景，不加入第三個字體或任意經文。保持英中文字形次序與可編輯性。利用 token 是否接觸中英轉換點決定哪個方塊需要墨底。
- **B / Counterform Cutouts「留白切口」：第二方案。** 只在合法語義節點周圍留下紙色切口，方塊間的負空間承擔閱讀停頓和視覺重心，避免所有詞組一樣平均。
- **C / Decorative Checkerboard「裝飾性棋盤」：淘汰。** 填滿大量格子不代表設計，與聖經語義無關時違反 OS 和 Award Rubric。

## OS / 硬規範

OS 色彩以 `design-system/tokens/westside.tokens.json` 的 paper、ink、olive、first-light、harvest 為權威；不得直接照抄其他作品的色彩。字體 Chiron Hei HK WS 900/200、Bodoni Moda SC 維持；不破壞 V14 H1–H10，尤其 H2 受保護詞組、H3 單一母版、H4 同帶多次語言轉換、H6 不均分嚴格過半、H8 同標稱字號。方塊應為排列資料中的可量測視覺元素，不能讓字型邏輯改成各自獨立的頁面。

## 藝術驗收：方向性 20 分內評估，不是獲獎聲明

10 項：意義、作品辨識度、構圖差異、字體、雙墨色、視覺層級、互動意義、手機、無障礙、可編輯性，各 0–2 分。探索最低 15/20 且意義、辨識、無障礙、可編輯不得 0。排版 H1–H10、無字形碰撞、實際 DOM/ink bounds、390px 與列印輸出，是藝術分數以外的獨立攔截條件。

**狀態：15 實例研究已記錄；工程方塊語法試作中。研究中所引用的作品圖像不會直接嵌入工程或聲稱有授權。**

## V34.0 實際工程試作／對照驗收（2026-11-11）

檔案：`static/experiments/scripture-studio-motherform-live.html`；實際代碼提交 `6814c1d63db4c9a6e70a2c5123570ec15e020489`。

**已接入（實際代碼）**：A / 套版墨塊、B / 留白切口、C / 純文字對照；依現有文字 `piece` 的 DOM width/height/offsetTop 計算每塊墨底／刻線框，背景保持在同一字帶和同一個 `forme` 內，跟隨整件 90° 旋轉；文字符合既定字型和大小，不為上色更改內容或斷句；配色選自 OS paper/olive/harvest。

**防止虛假通過**：如果沒有 V14 H4/H6 通過的構圖，仍允許只作概念比較的 `provisional` 試稿，頁面標 `STUDY · NOT APPROVED`，且阻止正式配方輸出與列印；V18 斷句已提供入口，但尚未接入當前求解器，任何印面目前均非出版核准。

### 得獎導向審稿（內部 20 分門檻，非外部獎項）

| 項目 | V34.0 靜態狀態 | 待補實際證據 |
|---|---|---|
| 意義 / 辨識度 | 方塊隨合法排字幾何而非獨立插畫，機制成立 | 觀看是否真正形成 Scripture Studio 獨有語法 |
| 構圖差異 / 字體 | A/B 依真字形矩形與反白，使用既有 OS 字型 | 實際 1648px/390px 截圖、墨底避讓、Small Caps glyph 渲染 |
| 兩墨色 / 層級 | 取現有 OS 紙色、橄欖、收穫色，不使用黑色大底 | 真實色彩對比和閱讀層級抽檢 |
| 互動 / 無障礙 / 編輯 | 三個模式 UI 可切換，同一母版 DOM 可編輯 | 瀏覽器讀屏、鍵盤、模式切換、列印一致性 |
| 全案驗收 | **NOT APPROVED**，尚未通過 V18 語義資料與完整 V14 H1–H10 | 語義接入、公式、合規比例及手機／列印截圖 |

**結論**：探索作品及代碼原型已完成，**不能給予可靠的 15/20 以上通過分數**，因尚未執行必要的真實視覺、可讀性與跨尺寸驗證。下一輪優先 V18 接入、實際字形量測與 A/B 的視覺淘汰；不能只因 A/B 都渲染成功就稱為得獎水平。
