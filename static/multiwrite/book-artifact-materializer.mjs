const JSZIP_URL='https://cdn.jsdelivr.net/npm/jszip@3.10.1/dist/jszip.min.js';
const JSPDF_URL='https://cdn.jsdelivr.net/npm/jspdf@2.5.2/dist/jspdf.umd.min.js';
function loadScript(src,test){if(test())return Promise.resolve();return new Promise((resolve,reject)=>{const s=document.createElement('script');s.src=src;s.onload=()=>resolve();s.onerror=()=>reject(new Error(`artifact dependency failed: ${src}`));document.head.appendChild(s)})}
function blobUrl(blob){return URL.createObjectURL(blob)}
function asBlob(content,type){return content instanceof Blob?content:new Blob([content],{type})}
function decodePackage(artifact){const raw=typeof artifact?.content==='string'?JSON.parse(artifact.content):artifact?.content;if(!raw?.files)throw new Error('EPUB package files missing.');return raw}
export async function materializePublicationArtifacts(artifactSet,{coverBlob=null}={}){
 if(!artifactSet?.web||!artifactSet?.epub||!artifactSet?.pdf)throw new Error('Artifact set incomplete.');
 await Promise.all([loadScript(JSZIP_URL,()=>Boolean(window.JSZip)),loadScript(JSPDF_URL,()=>Boolean(window.jspdf?.jsPDF))]);
 const webBlob=asBlob(artifactSet.web.content,'text/html;charset=utf-8');
 const pkg=decodePackage(artifactSet.epub),zip=new window.JSZip();
 zip.file('mimetype','application/epub+zip',{compression:'STORE'});
 zip.file('META-INF/container.xml','<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>');
 for(const [name,content] of Object.entries(pkg.files))zip.file(name,content);
 if(coverBlob)zip.file('OEBPS/cover.png',coverBlob);
 const epubBlob=await zip.generateAsync({type:'blob',mimeType:'application/epub+zip',compression:'DEFLATE'});
 const {jsPDF}=window.jspdf,pdf=new jsPDF({unit:'mm',format:'a5'}),text=(artifactSet.pdf.renderSource||'').replace(/<[^>]+>/g,' ').replace(/\s+/g,' ').trim();
 const lines=pdf.splitTextToSize(text,112);let y=18;for(const line of lines){if(y>192){pdf.addPage();y=18}pdf.text(line,15,y);y+=6}
 const pdfBlob=pdf.output('blob');
 const files={web:{filename:artifactSet.web.filename,blob:webBlob,url:blobUrl(webBlob)},epub:{filename:artifactSet.epub.filename.replace(/\.epub-package\.json$/,'.epub'),blob:epubBlob,url:blobUrl(epubBlob)},pdf:{filename:artifactSet.pdf.filename,blob:pdfBlob,url:blobUrl(pdfBlob)}};
 const acceptance={web:webBlob.size>100,epub:epubBlob.size>200,pdf:pdfBlob.size>500};
 const result={schema:'dore.materialized-publication.v1',status:Object.values(acceptance).every(Boolean)?'accepted':'blocked',acceptance,files};
 window.__doreMaterializedPublication=result;window.dispatchEvent(new CustomEvent('multiwrite:publication-materialized',{detail:result}));return result;
}
export function downloadMaterializedPublication(result){for(const item of Object.values(result?.files||{})){const a=document.createElement('a');a.href=item.url;a.download=item.filename;document.body.appendChild(a);a.click();a.remove()}}
