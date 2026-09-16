import fs from 'node:fs';

const evidence=JSON.parse(fs.readFileSync('static/dore-design/italian-editorial-evidence.v1.json','utf8'));
const grammars=JSON.parse(fs.readFileSync('static/dore-design/italian-editorial-grammars.v1.json','utf8'));

const SEED_IDS=['cg-1933-cover-12','cg-1933-cover-01-wrapper','cg-1933-p6-insert'];
const GAME_POTENTIAL={
  'cg-1933-cover-12':['block-composition','recomposition','visual-balance-under-mutation'],
  'cg-1933-cover-01-wrapper':['fold','2d-to-3d','world-state-transition'],
  'cg-1933-p6-insert':['collision','foreign-local-persistence','reveal-without-dissolution']
};

function eraGrammar(item){
  for(const family of grammars.families||[]){
    const era=(family.eras||[]).find(x=>x.id===item.era);
    if(era) return era;
  }
  return null;
}

export function buildItalianSeedProjection(){
  return SEED_IDS.map(id=>{
    const item=(evidence.items||[]).find(x=>x.id===id);
    if(!item) throw new Error(`missing evidence ${id}`);
    const era=eraGrammar(item);
    if(!era) throw new Error(`missing grammar era ${item.era}`);
    const grammarTokens=new Set(Object.values(era.grammar||{}).flat());
    const supportedTokens=(item.tokens||[]).filter(token=>grammarTokens.has(token));
    if(!supportedTokens.length) throw new Error(`no grammar support for ${id}`);
    return {
      evidenceId:item.id,
      family:item.family,
      era:item.era,
      authority:item.authority,
      researchState:'DECOMPOSED',
      modules:[...item.modules],
      supportedGrammarTokens,
      gamePotential:[...(GAME_POTENTIAL[id]||[])],
      benchmarkTarget:'benchmark.sheep-enters-world.v0',
      provenance:{evidenceRegistry:'static/dore-design/italian-editorial-evidence.v1.json',grammarRegistry:'static/dore-design/italian-editorial-grammars.v1.json'},
      authorityBoundary:{historicalEvidence:true,gameGrammarAuthority:false,productionAuthority:false,canonicalArtDirection:false}
    };
  });
}

if(import.meta.url===`file://${process.argv[1]}`) console.log(JSON.stringify(buildItalianSeedProjection(),null,2));
