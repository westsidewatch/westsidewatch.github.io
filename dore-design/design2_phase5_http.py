"""Resident HTTP integration for DORÉ DESIGN 2.0 Phase 5 recommendations."""
import json,os
from pathlib import Path
from urllib.parse import urlparse
import design2_recommendations


def _log(root):
    return Path(os.environ.get('DORE_DESIGN_RECOMMENDATION_LOG',Path(root)/'.dore-design-recommendations.json'))


def install(handler_cls,base,root):
    original_get=handler_cls.do_GET;original_post=handler_cls.do_POST
    log_path=_log(root)

    def body(self,limit=262144):
        size=int(self.headers.get('Content-Length','0'))
        if size<1 or size>limit: raise ValueError('invalid_body_size')
        return json.loads(self.rfile.read(size))

    def do_GET(self):
        path=urlparse(self.path).path
        if path=='/api/design2/recommendations':
            return self.out(200,{'ok':True,'log':design2_recommendations.state(log_path)})
        return original_get(self)

    def do_POST(self):
        path=urlparse(self.path).path
        try:
            if path=='/api/design2/recommendation':
                p=body(self)
                event=design2_recommendations.propose(base,log_path,p.get('page_id'),p.get('commands'),p.get('reason',''),p.get('context'),p.get('signals'))
                return self.out(201,{'ok':True,'recommendation':event})
            if path=='/api/design2/recommendation/decision':
                p=body(self)
                event=design2_recommendations.decide(base,log_path,p.get('recommendation_id'),p.get('decision'),p.get('revision'),p.get('commands'),p.get('note',''))
                return self.out(200,{'ok':True,'recommendation':event})
        except Exception as e:
            return self.out(409 if str(e)=='stale_revision' else 400,{'ok':False,'error':str(e)})
        return original_post(self)

    handler_cls.do_GET=do_GET;handler_cls.do_POST=do_POST
    return handler_cls
