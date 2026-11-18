// Existing specialist regression scenarios explicitly open the new review drawer.
// The V1 browser suite separately verifies the real collapsed default.
export async function openToolsForReview(page){
 if(!(process.env.J3K_URL||'').startsWith('https:'))await page.route('**/css/typography-sitewide.css',r=>r.fulfill({path:'static/css/typography-sitewide.css',contentType:'text/css'}));
 await page.addInitScript(()=>{const show=()=>{const tools=document.querySelector('.j3k-tools');if(!tools)return false;tools.open=true;return true;};if(!show()){const o=new MutationObserver(()=>{if(show())o.disconnect();});o.observe(document,{childList:true,subtree:true});}});
}
