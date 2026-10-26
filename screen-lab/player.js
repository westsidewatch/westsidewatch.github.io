/* Screen Lab: online playback only. No downloading, proxying, or persistence. */
(() => {
  const form = document.querySelector('#stream-form');
  const input = document.querySelector('#stream-url');
  const status = document.querySelector('#stream-status');
  const host = document.querySelector('#stream-stage');
  if (!form || !input || !host || !status) return;
  let hls = null;
  let playbackAttempt = 0;
  function cleanup() {
    if (hls) { hls.destroy(); hls = null; }
    const old = host.querySelector('video');
    if (old) { old.pause(); old.removeAttribute('src'); old.load(); old.remove(); }
  }
  function say(message) { status.textContent = message; }
  form.addEventListener('submit', event => {
    event.preventDefault();
    cleanup();
    const attempt=++playbackAttempt;
    let url;
    try { url = new URL(input.value.trim()); } catch { say('請輸入完整的 HTTPS 影片串流網址。'); return; }
    if (url.protocol !== 'https:') { say('只接受 HTTPS 媒體網址。'); return; }
    const path = url.pathname.toLowerCase();
    const isHls = path.endsWith('.m3u8');
    const isFile = /\.(mp4|m4v|webm|ogv|ogg)$/.test(path);
    if (!isHls && !isFile) { say('目前支援直接媒體連結：MP4、WebM、Ogg 或 HLS .m3u8；不解析影視網站頁面。'); return; }
    const video = document.createElement('video');
    video.controls = true;
    video.playsInline = true;
    video.preload = 'metadata';
    video.setAttribute('aria-label', 'Screen Lab 線上播放器');
    video.addEventListener('error', () => say('播放失敗。可能是來源失效、跨域限制或格式不支援。'));
    video.addEventListener('playing', () => say('影片正在播放。此結果僅證明當前瀏覽器能讀取來源，不代表播放授權已核實。'));
    video.addEventListener('waiting', () => say('正在緩衝影片…'));
    video.addEventListener('ended', () => say('影片播放結束。'));
    video.addEventListener('canplay', () => { if(attempt!==playbackAttempt)return; say('媒體已準備好。請按播放鍵開始觀看。'); });
    host.replaceChildren(video);
    if (isHls && window.Hls?.isSupported()) {
      hls = new window.Hls({ enableWorker: true });
      hls.on(window.Hls.Events.ERROR, (_, data) => { if (data.fatal && attempt===playbackAttempt) say('HLS 串流無法播放：' + data.type); });
      hls.loadSource(url.href);
      hls.attachMedia(video);
    } else if (!isHls || video.canPlayType('application/vnd.apple.mpegurl')) {
      video.src = url.href;
    } else {
      say('此瀏覽器不支援 HLS。');
      cleanup();
      return;
    }
    say('正在嘗試連接媒體來源，尚未確認可播放。');
    video.play().catch(() => { if(attempt===playbackAttempt && video.paused) say('瀏覽器未自動播放。請按影片上的播放鍵開始觀看。'); });
  });
  document.querySelector('#stream-stop')?.addEventListener('click', () => { ++playbackAttempt; cleanup(); say('已停止播放並釋放播放器。'); });
  window.addEventListener('pagehide', cleanup);
})();
