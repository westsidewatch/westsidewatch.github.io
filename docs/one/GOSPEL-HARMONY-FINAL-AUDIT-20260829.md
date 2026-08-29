# ONE Four-Gospel Harmony Final Audit — 2026-08-29

- Gospel source files inspected: **23**
- Harmony rows inspected: **288**
- Parser-review findings: **6**
- Wrong Gospel-column / chapter-bound findings: **0**
- Sermon-label placement findings: **0**
- Duplicate event labels with differing extents/notes: **12**

## Parser review

- john-17-20.js:40: Expecting property name enclosed in double quotes: line 2 column 11 (char 12)
- john-17-20.js:89: Expecting property name enclosed in double quotes: line 2 column 11 (char 12)
- john-17-20.js:138: Expecting property name enclosed in double quotes: line 2 column 11 (char 12)
- john-17-20.js:186: Expecting property name enclosed in double quotes: line 2 column 11 (char 12)
- john-21.js:49: Expecting property name enclosed in double quotes: line 2 column 9 (char 10)
- john-registry.js:51: Expecting value: line 2 column 9 (char 10)

## Editorial review set

### 不要憂慮
- `太 6:25–34 | — | 路 12:22–34 | —` — luke-9-12.js:11
- `太 6:25–34 | — | 路 12:22–32 | —` — matthew-complete.js:111

### 五餅二魚
- `太14:13–21 | 可6:30–44 | 路9:10–17 | 約6:1–15` — john-5-8.js:9
- `太 14:13–21 | 可 6:30–44 | 路 9:10–17 | 約 6:1–15` — luke-9-12.js:8, mark-5-8.js:31

### 別西卜爭論
- `太 12:22–30 | 可 3:20–27 | 路 11:14–23 | —` — luke-9-12.js:10
- `太 12:22–32 | 可 3:20–30 | 路 11:14–23 | —` — mark-core.js:79
- `太 12:22–37 | 可 3:20–30 | 路 11:14–23 | —` — matthew-complete.js:195

### 向門徒顯現
- `太 28:16–20 | 可 16:14–18 | 路 24:36–49 | 約 20:19–29` — luke-21-24.js:11
- `太 28:16–17 | 可 16:9–14（較長結尾） | 路 24:13–49 | 約 20:19–21:23` — matthew-complete.js:419

### 彼得認信
- `太 16:13–28 | 可 8:27–9:1 | 路 9:18–27 | —` — luke-9-12.js:8
- `太 16:13–20 | 可 8:27–30 | 路 9:18–21 | —` — mark-5-8.js:55, matthew-complete.js:251

### 拿撒勒被拒
- `太 13:53–58 | 可 6:1–6 | 路 4:16–30 | —` — luke-core.js:21, mark-5-8.js:31
- `太 13:53–58 | 可 6:1–6 | 路 4:16–30（較早安排） | —` — matthew-complete.js:209

### 最大誡命
- `太 22:34–40 | 可 12:28–34 | 路 10:25–28 | —` — mark-9-12.js:12
- `太 22:34–40 | 可 12:28–34 | 路 10:25–28（相近問答） | —` — matthew-complete.js:335

### 榮耀進城
- `太 21:1–11 | 可 11:1–11 | 路 19:28–40 | 約 12:12–19` — mark-9-12.js:11
- `太 21:1–11 | 可 11:1–11 | 路 19:28–44 | 約 12:12–19` — matthew-complete.js:321

### 潔淨聖殿
- `太21:12–17 | 可11:15–19 | 路19:45–48 | 約2:13–22（約翰置於事奉早期）` — john-core.js:18
- `太 21:12–17 | 可 11:15–19 | 路 19:45–48 | 約 2:13–22` — luke-17-20.js:10, mark-9-12.js:11
- `太 21:12–17 | 可 11:15–19 | 路 19:45–48 | 約 2:13–22（較早安排）` — matthew-complete.js:321

### 為耶路撒冷哀哭
- `太 23:37–39 | — | 路 13:34–35 | —` — luke-13-16.js:8, matthew-complete.js:349
- `— | — | 路 19:41–44 | —` — luke-17-20.js:10

### 耶穌受洗
- `太 3:13–17 | 可 1:9–11 | 路 3:21–22 | 約 1:29–34` — luke-core.js:20, mark-core.js:55
- `太 3:13–17 | 可 1:9–11 | 路 3:21–22 | 約 1:29–34（約翰的見證）` — one-data.js:85

### 醫治被鬼附的孩子
- `太 17:14–20 | 可 9:14–29 | 路 9:37–43 | —` — mark-9-12.js:9
- `太 17:14–21 | 可 9:14–29 | 路 9:37–43 | —` — matthew-complete.js:265

## Result

Every discoverable Gospel-source `harmony:` occurrence was traversed. JSON-compatible data rows were reference-column checked; non-literal/JS-expression blocks are surfaced above rather than silently skipped. The Matthew 5 sermon-label error is corrected. Differences in verse extent or explanatory notes are retained for editorial judgment rather than normalized mechanically.
