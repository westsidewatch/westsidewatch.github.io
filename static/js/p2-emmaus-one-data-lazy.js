/* P2 / 03 — lazy, read-only reuse of the ORIGINAL ONE chapter registries.
 * Load only the selected volume family, never all 1,189 chapters at entrance.
 * This source belongs to the P2 draft; original /one/ modules are not altered.
 */
(()=>{'use strict';
 const root=document.getElementById('emmaus'),D=window.ONE_DATA;if(!root||D?.books?.length!==66)return;
 const g=(...paths)=>paths,repeat=(prefix,parts)=>parts.map(p=>prefix+p+'.js');
 const registrations={
  genesis:g('genesis-core.js',...repeat('genesis-',['5-8','9-12','13-16','17-20','21-24','25-28','29-32','33-36','37-40','41-44','45-48','49-50']),'genesis-registry.js','genesis-postfix.js'),
  pentateuch:g('pentateuch-remaining-complete.js'),
  joshua:g('joshua-judges-ruth-complete.js'),
  samuel:g('samuel-core.js',...repeat('samuel-chapters-',['01-06','07-12','13-18','19-24','25-31']),'samuel-registry.js'),
  samuel2:g('samuel2-core.js',...repeat('samuel2-chapters-',['01-06','07-12','13-18','19-24']),'samuel2-registry.js'),
  history:g('ot-history-remainder-complete.js'),
  wisdom:g('ot-wisdom-remainder-complete.js'),
  psalms:g('psalms-core.js',...repeat('psalms-',['5-12','13-18','19-25','26-50','51-75','76-100','101-125','126-150']),'psalms-registry.js'),
  isaiah:g('isaiah-complete.js','isaiah-context.js','isaiah-maps.js','isaiah-connections-extra.js','isaiah-registry.js'),
  major:g('ot-major-prophets-remainder-complete.js'),
  minor:g('minor-prophets-complete.js'),
  matthew:g('matthew-complete.js'),
  mark:g('mark-core.js','mark-5-8.js','mark-9-12.js','mark-13-16.js'),
  luke:g('luke-core.js','luke-5-8.js','luke-9-12.js','luke-13-16.js','luke-17-20.js','luke-21-24.js','luke-registry.js'),
  john:g('john-core.js','john-5-8.js','john-9-12.js','john-13-16.js','john-17-20.js','john-21.js','john-registry.js'),
  acts:g('acts-complete.js'),
  epistles:g('remaining-nt-epistles-complete.js'),
  hebrews:g('hebrews-complete.js'),
  revelation:g('revelation-complete.js')
 };
 const group=n=>n===1?'genesis':n<=5?'pentateuch':n<=8?'joshua':
  n===9?'samuel':n===10?'samuel2':n<=17?'history':n===19?'psalms':
  n<=22?'wisdom':n===23?'isaiah':n<=27?'major':n<=39?'minor':
  n===40?'matthew':n===41?'mark':n===42?'luke':n===43?'john':
  n===44?'acts':n===58?'hebrews':n===66?'revelation':'epistles';
 const loaded=new Map();
 const fetchScript=file=>new Promise((resolve,reject)=>{
  const element=document.createElement('script');element.src='/one/'+file;element.async=false;
  element.onload=resolve;element.onerror=()=>reject(new Error('ONE chapter module unavailable: '+file));
  document.head.append(element);
 });
 const selected=()=>({n:Number(root.dataset.selectedBook)||42,ch:Number(root.dataset.selectedChapter)||24});
 const record=(n,ch)=>{
  const source=n===42?D.luke:n===40?D.matthew:D.studyBooks?.[n];
  return source?.chapterStudies?.[String(ch)]||null;
 };
 function request(n,ch){
  if(!Number.isInteger(n)||n<1||n>66)return;
  if(record(n,ch))return;
  const id=group(n),paths=registrations[id];if(!paths)return;
  if(!loaded.has(id)){
   loaded.set(id,(async()=>{
    for(const file of paths)await fetchScript(file);
    // ONE index.html registers Mark 41 with this small inline compatibility
    // mapping. Mirror the same published mapping here, without editing ONE.
    if(id==='mark'&&D.mark){
     D.mark.number=41;D.mark.code='MRK';D.mark.name='馬可福音';D.mark.nameEn='Mark';
     D.studyBooks={...(D.studyBooks||{}),41:D.mark};
    }
    return true;
   })().catch(error=>{console.warn('[P2 ONE]',error);loaded.delete(id);return false}));
  }
  void loaded.get(id).then(success=>{
   if(!success||!record(n,ch))return;
   const now=selected();if(now.n!==n||now.ch!==ch)return;
   // Update the original in-folio ONE panels, not an invented parallel copy.
   window.P2EmmausSelect?.(n,ch);
   window.P2EmmausONE?.refresh?.();
  });
 }
 root.addEventListener('p2:one-selection',event=>{
  request(Number(event.detail?.book),Number(event.detail?.chapter));
 });
 const first=selected();request(first.n,first.ch);
})();
