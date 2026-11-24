import copy, importlib.util, unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("gate",Path(__file__).resolve().parents[1]/"scripts/dore_visual_workchain.py")
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
P=g.CONTRACT["allowed_prefix"]
A=P+"a.html";B=P+"b.html";H={p:"current" for p in g.CONTRACT["authority"]}
def event(stage,**kw):return dict(stage=stage,status="pass",**kw)
def fixture():
    return {"events":[event("authority",authority=H),event("exploration",references=[dict(url=f"https://example{i}.org/work",mechanism="grid",application="composition",license_or_rights="reference only",decision="study") for i in range(3)]),event("composition",candidates=[dict(html=A,principle="collision"),dict(html=B,principle="quiet")]),event("technical",proofs=[dict(candidate=c,width=w,png=P+f"{c[-6]}-{w}.png",os_colors=True,os_fonts=True,no_overflow=True,readable=True) for c in (A,B) for w in (1440,390)]),event("critique",winner=A,comparison="comparison",blocking_issues=[])]}
def read(p):
    if p.endswith(".png"):return b"\x89PNG\r\n\x1a\n"+b"x"*200
    return ("<html><body>"+p+"</body></html>").encode()
class Gate(unittest.TestCase):
    def reject(self,r,reader=read):
        with self.assertRaises(ValueError):g.check(r,H,reader)
    def test_valid_waits_for_human(self):self.assertEqual(g.check(fixture(),H,read),"human")
    def test_missing_os(self):
        r=fixture();r["events"][0]["authority"]={};self.reject(r)
    def test_stale_os(self):
        r=fixture();r["events"][0]["authority"]={"old":"old"};self.reject(r)
    def test_skip_research(self):
        r=fixture();r["events"].pop(1);self.reject(r)
    def test_no_research(self):
        r=fixture();r["events"][1]["references"]=[];self.reject(r)
    def test_reused_css(self):
        self.reject(fixture(),lambda p:b"<html><body>westside-editorial-grammar.css</body></html>")
    def test_duplicate(self):
        self.reject(fixture(),lambda p:b"<html><body>same</body></html>")
    def test_p2(self):
        with self.assertRaises(ValueError):g.scope(["static/css/p2-living-water.css"])
    def test_wrong_color(self):
        r=fixture();r["events"][3]["proofs"][0]["os_colors"]=False;self.reject(r)
    def test_wrong_font(self):
        r=fixture();r["events"][3]["proofs"][0]["os_fonts"]=False;self.reject(r)
    def test_no_screenshot(self):
        r=fixture();r["events"][3]["proofs"]=[];self.reject(r)
    def test_report_only(self):
        self.reject(fixture(),lambda p:b"report")
    def test_self_approval(self):
        r=fixture();r["events"].append(event("human",approved=True));self.reject(r)
    def test_production(self):
        self.assertFalse(g.CONTRACT["production_allowed"])
if __name__=="__main__":unittest.main()
