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
