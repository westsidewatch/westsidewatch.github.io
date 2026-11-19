# G1 R05｜搜尋興趣實測與匿名受眾理解度研究：執行紀錄

**版本：2026-11-09 / R05 v1.0**  
**狀態：IMPLEMENTATION READY / NO LIVE DATA**  
**已完成：** YouTube 官方口徑查核、36 列 Studio 採集表、離線匿名文字測試頁、離線結果彙總程式、結果判讀與驗收要求。  
**尚未完成：** YouTube Studio 帳號授權或數值採集、任何真人同意與參與、任何客觀市場需求排序。  
**已確定的研究邊界：** 中文世界福音為主；中英文雙語，不排除英語世界（D-005、D-006）。本階段沒有批准新頻道上線或內容定位。

## 1. YouTube Studio 官方功能與本研究可得性

2026-11-09 重新核對官方文件：

1. [YouTube Studio Trends 官方說明](https://support.google.com/youtubecreatorstudio/answer/11962757?co=GENIE.Platform%3DDesktop&hl=en)：2026-07 起逐步推出新介面；使用 `Studio → Analytics → Trends`，輸入搜尋詞並保存搜尋。
2. 顯示「Top searches」（近 28 天、依現有觀眾及已儲存詞）、Breakout videos、Recent videos、Shorts 的 content gaps；查詢時部分主題有「Audience interest」（very low 到 very high）。興趣根據最近 28 天、每週觀看大於 1,000 次的影片等訊號判定，**不等於任何查詢的月搜尋數**。
3. 短片 content gap 可以代表缺精確答案、缺新近或有品質的短片；**不證明長片市場缺口，也不代表某題一定值得製作**。
4. 這些訊號受帳號、語言、地區、裝置或可用資料所限。沒有顯示值寫 `UNAVAILABLE`，不是低需求或 0。
5. 自有影片若已上線，可再從 `Content → 選影片 → Analytics → Reach` 查看「YouTube Search terms」。該報告是**觀眾實際找到自己影片的搜尋詞**，與 Trends 對全站興趣的代理訊號不同。[官方 Reach](https://support.google.com/youtube/answer/9314355)
6. YouTube Analytics 的 Advanced Mode 可下載部分報告；但 Trends 每張卡片不保證有 CSV 匯出，**不能聲稱 Trends 有統一的匯出 API 或檔案**。[官方 Advanced Mode](https://support.google.com/youtube/answer/9717005)

**目前存取狀態（2026-11-09）：** 本工作環境沒有連接可讀取 YouTube Studio 的已授權來源。已發現 vidIQ 可選連接器，能提供關鍵字搜尋量**估計**與競品資訊，**不是**官方 Trends 的等價來源；沒有使用者明確連接前不能擷取數據、不能假裝已查了後台。

## 2. 搜尋興趣採集 SOP｜36 個初始查詢

資料表：[r05-studio-trends-capture-template.csv](./data/r05-studio-trends-capture-template.csv)。

- **12 個主題 × 3 個語言詞組（繁中、簡中、英文）＝ 36 行預填查詢**；資料列全部 `NOT_CAPTURED`，**沒有預填任何搜尋量或興趣分數**。
- 用可授權的 YouTube Studio 在瀏覽器開啟 `https://studio.youtube.com/`，進入 `Analytics → Trends`；依 CSV 的逐行詞查找、保留關鍵字、抄下可見的「Top searches」「Audience interest」「Breakout videos」「Recent videos」「Shorts content gap」。
- 每一行記錄 **UTC 觀測日、頻道上下文、實際介面語言／地域（若可知）、觀察結果、截圖或可追溯的來源檔**。只有介面能切換地區時才記錄實際地域；不可把「我想研究香港」偽裝成實際以香港為條件篩選的 Studio 資料。
- `top_searches_28d` 填實際顯示的詞，不填自己猜測的對照詞；`audience_interest_band` 只填 Studio 真的顯示的 very low / low / medium / high / very high（或原樣本地化詞）；`shorts_content_gap` 只填其明確提示（TRUE / FALSE / UNAVAILABLE）。
- 如果頁面沒有某功能，`capture_status = UNAVAILABLE`，寫明原因，**不得把 0 寫作沒有搜尋量**。
- 多個帳號不能不經標記合併。Studio 的建議會受**既有頻道觀眾**影響，尚未經營的新頻道可能較缺個人化資料。要分析初訪中文世界的機會，務必把不同頻道背景與新頻道假設區分。
- 可輔以 [Google Trends 相對比較](https://trends.google.com/trends/) 作不同中文詞組的 YouTube Search 跨地區研究，但須保存相同時間窗、搜尋類型與相對指數口徑。0–100 是正規化**相對**值，不是實際每月搜尋次數。

### 搜尋數據評估規則

- 有官方 Studio 欄位／截圖：`E1-STUDIO`，**只代表該頻道上下文內的代理訊號**；
- 有 Google Trends 完整條件／匯出：`E1-TRENDS-RELATIVE`，記錄國家與詞組，可作相對比較；
- 有 vidIQ 搜尋量／競爭估計：`E1-ESTIMATE-THIRD-PARTY`，不可標示為 YouTube 官方資料；
- 只有網頁搜尋與影片：`E2-SUPPLY`，不得寫搜尋量或需求強度。

## 3. 匿名理解度試驗：已可直接使用的離線原型

測試工具：[tools/g1-anonymous-reading-test.html](./tools/g1-anonymous-reading-test.html)。

**如何使用：** 下載 HTML 並在本機現代瀏覽器開啟；這是一個**純文字閱讀測試**，不是已經完成的影片 A/B 留存測試。頁面無遠端 JS、字型、CDN、分析 SDK、Cookie、`fetch`、`localStorage` 或任何對伺服器的提交。測試者只在勾選知情同意後開始，完成兩題後自行決定是否下載 JSON，是否交給研究者是獨立選擇。

### 真正實作的內容

- **T1：耶穌是誰？** A 問題開場 / B 福音敘事情境開場；之後共用相同、經文已列查核基線的中文解釋。
- **T2：祭祖與孝道？** A 直接問題 / B 家庭情境；之後共用同一中文正文。
- 分組 `AB`（T1-A、T2-B）或 `BA`（T1-B、T2-A）在頁面開啟時隨機；閱讀先後亦隨機。**隨機分組不保證 16 人恰好 8/8**，必須看實際分布再分析；若需要嚴格等額配額，下一版須由研究管理員控制組別分配。
- 回答 3 條開放理解題（須**兩名人工評審按 R04 rubric 給 0–2 分**，不自動由 AI 斷定理解）；可跳過；對清晰、術語難度、尊重、下一步各填 1–5 分或不作答，另可提供困惑語句。
- **不詢問姓名、電子郵件、信仰身分、受洗史、國籍、移民或其他敏感個資**；受試者不應在自由文本寫入自己或他人的身分資訊。
- 結束後可在本地下載 JSON；沒有後台收集，也**不會讓研究者自動獲得測試結果**。若希望納入研究，必須由參與者主動通過事前核准的方式提供匿名檔案。這一方式利於隱私，但不構成有完整招募／提交功能的線上問卷平台。
- 英文受眾測試尚未實作：R05 第一版只採繁體中文文字。不得把它報成已完成中英雙語參與者比較。英語翻譯／文化校訂完成後，應另設同一套結構的英語版本。

## 4. 結果歸集與判讀

工具：[tools/summarize-g1-r05.py](./tools/summarize-g1-r05.py)。使用 Python 3 標準庫，無網路依賴。

```bash
python summarize-g1-r05.py ./anonymous-json-responses ./aggregate.csv
```

- 只讀取參與者**主動交付**的 `*.json` 檔案並驗證 schema、兩道題與 A/B 版本；輸出每個題目／版本的樣本數與四項 1–5 主觀感受的中位數。
- **不把任意自由文本寫進匯總 CSV**。人工評分理解題必須另行獨立進行；不得把「清楚」主觀分數當作理解正確的客觀分數。
- 試驗 sample size 16 僅供找到話術、詞彙、框架上的問題；不可宣稱統計顯著、跨華人市場代表性或可預測 YouTube CTR。
- 只有看了**文字**，不能聲稱獲得影片觀看留存結果；待完成有聲／視覺原型，才能做下一層媒體理解測試。
- 參與者若提供帶個人資訊的自由文本，研究者應先刪除或去識別化再分析；原始檔不可提交公開 GitHub、不能放入本專案或 Pull Request。
- 任何 A/B 結果須保留各組樣本數、缺失值、觀眾反饋；內容文字若被評判為誤解嚴重，先修正文稿，不因一版本看似更易吸引而忽視真實性。

## 5. 需要補的實測內容，及誰能完成

| 任務 | 本輪已做好 | 還需的真實行動 | 沒有時如何記 |
| --- | --- | --- | --- |
| 36 組官方搜尋訊號 | 官方欄位定義、CSV、觀測流程 | 有權限者進入 Studio 逐項擷取，或在取得同意後連接可讀的分析服務 | `NOT_CAPTURED`／`UNAVAILABLE` |
| 16 位受試者的知情同意 | 離線頁面、匿名問卷、隨機組別 | 真正邀請成年志願者並取得同意，選擇自行分享 JSON | `0 accepted responses`，不得假裝已做 |
| 中英雙語理解對照 | 中英術語核查框架及現有資源 | 英文腳本校譯、英語志願者試驗 | `NOT STARTED` |
| 研究判斷 | 審核與彙總工具 | 真實資料、兩位內容審核者及紀錄 | `G1 IN PROGRESS` |

## 6. G1 可以進入 G2 的決策條件（非形式性勾選）

- 每個候選高優先題能同時提供搜尋／受眾需求的明確來源、公開內容供應的清單與初訪者可理解的文本；資料缺失要明白標註。
- 可提出真正不同的「問題型」「聖經視覺敘事型」「生命對話型」比較包，並有工時、質檢、權利與中英製作成本。
- 受眾測試的目的只在於修正編輯品質，不以參與者對宗教的選擇作 KPI。
- 中文世界優先、中英文雙語的已批准方向不可在缺資料時被私自更改。
- **截至 2026-11-09 尚無真人數據、官方 Studio 測量值及完成的 G1 定位驗收。**

## 7. 來源

- YouTube Studio Trends（官方）https://support.google.com/youtubecreatorstudio/answer/11962757
- YouTube Reach / search terms（官方）https://support.google.com/youtube/answer/9314355
- YouTube Analytics Advanced Mode / export（官方）https://support.google.com/youtube/answer/9717005
- YouTube Analytics limited data（官方）https://support.google.com/youtubecreatorstudio/answer/9101241
- R04 理解度研究規格（內部）[r04-audience-comprehension-study-kit-2026-11-08.md](./r04-audience-comprehension-study-kit-2026-11-08.md)

**本工程已交付可執行採集與文字測試工具，但不能代替使用者的後台授權或真實志願者。**
