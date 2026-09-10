# DORÉ Biblical Long Scroll — Authoring & Recording Rules

> Status: LOCKED / CANONICAL  
> Applies to: DORÉ Biblical Long Scroll project  
> Date recorded: 2026-09-10

## 完全記錄／文案：逐字保留規則

在本項目中，當創作者說：

- 「完全記錄」
- 「完整記錄」
- 「這是文案」
- 「文案」
- 或其他明確表示這段文字本身需要成為作品內容的指令

均表示：**這些文字本身就是作品的一部分，必須完整保存。**

### 硬性規則

1. **不允許擅自總結。**
   不得把一段完整論述按照 AI 自己的理解壓縮成一句話、一個 bullet、一條 principle 或一段摘要後，就把摘要當成「已記錄內容」。

2. **不允許擅自改寫。**
   當內容被指定為「完全記錄」或「文案」時，原始文字的措辭、次序、語氣、重複、強調與邏輯關係本身都具有作品價值。除非創作者明確要求修改，否則不得自行潤色、重組、改成更正式的語言、替換詞語或改變表達。

3. **完整保存優先於整理。**
   可以另外增加索引、標題、metadata、工程註釋或摘要，但這些只能作為附加層；不能取代原始文案。原始文案必須完整存在並可以被重新取出。

4. **摘要與原文必須分離。**
   如果工程需要一份短版 specification，可以從文案另外派生；但必須明確標記為 summary / derived specification。不得把派生摘要回寫覆蓋 canonical copy。

5. **不得因為內容重複而自行刪除。**
   文案中的重複可能承擔節奏、強調、神學或敘事作用。是否刪除只能由創作者決定。

6. **不得因為 AI 認為有更好的說法而修改。**
   AI 可以提出建議，但在沒有明確批准前，建議不能進入 canonical copy，更不能替換創作者原話。

7. **GitHub 記錄必須保留可追溯性。**
   被指定為作品文案的內容應以 Markdown 等可版本控制形式保存，使原文、後續修訂與派生工程規格可以區分和追蹤。

### 判定原則

> **只要創作者說「完全記錄」或說這是「文案」，默認含義就是：我要保存的是這些文字本身，而不只是這些文字所表達的大意。**

> **文字本身就是作品。不得用 AI 的總結替代作品。不得胡亂改。**

### 與 Narrative Constitution 的關係

`DORÉ-BIBLICAL-LONG-SCROLL-NARRATIVE.md` 是本項目的 Narrative Constitution；本文件規定它以及後續所有作品文案應如何被記錄和修訂。

如果未來需要從 Narrative Constitution 生成動畫工程規格、scene schema、prompt、issue、PR 描述或其他技術文件，應從 canonical 文案派生，而不是反過來修改 canonical 文案以遷就工程格式。
