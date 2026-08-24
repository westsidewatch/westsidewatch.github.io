# Search Cognition Understanding Gate

Protocol under test: `dore-core/knowledge/search-cognition-protocol.md`

A declaration that Doré "understands" the protocol is forbidden until this gate passes.

## Stage A — taught contrasts
Doré must classify and explain:
- 聖靈 -> SEARCH
- 舊約聖靈 -> SEARCH + OT scope
- 舊約有聖靈嗎 -> QUESTION
- 馬利亞 -> SEARCH
- 馬利亞有幾位 -> QUESTION

## Stage B — unseen transfer cases
These cases are intentionally different from the teaching examples. The implementation/learning heartbeat must classify them from the principle, not from exact-string rules.

1. `約櫃` -> expected SEARCH
2. `撒母耳記 約櫃` -> expected SEARCH with contextual/book constraint
3. `約櫃為什麼不能隨便觸摸` -> expected QUESTION
4. `大衛 詩篇` -> expected SEARCH/contextual retrieval
5. `大衛為什麼不能建聖殿` -> expected QUESTION
6. `彼得提到聖靈的經文，他的理解和保羅有何不同` -> expected HYBRID
7. `新約 安息日` -> expected SEARCH + NT scope
8. `新約還需要守安息日嗎` -> expected QUESTION

## Stage C — explanation requirement
For every classification Doré must state a short reason in terms of user intent (find / understand-answer / both), not merely cite punctuation or a keyword regex.

## Stage D — product behavior requirement
Classification alone is insufficient.
- SEARCH must actually reach retrieval.
- scoped SEARCH must preserve scope through the asynchronous retrieval lifecycle.
- QUESTION must actually reach Brain; insufficient knowledge must reach sensory/research rather than empty search.
- HYBRID must permit Brain to use retrieval as evidence.

## Pass states
- `TAUGHT`: protocol exists but transfer has not been demonstrated.
- `CONCEPT_PASS`: unseen classifications + reasons pass.
- `PRODUCT_PASS`: unseen classifications pass and all routes execute correctly in the live product.

Current state: `TAUGHT`.

Do not report `CONCEPT_PASS`, `PRODUCT_PASS`, or "Doré understands" without recorded evidence from the corresponding gate.
