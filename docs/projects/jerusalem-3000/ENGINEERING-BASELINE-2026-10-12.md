# Jerusalem 3000 工程基線：M0 第一批

本文件記錄實測與候選審查，不宣告 M0、歷史復原或全時間軸完成。

## 版本

- 此工作基於 main `9e0d03333`；PR #1248 已合併。
- PR #1249 / `e2076d948`：待合併的王室城市草模，不計入已發佈主線。
- 線上量測 URL：https://westsidewatch.github.io/preview/jerusalem-3000/ 。本次沒有取得部署提交標記，不能以本機 main SHA 代替線上部署證明。

## 實測方法

使用 `scripts/measure_jerusalem_3000_baseline.mjs`，本機 headless Chromium、實際網路、沒有限速。桌面 1440×1000；mobile-viewport 390×844 是視窗模擬，不是真實手機。每個 profile 一次冷、一次暖載入，再往返早期／希律場景。CDP encoded bytes 包含協議相關開銷；ready 時間包含 networkidle 等待，不是首個可互動時間或 p95。

| Profile | 載入 | ready ms | CDP encoded bytes | 請求次數 |
|---|---|---:|---:|---:|
| desktop | cold | 1965 | 511846 | 60 |
| desktop | warm | 1145 | 38211 | 60 |
| mobile-viewport | cold | 1237 | 511190 | 60 |
| mobile-viewport | warm | 1067 | 38324 | 60 |

兩個 profile 在已載入的 David → Herodian → David → earliest 往返中，額外網路請求與傳輸均為 0；沒有 pageerror。這沒有量測 shared city 的第一次生成成本、FPS、20 次切換資源趨勢、真實手機性能或模型 token 成本。

暖啟動 Resource Timing 顯示地形 JSON 仍有約 16.7 KB transferSize；Herodian 物件包與 anchor-era-packs 各有重複請求。這是下一批資料 loader 合併與版本化快取的具體對象。CDP 與 Resource Timing 的統計邊界不同，不相加。

## 生成層與共同帳本落差

| 層 | 入口 | 共同資料現況 | 優先收斂 |
|---|---|---|---|
| 早期四期 | earliest-settlement.js | 場景資料與 metadata；未完全等同 TemporalCityCore ledger | 以 adapter 註冊來源、穩定 ID、物件與生命週期 |
| 王室候選 | royal-city.js（#1249） | inferred meshes 與段落切換 | 將聖殿、院落與城防變為資料物件，接入後代 |
| 第一聖殿／波斯／希臘化 | shared-era-runtime.js | 有 TemporalCityCore 與 projection | 替換縮放街網權威、保留帳本方法 |
| 希律主場景 | herodian-parcel-core.js、typology grammar、scene | 共同 core 與建築組裝 | 保留品質基準，審核 provisional 配準來源 |
| 其他舊期 | era morphology／inheritance | 多套生成與狀態規則 | 在前述 adapter 驗收後逐期遷移 |

共同地形已有，但 anchor pack 的 withheld、空間驗證的 pending、候選幾何與實际 runtime 狀態需要重新核對。更新資料狀態不能自動升級證據。

## 未合併 PR 審查建議

- #1171：針對舊 `eraCities`／`ensureEraCity`；目前 main 沒有這條路徑。建議標為被新 runtime 取代，避免直接套用。
- #1163：同樣修改舊路徑；可保留「隱藏 staging、可見性／診斷」意圖，需與新 runtime 比對，不能原樣合併。
- #1241：針對較新的 shared runtime，包含 Aelia、LRU 與測試。可作性能候選；下一步拆清快取能力與歷史資料，檢查在途取消、保留遺存依賴及資源預算。
- #1132：影響地塊與立面 grammar、另加 CI。此次只完成範圍審查；須在 M1/M2 統一基線後評估街面與幾何改動，暫不直接合併。
- #1249：保留為候選草模，後续接共同帳本與跨代狀態。仍依使用者授權合併。

以上是建議；本輪未合併、關閉或刪除上述 PR。

## Jev 與既有執行入口

當前會話無 Jev 工具；檢查的 PATH、Codex skills、常見 Hermes／local／config／工作目錄未發現 Jev/Jve 入口。這不證明其他主機沒有部署。現有 `127.0.0.1:4312/health` 回應 `ok:true`，service `dore-a2a-plus`；公布 speaker-cover、stage2 acceptance、compose、verify 四類設計能力，沒有 Jev。未讀出密鑰，未重新安裝，未建立 Gateway，也未透過 Jev 執行。

現有 Doré Context Packet 已可在本機索引整體規劃並保留祖先與來源 hash。先沿用它收斂上下文，Jev 接線獨立驗證；不得讓搜尋入口阻止資料盤點與契約工作。

## 下一批與完成門檻

1. M1：建立物件／來源／生命週期 adapter，先覆蓋 royal 候選與早期主體，不增加另一個權威 renderer。
2. 同一 loader 對同一版本資產去重；設計版本化快取更新規則，再比較冷暖數據。
3. 做大衛—所羅門—晚期—毀城—波斯的主體去向矩陣；未知記 unresolved，不用刪除假裝繼承。
4. 在固定硬體與網路測 shared first-generation、GPU 資源趨勢與真實手機；模型成本需可觀測的既有入口，現在不填虛構值。

M0 仍在進行：Jev 舊部署、模型成本與真實手機基線尚未完成。本輪的可用成果是候選審查、渲染層矩陣、可重跑量測工具與第一份線上數據。

## 共同資料入口：第二批

新增 city-data-loader.js，將 anchor 包、anchor 生命週期、Herodian ledger 與地塊配置的五個消費入口接入同一 document-lifetime loader。等價 URL 合併在途與已完成請求；structuredClone 隔離消費者修改；HTTP／JSON 失敗移除快取，可重試；可指定資產或全部失效。新頁面用 HTTP no-cache 重新驗證，不建立永久不更新的跨頁記憶快取。

同一電腦、同一 headless Chromium／Python 本機伺服器的改動前後 probe（各一次，非統計基準）：

| Profile | 項目 | 改動前 | 改動後 |
|---|---|---:|---:|
| desktop | cold CDP bytes | 702443 | 685058 |
| desktop | warm CDP bytes | 99462 | 64588 |
| desktop | 首屏請求 | 60 | 57 |
| mobile-viewport | cold CDP bytes | 702444 | 685068 |
| mobile-viewport | warm CDP bytes | 99462 | 64588 |
| mobile-viewport | 首屏請求 | 60 | 57 |

改動後四份共用資料均只請求一次；多出 loader 模組的一次請求計入總數。已載入時代往返仍沒有新增請求。CDN／正式站有壓縮與不同快取，不能把本機 bytes 直接當正式網站節省比例。這批沒有量測或宣稱模型 token、FPS、GPU 記憶體節省。

驗證：loader 單元測試覆蓋 URL 同一性、並行合併、消費者隔離、失效與 HTTP／JSON 重試；完整桌面／手機 viewport、18 期、原有缺資料處理通過。瀏覽器驗收加入四份資料各一次請求的檢查，CI 新增 loader 測試。

下一步仍是 M1 的物件來源／生命週期 adapter 與主體去向矩陣；本批只完成共同載入入口，沒有把所有 renderer 收斂或完成跨代繼承。
