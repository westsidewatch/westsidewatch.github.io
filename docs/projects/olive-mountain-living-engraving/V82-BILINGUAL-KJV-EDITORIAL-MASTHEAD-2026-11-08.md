# P2 橄欖山 V82｜中英 KJV 對讀與獲獎導向版頭排版

2026-11-08 · Draft PR #1385 · 不合併 main

## 使用者要求及不變項

1. 橄欖山版塊主題經文改為 **和合本中文 + King James Version 英文**（羅馬書 10:17）；原「OLIVE MOUNTAIN／橄欖山」中文不可消失。
2. 十二位講員旁邊各一個閱讀欄，原 CUV 配經**同時顯示 KJV 英文節錄**，中文主、英文次、雙語章節。**經文不放在翻轉卡背面**，保留 V81 被糾正後的相鄰關係：左講員右經文、右講員左經文。
3. 所有來源與經文證據分類保留於 V80 檔案，不能宣稱是講員引用頻次的統計；英譯只是同一聖經章節，不是把中文翻譯成自行撰寫的英文。
4. 保護原始 12 海報、Shadow DOM Bodoni、翻卡剛體與 V79 可逆動效、V77 地形、V79 植物、01–03／以馬忤斯和終場背景。

## 版頭藝術判斷

根據 `docs/design/WESTSIDE-EDITORIAL-MANUAL.md` §2、§3、§6：讀者的視線應是**刊號／邀請 → 英文書刊大標＋中文錨點 → 一條細金刻線 → 左側中文經文／右側 KJV → 章節出處 → 講員與其經文對開**。這不是把四段文字在同一中線等距垂直堆疊。

新排版採用同一 OS 字體和雙色墨：
- 細小第一行 `04 / 07 · THE WORD`，右端 `INVITATION TO HEAR ／ 誠邀聽道`，水平分散但閱讀關係明確。
- 第二行左側 Bodoni Moda 的 `OLIVE MOUNTAIN`（MOUNTAIN 斜體），右側較重中文 `橄欖山` 作**有重量的中文印章式錨點**。這不是新的第二個英文品牌。
- 第三行以**唯一一條細金色橫線**劃開中英主題經文：左側和合本，右側 KJV Bodoni Italic。每欄最下獨立標示 `羅馬書 10:17` 和 `ROMANS 10:17 · KJV`。
- 下方講員旁側的英文本身採 OS 英文 Bodoni Italic 較小級，中文經文採 OS Chiron Hei HK WS，書卷出處在金線之下成對校準；字數長時允許自然換行，但不剪斷原圖。
- 禁止大面積黑色背景、非 OS 顏色、拉伸字形、動畫淡入追趕、無意義的多重邊框，以及字體細到無法閱讀。

## 技術實作

- `static/js/p2-0104-olive-scriptures-v80.js`：保持十二人原順序和 `excerpt` 中文，新增 `excerptEn`（KJV 英文短節錄）及 `translationEn='KJV'`；版塊主題同樣有 KJV。
- `static/experiments/p2-0104-olive-continuation.html`：重構 `#olive-rubric` 成獨立刊號／同列中英文大標／雙欄經文三層；新增每個 `.olive-stage__companion` 的 `blockquote[lang=en]` 和英文章節。
- `static/js/p2-0104-olive-continuation.js`：資料依 speaker id 寫入原 V81 獨立旁側欄位；沿用一個 `paint()`，不引入新的動畫計時器。英文與中文同時隨講員更換；卡背仍只有版畫。
- `static/css/p2-0104-olive-continuation.css`：OS 範圍內的 V82 版頭和 CUV／KJV 雙語排版；1648／390／320 三寬度具體視覺驗收。

## 出處與使用界限

英語採原 King James Version 經文短節錄；其中使用刪節號「…」者是排版所需的部分節錄，沒有自行改寫語法。可核對的 KJV 文本資料：
- https://www.biblegateway.com/versions/King-James-Version-KJV-Bible/
- https://www.bible.com/versions/1-kjv-king-james-version
- 羅馬書 10:17、加拉太書 2:20、以弗所書 6:12、提摩太後書 3:16、羅馬書 1:16、啟示錄 1:3、馬可福音 1:38、雅各書 1:22、約翰福音 7:38、15:5、歌羅西書 1:16、以弗所書 3:20、腓立比書 4:7。

## 驗收門檻

- 十二位講員旁側均能見 CUV+KJV，且更新後同一講員的兩種語言不串人，全文及出處始終在同側閱讀欄。
- 版頭中英文真實字距和光學對位一致，金色唯一分隔線、兩個經文欄不撞、英文 KJV 不回繞成單獨一字；頂部刊頭不遮住任何 3:4 海報的鎖定文字。
- 320、390、1648 真正 Chromium 截圖檢查。GitHub CI 綠燈只是技術門檻，不等同獎項級視覺認可。
- 若任一寬度失敗，保持 Draft、修正後重測；不得借本版更改 01–03 或合併主站。
