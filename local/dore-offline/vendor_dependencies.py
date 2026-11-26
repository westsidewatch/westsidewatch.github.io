"""Localize explicitly allowed public web dependencies; never crawl media or links."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import html
from pathlib import Path
import re
import urllib.parse
import urllib.request

GSAP = "https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"
CHIRON = "https://cdn.jsdelivr.net/npm/chiron-hei-hk-webfont/css/vf.css"
GOOGLE = "https://fonts.googleapis.com/css2?family=Bodoni+Moda:ital,opsz,wght@0,6..96,400%3B1,6..96,400&family=Bodoni+Moda+SC:ital,opsz,wght@0,6..96,400%3B1,6..96,400&family=Noto+Serif+TC:wght@400%3B600&display=swap"
SOURCES = {GSAP: ".js", CHIRON: ".css", GOOGLE: ".css"}
CSS_URL = re.compile(r"url\(\s*(['\"]?)([^)'\"\s]+)\1\s*\)", re.I)
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
PREFIX = "/offline-vendor/"

def allowed(url):
    p = urllib.parse.urlsplit(url)
    return p.scheme == "https" and not p.username and not p.password and (
        url in SOURCES or (p.hostname == "fonts.gstatic.com" and p.path.endswith((".woff2", ".woff", ".ttf"))) or
        (p.hostname == "cdn.jsdelivr.net" and p.path.startswith("/npm/chiron-hei-hk-webfont") and p.path.endswith((".woff2", ".woff", ".ttf", ".css"))))

class Redirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not allowed(newurl):
            raise ValueError("Rejected dependency redirect: " + newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)

def fetch(url):
    if not allowed(url):
        raise ValueError("Dependency outside allowlist: " + url)
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.build_opener(Redirect()).open(request, timeout=35) as response:
        data = response.read(16 * 1024 * 1024 + 1)
        if not data or len(data) > 16 * 1024 * 1024:
            raise ValueError("Invalid dependency size: " + url)
        return data

def name_for(url):
    ext = SOURCES.get(url) or Path(urllib.parse.urlsplit(url).path).suffix
    return hashlib.sha256(url.encode()).hexdigest()[:24] + ext

def localize(root, get=fetch):
    # Discover only exact approved source URLs in built HTML/CSS/JS.
    references = []
    for p in sorted(root.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in (".html", ".css", ".js", ".mjs"):
            continue
        try:
            source = p.read_text(encoding="utf-8")
        except UnicodeError:
            continue
        hits = [url for url in SOURCES if url in source or html.escape(url, quote=False) in source]
        if hits:
            references.append((p, source, hits))
    required = sorted({url for _, _, hits in references for url in hits})
    if not required:
        return {}
    out = root / "offline-vendor"
    out.mkdir(exist_ok=True)
    assets = {}
    pending = set(required)
    while pending:
        batch = sorted(pending)
        pending.clear()
        with ThreadPoolExecutor(max_workers=8) as pool:
            payloads = list(pool.map(get, batch))
        for url, data in zip(batch, payloads):
            name = name_for(url)
            if name.endswith(".css"):
                css = data.decode("utf-8")
                def rewrite(match):
                    raw = match.group(2)
                    if raw.startswith("data:"):
                        return match.group(0)
                    child = urllib.parse.urljoin(url, raw)
                    if not allowed(child):
                        raise ValueError("Unapproved nested font dependency: " + child)
                    if child not in assets and child not in batch:
                        pending.add(child)
                    return 'url("' + PREFIX + name_for(child) + '")'
                css = CSS_URL.sub(rewrite, css)
                data = css.encode("utf-8")
            (out / name).write_bytes(data)
            assets[url] = {"path": PREFIX + name, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
    for p, source, hits in references:
        for url in hits:
            source = source.replace(url, assets[url]["path"]).replace(html.escape(url, quote=False), assets[url]["path"])
        p.write_text(source, encoding="utf-8")
    return assets
