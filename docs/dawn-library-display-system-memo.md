# 黎明書局館藏展示系統工程備忘

> Status: exploration / architecture memo
> Date: 2026-09-12
> Scope: Dawn Library / 三晨星 / 策展集 / 光譜 / 主站展示
>
> 本文件記錄產品與工程方向，不自行覆寫 `docs/MASTER_SITE_ARCHITECTURE.md` 的 canonical 主站結構。任何主站層級調整仍須由使用者明確確認後再進入結構修改與實作。

## 1. 背景：Step 7 之後的館藏條件

Dawn Phase I Step 7 已完成 canonical substrate 合流。Dawn 現在是 Work / Edition / Cover / Pointer 的唯一身份源；多寫書牆／聖經世界等只作 Surface，以 canonical Work ID 引用館藏，不再維護第二套圖書身份資料。

因此黎明書局已具備萬冊級 canonical Works 的共同館藏底座。下一階段展示問題不再是「把所有書卡一次擺出來」，而是：如何讓大量館藏可被感知、發現、理解、策展和使用。

核心原則：

> 館藏不是一萬張縮圖；館藏應成為可觀看、可遊走、可重新組織的知識世界。

## 2. 舊定義保持不變

三晨星、策展集、光譜仍維持既有品牌與編輯定義，不因新展示系統而重新命名或降格為普通分類。

### 三晨星 Morning Star

黎明書局最高級的三個大編輯欄目／編輯判斷。回答「什麼值得留下、首先被看見」。不是流量榜、熱門榜，也不是三個靜態分類。

### 策展集 Collection

圍繞選題，把館藏自動主題化、雜誌內容化，並形成可閱讀、可學習、可行走的內容道路。不是 tag 搜索結果，也不是相似 URL 文件夾。

### 光譜 Spectrum

長在館藏外面的「外表」與知識脈絡可見層。回答「這些知識彼此是什麼關係」。它不是普通 Topics、分類樹或單純知識圖譜，而是讓大型館藏按照經卷、人物、地點、時代、主題、神學概念、學習深度等不同坐標重新排列、顯影和遊走。

## 3. 新展示系統：同一座館的三種觀看尺度

新的探索不把三晨星、策展集、光譜做成三個彼此獨立的頻道，而讓它們成為同一 canonical 館藏的三個尺度。

```text
Dawn canonical Works
        ↓
Spectrum / 光譜：讓整個館藏形成可見的知識世界
        ↓
Collection / 策展集：從關係中形成主題與雜誌敘事
        ↓
Morning Star / 三晨星：從主題中形成最高級品牌編輯判斷
```

可以壓縮為：

> 光譜發現關係。
> 策展集整理關係。
> 三晨星表達判斷。
> Dawn 保證其中每一本書始終是同一 canonical Work。

## 4. 光譜的升級方向

光譜應從「黎明書局內的一個展示功能」進一步評估提升為主站級能力。

新的產品假設：

> 光譜可以成為主站第一層 Surface / capability，而不只藏在「橄欖山 → 黎明書局」內部。

理由：

1. 光譜展示的不是單一書局頁面，而是主站知識世界本身。
2. Dawn 館藏、Journal、ONE、多寫以及未來其他 canonical knowledge objects 都可以在光譜中建立關係。
3. 光譜天然適合承接多雷搜索、模糊搜索、知識脈絡與館藏發現。
4. 它可以成為使用者從品牌首頁進入「知識世界」的第一級入口，而不是先進入一個傳統資料庫頁。
5. 主站仍保持內容與品牌編輯結構；光譜作為跨 Surface 的觀看／發現層，不應建立第二套身份資料。

### 重要：主站結構尚未在此備忘中直接修改

目前 canonical `MASTER_SITE_ARCHITECTURE.md` 仍以 Journal / 橄欖山 / Church / About 為主站第一層。此備忘記錄的是**明確待評估的升級方向**：考慮將 Spectrum / 光譜提升為主站第一層。正式改動須在主站架構工程中單獨驗收。

## 5. 「活水動效」第二頁的接入假設

同步記錄另一個重要展示方向：

> 考慮把「光譜」放進主站第二頁「活水動效」中的其中一條流／其中一個方向。

這裡不應把光譜做成普通導航卡片。它應利用「活水」的流動語言表達館藏關係：

- 一條流可以從主站內容逐漸進入 Spectrum；
- canonical Works / 經卷 / 人物 / 主題等關係可以在流動過程中逐漸顯影；
- 使用者不是從首頁「跳轉到一張知識圖」，而是沿活水的一條流自然進入館藏的知識世界；
- 這條流應與其他主站入口保持同一動效語法，但進入光譜後可以發展自己的縮放、聚類、遠近、亮度與知識密度表達。

因此待探索的主站路徑可以是：

```text
第一頁 / 品牌入口
        ↓
第二頁 / 活水動效
        ├── …其他主站方向
        └── Spectrum / 光譜流
                ↓
          館藏知識世界
                ↓
       策展集 / Work / ONE / Journal / 多寫
```

## 6. 光譜 UI / interaction 原則

光譜不應直接渲染一萬多張完整書卡。推薦採用 progressive disclosure / semantic zoom：

- 遠景：主題密度、時代、經卷、知識區域、亮度／聚類；
- 中景：策展集、人物、概念、代表性 Works；
- 近景：具體 Work、Edition、Cover、Reading Pointer；
- 使用者改變觀察坐標時，同一批 Work ID 重新排列，而不是複製館藏；
- 同一 Work 可同時存在於多個主題、策展集和晨星內容中；
- UI 的核心體驗是「尺度轉換」，而不是頁面跳轉。

可探索的成熟思想包括大型文化館藏的 continuous canvas / semantic zoom、timeline、theme / online exhibit、dynamic collection、relational browsing；但實作必須服從黎明書局自己的品牌語言，而不是直接模仿第三方 UI。

## 7. 策展集的新展示角色

策展集應成為 Spectrum 與三晨星之間的雜誌內容層。

例如一個主題不應只輸出「相關書籍 38 本」，而應可以自動／半自動組成：

```text
策展命題
↓
開場文章／編輯導語
↓
關鍵經文／人物／問題
↓
核心 canonical Works
↓
Journal / ONE / 多寫中的相關成熟內容
↓
閱讀／學習順序
↓
延伸館藏
```

多雷可以負責聚類、關係發現、候選 Work、順序與策展命題候選，但公開 Surface 應保持「黎明書局策展」而非退化成「AI 推薦」。

## 8. 三晨星的新展示角色

三晨星繼續是最高級編輯欄目，不降格為分類或演算法榜單。

它可以從成熟策展集中提取本期最值得表達的命題，形成持續出版的 Editorial Stream：主標題、主視覺、主文、主書、策展集和當期館藏關係。

主站／黎明書局的 8:5 動態內容流可承載三晨星：不同內容有不同流速與視覺重量，重要內容可以占兩個或更多 8:5 單元；但三晨星仍然是編輯欄目，而不是三個固定按鈕。

## 9. Doré 在新系統中的位置

多雷不是三晨星、策展集、光譜之外的第四層，也不應以聊天框作為主要存在方式。

多雷在背後提供：

- semantic relation / embedding
- topic clustering
- fuzzy discovery
- curator candidate generation
- collection sequencing
- editorial resurfacing
- reading-context adaptation
- canonical Work relationship enrichment

使用者前台感受到的是：館藏會重排、相關知識會浮現、主題會形成策展、成熟策展會進入三晨星。

這符合既定原則：

> 多雷是一個能力越大負擔越小、越發展越輕量的 AI。

## 10. 自動化程度邊界

```text
光譜：多雷參與極高，編輯介入較低，可動態生成。
策展集：多雷參與高，編輯判斷中高，形成候選與成熟策展。
三晨星：多雷輔助，品牌編輯權最高，不以 engagement 自動排名取代判斷。
```

## 11. Data boundary

新展示系統不得破壞 Step 7 canonical substrate：

```text
Morning Star
    └── Curated Set IDs
            └── Work IDs

Spectrum View
    └── Work IDs + relations + weights
```

Work / Edition / Cover / Reading Pointer 仍全部由 Dawn canonical substrate 掌握。

光譜、策展集、三晨星只保存關係、編輯信息與 Surface 狀態，不建立第二套圖書身份資料。

## 12. 下一輪工程研究問題

1. Spectrum 是否正式升為主站第一層；若升級，它與 Journal / 橄欖山 / Church / About 的結構關係如何定義。
2. 主站第二頁「活水動效」如何讓 Spectrum 成為其中一條真正可進入的流，而不是導航卡。
3. Spectrum 的 canonical relation schema：Work ID + relation + weight + provenance + confidence + editorial state。
4. semantic zoom / continuous canvas 的性能策略，確保萬冊級館藏不一次渲染全部 DOM／封面。
5. 策展集如何從動態候選轉成可版本化、可編輯、可發布的 magazine artifact。
6. 三晨星如何引用策展集與 canonical Works，同時保持最高級人工／品牌編輯權。
7. Core Transcode 完成後，如何把「有身份的 Work」逐步提升為可搜索、可讀、可分析、可策展的 usable Work。

## 13. 本輪總結

> 黎明書局不是把一萬本書擺出來。
>
> 光譜讓一萬本書形成世界。
> 策展集從這個世界形成主題。
> 三晨星從主題形成編輯判斷。
>
> 館藏是資源；光譜是知識；策展集是雜誌；三晨星是黎明書局的聲音。
> 多雷是讓它們持續互相生長的能力。

新增主站探索假設：

> **考慮把光譜提升為主站第一層，並讓它成為第二頁「活水動效」中的其中一條流。**
