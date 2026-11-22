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
