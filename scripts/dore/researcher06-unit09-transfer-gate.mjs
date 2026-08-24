import fs from 'node:fs';
import {encodeMandarinV2,encodeEnglishControl,PHONETIC_ENCODER_V2} from './phonetic-encoders-v2.mjs';

const fixturePath=process.argv[2]||'dore-core/knowledge/researcher/fixtures/noise-retrieval-unit09-dev.json';
const outputPath=process.argv[3]||'dore-core/knowledge/researcher/evidence/researcher06-unit09-dev-gate.json';
const data=JSON.parse(fs.readFileSync(fixturePath,'utf8'));

const normalize=s=>String(s??'').normalize('NFKC').toLowerCase().replace(/[\p{P}\p{S}\s]+/gu,'');
const mkEvidence=f=>{
  const observed=String(f.observed??'');
  const candidate=f.candidate==null?null:String(f.candidate);
  const channels=[];
  if(candidate){
    const on=normalize(observed),cn=normalize(candidate);
    if(on===cn) channels.push({channel:'surface',relation:'normalized_exact'});
    else if(on&&cn&&(cn.includes(on)||on.includes(cn))) channels.push({channel:'surface',relation:'containment'});
    const op=encodeMandarinV2(observed),cp=encodeMandarinV2(candidate);
    if(op.key&&cp.key&&op.key===cp.key) channels.push({channel:'mandarin_phonetic',relation:'exact',encoder:op.version});
    const oe=encodeEnglishControl(observed),ce=encodeEnglishControl(candidate);
    if(oe.key&&ce.key&&oe.key===ce.key) channels.push({channel:'english_phonetic',relation:'exact',encoder:oe.version});
  }
  if(f.anchor) channels.push({channel:'fixture_canonical_anchor',relation:'declared_development_target'});
  return {observed,candidate,source:f.anchor??null,canonical_anchor:f.anchor??null,evidence_channels:channels,score_boundary:{calibrated_probability:false,note:'Unit 09 dev contract gate; no probability claim.'},decision:f.decision};
};

const adaptSearch=r=>({observed:r.observed,candidate:r.candidate,canonical_anchor:r.canonical_anchor,evidence_channels:r.evidence_channels,score_boundary:r.score_boundary,decision:r.decision});
const adaptSubtitle=r=>({observed:r.observed,candidate:r.candidate,canonical_anchor:r.canonical_anchor,evidence_channels:r.evidence_channels,score_boundary:r.score_boundary,decision:r.decision,mutation:r.decision==='suggest'?'proposal_only':'none',silent_overwrite:false});

const results=data.fixtures.map(f=>{
  const generic=mkEvidence(f),search=adaptSearch(generic),subtitle=adaptSubtitle(generic);
  const provenance=generic.observed===search.observed&&generic.observed===subtitle.observed&&generic.canonical_anchor===search.canonical_anchor&&generic.canonical_anchor===subtitle.canonical_anchor;
  const safeAmbiguity=f.family!=='ambiguous'||generic.decision!=='suggest';
  const negativeSafe=f.family!=='ordinary_negative'||(generic.decision==='abstain'&&generic.candidate===null);
  const noSilentOverwrite=subtitle.silent_overwrite===false;
  return {id:f.id,family:f.family,generic,search_adapter:search,subtitle_adapter:subtitle,checks:{provenance,safe_ambiguity:safeAmbiguity,negative_abstention:negativeSafe,no_silent_overwrite:noSilentOverwrite},pass:provenance&&safeAmbiguity&&negativeSafe&&noSilentOverwrite};
});
const summary={partition:data.partition,encoder:PHONETIC_ENCODER_V2,total:results.length,passed:results.filter(x=>x.pass).length,failed:results.filter(x=>!x.pass).length,ordinary_negative_abstention:results.filter(x=>x.family==='ordinary_negative').every(x=>x.generic.decision==='abstain'),ambiguous_not_forced:results.filter(x=>x.family==='ambiguous').every(x=>x.generic.decision!=='suggest'),shared_generic_object:true,subtitle_silent_overwrite:false,pass:results.every(x=>x.pass)};
fs.mkdirSync(outputPath.split('/').slice(0,-1).join('/'),{recursive:true});
fs.writeFileSync(outputPath,JSON.stringify({generated_at:new Date().toISOString(),summary,results},null,2)+'\n');
console.log(JSON.stringify(summary,null,2));
if(!summary.pass)process.exitCode=1;
