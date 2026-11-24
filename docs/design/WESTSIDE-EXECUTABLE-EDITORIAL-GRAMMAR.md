# Westside Design OS · 可執行雜誌編輯語法（Editorial Grammar v1）

**工程狀態：已實作，可直接輸出 Hugo HTML。七版塊使用相同渲染器，使用不同構圖資料。**
**藝術狀態：新方向候選；在七頁人工審核通過前不得合併到正式主站。**

此文件是設計 OS 的可執行章節，不另建 Design OS，不覆蓋首頁、Merci、P2、既有教會 3D、橄欖山十二海報或黎明書局第二／三層。

## 設計研究來源：四本雜誌，不是四套可供複製的外觀

| 參考網站 | 已確認的編輯結構 | Westside 實作語法 |
| --- | --- | --- |
| [The Paris Review](https://www.theparisreview.org/) · [2026 年第 257 期目錄](https://www.theparisreview.org/back-issues/257) | **期號、分類、作品、訪談與可跨期查找的完整館藏**，而不只是首頁廣告式卡片 | `issue`、`index.issue-toc`、`essay.narrow`、`conversation.editorial-dialogue` |
| [The Paris Review / Pentagram](https://www.pentagram.com/work/the-paris-review) | 2021 年紙本重設計參照 1960–1970 年代的編輯秩序，減少封面資訊、重視作品和舒適閱讀 | `cover.poster`、圖版優先、正文閱讀寬度、館藏條目 |
| [Emergence Magazine](https://emergencemagazine.org/) | 同一出版品牌容納文章、影像和長篇敘事 | 內容可以自由決定模組先後，不要求七頁一樣 |
| [Aperture](https://aperture.org/) | 從既有出版設計整合藝術機構品牌 | 以《西望》的字體、刊頭與期刊語法作為七版塊共同骨架 |
| [The Public Domain Review](https://publicdomainreview.org/) | 歷史文獻、圖像與文章策展的閱讀關係 | `plate` 的來源和圖說、`index` 的分層資料、`shelf` 的作品本位結構 |

The Paris Review 2016 年推出完整數位檔案；2021 年的 Pentagram 重設計著重藝術封面與書本閱讀感。這裡借用其**出版方法**，沒有複製對方的字體、版面資產或品牌識別。

## 1. 原則：設計語法本身必須產生可使用的網頁

**交付契約：**

`內容 JSON → 設計語法編譯器 → 共用 Hugo partials → Westside Design OS → HTML / CSS → Cloudflare Pages`。

不允許「設計研究完成後，又手動重做一份毫無關係的網頁」。同一份 JSON 就是預覽與正式發佈使用的內容母本。

**真實檔案：**

- `data/editorial/grammar/<composition-id>.json`：唯一可編輯的構圖指令、文字及資產連結。
- `layouts/partials/editorial/grammar/page.html`：共用出版外殼、版塊身份、期號、返回和七版塊目錄。
- `layouts/partials/editorial/grammar/cover.html`：七種版頭構圖。
- `layouts/partials/editorial/grammar/block.html`：六種可組合的正文模組。
- `static/css/westside-editorial-grammar.css`：唯一在這批頁面生效的 OS 樣式；使用 OS 的 Chiron、Bodoni、紙張、黎明金、活水藍、橄欖綠、收穫黃與各版塊權限。
- `layouts/_default/ws-editorial-interior.html`：現有 Hugo 頁型的調用點，已切換為 Grammar renderer。
- `content/{realm}/folio.md`：原有七個基準路由，**目前實際調用新語法**，不再使用之前被否決的固定左右雙欄母版。
- `scripts/editorial-grammar-new.mjs`：新增文章時從內容檔直接產生新的 Hugo 網頁。

## 2. 封面七種語法，而不是七頁只換顏色

| 指令 | 視覺構圖 | 頁面示例 |
| --- | --- | --- |
| `identity` | 使用不可修改的原始中文字樣；雙語名稱與導讀相互構成 | 教會 |
| `poster` | 大型藝術圖版先入場，文字作另一幅編輯面 | 西望 |
| `atlas` | 史地刻線全幅領先，經文及導讀隨後展開 | 以馬忤斯 |
| `portrait` | 講員肖像為主，人物名稱與導讀成右側排版 | 橄欖山 |
| `ledger` | 作品／圖版索引式刊頭，偏出版檔案 | 黎明書局 |
| `cinematic` | 深色銀幕構圖，適合電影影像與評論 | 天堂電影院 |
| `quiet` | 大留白與日常物件，安靜地進入生活閱讀 | 白晝咖啡館 |

**語法只選擇結構和排版角色，不覆寫內容系統。** 例如書局 Work ID 與封面來源仍由既有黎明書局管理；教會主日日程仍由 P2 單一來源管理；電影院片源仍需播放驗證。不能因「網頁模板已出現」就冒稱這些外部資料已更新。

## 3. 正文六個可以直接渲染的指令

- `essay`：真正可讀的長文。模式 `narrow` 或 `reading-with-margin`；需有小標、正文段落；可以附頁側引註。
- `scripture`：直接嵌入原有 Scripture Studio V60 的中文豎排鉛字母版；模式 `opening-margin`、`folio`、`inset` 或 `glass-aside`；**不允許重新發明字體排版**。
- `plate`：真正的攝影、原有書封或雕版圖像；需有可追溯的主站圖像路徑、替代文字和圖說。模式 `full-bleed`、`wide`、`portrait-folio` 或 `letterbox`。
- `index`：期刊目錄、真實分章鏈接；模式 `issue-toc`、`numbered` 或 `columns`。
- `conversation`：訪談或教會問答；以語義化 Q/A 排列，不得偽造講員或作者原話。
- `shelf`：作品及編輯欄目的來源清單；不能以無來源的虛構書封代替館藏。

這六種模組可以自由排列。沒有「每頁先大標、右邊經文、下面目錄、最後一張圖」這種固定規則。**要先編輯內容，再組成頁面。**

### 可直接渲染的實際 JSON（節錄）

```json
{
  "schema": "westside.editorial-grammar.v1",
  "realm": "emmaus",
  "genre": "scripture-study",
  "cover": {
    "mode": "atlas",
    "eyebrow": "Emmaus · Scripture and World",
    "titleZh": "以馬忤斯",
    "titleEn": "On the Road",
    "deck": "從經文出發，沿著歷史、人物與土地，進入一段可以繼續研讀的路。",
    "art": {
      "src": "/images/p2-realms/v15/03-emmaus-engraving-p2-runtime.svg",
      "alt": "以馬忤斯原有 P2 刻線經卷圖"
    },
    "issue": "03 / Study"
  },
  "blocks": [
    {"type": "scripture", "id": "luke", "mode": "opening-margin", "heading": "凡經上所指著自己的話"},
    {"type": "essay", "id": "reading", "mode": "reading-with-margin",
     "eyebrow": "Luke 24:27", "title": "從摩西和眾先知起",
     "paragraphs": ["路加福音二十四章描寫復活的耶穌在以馬忤斯路上，從摩西和眾先知起，向門徒講解聖經中指向祂的事。"]}
  ]
}
```

這不是概念性示意語法；語法結構正是目前用於 `/emmaus/folio/` 的渲染資料格式。

## 4. 新增一張網頁，只需要提供一份構圖資料

在本地編輯準備好的 JSON 後執行：

```bash
node scripts/editorial-grammar-new.mjs \
  --realm=journal \
  --slug=new-essay \
  --source=fixtures/editorial-grammar/journal-proof.json
```

這會生成：

1. `data/editorial/grammar/journal-new-essay.json`（完整內容與可編輯排版）。
2. `content/journal/new-essay.md`（Hugo 入口，**預設 draft: true**）。
3. `/journal/new-essay/`（使用原 OS、刊頭、導航及語法組件的實際頁面，透過 draft build 可預覽）。

本地預覽：`hugo server -D`。內容、來源和權限審核完成後才可將 `draft` 改為 `false` 發佈；命令初次生成時也支持經明確確認後的 `--publish`。已有路由與構圖文件**禁止覆蓋**。

這種模式可以產生更多新書單、講員詳情、文章、電影評論與生活專欄，而不是七份固定頁面。**如果編輯了一段文字，改動會直接顯示在生成網頁上；不再需要另一輪手工實現。**

## 5. 必須實際通過的技術驗收

工作流程 `.github/workflows/editorial-sevenfold.yml` 必須做四件事：

1. 七個版塊的組件結構、字體和資產權限通過契約測試；所有七份編輯資料都有實際內容。
2. 在 CI 裡使用新增頁面指令，從 `fixtures/editorial-grammar/journal-proof.json` **真正建立第八張測試網頁**。
3. Hugo 必須輸出七個 `public/{realm}/folio/index.html`，以及新生成的 `public/journal/grammar-proof/index.html`。
4. Chromium 打開七個實際頁面，逐一量測 1440、768、390、320px 的版頭、正文模組、原有 V60 經文、圖像實際顯示及頁面橫向溢出，保留截圖。瀏覽器還必須開啟生成的第八張測試頁，確認文字和模組由新 JSON 直接呈現。

**CI 綠燈只是工程可用，不代表藝術水準已經定稿。** 進入正式版塊之前還需跨頁視覺評審和內容來源逐項校對。

## 6. 遷移規則

以前的七張固定版型可以保留 Git 歷史，但不能作為 OS 的新標準。這次新語法首先只接手隔離的 `/folio/` 預覽頁。經人工批准後，才依照相同語法漸進接入第二／第三層的實際內頁，保留之前已完成的動效、資料模型與互動功能。

**成功標準只有一個：從資料、版面到可發布網頁是一條工作鏈。** 單純分析設計網站、畫一張風格參考圖或寫一份 UI 手冊，都不能算完成。

## 9.6 第一輪內容空間轉譯（R4，2026-11-24）

既有 cover mode 和 block mode 必須改變真實構圖，而非只換顏色。詳見編輯手冊 §9.6；實作只在原 CSS 和 Hugo renderer，保留原始內容、路由和 V60。首輪候選尚未覆蓋既有 P2、首頁、二三層正式交互頁；不將這七頁等同於全站提升完成。
