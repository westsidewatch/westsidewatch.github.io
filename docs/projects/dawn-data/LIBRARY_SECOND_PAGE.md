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

## 動效化預備：現在做資料契約，不做最終動效
全站 Layout 重建前，封面預覽必須先成為可以被未來動效安全接管的穩定物件。現在不決定封面最後如何飛出、聚集、上挑、放大或進入策展，但必須保留這些可能性。

每一個 cover-preview item 應具有穩定而唯一的 `workId` / `motionKey`，不能以 DOM index、當前排序位置或 shard 位置作動畫身份。重新排序、搜索、語言切換、三晨星／光譜／策展集抽取後，同一本書仍必須保持同一身份，才能做 shared-element / FLIP 類轉場。

封面視覺層與 metadata 層分離：封面 image、placeholder、書名、作者、狀態標記分成可獨立控制的子層。未來放大或移動封面時，不需要重建整張 card，也不把文字烘焙進封面圖片。

預覽資料應預留但不強制使用：

- `motionKey`: 默認由 canonical workId 派生；
- `coverAspectRatio`: 封面天然比例，避免圖片載入後 layout jump；
- `coverWidth` / `coverHeight`: 已知時寫入；
- `coverSource`: 原始封面／來源縮圖／Dawn placeholder；
- `dominantTone` 或等價的輕量視覺提示：僅在可低成本取得時加入，不為此下載大圖；
- `curationRefs`: 三晨星、光譜、策展集對同一 Work 的引用；
- `readingCapability`: 點選後的去向能力，不與視覺動畫耦合。

虛擬化不能破壞動畫身份。二十萬館藏只渲染視窗附近的封面，但被使用者選中的 Work 應能暫時脫離 virtual window，進入獨立的 selection / transition layer；否則封面一旦滾出視窗被卸載，未來的上挑、放大與 shared-element transition 會中斷。

封面尺寸應先有穩定估值／aspect ratio，再載入圖片。虛擬化系統可以動態校正尺寸，但不能讓大量封面在圖片載入後反覆推動整頁 Layout。

動畫性能契約：未來大規模互動優先只改 `transform`、`opacity` 等 compositor-friendly 屬性；避免在大量封面上逐幀改 width/height/top/left。需要重新編排時，使用 layout measurement + transform（FLIP/shared layout）思路，而不是讓二十萬項目參與連續 Layout animation。

第二頁的虛擬化與未來的動效層必須解耦：virtualizer 負責「哪些封面此刻存在」，motion layer 負責「被挑中的少量封面如何運動」。不能把二十萬館藏全部變成常駐 animation nodes。

同時保留 `prefers-reduced-motion` 路徑；動效是導航與策展的提升層，不是進入館藏的必要條件。

## 與第一頁的關係
第一頁暫不鎖定產品答案。

- 若 Dawn 的瞬時翻譯能力很快形成足夠覆蓋，第一頁可成為「外文館藏 → 中文瞬時閱讀」的特色表面。
- 若翻譯覆蓋尚不足，第一頁先以中文資源、中文選題與中文策展作第一可見性。

無論第一頁最後選哪條路，第二頁的二十萬館藏封面預覽層保持不變。

## 第一階段驗收
- canonical Work 能穩定投影為 cover-preview item；
- 不依賴全文下載；
- 大館藏採分片／虛擬化載入；
- 每一本書具有跨排序、跨策展仍穩定的 motion identity；
- 封面比例在圖片到達前已可預估，避免 layout jump；
- 被選中的 Work 可以脫離 virtual window 進入獨立 transition layer；
- 有封面的作品顯示來源封面；
- 無封面的作品仍有穩定 placeholder；
- 點擊後能保持 canonical workId 並進入相應閱讀去向；
- 第二頁成為整個黎明書局館藏的主要可視化入口。
