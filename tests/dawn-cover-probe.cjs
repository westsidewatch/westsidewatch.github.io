// Diagnostic only: discover an actually accessible exact Chinese edition image.
const urls=[
["campus_01_jpg","https://shop.campus.org.tw/Images/thumbs/000616607_01_500_500.jpg"],
["campus_02_png","https://shop.campus.org.tw/Images/thumbs/000616607_02_500_500.png"],
["campus_plain_jpg","https://shop.campus.org.tw/Images/thumbs/000616607_500_500.jpg"],
["publisher","https://resource.cosmiccare.org/api/Resource/Image/947305e3-2659-45ff-8f79-284107b2b0ac"],
["eslite","https://s.eslite.com/b2b/vendor/vendor175876280585020250925091252/mainCoverImage1_1529547.jpg"]
];
(async()=>{for(const [label,url] of urls){try{
 const controller=new AbortController();const timer=setTimeout(()=>controller.abort(),6500);
 const r=await fetch(url,{redirect:"follow",signal:controller.signal,headers:{"User-Agent":"Mozilla/5.0 (compatible; DawnLibraryBookCoverAudit/1.0)","Referer":"https://shop.campus.org.tw/ProductDetails.aspx?ProductID=000616607"}});
 clearTimeout(timer);
 const bytes=new Uint8Array(await r.arrayBuffer());
 console.log(JSON.stringify({label,status:r.status,type:r.headers.get("content-type"),bytes:bytes.length,magic:Array.from(bytes.slice(0,9)).map(x=>x.toString(16).padStart(2,"0")).join(""),url}));
 }catch(e){console.log(JSON.stringify({label,error:String(e).slice(0,170),url}));}}
})().catch(e=>{console.error(e);process.exitCode=1});
