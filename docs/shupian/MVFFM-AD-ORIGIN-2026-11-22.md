# PARADISO／数片 — mvffm.net 廣告來源反向鑑識及核心升級

**案件頁面：** https://www.mvffm.net/drama/420952/  
**原始問題：** 影視播放突然出現賭場廣告，究竟是影像本體、HLS 分段，還是網站／第三方播放器附加腳本？  
**調查日期：** 2026-11-22  
**狀態：** 既有歷史頁面證據已找到；本次指定頁面未成功讀取，不能冒稱已抓到目前 HTML 或 M3U8。

## P0 — 已找到的早期反向分析：不能再遺失

**2026-09-27**，外部公開專案 [weber87na/mvffm-redirect-guard](https://github.com/weber87na/mvffm-redirect-guard) 已對 **mvffm.net** 做過針對性逆向檢查，並寫出 Chrome Manifest V3 擴充元件。它不是泛用的 Scrapling／Firecrawl，也不是推定的影片源；它才是此網站**已存在的、可追溯的現場分析與防跳轉技術**。原專案 README 記錄：

1. 當時頁面有壓縮腳本在 `mousedown` 上觸發，參考 `localStorage` 的 `shown_at`，約一小時節流，並在離站後可能清理。
2. 觸發時用 `window.open` 或臨時 `iframe` 開啟動態生成的站外地址，因此會出現間歇性「亂跳」。
3. 原作者採用頁面腳本防護、`declarativeNetRequest` 的站外頂層跳轉限制，及 `webNavigation.onCreatedNavigationTarget` 的第三方 iframe 彈窗管理。
4. **不得粗暴阻斷全部 iframe 或 media 請求**，否則可能直接破壞影片播放。
5. 上述是 **2026-09-27 當時的站點觀察**，不能直接證明 11 月 22 日指定的 `/drama/420952/` 仍使用相同腳本；但它提供了網站層廣告的高價值技術指紋。

**本次限定性判斷：** mvffm.net 曾經確有**網站／播放器頁面層的跳轉／彈窗廣告機制**。這使「站點腳本或第三方 iframe 加入賭場廣告」成為有歷史實證支持的假設，**不能直接判定影片源的 HLS 片段已被污染**。沒有當次 HAR／HLS／解碼畫面就不能宣稱完全排除影片內嵌廣告。

## 一次逆向採集須產生三類互相獨立的證據

| 分層 | 證據來源 | 判定方法 | 禁止混淆 |
| --- | --- | --- | --- |
| A. 網站／播放器層 | 頁面 HTML、JS、Click/Mouse 監聽器、外部 iframe、瀏覽器 HAR 與開頁面事件 | `mousedown`、`shown_at`、`window.open`、站外彈窗、可疑網路 URL；要有真正發生的請求／跳轉才能高信心歸因 | HTML 出現 `window.open` 字串不等於真有賭場彈窗 |
| B. HLS／清單層 | `m3u8` master/media playlists、播放時段、分段 | `EXT-X-DATERANGE`／`CUE-OUT`／SCTE-35／疑似 ad segments、前中後片段及時間軸驗證 | 無標記不等於沒有廣告 |
| C. 影片畫面內嵌 | 合法取得的影片解碼影格及音訊取樣 | 廣告畫面比對、時段核對、人工抽檢；仍不能以抽樣當全片認證 | 網站彈窗不能當作影片畫面被污染 |

## 已正式接入 PARADISO 的診斷功能

- `scripts/shupian_recovery/media_ad_origin.py`：離線讀取**保存的 HTML／HLS／HAR 證據**，把頁面彈窗線索、第三方請求、M3U8 廣告標記及**影片內嵌狀態不明**分開輸出。此階段不需要直播網站可訪問，不會自行下載或公播影片。
- `scripts/shupian_recovery/test_media_ad_origin.py`：至少四組回歸樣例：頁面腳本可疑但 HLS 無廣告標記、HLS 有廣告標記但網站未觀測、HAR 顯示可疑第三方請求、沒有證據時必須回答「未判定」。
- CLI 範例：`python3 scripts/shupian_recovery/media_ad_origin.py --html saved-page.html --har saved-network.har --hls saved-manifest.m3u8 --output mvffm-origin.json`。

**必要的後續整合：** 在獲得可訪問頁面的受控瀏覽器網路記錄後，用來源追蹤 `page → iframe/player → master m3u8 → media m3u8 → segments` 建立關聯；對比阻擋站外頂層開頁前後是否仍正常播放。若廣告消失且媒體請求／解碼保持一致，支持「網站層干擾」；若廣告出現在已解碼影格內，進一步回查清單／分段。測試不得繞過 DRM 或存取控制。

## 重要調查糾偏

此前將「更新的反向爬蟲」匆忙猜為 Firecrawl Local／Scrapling，忽略用戶**實際提供的反向研究目標 mvffm.net**；這項漏查已造成方向錯誤。本案件採用**真實站點已觀察到的技術指紋**作為優先證據，不以通用爬蟲框架取代實地鑑識。

## 每一輪的四關驗收

① 搜尋與逆向發現媒體源；② 分層去廣告與質量判斷；③ 播放穩定性、跳轉／彈窗是否消失、影片內容是否正確；④ 結果與證據落地「数片」網頁。不能完成第④關就不可報稱本輪已通過。此案件目前完成歷史線索還原與**分層鑑識程式提交**，但**現場抓取、播放及網頁驗收仍未完成**。

**來源：**
- https://github.com/weber87na/mvffm-redirect-guard
- https://www.mvffm.net/drama/420952/ （本次目標，遠端擷取失敗）
- https://github.com/westsidewatch/westsidewatch.github.io/blob/main/docs/shupian/ENGINE-REGRESSION-FORENSICS-2026-11-22.md


## 2026-11-22 回到最初網站的「反向工具完整性審計」

**唯一指定的起始觀測頁：** `https://www.mvffm.net/drama/420952/`。原始網站鑑識／廣告追蹤不能被其他劇集、一般片源關鍵字或 Scrapling/Firecrawl 工具名稱取代。

重新逐檔核對外部舊工程 `weber87na/mvffm-redirect-guard`：
- `manifest.json` 使用 Chrome MV3、`document_start`、MAIN／ISOLATED worlds、`webNavigation` 與 `declarativeNetRequest`。
- `page-guard.js` 具可執行的 `window.addEventListener('mousedown', ...)` 特徵分析、`shown_at` 監聽器略過、`window.open` 攔截、站外連結／Navigate API 防護，而非僅對 HTML 做文字搜尋。
- `background.js` 經 `webNavigation.onCreatedNavigationTarget` 判定第三方 iframe 發起的新分頁，並可按狀態啟用／停用網路規則。
- `rules.json` 僅阻止由 mvffm 起始的**站外頂層導覽**，不全面阻斷 `sub_frame` 或 `media`，因此避免以去廣告為由毀掉影片播放。
- `state-bridge.js` 管理 MAIN 與擴充功能儲存狀態同步。

**當前工程核對：** `scripts/shupian_recovery/media_ad_origin.py` 是離線 HTML／HAR／HLS 判定器，**沒有瀏覽器事件注入、沒有實際窗口／iframe 監測、沒有分頁導航生命週期追蹤**。原統一採集路徑 `tools/dore-exploration/dore_acquire.py` 在目前主分支指定路徑也是 404。原 mvffm 擴充功能存在外部 GitHub 倉庫，但**沒有證據證明它曾經已集成在 PARADISO 主線**，所以精確說法是「關鍵動態逆向能力在 PARADISO 缺失」，不是「外部擴充功能原始碼已被刪除」。

**本次已修復的一部分：** 新增 `scripts/shupian_recovery/mvffm_live_reverse.py`，用 Playwright `add_init_script` 在目標頁面執行前注入**只觀測、不阻擋媒體**的事件追蹤，蒐集 `mousedown`、`shown_at` 讀寫、`window.open`、臨時 iframe、彈窗／導航、媒體資源路徑與 JS 錯誤，輸出經過 URL query 脫敏的 JSON。支援明確指定播放按鈕選擇器時再做點擊對照。新增 `test_mvffm_live_reverse.py` 檢查此能力不可再次退化。另有 `.github/workflows/shupian-mvffm-reverse.yml` 用 GitHub Runner 做只觀測的實際頁面測試並保存 artifact。

**未修復／尚未證明：** PARADISO 並未直接引入外部 MV3 擴充功能的四層防護，也尚未通過頁面「允許彈窗／防護後播放」的 A/B 驗證。指定頁面目前從 web 讀取顯示 DisabledError，本地容器 DNS 也無法解析 mvffm.net，**不能聲稱已成功執行當前網頁的實際逆向或確認賭場廣告來源**。需核對 CI artifacts 的現場事件、再比對影片播放器與 HLS，經過四關到網站交付方可結案。

**防回退硬規則：** 任何「反向爬蟲／去廣告工具恢復」宣稱都必須有 `site URL → browser event instrumentation → navigation/popup/request graph → media-vs-site attribution → playback verification → site delivery` 的逐項證據。僅有 MacCMS API 索引、靜態分析、歷史 README、Scrapling／Firecrawl 名稱均不可替代原網站動態逆向。
