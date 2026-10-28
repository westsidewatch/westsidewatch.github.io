# 拾字｜碑帖真跡集字 → SVG → AI 缺字補全（方法備忘 v1.0）

**建立：2026-10-28**  
**歸屬：拾字 · GLEAN／池底設 NODesign Chinese Logo Lab**  
**上位設計權威：[LOGO-RESEARCH-DESIGN-CENTER.md](./LOGO-RESEARCH-DESIGN-CENTER.md)**  
**狀態：方法已保存，非功能部署或正式 Logo 定稿。**

## 一、已確定的核心路線

**先從碑帖真跡找字、集字；再向量化；只在缺字時考慮 AI 補全。**

不為兩個字先訓練完整中文字體，也不直接用通用書法字型冒充歷史書家原帖。

流程：

1. **輸入目標文字**（「拾字」「西望」或任何中文字詞）。
2. **Source Board**：查現有字庫、碑帖釋文、博物館開放館藏／IIIF，對每個字獲得可追溯的原帖候選。
3. **裁字與校對**：保持原圖不可覆蓋；OCR 只提供字框／識別建議，逐字人工核對；保存頁碼、原圖尺寸、SHA-256、crop 座標、異體與權利狀態。
4. **Pairing Board**：優先同作品，其次同書家同書體／相近書寫狀態，再比較跨作品、跨書家混排；不因兩字單獨漂亮就宣稱已配成完整字標。
5. **Vector Board**：先使用現有 ImageMagick＋Potrace 路徑，並以 VTracer 試驗同源的 SVG 路徑；對照真跡筆畫，不可擅自修成「看似書法」的假字。
6. **Optical Board**：基線、比例、傾斜、重心、字距、墨量、負空間、行氣，保留原字與每次修改參數。
7. **Master**：每個字一個可追溯的向量群組；保留原裁字、來源、rights、派生關係和可重建的 canonical SVG。
8. **AI 只作缺字候選**：真跡查不到合適字時，從合法可用的參考字試生成，明確標 AI 衍生，人工驗字法與筆畫，不得冒稱書家親筆。
9. **實頁驗收**：在《拾字》工具與《西望》Contents 的真實版面比較桌面／手機、紙色／版畫／單色與縮放後的可讀性，避開文字碰撞；由人決定是否晉升 Master。

**禁止捷徑：**未知版權就直接收庫、未核對原頁就標名家、AI 字冒稱真跡、用美觀代替字形正確、默默覆寫原圖、在驗收前自動替換正式站點字標。

## 二、直接接入「拾字」既有四層架構，不另建管理系統

| 已有研究板 | 本方法增加的能力 | 必須保留 |
| --- | --- | --- |
| Source Board | 原帖影像、單字框、候選字、字源權威及使用權利 | 原始文件不可修改 |
| Pairing Board | 同書家／同帖／跨帖配字，筆勢與黑白平衡比較 | 每個字獨立 provenance |
| Optical Board | 參數化調整字距、重心、傾斜、筆畫比例 | 每次修改可逆可比較 |
| Master | 逐字 SVG group/path、導出版本、來源及審核 | 不能把集字成果冒稱原件 |

**已存在的工程入口：**

- 集字核心：assets/js/calligraphy/jizi-core.js。
- 館藏／IIIF 輸入：assets/js/calligraphy/open-image-ingest.js、iiif-region.js、iiif-crop.js、crop-resolver.js。
- 字源與像素核驗：assets/js/calligraphy/source-integrity.js、pixel-proof-gate.js、pixel-proof-promoter.js。
- Corpus 標準：data/calligraphy/schema.json、data/calligraphy/sources/。
- **已可用的向量化路徑：scripts/calligraphy_vectorize.py（ImageMagick→Potrace）**。新增 VTracer 是比較實驗，不能替換未經測試的生產流程。
- 拾字工作台：static/calligraphy/workbench-core.js；保持既有「拾字→寫心→成卷」流程不動。

重要：現有 schema 的 source 有 rights 三態（public-domain / licensed / unknown）；glyph 有 sourceId、asset、crop、derivativeOf 等欄位，故新流程應**向後相容地補充**模型／修正 metadata，而不是再造孤立 JSON 格式。

## 三、開源工具：角色與授權邊界

| 工程 | 用途 | 2026-10-28 的審核結論 |
| --- | --- | --- |
| [visioncortex/vtracer](https://github.com/visioncortex/vtracer) | PNG/JPG→SVG 的 raster tracing；灰階與不平整掃描測試 | Rust/CLI/Python 開源核心為 MIT OR Apache-2.0；桌面增值功能另行核對，**不假定免費** |
| **既有** Potrace + ImageMagick | 黑白原字輪廓向量化 | 先保留；需要區分工具的 GNU GPL/其他授權與部署方式，評估整合義務 |
| [LL0mc/calligraphy_chopping_tool](https://github.com/LL0mc/calligraphy_chopping_tool) | 字帖 PDF 切字、OCR、人工校對、單字庫、集字 GUI 參考 | 小型研究工程，未核實清楚授權時**只借鑑流程，不複製程式碼** |
| [kaonashi-tyc/zi2zi-JiT](https://github.com/kaonashi-tyc/zi2zi-JiT) | 少量風格參考／缺字補全的第一 AI 候選 | 程式 MIT；生成字型成果有 Font Artifact License Addendum；超過 200 個字的字型產品有標示要求；原始訓練／參考影像仍另核 |
| [yeungchenwa/FontDiffuser](https://github.com/yeungchenwa/fontdiffuser) | 少樣本字形風格轉換對照 | README 標示 **non-commercial research only**，不得直接當品牌商用依據 |
| [lsflyt-pku/DeepCalliFont](https://github.com/lsflyt-pku/DeepCalliFont) | 結合字形與書寫序列的書法研究 | 研究型工程，未確認完整權利條款與可部署環境前不納入產品 |
| [wangwenho/HanziGen](https://github.com/wangwenho/HanziGen) | 較大規模缺字補全／字庫研究 | 程式 Apache-2.0，參考字型／資料仍有不同授權 |

**比較順序：**歷代原裁字 > 可驗證真跡的單色向量化 > 合法且經人工核對的 AI 補字。VTracer 能「描」原字，不等於能「寫」出書法。

**資料權利至少分五層**核實：書法作品本身、原作攝影與館藏數位圖、來源網站／字庫資料、模型程式與權重、最終輸出資產。程式碼 MIT 並不授權下載任何網站的圖。

## 四、建議的實驗順序

### A. 先做拾字既有字符測試

1. 現有 corpus 逐字查「拾」「字」，展示候選數量、來源可信度、真實原帖可打開與否。
2. 匯出原頁縮圖及所選單字裁圖，經 pixel-proof gate。
3. 對同一對字輸出 Potrace、VTracer 對照，使用相同掃描圖、裁框、輸出視圖。
4. Pairing Board 至少兩組不同構圖候選；校正參數獨立記錄。
5. 人工審核後決定是否升格為 GLEAN wordmark Master。不能自動蓋過現有正式標誌。

### B. 把同一管線複用到「西望」

**優先設計約束修正（2026-10-28）：**《西望》是刊名題額，按照**宮殿匾額、殿柱楹聯、碑額、北朝摩崖與榜書擘窠大字**研究；小字帖來源只作歷史檢索，不得先裁小字硬放大。07 = 偏平面設計的厚重結體，09 = 有雄渾骨力的大字書寫筆觸，兩者目前皆不夠渾厚。判準及實物來源詳見[碑／帖／宮殿匾聯研究](./XIWANG-STELE-PLAQUE-BANGSHU-ARCHITECTURAL-LETTERING-20261028.md)。董其昌仍排除。



歷代蘇軾、王鐸、米芾、趙孟頫、文徵明等小字原帖只保留為非優先史料；首輪應研究殿額／柱聯／碑額／摩崖題署中**實際按大字觀看尺度書寫**的真實作品；**董其昌因不符《西望》力量雄渾的藝術取向而明確淘汰，不得重新加入候選。**分別尋找原帖「西」與「望」，先求同源，再衡量同書家跨帖。尚未核驗的網路書法字典只能幫忙**定位原帖**，不是可直接發佈的真跡檔。

參考檢索入口：
- 西：https://cha.jiguzuo.com/cha/7o5fqe-21412/
- 望：https://cha.jiguzuo.com/cha/stbobp-20331/
- 王羲之《西問帖》線索：https://m.zitiewang.com/shufa/chun32631.htm

同時把「西望」放入 P2 的**10 號 Contents**檢查：不動右頁保護資產、多雷原作、晨星；書法字應與多雷雕版細線／金色動態刻線協調，避免巨字與 Contents、文章標題疊字。這只是字標對照場景，**不自動替換站點現有正式 SVG**。

## 五、Source / Pairing / Master 必備證據

- **字源**：character、originalCalligrapher（含歸屬爭議）、sourceId、作品題名／版本、年代、書體、holding、sourceUrl、圖像權利。
- **像素證據**：原始圖片 ID、SHA-256、尺寸、原始裁切 x/y/w/h、頁碼、humanVisualVerified。
- **配字證據**：原圖候選 IDs、兩字次序／方向、字體尺寸、重心、間距、傾角、特殊筆勢、各版本差異。
- **向量證據**：原圖、原裁字、Potrace/VTracer 工具版本和參數、SVG group/path、原筆畫損失比較。
- **AI 補字證據（若有）**：origin=ai-generated、模型／權重／提示／參考字、輸入授權、人工逐筆驗證、是否可商用。
- **晉升記錄**：權利、來源、字形、排版（桌面／手機）、小尺寸辨識及人工核准結果。

字形狀態按順序記錄：discovered → source-verified → pixel-verified → paired → vector-reviewed → eligible-for-master → approved。生成字額外標明 generated-candidate，**不允許繞過驗收門檻**。

## 六、首次驗收清單

- [ ] 兩字都能點開原作或真實報告缺字，未冒充已有；
- [ ] 原頁、裁圖、sha256、座標、rights 可回溯；
- [ ] 至少兩組具有設計差異的字源配對（若來源不足則如實記錄限制）；
- [ ] Potrace 和 VTracer 用相同圖片做向量對照；
- [ ] 所有筆畫、閉合空間、飛白、字法人工審核；
- [ ] 修正前後可比較且可逆；
- [ ] SVG 逐字可編輯，不因換尺寸而失真；
- [ ] 生成字與真跡在資料和 UI 上明確區分；
- [ ] 真實桌面／手機頁避碰，內容清楚可讀；
- [ ] 法律權利和人工設計判斷均完成，才提升 Master。

**本備忘僅保存方法與候選技術。當前沒有證據表明新 VTracer、zi2zi-JiT、DeepCalliFont 已經安裝、接入或成功生成「西望」字形。**

**07／09 已進入館藏級來源研究：**[《西望》蘇軾／趙孟頫／文徵明／張照六件在研原作（另記董其昌淘汰）及米芾單字線索字源板（2026-10-28）](./XIWANG-07-09-ORIGINAL-SOURCE-BOARD-20261028.md)。其中六件在研作品的作者、館藏／官方展示及「西望」釋文已建立來源記錄，但尚未下載原像素或裁字；不得把館藏核實誤稱為已完成原字圖稿。

## 七、《西望》初步字形基準：07／09（2026-10-28）

**決策：**使用使用者選定的既有字形探索圖中「07」「09」作為**審美／造型基準，不是來源字帖，也不是待直接臨摹的歷史真跡**。此前使用 AI 在兩個基準上反覆重畫的十二版均淘汰，不收入單字庫。

### 兩條研究路徑

| 基準 | 研究重點 | 避免的退步 |
| --- | --- | --- |
| **07 / 沉雄、厚重的結體** | 「西」上部起筆的力度、主體負空間和穩定重心；「望」下部承重、末橫厚度及有控制的伸展 | 空泛的碑刻紋理、過度方正僵化、僅改墨量而不改真正結體 |
| **09 / 同樣雄渾、以強勁欹側和運筆張力見長** | 研究「西」果斷起筆、厚實墨量、方向與速度；「望」上下相貫、力透收筆、體勢能壓住整個刊頭 | **靈動纖細、飄逸清秀、輕巧賣弄**；筆畫亂飛或結構失字法；只縮放粗細充作十二版 |

**共同美學硬門檻：兩條路線都必須力量雄渾、骨力充足、字身有重量與壓迫感。07／09 不是厚重與纖細之分，而是沉雄穩健與沉雄奔放之分。** 原字即使是真跡，若呈清秀疏朗、飄逸輕巧或技巧炫耀，直接淘汰；不得靠背景、加粗濾鏡、飛白或金色裝飾替代字形骨力。

**共同約束：**每個字必須準確可辨；研究預覽僅用黑字／白底、逐字來源說明，優先保留縱向「西／望」兩字組合；與右頁封面、金色刻線和 P2 Contents 的關係留到**字形本身驗收後**再研究，不用背景遮掩字形問題。

### 目前查到的檢索入口；注意「書家歸名」不等於「作品級原帖核驗」

- [「西」行書彙目，集古作網](https://cha.jiguzuo.com/cha/7o5fqe-21412/)：含趙孟頫、米芾、王鐸等字源索引；董其昌已排除，不得列為品牌候選。
- [「望」行書彙目，集古作網](https://cha.jiguzuo.com/cha/stbobp-20331/)：含趙孟頫、米芾、王鐸等字源索引；董其昌已排除，不得列為品牌候選。
- [「西」79 圖，澳典](https://zidian.odict.net/zh-tw/860436843/ftxingshu/)：提供更多書家來源線索。
- [「望」字行書書家彙目，漢文360](https://hanwen360.com/s-xs/671B.html)：可交叉核對書家名稱。

**此階段已可確認：**上述公開目錄中確實有兩個字的候選索引，可按書家先配對研究；**此階段尚未確認：**每個單字的原作品、完整原頁、館藏 ID、crop 像素證據、複製利用授權以及「07／09」相似度。這些缺一不可；不能把目前搜到的字典圖片直接宣稱「已完成真跡集字」。

### 下一個實際交付的驗收門檻

1. 為 07、09 各從蘇軾、王鐸、米芾、趙孟頫等未淘汰書家的字帖線索中找能追溯到具體**作品與原頁**的「西」「望」字；找不到必須標缺字。
2. 製作不含任何背景裝飾的「原字來源 → 原字裁圖 → 縱排配字」比較；**只比較字形本身**。
3. 每一組標註來源：作者／歸屬狀態／帖名／影像頁與座標／版權狀態；保存 Source Board 和 Pairing Board。
4. 07／09 的評判是兩條**參照軸**，不是強制只許沿兩種原 AI 字形複刻；無明顯字形品質提升的候選淘汰。
5. 候選選出後才進入 SVG 和 P2 真實版式測試。**不自動覆蓋現有「西望」官方 SVG**。
