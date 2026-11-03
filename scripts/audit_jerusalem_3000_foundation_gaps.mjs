import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {dirname,resolve} from 'node:path';
import {createHash} from 'node:crypto';
import {buildFoundationGapAudit,renderFoundationGapMarkdown} from './lib/jerusalem-foundation-gap-audit.mjs';
const args=process.argv.slice(2),options={};for(let i=0;i<args.length;i+=2){if(!['--report','--render-commit','--out','--overview-report','--enclosure-report','--transition-report'].includes(args[i])||!args[i+1])throw new Error('Use --report PATH --render-commit SHA --out PREFIX');options[args[i]]=args[i+1];}
for(const key of ['--report','--render-commit','--out'])if(!options[key])throw new Error(`Missing ${key}`);
const root=new URL('../preview/jerusalem-3000/',import.meta.url),[planRaw,timelineRaw,reportRaw]=await Promise.all([readFile(new URL('data/city-foundation-plan.v1.json',root),'utf8'),readFile(new URL('data/continuous-build-timeline.json',root),'utf8'),readFile(options['--report'],'utf8')]);
const sha=raw=>createHash('sha256').update(raw).digest('hex');
const qualityArgs=['--overview-report','--enclosure-report','--transition-report'];let qualityReports=null,qualityReportSha256={};if(qualityArgs.some(k=>options[k])){if(!qualityArgs.every(k=>options[k]))throw new Error('Provide all3 quality reports together');qualityReports={};for(const [i,k]of qualityArgs.entries()){const raw=await readFile(options[k],'utf8'),name=['overview','enclosure','transition'][i];qualityReports[name]=JSON.parse(raw);qualityReportSha256[name]=sha(raw);}}
const audit=buildFoundationGapAudit({plan:JSON.parse(planRaw),timeline:JSON.parse(timelineRaw),report:JSON.parse(reportRaw),qualityReports,provenance:{qualityReportSha256,renderBaselineCommit:options['--render-commit'],baselinePolicy:'caller-declared render revision; input-byte hashes recorded; no automatic freshness certification',reportSha256:sha(reportRaw),planSha256:sha(planRaw)}});
const prefix=resolve(options['--out']);await mkdir(dirname(prefix),{recursive:true});await writeFile(prefix+'.json',JSON.stringify(audit,null,2)+'\n');await writeFile(prefix+'.md',renderFoundationGapMarkdown(audit));
console.log(JSON.stringify({phases:audit.phases.length,transitions:audit.transitions.length,nextPackage:audit.nextPackage,historicalFoundationAccepted:audit.historicalFoundationAccepted,output:prefix}));
