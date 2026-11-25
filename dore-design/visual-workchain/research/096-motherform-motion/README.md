# 多雷探索 §9.6 — 母本作為畫面、邊界與時間（2026-11-25）
研究證據；不修改 OS，不改正式網頁、不改既有 P2/3D、不採用 R19 或已否決的 #1442。分支從 R14 b01ede0ac27e018b2dae169e293b6c18ed9ecd93 建立。
## 新查核的原始案例
- Columbia Books (Linked by Air, 2015): https://www.linkedbyair.net/work/37-columbia-books-on-architecture-and-the-city 。實際原始規格圖顯示五種比例與十三種線粗；頁數決定線粗、書形決定比例，原標誌同時是網頁點擊熱區。規格圖 https://cdn.filepicker.io/api/file/W5n2crz4So6gwJDipAtR/convert?compress=true&fit=max&format=jpg&w=3072 已直接檢視。現行 https://www.arch.columbia.edu/books 可取得文字，但未實測其當前動效。不是照抄叉線或固定方框。
- Museo del Contemporaneo (Simone Stucchi / Blank_Spaces): https://simostucchi.com/work/museodelcontemporaneo 。標誌字母延展至版緣，構成內容的框架。原始品牌總圖已查看；工作室聲明涵蓋網站，未取得實際動態網站證明，不宣稱已檢視其運行。
- Tang Museum: 2015 網站 https://www.linkedbyair.net/work/8-tang-museum-website （風速風向／訪客變化的底紋，印刷物有相同邊紋）；2018 館藏 https://www.linkedbyair.net/work/85 （雙聯畫、內容關聯），直接查看工作室館藏截圖；2025 識別 https://www.linkedbyair.net/work/248-tang-museum （建築階梯、混凝土方塊）。三者不同年份，不能拼接成已證實同一套當代識別演化。現行 https://tang.skidmore.edu/ 可取得文字，未操作其動畫。
- Future Expansion: https://www.linkedbyair.net/work/5-future-expansion 。建築平面圖即網站，篩選改變空間；查看設計師歷史項目內頁截圖，現站未核實。借鑑內容關係改變構成，不複製頁面或箭頭。
- DIA Flodesk: https://dia.tv/project/flodesk/ 。動效系統延續至實際產品，動作本身可成為品牌規則。
- Garden Museum: https://www.pentagram.com/work/garden-museum 。抽象形態組合成插畫，拆解成識別；網站採較克制的應用。借鑑同一形態在高密度藝術與日常閱讀的尺度轉換，不複製配色。
## 已存在的本站證據
基線 #1419 SHA b58bd2fb6f75310a79386581f6ecdd4e28ac56ea；docs/design/WESTSIDE-EDITORIAL-MANUAL.md blob eab0c4a38c6f433360bc009b1eff0267a87a60df 的 §9.6 已查閱。static/js/p2-0105-dawn-continuation.js blob 101d8e3c5915f618141881a52d0146b436a19e5d 的 paintAnchor、paint：實際來源雙方塊在 26.63–26.83 移動、26.83–27.13 旋轉、27.13–27.33 替換；左、右分開遮罩反向揭露，兩半完成前原畫面仍保留。這是既有正確的動態語法證據（源碼，不是本輪瀏覽器驗收）。
## 可執行原理校樣：母本的刻線成為裁切邊界
R11 原始 art-water（blob f44194c40a34731ff73a8bbb9527aadacb802082）完全不改。讀取原始六線與原有180°對向群組；將最內側真實階梯線的座標解析成遮罩，沿原線邊界揭露原活水刻線圖，兩組線向外退讓，露出完整畫面後才顯現既有建築白模。原刻線與白模皆是既有資產，沒有另造方塊、網格、按鈕卡或新整站版面。以手動控制進程作逐幀視覺研究，未改實際 P2 的水開與白模生長時間。這是單一藝術機制試片，非七版塊視覺設計定稿；模型只是既有最終白模，不聲稱重新製作其生長。需驗收實際畫面、整體藝術性，才能擴展。不得僅以幾何測試通過作設計通過。
