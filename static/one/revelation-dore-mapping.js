/* Revelation Doré canonical mapping — P1 ORIGINAL_LOCKED only.
 * DATA ONLY. This file never writes study.illustration; ONE_COVER_POLICY remains the sole runtime writer.
 * Verified against Wikimedia Commons Doré's Bible Illustrations gallery:
 * Rev 1:9 -> 236 John at Patmos
 * Rev 6:7-8 -> 237 The Vision of Death
 * Rev 12:1-3 -> 238 The Crowned Virgin: A Vision of John
 * Rev 18:2 -> 239 Babylon Fallen
 * Rev 20:12 -> 240 The Last Judgment
 * Rev 21:1-2 -> 241 The New Jerusalem
 */
(() => {
  "use strict";
  const R = window.ONE_DORE_COVER_REGISTRY;
  if (!R) return;

  R.titles = R.titles || {};
  R.titles[236] = "John at Patmos";
  R.titles[237] = R.titles[237] || "The Vision of Death";
  R.titles[238] = "The Crowned Virgin: A Vision of John";
  R.titles[239] = "Babylon Fallen";
  R.titles[240] = R.titles[240] || "The Last Judgment";
  R.titles[241] = R.titles[241] || "The New Jerusalem";

  R.maps = R.maps || {};
  R.maps[66] = "1:236,6:237,12:238,18:239,20:240,21:241";

  R.revelationOriginalLocked = Object.freeze({
    1:236,
    6:237,
    12:238,
    18:239,
    20:240,
    21:241
  });
  R.revelationMappingBasis = "P1_ORIGINAL_LOCKED_WIKIMEDIA_DORE_GALLERY";
  R.revelationMappedChapters = 6;
  R.revelationUnmappedChapters = 16;
  document.documentElement.dataset.revelationDore = "6-original-locked";
})();