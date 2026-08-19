/* ONE Doré audited exact mapping data.
 * Replaces the old Round-3 semantic expansion table.
 * DATA ONLY: only chapter-event matches survive here; no generic/theme-only reuse.
 */
(() => {
  "use strict";
  const R = window.ONE_DORE_COVER_REGISTRY;
  if (!R) return;
  R.maps = {
    1:"1:001,2:002,3:003,4:004,7:007,8:008,9:009,11:010,12:011,18:012,19:013,21:014,22:016,23:017,24:018,27:020,28:021,29:022,32:024,33:025,37:026,41:027,45:028,46:029",
    9:"6:072,10:073,15:074,17:075,18:076,19:077,20:078,24:079,28:080,31:081",
    10:"2:082,10:083,18:084,19:085,21:086,24:106",
    19:"",
    23:"",
    40:"1:194,2:161,3:184,4:196,5:164,12:165,14:168,17:170,19:187,21:172,22:173,26:174,27:178,28:182",
    41:"1:183,2:185,4:186,5:200,6:167,8:168,9:171,10:187,11:172,12:188,14:190,15:191,16:192",
    42:"1:193,2:194,3:184,4:196,5:223,8:200,9:170,10:201,15:206,16:207,18:208,19:172,22:209,23:177,24:212",
    43:"2:213,4:215,6:216,8:217,11:218,12:172,13:189,18:219,19:222,21:223",
    52:"",
    53:""
  };
  R.version = "2026-08-19-audited-exact-only";
  R.mappingSource = "manual chapter-event audit of Doré 241 originals";
  R.semanticExpansionRemoved = true;
  R.totalCompletedChapters = Object.values(R.maps).reduce((sum,raw)=>sum+(raw?raw.split(',').filter(Boolean).length:0),0);
  document.documentElement.dataset.doreMapping = "audited-exact-only";
})();