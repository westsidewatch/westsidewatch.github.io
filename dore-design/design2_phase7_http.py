#!/usr/bin/env python3
"""Phase 7 production acceptance overlay for resident entrypoint."""
def install(H,base):
    old=H.do_GET
    def do_GET(self):
        from urllib.parse import urlparse
        if urlparse(self.path).path=='/api/design2/production-health':
            import design2_final_acceptance
            final=design2_final_acceptance.check(base)
            return self.out(200,{'ok':final['ok'],'service':'dore-design','version':'2.0-production','phase':7,'status':'complete' if final['ok'] else 'incomplete','acceptance':final})
        return old(self)
    H.do_GET=do_GET
