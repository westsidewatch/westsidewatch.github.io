# 多雷探索 001｜書法庫、經文書法與經文春聯

## 已固定的產品邊界

- 全站共享書法庫；白晝咖啡館只作公開館藏展示。
- 集字工具維持 internal-development，成熟後才經 public-release gate 上線。
- 白晝咖啡館館藏可擴展歷代作者、書體、原作、摹本、臨本、拓本。
- 全庫 admission 排除：《金剛經》《道德經》以及與佛教寺廟相關作品。
- 集字 Core View 第一階段只以王羲之、文徵明、米芾、趙孟頫的行書／行草為核心。
- Test Case 001 永久固定：「敬畏耶和華是智慧的開端」。
- 兩條產品線：A 經文書法；B 經文春聯。

## 探索得到的工程判斷

### 1. 不應把單字生成模型當主架構
MCCD、CalliECD、CalliFormer 等證明 character-level 的作者／書體／結構標註很有價值，但它們主要解決單字辨識、結構保真和缺字生成。本站真正難題是行書的上下文關係，因此 character-level 只作底層能力。

### 2. 核心資料單位升級為 column / phrase context
UniCalli 的列級方法直接針對孤立字符方法遺失 ligature、spacing、scale、layout 的問題。本站應吸收這一點，但不直接綁定其大型 FLUX 模型。

Canonical observation hierarchy:
work -> column/line -> phrase window -> character -> stroke/structure derivative

每個 character 除 glyph 外，保存：
- bbox / baseline or vertical-axis offset
- relative scale
- ink density proxy
- slant / center of gravity
- predecessor / successor
- inter-character gap
- connected-stroke / ligature evidence
- phrase-window id
- line/column id

### 3. 補字採 retrieval-first，generation-last
優先級：
1. 同一作品真字
2. 同一書家同書體其他作品真字
3. 同一書家可相容行書／行草真字
4. 結構相近字的部件／筆勢作 reconstruction evidence
5. 最後才使用生成式補字

生成字永遠標 reconstructed，不得冒充 historical glyph。

### 4. 補字不是單字問題，而是 contextual ranking
候選排序至少由兩組分數組成：
- glyph fidelity：作者、書體、結構、筆勢、墨色相容
- flow compatibility：前後字出入筆方向、大小、重心、欹側、疏密、牽絲、行軸、節奏

同一個字在不同上下文可以選不同 glyph。

### 5. 四家不可平均化
四家共享的是行書 grammar feature space，不共享身份。王羲之模式只能以王羲之 provenance 的真字／其明確 reconstruction 生成成品；其他三家只可提供一般關係先驗，不可把其字形混入並標成王羲之。

### 6. 兩條生產線共享一個 Flow Engine
Scripture Calligraphy：重點為單列／多列行氣、章法、落款空間。
Scripture Couplet：在 Flow Engine 上增加 pair constraints：上下聯字數、對應位置視覺重量、起收勢呼應、左右列密度、橫批；scripture quotation 與 scripture-inspired 永久分離。

### 7. Benchmark 應是逐步增長的經文 corpus
TC001 = 敬畏耶和華是智慧的開端。
每新增經文，不只增加字覆蓋，也新增 phrase transitions 和 layout cases。每次修改 retrieval / reconstruction / flow / layout engine 都重跑 TC001。

## 外部方案吸收策略

- MCCD：吸收 multi-attribute schema（character/style/dynasty/calligrapher）思想；其資料授權限制為非商業研究，不直接成為本站 canonical production corpus。
- UniCalli：重點吸收 column-level annotation、box map、recognition + generation 相互約束的架構思想；不把 23GB FLUX 模型設成產品依賴。
- CalliECD：吸收 skeleton/recognition correction，作 reconstructed glyph 的 correctness gate。
- CalliFormer / CCTS：吸收部件結構關係標註，用於缺字 reconstruction 的結構約束。
- Chinese Calligraphy Dataset 等網路聚合資料：只可作 discovery/reference；未核 rights/provenance 前不進 canonical corpus。

## 下一階段工程

1. shared calligraphy corpus schema 從 work/character 擴到 work/column/phrase/character。
2. 對四家第一批行書／行草作品建立 column-level annotation queue。
3. 建 phrase-window extractor，先保存真實相鄰 2/3/5 字組。
4. 建 Flow Feature extractor，不做生成。
5. TC001 先跑 retrieval-only baseline，明確列出真字、缺字與每個相鄰 pair 的 evidence coverage。
6. retrieval baseline 穩定後才開始 reconstructed glyph；最後才引入生成模型。
