import { chromium } from 'playwright';
import assert from 'node:assert/strict';
const browser=await chromium.launch({headless:true});
const page=await browser.newPage();
await page.goto('http://127.0.0.1:8000/static/multiwrite/');
const result=await page.evaluate(async()=>{
  const {buildPublicationArtifacts}=await import('/static/multiwrite/book-artifact-build.mjs');
  const {materializePublicationArtifacts}=await import('/static/multiwrite/book-artifact-materializer.mjs');
  const {admitSourceUses}=await import('/static/multiwrite/source-capability-admission.mjs');
  const {runPublishingAutopilot}=await import('/static/multiwrite/book-publishing-autopilot.mjs');
  const {publicationProjection}=await import('/static/multiwrite/book-model.mjs');
  const envelope=(overrides={})=>({
    ok:true,
    status:'completed',
    schema:'dore.source-capability-envelope.v1',
    sourcePointer:'https://example.org/source',
    authority:{sourceIsAuthority:true,identityClaimOnly:true,canonicalIdentityAuthority:false,envelopeAuthority:false},
    access:{modes:['static-http'],preferred:'static-http'},
    media:['text'],
    operations:['cite','read','extract'],
    rights:{rehost:false,decision:'not-inferred-by-envelope',claims:{rehost:true},requiresRightsAdmissionFor:['rehost','redistribute']},
    runtimeBoundary:{required:false,mode:'static-http'},
    editorialBoundary:{canonRequiredFor:['publish','material-transform','rehost'],sourceContentMayBeRewrittenSilently:false},
    surfaceHints:['dawn','multiwrite'],
    provenance:{probeSchema:'dore.source-probe.v0',probeStatus:'completed'},
    persistence:'request-scoped-none',
    ...overrides
  });
  const admitted=admitSourceUses([{id:'static-source',use:'extract',envelope:envelope()}]);
  const rightsBlocked=admitSourceUses([{id:'rights-source',use:'rehost',envelope:envelope()}]);
  const rightsAdmitted=admitSourceUses([{id:'rights-source',use:'rehost',envelope:envelope(),rightsAdmission:{admitted:true,permissions:['rehost']},editorialAdmission:{admitted:true,permissions:['rehost']}}]);
  const deferred=admitSourceUses([{id:'runtime-source',use:'read',envelope:envelope({access:{modes:['browser-runtime'],preferred:'browser-runtime'},runtimeBoundary:{required:true,mode:'browser-runtime'}})}]);
  const forbiddenAuthority=admitSourceUses([{id:'authority-source',use:'cite',envelope:envelope({authority:{sourceIsAuthority:true,identityClaimOnly:false,canonicalIdentityAuthority:true,envelopeAuthority:false}})}]);
  const blockedBook={schema:'dore.book-model.v1',id:'blocked-book',workId:'blocked-book',editionId:'',intent:{},publicationMetadata:{title:'Blocked'},structure:{frontMatter:[],body:[],backMatter:[]},sections:[],assets:[],notes:[],citations:[],relations:[],design:{},artifacts:{web:null,epub:null,pdf:null},validation:{status:'pending',gates:[]},internalProvenance:{}};
  const blockedBuild={schema:'dore.book-build.v1',qaResult:{status:'pending'},validation:{}};
  const blockedAutopilot=await runPublishingAutopilot({bookModel:blockedBook,bookBuild:blockedBuild,editorialReport:{readiness:'ready',counts:{authorialDecisions:0}},sourceUses:[{id:'rights-source',use:'rehost',envelope:envelope()}]});
  const publicProjection=publicationProjection(blockedBook);

  const coverSvg='<svg xmlns="http://www.w3.org/2000/svg" width="600" height="900"><rect width="100%" height="100%" fill="#eee8da"/><text x="60" y="160" font-size="52">Dore Test</text></svg>';
  const cover={id:'cover-test',data_url:'data:image/svg+xml;base64,'+btoa(coverSvg),mime_type:'image/svg+xml'};
  const bookModel={id:'artifact-e2e',workId:'work-e2e',editionId:'edition-e2e',publicationMetadata:{title:'Doré Artifact E2E',language:['en']},sections:[{id:'c1',title:'Chapter One',text:'A real publication artifact test.'}],design:{cover},artifacts:{},validation:{gates:[]}};
  const bookBuild={qaResult:{}};
  const set=buildPublicationArtifacts({bookModel,bookBuild,requireCover:true});
  const mat=await materializePublicationArtifacts(set);
  const head=async(blob,n)=>Array.from(new Uint8Array(await blob.slice(0,n).arrayBuffer()));
  document.body.insertAdjacentHTML('beforeend','<div id="menuExport"><div class="mac-submenu"><button data-export="pdf">PDF</button></div></div><span id="saveState"></span>');
  await import('/static/multiwrite/publication-output.mjs');await new Promise(r=>setTimeout(r,20));
  return{
    status:mat.status,
    acceptance:mat.acceptance,
    epubHead:await head(mat.files.epub.blob,2),
    pdfHead:String.fromCharCode(...await head(mat.files.pdf.blob,5)),
    sizes:{epub:mat.files.epub.blob.size,pdf:mat.files.pdf.blob.size,web:mat.files.web.blob.size},
    cover:Boolean(mat.files.cover),
    wiring:{epub:Boolean(document.querySelector('[data-formal-export="epub"]')),web:Boolean(document.querySelector('[data-formal-export="web"]')),pdfHook:document.querySelector('[data-export="pdf"]')?.dataset.legacyPdf==='1'},
    capability:{
      admitted:admitted.status,
      rightsBlocked:rightsBlocked.status,
      rightsReason:rightsBlocked.rows[0]?.reason,
      rightsAdmitted:rightsAdmitted.status,
      deferred:deferred.status,
      deferredReason:deferred.rows[0]?.reason,
      forbiddenAuthority:forbiddenAuthority.status,
      autopilotState:blockedAutopilot.state,
      autopilotArtifacts:Boolean(blockedAutopilot.artifacts),
      privateAdmissionStored:Boolean(blockedBook.internalProvenance?.sourceCapabilityAdmission),
      publicAdmissionLeaked:Object.prototype.hasOwnProperty.call(publicProjection,'internalProvenance')
    }
  };
});
await browser.close();
assert.equal(result.status,'accepted');
assert.deepEqual(result.epubHead,[80,75]);
assert.equal(result.pdfHead,'%PDF-');
assert.equal(result.acceptance.cover,true);
assert.ok(result.sizes.epub>200);
assert.ok(result.sizes.pdf>1000);
assert.ok(result.sizes.web>100);
assert.equal(result.cover,true);
assert.deepEqual(result.wiring,{epub:true,web:true,pdfHook:true});
assert.deepEqual(result.capability,{
  admitted:'admitted',
  rightsBlocked:'blocked',
  rightsReason:'rights-admission-required:rehost',
  rightsAdmitted:'admitted',
  deferred:'deferred',
  deferredReason:'runtime-capability-required',
  forbiddenAuthority:'blocked',
  autopilotState:'blocked',
  autopilotArtifacts:false,
  privateAdmissionStored:true,
  publicAdmissionLeaked:false
});
console.log(JSON.stringify({ok:true,...result}));
