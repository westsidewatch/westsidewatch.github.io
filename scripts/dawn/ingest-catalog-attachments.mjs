#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

// Universal catalog attachment normalizer for Dawn Chinese acquisition.
// Accepts pre-fetched CSV/TSV/JSON/JSONL and spreadsheet rows exported to CSV.
// Binary XLS/XLSX/PDF acquisition remains provider/fetch-layer responsibility;
// this script deliberately does not infer rights from file availability.

const args=process.argv.slice(2);
const get=(name,fallback=null)=>{const i=args.indexOf(name);return i>=0?args[i+1]:fallback};
const input=get('--input');
const pool=get('--pool','catalog-import');
const provider=get('--provider','unknown');
const providerBase=get('--provider-base',null);
if(!input) throw new Error('usage: node ingest-catalog-attachments.mjs --input <file> --pool <id> --provider <name> [--provider-base <url>]');

const ext=path.extname(input).toLowerCase();
const text=fs.readFileSync(input,'utf8');
const splitDelimited=(line,sep)=>{let out=[],cur='',q=false;for(let i=0;i<line.length;i++){const ch=line[i];if(ch==='"'){if(q&&line[i+1]==='"'){cur+='"';i++}else q=!q}else if(ch===sep&&!q){out.push(cur);cur=''}else cur+=ch}out.push(cur);return out.map(x=>x.trim())};
const parseDelimited=(txt,sep)=>{const lines=txt.replace(/^\uFEFF/,'').split(/\r?\n/).filter(x=>x.trim());if(!lines.length)return[];const head=splitDelimited(lines[0],sep).map(x=>x.toLowerCase());return lines.slice(1).map(line=>{const vals=splitDelimited(line,sep),o={};head.forEach((h,i)=>o[h]=vals[i]??'');return o})};
let rows;
if(ext==='.jsonl') rows=text.split(/\r?\n/).filter(Boolean).map(JSON.parse);
else if(ext==='.json'){const j=JSON.parse(text);rows=Array.isArray(j)?j:(j.rows||j.items||j.candidates||[])}
else if(ext==='.csv') rows=parseDelimited(text,',');
else if(ext==='.tsv'||ext==='.txt') rows=parseDelimited(text,'\t');
else throw new Error(`unsupported normalized catalog format: ${ext}; convert XLS/XLSX/PDF to CSV/TSV first`);

const pick=(r,names)=>{for(const n of names){if(r[n]!=null&&String(r[n]).trim())return String(r[n]).trim()}return''};
const candidates=[];
for(const r of rows){
 const title=pick(r,['title','書名','题名','題名','name','名稱','名称']);if(!title)continue;
 const author=pick(r,['author','creator','作者','著者','編者','编者']);
 const year=pick(r,['year','date','出版年','年代','publication year']);
 const providerId=pick(r,['id','identifier','call number','callnumber','索書號','索书号','record id']);
 const url=pick(r,['url','link','uri','網址','链接','連結']);
 const type=pick(r,['type','format','resource type','資料類型','资源类型'])||'text';
 candidates.push({sourcePool:pool,provider,title,author:author||null,year:year||null,language:'zh',resourceType:type,providerId:providerId||null,providerUrl:url||(providerBase&&providerId?`${providerBase}${providerId}`:null),rightsStatus:'unknown',admissionAuthority:false,rehost:false});
}
const outDir=path.join(process.cwd(),'static/dawn-library/acquisition/chinese');fs.mkdirSync(outDir,{recursive:true});
const safe=pool.replace(/[^a-z0-9._-]+/gi,'-').toLowerCase();const out=path.join(outDir,`${safe}.json`);
fs.writeFileSync(out,JSON.stringify({schema:'dawn.chinese-acquisition.candidates.v1',sourcePool:pool,provider,generatedAt:new Date().toISOString(),candidateCount:candidates.length,candidates},null,2)+'\n');
console.log(JSON.stringify({input,pool,provider,candidateCount:candidates.length,output:out},null,2));
