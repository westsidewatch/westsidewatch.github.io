# ONE Four-Gospel Harmony Audit — 2026-08-29

- Harmony blocks inspected: **84**
- Harmony rows inspected: **288**
- Source files: **john-13-16.js, john-5-8.js, john-9-12.js, john-core.js, luke-13-16.js, luke-17-20.js, luke-21-24.js, luke-5-8.js, luke-9-12.js, luke-core.js, mark-13-16.js, mark-5-8.js, mark-9-12.js, mark-core.js, matthew-complete.js, one-data.js**
- Structural/reference-column issues: **32**

## Matthew 5 correction

`寶訓 | 山上寶訓 · 太 5:1–7:29 | — | 平原寶訓 · 路 6:20–49 | —`

## Audit findings

- static/one/hebrews-complete.js:22: harmony block could not be parsed
- static/one/john-17-20.js:40: harmony block could not be parsed
- static/one/john-17-20.js:89: harmony block could not be parsed
- static/one/john-17-20.js:138: harmony block could not be parsed
- static/one/john-17-20.js:186: harmony block could not be parsed
- static/one/john-21.js:49: harmony block could not be parsed
- static/one/john-core.js:20: 大臣之子得醫治: 約 column cites 太: 約4:43–54（不宜直接等同太8／路7百夫長事件）
- static/one/john-core.js:20: 大臣之子得醫治: 約 column cites 路: 約4:43–54（不宜直接等同太8／路7百夫長事件）
- static/one/john-registry.js:51: harmony block could not be parsed
- static/one/joshua-judges-ruth-complete.js:9: harmony block could not be parsed
- static/one/minor-prophets-complete.js:7: harmony block could not be parsed
- static/one/one-data.js:57: 家譜: 太 column lacks a Gospel ref: 馬太福音 1:1–17
- static/one/one-data.js:57: 家譜: 路 column lacks a Gospel ref: 路加福音 3:23–38
- static/one/one-data.js:57: 降生宣告: 太 column lacks a Gospel ref: 馬太福音 1:18–25
- static/one/one-data.js:57: 降生宣告: 路 column lacks a Gospel ref: 路加福音 1:26–38；2:1–7
- static/one/one-data.js:57: 降生宣告: 約 column lacks a Gospel ref: 約翰福音 1:1–18
- static/one/one-data.js:71: 博士來訪: 太 column lacks a Gospel ref: 馬太福音 2:1–12
- static/one/one-data.js:71: 逃往埃及: 太 column lacks a Gospel ref: 馬太福音 2:13–23
- static/one/one-data.js:71: 逃往埃及: 路 column lacks a Gospel ref: 路加福音 2:39–40（回拿撒勒摘要）
- static/one/one-data.js:85: 約翰傳道: 太 column lacks a Gospel ref: 馬太福音 3:1–12
- static/one/one-data.js:85: 約翰傳道: 可 column lacks a Gospel ref: 馬可福音 1:1–8
- static/one/one-data.js:85: 約翰傳道: 路 column lacks a Gospel ref: 路加福音 3:1–18
- static/one/one-data.js:85: 約翰傳道: 約 column lacks a Gospel ref: 約翰福音 1:19–28
- static/one/one-data.js:85: 耶穌受洗: 太 column lacks a Gospel ref: 馬太福音 3:13–17
- static/one/one-data.js:85: 耶穌受洗: 可 column lacks a Gospel ref: 馬可福音 1:9–11
- static/one/one-data.js:85: 耶穌受洗: 路 column lacks a Gospel ref: 路加福音 3:21–22
- static/one/one-data.js:85: 耶穌受洗: 約 column lacks a Gospel ref: 約翰福音 1:29–34（約翰的見證）
- static/one/ot-history-remainder-complete.js:9: harmony block could not be parsed
- static/one/ot-major-prophets-remainder-complete.js:12: harmony block could not be parsed
- static/one/ot-wisdom-remainder-complete.js:9: harmony block could not be parsed
- static/one/pentateuch-remaining-complete.js:18: harmony block could not be parsed
- static/one/remaining-nt-epistles-complete.js:6: harmony block could not be parsed

## Scope

This automated pass checks every `harmony:` table currently present under `static/one/*.js` for table shape, Gospel-column/reference consistency, valid Gospel chapter bounds, and the sermon-name placement error reported for Matthew 5. Event-level historical/chronological equivalence still requires editorial comparison with the Gospel texts; automation is a guardrail, not a substitute for textual judgment.
