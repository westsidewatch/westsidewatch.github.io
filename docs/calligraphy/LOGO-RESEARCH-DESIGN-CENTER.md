# 池底設｜NODesign Chinese Logo Lab

## 歸屬

本研究設計中心歸入 **池底設**。

池底設的設計理念是 **NODesign**：

> 不完成，因為還會一直生長。

NODesign 不是不設計，也不是殘缺、半成品或刻意去風格化。每一個當下的作品都必須充分成立；但系統不以封閉的「完成」為目標，而保留繼續生長、追加、變體與重新組合的能力。

「拾字」書法 Logo 研究是池底設的第一個可執行設計研究。它先服務「拾字」，再驗證「西望」，最終可能生長為：
- 一套專門處理中文 Logo／中文字標的工具；
- 一套符合池底設 NODesign 美學的中文字標方法；
- 可持續擴充的碑帖字形、配對、校正與來源系統。

## 核心命題

**碑骨 × 帖氣 × Optical Correction → Brand Wordmark**

不尋找一個「最像 Logo 的書法字體」，而從歷史字形中保留來源，研究哪些骨架能壓住、哪些筆勢能讓它活起來，再進行最低限度、可追溯的品牌視覺校正。

## NODesign 對 Logo 工具的要求

工具本身必須可生長，而不是為「拾字」或「西望」寫死：

1. 任意中文詞都可成為新的研究節點。
2. 新碑帖、新書家、新字庫可以持續加入。
3. 原始字永遠保留，設計修改不覆蓋來源。
4. 每次配對與 optical correction 都可回溯。
5. 當下選出的 Master 可以正式使用，但不是宣告方法終結。
6. 工具不替設計師自動宣布「最佳 Logo」；它負責把真正值得判斷的候選浮現出來。

## 四層資產

### Source Board
原始候選字。保留書家、作品、年代、碑／帖、書體、檔案定位與權利狀態。

### Pairing Board
把指定文字的候選組合成可比較字標。分為：
- 碑 × 碑
- 帖 × 帖
- 碑骨 × 帖氣

### Optical Board
只研究品牌使用所需的比例、字距、基線、重心、墨量、負空間與縮小辨識。

### Master
當下被鎖定使用的品牌標準字。保存來源與所有修正參數，可重新生成。

## 研究維度

### 碑骨
現有起點：魏碑、趙之謙。

觀察字面、外輪廓、中宮、主幹、墨量、重心、黑白反轉與遠距辨識。

### 帖氣
現有起點：王羲之、米芾及現有行書／行草 corpus。

觀察起收、提按、傾側、速度、行氣，以及字與字之間不依賴裝飾性牽絲的承接。

### 碑帖融合
不是把碑字與帖字做平均，也不是製造「仿古字體」。先找到能成立的骨，再研究可以引入多少帖的動勢。

允許：比例、字距、基線、重心、墨量及局部尺度校正。

不允許：任意重畫古人筆跡；丟失 provenance；用毛筆、印章、墨圈等符號代替字標本身。

## 第一個節點：拾字

不預設王羲之或任何書家優先。

第一輪 Source Board 先抽取現有 corpus 中所有可用的「拾」「字」，按碑／帖與來源排列；之後才生成 Pairing Board。

## 第二個節點：西望

「拾字」完成方法驗證後，用同一工具處理「西」「望」。

額外測試：
- 遠距招牌感
- 與 Westside Watch 英文並置
- 主站頁眉小尺寸
- 單色刻線／初光金環境
- 離開教會與出版內容後的獨立辨識

## 外部研究庫

HCSU：碑／帖分類、筆法、結構 metadata 研究參照。

ARMCD：具體碑刻／墨跡來源與碑線候選研究。

外部資料首先只取得研究身份。進入正式 Master 前重新確認原始來源、授權與可使用範圍。

## 下一階段

建立可視化 **Source Board**，把「拾／字」的現有候選真正攤開。這是 NODesign Chinese Logo Lab 的第一個工具介面，而不是一次性的 Logo 草稿。


## 文徵明專項探索

文徵明不只作為「一位書家」加入，而作為 NODesign Chinese Logo Lab 的一條獨立研究線。

### 已確認的成熟來源

1. **National Palace Museum｜文徵明四體千文**
   - 同一核心文本存在篆、隸、楷、草等多體材料。
   - 適合做「同一書家／同一文字／不同書體」的結構與動勢比較。
   - 優先研究官方開放資料與可下載影像，不以二次整理圖包作 source of truth。

2. **National Palace Museum｜文徵明草書千字文**
   - 用於帖氣、速度、連帶、傾側研究。
   - 與四體千文形成同書家跨書體對照。

3. **National Palace Museum Open Data｜文徵明行書**
   - 已確認存在可下載的 CC0 presentation image，並有較高解析度 CC BY 4.0 資產。
   - 可作 provenance 清楚的候選來源。

4. **Paris Musées / Musée Cernuschi**
   - 已確認文徵明相關書法影像提供 CC0，並暴露 IIIF Manifest。
   - IIIF 適合作為後續自動切字／Source Board ingestion 的成熟接口。
   - 館藏條目標示為後世拓本時，必須保留「拓本／原作」層級，不與原墨跡混標。

### 現有開源字庫

neil-zt/calligraphy-community / zhuojg/chinese-calligraphy-dataset 繼續作快速單字檢索層。其優點是已切字、已有索引；缺點是 provenance 粒度不足，不能取代博物館原始館藏記錄。

### 研發策略

文徵明線採兩層結構：

- **Fast corpus**：成熟切字庫，用於快速查「這個字有沒有」。
- **Authority corpus**：故宮、Paris Musées 等館藏，用於確認作品、書體、年代、影像權利與原始上下文。

研究中心最終不只存單字圖片，而要存：

character → glyph → calligrapher → work → script → source image → crop coordinates → rights → source URL/IIIF → design corrections

這將成為未來中文字 Logo 工具的 provenance backbone。


## 文徵明研究計畫 v1

### 研究問題
不把文徵明簡化成一條按年齡前進的「風格時間線」。研究單位改為：

**作品 → 段落／書寫狀態 → 行 → 字 → 字間關係**

核心問題：
1. 同一作品內是否存在可重複辨識的多種行書狀態？
2. 單字骨架、筆勢與整行行氣之間如何互相制約？
3. 文徵明如何由精整的小字／行書，發展到能承擔大尺度的晚年行書？
4. 哪些特徵可以轉譯為中文字標，而不需要仿造一套「文徵明字體」？

### Anchor Work 01｜題仿米雲山圖（1535）
第一階段不預設「兩種風格」的名稱，也不先把它們解釋成早／晚風格。先建立可驗證的 A/B segmentation。

保存五層資料：
- 原卷／權威圖版
- 段落
- 完整行
- 單字 crop
- 相鄰字與行位置 context

每個字除 glyph 外，記錄：
- bounding box / crop coordinates
- 字高、字寬、墨面比例
- 重心
- 傾側
- 行軸偏移
- 與前後字距
- 前後字尺度變化
- 可見連帶／呼應
- Style A / B / transition / uncertain

研究輸出：
- A/B 全卷分布圖
- 兩種狀態的代表字板
- 同字異寫對照
- 行氣樣本
- transition zones
- 可用於 Logo 的「骨」與「勢」特徵，不直接生成 Logo

### 對照作品
不只按年代選，而按研究功能選：
- 早期／早年端整材料：觀察原始骨架
- 中年行楷／行書：觀察控制性
- 1535 前後作品：驗證《題仿米雲山圖》是否為孤例
- 約六十九歲草書：觀察節奏與行氣上限
- 晚年大字行書：觀察尺度放大後的骨架、墨量與招牌性
- 晚年小楷：作反向控制組，避免把「晚年」錯等同於「粗壯／大字」

### 三個 Corpus Layer
1. **Authority Layer**：博物館原件、IIIF、權威著錄。
2. **Context Layer**：整卷、段落、整行；專門保存行氣。
3. **Glyph Layer**：切字與同字聚類；服務「拾字」與 Logo Lab。

任何 Glyph 都必須能返回 Context，再返回 Authority。

### 第一階段完成標準
不是「收了多少字」，而是：
- Anchor Work 01 可逐行瀏覽；
- A/B/transition 標記可以被人工覆核；
- 任一單字可一鍵回到原行；
- 至少找到一組同字在 A/B 狀態下的異寫；
- 能與至少三件不同功能的對照作品並排比較。

這一階段只是驗證研究方法；文徵明線從現在起直接按完整 corpus 建設，不再以 Anchor Work 01 的結果決定是否擴建。


## Corpus Architecture v2｜書家庫與 Logo 研究解耦

### 原則
Chinese Logo Lab 不以任何單一書家作為 Logo 方法的中心。文徵明是第一個建立完整作品級研究庫的書家，但不是 Logo 的預設答案。

系統分成兩層：

**A. Calligrapher Corpus**
每位書家獨立、完整、可持續生長。研究其作品、年代、書體、尺度、書寫狀態、行氣、單字、來源與權利。

**B. Logo Research Index**
跨書家、跨碑帖、跨時代調用 Corpus。針對一個品牌詞，按設計需求比較候選，而不是按書家名氣選字。

### 文徵明完整研究庫

文徵明 corpus 的目標不是只收「適合 Logo」的作品，而是盡量建立完整的可研究作品譜系：

- 小楷
- 楷書／行楷
- 行書
- 行草
- 草書
- 大字
- 題跋／手卷／冊頁／立軸等不同載體
- 早、中、晚不同時期
- 同一作品內的書寫狀態變化
- 臨古／自運／題畫等不同書寫情境

每件作品至少保存：
authority record、作品名、年代／年齡、書體、載體、尺寸、原作／拓本／摹本狀態、館藏、rights、source/IIIF、完整圖像、段落、行、glyph、context、研究註記。

《題仿米雲山圖》保留為 Anchor Work 01，作用是驗證「作品內多狀態＋行氣」資料模型，不代表整個文徵明庫的範圍。

### Logo Lab 的跨書家研究池

現階段至少保留以下研究方向，不預設排名：

- 魏碑系：骨架、方整、碑刻尺度、招牌性
- 趙之謙：碑學轉化、篆隸意、個人化大字
- 王羲之：帖學骨幹、自然行氣
- 米芾：動勢、欹側、速度與空間
- 文徵明：從精整小字到晚年大字的完整尺度光譜

後續新增書家／碑刻時，只進 Corpus；Logo Lab 通過 index 取用，不把產品邏輯寫死在任何名單。

### Logo 查詢模型

品牌詞 → 設計條件 → 全 Corpus 搜索 → 候選聚類 → Source Board → Pairing Board → Optical Board → Master

設計條件可包括：
- 碑骨強度
- 帖氣／動勢
- 墨量
- 中宮
- 尺度適應
- 遠距辨識
- 同源／跨源
- 時代
- 書體
- provenance / rights

這使「西望」未來可以同時看魏碑、趙之謙、文徵明、王羲之、米芾及後續 corpus，而不是先選一個書家再找「西」「望」。


## 拾字插入工程｜SEAL LAB

### 定位
在「拾字」既定流程中，把後續的印章生成提前成一個可研究節點：

**拾字 GLEAN → 寫心 INSCRIBE → 印章 SEAL LAB → 成卷**

SEAL LAB 同時服務兩個目的：
1. 拾字產品：生成可實際使用的印章；
2. 池底設 Logo Lab：把篆刻視為高度濃縮的中文字標實驗場。

印章不是 Logo 的附屬裝飾，也不等同 Logo；研究的是兩者共有的造形問題。

### 研究維度
**字法**：篆書、古文字與印化字形；同字變體；增減、屈曲、伸縮、挪讓；為方寸空間而發生的字形變化。

**章法**：一字、二字、三字、四字及多字印；縱／橫／回文等次序；字的面積分配；主次、疏密、呼應；邊欄與字的關係。

**空間**：正負形；留紅／留白；中宮與外輪廓；邊角壓力；視覺重心；不對稱平衡。

**刀法／邊界**：朱文／白文；線條粗細；粘連、斷裂、殘邊；石味與印面邊界；小尺寸辨識。

### 資料模型
印章研究不只保存成品圖。每枚印建立可逆資料：

**seal → inscription → reading order → grid/regions → glyph variants → transformations → positive/negative space → border → source/provenance**

由此研究：字為什麼因整體而變形、字間為何不是平均分配、哪些空間關係能遷移到二字／三字 Logo，以及哪些只是篆刻媒介特徵。

### Logo Lab 的橋接
從 SEAL LAB 抽取的不是「印章風 Logo」，而是可跨媒介的規則：
- 字形允許為整體而變；
- 字與字可以共享／競爭空間；
- 負空間也是造形；
- 外輪廓可以先於單字局部；
- 視覺面積不等於幾何面積；
- 小尺度必須重新做 optical correction。

這些規則進入 Pairing Board 與 Optical Board，但保留來源標記 seal-derived，避免把篆刻語法與碑帖語法混為一談。

### 工程順序
1. 建立印章 authority/source corpus；
2. 做章法標註，不急著生成；
3. 建立可調 grid / region / reading-order 模型；
4. 接入拾字現有 glyph resolver；
5. 生成候選印面；
6. 人工選擇後做 optical correction；
7. 輸出印章，同時把可泛化的佈局規則送入 Logo Lab。


## SEAL LAB｜多雷探索：可搬成熟方案（第一輪）

目標遵循拾字的成功路徑：先取得成熟、授權清楚、可拆用的資源，不從零造引擎。

### 第一核心：vYinn（殷人）
定位為首要工程參考／移植來源。MIT。其現成能力與拾字印章需求高度重合：
- 陰文／陽文；
- 方、圓、橢圓印框；
- 每字獨立大小、座標、橫縱變形、旋轉；
- 字與印框分層；
- 做殘、油墨、擴散；
- 透明 PNG；
- 配置驅動；
- 從既有印文圖像扣取透明印文。

策略：不搬 Perl UI；抽取它已驗證的「印面參數模型、圖層模型、變形模型、效果模型」，重寫為拾字現有 Web runtime。

### 第二核心：篆字字形層
**LXGW Seal / 霞鶩篆書**：OFL 1.1，小篆 Unicode 18.0 對應與今字映射清楚；現階段字數有限，適合作為來源可靠的基礎／fallback，不作唯一字庫。

**JFZSKSealScript / 中山王篆**：OFL 1.1，兩千字級覆蓋，可作第二種篆書造形來源。其擴展字形包含設計性補字，因此必須和《說文》來源型字形分級標註，不混為同一 authority。

### 第三核心：Authority / provenance
博物館開放資料只做來源與研究層。優先接有 CC0 / CC BY 高解析圖與 IIIF 的館藏，保存原印面與書畫上的作者／收藏印記，用於章法研究和後續 provenance，不直接把未知權利的網路印譜切字塞進產品。

### 暫不採用
- 現代公司公章 generator：幾何渲染可參考，但與文人篆刻章法目標不同；
- OCR seal datasets：可留給未來自動切印／識別，不作第一版生成核心；
- 權利不清楚的「古印字體包」：不進 runtime。

### 最小可行版本
第一版只做：
**輸入 1–4 字 → 篆字解析 → 方印 → 朱文／白文 → 2–4 個成熟章法 preset → 每字 optical adjustment → 印框 → PNG/SVG**

第一版不做 AI 自動審美、不做大量仿舊、不做公司公章模板。

資料結構從第一天保留：
**text → glyph source → layout preset → per-glyph transform → positive/negative mode → border → optical corrections → export**

這使拾字印章生成器本身可立即使用，同一批 layout/transform 資料又可被池底設 Logo Lab 研究。


## SEAL GLYPH STACK v2｜先擴米，再接章法

### 重大更新：Unicode 18 小篆層
2026 年 Unicode 18 已正式加入 Small Seal Script block。工程不再把「現代漢字直接套一款篆體字型」當唯一方案，而建立：
**modern Han → Small Seal mapping → Unicode Small Seal code point → seal glyph source**

### Tier 0｜全覆蓋基礎層
- **PlanschriftSeal**：Unicode 18 Small Seal 11,328 字符全覆蓋；MIT/OFL 雙許可。作為拾字 SEAL 的高覆蓋基底。
- **Kaiyuan Small Seal**：現有對齊資料顯示 11,328 小篆字符中僅約 348 glyph 尚缺；OFL。作為第二高覆蓋 renderer / cross-check source。

Tier 0 的目的：解決「輸入一句話卻大量缺字」。它保證可生成，不等同於最終藝術選字。

### Tier 1｜權威字源層
- **小學堂小篆**：9,831 字頭、11,101 字形。保存《說文》部目、異體與來源描述。作 authority/reference；權利逐項確認後再決定哪些圖像可進 runtime。
- **Unicode SealSources /《說文》四大來源**：THX、CCZ、QJZ、DYC。作 modern↔seal 映射與字源核對。
- **全字庫《說文解字》**：已有開源項目記錄 6,721 字、OGDL-TW-1.0/CC-BY-4.0-compatible；需在實際納入前重新核驗原始授權與下載源。

### Tier 2｜藝術變體層
- **LXGW Seal**：OFL；字必有《說文》依據，數量少但 provenance 強。
- **JFZSKSealScript / 中山王篆**：OFL；約 2,700 vocabulary entries，提供戰國金文／中山王系造形。
- **思文小篆**：OFL 1.1；候選完整文本字體，需下一輪做 glyph coverage audit。
- 後續加入可驗證授權的秦篆、漢篆、古璽、清人篆書／篆刻字形，不混成單一「篆體」。

### Tier 3｜研究資料層
- **EVOBC**：甲骨、金文、春秋、戰國、Seal Script、隸書的跨時代字形資料；CC BY-NC-SA 4.0，只進研究，不進商用 runtime。
- **小學堂衍生工具／crawler**：證明可把字頭、異體、來源描述結構化；只借資料模型與檢索思路，抓取及再利用須遵守原資料權利。

### Resolver 原則
SEAL 不應只有 font fallback，而是候選 resolver：
1. 解析今字；
2. 找 Unicode Small Seal 對應；
3. Tier 0 保證 glyph；
4. Tier 1 驗證字源；
5. Tier 2 提供藝術候選；
6. 送入 vYinn-derived layout/transform engine；
7. 保留每個 glyph 的 source / authority / license。

因此同一個「西」將來不是一個篆字，而是一組有來源的候選，章法引擎再決定哪一個最適合當前印面。


## SEAL RESOURCE MAP v3｜擴大探索，不急於實作

本輪把資源從「篆書字體」擴成五個彼此獨立的池，避免把小篆、古璽、印人篆刻混成一種字體。

### A. 可直接使用的高覆蓋 glyph
- PlanschriftSeal：Unicode 18 Small Seal 11,328 code points 全覆蓋；MIT/OFL。
- 全字庫《說文解字》字形：約 6,721 字；作第二套《說文》型字形來源，授權在納入 runtime 前以原始來源再核驗。
- 思文小篆：OFL 1.1；完整文本取向，待做 coverage audit。
- 峄山碑篆體：已有 MIT Web 工具 XiaoZhuan 以 2,503 常用字方式整合；字體本身的原始授權仍須獨立核驗。
- LXGW Seal：OFL，少量但字源規則嚴格。
- JFZSKSealScript：OFL，2,700 vocabulary entries，戰國中山王系。

### B. 字源／異體 authority
- Unicode Small Seal + THX / CCZ / QJZ / DYC 四大《說文》來源。
- 小學堂：楷篆對應、異體、部件、《說文》釋義；作 reference/authority，不把網站資料權利自動視為可再發布。
- CC0《說文解字》結構化文本可作釋義、字頭與 resolver 輔助，不等於 glyph 圖像授權。

### C. 真實印面／章法母庫
- 復旦「印藏」：一期 501 種印譜、約 15 萬圖、約 200 位印人；IIIF。優先研究印面、章法、印文與印人關聯；逐項確認影像再利用條件。
- 上海博物館中國歷代璽印篆刻館：約 15,000 件館藏，古璽印、封泥、明清篆刻脈絡完整；適合作時代／類型 authority 和研究索引。
- 故宮璽印專題：作宮廷璽印、古璽、漢印及研究書目的 authority index。
- 西泠印社／中國印學博物館：作近現代篆刻、印學史、印人與印譜研究索引。

### D. 開放博物館圖像
建立 CC0 / Public Domain 印章清單，優先從 Met Open Access、Smithsonian metadata、Wikimedia Commons 等逐件確認。只把明確開放的圖像進可再利用 corpus。

### E. 成熟工具／工程模型
- vYinn：MIT；核心章法、逐字 transform、朱白文、邊框、做殘／擴散、PNG。
- ChinaSeal：現成開源篆刻印稿、排版、鏡像與精密打印工具；作第二工程對照，特別研究 Web 版未必需要但實際治印需要的鏡像／打印尺度。
- XiaoZhuan：MIT；2,503 字現成今字↔小篆 Web dictionary，可借 resolver/data UX，不直接假定其 bundled font 授權可轉移。

### 暫定結論
目前不應鎖定單一「字庫」。拾字 SEAL 應形成：
**高覆蓋小篆底庫 + 權威異體層 + 戰國／秦篆等藝術變體 + 真實歷代印面 corpus + vYinn/ChinaSeal 章法工程。**

下一輪探索重點不再是一般關鍵詞「seal font」，而是：
1. 復旦印藏 IIIF manifest 是否可批量取得及 metadata 粒度；
2. 上海博物館 15,000 件中線上可機讀／可下載比例；
3. Unicode 18 Small Seal 的官方 mapping/source files；
4. PlanschriftSeal、全字庫說文、思文小篆的實際 glyph coverage/授權 audit；
5. 古璽、秦漢印、明清流派印的可開放圖像來源。
