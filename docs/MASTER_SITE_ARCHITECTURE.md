# Living Water Westside Watch — 主站唯一結構記錄

> **Status: Canonical / Current**  
> 本文件是 Living Water Westside Watch 主站資訊架構的唯一入口。今後涉及主站欄目結構、上下層級、欄目定位、功能組合、網站設計學習與 Doré 學習，先讀本文件；其他舊筆記、對話整理、品牌 PDF、早期結構文件只作歷史參考，不得覆蓋本文件。

## 0. 權威規則

1. **現行使用者明確定論優先於舊文件、舊 PDF、舊對話摘要。**
2. GitHub `main` 的實際網站結構用來核對已落地的程式結構；概念架構以本文件為準。
3. **不存在「安提阿」欄目。** 任何舊文件出現「安提阿」均視為歷史版本，不得恢復。
4. Journal 的 12 個欄目、三個間奏仍然屬於 **Journal**；被新功能組合使用，不等於離開 Journal。
5. 「功能」與「欄目」不是同一層：一個功能可以調用多個既有欄目，但不得因此改寫欄目的歸屬。
6. Doré 不是網站；Doré 是支撐網站、內容、研究、設計、工程、編輯與自動化的 AI / Agent 工作系統。
7. Storybook 不是黎明書局的子項；Storybook 是 Doré Design 用來訓練、驗證整個 Westside Watch 網站設計系統的環境。

---

# 1. 主站總體結構

**Living Water Westside Watch** 是網站本體。

現行主站的核心第一級資訊架構為：

```text
Living Water Westside Watch
│
├── Journal          期刊核心
├── Website          品牌內容容器／網站延伸內容
├── Church           教會生活服務
└── About            關於／功能入口
```

這一級關係已在網站建置中確立：Journal 是期刊核心，Website 是品牌內容容器，Church 服務教會生活。舊版曾把 Website 誤命名為 Resources，後已恢復為 Website；`/resources/` 僅作舊網址轉址，不代表現行架構名稱。

> **重要：這裡的 Website 是主站第一級架構名稱，不是「整個網站」的另一個名字。**

---

# 2. Journal

## 2.1 Journal 的地位

Journal 是 Westside Watch 的期刊核心。

它不是普通文章列表，而是一個具有四個樂章、十二個固定欄目、三個間奏的完整編輯結構。

閱讀主路徑曾確立為：

```text
Cover → Opening → Contents → WATCH → WALK → WITNESS → WORSHIP
```

Vol.00 是 founding volume / 基礎卷，不是普通的一期雜誌。

## 2.2 四個樂章

```text
I   WATCH      守望
II  WALK       同行
III WITNESS    見證
IV  WORSHIP    敬拜
```

四個 W 是 Journal 的生命／禮儀循環，不只是視覺分區。

已確立的樂章轉調為：

```text
WATCH → WALK
WALK → WITNESS
WITNESS → WORSHIP
```

三個間奏位於樂章之間，承擔 modulation / 轉調，而不是第 13、14、15 個固定欄目。

## 2.3 十二個固定欄目

目前採用的 12 欄目骨架為：

### I WATCH 守望

1. **米斯巴 Mizpah** — 卷首
2. **伯利恆 Bethlehem**
3. **門 The Gate** — 守望神學／公共信仰思考的持續對話
4. **迦密 Carmel** — Feature / Living Feature
5. **何烈山 Horeb** — 神學、聖經與教義；核心意義是神先尋找人
6. **西區的夜晚 Westside Night / Emmaus** — 線上查經工具／查經工作台

### II WALK 同行

7. **以琳 Elim** — 神的供應、靈命滋養、禱告與恢復
8. **別是巴 Beersheba** — 人對神恩典的回應、盟約、信靠與委身
9. **伯特利 Bethel** — **目前最新定論：每日靈糧／A Day 所在的固定欄目**；A Day 是伯特利在網站上的活體形態。其欄目歸屬仍然是 Journal，不是獨立功能。

### III WITNESS 見證

10. **以斯帖 Esther** — 人物／見證類內容
11. **亞杜蘭洞 Adullam / 守望者** — 當代人物／對話／訪談方向

### IV WORSHIP 敬拜

12. **瑪拉拿 Maranatha** — 結語、閉卷禱告與讚美

### 關於十二欄目名稱的版本衝突

早期 PDF／舊討論中曾出現「安提阿」，也曾把伯利恆寫成每日靈糧、把伯特利寫成教會生活。**這些均不得作為目前結構的覆蓋來源。**

現行最新定論以使用者明確修正為準：

- **伯特利 = 12 個固定欄目之一**
- **A Day / 每日靈糧 = 伯特利欄目目前的活體內容形態**
- **三個間奏仍然存在**
- **不存在安提阿**

尚未被最新定論重新指定的舊欄目副標，不得自行推導新結論。

---

# 3. Journal → 西區的夜晚 → ONE

這條上下級關係已經明確：

```text
Journal
└── 西區的夜晚 / Emmaus
    └── ONE
```

「西區的夜晚」不是普通文章展示欄，也不是資源庫。

它是可以在實際查經現場使用的 **online Bible-study workbench / 查經工作台**，包括：

- 經文對比
- 解經內容
- 查經資料
- 相關工具與網站集合
- 查經進度
- 聚會通知／海報
- 查經內容與心得

其中發布與存檔只是外層；核心是「現在就可以一起打開聖經使用的工具」。

**ONE 是西區的夜晚下面的工具，不屬於 Website／橄欖山／黎明書局。**

---

# 4. Journal 的三個間奏

三個間奏不是被刪除的舊欄目，也不是離開 Journal 的獨立模塊。

現行已知三個間奏為：

```text
Journal
│
├── 間奏一：Selah／細拉
├── 間奏二：遠方無聲鴿
└── 間奏三：基尼烈 Kinneret
```

它們的原始結構作用是三次 modulation：

```text
WATCH → WALK       Selah
WALK → WITNESS     遠方無聲鴿
WITNESS → WORSHIP  基尼烈
```

三個間奏仍是 Journal 的欄目性結構單元。

---

# 5. A Day／每日靈糧與「新聞播報」新功能

這是目前最容易再次發生層級混亂的地方。

## 5.1 欄目層

```text
Journal
└── 伯特利
    └── A Day / 每日靈糧
```

A Day **不是 Journal 外部的新模塊**。

## 5.2 功能層

現在建立一個新的 **新聞播報功能**，它重新組合 Journal 中已經存在的內容單元：

```text
新聞播報
│
├── 伯特利／A Day／每日靈糧
├── 間奏一
├── 間奏二
└── 間奏三
```

因此：

> **欄目仍歸 Journal；新聞播報只是跨欄目功能組合。**

不能把「新聞播報」寫成 Journal 的第 13 個欄目，也不能把 A Day 或三個間奏移出 Journal。

## 5.3 秒報

「秒報」是新聞播報中的新聞滾動／即時信息概念。

它與西望正在形成的 Editorial Flow 相連：

```text
世界發生
→ Doré 看見
→ 搜索／核驗／理解
→ 編輯判斷
→ 信息進入流
→ 權重變化
→ 必要時重新編排
```

秒報不是要求畫面每秒閃動，而是允許 Doré 持續判斷；只有編輯重量真正改變時，頁面才重新排列。

---

# 6. Editorial Flow / 信息瀑布流

這是網站正在形成的重要跨內容視覺／產品語法，但它不是一個新的網站第一級欄目。

基本語法：

```text
尺寸 = 編輯重量
位置 = 內容關係
聚集 = 主題關係
流入 = 新信息出現
移動 = 編輯判斷改變
縮小 = 重要度下降但沒有消失
退出主流 = archive / knowledge layer
放大 = 從瀏覽進入閱讀／觀看／聆聽
```

5:8 是最高編輯重量的核心視覺比例之一。

同一套 Editorial Flow 可以容納：

- 三間奏新聞
- A Day／伯特利靈糧
- 《西望》文章
- ONE 經文入口
- 影片
- 圖像
- 聲音
- 問題
- 黎明書局新發現

但它們的**內容歸屬不因此改變**。

---

# 7. Website → 橄欖山

Website 是主站第一級架構名稱；進入其內容入口後，目前實際呈現名稱為：

**橄欖山**

現行 repo 已確認 `content/website/_index.md` 使用「橄欖山」作 display title。

橄欖山是 Journal 之外的品牌內容／生活／資源空間。

目前已確認的子項包括：

```text
Website / 橄欖山
│
├── 黎明書局 / Dawn Library
├── 白晝咖啡館 / Daylight Café
├── 守望禱告會（持續內容系列）
├── Podcast
├── Video
├── Newsletter
└── 其他後續內容系列
```

## 7.1 黎明書局

黎明書局是具有編輯判斷與策展邏輯的數位資源系統。

核心原則：

> 從經文開始，讓工具服務研讀，讓資源進入生命。

它是橄欖山下面的內容／產品空間，不是 Journal 的一個固定欄目。

## 7.2 白晝咖啡館

白晝咖啡館是橄欖山下面的生活與文化空間，服務：

- 信仰與工作
- 城市生活
- 文化
- 對話
- 日常生活

它：

- **不是 Journal 十二欄目之一**
- **不是 Church 聚會公告頁**

## 7.3 守望禱告會

Website 下的「守望禱告會」是持續內容系列。

它不能與 Church 下實際的 Prayer Meeting 混為同一頁／同一層級。

---

# 8. Church

Church 是與 Journal、Website 同級的主站第一級架構。

它服務真實教會生活，而不是 Journal 的欄目集合。

現行 Church 結構基礎：

```text
Church
│
├── About
├── Sunday Worship
├── Bible Study
├── Prayer Meeting
├── Contact
└── Giving
```

其中：

- Bible Study 是 Church 的實際教會服務入口；西區的夜晚／Journal 欄目可以成為其內容與工具的關聯入口，但**西區的夜晚本身仍是 Journal 欄目**。
- Prayer Meeting 是 Church 的實際聚會頁。
- Website 下的「守望禱告會」是內容系列，二者不能混成一頁。

---

# 9. About

About 是主站第一級導航／功能入口。

它不是 Journal 欄目，也不是 Website 子欄目，也不是 Church 子欄目。

---

# 10. Vol.00

Vol.00 是 Westside Watch 的 founding volume / 基礎卷。

它承擔建立整個 Journal 世界觀、四樂章、十二欄目與三個間奏的作用。

閱讀上採取：

```text
Cover
→ Opening
→ Contents
→ WATCH
→ WALK
→ WITNESS
→ WORSHIP
```

連續閱讀是主要路徑；跳轉是輔助。

---

# 11. Journal、Website、Church 三者不能混層

最簡明的判斷方式：

| 層級 | 核心問題 | 內容 |
|---|---|---|
| Journal | 我們如何觀看、同行、見證、敬拜？ | 12 欄目 + 3 間奏 + 4 樂章 |
| Website / 橄欖山 | 期刊之外，哪些品牌內容繼續流動？ | 黎明書局、白晝咖啡館、Podcast、Video、Newsletter、守望禱告會等 |
| Church | 教會實際生活如何被服務？ | About、Sunday Worship、Bible Study、Prayer Meeting、Contact、Giving |
| About | 我們是誰／網站功能資訊 | About |

---

# 12. Doré 與 Storybook

## Doré

Doré **不是主站的一級欄目**，也不是網站名稱。

Doré 是支撐整個系統的 AI / Agent 工作系統，包括研究、搜索、內容理解、編輯、設計、工程、圖片生成、工作流與自動化等。

## Storybook

Storybook 不屬於黎明書局，也不屬於 Journal 的某一欄。

Storybook 是 Doré Design 的**全站設計系統訓練／驗證環境**。

它的範圍是整個 Living Water Westside Watch：

- Homepage
- Journal
- Journal 12 欄目
- Website / 橄欖山
- 黎明書局
- 白晝咖啡館
- Church
- About
- 搜索與其他網站功能

因此今後 Storybook 的工作不能只以黎明書局為範圍。

---

# 13. 「唯一入口」工作規則

今後任何涉及主站結構的工作，按以下順序：

```text
使用者提出修改／新功能
        ↓
先讀本文件
        ↓
判斷：這是「欄目」「內容」「功能」「產品」「跨欄目組合」還是「設計系統」
        ↓
確認父層與子層
        ↓
若與本文件衝突，以最新使用者明確定論更新本文件
        ↓
再修改網站／Doré／Storybook
```

不得再從零散的舊 MD、PDF、聊天摘要自行拼裝主站樹。

## 變更記錄規則

每次主站結構發生正式變更，必須更新本文件，至少記錄：

- 日期
- 變更項目
- 原結構
- 新結構
- 父子層級變化
- 是否改變欄目歸屬
- 是否只是新增功能組合
- 受影響的 Doré／Storybook／網站項目

---

# 14. 歷史資料的處理

下列資料可以保留作歷史討論，但**不能作為現行結構權威**：

- 舊版 Brand Standards 中出現的「安提阿」
- 舊版把伯利恆定為每日靈糧、伯特利定為教會生活的描述
- 早期 Website / Resources 混用版本
- 早期把西區的夜晚當普通內容欄的版本
- 任何沒有經過最新定論確認的欄目名稱或副標

歷史資料的價值是解釋「怎麼走到今天」，不是決定「今天是什麼」。

---

# 15. 一句話總索引

> **Living Water Westside Watch = Journal + Website / 橄欖山 + Church + About；Journal 內固定有 12 欄目與 3 間奏，其中伯特利承載 A Day／每日靈糧，西區的夜晚之下有 ONE；A Day 與三個間奏現在被重新組合成新聞播報功能，秒報是其滾動新聞機制，但這些欄目仍全部屬於 Journal；Website／橄欖山之下有黎明書局、白晝咖啡館等內容系列；Church 與 Journal、Website 同級；Doré 是支撐系統，Storybook 是全站設計訓練／驗證環境。**
