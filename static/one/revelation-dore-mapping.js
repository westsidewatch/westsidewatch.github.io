/* Revelation + Acts Doré canonical mapping — P1 ORIGINAL_LOCKED only.
 * DATA ONLY. This file never writes study.illustration; ONE_COVER_POLICY remains the sole runtime writer.
 * Verified against Wikimedia Commons Doré's Bible Illustrations gallery.
 */
(() => {
  "use strict";
  const R = window.ONE_DORE_COVER_REGISTRY;
  if (!R) return;

  R.titles = R.titles || {};
  R.titles[224] = "The Descent of the Spirit";
  R.titles[225] = "The Apostles Preaching the Gospel";
  R.titles[226] = "St. Peter and St. John at the Beautiful Gate";
  R.titles[227] = "The Death of Ananias";
  R.titles[228] = "The Death of Stephen";
  R.titles[229] = "The Conversion of Saul";
  R.titles[230] = "St. Peter at the House of Cornelius";
  R.titles[231] = "St. Peter Delivered from Prison";
  R.titles[232] = "St. Paul at Ephesus";
  R.titles[233] = "St. Paul Rescued from the Multitude";
  R.titles[234] = "St. Paul Shipwrecked";
  R.titles[236] = "John at Patmos";
  R.titles[237] = R.titles[237] || "The Vision of Death";
  R.titles[238] = "The Crowned Virgin: A Vision of John";
  R.titles[239] = "Babylon Fallen";
  R.titles[240] = R.titles[240] || "The Last Judgment";
  R.titles[241] = R.titles[241] || "The New Jerusalem";

  R.maps = R.maps || {};
  // Acts has two canonical Doré plates for chapter 2 (224 and 225). The cover uses
  // 224, the scene closest to the chapter's opening event; 225 remains in the immutable library.
  R.maps[44] = "2:224,3:226,5:227,7:228,9:229,10:230,12:231,19:232,21:233,27:234";
  R.maps[66] = "1:236,6:237,12:238,18:239,20:240,21:241";

  R.actsOriginalLocked = Object.freeze({
    2:224, 3:226, 5:227, 7:228, 9:229, 10:230, 12:231, 19:232, 21:233, 27:234
  });
  R.actsAdditionalOriginals = Object.freeze({2:Object.freeze([225])});
  R.actsMappingBasis = "P1_ORIGINAL_LOCKED_WIKIMEDIA_DORE_GALLERY";
  R.actsMappedChapters = 10;
  R.actsCanonicalOriginalPlates = 11;
  R.actsUnmappedChapters = 18;

  R.revelationOriginalLocked = Object.freeze({
    1:236, 6:237, 12:238, 18:239, 20:240, 21:241
  });
  R.revelationMappingBasis = "P1_ORIGINAL_LOCKED_WIKIMEDIA_DORE_GALLERY";
  R.revelationMappedChapters = 6;
  R.revelationUnmappedChapters = 16;

  document.documentElement.dataset.actsDore = "10-chapters-11-originals-locked";
  document.documentElement.dataset.revelationDore = "6-original-locked";
})();