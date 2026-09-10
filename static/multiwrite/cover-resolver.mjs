// DORÉ Cover Resolver: explicit/embedded → source-native → edition identity → ONE fallback.
// No model/provider is loaded globally; remote lookups are lazy and cacheable.
const CACHE_PREFIX='dore.cover.v1:';
const gutenbergId=url=>String(url||'').match(/gutenberg\.org\/ebooks\/(\d+)/i)?.[1]||null;
function cached(id){try{return JSON.parse(localStorage.getItem(CACHE_PREFIX+id)||'null')}catch{return null}}
function remember(id,value){try{localStorage.setItem(CACHE_PREFIX+id,JSON.stringify(value))}catch{}return value}
async function imageExists(url){return new Promise(resolve=>{const img=new Image();const done=v=>{img.onload=img.onerror=null;resolve(v)};img.onload=()=>done(true);img.onerror=()=>done(false);img.src=url})}
function explicitCover(book){const c=book?.cover;if(c?.url&&c.mode!=='one-fallback')return {url:c.url,kind:c.kind||'explicit',provider:c.provider||'catalog',provenance:c.provenance||c.url};return null}
async function sourceCover(book){for(const source of book?.sources||[]){const id=gutenbergId(source.url);if(!id)continue;for(const url of [`https://www.gutenberg.org/cache/epub/${id}/pg${id}.cover.medium.jpg`,`https://www.gutenberg.org/cache/epub/${id}/pg${id}.cover.small.jpg`])if(await imageExists(url))return {url,kind:'source-native',provider:'Project Gutenberg',provenance:source.url};}return null}
function identifiers(book){const e=book?.edition||{},w=book?.work||{},ids=e.identifiers||w.identifiers||{};return {isbn:e.isbn||w.isbn||ids.isbn||ids.ISBN,olid:e.olid||w.olid||ids.olid,oclc:e.oclc||w.oclc||ids.oclc,lccn:e.lccn||w.lccn||ids.lccn}}
async function editionCover(book){const ids=identifiers(book);for(const [key,value] of Object.entries(ids)){if(!value)continue;const type={isbn:'isbn',olid:'olid',oclc:'oclc',lccn:'lccn'}[key];const url=`https://covers.openlibrary.org/b/${type}/${encodeURIComponent(value)}-L.jpg?default=false`;if(await imageExists(url))return {url,kind:'edition-identity',provider:'Open Library',identifier:{type,value},provenance:'https://openlibrary.org/dev/docs/api/covers'};}return null}
export async function resolveCover(book){if(!book)return null;const direct=explicitCover(book);if(direct)return direct;const hit=cached(book.id);if(hit?.url&&await imageExists(hit.url))return hit;const resolved=await sourceCover(book)||await editionCover(book);return resolved?remember(book.id,resolved):null}
