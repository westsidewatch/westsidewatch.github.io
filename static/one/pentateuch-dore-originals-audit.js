/* ONE Pentateuch Doré original audit correction.
 * Runs after pentateuch-remaining-complete.js and the canonical Doré registry,
 * and before ONE_COVER_POLICY resolves covers.
 * Source authority is the canonical 241-file inventory, not the sparse display-title table.
 *
 * RUNTIME CONTRACT: this audit never loads other scripts. Geography and final cover sync
 * are explicit entries in the canonical index load order.
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

  apply(2,
    {2:31,5:32,9:33,10:34,12:36,14:37,17:38,19:39,32:41},
    [30,31,32,33,34,35,36,37,38,39,40,41],
    {2:[30],12:[35],32:[40]}
  );
  apply(4,{13:42,16:43,21:44,22:45},[42,43,44,45]);
  apply(3,{},[]);
  apply(5,{},[]);

  window.ONE_PENTATEUCH_DORE_AUDIT_READY=true;
  document.documentElement.dataset.pentateuchDoreAudit="241-file-inventory-complete";
})();
