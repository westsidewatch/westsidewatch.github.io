#!/usr/bin/env python3
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
rt=(ROOT/'static/dore/dore-search-runtime.js').read_text(encoding='utf-8')
api=(ROOT/'local/dore-local/dore_local.py').read_text(encoding='utf-8')
checks={
 'runtime-v7': "version:'7.0.0'" in rt,
 'persistent-current-id': "localStorage.getItem(CONVERSATION_KEY)" in rt and "localStorage.setItem(CONVERSATION_KEY" in rt,
 'open-zh-en': 'ask\\s+dore' in rt and '(?:問|问)多雷' in rt,
 'close-zh-en': '(?:搜索|search)' in rt,
 'history-endpoint': "LOCAL_CONVERSATIONS='http://127.0.0.1:8788/conversations'" in rt,
 'reopen-endpoint': "LOCAL_CONVERSATION='http://127.0.0.1:8788/conversation'" in rt,
 'history-control': 'id="dore-history-btn"' in rt,
 'new-control': 'id="dore-new-btn"' in rt,
 'search-control': 'id="dore-search-btn"' in rt,
 'thread-appends': "appendMessage('user'" in rt and "appendMessage('assistant'" in rt,
 'local-only-chat': "LOCAL_CHAT='http://127.0.0.1:8788/chat'" in rt and 'cloudflare-workers-ai' not in rt and 'CONVERSATION_API' not in rt,
 'backend-list': "if path=='/conversations':" in api and 'conversation_list(' in api,
 'backend-history': "if path=='/conversation':" in api and 'conversation_history(' in api,
 'backend-ordered-messages': "ORDER BY created_at ASC" in api,
 'gemma-default': "DORE_LOCAL_MODEL','gemma4:e4b'" in api,
 'gemma-no-thinking': "'think':False" in api,
}
failed=[k for k,v in checks.items() if not v]
for k,v in checks.items(): print(('PASS' if v else 'FAIL')+' '+k)
if failed: raise SystemExit('DORÉ_CONVERSATION_INTERFACE_CONTRACT_FAIL '+','.join(failed))
print('DORE_CONVERSATION_INTERFACE_CONTRACT_PASS')
