# PARADISO / 数片 — 搜尋引擎退化鑑識與修復（2026-11-22）

## 結論（已確認／未確認必須區分）

**已確認搜尋功能在移植時退化**。原始 `paradiso_engine_v1.zip/paradiso_engine/engine.py` 的 CLI 提供 `sources` 命令，掃描 `providers.json` 的多個 MacCMS 採源接口，解析多播放組及逐集 `vod_play_url`。此前 GitHub 的 `scripts/shupian_recovery/legacy_engine_core.py` 只保留 HLS 檢查等功能，**缺少來源發現命令**。

**另有獨立的執行環境故障**：2026-11-22 本地容器的 DNS 解析全部失敗，包含 `github.com`、`example.com`、`api.changzhang.tv` 與 `cj.ffzyapi.com`。原始命令六家 API 查詢均報 `NameResolutionError`，因此本次返回空列表不是來源不存在的證據；亦不能從中推斷六個供應商現在均已失效。

**尚無證據能證明在外部可正常連線的 GitHub Actions runner 上，全部來源也會失敗**。因而不能拿本地 DNS 故障推定所有環境都有同一結果，也不能謊稱新版已取得新的線上片源。

## 歷史成功有多少？原始證據怎麼說？

來源：用戶擁有的 `paradiso-sweep-evidence-2026-11-20.tar.gz`，其中 `sweep.json`、`REPORT.md`、三個 `decoded-*/verification.json` 與畫面證據。

| 日期 | 來源／工作 | 發現 | 分段初篩通過 | 不合格原因 |
| --- | --- | ---: | ---: | --- |
| 2026-11-20 | Changzhang | 12 | 10 | 2 筆分段讀取失敗 |
| 2026-11-20 | Feifan | 12 | 2 | 10 筆原始來源 HTTP 403 |
| 2026-11-20 | DYTT | 12 | 0 | 12 筆原始來源 HTTP 403 |
| 2026-11-20 | Jisu | 12 | 0 | 12 筆原始來源 HTTP 444 |
| **總計** | **48 個片目記錄** | **48** | **12** | **36** |

最早的海巡在約 2 分 48 秒內讀取四家可用片目列表，對首集進行 M3U8 及三位置分段 HTTP 抽樣。另從其中三條來源各抽 7 個位置，得到**21/21 個可解碼的抽樣幀**；未見博彩廣告，但**未完成全片、全季無廣告及網站實播認證**。所以該階段「搜尋與網路分段初篩有成果」是有證據的；「已取得 12 部乾淨可看完整作品」則沒有證據。

## 退化因果鏈

1. **工程移植縮減核心**：從原 `engine.py` CLI 遺失 `sources`，保留下來的模組主要是檢驗／審批。這是無需依賴網路即可核對的回退。
2. **搜尋任務被錯誤轉向單部作品和靜態片單**：只增加作品資訊、海報和舊候選，而沒有持續執行多站大範圍反向採源；網站發展與核心引擎分離。
3. **本地 DNS 故障**：將 `NameResolutionError` 當成普通「找不到」，使六家接口看上去全部零結果。應先進行基礎網路診斷，另在具有外網連線的受控執行環境測試。
4. **新搜尋器第一版也存在算法弱點**：以 `美剧`、`经典电影` 等分類名作 `wd` 片名搜尋，不能替代類別索引；`ac=list` 一般不包含 `vod_play_url`，需要進一步 `ac=detail&ids=...`；四桶廣搜容易重複讀同一批目錄而錯誤統計。
5. **來源有效率從未等於成功播放率**：2026-11-20 的 48 筆中 34 筆來源清單讀取失敗，另兩筆分段讀取失敗。這些源本身的 HTTP 403/444，需要記入供應商健康度和失敗分類，但不等於網頁爬取「被對方完全封死」。

## 已實施的工程修正（不冒充線上驗收）

- `scripts/shupian_recovery/source_discovery.py`：恢復多來源、多語模糊、分頁候選搜尋；保留 MacCMS 多播放組／全部集數；`ac=list → ac=detail&ids` 解析媒體；**從各 API 的 class 分類表獲取各自 type_id，對 `ac=list&t=...` 分類索引進行遍歷**。同時阻止不受控的 API 跳轉。
- `scripts/shupian_recovery/four_category_round.py`：四個固定桶「最新美劇／英劇、日漫、經典電影、福音影視」同時執行；跨桶網路快取、按候選元資料產生 `MATCH/UNKNOWN/NO_MATCH` 分類證據、跨桶去重、遇到 DNS 不通時對該主機實施當輪熔斷，避免重複浪費請求。
- `scripts/shupian_recovery/engine_health.py`：逐站輸出 `INFRASTRUCTURE_DNS`、`API_OR_SCHEMA_FAILURE`、`DETAIL_OR_MEDIA_FAILURE`、`EMPTY_CATALOG` 或 `WORKING_DISCOVERY`，不允許把連線失敗寫成零片源。
- `scripts/shupian_recovery/test_source_discovery.py`、`test_four_category_round.py`、`test_engine_health.py`：包含分類 ID、列表詳情補全、四桶遍歷、來源容錯、DNS 故障分類等回歸測試；已新增測試代碼，不得未查 CI 便宣稱測試已通過。
- `.github/workflows/shupian-four-category-discovery.yml`：GitHub Actions 用真實外網環境運行四類搜尋並保存原始結果 artifact（已提交觸發配置，但**本次無可核對的 Actions 運行日誌／artifact**）。

本地對原始 ZIP 的獨立測試已實際執行：**10 tests passed**。這是**原始引擎**測試結果，不能拿來取代新移植模組的 CI 測試。

## 下一個必須取得的真實證據

1. 取得最新 GitHub Actions `数片 Legacy Engine Recovery Tests` 與 `PARADISO four-category discovery live experiment` 的運行日誌及 artifacts，確認新版程式有否語法、運行、網路錯誤。
2. 在可連外的受控環境執行 `python3 scripts/shupian_recovery/engine_health.py`，逐站分辨 DNS、HTTP 403/444、JSON schema、分類索引、detail URL、媒體 URL；按實際通過率決定優先爬取來源，而不是盲目把六家當成同等有效。
3. 同一輪四大類動態廣搜，對實際匹配候選逐集執行 HLS 廣告標記與解碼驗證；未能辨識的作品不得因出現在某個搜尋桶便算作類別命中。
4. 只有上述可核對結果在正式「数片」網頁完成實際播放及無廣告檢驗，才符合用戶指定的**四關閉環交付標準**。**當前仍未完成第四關，不得報稱本輪已交付。**

## 多雷探索：搜尋效率與爬取架構

**先適配真實 API，再考慮瀏覽器模擬或複雜反爬技術**。MacCMS v10 官方 `Provide.php` 區分 `list` 與 `detail`；分類 ID 因站不同需分別發現。以 API 索引及詳情補全做主路徑，Scrapy 的多域名廣域併發與可恢復排程做中期方案，Scrapling／Playwright 僅對允許抓取而 API 不足的動態頁面按需採用。對來源故障做指數退避與熔斷，避免 403/444 高成本重試；遵守站點存取規則，不繞過 DRM 或其他安全保護。

來源：
- https://github.com/magicblack/maccms10/blob/master/application/api/controller/Provide.php
- https://www.maccms.club/docs/integrations/provide
- https://docs.scrapy.org/en/latest/topics/broad-crawls.html
- https://docs.scrapy.org/en/latest/topics/scheduler.html
- https://playwright.dev/python/docs/network
