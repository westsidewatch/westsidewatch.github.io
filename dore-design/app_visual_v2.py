#!/usr/bin/env python3
"""Doré Design 1.1 — real New Westside homepage is the default visual surface; editor remains at /editor."""
import os
from pathlib import Path
from http.server import ThreadingHTTPServer
import app_visual as visual

ROOT=Path(__file__).resolve().parent.parent
HOMEPAGE=ROOT/'dore-design/new-westside/homepage-v1.html'

# Keep the structured editor, but make its relationship to the visual surface explicit.
EDITOR_HTML=visual.HTML.replace(
    '<div id="top"><b>DORÉ DESIGN 1.0 · NEW WESTSIDE</b>',
    '<div id="top"><b>DORÉ DESIGN 1.1 · STRUCTURE EDITOR</b><button onclick="location.href=\'/\'">Visual Homepage</button>'
)

class H(visual.H):
    def send_bytes(self, status, body, ctype):
        self.send_response(status)
        self.send_header('Content-Type', ctype)
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path=self.path.split('?',1)[0]
        if path=='/':
            if not HOMEPAGE.exists():
                return self.out(500, {'ok':False,'error':'homepage_visual_missing'})
            html=HOMEPAGE.read_text(encoding='utf-8')
            # Local Doré Design serves canonical repo assets directly.
            html=html.replace('/images/westside-watch-masthead-landscape.svg','/asset/masthead.svg')
            html=html.replace('/images/westside-watch-morning-star.svg','/asset/morning-star.svg')
            # Add one unobtrusive workbench affordance without altering the design composition.
            html=html.replace('</body>', '<a href="/editor" style="position:fixed;right:18px;bottom:18px;z-index:9999;background:#102a43;color:#faf9f5;border:1px solid #a2872a;padding:9px 12px;text-decoration:none;font:10px ui-monospace,monospace;letter-spacing:.12em">EDIT IN DORÉ DESIGN</a></body>')
            return self.send_bytes(200, html.encode('utf-8'), 'text/html; charset=utf-8')
        if path=='/editor':
            return self.send_bytes(200, EDITOR_HTML.encode('utf-8'), 'text/html; charset=utf-8')
        if path=='/asset/morning-star.svg':
            p=ROOT/'static/images/westside-watch-morning-star.svg'
            if p.exists(): return self.send_bytes(200,p.read_bytes(),'image/svg+xml')
        if path=='/api/health':
            return self.out(200,{
                'ok':True,
                'service':'dore-design',
                'version':'1.1',
                'workspace':'new-westside',
                'default_surface':'real-homepage-v1',
                'editor':'/editor',
                'visual_grammar':['official-masthead','editorial-gravity','5:8','huarong-reflow','crenellation','central-gate','dore-engraving','archival-print','time-flow']
            })
        return super().do_GET()

if __name__=='__main__':
    ThreadingHTTPServer(('127.0.0.1',int(os.environ.get('DORE_DESIGN_PORT','4310'))),H).serve_forever()
