# Changzhang 專項引擎實驗｜2026-11-22

## 判斷結論

這一輪**不可宣稱「核心已完全修復」**。原始引擎本地回歸測試 10/10 通過，源頭發現功能已在 GitHub 以獨立模組重建並增加分類遍歷／批量詳情功能，但此次容器 DNS 無法連線到 Changzhang 或 GitHub；因此未取得**當次、可驗證的廠長 API 命中及 HLS 分段結果**。測試中的外部執行程序需要有可核對的 Actions 日誌與 artifact 才能判斷是否恢復。

## 原始有效基準（已保存的實驗證據）

2026-11-20 `paradiso-sweep-evidence` 首輪 Changzhang 樣本：最新目錄 12 條，10 條首集 M3U8 前中後三位置分段讀取成功，2 條分段失敗；後續選定的首集樣本包括 148776／618，各完成 7/7 截圖解碼抽樣。這些紀錄只證明當時網路、解碼抽樣有效，**不能證明整部影視作品已完成無廣告認證**。

## 已重新核對的 Changzhang 專用入口

官方 `https://changzhang.tv/help/app` 在 2026-11-22 的搜尋索引中列明：
- 綜合 JSON API：`https://api.changzhang.tv/api.php/provide/vod/`
- 獨立 M3U8 資源：`https://api.changzhang.tv/api.php/provide/vod/from/changzhangm3u8/`
- `ac=list`：分類 `class.type_id / type_pid / type_name`、分頁 `pg` 和 `pagesize`
- `ac=detail&ids=1,2`：批量詳情，一次最多 100 IDs；播放組 `vod_play_from` 和 `vod_play_url`
- `t` 分類大類含子類；`wd` 關鍵詞；`h` 時段增量；`year` 年份範圍；`from=changzhangm3u8` 只返回 M3U8 播放組。

接口說明不是當次成功取得 JSON 的證據。**當前容器連線實測**：`requests.get('https://api.changzhang.tv/api.php/provide/vod/?ac=list&pg=1')` 因 `NameResolutionError` 失敗；`https://github.com` 同樣失敗。此結果是基礎網路故障，不能把它算作廠長搜尋零命中。

## 本輪專項掃描程序（新增核心增長）

`scripts/shupian_recovery/changzhang_sweep.py`：

1. 查廠長原生分類樹，辨認每個 ID 與子類後代，**不使用其他站的分類 ID**；
2. 同一輪覆蓋最新美／英劇、日本動漫、電影經典及福音影視；福音類別另外搜尋中英文相關詞，且保留類別是否有直接對應的證據；
3. 逐類遍歷 `ac=list&t=ID&pg=N&pagesize=M`，明確記錄限制、返回量、缺失欄位及錯誤；
4. 跨類去重後用 `ac=detail&ids=id1,id2...` 批量抓逐集 `m3u8/mp4/mpd`，保留全部播放組；
5. 在少量樣本上以既有 `shupian_source_audit.audit_one` 讀取清單與前／中／末分段；**每個唯一作品只選首條 HLS**，避免同劇多集偷換原來 10/12 的基準；
6. 產出總片目數、真正有媒體地址的作品數、唯一 HLS 地址數、各類分類命中、三位置抽樣及錯誤分類；
7. 原始 10/12 的比較，只有重新抽到至少 12 部**不同作品**、同等三位置檢查，才可標記 `comparable=true`。新樣本不同於歷史 12 部時也只能比較流程與抽樣比例，不能假稱同批影片的逐條回歸。

新的 GitHub Actions：`.github/workflows/shupian-changzhang-specialist.yml`，在 Ubuntu runner 執行回歸測試，再以最多每分類 5 頁／20 條、12 部不同作品 HLS 三位置抽樣做第一批外網掃描；上傳完整 JSON artifact，不會自動寫入公開影視網站。

## 成功標準：四關不可省略

**關 1** 搜尋：Chanzghang 有當次 JSON `list` + `detail` 的可追溯命中，四類全面報告、至少 12 部不同作品作可比樣本；**關 2** 去廣告：HLS cue、媒體分段及畫面廣告檢驗；**關 3** 播放：真實起播、跳轉和連續播放；**關 4** 網站：已驗證結果在 `static/shupian/` 正式頁面可見、可操作、可播並完成驗收。

**目前只完成專項程式與測試的提交；沒有當次外網掃描成功結果或網站播放證據，因此第一輪未完成。** 不得把 GitHub commit、歷史 10/12、模擬回歸測試或第三方官方文件冒充這四關的完成。

## 調查與工程源頭

- Changzhang 官方 API 文件：https://changzhang.tv/help/app
- MacCMS 10 官方資源采集：https://changzhang.tv/help/maccms10
- Changzhang 首頁目錄：https://changzhang.tv/
- 專項掃描器：`scripts/shupian_recovery/changzhang_sweep.py`
- 專項測試：`scripts/shupian_recovery/test_changzhang_sweep.py`
- CI：`.github/workflows/shupian-changzhang-specialist.yml`
- 2026-11-20 原始證據：`paradiso-sweep-evidence-2026-11-20.tar.gz` 的 `sweep.json` 和 `REPORT.md`（用戶檔案，未隨意公開分發）

## 2026-11-22 第二輪同站四關施工：實際變更與阻塞

**本輪目標固定：廠長 Changzhang，四個內容桶同時搜尋。** 不能以某部劇、舊《The Institute》或別站代替。本輪必須依 ① 搜尋 → ② 去廣告／品質 → ③ 播放驗證 → ④ 正式網站落地，且每關要有當次證據。

### 第①關——廠長原生搜尋

- 原始 `paradiso_engine_v1.zip` 單元測試已在本地執行：10/10 通過。**只證明原始程序離線回歸**。
- 專項掃描器 `scripts/shupian_recovery/changzhang_sweep.py` 已接廠長分類樹、逐類分頁、批量詳情及 M3U8 地址去重。
- 新增 **廠長 M3U8 專用接口二次查詢** `https://api.changzhang.tv/api.php/provide/vod/from/changzhangm3u8/`：當綜合詳情只有網頁播放組或未含可識別媒體地址時，用同一作品 ID 查專用來源；不刪除既有作品資料。新增 `test_hls_only_endpoint_recovers_missing_combined_stream` 的回歸測試。
- 本地 `https://api.changzhang.tv/api.php/provide/vod/?ac=list&pg=1` 仍因 `NameResolutionError` 失敗；對 `https://github.com` 的 DNS 也失敗。這是**當前容器連線障礙**，不等於廠長無片源。
- GitHub runner 專項 Workflow 有推送觸發和 artifact 上傳，但**目前無可讀取的最新運行結果**；不能聲稱已取得新的廠長片目／M3U8。

### 第②關——廣告與來源品質

- `scripts/shupian_source_audit.py` 已加入 `ad_manifest_signals()`，區分 HLS cue／DATERANGE／SCTE 等標記、可疑廣告分段名稱，以及單純三位置 HTTP bytes 成功；未見標記不等於無廣告。
- 新增 `test_hls_ad_signals.py`，分開測試 manifest ad cues、廣告路徑、未見標記但不應宣稱乾淨。
- 新版廠長的**當次 HLS 來源仍未擷取成功**，所以廣告判定無當次實測證據；絕不以 2026-11-20 歷史數據取代。

### 第③關——播放器與實際視頻

- 原網站播放器已有 HLS.js／Safari native HLS 及播放狀態處理，未擅自修改已存在的片庫。
- **目前未取得廠長來源的當次首幀、跳轉、連續播放或全片廣告結果**；第③關未通過。不得把單元測試或 HTTP 分段抽樣算成實際播放。

### 第④關——「数片」網頁落地

- 已在 `main/static/shupian/index.html` **和真正發布的 `gh-pages/shupian/index.html`** 增加同一個克制的廠長實驗狀態區，包含四類別及四關結果。沒有驗證的新來源不會變成可播放卡片。
- `main/static/shupian/recovery/changzhang-round-status.json` 與 `gh-pages/shupian/recovery/changzhang-round-status.json` 均已建立，記錄**2026-11-20 歷史 10/12 基準**與「本輪結果未取得」。新 `changzhang_status_export.py` 將 runner 原始掃描 JSON 轉成匿名化、無原始媒體地址的實驗摘要。
- `.github/workflows/shupian-changzhang-specialist.yml` 已增加**自動同步安全摘要至 main 和 gh-pages**，保留詳細結果只在 Actions artifacts；後續實際執行時可更新網站驗收資訊，但不能提前聲稱跑通。
- 本次已直接檢查兩個分支的摘要 JSON，狀態均仍是 `LIVE_RESULT_NOT_YET_VERIFIED`。**網站的實驗狀態呈現已寫入發布分支，不等於站內影片已驗收或 CDN 實際播放成功。**

**當次結論：四關尚未閉環，不得標記「完成」。** 已落地的是診斷／搜尋算法與網站證據面板；缺的是可連外環境的真實廠長 JSON、HLS 與媒體播放結果。下輪應從取得 GitHub Actions 實際運行日誌／artifact 著手，直接排除 runner 連線、程式 API 格式及 HLS 失敗根因，不要重新製作網站或遺失已修復的掃描器。


## 2026-11-22 外部 Runner 實際搜尋成功（10:20 UTC）

**本項取代前文「當次完全沒有來源結果」的過時觀察。** 已核對 GitHub `main/static/shupian/recovery/changzhang-round-status.json` 和 `gh-pages/shupian/recovery/changzhang-round-status.json`，兩份有效 JSON 的觀測時間均為 `2026-11-22T10:20:57.893876+00:00`。

| 指標 | 當次實測 |
| --- | ---: |
| 廠長不同片目 ID | 1,244 |
| 有已解析媒體來源的作品 | 834 |
| 不同 M3U8 地址 | 4,553 |
| 分段網路抽樣 | 12 |
| 抽樣通過 | 9 |
| 掃描器報告錯誤數 | 0 |
| 最新美／英劇分類片目／匹配 | 100 / 55 |
| 日本動漫分類片目／匹配 | 100 / 70 |
| 經典電影分類片目／匹配 | 1,000 / 90 |
| 福音影視分類片目／匹配 | 46 / 35 |

**嚴格解讀：** 數據證明廠長原生分類、詳情及 M3U8 來源恢復工作可以在 GitHub 可連外 Runner 上取得真實成果，故本地 DNS 故障不是廠長接口整體失效；**834 部並非已驗證可完整播放且無廣告的作品，4,553 條也不是已通過瀏覽器解碼的來源**。同樣地，歷史 2026-11-20 的 10/12 和本輪 9/12 的影片樣本並未證實同一批，不能直接判定演算法退步或進步。

**四關狀態（來源 JSON）：**
1. 搜尋 → `PARTIAL`（有真實片目與媒體地址，未逐條核實）；
2. 去廣告與品質 → `SAMPLED_NOT_CERTIFIED`（9/12 分段網路初篩通過，尚未完成全片廣告檢查）；
3. 實際瀏覽器播放 → `NOT_TESTED`（當次 JSON 尚無首幀和時間前進證據）；
4. 網頁落地 → `DIAGNOSTIC_ONLY`（已在 main 與 gh-pages 發布真實診斷面板，非媒體播放驗收）。

**網站同步事故與修復：** 當次發布分支 JSON 曾意外包含 `<<<<<<< HEAD`、`=======`、`>>>>>>>` Git 合併衝突標記，造成 JSON 無法解析。已直接以 main 合法 JSON 覆蓋 gh-pages，提交 `6249e28a`；另在 Workflow 增加同一工作流併發序列化、雙分支寫入前 `python3 -m json.tool` 格式驗證，防止將衝突檔案交付網站，提交 `8d109973`。

**第三關新工程：** 已增加 `changzhang_browser_probe.py`，從完成分段採樣且未見廣告標記的候選中選最多三個不同作品，在獨立 Chromium + HLS.js 沙盒檢查實際首幀／播放時間前進；結果由 `changzhang_status_export.py` 輸出到網站。此功能是新增程式及 CI 流程，**本次 10:20 UTC 的實測檔尚未包含其執行結果**。

下一次真正能宣稱本輪四關完成的前提：當次 HLS 廣告與內容檢驗、實際瀏覽器播放、合法授權與站內播放驗收全部有證據，不能僅依片目數或分段 HTTP 通過數宣布成功。
