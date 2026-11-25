// One display/admission inventory for all owners. This is not a lifecycle ledger.
const IRON='https://hadashot.iaa.org.il/Report_Detail_eng.aspx?id=25841&mag_id=128&print=all';
const UPPER='https://www.gov.il/en/pages/jerusalem-the-upper-city-during-the-second-temple-period';
const BYZ='https://hadashot.iaa.org.il/Report_Detail_Eng.aspx?id=25729';
const VAULT='https://hadashot.iaa.org.il/Report_Detail_Eng.aspx?id=25547&mag_id=127';
const MODERN='https://www.imj.org.il/en/exhibitions/live-jerusalem';
const sourceLimits={
 [IRON]:'Area U eighth–sixth-century BCE buildings; not tenth-century proof, roof reconstruction, or citywide house locations',
 [UPPER]:'excavated elite Upper City examples, not the architecture of every household',
 [BYZ]:'possible extramural Byzantine domestic unit and separate 1895 consular complex; not a citywide roof or residential template',
 [VAULT]:'cross-vaulted rooms in a building with an Ottoman industrial phase; not evidence for exposed domes over every house',
 [MODERN]:'museum exhibition covering diverse late Ottoman to modern residences; no admitted building plans',
};
const rows=[
 ['chalcolithic-early-bronze','早期單室聚落',['single-room'],'early-settlement-analogy'],
 ['middle-bronze','中青銅單室住宅示意',['single-room'],'early-settlement-analogy'],
 ['late-bronze-iron1','晚青銅／早鐵器住宅示意',['single-room'],'early-settlement-analogy'],
 ['david-solomon','四室住宅的較晚形制類比',['four-room-analogy'],'later-analogy-not-tenth-century-proof',null,[IRON]],
 ['late-first-temple','鐵器時代四室住宅類比',['four-room-analogy'],'excavated-plan-analogy-not-located-houses',null,[IRON]],
 ['babylonian-destruction','第一聖殿住宅的毀壞投影',['four-room-analogy'],'same-model-destruction-projection','late-first-temple',[IRON]],
 ['persian-nehemiah','波斯期開放院落假說',['open-court'],'design-analogy-unverified'],
 ['hellenistic-hasmonean','希臘化期院落住宅暫模',['courtyard'],'independent-typology-pending'],
 ['herodian-jesus','第二聖殿期院落住宅類比',['courtyard'],'elite-examples-not-all-households',null,[UPPER]],
 ['roman-destruction','希律住宅的毀壞投影',['courtyard'],'same-model-destruction-projection','herodian-jesus',[UPPER]],
 ['aelia','羅馬期街區暫模',['courtyard'],'independent-typology-pending'],
 ['byzantine','拜占庭期街區暫模',['courtyard'],'independent-typology-pending',null,[BYZ]],
 ['early-islamic','早期伊斯蘭街區暫模',['courtyard'],'independent-typology-pending'],
 ['crusader','十字軍期街區暫模',['courtyard'],'independent-typology-pending'],
 ['ayyubid-mamluk','阿尤布／馬穆魯克街區暫模',['courtyard'],'independent-typology-pending'],
 ['ottoman','奧斯曼舊城院落暫模',['courtyard'],'independent-typology-pending',null,[VAULT]],
 ['outside-walls','舊城與城外擴展的混合暫模',['courtyard'],'old-city-and-extension-typologies-pending','ottoman',[BYZ,MODERN]],
 ['modern','歷史舊城與現代街區的混合暫模',['courtyard'],'old-city-and-extension-typologies-pending','ottoman',[MODERN]],
];
export const RESIDENTIAL_ERA_PROFILES=Object.freeze(Object.fromEntries(rows.map(([phase,label,planForms,authority,modelPredecessor=null,sources=[]])=>[phase,Object.freeze({phase,label,planForms:Object.freeze(planForms),authority,modelPredecessor,sources:Object.freeze(sources),sourceLimitations:Object.freeze(sources.map(url=>sourceLimits[url])),historicalGeometryAccepted:false,wholeCityTypologyVerified:false})])));
export function residentialEraProfile(phase){
 const profile=RESIDENTIAL_ERA_PROFILES[phase];
 if(!profile)throw new Error(`Missing residential era profile: ${phase}`);
 return {...profile,planForms:[...profile.planForms],sources:[...profile.sources],sourceLimitations:[...profile.sourceLimitations]};
}
export function overviewPlanForArchitecture(profile){
 if(profile?.id==='iron-age-four-room-analogy')return 'four-room-analogy';
 if(profile?.id==='persian-courtyard-analogy')return 'open-court';
 return 'courtyard';
}
