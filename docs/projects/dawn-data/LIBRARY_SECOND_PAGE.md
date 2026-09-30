# 黎明書局第二頁｜館藏浮現層

## 目的
第一步不是改首頁，也不是先決定「中文資源」或「瞬時翻譯」誰佔第一可見性。

第一步是讓目前 canonical 中二十餘萬館藏真正浮現出水面。

第二頁固定為 **館藏封面預覽頁**。它直接建立在 Dawn canonical / living projection 上，以極輕的方式把大量館藏轉化為可看、可掃、可進入的書籍表面。

## 第二頁的基本單元
每一個 Work 以書籍封面為第一視覺，最少包含：

- cover preview
- title
- author
- language
- canonical workId
- reading destination / capability

封面不存在時允許生成一致的 editorial placeholder，但不得因此把 Work 排除出館藏。

## 原則
1. 不下載全文，不因正文能力阻塞封面館藏頁。
2. 封面是 preview / navigation asset，不是新的館藏 authority。
3. 優先使用來源已提供的合法封面／縮圖；沒有時再使用黎明書局自己的輕量封面生成。
4. 第二頁必須支持二十萬級館藏，因此不得一次把全部封面 DOM 或全部圖片載入瀏覽器。
5. 使用 shard/index + window/virtualized rendering + lazy cover loading；只載入當前視窗附近的作品。
6. 搜索、分類、語言、作者、三晨星、光譜、策展集都應指向同一 canonical Work，不建立另一套書目身份。
7. 點擊作品後按其 reading capability 進 Dawn Reader、翻譯閱讀或外部閱讀；第二頁本身不負責解決正文取得。

## 與第一頁的關係
第一頁暫不鎖定產品答案。

- 若 Dawn 的瞬時翻譯能力很快形成足夠覆蓋，第一頁可成為「外文館藏 → 中文瞬時閱讀」的特色表面。
- 若翻譯覆蓋尚不足，第一頁先以中文資源、中文選題與中文策展作第一可見性。

無論第一頁最後選哪條路，第二頁的二十萬館藏封面預覽層保持不變。

## 第一階段驗收
- canonical Work 能穩定投影為 cover-preview item；
- 不依賴全文下載；
- 大館藏採分片／虛擬化載入；
- 有封面的作品顯示來源封面；
- 無封面的作品仍有穩定 placeholder；
- 點擊後能保持 canonical workId 並進入相應閱讀去向；
- 第二頁成為整個黎明書局館藏的主要可視化入口。
