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


## R67｜中文館藏原書封面補完與空白分類修復

- `static/dawn-library/chinese-collection.json` 保有原 **47 個 canonical Chinese Work IDs**；1 部《靈歷集光》沿用其 Project Gutenberg 指標，原 **46 部廣學會（CLSC）** 在此版全部從 Yale Divinity Library / HKBU CLSC **同一書籍的原掃描 PDF** 擷取封面或題名頁，生成實體 WebP 46 張於 `static/dawn-library/chinese-facsimile-covers/`。
- 來源映射以 `https://adhoc.yalepages.org/Collections/HKBU/CLSC/clsc_list.js` 的 692 條 `title/author/year/filename` 明確索引，檔案由 `https://divinity-adhoc.library.yale.edu/HKBU/CLSC/` 讀取，兩個同名不同版《宗教道德教育學》（1920）／《基督之友》（1929）使用年份解歧。源檔、頁碼、掃描圖 SHA-256 全寫入 Work cover provenance，來源性質為 **原書封面／掃描題名頁，不可宣稱是現代商品封面**。
- 真正二進位 GitHub 資產提交：`0e8487186019fc3977a4f931df22c691d29e52c1`；此來源只在 **PR #1411 隔離分支**，未覆寫主站。
- `static/js/p2-0105-dawn-continuation.js` 接通中文單書卡與分類封面，禁止單書使用同名異版替代。修復先前 `for (const [i,[domain,items]] of subgroups.entries())` 的錯誤解構（導致 `domain.split is not a function` 和整面書牆清空），調整為 `[...subgroups.entries()].entries()`。分類卡首圖遇外站來源失敗時，可從 **本分類內其他已核實作品的原掃描** 選擇下一張，不會把其他類別封面混入該類，也不會改動單書的封面身份。
- 真實 **R67** Chromium [中文 47 原書封面 gate #45034357332](https://github.com/westsidewatch/westsidewatch.github.io/actions/runs/45034357332) **SUCCESS**。檢查 46 本地 WebP 存在、HTTP 200、SHA-256 與各 Work provenance 一致、桌面與手機中文入口、子分類和單書圖片載入；證據 [browser artifact #14759140640](https://github.com/westsidewatch/westsidewatch.github.io/actions/runs/45034357332/artifacts/14759140640)。
- [Cloudflare R67 隔離預覽](https://pr-1411.westsidewatch-github-io.pages.dev/experiments/p2-0105-dawn-preview.html?layer=catalogue&category=zh&d=28.4&v=r67) 已部署；獨立首頁 OS 視覺 gate 尚有失敗，**不可因此宣告整個 P2 已完成／可合併**。剩下 Gutenberg 單一外站封面 URL 的可用性並未獲本地 46-WebP 雜湊 gate 確認。


## R69｜當代中文與中文譯作擴源研究

2026-11-22 新增**正式來源發現資料集** `static/dawn-library/chinese-contemporary-discovery.json`，六個可追溯出版者/圖書館/研究入口，首輪核對七部現代中文書目（四部中文譯作、三部中文原創），每部有候選識別 `dawn:discovery:zh:*`、作者、中文及原文資訊（能核對才填）、來源出版社、具體作品頁、書目／閱讀狀態、版權與取用限制。七部僅屬 **source discovery**，未更改原 47 部中文 Canonical Works，亦未納入 203,448 Work Count。

**翻譯與來源：**
- 馬丁路德《一個簡單的祈禱方法－給理髮師彼得的信》，基督教電子書圖書館（繁中）。書號 TC01004，ISBN 9780645448535。
- 慕安德烈《不住禱告》，同館繁中譯本，書號 TC01027，ISBN 9781923383005。
- Robert Preus《認識協同書的神學》，李明知／魯思豪譯，中華福音道路德會，2022。
- 《協同書：基督教信義宗信仰告白，信徒版》，闞小玲譯，路德傳產基金會 2021，ISBN 9789869640336。
- 中文著作：唐佑之《系統神學叢書07－凡人論》、聶錦勳《神恩六記》、李吳惠冰《師母手記》，各具出版者書籍詳頁。

主要後續入口：`chinachristianbooks.org`（中文翻譯改教經典）、`bible.org/chinese/t`（CNET 中文譯經與研究資料：版權限制明示）、GETS 神學院開放館藏導航、信義宗神學院中文電子資源。資訊有些屬外部出版社訂閱或圖書館權限，不代表本站有權重製全文及封面。原始已證實的 publisher cover URLs 有四筆，但仍須以瀏覽器 HTTP 載入與授權分別查核。不要為缺封面的候選書偽造別種書封。

**原 P2 第二層交互接入：** 在 `displayChineseGroups()` 保留所有原中文分類與 47 部數量，另增獨立的「當代中文與譯作」來源欄目；選書第一次點擊採用原 Codrops in-grid expander，不轉跳，第二次明確點擊「前往出版方查看此書」才訪問官方頁面。候選書籍與 canonical Works 分開處理，不允許直接計入讀者 Personal Dawn 的既有 Work 身份；未授權全文不複製入本站。用 `tests/p2-dawn-chinese-contemporary.cjs` 驗證 7 部／4 譯作／不改 47、來源身份與雙步交互，CI `.github/workflows/p2-dawn-chinese-covers.yml`。

本輪另外修復原七大學科封面牆空白源頭：`refreshCategoryCovers()` 用 detached `new Image()` 加 `loading='lazy'`，載入事件可能永不觸發；改為提前以 eager 載入再插入。此錯誤與新增中文譯作無關但必須共同驗收。


**R69 補充發現：真正可合法外部閱讀的新譯作來源**
- `Frame-Poythress / P&R China`：出版社計畫逐年推出 450–500 部簡體中文譯作，現有「牧者／家庭／學生」分系列及官方下載入口。版權條款允許在其他網頁放置**連到官方頁或官方 PDF** 的連結，嚴禁將 PDF 上傳別站，亦不可編改；故 Dawn 只收錄書目及官方來源連結，絕不把其 PDF／封面拷入本站（https://frame-poythress.org/chinese-zw/）。
- `9Marks 繁體書庫`：已找到 4 部具體可核對的中文譯作與出版方獨立書頁：《認識大使命》（Mark Dever）、《解經式講道》（David Helm）、《健康的教會成員》（Thabiti Anyabwile）、《為何相信聖經》（Greg Gilbert）。有官方 ePub／下載入口，但明確僅供個人閱讀，禁轉載到其他網站；只做 Dawn 外部查找、預覽、再確認出版方來源之二步操作。
- `澳洲中信 CCMA`：文字事工網頁公開至少 7 部中文 PDF 作品與 2026 年的繁簡《中信月刊》，可在官方站直接閱讀。先列為官方可讀書源；如需任何全文鏡像與封面再利用，仍須檢查其授權。
- 因此此次來源資料集增為 **9 個來源通路／11 部逐冊候選，其中 8 部已確認屬中文譯作、3 部當代中文原著**。不要把「P&R 目標 450–500 部」當成已驗證出版數，也不要把九標誌的免費個人下載誤判為網站可重製授權。


## R73｜出版社導覽：公開文案與內部工程隔離

使用者指出 R72「當代中文與譯作」頁面仍展示「已核對的出版方書目與譯本線索；尚未獲本站全文轉載授權」和預覽中「本站沒有複製受版權保護的全文」。這些是**來源研究及授權審查的工程語言，不是讀者書籍介紹**，違反 `docs/design/WESTSIDE-EDITORIAL-MANUAL.md` §11 的公開網站文案隔離。

**書局定位正式固定**：黎明書局為具原創編輯與策展選書的閱讀導覽／出版方宣傳出口，讀者在書局看到書名、作者、題材、出版方、書影、簡短選書介紹，首先原頁展開預覽；讀者確認有興趣後再自行前往出版方介紹頁或其提供的閱讀通路。書局沒有在此工作線進行全文轉載；不得以「我們沒有轉載／未取得轉載權」之類工程風險自述充斥讀者頁。授權與不鏡像全文的限制仍保留在研究 JSON、內部手冊及代碼審核，以保護出版方，與對外文案完全分離。

R73 修改 JS 原始輸出而不是 CSS 隱藏：中文現代館藏版頭改為讀者閱讀邀請，單書預覽根據原始資料的主題和出版方給出中性引介；英文欄目紙牌 `DAWN · SOURCE EDITION` 改成 `CHINESE TRANSLATIONS / CHINESE BOOKS`；共用 Codrops 預覽模組去除內部 `WORK ID`、`原書書名待核對` 等不必要的讀者文案，出版方入口改為「前往出版方了解本書」。原有具體作品來源頁、原 Work IDs、兩步互動和出版方權利資料不變。

`tests/p2-dawn-chinese-contemporary.cjs` 新增真實瀏覽器顯示文案的禁止字串核驗，防止「已核對／未獲本站／沒有複製／受版權保護／SOURCE EDITION／WORK ID／QA／PR／commit」再進讀者介面；仍驗證第一次點書不轉跳、第二次點選出版社入口才離站。不可在讀者介面硬塞內部法律或工程說明。


## R74｜中文館藏當代優先、早期文獻後置

**已確定的中文館藏策展順序**：黎明書局中文書籍以當代中文原著及中文譯作為**入口和首頁主視覺**。先讓讀者看見當代的神學、講道、教會生活、禱告與靈修出版物，再於後段進入早期中文基督教文獻與古籍。此前先展示 47 部早期館藏、把 11 部當代著作放到分類最後的次序是錯誤的，不能以古籍封面已補齊來合理化。

R74 正式修正原 `static/js/p2-0105-dawn-continuation.js`：
- 點擊 `#dawn-primary-chinese`、開啟 `?category=zh` 或 `?category=zh-modern` 都先進入當代中文與譯作的實際書影牆。
- 讀者在當代書牆後方可選「閱讀早期中文古籍 · 47 部」，才回到原分類頁。中文分類頁依序排列當代入口、再是原四十七冊所屬歷史分類；不刪除或重排 canonical Work IDs。
- 原舊分類之直接驗收路徑為 `?category=zh-archive`，保留原 Yale 中文古籍／封面驗收；既有 46 張本地原書掃描、1 本 Gutenberg 書、真正出版方來源資料全部保留。
- 首層中文分類圖塊以「中文圖書／當代著作與譯本」進入當代書牆，而不是先用 47 部古籍定義中文書局；頂部主導航移除只代表古籍數量的「47 部」，避免向讀者造成錯誤館藏印象。
- Codrops 選書預覽、逐冊來源出版方導流、OS 中英字重、收穫黃識別不改動。

新瀏覽器 `tests/p2-dawn-chinese-contemporary.cjs` 必須驗證：中文入口不需額外點擊即顯示當代書牆；11 部書源與八部譯作現存；前後章次正確、原古籍完整保留，點擊主導航可由古籍返回當代。早期封面驗收 `tests/p2-dawn-chinese-covers.cjs` 經明確 `zh-archive` 路徑驗證。工程未合併主站，仍留於 Draft PR #1411。


## R76｜字體方塊 → 書籍封面展開

正式採用的兩段式視覺語法：**當代中文書牆首先全部採用收穫黃的完整字體方塊（中文 Chiron Hei HK WS 200；原書名、作者、主題與英文欄目填滿方塊）。點選方塊，才在同頁原 Codrops 展開區顯示這本書的真實封面、作者、介紹及出版方入口。** 這個先抽象／再實體化的視覺對照是有意設計，不得再提前把封面塞入第一層方塊。切換另一方塊沿用展開區原有的動效；第一次點擊不外跳，第二次讀者明確選擇才前往出版方。

R76 原始工程：`static/js/p2-0105-dawn-continuation.js` 移除當代分類書牆的提前封面載入；真實封面 URL 原值繼續交給 `static/js/p2-dawn-expanding-book-preview.mjs`，展開後才顯示。CSS `static/css/p2-0105-dawn-integrated.css` 固定書牆方塊 1:1 的 OS 收穫黃文字構圖；展開時保留原真實封面比例，不裁書封、也不混用封面。原有 47 部古籍的數位掃描書目及前後主次、11 部當代來源均不變。

驗收：`tests/p2-dawn-chinese-contemporary.cjs` 逐卡檢查方塊 **沒有 img／沒有錯書封、收穫黃、尺寸為正方形、完整書名與作者**；點選後在 `#dawn-book-expanding-preview` 檢查真實同書封面 URL，繼續驗證出版社入口只在明確第二次操作才觸發。GitHub [中文封面與新譯作瀏覽器驗收 #45067968015](https://github.com/westsidewatch/westsidewatch.github.io/actions/runs/45067968015) **SUCCESS**，桌面與手機截圖已存檔。隔離 Cloudflare 預覽已部署；全域 P2 Design OS gate 另有失敗，因此不宣稱整站完成、不合併主站。


## R78｜真實封面填滿當代中文方塊

本輪承認此前 R76 的關鍵錯誤：使用者明確要求 **「方塊內就是封面圖，封面必須填滿方塊」**，而非「收穫黃色塊填滿、點開才出現封面」。先前錯做成無圖片的文字方塊。R78 已**重新在原工程**修正：中文當代書牆每塊 1:1 卡片用與本書正確對應的出版方原始封面圖片以 `object-fit:cover` **滿版顯示**；只有點開 Codrops 原位展開後，才看到完整、不裁切的原書書封、書名、介紹及出版社導流。第一段是滿版圖像、第二段是完整書籍，不應再顛倒。

來源不可互換：九部符合原書局免費閱讀標準的當代中文作品，完整找到 **9/9 官方出版方的相同作品封面 URL**；四部 9Marks 繁中作品（《認識大使命》《解經式講道》《健康的教會成員》《為何相信聖經》）引用其官方圖像 CDN；其餘五部基督教電子書圖書館作品使用同一本書的公開商品圖。封面不下載到本站、不鏡像，不拿英文／不同版封面冒充，逐筆儲存 `coverProvenance`（出版方 URL、同書對應關係、外部使用說明）。發現九個圖片連結的 HTTP 200 且返回 MIME image/jpeg 或 image/png 的探測程序：`scripts/dawn-chinese-cover-audit.cjs`；GitHub [publisher jacket audit #45070552679](https://github.com/westsidewatch/westsidewatch.github.io/actions/runs/45070552679) 全 **9/9** URL 來源確認。

R78 原始工程修改：
- `static/dawn-library/chinese-contemporary-discovery.json`：九部都有同書來源封面。
- `static/js/p2-0105-dawn-continuation.js`：只以該作品自己的封面填滿縮圖；源圖片失效才退回可讀的同書原創標籤，且不會顯示空白、猜圖或誤植別本封面。
- `static/css/p2-0105-dawn-integrated.css`：現代書牆 square 1:1、`object-fit:cover` 佔滿，僅在展開區 `object-fit:contain` 完整顯示。
- `tests/p2-dawn-chinese-contemporary.cjs`：由舊「禁止在方塊中出現圖片」反轉為實際 computed style、九張圖的 naturalWidth 和方塊占幅驗收，並驗證展開的完整同書封面與出版方二段式導覽。

**不混淆三種驗收**：九個來源可下載（HTTP）不等於九張圖實際在網站展示；最後仍以 Chromium 桌面、手機與 Cloudflare 部署實際頁面為準。正式主站不合併，P2 V9 和其他版塊不修改。不得聲稱整站獲獎標準已通過。


### R78 實際瀏覽器驗收結果（9／9）

2026-11-22 GitHub Actions [#45070980489](https://github.com/westsidewatch/westsidewatch.github.io/actions/runs/45070980489) **SUCCESS**，Chromium 桌面 1440×900 與手機 390×844 證實：當代中文**9／9** 真實出版方圖像已載入且 `naturalWidth>120`；每張滿版覆蓋 1:1 方塊的 computed `object-fit:cover`、封面圖片 bounding box ≥ 卡片寬高；在卡片點擊展開時仍以**同一本書的來源 URL** 展示完整封面，改選下一本沒有跳轉，出版方需第二次明確點選才開啟。46 本 Yale CLSC 原始古籍掃描 SHA-256 與本地 HTTP 200 亦一併通過。保存的 Chromium 截圖 artifact [#14773131864](https://github.com/westsidewatch/westsidewatch.github.io/actions/runs/45070980489/artifacts/14773131864) 包含 `desktop-modern-chinese-source-wall.png`、`desktop-translation-expanded-preview.png`、`phone-modern-chinese-source-wall.png`、`phone-translation-expanded-preview.png`，以及原版中文、七學科壁的測試截圖。

外部來源獨立測試 [#45070552679](https://github.com/westsidewatch/westsidewatch.github.io/actions/runs/45070552679) **9／9** 官方封面皆 HTTP 200 且 MIME 真實圖片，沒有用未知書的封面。隔離 Cloudflare [#45070980439](https://github.com/westsidewatch/westsidewatch.github.io/actions/runs/45070980439) **部署成功**，但同流程整體仍因 Design OS 字體/導航 gate 失敗，沒有正式站合併；**封面子系統通過不等於 P2 所有驗收通過。**
