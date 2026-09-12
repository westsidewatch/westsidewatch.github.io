const VERSION = '6.3.289';
const MODULE_URL = `https://cdn.jsdelivr.net/npm/pdfjs-dist@${VERSION}/build/pdf.min.mjs`;
const WORKER_URL = `https://cdn.jsdelivr.net/npm/pdfjs-dist@${VERSION}/build/pdf.worker.min.mjs`;

const root = document.querySelector('[data-dawn-pdf-surface]');
if (root) {
  const params = new URLSearchParams(location.search);
  const source = params.get('src') || '';
  const status = root.querySelector('[data-pdf-status]');
  const canvas = root.querySelector('[data-pdf-canvas]');
  const pageNode = root.querySelector('[data-pdf-page]');
  const pagesNode = root.querySelector('[data-pdf-pages]');
  const prev = root.querySelector('[data-pdf-prev]');
  const next = root.querySelector('[data-pdf-next]');
  const zoomIn = root.querySelector('[data-pdf-zoom-in]');
  const zoomOut = root.querySelector('[data-pdf-zoom-out]');
  const sourceLink = root.querySelector('[data-pdf-source]');

  let sourceUrl;
  try {
    sourceUrl = new URL(source);
    if (sourceUrl.protocol !== 'https:') throw new Error('https required');
  } catch (_) {
    root.dataset.viewerState = 'invalid-source';
    status.textContent = '無效的 PDF 來源。';
    throw new Error('Dawn PDF Surface requires an HTTPS ?src= URL');
  }

  sourceLink.href = sourceUrl.href;
  root.dataset.externalSource = 'true';
  root.dataset.viewerState = 'loading';

  const pdfjsLib = await import(MODULE_URL);
  pdfjsLib.GlobalWorkerOptions.workerSrc = WORKER_URL;

  let pdf;
  let currentPage = 1;
  let scale = 1.25;
  let renderTask = null;

  async function render() {
    if (!pdf) return;
    if (renderTask) {
      renderTask.cancel();
      renderTask = null;
    }
    const page = await pdf.getPage(currentPage);
    const viewport = page.getViewport({ scale });
    const ratio = window.devicePixelRatio || 1;
    const context = canvas.getContext('2d');
    canvas.width = Math.floor(viewport.width * ratio);
    canvas.height = Math.floor(viewport.height * ratio);
    canvas.style.width = `${Math.floor(viewport.width)}px`;
    canvas.style.height = `${Math.floor(viewport.height)}px`;
    context.setTransform(ratio, 0, 0, ratio, 0, 0);
    renderTask = page.render({ canvasContext: context, viewport });
    try {
      await renderTask.promise;
      root.dataset.viewerState = 'ready';
      status.textContent = 'PDF.js · external source';
    } catch (error) {
      if (error?.name !== 'RenderingCancelledException') throw error;
    } finally {
      renderTask = null;
    }
    pageNode.textContent = String(currentPage);
    pagesNode.textContent = String(pdf.numPages);
    prev.disabled = currentPage <= 1;
    next.disabled = currentPage >= pdf.numPages;
  }

  try {
    pdf = await pdfjsLib.getDocument({ url: sourceUrl.href }).promise;
    root.dataset.pdfjsVersion = VERSION;
    root.dataset.pageCount = String(pdf.numPages);
    await render();
  } catch (error) {
    root.dataset.viewerState = 'failed';
    status.textContent = 'PDF.js 無法讀取此外部 PDF；可使用「原始 PDF」開啟。';
    console.warn('[Dawn PDF Surface]', error);
  }

  prev.addEventListener('click', async () => {
    if (currentPage <= 1) return;
    currentPage -= 1;
    await render();
  });
  next.addEventListener('click', async () => {
    if (!pdf || currentPage >= pdf.numPages) return;
    currentPage += 1;
    await render();
  });
  zoomIn.addEventListener('click', async () => {
    scale = Math.min(3, scale + 0.2);
    await render();
  });
  zoomOut.addEventListener('click', async () => {
    scale = Math.max(0.6, scale - 0.2);
    await render();
  });
}
