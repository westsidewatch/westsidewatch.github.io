(()=>{"use strict";
const MANIFESTS=[
 "https://iiif.fudan.edu.cn/p/3/3bab87ca-7f9c-4327-812e-4f3076554ba2",
 "https://iiif.fudan.edu.cn/p/3/0c8472b7-dbd1-4fad-b789-21b033b0ff30",
 "https://iiif.fudan.edu.cn/p/3/82482aaa-a1c4-4849-a5b7-9b7b54ef0da1",
 "https://iiif.fudan.edu.cn/p/3/cb1bb75b-3080-47ba-8303-29c5abb06454",
 "https://iiif.fudan.edu.cn/p/3/ce57f5b0-760d-4b22-87c7-fcf832d06a9a",
 "https://iiif.fudan.edu.cn/p/3/035f4550-148b-4104-a3f3-35bb8ec6ff5a",
 "https://iiif.fudan.edu.cn/p/3/92c28c86-9a27-4afe-a0e6-96e94da69df3"
];
const CORPUS={id:"fudan-yincang-iiif-v1",source:"Fudan University Yincang IIIF",sourceUrl:"https://yin.fudan.edu.cn/",policy:"remote-only; no source images stored",manifests:MANIFESTS,stats:null,status:"idle"};
async function refresh(){if(!window.SEAL_IIIF)throw new Error("SEAL_IIIF unavailable");CORPUS.status="loading";const settled=await Promise.allSettled(MANIFESTS.map(url=>window.SEAL_IIIF.inspect(url))),records=settled.filter(x=>x.status==="fulfilled").map(x=>x.value),failed=settled.length-records.length;CORPUS.records=records;CORPUS.stats=window.SEAL_IIIF.summarize(records);CORPUS.stats.requestedManifests=MANIFESTS.length;CORPUS.stats.failedManifests=failed;CORPUS.status=records.length?"ready":"unavailable";window.dispatchEvent(new CustomEvent("seal-corpus-ready",{detail:CORPUS}));return CORPUS}
window.SEAL_CORPUS={...CORPUS,refresh};
})();
