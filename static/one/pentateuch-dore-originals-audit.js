/* ONE Pentateuch Doré original audit correction.
 * Runs after pentateuch-remaining-complete.js and before ONE_COVER_POLICY resolves covers.
 * Source authority is the canonical 241-file inventory, not the sparse display-title table.
 */
(() => {
  "use strict";
  const D=window.ONE_DATA;
  const R=window.ONE_DORE_COVER_REGISTRY;
  if(!D?.studyBooks)return;

  const apply=(bookNumber,mapping,inventory,alternates={})=>{
    const book=D.studyBooks[bookNumber];
    if(!book)return;
    book.canonicalDoreMapping={...mapping};
    /* Publish the audited mapping into the central registry immediately as well.
     * This removes any dependency on later studyBooks lookups or render timing.
     */
    if(R){R.maps=R.maps||{};R.maps[bookNumber]={...mapping};}
    book.doreAudit={
      ...(book.doreAudit||{}),
      status:"AUDITED_241_FILE_INVENTORY_ORIGINALS_FIRST",
      exactChapters:Object.keys(mapping).map(Number),
      originalInventory:inventory.slice(),
      alternateOriginals:{...alternates},
      missingPlateChapters:(book.chapters||[]).map((_,i)=>i+1).filter(n=>!mapping[n]),
      generatedNow:false
    };
  };

  /* Exodus originals in the canonical 241 inventory:
   * 030 Child Moses on the Nile; 031 Finding of Moses;
   * 032 Moses and Aaron before Pharaoh; 033 Fifth Plague;
   * 034 Ninth Plague; 035 Firstborn slain; 036 Egyptians ask Moses to depart;
   * 037 Egyptians drown in the sea; 038 Moses strikes Horeb;
   * 039 Giving of the Law; 040 Moses comes down Sinai; 041 Moses breaks the tablets.
   */
  apply(2,
    {2:31,5:32,9:33,10:34,12:36,14:37,17:38,19:39,32:41},
    [30,31,32,33,34,35,36,37,38,39,40,41],
    {2:[30],12:[35],32:[40]}
  );

  /* Numbers originals: 042 spies return; 043 Korah/Dathan/Abiram;
   * 044 bronze serpent; 045 angel appears to Balaam.
   */
  apply(4,
    {13:42,16:43,21:44,22:45},
    [42,43,44,45]
  );

  /* No chapter-specific Doré original in the canonical 241 inventory is assigned
   * to Leviticus or Deuteronomy. They remain genuine Missing Plate books for now.
   */
  apply(3,{},[]);
  apply(5,{},[]);

  window.ONE_PENTATEUCH_DORE_AUDIT_READY=true;
  document.documentElement.dataset.pentateuchDoreAudit="241-file-inventory-complete";
})();

/* Geography correction belongs to the same preflight lane: load the actual Holy Light
 * source maps before ONE renders chapter modules. */
if(!window.ONE_PENTATEUCH_REAL_MAPS_READY&&document.readyState==="loading"){
  document.write('<script src="./pentateuch-real-maps.js?v=20260818c"><\/script>');
}

/* Final cover synchronization is deliberately last. It re-applies the audited
 * mappings after the canonical policy/app have initialized, eliminating the race
 * that left valid Doré originals absent from visible Pentateuch covers. */
if(!window.ONE_PENTATEUCH_COVER_SYNC_LOADING&&document.readyState==="loading"){
  window.ONE_PENTATEUCH_COVER_SYNC_LOADING=true;
  document.write('<script src="./pentateuch-cover-runtime-sync.js?v=20260818d"><\/script>');
}
