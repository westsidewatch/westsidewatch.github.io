# 黎明書局｜單一工程總入口（Unified Dawn Library Engineering Root）

> **工程身份：GitHub Issue [#273](https://github.com/westsidewatch/westsidewatch.github.io/issues/273) — 黎明書局 / Dawn Library — Genesis Project。**
>
> 設立日期：2026-08（原 #273）；本統一索引版本：2026-11-22。
> 此文件為**工程治理和證據導航**，不是公開書局頁面、不是第二個 catalog，也不是新的設計 OS。
> 本版只存在於隔離分支 `work/p2-05-integration-repair-20261121`，未合併 main。

## 零、唯一工程／永久回溯規則

- **唯一母工程：#273。** 既有 Issues、PR、分支、Formal Edition、P2 05 及其後所有工作，都是 #273 的工程階段／子任務，不另創「新版黎明書局」母工程。
- **單一資料權威：** `static/dawn-library/canonical/root.json` + 21 Works shards；admission、rights、edition、witness、provenance 由既有 Dawn 工程處理。不得以 P2 或歷史索引建立新的 Work ID。
- **統一工作台：** 本文件（入口）＋[跨時期總帳](DAWN-CROSS-ERA-INTEGRATION-AUDIT-20261122.md)（證據詳情）＋[機讀登錄表](DAWN-ENGINEERING-REGISTRY.json)（可盤點項）。三者均屬 #273；總帳不另立項。
- **每次開工必讀本文件和總帳**，核對 registry 所列既有實作和分支，然後才施工。找不到來源只記為「未確認」，絕不可宣布該功能不存在或重做。
- **盤點不可無限宣告「完成」：** 每項以 `located / content-verified / integrated / runtime-tested / editorial-approved` 分層記錄；未逐項核對的分支、shard、作品、圖像皆列未完成。每次新發現追加到同一張 registry，避免無痕重盤。
- **禁止 Sites**；所有工程以 GitHub 版本與 Cloudflare Pages 隔離預覽進行。不得強制合併古老分支、改壞現行 OS、覆寫 P2 01–04 或原館藏。

## 一、原始概念與跨時代不可變要求

- 原工程 #273 核心是可持續成長的福音館藏、知識資源和策展系統，支援 ONE、Journal、Search、Cinema、Doré，而非一次性圖書展示。
- 2026-09 的 `Dual Index Canon`：材質／體驗入口（策展集、天堂電影院、光譜、三晨星）與語義／事工／知識索引互相交叉。
- `Editorial Projection Canon`：同一 canonical Work 可被多個產品和策展引用，不複製作品；投影的媒材主導性不代表排他。
- 三晨星是持久編輯選書，不是評星；策展集可用圖像／古地圖／建築／考古；光譜以知識關係為主；Cinema 以動態影像為主。
- 編輯權威仍為 `docs/design/WESTSIDE-EDITORIAL-MANUAL.md`、Westside Design OS。獲獎級只是一個待驗收標準，不能被 CI 綠燈替代。

## 二、一次尋回的歷代成果：以資料身份分類，不以版本名稱分類

| 沿革／領域 | 唯一權威或仍需回收的工程 | 現在的處置 |
|---|---|---|
| 2026-08 Genesis | #273；`dore-core/knowledge/library/LIMING-LIBRARY-BUILD-PLAN-v0.1.md`；三晨星研究 | 保留理念、研究歷史與拒絕方案 |
| Ingest / admission | `LIMING-LIVE-INGEST-CONTRACT-v1.md`；harvest/relevance/rights/source ledgers | 來源驗證先於正式收錄；禁止候選偽裝正式藏書 |
| Canonical Works | `static/dawn-library/canonical/root.json`：203448 Works、21 shards；authority-backed 201336（manifest） | 身份唯一；203448 不代表 203448 個全文或真封面 |
| Living Library | `static/dawn-library/living/root.json`、21 shards、7 主類、42 子類 | 學科投影；逐書關聯待實證 |
| Formal Edition Phase 1–8 | `docs/dawn-library-formal-edition/PHASE-01..08-AUDIT.md`；runtime 與原資料契約 | 重用正式能力，歷史 PASS 不自動轉移到 P2 |
| Cover Preview / Authority | `static/dawn-library/cover-preview/root.json`（407 shards）、cover-authority、validators | 逐封面 URL、Work ID、同冊來源、權利與 shard counts 審計 |
| 中文作品與中文採購 | `chinese-collection.json`；CLSC；`dawn/full-library-editorial-scan-v1` 的 acquisition pipeline | 區分中文前台 47、canonical 語言 facet 2994、譯名／全文的真實覆蓋 |
| 閱讀與翻譯 | `reading-pointer-map.json`；`formal-edition/runtime/translation-surface.mjs`；Dawn Reader | 原文、繁中、雙語契約≠已物化全文；來源讀取／權利另驗 |
| Personal Dawn | `formal-edition/runtime/personal-state.mjs`；Library Card、Bookmark、Saved View、Reading Trail | 直接復用 `dawn.personal-state.v1`，不創第二套個人資料 |
| Dual Index / Editorial World | `dawn/full-library-editorial-scan-v1` 的三份 Canon / Scan 文件 | 理念找回；P0/P1 原狀為 ACTIVE，P2–P6 當時 QUEUED；現況須核查 |
| Visual Graph / IIIF | `dawn-library-visual-graph-phase1`、`dawn/step5-iiif-runtime-mount` 等 | 查找實際圖像來源／高解析閱讀能力；未合入不等於可直接接入 |
| Jerusalem 3000 | `dawn/jerusalem-3000-curated-v2`、`static/dawn-library/p2-exhibitions/jerusalem-3000.json` | 12 書＋6 視覺來源與各景同作身份逐件核查；策展可進入 P2 |
| P2 05 | PR #1403 原工程、保全分支、隔離 PR [#1411](https://github.com/westsidewatch/westsidewatch.github.io/pull/1411) | **唯一當前 P2 展示層**，禁止代替館藏核心，禁止未驗收合併 |
| 多雷設計探索 | `docs/design/DAWN-DORÉ-EXPLORATION-20261122.md`、OS 編輯手冊 | 研究案例≠已採用；原藝術母本與授權逐項回溯 |
| 對外子項 | #278 Daily Bread；ONE、Journal、Cinema、Search 等 consumers | 由 Dawn 共享底層供給，不另開圖書資源資料庫 |

## 三、持續盤點而不反覆遺漏的機制

每一個歷史資產都必須有 **原始路徑、分支/commit、身份權威、功能、重用狀態、檢驗證據、缺口、對應 Issue/PR**。機讀清單詳見 `DAWN-ENGINEERING-REGISTRY.json`。

新增或發現歷史資產時：

1. 查 `registry`：同一功能已存在嗎？避免「找不到→重做」。
2. 列入 inventory；`status=located` 只表示找到路徑，不能寫成完整核驗。
3. 比對 `main`、原分支與 P2 adapter；若主線已包含歷史分支，記為歷史 lineage 而非新功能。
4. 核驗具體內容（shard/metadata/WorkID/rights/來源/中英文本）；瀏覽器實測另外獨立記錄。
5. 修改現有模組或建立狹義 adapter；禁止第二份 canonical、第二套 Personal 資料或將演示 JSON 當總館藏。
6. 在同一 registry 更新 evidence、status、remaining；進行當輪 Gate 記錄並更新 #273。無證據保持 pending。

**防漏覆蓋矩陣**：歷史分支、Issue/PR、原始文檔、數據 manifest/shards、來源與權利、UI/動效、第三方依賴、資料庫身份、中文、封面/同書圖版、Reader、Personal、策展、QA/Cloudflare。任何一欄沒有證據都不得自稱全盤完成。

## 四、權威數字與嚴禁混淆項

- Canonical Work count: **203,448**，這是 manifest count，不是 203,448 本可全文閱讀的完整數量。
- Living: **7 根類 / 42 子類**；屬於分類投影，不代表所有作品都有逐冊通過審核的分類 join。
- Cover Preview: **407 shards**；不等於全部作品均有真實可用封面。歷史檢查分片 1/2/3/10 的 items 數為 463/499/498/498（manifest 原宣告各 500），待全量重核。
- Historical catalogue: **21,047**，獨立古籍／歷史書目入口，不能取代全館 canonical。
- 中文前台集合 **47** 和語言 facet `chi=2,994` 不同口徑；無法據此推論繁中譯名與全文覆蓋。
- `firstReadableCount=0` 為歷史閱讀層報告，不可因擁有 reader UI 就宣稱全館雙語可讀。

## 五、工程缺口與明確完成條件

| Gate | 目前可證實的階段 | 完成條件 |
|---|---|---|
| G0 工程資產全景 | **部分完成**：本輪已找到 #273、分支群、總帳；並非完整分支/PR 全量掃描 | 分支與 Issue/PR 全面機讀，按功能去重、保留差異，附 ref 和 SHA |
| G1 Canonical | manifest 已讀；**尚未逐 shard 審計** | 21 shard SHA、筆數、Work ID 唯一性與總數驗證 |
| G2 Living 雙索引 | root 與規範已讀；分類逐書 join 未完成 | 每一公開分類有真實可回溯的 Work membership |
| G3 封面/圖版 | 407 shard 已知；部分漂移已定位 | 全部 shards / Work ID / source / HTTP image / rights / 同書圖版檢驗 |
| G4 中文／讀者 | 原 contracts 存在，翻譯及閱讀率未完成 | 逐冊按原文／繁中／雙語／合法外部來源分列可讀狀態 |
| G5 Personal | 原 state 模組已復用；跨 origin 未證實 | 個人卡、bookmark、view、trail、export/import 全流程 QA |
| G6 策展 | 先前 selection 有來源但未全部藝術驗收 | 三晨星／光譜／策展／Jerusalem 圖像與 Work ID 一致 |
| G7 P2 UI | PR #1411 隔離，未放行 | 桌面/手機/鍵盤/可逆翻頁/原版轉場/無工程文案驗收 |
| G8 治理 | **本文件為單一入口已建**；歷代差異尚待補齊 | #273、registry、總帳隨後續提交一致更新 |

## 六、保全與分支路由

- **正式 repo**：`westsidewatch/westsidewatch.github.io`；`main` 是現行已發布底座。
- **原 P2 05**：`p2-0105-dawn-library-preview-20261120`，保留且不修改。
- **只讀 archive**：`archive/p2-05-preserved-20261121`。
- **目前統合工作**：`work/p2-05-integration-repair-20261121`，PR #1411（Draft，且不得合併）。
- 歷史分支如 `dawn/full-library-editorial-scan-v1`（ahead 32 / behind 3011）、`dawn/step5-iiif-runtime-mount`（ahead 4 / behind 4366）是**待審證據來源**，不得直接整枝合併。
- 若需要後續施工，先在 #273 及本索引登錄工作歸屬和改動範圍；不能另起一套 Dawn 核心。

## 七、讀取與驗收先後順序

1. [母工程 #273](https://github.com/westsidewatch/westsidewatch.github.io/issues/273)
2. 本統一入口與 `DAWN-ENGINEERING-REGISTRY.json`
3. [跨時期整合總帳](DAWN-CROSS-ERA-INTEGRATION-AUDIT-20261122.md)
4. `docs/design/WESTSIDE-EDITORIAL-MANUAL.md` 及正式 OS
5. 按任務讀原 Work / Living / Cover / Personal / Reader modules 和歷史分支
6. 只在隔離分支修復、部署 Cloudflare 驗收；視覺、真實資料和讀者操作各自達標後才提交審核

**此文件的存在不代表全部歷史盤點已完成；它把盤點、補遺、統合和驗收鎖在同一個長期工程，防止下次重開與漏項。**
