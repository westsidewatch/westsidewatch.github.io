"""Resident HTTP integration for DORÉ DESIGN 2.0 Phase 4."""
import json,os
from pathlib import Path
from urllib.parse import urlparse,parse_qs
import design2_publication,design2_renderer,design2_staging


def _registry(root):
    return Path(os.environ.get('DORE_DESIGN_PUBLICATION_REGISTRY',Path(root)/'.dore-design-publication.json'))


def install(handler_cls,base,root):
    original_get=handler_cls.do_GET;original_post=handler_cls.do_POST
    registry=_registry(root)

    def body(self,limit=262144):
        size=int(self.headers.get('Content-Length','0'))
        if size<1 or size>limit: raise ValueError('invalid_body_size')
        return json.loads(self.rfile.read(size))

    def send_html(self,html,status=200):
        data=html.encode('utf-8')
        self.send_response(status);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)

    def current_release():
        return design2_publication._load(registry).get('current_release')

    def candidate_row(cid):
        return (design2_publication._load(registry).get('candidates') or {}).get(cid)

    def do_GET(self):
        u=urlparse(self.path);path=u.path;q=parse_qs(u.query)
        if path=='/api/design2/publication':
            reg=design2_publication._load(registry)
            return self.out(200,{'ok':True,'registry':reg})
        if path=='/api/design2/preview':
            cid=(q.get('candidate') or [''])[0];row=candidate_row(cid)
            if not row:return self.out(404,{'ok':False,'error':'candidate_not_found'})
            try:return send_html(self,design2_renderer.render_snapshot(row['snapshot']))
            except Exception as e:return self.out(400,{'ok':False,'error':str(e)})
        if path=='/design2/published':
            rel=current_release()
            if not rel:return self.out(404,{'ok':False,'error':'no_published_release'})
            row=candidate_row(rel.get('candidate_id'))
            if not row:return self.out(500,{'ok':False,'error':'published_candidate_missing'})
            html=design2_renderer.render_snapshot(row['snapshot'])
            manifest=rel.get('staging') or {}
            if not design2_staging.same_render(manifest,html):return self.out(500,{'ok':False,'error':'published_render_hash_mismatch'})
            return send_html(self,html)
        return original_get(self)

    def do_POST(self):
        path=urlparse(self.path).path
        if path=='/api/design2/candidate':
            try:
                p=body(self);w=base.workspace();expected=p.get('revision')
                if expected is None or int(expected)!=int(w.get('revision',0)):raise ValueError('stale_revision')
                row=design2_publication.create_candidate(w,p.get('page_id'),registry)
                return self.out(201,{'ok':True,'candidate':row,'preview':'/api/design2/preview?candidate='+row['id']})
            except Exception as e:return self.out(409 if str(e)=='stale_revision' else 400,{'ok':False,'error':str(e)})
        if path=='/api/design2/publish':
            try:
                p=body(self);cid=p.get('candidate_id');row=candidate_row(cid)
                if not row:raise ValueError('candidate_not_found')
                if int(p.get('revision',-1))!=int(row['snapshot']['revision']):raise ValueError('publish_revision_mismatch')
                target=p.get('target')
                html=design2_renderer.render_snapshot(row['snapshot'])
                manifest=design2_staging.build_manifest(row,target,html)
                release=design2_publication.promote(cid,registry,manifest)
                return self.out(200,{'ok':True,'release':release,'published':'/design2/published'})
            except Exception as e:return self.out(400,{'ok':False,'error':str(e)})
        if path=='/api/design2/rollback':
            try:return self.out(200,{'ok':True,'release':design2_publication.rollback(registry),'published':'/design2/published'})
            except Exception as e:return self.out(400,{'ok':False,'error':str(e)})
        return original_post(self)

    handler_cls.do_GET=do_GET;handler_cls.do_POST=do_POST
    return handler_cls
