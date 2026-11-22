# 黎明書局跨時期工程盤點與整合總帳

日期：2026-11-22。作用域：P2 05 隔離 Draft 工程；非公開網頁文案、非「另一個黎明書局產品」。不得使用 ChatGPT Sites，不得合併 main 或覆寫原始素材。

## 盤點方法及證據界限

- 對 GitHub `main` 全倉樹 **6,054 個路徑**作 Dawn／Library／Cover／Reading／Translation／Editorial／Personal 等關鍵線索定位，不只搜索 P2 05 的少數靜態檔案；另對 `dawn/full-library-editorial-scan-v1`、`dawn-library-books-v1`、`dore/dawn-library-formal-edition`、`redesign-dawn-library-public`、`p2-0105-dawn-library-preview-20261120` 等歷史分支做 main ahead/behind 比對。
- `main` 的靜態檔案與驗收報告是已存在資產的證據；**文檔說「PASS」不等於今日 P2 的功能已接入**。
- `dawn/full-library-editorial-scan-v1` 分支與 `main` **diverged（ahead 32 / behind 3011）**；其雙索引規範、中文採購生產線與掃描工序必須逐項確認和選取，不得整枝合併、覆寫當代主線。
- `dawn-library-books-v1` 為 **ahead 6 / behind 6765** 的原初低成本 Open Library 書本研究 adapter，保留為研究史；不是現今 canonical authority 或大量擷取方案。
- 靜態大型 JSON 透過 GitHub 連接器讀取會出現零位元組／受限（例如 10k shard 和 canonical-index），所以此處的總量是由 root manifest 與既有建置驗收交叉確認，**不是逐冊讀回 203,448 筆的獨立內容審計**。

## 歷代工程脈絡與權威統合

| 時期 | 原始工程／記錄 | 已有能力 | 身份地位與整合決策 |
|---|---|---|---|
| 2026-08 起 | `dore-core/knowledge/library/LIMING-LIBRARY-BUILD-PLAN-v0.1.md`（內文 v0.4）、`THREE-MORNING-STAR-CURATION-PROJECT-01.md` | 先學館藏科學，名師標準，三晨星精選／研究方法 | 保留治理與策展倫理，不把三晨星做成星級評分 |
| 2026-08 起 | `LIMING-LIVE-INGEST-CONTRACT-v1.md` | discover→verify→classify→registry→relations→use→feedback；權利／來源／中文可及性 | 保留外部來源 discovery 和 live ingest，候選不得混入正式 canonical |
| 2026-09 上旬 | `DORÉ-DAWN-LIBRARY-AUTONOMOUS-GROWTH/STOREFRONT-EVIDENCE-LEDGER`、`reports/DAWN-LIBRARY-*.json` | 自動發現、relevance、rights/provenance、遠端來源、精品書架 | 決策依證據，不把搜索命中當合格內容；精品書架存在非基督教小說，不能不經審核照搬進 P2 福音策展 |
| 2026-09 Formal Edition | `docs/dawn-library-formal-edition/PHASE-01..08-AUDIT.md` | 唯一 Work 身份、Relation/CollectionContext/Projection、Editorial World、Personal Dawn、單站整合；Phase 8 歷史驗收 PASS | **復用核心模組**，舊 Phase 4 技術驗收 UI 不作為新公開刊物頁 |
| 2026-09 canonical substrate | `static/dawn-library/canonical/root.json`、21 shard、`living/root.json`、21 shard | 203,448 canonical Works、201,336 authority-backed；七大分類 42 子類、lazy window、facets、Work counts | 權威 Work／學科投影，取代 P2 二次造出來的弱分類數量 |
| 2026-09 封面 | `static/dawn-library/cover-preview/root.json`、407 shard、`cover-authority/authority-000001.json`、封面驗證 scripts | Canonical Work ID→cover pointer；407 shard；首個 Authority sample eligible 463 / resolved 228 | 不是 203,448 張「已核實封面」：root 來源統計 201,333 Open Library fallback + 2,115 placeholder；逐項 image 404、權利仍要驗 |
| 2026-09 中文作品 | `chinese-collection.json`、`cover-preview/chinese-collection.json`、CLSC admission ledger、中文素材探索 | 47 筆前台中文集合；CLSC canonical 46 與《靈歷集光》候選狀態需保留；來源、領域、access、Work ID | 用原有中文記錄與分類家族；不得以「47 張皆有真封面」呈現 |
| 2026-09–10 讀者閱讀 | `reading-pointer-map.json`、`surfaces/dawn-reading-layers.json`、`formal-edition/runtime/translation-surface.mjs` | 已建指標／原文／繁中／雙語合約；讀者的 Bookmark/View/Trail 原 local-first store | 整合真實路徑，權利和文本物化分開；當前 firstReadableCount=0，不能宣稱全文已本地化 |
| 2026-09 未合入研究 | 分支 `dawn/full-library-editorial-scan-v1`：`DUAL-INDEX-CANON.md`、`EDITORIAL-PROJECTION-CANON.md`、`FULL-LIBRARY-EDITORIAL-SCAN-V1.md` | **雙索引**：材質／體驗（策展集、電影院、光譜、三晨星） × 語義／事工（聖經、歷史、神學、禱告、中文等）；中文缺口掃描 | 必須保留這一創新；審核概念後納入當代 P2 UI 導航，不直接 cherry-pick 3,011 commits 落後的分支 |
| 2026-09–11 視覺與閱讀 | `docs/dawn-library-display-system-memo.md`、`docs/projects/dawn-data/LIBRARY_SECOND_PAGE.md` | 同一 canonical Work 對應不同觀看尺度，封面→作品→閱讀，避免 200k 同屏 DOM | 僅保留成熟原理與原始 motion identity；原生 lazy-load、bounded window |
| 2026-10–11 P2 | `p2-0105-dawn-library-preview-20261120`、P2 01–04、`p2-editorial-channels.json`、`p2-exhibitions/jerusalem-3000.json` | 12 書＋6 獨立視覺的 18 景策展；三大入口；長閱讀鏈 | **視覺／交互層**，不得製造獨立 Work 身份；原 P2、保全分支不覆寫 |

## 先前 P2 05 的具體偏差（已驗證）

1. 使用孤立的 `catalogue/index.json`（21,047 筆／85 頁）冒充全部 canonical（203,448）——兩者用途不同；且此 21k historical bibliographic set 語言全部 unknown，不能作整館語言統計。
2. 分類入口曾只從 `classification.json` 取七個名稱，而非 `living/root.json` 既有真實 Work counts；葉節點用英文搜尋詞模仿正式學科 membership。**已先改為 Living 根分類及 counts，但正式逐冊葉節點 join 尚未完成**，在未完成前必須標示「相關書名」而非偽稱已遍歷所有 members。
3. 三晨星／策展／光譜入口曾混入沒有對應當期策展 Work 的圖像；光譜曾使用科幻小說與一般小說封面。已改由 `dawn-launch.json`、`p2-exhibitions` 及 `p2-editorial-channels`＋原源書架取材；原作缺圖顯示原文作品標題，**絕不借用其他 Work 的封面**。
4. P2 05 沒接回正式 Personal Dawn 的閱讀卡與收藏。現在從原 `runtime/personal-state.mjs` 模組讀寫同一 `dawn.personal-state.v1` local-first store；個人書房包含真實 Work ID 的 bookmark、saved view、trail、匯出／匯入；不是另建個人身份系統。
5. 曾把「全部館藏」「分類索引」與工程說明當巨大公開標題，違反 `WESTSIDE-EDITORIAL-MANUAL.md` §11。已從 HTML 源移除，文案隔離仍要全頁檢查。
6. 舊分類「中文 47」與 `Chinese 2994` 語言 facet 是不同資料範圍，**不可互換、不可用 47 計算 203k 繁中覆蓋率**。

## 單一產品架構（不增加第二 engine）

```
已有 Dawn Canonical Work + Edition/Witness/Source + rights/admission
                           │
        Relations + Subject Facets + editorial evidence
                           │
           CollectionContext / dual-index routes
                  ┌────────┴─────────────┐
    材質／閱讀方式          語義／學科／事工
   三晨星  策展  光譜          聖經  歷史  神學  禱告…
                  └────────┬─────────────┘
                Canonical cover-preview + source image
                           │
       P2 05 reader-facing surface / OS / source-faithful artwork
                           │
           Library Card / reading + zh-Hant projection
                           │
              原 Personal Dawn 本機收藏、視圖、足跡
```

## 整合狀態（不可用「完成」掩蓋未完成）

| Gate | 狀態與證據 |
|---|---|
| A. GitHub 全倉／分支定位 | 完成第一輪 6,054 tree 路徑與歷史分支 compare；逐字逐件 artwork 與逐冊分片未完成 |
| B. Canonical root / Living 分類 | P2 已改以既有 `living/root.json` 讀取權威主類／子類 counts（JS syntax pass）；仍需瀏覽器 QA |
| C. Personal Dawn | 新 bridge 動態匯入原模組，共用原 storage key，支持 Work bookmark、view、trail；需 browser QA 和跨 Formal Edition 存取驗證 |
| D. 策展圖像原作關聯 | 新 bridge 讀取既有三晨星 selection、18 景、光譜 source shelves；需逐張 URL 和 artwork provenance QA |
| E. 實際分類逐冊 join | **未完成**；應透過原 Living Work refs/semantic projection 而非 lexical keyword 假關聯 |
| F. 203k 全館繁中譯名 | **未完成核證，不能視為已翻譯**；原語言服務狀態 bound-awaiting-materialized-text |
| G. 203k 封面逐件有效與同冊插圖補全 | **未完成**；407 shard 是指標不代表 407×500 張可用圖 |
| H. 全文閱讀／權利 | **未完成**；source pointer與保護邊界已有，閱讀層 firstReadable=0；不能擅自重新託管外部全文 |
| I. 桌面／手機、可逆 P2、無工程文案 | 待 Chromium 圖像和 P2 01–04 保護測試，以最新 Cloudflare preview 判斷 |
| J. 公開得獎級驗收 | **未達成**；以圖像真實性、完整分類、中文可讀性與有據來源，以及用戶藝術審核為準，不把 CI success 當得獎 |

## 下一步技術原則

- **不合併歷史分支**：將重要雙索引 concept 先以 scoped reader-nav 方式在 P2 驗證，現有 source/admission 仍為 main 權威。
- **不複製書目**：逐書從 workId 查原封面、書名／譯名、作者、版本、rights、閱讀能力；P2 state 只持 workId、context、視覺投影。
- **不假造字幕與譯本**：原文／繁中／雙語切換只能使用已物化的來源和可信翻譯，頁面若缺席則明確標示，不把 UI contract 視為正文完成。
- **出圖來源**：封面原書→同一 Work 來源扉頁／插圖→透明的無圖 metadata 排版；不可使用跨作品借圖和黑色假封面。
- **多雷探索觸發點**：真實需用但原技術缺少的原生轉場、IIIF zoom、圖像位址穩定性或海量索引渲染；先復用原 runtime，外來技術須核查開源授權／負擔／維護，再做隔離 Chromium 實驗。

## 2026-11-22 新增：封面分片數量與出版過濾漂移（來源實測）

驗證 `cover-preview/root.json` 與實際分片：第一分片 manifest 500，資料實有 463；第二分片 manifest 500，實際 items 499；第三分片 498；第十分片 498。這表示部分 manifest count/offset **不再準確反映範圍過濾後可展示的 Work 數量**。不能直接拿 203,448 除以 500 當公開有效封面數，也不能在縮短的分片中以舊 offset 切片，否則漏書、斷頁。

P2 的 `p2-dawn-canonical-gallery.mjs` 已改為 `{shardIndex,indexInsideActualItems}` cursor，依 `data.items.length` 循序跨分片，60 張一頁；讀者的總數標示為「主書目」而不是「已全部核實的可讀書」。**原始 root / shard 零改動**；完整清點與重建各 shard sha256/count 的計畫需在專門的 canonical admission 流程進行，不得由 P2 覆寫權威來源。查核作為未解決資料一致性問題留在 Gate F。

## 來源圖像錯配阻斷

比對 `storefront.json` 已發現「精品書架」有一般科幻和小說，例如 *A Fighting Man of Mars*、*Confessions of Zeno*。之前 P2 三大入口把這些放在「光譜」，不符合原分類及福音閱讀定位。P2 新 `p2-dawn-editorial-art.mjs` 先依 `dawn-launch.json`、`p2-editorial-channels.json`、`p2-exhibitions/jerusalem-3000.json` 調取對應作品／有來源圖版，找不到時使用原書名排版，而不是借別書圖像。需做逐張實際圖片、權利與讀者文案驗收。


## 2026-11-22 P2 第二層：恢復 Living 真實逐書分類接線

歷代 `living/wall-*.json` 分片已有 `workRefs[].classification.roots/leaves`，無須以英文書名模糊搜索代替學科 membership。P2 已新增 `p2-dawn-living-membership.mjs`，按原 root 的 21 分片查詢 Work ID，交由原 Resource Fabric 解出作品信息；字串關鍵字假分類路徑已從 P2 子分類頁移除。這是**原工程能力接通**，不是新增 authority。

已進行 V8 模擬驗證：子分類包含、同 Work ID 去重、限量、取消與不調 keyword 路徑通過；未做完整實站與圖像 QA，不可聲稱整個館藏分類已逐冊編輯核對完畢。
