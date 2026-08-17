# ONE — 1,189 Chapter Visual Master Inventory

Status: ACTIVE · SOURCE AUDIT FIRST · NO IMAGE GENERATION DURING AUDIT

ONE's visual production unit is the **chapter**, not the book. The Protestant 66-book canon contains 1,189 chapters (OT 929 + NT 260). Every chapter must ultimately have one canonical artwork identity, one portrait cover composition, one horizontal illustrated-Scripture spread, and one theme verse from that chapter.

## Required chapter record

Each of the 1,189 records must eventually contain:

- book number / code / Chinese + English book name
- chapter number
- `artStatus`: `HISTORICAL` | `GENERATE-ONCE` | `FIXED-GENERATED` | `REVISION-REQUESTED`
- verified Doré / historical artwork title, if a direct chapter illustration exists
- exact Scripture reference depicted by the historical artwork
- source URL / provenance
- source/native aspect ratio (`portrait` | `landscape`)
- canonical ONE asset path (for fixed local assets)
- chapter theme verse reference + approved text
- portrait-cover focal/crop metadata
- horizontal spread layout (`landscape-with-verse` | `portrait-with-verse`)
- Morning Star eligibility (only when compositionally appropriate)
- audit notes

## Non-negotiable audit rule

Do **not** infer that a chapter has Doré art because the same event appears in a parallel Gospel or because an image is thematically similar. Historical status requires a direct, defensible chapter/verse mapping from the source catalog.

If more than one Doré plate maps directly to the same chapter, retain all candidates in the audit metadata, then choose one canonical chapter artwork editorially. Do not throw the other historical plates away; keep them in the source library for possible chapter-body supporting use.

If no verified direct plate maps to a chapter, mark it `GENERATE-ONCE`. Do not generate during this inventory/audit pass.

## Canon structure / chapter totals

### Old Testament — 929 chapters

01 GEN Genesis 創世記 — 50
02 EXO Exodus 出埃及記 — 40
03 LEV Leviticus 利未記 — 27
04 NUM Numbers 民數記 — 36
05 DEU Deuteronomy 申命記 — 34
06 JOS Joshua 約書亞記 — 24
07 JDG Judges 士師記 — 21
08 RUT Ruth 路得記 — 4
09 1SA 1 Samuel 撒母耳記上 — 31
10 2SA 2 Samuel 撒母耳記下 — 24
11 1KI 1 Kings 列王紀上 — 22
12 2KI 2 Kings 列王紀下 — 25
13 1CH 1 Chronicles 歷代志上 — 29
14 2CH 2 Chronicles 歷代志下 — 36
15 EZR Ezra 以斯拉記 — 10
16 NEH Nehemiah 尼希米記 — 13
17 EST Esther 以斯帖記 — 10
18 JOB Job 約伯記 — 42
19 PSA Psalms 詩篇 — 150
20 PRO Proverbs 箴言 — 31
21 ECC Ecclesiastes 傳道書 — 12
22 SNG Song of Songs 雅歌 — 8
23 ISA Isaiah 以賽亞書 — 66
24 JER Jeremiah 耶利米書 — 52
25 LAM Lamentations 耶利米哀歌 — 5
26 EZK Ezekiel 以西結書 — 48
27 DAN Daniel 但以理書 — 12
28 HOS Hosea 何西阿書 — 14
29 JOL Joel 約珥書 — 3
30 AMO Amos 阿摩司書 — 9
31 OBA Obadiah 俄巴底亞書 — 1
32 JON Jonah 約拿書 — 4
33 MIC Micah 彌迦書 — 7
34 NAM Nahum 那鴻書 — 3
35 HAB Habakkuk 哈巴谷書 — 3
36 ZEP Zephaniah 西番雅書 — 3
37 HAG Haggai 哈該書 — 2
38 ZEC Zechariah 撒迦利亞書 — 14
39 MAL Malachi 瑪拉基書 — 4

### New Testament — 260 chapters

40 MAT Matthew 馬太福音 — 28
41 MRK Mark 馬可福音 — 16
42 LUK Luke 路加福音 — 24
43 JHN John 約翰福音 — 21
44 ACT Acts 使徒行傳 — 28
45 ROM Romans 羅馬書 — 16
46 1CO 1 Corinthians 哥林多前書 — 16
47 2CO 2 Corinthians 哥林多後書 — 13
48 GAL Galatians 加拉太書 — 6
49 EPH Ephesians 以弗所書 — 6
50 PHP Philippians 腓立比書 — 4
51 COL Colossians 歌羅西書 — 4
52 1TH 1 Thessalonians 帖撒羅尼迦前書 — 5
53 2TH 2 Thessalonians 帖撒羅尼迦後書 — 3
54 1TI 1 Timothy 提摩太前書 — 6
55 2TI 2 Timothy 提摩太後書 — 4
56 TIT Titus 提多書 — 3
57 PHM Philemon 腓利門書 — 1
58 HEB Hebrews 希伯來書 — 13
59 JAS James 雅各書 — 5
60 1PE 1 Peter 彼得前書 — 5
61 2PE 2 Peter 彼得後書 — 3
62 1JN 1 John 約翰一書 — 5
63 2JN 2 John 約翰二書 — 1
64 3JN 3 John 約翰三書 — 1
65 JUD Jude 猶大書 — 1
66 REV Revelation 啟示錄 — 22

## Historical source baseline

Primary mapping baseline for the Doré audit: chapter/verse-indexed catalogs of Doré's Bible illustrations. The complete Doré corpus is commonly cataloged as 241 Bible plates; source editions can differ in presentation/order, so chapter mapping must be recorded explicitly rather than inferred from filenames.

Audit sequence:

1. Old Testament Doré chapter/verse index.
2. New Testament Doré chapter/verse index.
3. Cross-check ambiguous titles against Wikimedia Commons / a second catalog.
4. Map plates to the 1,189 Protestant-canon chapter records only; deuterocanonical plates stay in the source library but outside this master count.
5. Count unique chapters with >=1 verified direct historical plate.
6. Remaining chapters become `GENERATE-ONCE` only after the audit is complete.

## Production gate

No bulk ONE Studio generation starts until this master audit yields an exact count of:

- unique chapters with direct Doré/historical artwork;
- chapters with multiple direct historical candidates;
- chapters without direct historical artwork;
- OT / NT breakdown;
- per-book breakdown.

After that gate, generation proceeds chapter-by-chapter from `GENERATE-ONCE`, never as an uncontrolled batch.