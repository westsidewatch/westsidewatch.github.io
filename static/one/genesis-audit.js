/* Genesis runtime integrity audit. Fail closed rather than expose a partially broken book. */
(() => {
  "use strict";
  const D=window.ONE_DATA,genesis=D?.genesis,studies=genesis?.chapterStudies;
  const errors=[];
  const requiredText=["title","passage","movement","story","position"];
  const requiredArrays=["route","background","scout","connections","questions","prepare"];

  if(!D)errors.push("ONE_DATA missing");
  if(!genesis)errors.push("genesis missing");
  if(!studies)errors.push("chapterStudies missing");
  if(genesis){
    if(genesis.number!==1)errors.push("book number is not 1");
    if(genesis.code!=="GEN"||genesis.zhCode!=="GEN"||genesis.enCode!=="GEN")errors.push("GEN codes invalid");
    if(!Array.isArray(genesis.chapters)||genesis.chapters.length!==50)errors.push("chapter title array is not 50");
  }

  if(studies){
    for(let number=1;number<=50;number+=1){
      const study=studies[String(number)];
      if(!study){errors.push(`chapter ${number} missing`);continue;}
      requiredText.forEach(key=>{if(typeof study[key]!=="string"||!study[key].trim())errors.push(`chapter ${number} ${key} missing`);});
      requiredArrays.forEach(key=>{if(!Array.isArray(study[key])||study[key].length===0)errors.push(`chapter ${number} ${key} empty`);});
      if(study.map){
        if(!Array.isArray(study.map.places))errors.push(`chapter ${number} map places invalid`);
        if(study.map.routeCount!=null){
          const routes=Array.isArray(study.map.routes)?study.map.routes:[];
          if(routes.length!==study.map.routeCount)errors.push(`chapter ${number} map route count ${routes.length}/${study.map.routeCount}`);
          routes.forEach((route,index)=>{if(!Array.isArray(route)||route.length<3)errors.push(`chapter ${number} map route ${index+1} malformed`);});
        }
      }
    }
  }

  const ok=errors.length===0;
  document.documentElement.dataset.genesisContentAudit=ok?"ok":"failed";
  if(!ok)console.error("[ONE Genesis audit]",errors);
})();