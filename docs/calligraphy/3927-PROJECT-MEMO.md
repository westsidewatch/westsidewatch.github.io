# 三九二七｜3927

**池底設 · NODesign 001**  
內部工程名：SEAL 66

## 立項

「三九二七」是池底設 NODesign 的第一件正式設計作品。

作品從聖經自身的結構出發：舊約 39 卷，新約 27 卷，共 66 卷。作品不另外附加一套外在品牌語言，而讓 39 / 27、經卷、文字、篆刻與生成系統本身形成識別。

NODesign 原則：

> 不是少設計，而是不增加作品原本不需要的東西。  
> 不完成，因為還會一直生長。

## 作品識別：兩枚總章

作品不另造 Logo。兩枚總章本身就是作品的核心識別。

### 陰文總章

三　9  
二　7

### 陽文總章

3　九  
2　七

兩枚章互為語言與陰陽的交換：中文數字與西方數字各取兩位；陰文與陽文成對。它們同時指向「三九二七」「3927」「39 + 27」以及舊約／新約的結構。

兩枚總章獨立於 66 卷 Style Genome，可作為「三九二七」自身的母風格／第 0 組識別。

## 66 枚經卷章

66 卷各形成一枚 canonical SVG Master。不是 66 次隨機生成，也不是套模板換字，而是 66 個彼此有性格、又屬於同一作品系統的設計。

每卷從經文本身建立設計鏈：

**經卷 → 神學／文學特徵 → 造形命題 → 字形來源 → 章法 → 印形 → 陰陽文 → companion 數字章**

例：《創世記》可探索石鼓文方向。這是當代設計詮釋，不冒充經卷原始書寫形式或歷史字體。

可使用的造形語彙包括：
- 陰文／陽文
- 大篆／小篆
- 金文／石鼓文及其他有可靠來源的古文字／篆書變體
- 方、長方、圓、橢圓、隨形
- 疏密、朱白比例、邊欄、線條重量、負空間與 optical correction

所有字形保存 provenance。

## 66 Style Genomes

每枚經卷 Master 同時抽取可生成的 Style Genome，而不只是保存一張 SVG。

至少包含：
- script / glyph source preferences
- layout families
- enclosure families
- positive / negative tendencies
- density range
- stroke-mass range
- asymmetry range
- border behavior
- glyph deformation limits
- spacing / negative-space rules
- companion-seal rules
- editorial / theological design notes

66 是第一批基礎風格，不是上限。

## 經卷章 × 章節數字章

經卷章與章節章不是兩個孤立物件，而是一個 composition。

拾字已知：

**book_id + chapter + verse**

因此引用經文時可直接組合：

**經文 + 經卷章 + 章節章**

章節章獨立生成，不需要為所有經節預製完整印章。

兩枚章的 companion rules 控制：
- 主副尺度
- 間距
- 對齊／錯位
- 陰陽搭配
- 外形互補
- 朱白比例
- 視覺重量
- 可接受旋轉與不規則度

## 數字章：隨機生成器第一個 benchmark

章／節數字是生成系統最合適的第一個試驗場：字符有限、組合很多、結果容易人工判斷。

生成不是無約束 random：

**Style Genome + Constraints + Seed → deterministic candidate SVG**

同一 seed 必須可重現。

每次保存：
- style_id
- seed
- glyph choices
- layout topology
- transforms
- positive / negative
- enclosure
- optical corrections

用它驗證隨機候選是否仍屬於所選風格、是否碰撞失衡、是否可讀，以及是否與經卷章形成和諧畫面。

## 人名章：生成器主要產品出口

數字章驗證生成能力後，最大的實際用途之一是人名章。

流程：

**輸入姓名 → 選 Style Genome → 選形狀 → 選陰／陽文 → resolver 取得候選字形 → seeded generator 生成候選 → optical checks → 使用者選擇／微調 → canonical SVG**

例如使用者可選「馬太福音」風格，再選形狀與陰陽文，輸入姓名。生成器繼承的是馬太福音的章法、密度、空間、字形偏好與邊界規則，而不是把姓名塞入固定模板。

後續 Style Genome 可由古璽、秦漢印、金文、石鼓、明清流派、具體篆刻研究與池底設新章法繼續生長。

## SVG 是 canonical master

印章的核心不是 PNG，而是可逆、可編輯的 SVG scene。

每個 glyph 保持獨立 vector path/group，保存：
- character
- source
- variant
- transform
- optical correction
- provenance

同一 SVG scene 同時服務：
- 印章成品
- 網頁互動
- PNG 輸出
- 生成器
- Logo Lab

PNG 只是輸出格式。

## 拾字整合

「三九二七」首先是一件獨立設計作品，同時直接成為拾字的正式產品內容。

拾字選中經文後：
1. resolver 得到 book_id / chapter / verse；
2. 調用該卷 canonical book seal / Style Genome；
3. 生成或調用章節數字章；
4. 依 companion rules 完成雙章 composition；
5. INSCRIBE / SEAL 可直接帶入；
6. 使用者可關閉、替換、重生成或微調。

## 作品展示

完成 66 枚後，「三九二七」本身作為獨立數字設計作品呈現，而不是功能展示頁。

遠觀：66 枚形成完整朱色視覺圖景。  
近觀：每枚可看到經卷、設計命題、字源、章法與 provenance。  
互動：從經卷 Master 生成章節章，再用同一 Style Genome 生成人名章。

最終形成：

**39 + 27 → 66 卷 → 66 枚 Master → 66 Style Genomes → 章節章 → 人名章 → 持續生長**

## 工程原則

- 內部工程名保留 SEAL 66；不作作品主標題。
- 正式作品名：**三九二七 / 3927**。
- 對外識別優先使用兩枚總章，不另加不必要 Logo。
- 66 卷同時是產品內容與 regression corpus。
- 研究 corpus 與 runtime 可分離；權利不明的材料只作研究。
- 不把所有篆書／古文字混稱為單一「篆體」。
- 不把當代視覺詮釋宣稱為經卷的歷史書寫形式。
- 生成器輸出候選，不以演算法宣告唯一「最佳」。
- 先建立可靠生成與 SVG 架構，再提升到完整作品展示。
- 不破壞拾字目前已解決的搜索、經文推薦、落款、繁簡 resolver、PNG／列印流程。

## 第一階段工程

1. 建立 66 卷 canonical book registry。
2. 建立 Style Genome schema。
3. 建立 SVG seal scene / layout / export core。
4. 以章節數字章完成 seeded generator 第一輪。
5. 建立 book seal + reference seal companion composition。
6. 先完成兩枚「三九二七」總章作為第 0 組真實案例。
7. 開始 66 卷 Master；《創世記》作為石鼓文方向的首批研究候選之一。
8. 將可用成果逐步接入拾字，而不是等待全部 66 枚完成後一次上線。
