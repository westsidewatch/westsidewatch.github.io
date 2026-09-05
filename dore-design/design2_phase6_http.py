"""HTTP status surface for the Phase 6 Multiwrite production specimen."""
from urllib.parse import urlparse
import design2_phase6


def install(handler_cls,base):
    original_get=handler_cls.do_GET
    def do_GET(self):
        if urlparse(self.path).path=='/api/design2/specimen':
            status=design2_phase6.inspect(base.workspace())
            return self.out(200 if status.get('ok') else 503,status)
        return original_get(self)
    handler_cls.do_GET=do_GET
    return handler_cls
