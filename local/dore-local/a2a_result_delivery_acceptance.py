#!/usr/bin/env python3
import os,tempfile

with tempfile.TemporaryDirectory(prefix='dore-a2a-result-') as td:
 os.environ['DORE_LOCAL_HOME']=td
 import a2a_result_delivery as rd
 source='result-delivery-acceptance-1'
 proof={'ok':True,'task':{'status':'PASS','artifact':{'type':'acceptance','sha256':'a'*64},'verification':{'ok':True,'method':'acceptance'}},'completion_evidence':True}
 receipt=rd.build(source,'PASS',{'ok':True},proof,attempt=1,terminal=True)
 assert receipt['completion_evidence'] is True
 assert receipt['verification_ok'] is True
 assert rd.record(receipt)['code']=='EXECUTION_RECEIPT_RECORDED'
 assert rd.record(receipt)['code']=='EXECUTION_RECEIPT_REPLAY'
 running={'ok':True,'task':{'status':'RUNNING'},'completion_evidence':False}
 rd.record(rd.build('result-delivery-acceptance-2','RETRYABLE',{'ok':False},running,attempt=1))
 rd.record(rd.build('result-delivery-acceptance-2','PASS',{'ok':True},proof,attempt=2,terminal=True))
 assert rd.latest('result-delivery-acceptance-2')['task_status']=='PASS'
 print('A2A_RESULT_DELIVERY_PASS')
