# DORÉ Foundation — First Biblical Aramaic Reading

**Course:** Scripture Canon  
**Lesson:** 03 — Textual Witnesses and Original Languages  
**Canonical reference:** Daniel 2:4b  
**Language:** Biblical Aramaic  
**Corpus:** Open Scriptures Hebrew Bible / Westminster Leningrad Codex  
**Pinned upstream:** `openscriptures/morphhb@3d15126fb1ef74867fc1434be1942e837932691f`

## Reading boundary

Daniel 2:4 is a critical language-boundary exercise for Doré: the verse begins in Hebrew narrative and then moves into the Aramaic section of Daniel. Doré must therefore learn that book-level metadata such as an OSIS document's default `xml:lang="he"` cannot be used to flatten every token in the book into Hebrew.

The Aramaic speech begins with the familiar transition:

> אֱדַיִן מַלְּלוּ כַשְׂדָּיֵא לְמַלְכָּא אֲרָמִית

This reading is stored as a language-boundary lesson, not merely as another Semitic string.

## What Doré must learn

- Biblical Aramaic is a distinct language layer and must be represented as `arc`, not silently normalized to `he`.
- A biblical book can contain more than one original language.
- Document-level language metadata is not sufficient for token-level language classification.
- Hebrew and Aramaic share scripts and many cognate forms; visual similarity is not a valid language classifier.
- The explicit textual marker `אֲרָמִית` is itself significant evidence that the following speech is Aramaic, but corpus language boundaries still require structured validation rather than a one-word heuristic.
- Surface text, morphology, lemma and language assignment remain separately provenance-bearing analytical layers.

## Research restraint

Doré is not yet asked to derive theology from the language shift or to settle every scholarly question about the extent, literary function, dating, or compositional history of Daniel's Aramaic sections. Those belong to later Biblical Worlds, textual criticism, historical, and interpretive courses.

At this stage the task is simpler and stricter:

> **Recognize the language change and do not erase it.**

## Provenance

The pinned OSHB Daniel source identifies the same OSHB/WLC foundation used for the Hebrew corpus and declares `Bible.MT` as its reference system. Because the file-level OSIS language is Hebrew, this lesson also records a design requirement: Doré's ingestion pipeline must derive or validate token/passage-level Biblical Aramaic language metadata rather than inherit the document default blindly.

## Status

`BIBLICAL_ARAMAIC_READING_STARTED`

With this reading, Doré has now begun direct foundation reading in all three biblical original-language categories used by the Protestant 66-book canon:

- Biblical Hebrew
- Biblical Aramaic
- Koine/Biblical Greek

Lesson 03 remains in progress until corpus ingestion and provenance tests pass.
