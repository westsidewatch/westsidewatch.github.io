#!/usr/bin/env python3
"""Mount Multiwrite Cover as a real editable DORÉ DESIGN page."""
PAGE_ID='multiwrite-cover'

def ensure(base):
    w=base.workspace()
    if base.page(w,PAGE_ID): return w
    p={
      'id':PAGE_ID,'name':'多寫 · Cover','canvas':{'w':1200,'h':1500},
      'design':{'schema':'dore.design-decision.v1','surface':'multiwrite.cover','decision':{'color':'first-light','hierarchy':'display','axis':'center','density':'1','lines':'1'}},
      'nodes':[
        {'id':'mwc-frame','type':'block','role':'frame','semantic_zone':'cover-frame','x':58,'y':58,'w':1084,'h':1384,'frame_fill':'transparent','frame_stroke':'#8c6818'},
        {'id':'mwc-kicker','type':'text','semantic_zone':'cover-kicker','text':'DORÉ · MULTIWRITE','x':300,'y':180,'w':600,'h':36,'size':18},
        {'id':'mwc-title','type':'text','role':'hero','semantic_zone':'cover-title','text':'多寫','x':250,'y':500,'w':700,'h':150,'size':108},
        {'id':'mwc-subtitle','type':'text','semantic_zone':'cover-subtitle','text':'讓文字成為作品','x':300,'y':690,'w':600,'h':70,'size':32},
        {'id':'mwc-rule','type':'rule','semantic_zone':'cover-rule','x':440,'y':820,'w':320,'h':1},
        {'id':'mwc-note','type':'text','semantic_zone':'cover-note','text':'WRITE · EDIT · PUBLISH','x':360,'y':1180,'w':480,'h':40,'size':16}
      ]
    }
    w['pages'].insert(0,p)
    return base.save(w)
