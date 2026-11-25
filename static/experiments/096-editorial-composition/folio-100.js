(()=>{if(!document.documentElement.classList.contains('art100'))return;
const $=s=>document.querySelector(s),main=$('main');
function bind(){for(const e of main.querySelectorAll('h2,h3,.ws-church-sunday-row strong,.church-visit__contact-grid strong'))e.dataset.folioZh='title';
for(const e of main.querySelectorAll('.church-visit__seal,.folio-day,.folio-mode,.folio-time-note,.church-visit__gathering>small,.folio-index-title [lang=zh-Hant],.ws-sunday-source-status,.ws-church-scriptures small'))e.dataset.folioZh='air';
for(const e of main.querySelectorAll('.folio-meeting-time'))if(/[\u3400-\u9fff]/.test(e.textContent)){e.lang='zh-Hant';e.dataset.folioZh='air'}else e.lang='en';
for(const e of main.querySelectorAll('.folio-index nav a [lang=en],.church-visit__section-head>span b,.folio-ministry-en,.folio-day-en,.folio-index-caption')){e.lang='en';e.dataset.wsDesignable='true'}
const meetings=$('#church-gathering-list');if(meetings.querySelectorAll('article').length===4&&!meetings.dataset.week){meetings.dataset.week='1';const days={'Sunday':1,'Monday':2,'Wednesday':4,'Friday':6};for(const a of meetings.querySelectorAll('article'))a.style.setProperty('--day-start',String(days[a.querySelector('.folio-day-en')?.textContent]||1));}}
const observer=new MutationObserver(bind);for(const id of ['#church-gathering-list','#church-sunday-live','#church-ministry-list'])observer.observe($(id),{childList:true,subtree:true});bind();
const link=document.createElement('a');link.href='#welcome';link.textContent='返回篇章目錄';$('.church-visit__footer nav').prepend(link);
})();