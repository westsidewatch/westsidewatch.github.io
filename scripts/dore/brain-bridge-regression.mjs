import fs from 'node:fs';

const brain = JSON.parse(fs.readFileSync('static/dore/brain/knowledge-index.json','utf8'));
const norm=s=>String(s??'').toLowerCase().normalize('NFKC').replace(/[\s.,;:!?，。；：！？「」『』()（）\-–—_'"`]/g,'');
function scoreNode(node,q){const nq=norm(q);if(!nq)return 0;let best=0;for(const v of node.questions||[]){const nv=norm(v);if(nv===nq)return 100;if((nv&&nq.includes(nv))||nv.includes(nq))best=Math.max(best,82)}let conceptHits=0;for(const c of node.concepts||[]){const nc=norm(c);if(nc&&nq.includes(nc))conceptHits++}if(conceptHits>=2)best=Math.max(best,72+Math.min(12,conceptHits*3));else if(conceptHits===1)best=Math.max(best,46);return best}
function choose(q){let best=null,bestScore=0;for(const node of brain.nodes||[]){const s=scoreNode(node,q);if(s>bestScore){best=node;bestScore=s}}return bestScore>=70?{node:best,score:bestScore}:null}
const cases=[
  ['馬利亞有幾位？','research.nt.mary-count'],
  ['馬利亞有幾位?','research.nt.mary-count'],
  ['新約有多少位馬利亞','research.nt.mary-count'],
];
let failed=0;
for(const [q,id] of cases){const hit=choose(q);const ok=hit?.node?.id===id;console.log(JSON.stringify({q,expected:id,actual:hit?.node?.id??null,score:hit?.score??0,ok}));if(!ok)failed++;}
const scriptureProbe='約翰福音 3:16';
const scriptureLike=/[創创出利民申書书士得撒王代拉尼斯伯詩诗箴傳传歌賽赛耶哀結结但何珥摩俄拿彌弥鴻鸿哈番該该亞亚瑪玛太可路約约徒羅罗林加弗腓西帖提前後后多門门來来雅彼約约猶犹啟启]\S{0,6}\s*\d+/u.test(scriptureProbe)||/\d+\s*[:：]\s*\d+/.test(scriptureProbe);
console.log(JSON.stringify({scriptureProbe,scriptureLike,ok:scriptureLike}));
if(!scriptureLike) failed++;
process.exitCode=failed?1:0;
