#!/usr/bin/env python3
from __future__ import annotations
import importlib.util,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('dw',HERE/'dimensional_writing_capability.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

BAD='''亚伯死在田间。\n\n而且，是从地里。\n\n但是血没有沉默。于是土地开始说话。\n\n为什么？\n\n因为神记得。\n\n然而真正的问题，是义人的血意味着什么？\n\n所以到了这里，我们终于看见十字架。'''
GOOD='''该隐把亚伯带到田间，在那里杀了他。创世记没有留下埋葬的场面，叙事停在另一件事上：耶和华问该隐，他兄弟在哪里。该隐回答不知道。紧接着出现的是血的声音；希伯来文把“血”写成复数形式的构词 דְּמֵי，把“呼叫”写成 צֹעֲקִים，声音从土地上来到神面前。\n\n这块土地并非背景。亚当从地而出，该隐靠地谋生，亚伯的血又被地张口接住。民数记后来把杀人的后果写进以色列的土地秩序：流无辜人的血会污秽那地。申命记面对旷野中一个找不到凶手的尸体，要求长老和审判官量到四围城邑的距离；一个倒在野外的人，把附近的城、长老、祭司和土地一同带进责任之中。创世记第四章那声从土里来的呼喊，由此有了更大的尺度。'''

def fake_infer(_messages):
 return json.dumps({'manuscript':GOOD,'semanticAdmission':{'paragraphIntegrity':{'pass':True,'reason':'paragraphs carry complete movements'},'semanticPressure':{'pass':True,'reason':'meaning accumulates through evidence'},'evidenceBeforeIntensity':{'pass':True,'reason':'claims follow textual and legal material'},'depthBeforeAnalogy':{'pass':True,'reason':'no premature analogy'},'prematureCoherence':{'pass':True,'reason':'conclusion not announced early'},'authorAuthority':{'pass':True,'reason':'no thesis rewrite'}},'revisions':['removed manufactured line breaks and connective scaffolding'],'unresolved':[]},ensure_ascii=False)

bad=m.execute({'manuscript':BAD});assert 'isolated-short-paragraphs' in bad['report']['diagnostics']['risks'];assert bad['report']['admission']=='diagnostics-only'
result=m.execute({'manuscript':BAD,'authorThesis':'十字架的影子里有生命'},fake_infer);report=result['report'];assert report['publishable'] is True,report;assert report['authority']['mayRewriteThesis'] is False;assert not report['postDiagnostics']['risks'],report['postDiagnostics']
print(json.dumps({'schema':'dore.dimensional-writing-acceptance.v0','status':'PASS','badRisks':bad['report']['diagnostics']['risks'],'postRisks':report['postDiagnostics']['risks'],'authorAuthority':report['authority']},ensure_ascii=False,indent=2))
