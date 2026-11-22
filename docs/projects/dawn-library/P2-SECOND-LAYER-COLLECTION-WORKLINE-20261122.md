# 黎明書局｜P2 第二層「館藏」施工主線

日期：2026-11-22。唯一母工程：[#273](https://github.com/westsidewatch/westsidewatch.github.io/issues/273)。
**非公開設計文案。** 在 `work/p2-05-integration-repair-20261121` 隔離施工；PR #1411 未驗收不得合併。

## 判斷：工程資料線清楚；視覺定稿仍欠實際驗收

P2 第二層不是再建立一本「獨立圖書館」，而是原 Dawn Library 的讀者呈現層。

```text
P2 01–04 不動 → 05 第一層 V9（保留） → 05 第二層
  ├─ 編輯式入口：三晨星 / 策展集 / 光譜（遵守媒材主導的 Editorial Projection）
  ├─ 館藏入口：Living Library 7 根類 + 42 子類
  │     └─ canonical Work ID / 真實分類關聯 / 作品頁
  ├─ 中文入口：原中文 47 個前台收錄，與 chi 2994 分開
  ├─ 全部書目：Canonical 203448 root + 21 shards，cover-preview 407 shards 有漂移
  ├─ 歷史古籍：獨立 21047 書目，不作總館藏
  └─ 個人書房：直接復用 Formal Edition Personal Dawn store

單書 → 來源/版次/原文繁中閱讀能力 → 同 Work 圖像 → Bookmark/View/Trail
```

### 已存在且不再重做

- Canonical：`static/dawn-library/canonical/root.json` + 21 shard。
- Living：`static/dawn-library/living/root.json` + 21 shard 的根分類及數量。
- Resource Fabric：`static/js/resource-fabric-client.mjs` 原生 `resourceSearch`, `resourceWork`, `resourceWorks`。
- 原 Reader／Personal：`dawn-reading-resolver.mjs`、Formal Edition `personal-state.mjs`。
- 原 P2 05 V9、P2 01–04、OS 和 SVG 素材保護。
- 編輯雙索引：舊分支 `dawn/full-library-editorial-scan-v1` 2026-09-25 的 `DUAL-INDEX-CANON.md` 和 `EDITORIAL-PROJECTION-CANON.md`。
- 視覺調研：`docs/design/DAWN-DORÉ-EXPLORATION-20261122.md` 已有 15 個案例、11 個技術候選。它是研究，不代表已經實施。

### 2026-11-22 本輪真實程式修改

1. `static/js/p2-dawn-canonical-gallery.mjs`：全館輸入時改調用原 Resource Fabric `resourceSearch(term)`，不再只在已載入 60 筆封面中做本地文字過濾。結果仍由同一 Work ID 開啟單書、圖片跟隨自身 Work。清空搜尋恢復原 pagination；搜尋時上一頁/下一頁暫停，並清楚標明「搜尋索引不等於全文檢索」。
2. `static/js/p2-0105-dawn-continuation.js`：已接上 `searchCatalogue()`；原分類、Personal、轉場未重寫。
3. `static/experiments/p2-0105-dawn-preview.html`：搜尋提示改成全館索引語意；修改預覽快取版號。
4. JS syntax：主程式與 module（移除匯入/匯出作解析檢查）通過；source-level 接線與 HTML 控件存在性通過。
5. **未通過／未宣稱：** 尚未完成最新 Cloudflare 部署有效性或 Chromium/Firefox 實際搜尋與動畫回歸測試。不得寫成 E2E PASS。

### 次序固定的下一段工程

**S1 導航真實性（阻斷）**：替換 `taxonomyQueries` 所做的英文書名搜尋假分類，用 Living 已驗證的 per-Work subject membership / projection，若源資料未齊就顯示「相關檢索」且不冒用分類數。具體需要原 shard 內分類資料契約和來源檢驗。

**S2 圖像身份（阻斷）**：407 shards 的 count/offset 修復不由 P2 偽造；對首屏與分頁的實際 image requests 驗證，`Work ID → cover / same-work plate → rights / source`；缺圖先找原冊合法扉頁、手稿或插圖，仍缺則有誠實 metadata 的紙質排版，不能黑色假封面/跨書借圖。

**S3 第二層編輯視覺（藝術驗收）**：用原有 Doré 研究中 Rijksmuseum 的 image-first、Pell Mell 的克制排版節奏、PDIA 的不同資料觀看模式，改進 2×2 編輯式入口、分類封面牆、書籍細節；不是照抄對方視覺。遵守 OS 字體、黃金和紙色、閱讀優先、封面不壓暗遮罩、長文不截斷。先看現行實際 Chromium 畫面再局部修改，不能在未看到缺陷時大改 CSS。

**S4 閱讀閉環**：分類/搜尋/策展→單書→原文、繁中、雙語可用狀態→合法閱讀→返回原分類與原位置；Personal Dawn 的卡、收藏、閱讀足跡與跨 origin 匯入/匯出。只展示已物化且有合法來源的正文。

**S5 真機與瀏覽器 gate**：1648×928、390×844、200% zoom、鍵盤、reduced motion、圖像 404、延遲網路、反向滾動、空結果、多次搜尋與快速輸入、單書返回、所有 P2 01–04 無回歸。CI≠視覺驗收。

### 清晰與不清晰的分界

- 清晰：權威資料、單一 Work ID、雙索引概念、P2 層級、既有搜索／閱讀／Personal runtime。
- 不清晰：分類逐書已驗證的資料映射、全部封面真實可用性、全館中英文可讀率、實際視覺藝術審定與瀏覽器效果。
- 因此**不需要再做廣泛的重新選型或發明一套視覺框架**。若 S2/S3 遇到具體技術／藝術瓶頸，再依編輯手冊 §9 作「問題→成熟案例→開源授權→隔離試驗→選擇」的定向多雷探索，記回本工程及原研究文件。

### 明確否決的工程方式

- 第二套 catalogue、第二套 Personal Dawn、另一個 Library Work ID。
- 把 21,047 當 203,448；把 47 中文前台當作 2,994 chi 語言 facet。
- 用全文未物化的 UI 契約宣稱「已實現完整雙語閱讀」。
- 用一串 hardcoded keyword 取代真正的 Living semantic subject membership。
- 因為某次 CI PASS 就宣稱第二層完工或放行 PR。

## 2026-11-22 第二輪實際修復：Living subject membership

- 新增 `static/js/p2-dawn-living-membership.mjs`，從原 `living/root.json` 的 `shards[].href` 逐片讀取 `living/wall-*.json`，以每筆 `workRefs[].classification.leaves` 查詢真正屬於所選子分類的 canonical Work ID，再由原 `resourceWorks(ids)` 解析單書書目。最多展示 36 筆，並在頁面說明屬分類樣本或已讀完整分片。
- `static/js/p2-0105-dawn-continuation.js` 的 `displayClassificationLeaf` 不再調用 `resourceSearch(英文關鍵字)` 充當正式分類；刪除 42 組 `taxonomyQueries`。分類與收藏、閱讀入口均保留原導航。
- 對有 canonical Work ID 的單書卡與詳細頁，不再透過書名匹配其他書籍的封面或圖版。僅接受該 Work 資料的直接封面/圖像指標，缺圖保持文字排版。
- 新增 `tests/p2-dawn-living-membership.cjs`；使用同等 mock Living root/shards 的 V8 執行測試驗證分類、Work ID 去重、36 上限的樣本模式、取消過期請求、禁止舊 keyword 路徑。主腳本與 adapter 靜態語法解析 PASS。
- **限制：** mock 測試不等於 Cloudflare 的真實 browser E2E；全 21 分片的數據品質、總量、封面與操作仍未通過實站逐件檢驗，PR 保留 Draft。

## 全量資料驗收與封面差異修復（2026-11-22）

GitHub Actions [run #45001795311](https://github.com/westsidewatch/westsidewatch.github.io/actions/runs/45001795311) 已實際跑完 449 個分片：Canonical 203448/21、Living 203448/21、封面實有 202428/407。Canon/Living 重複 ID 0、sha256 差異 0；封面 335 個 manifest count/sha256 漂移、對 Canonical 少 1020 Work ID，無重複 Work ID。圖像指標 200417，無圖 2011，未逐 URL 測試。

現行 `scripts/audit-dawn-library-shards.cjs` v2 會產生 `coverReconciliation` 的逐 Work 和逐 shard 對賬清單，供原 Admission/Build pipeline 修復。P2 不能為求畫面整齊擅自改寫館藏權威或封面來源。

## 2026-11-22 下一工程關卡：封面缺失 Work 的原權威修復候選（CI 已驗收）

**根據 GitHub Actions v2 真實完整性報告**：1,020 個 canonical Work 缺少 Cover Preview 行；335 個分片 manifest 宣告 count/hash 漂移。v2 全名單 artifact: [run #45001956068](https://github.com/westsidewatch/westsidewatch.github.io/actions/runs/45001956068)。

已新增 `scripts/stage-dawn-cover-reconciliation.cjs`，以 `canonical/root.json` 的原始 21 個 shard 的 metadata 為權威，讀取既有 407 個 Cover Preview shards，不覆寫它們；為 1,020 缺口建立與 canonical ID、原書名、作者、語言一致的 **text-only / dawn-placeholder** 預覽紀錄，不冒充已驗證封面，並計算正確 count/sha256/offset 的候選 root。

**實際完成的候選驗收**：GitHub Actions [run #45003268137](https://github.com/westsidewatch/westsidewatch.github.io/actions/runs/45003268137) SUCCESS；產物 [dawn-cover-staged-reconciliation](https://github.com/westsidewatch/westsidewatch.github.io/actions/runs/45003268137/artifacts/14746433995)。已解析 artifact 實檔：
- `covers-000408.json` 500 條；`covers-000409.json` 500 條；`covers-000410.json` 20 條。
- 新候選 `root.json`：**410 shards / 203,448 Works / sum(shards[].count)=203,448**。保留既有 407 個分片原位元組，修正它們的 root metadata；新增 3 片僅包含缺失 Work。
- `reconciliation-report.json` status PASS、original 202,428、missing 1,020、canonical total 203,448；有 ID 和真正原書名（如 OL100859W *Enlightened courage*）。
- `manifestChangedShards=407` 表示候選根清單中 407 個舊分片的 metadata（offset、count 或 SHA）至少一項有變化，**不是 407 個原始 JSON 檔都需要覆寫**。
- 候選 1,020 筆刻意不宣稱有真封面（`dawn-placeholder`）。這是「身份與館藏容量的修復候選」，不是「完成圖像修復」。

**出版門檻**：目前 artifact 尚未被複製進 PR 的對外靜態根，也未接入 P2 runtime；必須先驗證每個候選 shard 與新 root 的 checksum、跨 410 分片瀏覽邊界、全文/圖像來源，以及 Cloudflare desktop/mobile，才允許在隔離分支受控發布。不得自動合併 main。

## 2026-11-22 正式視覺施工｜P2 第二層原閱讀室（不是平行新大廳）

重新核實現行 P2 05 源碼後發現，原版三晨星／策展集／光譜**已由** `openCollection(kind)`、`showPortalCollection(kind)`、`renderPortalWorks()` 接線，並有 `p2-dawn-editorial-art.mjs` 的真實作品圖像。故否決在已存在的 `#dawn-wall` 外再創立平行 `p2-dawn-collection-hall.mjs`；不採用任何 `console.log` 空操作入口。

**本輪實際提交：**
- `static/experiments/p2-0105-dawn-preview.html`：在原 `#dawn-wall` 內新增閱讀室編輯刊頭、Canonical Work 數量、七大學科導航（`#dawn-department-grid`）。原三大型編輯入口／真實 2×2 圖像／個人書房未刪。
- `static/js/p2-0105-dawn-continuation.js`：從原 `living/root.json` 讀入七根分類；各學科點擊原 `openCollection()`，等待原 `renderCatalogueClassification()` 後調用 `displayClassificationGroup()`，可以繼續進 42 子類與已驗證的 `livingSubjectBooks(child.id)`。保留 V9 與返回路徑。
- `static/css/p2-0105-dawn-integrated.css`：新增 OS 紙色／金色／中文字體/英文字體規範下的閱讀室與 7 格字體牆，桌面 4 欄、平板/手機 2 欄，不覆寫原三大型編輯卡排布。
- `tests/p2-dawn-reading-hall.cjs`：以真實 Living root 驗證 7 根/42 葉、原三入口保留，模擬 7 次點擊均路由到原分類；`.github/workflows/p2-dawn-reading-hall.yml` 使其成為 PR gate。
- 測試 [GitHub Actions 45005646658](https://github.com/westsidewatch/westsidewatch.github.io/actions/runs/45005646658) **SUCCESS**；原 Living subject membership 測試同時成功。
- Cloudflare 隔離部署流程 [run 45005646644](https://github.com/westsidewatch/westsidewatch.github.io/actions/runs/45005646644) 的 Hugo build/Cloudflare deploy steps SUCCESS，Chomium 原館藏回歸結果需另核對。預覽部署分支 `pr-1411`；預覽入口 `/experiments/p2-0105-dawn-preview.html?layer=second&d=28.4`。

**不可宣稱：** 完整視覺得獎驗收、所有 203448 本的封面與閱讀權限、410 候選分片正式部署、正式主站合併；均未完成。


## R61｜第二、三層不得重複版塊大刊頭

**不可違反的既定層級**：版塊的獨立大刊頭只在 P2 第一層出現一次；進入 P2 第二、第三層後，版塊身份由最先出現的「經文方塊／鉛字母版」承接。不得在閱讀室、館藏、書籍詳情、導航或其他子層再次設置巨大的「黎明書局／DAWN LIBRARY／THE READING ROOM」版塊刊頭。這個規範已被此前工程多次確認，R57 重複刊頭屬實際設計回歸缺陷，R61 已從 HTML 實際刪除，不是單純隱藏。

三個編輯欄目 **三晨星／策展集／光譜** 應在原同一館藏牆作為一組完整的同級入口呈現：三卡同 OS `--ws-harvest: #b8944a` 收穫黃色底版，同等結構、同等版式，Bodoni Moda SC 英文主標大、Chiron Hei HK WS 200 中文次標小，現有真實書籍圖像位於黃底內窗。桌面三欄同排；小螢幕有序折行；不得使用三種互不相干的淡色紙板或大面積黑底。

變更檔案：`static/experiments/p2-0105-dawn-preview.html`、`static/css/p2-0105-dawn-integrated.css`、`static/js/p2-0105-dawn-continuation.js`；驗收 `tests/p2-dawn-os-visual-hierarchy.cjs` 與 `tests/p2-dawn-reading-hall.cjs` 已同步修改。保留原經文母版 iframe、三欄目真實資料、Living 7×42 分類、原 Codrops 展開書籍與 V9 轉場。正式主站未合併，仍只在隔離 PR #1411 驗收。


## R65｜OS 正文與展示中文字重分離

本次排版回歸缺陷：不應將「所有中文極細」誤解為「中文正文也 Chiron 200」。**原 OS 有明確的語義字體角色，不得互換。**

- 分類、欄目副標、卡片名稱、按鈕與導航：`--ws-type-display-zh` = Chiron Hei HK WS；展示性中文輕量角色 `--ws-weight-zh-air:200`，不得把 `900/bold` 當一般分類或個人書房標題。
- 連續閱讀正文：`--ws-type-reading-zh` = Noto Serif TC；標準字重 `400`；`--ws-type-scale-reading` 和 `--ws-type-leading-reading:1.82`。正文不應被覆蓋成 Chiron 200，也不得降到極小的 micro/meta 字級。
- 原已核實的經文方塊是特殊主視覺，其原版中文 900 重獨立保留，不受此修正污染；第二、三層不額外製作版塊大刊頭。
- R65 已修改第二層分類卡/標題、個人書房標題的 900 殘留；只對指定正文段落設置 Noto Serif 400；修改 `tests/p2-dawn-os-visual-hierarchy.cjs` 以真實瀏覽器 computed style 分別驗證展示 200 / 閱讀 400。P2 01–04、原經文 SVG/iframe、原館藏資料保持不動。
