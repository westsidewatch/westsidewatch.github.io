# Live Sensory Research — 馬利亞有幾位？

Signal: `5cf2c608-e66f-4176-a3f8-b3284819158a`
State: EXAM_PASS → PRODUCT_READABLE
Date: 2026-08-23

## Question boundary
The bare question 「馬利亞有幾位？」 is ambiguous. The useful default scope for Doré Bible Search is **distinct women named Mary/Maria/Mariam in the New Testament**, not every historical Mary and not the OT Miriam.

## Finding
A standard conservative identification yields **six distinct New Testament women named Mary**, while some identifications among Gospel descriptions are debated. The six-person answer is therefore a useful default only when the scope is stated.

1. Mary, mother of Jesus.
2. Mary Magdalene.
3. Mary of Bethany, sister of Martha and Lazarus.
4. Mary associated with James/Joses and Clopas/Cleopas in the passion narratives; exact harmonization of the Gospel descriptions should not be overstated.
5. Mary, mother of John Mark (Acts 12:12).
6. Mary greeted by Paul in Rome (Romans 16:6).

## Evidence
- Bible Gateway, Encyclopedia of the Bible, `Mary`: explicitly says six women are mentioned in the NT **assuming the correctness of the identifications** and lists the major identities. https://www.biblegateway.com/resources/encyclopedia-of-the-bible/Mary
- Acts 12:12 independently anchors Mary the mother of John/Mark and her Jerusalem house. https://www.biblegateway.com/verse/en/Acts12%3A12
- Romans 16:6 independently anchors another Mary in Paul's Roman greetings. https://www.biblegateway.com/verse/en/Romans%2016%3A6

## Counter-check / uncertainty
The number is not obtained by merely counting every surface occurrence of `Mary`, because the same woman appears in multiple passages and some Gospel descriptions may or may not refer to the same individual. Therefore Doré must not answer an unqualified `six` as though the scope and harmonization were indisputable.

## Examination gate
1. Does the answer state scope? PASS.
2. Does it distinguish repeated mentions from distinct people? PASS.
3. Does it independently verify Mary mother of John Mark? PASS — Acts 12:12.
4. Does it independently verify Mary in Romans? PASS — Romans 16:6.
5. Does it preserve Gospel-identification uncertainty? PASS.
6. Does it avoid importing OT Miriam into the NT count? PASS.
7. Can the answer survive the adversarial prompt `是不是其實只有三個馬利亞？` by showing independent Acts/Romans identities beyond the famous Gospel Marys? PASS.

Gate: **7/7 PASS**.

## Product decision
Promote a generic `research.nt.mary-count` node as `CONSOLIDATED`, but make the lead conditional: **if you mean distinct New Testament women named Mary, a common identification counts six; the exact harmonization of some Gospel descriptions is debated.**
